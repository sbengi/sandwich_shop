"""
All database manupulation functions
Sources:
https://docs.python.org/3/library/sqlite3.html
https://www.tutorialspoint.com/sqlite/sqlite_python.htm
https://www.geeksforgeeks.org/python-sqlite/
"""

from sqlite3 import connect

new_menu_table = '''CREATE TABLE menu (
    SandwichID INTEGER PRIMARY KEY AUTOINCREMENT,
    ItemName TEXT NOT NULL,
    Price REAL NOT NULL,
    Vegetarian NUMERIC,
    DairyFree NUMERIC)
    '''

new_order_table = '''CREATE TABLE orders (
    OrderID INTEGER PRIMARY KEY AUTOINCREMENT,
    CustomerName TEXT NOT NULL,
    Location TEXT NOT NULL,
    Items TEXT,
    Total REAL)
    '''


class DatabaseController:
    def __init__(self, row: object = None) -> None:
        """
        Class containing all database connection, execution, session functions

        Args:
            row (object, optional): dataclass object like MenuItem or Order. Defaults to None.
        """
        self.start_session()
        if row is not None:
            self.set_row(row)

    def start_session(self):
        self.connection = connect("code//model//sandwich_shop.db")
        self.cursor = self.connection.cursor()

    def set_row(self, row: object) -> None:
        """Takes instance of a dataclass object, parses into dictionary, gets associated table name

        Args:
            row (object): datalcass object MenuItem or Order
        """
        self.row = row
        self.data = row.__dict__
        self.table = row.table_name()
        self.id_col = row.id_column()

    def create_table(self, new_table_query: str) -> None:
        """
        Create new sqlite table

        Args:
            new_table_query (str): SQLite query for creating new table
        """
        self.cursor.execute(new_table_query)
        self.connection.commit()

    def insert_new(self) -> None:
        """
        Parses data dictionary into new row in the relevant table
        """
        self.cursor.execute(
            f"""INSERT INTO {self.table} {
                tuple(self.data.keys())} VALUES {tuple(self.data.values())}""")
        self.connection.commit()

    def display_table(self, table: str = None) -> list:
        """
        Returns all rows in a table based on input or table associated with set data row
        """
        if table is None:
            table = self.table
        self.cursor.execute(f"SELECT * from {table}")
        return self.cursor.fetchall()

    def delete_row(self, row_id: int) -> None:
        """
        Delete row from table where Name column matches

        Args:
            row_id (int): ID number of row to be updated
        """
        self.cursor.execute(
            f"DELETE FROM {self.table} WHERE {self.id_col} = {row_id}")
        self.connection.commit()

    def update_row(self, row_id: int) -> None:
        """
        Updates the row with given id number to data in set data row

        Args:
            row_id (int): ID number of row to be updated
        """
        query = f"UPDATE {self.table} SET "
        for key, val in self.data.items():
            if "Name" in key:
                query += f"{key} = '{val}', "
            else:
                query += f"{key} = {val}, "
        query = query[:-2] + f" WHERE {self.id_col} = {row_id}"

        self.cursor.execute(query)
        self.connection.commit()

    def find_row(self, table: str, name: str) -> list:
        """
        Finds row od data in a given table based on Name column

        Args:
            table (str): name of table to query from
            name (str): name of item to find in the NAme column of the table

        Returns:
            list: list of tuples containing data in each row
        """
        self.cursor.execute(
            f"SELECT* FROM {table} WHERE {list(self.data.keys())[0]} = '{name}'")
        return self.cursor.fetchall()

    def get_value_from_name(self, value: str, table: str, name: str) -> str:
        """
        Finds row of data in given table by item name

        Args:
            value (str): column name to get value from
            table (str): table name
            name (str): name of item

        Returns:
            str|int: value from the specified column of the found row
        """
        self.cursor.execute(
            f"SELECT {value} FROM {table} WHERE {list(self.data.keys())[0]} = '{name}'")
        return list(self.cursor.fetchall()[0])[0]

    def get_value(self, value: str, table: str, col: str, id: int) -> str:
        """
        Finds data in row in given table by ID of the item

        Args:
            value (str): column name to get value from
            table (str): table name
            col (str): name of ID column to use for search
            id (str): ID number of the row

        Returns:
            str: value from the specified column of the found row
        """
        self.cursor.execute(f"SELECT {value} FROM {table} WHERE {col} = {id}")
        return list(self.cursor.fetchall()[0])[0]

    def end_session(self) -> None:
        """
        Commit changes and close connection
        """
        self.connection.commit()
        self.connection.close()
