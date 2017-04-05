from time import sleep

import betamax
import os
import pytest
import requests
from unittest.mock import patch

from rasp.engines.base import DefaultEngine
from rasp.webpage import Webpage
from rasp.errors import ControllerError
from rasp.engines.tor_engine import TorEngine, TorController

with betamax.Betamax.configure() as config:
    current_dir = os.path.abspath(os.path.dirname(__file__))
    config.cassette_library_dir = os.path.join(current_dir, 'cassettes')


class TestDefaultEngine(object):
    @patch('rasp.base.DefaultEngine._session')
    def setup(self, req_mock):
        session = requests.session()
        req_mock.return_value = session
        self.session = session
        self.engine = DefaultEngine()

    def test_get_source_empty_url(self):
        with pytest.raises(ValueError):
            self.engine.get_page_source('')

    def test_get_source_valid_url(self):
        with betamax.Betamax(self.session) as vcr:
            vcr.use_cassette('test_get_source_valid_url')
            url = 'http://www.google.com'
            response = self.engine.get_page_source(url)
            assert isinstance(response, Webpage)
            assert isinstance(response.source, str)

    def test_curried_function(self):
        """
        Changes to the state of the Engine instance after currying shouldn't
        affect the parameters of the curried method
        """
        self.engine.headers.update({'X-Test': 'foo'})
        get_source = DefaultEngine.as_func(self.engine, 'get_page_source')
        self.engine.headers.update({'X-Test': 'bar'})
        page = get_source('http://httpbin.org/headers')
        assert '"X-Test": "foo"' in page.source

    def test_webpage_correct_status(self):
        with betamax.Betamax(self.session) as vcr:
            vcr.use_cassette('test_webpage_correct_status')
            url = 'http://google.com/404'
            response = self.engine.get_page_source(url)
            assert response.response_code == 404


class TestTorEngine(object):
    @patch('rasp.base.DefaultEngine._session')
    def setup(self, req_mock):
        session = requests.session()
        req_mock.return_value = session
        self.session = session
        self.engine = TorEngine()

    def test_tor_get_source_valid_url(self):
        with betamax.Betamax(self.session) as vcr:
            vcr.use_cassette('test_tor_get_source_valid_url')
            url = 'http://www.google.com'
            response = self.engine.get_page_source(url)
            assert isinstance(response, Webpage)
            assert isinstance(response.source, str)

    def test_call_limiter_before_limit(self):
        lim_func = TorController.call_limited(2)
        assert not lim_func()

    def test_call_limiter_after_limit(self):
        lim_func = TorController.call_limited(2)
        lim_func()
        assert lim_func()

    def test_time_limiter_before_limit(self):
        lim_func = TorController.time_limited(0.01)
        assert not lim_func()

    def test_time_limiter_after_limit(self):
        lim_func = TorController.time_limited(0.01)
        sleep(0.01)
        assert lim_func()

    def test_controller_connection_enforcement_fails(self):
        ctrl = TorController(password='thang')
        enforced = TorController._enforce_connection(TorController.signal)
        with pytest.raises(ControllerError):
            enforced(ctrl)

    def test_controller_connection_enforcement(self):
        ctrl = TorController(password='thang')

        class ConnMock(object):
            def is_newnym_available(self):
                return True

        ctrl.connection = ConnMock()
        enforced = TorController._enforce_connection(
            TorController.ready_to_signal
        )
        enforced(ctrl)
