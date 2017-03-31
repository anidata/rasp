import datetime
import time

__author__ = 'willmcginnis'


class Webpage(object):
    def __init__(self, url=None, source=None, headers=None, response_code=None):
        """The Webpage object represents all we know about a single scraped page.

        The Webpage object is the key object constructed by an engine to represent what we know about a given webpage.
        It includes things like the page source, url, and date of access.

        Attributes:
            url (str): The url of the webpage you are representing
            source (str): The source, as text of the webpage
            headers (dict): The headers of the response
            response_code (int): The `HTTP code`_ of the response
        Returns:
            ``rasp.base.Webpage``

        .. _HTTP code: http://www.restapitutorial.com/httpstatuscodes.html
        """

        self._url = url
        self._source = source
        self._access_timestamp = time.time()
        self.headers = headers
        self.response_code = response_code

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