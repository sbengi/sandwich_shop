"""Unit tests for dataclasses"""
from dataclasses import asdict
from pytest import raises

import os
import sys
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..//code//")))

from code.model.data import MenuItem, Order, validate_types


class TestMenuItem:
    """All tests for MenuItem dataclass"""
    def test_menuitem_data(self) -> None:
        """Checks values are assigned to expected keys"""
        item = MenuItem(ItemName="Coronation Chicken",
                        Price=5.99,
                        Vegetarian=0,
                        DairyFree=0)
        assert asdict(item) == {"ItemName": "Coronation Chicken",
                                "Price": 5.99,
                                "Vegetarian": 0,
                                "DairyFree": 0}

    def test_menuitem_datatypes(self) -> None:
        """Checks that wrong datatypes raise TypeError"""
        with raises(TypeError):
            MenuItem(ItemName=1, Price=5.99, Vegetarian=0, DairyFree=0)
            MenuItem(ItemName="Coronation Chicken", Price="not float", Vegetarian=0, DairyFree=0)
            MenuItem(ItemName="Coronation Chicken", Price=5.99, Vegetarian=8, DairyFree=0)

    def test_table_name(self) -> None:
        """Table name return check"""
        assert MenuItem.table_name() == "menu"

    def test_id_column(self) -> None:
        """Id column name return check"""
        assert MenuItem.id_column() == "SandwichID"


class TestOrder:
    """All tests for Order dataclass"""
    def test_order_data(self) -> None:
        """Checks values are assigned to expected keys"""
        item = Order(CustomerName="John Bob",
                     Location="filled.count.soap",
                     Items="[1, 2, 2]",
                     Total=11.70)
        assert asdict(item) == {"CustomerName": "John Bob",
                                "Location": "filled.count.soap",
                                "Items": "[1, 2, 2]",
                                "Total": 11.7}

    def test_menuitem_datatypes(self) -> None:
        """Checks that wrong datatypes raise TypeError"""
        with raises(TypeError):
            Order(CustomerName=1235,
                  Location="filled.count.soap",
                  Items="[1, 2, 2]",
                  Total=11.70)
            Order(CustomerName="John Bob",
                  Location="filled.count.soap",
                  Items=(1, 2, 2),
                  Total=11.70)
            Order(CustomerName="John Bob",
                  Location="filled.count.soap",
                  Items=4,
                  Total=11.70)
            Order(CustomerName="John Bob",
                  Location="filled.count.soap",
                  Items="[1, 2, 2]",
                  Total="11")

    def test_table_name(self) -> None:
        """Table name return check"""
        assert Order.table_name() == "orders"

    def test_id_column(self) -> None:
        """Id column name return check"""
        assert Order.id_column() == "OrderID"


def test_validate_types() -> None:
    """Checks function used to confirm datatypes returns None if correct"""
    item = MenuItem(ItemName="Coronation Chicken",
                    Price=5.99,
                    Vegetarian=0,
                    DairyFree=0)
    assert validate_types(item) is None
