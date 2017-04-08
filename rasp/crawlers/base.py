class BaseBoundedCrawler(object):
    def run(self):
        raise NotImplemented("run not implemented for {}"
                             .format(str(self.__class__.__name__)))


class DefaultBoundedCrawler(BaseBoundedCrawler):
    def __init__(self, engine, urls, callback):
        self._engine = engine
        self._data = urls
        self._callback = callback

    def _process(self, url):
        wp = self._engine.get_page_source(url)
        self._callback(wp)

    def run(self):
        for url in self._data:
            self._process(url)