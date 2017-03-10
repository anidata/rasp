import getpass
import http.client
import time
import urllib
import urllib.error
import urllib.request

import stem.connection
from stem import Signal

from rasp.base import Webpage, DefaultEngine


class TorEngine(DefaultEngine):
    def __init__(self, pw=None, control=None, signal=Signal.NEWNYM, proxy_handler=None, data=None, headers=None):
        super(TorEngine, self).__init__(data, headers)

        self.signal = signal
        self.pw = pw or getpass.getpass("Tor password: ")
        self.control = control or ("127.0.0.1", 9051)

        default_handler = urllib.request.ProxyHandler({"http": "127.0.0.1:8118"})
        self.proxy_handler = proxy_handler or default_handler

        proxy_opener = urllib.request.build_opener(self.proxy_handler)
        urllib.request.install_opener(proxy_opener)

    def __copy__(self):
        return TorEngine(
            self.pw,
            self.control,
            self.signal,
            self.proxy_handler,
            self.data,
            self.headers
        )

    def send_signal(self):
        conn = stem.connection.connect(
            control_port=self.control,
            password=self.pw
        )
        conn.signal(self.signal)
        conn.close()

    def get_page_source(self, url):
        try:
            self.send_signal()
            req = urllib.request.Request(url, self.data, self.headers)
            res = urllib.request.urlopen(req)

            try:
                return Webpage(url, str(res.read()))
            except http.client.IncompleteRead:
                return
        except urllib.error.HTTPError as e:
            time.sleep(2)
