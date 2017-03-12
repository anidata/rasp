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

    def get_page_source(self, url, params=None, headers=None):
        """Fetches the specified url.

        Attributes:
            url (str): The url of which to fetch the page source code.
            params (dict, optional): Key\:Value pairs to be converted to
                x-www-form-urlencoded url parameters_.
            headers (dict, optional): Extra headers to be merged into
                base headers for current Engine before requesting url.
        Returns:
                    ``rasp.base.Webpage`` if successful, ``None`` if not

        .. _parameters: http://docs.python-requests.org/en/master/user/quickstart/#passing-parameters-in-urls
        """
        if not url:
            raise ValueError('url needs to be specified')
        if isinstance(headers, dict):
            temp = headers
            headers = deepcopy(self.headers)
            headers.update(temp)
        response = self.session.get(
            url, params=params, headers=headers
        )
        if response.status_code is not requests.codes.ok:
            return
        return Webpage(url, source=str(response.content))


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
