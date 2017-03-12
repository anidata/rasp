import getpass
import os

from stem import Signal
from stem.control import Controller

from rasp.base import DefaultEngine


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
        control_port (int, optional): Port number for control
            port usage to refresh endpoint address,
            can also be set with the ``RASP_TOR_CONTROL_PASSWORD``
            environment variable.
        control_password (str, optional): Password to protect control
            port usage,
            can also be set with the ``RASP_TOR_CONTROL_PORT``
            environment variable.
     """
    def __init__(self,
                 headers=None,
                 address=None,
                 port=None,
                 control_port=None,
                 control_password=None):
        super(TorEngine, self).__init__(headers)

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
        self.control_password = (
            control_password
            or os.environ.get('RASP_TOR_CONTROL_PASSWORD')
            or getpass.getpass("Tor control password: ")
        )
        self.control_port = (
            control_port
            or os.environ.get('RASP_TOR_CONTROL_PORT')
            or 9051
        )

        proxy_uri = 'socks5://{}:{}'.format(self.address, self.port)
        proxies = {'http': proxy_uri, 'https': proxy_uri}
        self.session.proxies.update(proxies)

    def __copy__(self):
        return TorEngine(
            self.data,
            self.headers,
            self.address,
            self.port,
            self.control_port,
            self.control_password,
        )

    def clean_circuits(self):
        """Refreshes the mapping of nodes we connect through.

        When a new path from the user to the destination is required, this
        method refreshes the node path we use to connect. This gives us a new IP
        address with which the destination sees."""
        kwargs = {'address': self.address, 'port': self.control_port}
        with Controller.from_port(**kwargs) as controller:
            controller.authenticate(password=self.control_password)
            controller.signal(Signal.NEWNYM)

    def get_page_source(self, url, params=None,
                        headers=None, clean_circuits=True):
        """Fetches the specified url.

        Attributes:
            url (str): The url of which to fetch the page source code.
            params (dict, optional): Key\:Value pairs to be converted to
                x-www-form-urlencoded url parameters_.
            headers (dict, optional): Extra headers to be merged into
                base headers for current Engine before requesting url.
            clean_circuits (bool, optional): Determines whether or not
                we want to get a new IP with which to connect ``url``.
        Returns:
            ``rasp.base.Webpage`` if successful, ``None`` if not

        .. _parameters: http://docs.python-requests.org/en/master/user/quickstart/#passing-parameters-in-urls
        """
        if clean_circuits:
            self.clean_circuits()
        return super(TorEngine, self).get_page_source(url, params=params, headers=headers)
