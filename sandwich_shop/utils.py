"""Module for all external calls"""

import what3words


def what3words_converter(words: str) -> str:
    geocoder = what3words.Geocoder("N1N5YKSR")
    res = geocoder.convert_to_coordinates(words)
    location = f"{res['coordinates']['lat']}, {res['coordinates']['lng']}"
    return location

def location_converter(lat_long: list) -> str:
    geocoder = what3words.Geocoder("N1N5YKSR")
    res = geocoder.convert_to_3wa(what3words.Coordinates(*lat_long))
    location = res["words"]
    return location
