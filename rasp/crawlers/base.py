from rasp.engines.base import DefaultEngine
import time

__author__ = 'willmcginnis'


class DefaultBoundedCrawler:
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


def example_callback(wp):
    print('...')

if __name__ == '__main__':
    data = ('https://www.google.com?q=%s' % _ for _ in range(10))
    engine = DefaultEngine()
    start_time = time.time()
    crawler = DefaultBoundedCrawler(engine, data, callback=example_callback)
    crawler.run()
    end_time = time.time()
    print('%s elapsed' % (end_time - start_time, ))