import unittest

from rasp import DefaultEngine


class test_DefaultEngine(unittest.TestCase):
    def test_pull_source(self):
        eng = DefaultEngine()
        response = eng.get_page_source('http://www.google.com')
        self.assertIsNotNone(response.source)
        self.assertIsNotNone(response.url)
