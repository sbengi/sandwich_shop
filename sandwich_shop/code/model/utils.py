"""Module for external what3words api call functions"""
import requests
import os

# get the environment variable api key
api_key = os.environ.get("API_KEY")

def what3words_converter(words: str) -> str:
    """
    Calls api to convert what3words to coordinates

    Args:
        words (str): what3words string

    Returns:
        str: latitude, logitude converted to string
    """
    request_link = "https://api.what3words.com/v3/convert-to-coordinates"
    req = {"words": words, "key": api_key}
    result = requests.get(request_link, params=req)
    result = result.json()["coordinates"]
    lat_long = f"{result['lat']}, {result['lng']}"
    return lat_long


def location_converter(lat_long: str) -> str:
    """
    Calls api to convert latitude, longutude to what3words

    Args:
        lat_long (str): two flaot numbers for coordinates

    Returns:
        str: what3words
    """
    request_link = "https://api.what3words.com/v3/convert-to-3wa"
    query = {"coordinates": lat_long, "key": api_key}
    result = requests.get(request_link, params=query)
    print(result)
    words = result.json()["words"]
    return words
