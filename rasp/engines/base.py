from copy import deepcopy

import requests

from rasp.constants import DEFAULT_USER_AGENT
from rasp.webpage import Webpage


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
    def as_func(cls, method_name):
        """Curries the specified function with the current state of the Engine

        Attributes:
            cls (Engine): An Engine class instance
            method_name (str): The name of the method to be curried

        Example:
            engine = DefaultEngine()
            c = DefaultEngine.as_func(engine, 'get_page_source')
            c('http://google.com')

        Returns:
            User-defined function, if successful
        """
        TmpEngine = deepcopy(cls)

        class_name = TmpEngine.__class__.__name__
        try:
            return getattr(TmpEngine, method_name)
        except AttributeError:
            raise NotImplementedError('Class {} does not implement {}'.format(class_name, method_name))

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


