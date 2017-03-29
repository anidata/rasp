import getpass
import os
from contextlib import contextmanager
from datetime import datetime, timedelta
from stem import Signal
from stem.connection import connect

from rasp.base import DefaultEngine
from rasp.errors import ControllerError


class TorController(object):
    """
    Attributes:
        address (str): IP address of Tor SOCKS proxy to connect,
            can also be set with the ``RASP_TOR_ADDRESS``
            environment variable.
        control_port (int, optional): Port number for control
            port usage to refresh endpoint address,
            can also be set with the ``RASP_TOR_CONTROL_PASSWORD``
            environment variable.
        control_password (str, optional): Password to protect control
            port usage,
            can also be set with the ``RASP_TOR_CONTROL_PORT``
            environment variable.
        callback (callable, optional): A function that returns a boolean value
            to determine when to send a signal to Tor"""

    def __init__(self,
                 address=None,
                 port=None,
                 password=None,
                 signal_limiter=None):
        self.address = (
            address
            or os.environ.get('RASP_TOR_ADDRESS')
            or '127.0.0.1'
        )
        self.port = (
            port
            or os.environ.get('RASP_TOR_CONTROL_PORT')
            or 9051
        )
        self.password = (
            password
            or os.environ.get('RASP_TOR_CONTROL_PASSWORD')
            or getpass.getpass("Tor control password: ")
        )

        def default_limiter(): return True
        self.limiter = (
            signal_limiter or default_limiter
        )

    def __copy__(self):
        return TorController(
            address=self.address,
            port=self.port,
            password=self.password,
            signal_limiter=self.limiter
        )

    def _enforce_connection(method):
        """Method decorator to enforce that the connection was established"""

        def enforce(self, *args, **kwargs):
            if not hasattr(self, 'connection'):
                raise ControllerError(
                    'Signal controller has not been opened'
                )
            return method(self, *args, **kwargs)

        return enforce

    def open(self):
        """Establishes a connection to the Tor server"""
        info = (self.address, self.port)
        self.connection = connect(
            control_port=info,
            password=self.password
        )

    @_enforce_connection
    def close(self):
        """Closes the TorController connection"""
        self.connection.close()

    @_enforce_connection
    def ready_to_signal(self):
        """Checks to see if the Tor server is available to be signalled.

        The availability only applies to the instance's connection, and
        doesn't take into account any other instances.

        Returns:
            True if signal can be sent, False if not
        """
        return self.connection.is_newnym_available()

    @_enforce_connection
    def signal(self):
        """Refreshes the mapping of nodes we connect through.

        When a new path from the user to the destination is required, this
        method refreshes the node path we use to connect. This gives us a new IP
        address with which the destination sees.
        """
        if self.ready_to_signal():
            self.connection.signal(Signal.NEWNYM)

    def limited_signal(self):
        if self.ready_to_signal() and self.limiter():
            self.signal()

    @contextmanager
    def connected(self):
        """Context manager to automatically handle closing the connection"""
        try:
            self.open()
            yield
        finally:
            self.close()

    @staticmethod
    def call_limited(request_amount):
        """Returns a function that returns True when the
            number of calls to it is equal to
            ``request_amount``.

            Parameters:
                request_amount (int): the time to wait before
                the returned function will return True
        """

        def call_limit():
            call_limit.total_calls += 1
            enough_calls = call_limit.total_calls == request_amount
            if enough_calls:
                call_limit.total_calls = 0
                return True
            else:
                return False

        call_limit.total_calls = 0
        return call_limit

    @staticmethod
    def time_limited(time_window_seconds):
        """Returns a function that returns True when the
        elapsed time is greater than ``time_window_seconds``
        from now.

        Parameters:
            time_window_seconds (float): the time to wait before
            the returned function will return True
        """

        def time_limit():
            delta = timedelta(seconds=time_window_seconds)
            out_of_window = time_limit.last_signal <= (datetime.now() - delta)
            if out_of_window:
                time_limit.last_signal = datetime.now()
                return True
            else:
                return False

        time_limit.last_signal = datetime.now()
        return time_limit


class TorEngine(DefaultEngine):
    """Uses ``Tor`` as a socks proxy to route all ``requests`` based calls through.

    This engine provides two functions on top of ``DefaultEngine``:
        1. Route web requests through an anonymous proxy.
        2. Get new endpoint IP address for every request.

    Attributes:
        session (:obj:`requests.Session`): Session object for which all
         requests are routed through.
        headers (dict, optional): Base headers for all requests.
        address (str): IP address of Tor SOCKS proxy to connect,
            can also be set with the ``RASP_TOR_ADDRESS``
            environment variable.
        port (int): Port number of Tor SOCKS proxy for web requests,
            can also be set with the ``RASP_TOR_PORT``
            environment variable.
     """

    def __init__(self,
                 headers=None,
                 pre_fetch_callback=None,
                 address=None,
                 port=None):
        super(TorEngine, self).__init__(headers, pre_fetch_callback)

        self.address = (
            address
            or os.environ.get('RASP_TOR_ADDRESS')
            or '127.0.0.1'
        )
        self.port = (
            port
            or os.environ.get('RASP_TOR_PORT')
            or 9050
        )

        proxy_uri = 'socks5://{}:{}'.format(self.address, self.port)
        proxies = {'http': proxy_uri, 'https': proxy_uri}
        self.session.proxies.update(proxies)

    def __copy__(self):
        return TorEngine(
            self.headers,
            self.callback,
            self.address,
            self.port
        )
