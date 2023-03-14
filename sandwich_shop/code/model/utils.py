"""Module for external api call functions"""
import what3words


def what3words_converter(words: str) -> str:
    """
    Calls api to convert what3words to coordinates

    Args:
        words (str): what3words string

    Returns:
        str: latitude, logitude converted to string
    """
    geocoder = what3words.Geocoder("N1N5YKSR")
    res = geocoder.convert_to_coordinates(words)
    location = f"{res['coordinates']['lat']}, {res['coordinates']['lng']}"
    return location


def location_converter(lat_long: list) -> str:
    """
    Calls api to convert latitude, longutude to what3words

    Args:
        lat_long (list): list with two flaot numbers for coordinates

    Returns:
        str: what3words
    """
    geocoder = what3words.Geocoder("N1N5YKSR")
    res = geocoder.convert_to_3wa(what3words.Coordinates(*lat_long))
    location = res["words"]
    return location
