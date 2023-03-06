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
    connection = connect("sandwich_shop.db")
    cursor = connection.cursor()

    def __init__(self, row:object=None):
        if row is not None:
            self.set_row()

    def set_row(self, row):
        """_summary_

        Args:
            row (object): _description_
        """
        self.row = row
        self.data = row.__dict__
        self.table = row.table_name()

    def create_table(self, new_table_query: str):
        """
        Create new sqlite table

        Args:
            new_table_query (str): SQLite query for creating new table
        """
        self.cursor.execute(new_table_query)
        self.connection.commit()

    def insert_new(self):
        """_summary_
        """
        self.cursor.execute(
            f"INSERT INTO {self.table} {tuple(self.data.keys())} VALUES {tuple(self.data.values())}")
        self.connection.commit()

    def display_table(self, table:str=None):
        """_summary_
        """
        if table is None:
            table = self.table

        self.cursor.execute(f"SELECT * from {table}")
        return self.cursor.fetchall()

    def delete_row(self):
        """
        Delete row from table where ItemName matches
        """
        name = list(self.data.values())[0].replace("'", "")
        self.cursor.execute(
            f"DELETE FROM {self.table} WHERE {list(self.data.keys())[0]} = '{name}'")
        self.connection.commit()

    def update_row(self, row_id):
        """
        _summary_
        """
        query = f"UPDATE {self.table} SET "
        for key, val in self.data.items():
            query += f"{key} = {val}, "
        query = query[:-2] + f" WHERE {self.row.id_column()} = {row_id}"

        self.cursor.execute(query)
        self.connection.commit()

    def find_row(self, table, name):
        self.cursor.execute(f"SELECT* FROM {table} WHERE {list(self.data.keys())[0]} = '{name}'")
        return self.cursor.fetchall()
    
    def get_value(self, value, table, name):
        self.cursor.execute(f"SELECT {value} FROM {table} WHERE {list(self.data.keys())[0]} = '{name}'")
        return list(self.cursor.fetchall()[0])[0]

    @classmethod
    def end_session(cls):
        """
        Commit changes and close connection
        """
        cls.connection.commit()
        cls.connection.close()
