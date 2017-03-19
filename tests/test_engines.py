import os
from unittest.mock import patch

import requests

import betamax
import pytest
from rasp.webpage import Webpage
from rasp import DefaultEngine
from rasp.engines.tor_engine import TorEngine

with betamax.Betamax.configure() as config:
    current_dir = os.path.abspath(os.path.dirname(__file__))
    config.cassette_library_dir = os.path.join(current_dir, 'cassettes')


class TestDefaultEngine:
    @patch('rasp.base.DefaultEngine._session')
    def setup(self, req_mock):
        session = requests.session()
        req_mock.return_value = session
        self.session = session
        self.engine = DefaultEngine()

    def test_default_pull_source_empty_url(self):
        with pytest.raises(ValueError):
            self.engine.get_page_source('')

    def test_default_pull_source_valid_url(self):
        with betamax.Betamax(self.session) as vcr:
            vcr.use_cassette('test_default_pull_source_valid_url')
            url = 'http://www.google.com'
            response = self.engine.get_page_source(url)
            assert isinstance(response, Webpage)
            assert isinstance(response.source, str)

    def test_default_pull_source_not_found(self):
        with betamax.Betamax(self.session) as vcr:
            vcr.use_cassette('test_default_pull_source_not_found')
            url = 'http://google.com/404'
            response = self.engine.get_page_source(url)
            assert response is None


class TestTorEngine:
    @patch('rasp.base.DefaultEngine._session')
    def setup(self, req_mock):
        session = requests.session()
        req_mock.return_value = session
        self.session = session
        self.engine = TorEngine(control_password='raspdefaulttorpass')

    def test_tor_pull_source_valid_url(self):
        with betamax.Betamax(self.session) as vcr:
            vcr.use_cassette('test_tor_pull_source_valid_url')
            url = 'http://www.google.com'
            response = self.engine.get_page_source(url)
            assert isinstance(response, Webpage)
            assert isinstance(response.source, str)
