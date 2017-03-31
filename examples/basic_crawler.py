from rasp import DefaultEngine, DefaultBoundedCrawler
import time


def example_callback(wp):
    print(wp.url)

if __name__ == '__main__':
    data = ('https://www.google.com?q=%s' % _ for _ in range(10))
    engine = DefaultEngine()
    start_time = time.time()
    crawler = DefaultBoundedCrawler(engine, data, callback=example_callback)
    crawler.run()
    end_time = time.time()
    print('%s elapsed' % (end_time - start_time, ))