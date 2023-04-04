"""
Unit tests for xternal call functions\n
Sources:\n
https://docs.pytest.org/en/latest/how-to/monkeypatch.html\n
https://pytest-with-eric.com/pytest-best-practices/pytest-monkeypatch/
"""
import requests

from code.model import utils
from mock_data import mock_latlong, mock_latlong_response, mock_words, mock_words_response


def test_what3words_converter(monkeypatch):
    """
    Creates a monkeypatch for requests from the what3words api,
    tests what3words_converter returns expected response

    Args:
        monkeypatch (function): mock patch for what3words HTTP request
    """
    def mock_get(*args, **kwargs):
        class MockResponse:
            def __init__(self, response, response_code):
                self.response = response
                self.response_code = response_code

            def json(self):
                return self.response

        if "convert-to-coordinates" in args[0]:
            return MockResponse(mock_latlong_response, 200)
        else:
            return MockResponse(None, 404)
    monkeypatch.setattr(requests, "get", mock_get)

    assert utils.what3words_converter(mock_words) == mock_latlong


def test_location_converter(monkeypatch):
    """
    Creates a monkeypatch for requests from the what3words api,
    tests location_converter returns expected response

    Args:
        monkeypatch (function): mock patch for what3words HTTP request
    """
    def mock_get(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data

        if "convert-to-3wa" in args[0]:
            return MockResponse(mock_words_response, 200)
        else:
            return MockResponse(None, 404)
    monkeypatch.setattr(requests, "get", mock_get)

    assert utils.location_converter(mock_latlong) == mock_words
