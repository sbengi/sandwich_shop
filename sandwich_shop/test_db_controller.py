"""Tests for DatabaseController class containing connection and manipulation of the sqlite3 database"""

import pytest
import sqlite3
from sqlite3 import OperationalError
from unittest.mock import MagicMock

from .db_controller import DatabaseController
from .mock_data import mock_row, mock_create_query, MockData


class TestDatabaseController:
    
    @pytest.fixture
    def mock_db(self) -> object:
        """
        Sets up all mock values used for all tests in this module

        Returns:
            object: DatabaseController with mock sqlite3 connection and data row
        """
        # mock sqlite3 database
        self.mock_connection = MagicMock(spec=sqlite3.Connection)
        self.mock_cursor = MagicMock(spec=sqlite3.Cursor)
        self.mock_cursor.fetchall.return_value = [(1, "mock", 5),]
        # assign mock values to my class
        dbc = DatabaseController(mock_row)
        dbc.connection = self.mock_connection
        dbc.cursor = self.mock_cursor
        
        return dbc

    def test_set_row(self, mock_db: object) -> None:
        """
        Tests all attributes are set correctly

        Args:
            mock_db (object): pytest fixture containing mocked DatabaseController
        """
        mock_db.set_row(mock_row)
        assert mock_db.row == MockData(MockName="mock", MockAmount=5)
        assert mock_db.data == {"MockName": "mock", "MockAmount": 5}
        assert mock_db.table == "TestTable"

    def test_start_session(self, mock_db: object) -> None:
        """
        Tests connection and cursor are set to mock as expected

        Args:
            mock_db (object): pytest fixture
        """
        assert isinstance(mock_db.connection, sqlite3.Connection)
        assert isinstance(mock_db.cursor, sqlite3.Cursor)

    def test_create_table(self, mock_db: object) -> None:
        """
        Checks if table is created and committed

        Args:
            mock_db (object): pytest fixture
        """
        try:
            mock_db.create_table(mock_create_query)
            self.mock_cursor.execute.assert_called_once_with(mock_create_query)
        except AssertionError:
            with pytest.raises(OperationalError):
                mock_db.create_table(mock_create_query)

    def test_insert_new(self, mock_db: object) -> None:
        """
        Checks if insert new row query is constructed and run correctly

        Args:
            mock_db (object): pytest fixture
        """
        mock_db.table = "TestTable"
        mock_db.data = {"MockName": "'mock'", "MockAmount": 5}
        insert_query = 'INSERT INTO TestTable (\'MockName\', \'MockAmount\') VALUES ("\'mock\'", 5)'
        mock_db.insert_new()
        #self.mock_connection.commit.assert_called_once()
        self.mock_cursor.execute.assert_called_once_with(insert_query)

    def test_display_table(self, mock_db: object) -> list:
        """
        Checks if fetchall query is constructed and run correctly

        Args:
            mock_db (object): pytest fixture
        """
        mock_db.table = "TestTable"
        mock_db.cursor.execute('INSERT INTO TestTable (\'MockName\', \'MockAmount\') VALUES ("\'insert\'", 8)')
        mock_db.connection.commit()
        result = mock_db.display_table()
        assert "mock" in [list(r)[1] for r in result]
        assert 5 in [list(r)[2] for r in result]
        assert isinstance(result, list)

    def test_update_row(self, mock_db: object) -> None:
        mock_db.set_row(MockData("'Updated'", 4))
        query = "UPDATE TestTable SET MockName = 'Updated', MockAmount = 4 WHERE MockID = 1"
        mock_db.update_row(1)
        mock_db.cursor.execute.assert_called_once_with(query)

    def test_find_row(self, mock_db: object) -> None:
        result = mock_db.find_row("TestTable", "'mock'")
        mock_db.connection.commit.assert_not_called()
        assert isinstance(result, list)
        assert len(result) > 0

    def test_get_value_from_name(self, mock_db: object) -> None:
        mock_db.cursor.execute('INSERT INTO TestTable (MockName, MockAmount) VALUES ("insert", 8)')
        result = mock_db.get_value_from_name("MockName", "TestTable", "'insert'")
        mock_db.cursor.execute.assert_called()
        mock_db.connection.commit.assert_not_called()

    def test_get_value(self, mock_db: object) -> None:
        result = mock_db.get_value("MockName", "TestTable", "MockID", 1)
        mock_db.cursor.execute.assert_called_once()
        mock_db.connection.commit.assert_not_called()

    def test_delete_row(self, mock_db: object) -> None:
        """Checks delete query is constructed and executed correctly

        Args:
            mock_db (object): _description_
        """
        mock_db.table = "TestTable"
        mock_db.data = {"MockName": "'insert'", "MockAmount": 8}
        query = "DELETE FROM TestTable WHERE MockName = 'insert'"
        mock_db.delete_row()
        self.mock_cursor.execute.assert_called_once_with(query)      

    def test_end_session(self, mock_db: object) -> None:
        """
        Checks that commit and close commands were run

        Args:
            mock_db (object): pytest fixture
        """
        mock_db.end_session()
        mock_db.connection.commit.assert_called_once()
        mock_db.connection.close.assert_called_once()