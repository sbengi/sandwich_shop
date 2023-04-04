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

mock_latlong = "51.520847, -0.195521"
mock_latlong_response = {"coordinates": {"lat": 51.520847, "lng": -0.195521}}
mock_words = "filled.count.soap"
mock_words_response = {"words": "filled.count.soap"}
