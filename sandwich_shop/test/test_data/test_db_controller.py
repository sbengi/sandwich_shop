import unittest
import sqlite3
from your_module import MenuItem, Order, DatabaseController

import unittest
from unittest.mock import MagicMock
from your_module import MenuItem, Order, YourClass

class TestYourClass(unittest.TestCase):

    def setUp(self):
        self.your_class = YourClass()

    def test_set_row_with_menu_item(self):
        menu_item = MenuItem(name="Cheeseburger", price=9.99)
        menu_item.table_name = MagicMock(return_value="menu_items")
        self.your_class.set_row(menu_item)
        self.assertEqual(self.your_class.row, menu_item)
        self.assertEqual(self.your_class.data, {"name": "Cheeseburger", "price": 9.99})
        self.assertEqual(self.your_class.table, "menu_items")

    def test_set_row_with_order(self):
        order = Order(table_number=4, items=["Cheeseburger", "Fries"])
        order.table_name = MagicMock(return_value="orders")
        self.your_class.set_row(order)
        self.assertEqual(self.your_class.row, order)
        self.assertEqual(self.your_class.data, {"table_number": 4, "items": ["Cheeseburger", "Fries"]})
        self.assertEqual(self.your_class.table, "orders")

class TestDatabaseController(unittest.TestCase):

    def setUp(self):
        self.database = DatabaseController()

    def tearDown(self):
        self.database.cursor.execute("DROP TABLE IF EXISTS menu_items")
        self.database.cursor.execute("DROP TABLE IF EXISTS orders")

    def test_create_table(self):
        new_table_query = "CREATE TABLE menu_items (name TEXT, price REAL)"
        self.database.create_table(new_table_query)
        self.database.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = self.database.cursor.fetchall()
        self.assertIn(('menu_items',), tables)

    def test_set_row_with_menu_item(self):
        menu_item = MenuItem(name="Cheeseburger", price=9.99)
        menu_item.table_name = lambda: "menu_items"
        self.database.set_row(menu_item)
        self.assertEqual(self.database.row, menu_item)
        self.assertEqual(self.database.data, {"name": "Cheeseburger", "price": 9.99})
        self.assertEqual(self.database.table, "menu_items")

    def test_insert_new_with_menu_item(self):
        new_table_query = "CREATE TABLE menu_items (name TEXT, price REAL)"
        self.database.create_table(new_table_query)
        menu_item = MenuItem(name="Cheeseburger", price=9.99)
        menu_item.table_name = lambda: "menu_items"
        self.database.set_row(menu_item)
        self.database.insert_new()
        result = self.database.display_table()
        self.assertIn(('Cheeseburger', 9.99), result)

    def test_set_row_with_order(self):
        order = Order(table_number=4, items=["Cheeseburger", "Fries"])
        order.table_name = lambda: "orders"
        self.database.set_row(order)
        self.assertEqual(self.database.row, order)
        self.assertEqual(self.database.data, {"table_number": 4, "items": ["Cheeseburger", "Fries"]})
        self.assertEqual(self.database.table, "orders")

    def test_insert_new_with_order(self):
        new_table_query = "CREATE TABLE orders (table_number INTEGER, items TEXT)"
        self.database.create_table(new_table_query)
        order = Order(table_number=4, items=["Cheeseburger", "Fries"])
        order.table_name = lambda: "orders"
        self.database.set_row(order)
        self.database.insert_new()
        result = self.database.display_table()
        self.assertIn((4, "['Cheeseburger', 'Fries']"), result)
