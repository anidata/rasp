import urllib
import urllib.error
import urllib.request
import time
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
        self.headers = headers or {'User-Agent': DEFAULT_USER_AGENT}

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
        """The Webpage object represents all we know about a single scraped page.

        The Webpage object is the key object constructed by an engine to represent what we know about a given webpage.
        It includes things like the page source, url, and date of access.

        :param url: the url of the webpage you are representing
        :param source: the source, as text of the webpage.
        :return: Webpage
        """

        self._url = url
        self._source = source
        self._access_date = time.time()

    @property
    def source(self):
        """Source of the webpage, in text.
        """
        return self._source

    @property
    def url(self):
        """Url of the webpage accessed
        """
        return self._url

    @property
    def access_date(self):
        """Date of access of the webpage data, as a unix timestamp in UTC
        """
        return self._access_date

    def __repr__(self):
        return "url: {} at {}".format(self.url, self.access_date)
