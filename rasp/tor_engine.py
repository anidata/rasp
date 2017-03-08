import urllib
import urllib.request
import urllib.error
import getpass
import http.client
import time
from stem import Signal
import stem.connection

from rasp.base import Webpage, DefaultEngine


class TorEngine(DefaultEngine):
    def __init__(self, pw=None, control=None, signal=Signal.NEWNYM, proxy_handler=None, data=None, headers=None):

        if pw:
            self.pw = pw
        else:
            self.pw = getpass.getpass("Tor password: ")

        if control is None:
            self.control = ("127.0.0.1", 9051)
        else:
            self.control = control

        if proxy_handler is None:
            self.proxy_handler = urllib.request.ProxyHandler({"http": "127.0.0.1:8118"})
        else:
            self.proxy_handler = proxy_handler

        self.signal = signal
        proxy_opener = urllib.request.build_opener(self.proxy_handler)
        urllib.request.install_opener(proxy_opener)

        super(TorEngine, self).__init__(data, headers)

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
            if url:
                self.send_signal()
                req = urllib.request.Request(url, self.data, self.headers)
                res = urllib.request.urlopen(req)
                if res:
                    try:
                        return Webpage(url, str(res.read()))
                    except http.client.IncompleteRead:
                        return None
                else:
                    return None
            else:
                return None
        except urllib.error.HTTPError as e:
            time.sleep(2)
            return None

