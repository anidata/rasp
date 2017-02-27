import urllib
import urllib.error
import urllib.request

from rasp.constants import DEFAULT_USER_AGENT
from rasp.errors import EngineError


class Engine(object):
    def get_page_source(self, url):
        raise EngineError("get_page_source not implemented")

    def cleanup(self):
        return

    def clone(self):
        raise EngineError("clone not implemented")


class DefaultEngine(Engine):
    def __init__(self, data=None, headers=None):
        self.data = data

        if headers is None:
            self.headers = {'User-Agent': DEFAULT_USER_AGENT}
        else:
            self.headers = headers

        return

    def get_page_source(self, url):
        try:
            if url:
                req = urllib.request.Request(url, self.data, self.headers)
                return Webpage(url, str(urllib.request.urlopen(req).read()))
            else:
                return None
        except urllib.error.HTTPError as e:
            return None

    def clone(self):
        return DefaultEngine(self.data, self.headers)


class Webpage(object):
    def __init__(self, url=None, source=None):
        self.url = url
        self.source = source
        return

    def set_source(self, source):
        self.source = source
        return

    def set_url(self, url):
        self.url = url
        return

    def __repr__(self):
        return "url: %s" % self.url