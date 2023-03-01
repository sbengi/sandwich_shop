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
        self.cursor.execute(f"INSERT INTO {self.table} {tuple(self.data.keys())} VALUES {tuple(self.data.values())}")
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
        self.cursor.execute(f"DELETE FROM {self.table} WHERE ItemName = '{self.row.ItemName}'")
        self.connection.commit()

    def update_row(self):
        """
        _summary_
        """
        query = f"UPDATE {self.table} SET "
        for key, val in self.data.items():
            query += f"{key} = {val},"
        query = query[:-1] + f" WHERE ItemName is {self.row.ItemName}"
        
        self.cursor.execute(query)
        self.connection.commit()

    def find_row(self, table, name):
        self.cursor.execute(f"SELECT* FROM {table} WHERE ItemName = '{name}'")
        return self.cursor.fetchall()
    
    def get_value(self, value, table, name):
        self.cursor.execute(f"SELECT {value} FROM {table} WHERE ItemName = '{name}'")
        return list(self.cursor.fetchall()[0])[0]


    @classmethod
    def end_session(cls):
        """
        Commit changes and close connection
        """
        cls.connection.commit()
        cls.connection.close()


if __name__ == "__main__":
    hi = DatabaseController()

    from data import MenuItem, Order
    menu_items = [('Turkey Club', 7.99, 0, 1),
    ('Grilled Cheese', 4.99, 1, 0),
    ('Cheese Steak', 8.99, 0, 0),
    ('Falafel Wrap', 6.99, 1, 1),
    ('Reuben', 9.99, 0, 1)]

    #for itm in menu_items:
    #    i = MenuItem(*itm)
    #    hi.set_row(i)
    #    hi.insert_new()
    print(hi.display_table("orders"))
