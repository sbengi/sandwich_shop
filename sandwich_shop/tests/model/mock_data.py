"""Objects and values used for mock patching unit tests"""
from dataclasses import dataclass


@dataclass
class MockData:
    MockName: str
    MockAmount: int

    @staticmethod
    def table_name() -> str:
        return "TestTable"

    @staticmethod
    def id_column() -> str:
        return "MockID"


mock_row = MockData("mock", 5)

mock_create_query = '''CREATE TABLE TestTable (
    MockID INTEGER PRIMARY KEY AUTOINCREMENT,
    MockName TEXT NOT NULL,
    MockAmount NUMERIC NOT NULL)
    '''

# example taken from https://developer.what3words.com/public-api/docs#convert-to-3wa
mock_location = {
    "country": "GB",
    "square": {
        "southwest": {
            "lng": -0.195543,
            "lat": 51.520833
        },
        "northeast": {
            "lng": -0.195499,
            "lat": 51.52086
        }
    },
    "nearestPlace": "Bayswater, London",
    "coordinates": {
        "lng": -0.195521,
        "lat": 51.520847
    },
    "words": "filled.count.soap",
    "language": "en",
    "map": "https://w3w.co/filled.count.soap"
    }

mock_latlong = "51.520847, -0.195521"
mock_latlong_list = [float(i) for i in mock_latlong.split(",")]
mock_words = "filled.count.soap"
