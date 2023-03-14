"""Unit tests for xternal call functions"""
import what3words

from code.model.utils import what3words_converter, location_converter
from .mock_data import mock_location, mock_latlong, mock_latlong_list, mock_words


def mock_api_call(monkeypatch: object):
    """
    Creates a mock for what3words api call coordinate conversion function

    Args:
        monkeypatch (object): mock object
    """
    def mock_convert_to_coordinates(*args):
        return mock_location
    monkeypatch.setattr(what3words,
                        "geocoder.convert_to_coordinates",
                        mock_convert_to_coordinates)


def mock_api_get(monkeypatch: object):
    """
    Creates a mock for what3words api call 3word conversion function

    Args:
        monkeypatch (object): mock object
    """
    def mock_convert_to_3wa(*args):
        return mock_location
    monkeypatch.setattr(what3words,
                        "geocoder.convert_to_3wa",
                        mock_convert_to_3wa)


def test_what3words_converter(monkeypatch):
    """
    Checks converter function returns expected string

    Args:
        monkeypatch (object): mock object
    """
    location = what3words_converter(mock_words)
    assert location == mock_latlong


def test_location_converter(monkeypatch):
    """
    Checks converter function returns expected string

    Args:
        monkeypatch (object): mock object
    """
    location = location_converter(mock_latlong_list)
    assert location == mock_words
