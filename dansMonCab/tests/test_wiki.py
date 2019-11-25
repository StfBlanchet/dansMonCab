#! /usr/bin/env python3
# coding: utf-8

"""
dansMonCab chatbot
File that allows to test Wikipedia API.
"""


from dansMonCab.parser import *
import unittest
from unittest.mock import Mock


# Mock requests to control its behavior
requests = Mock()


def get_content():
    r = requests.get('https://some_url/w/api.php')
    if r.status_code == 200:
        return r.json()
    return None


class TestWikiReq(unittest.TestCase):
    def log_request(self, url):
        # Log a fake request for test output purposes
        print(f'Making a request to {url}.')
        print('Request received!')

        # Create a new Mock to imitate a Response
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.json.return_value = {
            'title': 'OpenClassroom',
            'pageid': '4338589',
        }
        return response_mock

    def test_get_wiki_logging(self):
        # Test a successful, logged request
        requests.get.side_effect = self.log_request
        assert get_content()['title'] == 'OpenClassroom'
        assert get_content()['pageid'] == '4338589'


class TestWikiJson(unittest.TestCase):
    def test_json(self):
        json = Mock()
        json.loads({
            'query': {
                'searchinfo': {'totalhits': 1},
                'search': [{'ns': 0,
                            'title': 'Wiki Test',
                            'pageid': 842690,
                            'size': 357159,
                            'wordcount': 78931}]}
        })
        json.loads.assert_called()
        json.loads.assert_called_once()
        json.loads.assert_called_with({
            'query': {
                'searchinfo': {'totalhits': 1},
                'search': [{'ns': 0,
                            'title': 'Wiki Test',
                            'pageid': 842690,
                            'size': 357159,
                            'wordcount': 78931}]}})


d = Driver('openclassroom')


if __name__ == '__main__':
    unittest.main()
