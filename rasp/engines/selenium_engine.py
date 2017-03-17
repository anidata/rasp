import selenium
import selenium.webdriver

from rasp.webpage import Webpage
from rasp.engines.base import Engine
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
        if not url:
            return EngineError('url needs to be specified')
        self.load_page(url)
        page = Webpage(self.get_url(), self.get_source())
        return page
