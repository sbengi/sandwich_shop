"""All database manupulation functions"""

from sqlite3 import connect

from data import MenuItem, Order

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
    connection = connect("sandwich_shop.db")
    cursor = connection.cursor()

    def __init__(self, row:object=None)->None:
        """
        Class containing all database connection, execution, session functions

        Args:
            row (object, optional): dataclass object like MenuItem or Order. Defaults to None.
        """
        if row is not None:
            self.set_row()

    def set_row(self, row:MenuItem|Order)->None:
        """Takes instance of a dataclass object, parses into dictionary, gets associated table name

        Args:
            row (object): datalcass object MenuItem or Order
        """
        self.row = row
        self.data = row.__dict__
        self.table = row.table_name()

    def create_table(self, new_table_query:str)->None:
        """
        Create new sqlite table

        Args:
            new_table_query (str): SQLite query for creating new table
        """
        self.cursor.execute(new_table_query)
        self.connection.commit()

    def insert_new(self)->None:
        """
        Parses data dictionary into new row in the relevant table
        """
        self.cursor.execute(
            f"INSERT INTO {self.table} {tuple(self.data.keys())} VALUES {tuple(self.data.values())}")
        self.connection.commit()

    def display_table(self, table:str=None)->None:
        """
        Returns all rows in a table based on input or table associated with set data row
        """
        if table is None:
            table = self.table

        self.cursor.execute(f"SELECT * from {table}")
        return self.cursor.fetchall()

    def delete_row(self)->None:
        """
        Delete row from table where Name column matches
        """
        name = list(self.data.values())[0].replace("'", "")
        self.cursor.execute(
            f"DELETE FROM {self.table} WHERE {list(self.data.keys())[0]} = '{name}'")
        self.connection.commit()

    def update_row(self, row_id:int)->None:
        """
        Updates the row with given id number to data in set data row

        Args:
            row_id (int): ID number of row to be updated
        """
        query = f"UPDATE {self.table} SET "
        for key, val in self.data.items():
            query += f"{key} = {val}, "
        query = query[:-2] + f" WHERE {self.row.id_column()} = {row_id}"

        self.cursor.execute(query)
        self.connection.commit()

    def find_row(self, table:str, name:str)->list:
        """
        Finds row od data in a given table based on Name column

        Args:
            table (str): name of table to query from
            name (str): name of item to find in the NAme column of the table

        Returns:
            list: list of tuples containing data in each row
        """
        self.cursor.execute(f"SELECT* FROM {table} WHERE {list(self.data.keys())[0]} = '{name}'")
        return self.cursor.fetchall()
    
    def get_value_from_name(self, value, table, name)->str:
        self.cursor.execute(f"SELECT {value} FROM {table} WHERE {list(self.data.keys())[0]} = '{name}'")
        return list(self.cursor.fetchall()[0])[0]
    
    def get_value(self, value, table, col, id)->str:
        self.cursor.execute(f"SELECT {value} FROM {table} WHERE {col} = {id}")
        return list(self.cursor.fetchall()[0])[0]

    @classmethod
    def end_session(cls):
        """
        Commit changes and close connection
        """
        cls.connection.commit()
        cls.connection.close()
