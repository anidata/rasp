from time import sleep

import betamax
import os
import pytest
import requests
from unittest.mock import patch
from rasp.webpage import Webpage
from rasp.engines.base import DefaultEngine
from rasp.crawlers.base import DefaultBoundedCrawler

with betamax.Betamax.configure() as config:
    current_dir = os.path.abspath(os.path.dirname(__file__))
    config.cassette_library_dir = os.path.join(current_dir, 'cassettes')

class TestDefaultBoundedCrawler(object):
    @patch('rasp.engines.base.DefaultEngine._session')
    def setup(self, req_mock):
        session = requests.session()
        req_mock.return_value = session
        self.session = session
        self.engine = DefaultEngine()
        self._count = 0

    def example_callback(self, response):
        assert isinstance(response, Webpage)
        assert isinstance(response.source, str)
        self._count += 1

    def test_basic_crawl(self):
        with betamax.Betamax(self.session) as vcr:
            vcr.use_cassette('test_default_crawl')
            data = ('https://www.google.com' for _ in range(10))
            engine = DefaultEngine()
            crawler = DefaultBoundedCrawler(engine, data, callback=self.example_callback)
            crawler.run()

            assert self._count == 10
