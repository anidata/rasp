import getpass
import os

from stem import Signal
from stem.control import Controller

from rasp.base import DefaultEngine


class TorEngine(DefaultEngine):
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
        kwargs = {'address': self.address, 'port': self.control_port}
        with Controller.from_port(**kwargs) as controller:
            controller.authenticate(password=self.control_password)
            controller.signal(Signal.NEWNYM)

    def get_page_source(self, url, params=None, clean_circuits=True):
        if clean_circuits:
            self.clean_circuits()
        return super(TorEngine, self).get_page_source(url)
