import datetime
import time
from copy import deepcopy

import requests

from rasp.constants import DEFAULT_USER_AGENT


class Engine(object):
    def get_page_source(self, url):
        raise NotImplemented("get_page_source not implemented for {}"
                             .format(str(self.__class__.__name__)))

    def cleanup(self):
        return


class DefaultEngine(Engine):
    """The parent class for all ``requests`` based engines.

    Attributes:
        session (:obj:`requests.Session`): Session object for which all
            requests are routed through.
        headers (dict): Base headers for all requests.
    """

    def __init__(self, headers=None):
        self.session = self._session()
        self.headers = headers or {'User-Agent': DEFAULT_USER_AGENT}
        self.session.headers.update(self.headers)

    def __copy__(self):
        return DefaultEngine(self.headers)

    def _session(self, *args, **kwargs):
        """Internal Session object creator.

        Note:
            This method exists to accommodate injecting a
            mock Session object during testing runtime.

        Returns:
            ``requests.Session``
        """
        return requests.session(*args, **kwargs)

    @staticmethod
    def as_func(cls, func_name):
        """Curries the specified function

        Attributes:
            cls (DefaultEngine): An instance of the DefaultEngine class or subclass
            func_name (str): The name of the method to be curried

        Example:
            engine = DefaultEngine()
            c = DefaultEngine.as_func(engine, 'get_page_source')
            c('http://google.com')

        Returns:
            User-defined class method, if successful
        """
        TmpEngine = deepcopy(cls)

        class_name = TmpEngine.__class__.__name__
        try:
            return getattr(TmpEngine, func_name)
        except AttributeError:
            raise NotImplementedError('Class {} does not implement {}'.format(class_name, func_name))

    def get_page_source(self, url, params=None, headers=None):
        """Fetches the specified url.

        Attributes:
            url (str): The url of which to fetch the page source code.
            params (dict, optional): Key\:Value pairs to be converted to
                x-www-form-urlencoded url parameters_.
            headers (dict, optional): Extra headers to be merged into
                base headers for current Engine before requesting url.
        Returns:
            ``rasp.base.Webpage`` if successful

        .. _parameters: http://docs.python-requests.org/en/master/user/quickstart/#passing-parameters-in-urls
        """
        if not url:
            raise ValueError('url needs to be specified')

        merged_headers = deepcopy(self.headers)
        if isinstance(headers, dict):
            merged_headers.update(headers)

        response = self.session.get(
            url, params=params, headers=merged_headers
        )
        return Webpage(
            url,
            source=response.text,
            headers=response.headers,
            response_code=response.status_code
        )


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
