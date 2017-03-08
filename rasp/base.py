import urllib
import urllib.error
import urllib.request

from rasp.constants import DEFAULT_USER_AGENT
from rasp.errors import EngineError


class Engine(object):
    def get_page_source(self, url):
        raise NotImplemented("get_page_source not implemented for {}"
                             .format(str(self.__class__.__name__)))

    def cleanup(self):
        return

class DefaultEngine(Engine):
    def __init__(self, data=None, headers=None):
        self.data = data

        if headers is None:
            self.headers = {'User-Agent': DEFAULT_USER_AGENT}
        else:
            self.headers = headers

    def __copy__(self):
        return DefaultEngine(self.data, self.headers)

    def get_page_source(self, url, data=None):
        if not url:
            return EngineError('url needs to be specified')
        data = self.data or data
        try:
            req = urllib.request.Request(url, data, self.headers)
            source = str(urllib.request.urlopen(req).read())
            return Webpage(url, source)
        except urllib.error.HTTPError as e:
            return


class Webpage(object):
    def __init__(self, url=None, source=None):
        self.url = url
        self.source = source

    def set_source(self, source):
        self.source = source

    def set_url(self, url):
        self.url = url

    def __repr__(self):
        return "url: {}".format(self.url)
