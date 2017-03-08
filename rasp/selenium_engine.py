import selenium
import selenium.webdriver
import time

from rasp.base import Engine, Webpage
from rasp.errors import EngineError


class BaseSeleniumEngine(Engine):
    def __init__(self, *args, **kwargs):
        self.driver = selenium.webdriver.Firefox()

    def get_source(self):
        return str(self.driver.page_source)

    def cleanup(self):
        self.driver.quit()

    def load_page(self, url):
        self.driver.get(url)

    def get_url(self):
        return self.driver.current_url


class SeleniumEngine(BaseSeleniumEngine):
    def get_page_source(self, url):
class TimedWaitEngine(BaseSeleniumEngine):
    def __init__(self, delay, parent=None):
        super(TimedWaitEngine, self).__init__()
        self.delay = delay
        if not parent:
            raise EngineError("Selenium Decorator must wrap a Selenium Engine object")
        self.parent = parent
        return

    def get_page_source(self, url):
        if url:
            self.parent.get_page_source(url)
            time.sleep(self.delay)
            return Webpage(
                    self.parent.get_url(),
                    self.parent.get_source()
                    )
        else:
            return None

    def cleanup(self):
        self.parent.cleanup()
        return

    def clone(self):
        return TimedWaitEngine(self.delay, self.parent.clone())

    def get_source(self):
        return self.parent.get_source()

    def get_url(self):
        return self.parent.get_url()        if not url:
            return EngineError('url needs to be specified')
        self.load_page(url)
        page = Webpage(self.get_url(), self.get_source())
        return page