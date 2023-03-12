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
    

