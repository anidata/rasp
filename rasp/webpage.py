import datetime
import time


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
        self._access_timestamp = time.time()

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
    def access_timestamp(self):
        """Date of access of the webpage data, as a unix timestamp in UTC
        """
        return self._access_timestamp

    @property
    def access_datetime(self):
        """Date of access of the webpage data, as a datetime object
        """
        return datetime.datetime.utcfromtimestamp(self.access_timestamp)

    @access_datetime.setter
    def access_datetime(self, access_datetime):
        self._access_timestamp = access_datetime.timestamp()

    def __repr__(self):
        return "url: {} at {}".format(self.url, self.access_datetime.strftime('%Y-%m-%d %H:%M:%S'))
