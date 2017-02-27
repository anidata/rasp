import selenium
import selenium.webdriver
import time

from rasp.base import Engine, Webpage
from rasp.errors import EngineError


class BaseSeleniumEngine(Engine):
    def __init__(self):
        self.driver = None
        return

    def get_source(self):
        return str(self.driver.page_source)

    def cleanup(self):
        self.driver.quit()
        return

    def setup(self):
        self.driver = selenium.webdriver.Firefox()
        return

    def load_page(self, url):
        self.driver.get(url)
        return

    def get_url(self):
        return self.driver.current_url

    def clone(self):
        return BaseSeleniumEngine()


class SeleniumEngine(BaseSeleniumEngine):
    def __init__(self):
        super(SeleniumEngine, self).__init__()
        super(SeleniumEngine, self).setup()
        return

    def get_page_source(self, url):
        if url:
            super(SeleniumEngine, self).load_page(url)
            return Webpage(
                    super(SeleniumEngine, self).get_url(),
                    super(SeleniumEngine, self).get_source()
                    )
        else:
            return None

    def cleanup(self):
        super(SeleniumEngine, self).cleanup()
        return

    def clone(self):
        return SeleniumEngine()


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
        return self.parent.get_url()