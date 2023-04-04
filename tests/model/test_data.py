"""Unit tests for dataclasses"""
from dataclasses import asdict
from pytest import raises

from code.model import data


class TestMenuItem:
    """All tests for MenuItem dataclass"""
    def test_menuitem_data(self) -> None:
        """Checks values are assigned to expected keys"""
        item = data.MenuItem(ItemName="Coronation Chicken",
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
            data.MenuItem(ItemName=1, Price=5.99, Vegetarian=0, DairyFree=0)
            data.MenuItem(ItemName="Coronation Chicken", Price="not float",
                          Vegetarian=0, DairyFree=0)
            data.MenuItem(ItemName="Coronation Chicken", Price=5.99,
                          Vegetarian=8, DairyFree=0)

    def test_table_name(self) -> None:
        """Table name return check"""
        assert data.MenuItem.table_name() == "menu"

    def test_id_column(self) -> None:
        """Id column name return check"""
        assert data.MenuItem.id_column() == "SandwichID"


class TestOrder:
    """All tests for Order dataclass"""
    def test_order_data(self) -> None:
        """Checks values are assigned to expected keys"""
        item = data.Order(CustomerName="John Bob",
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
            data.Order(CustomerName=1235,
                       Location="filled.count.soap",
                       Items="[1, 2, 2]",
                       Total=11.70)
            data.Order(CustomerName="John Bob",
                       Location="filled.count.soap",
                       Items=(1, 2, 2),
                       Total=11.70)
            data.Order(CustomerName="John Bob",
                       Location="filled.count.soap",
                       Items=4,
                       Total=11.70)
            data.Order(CustomerName="John Bob",
                       Location="filled.count.soap",
                       Items="[1, 2, 2]",
                       Total="11")

    def test_table_name(self) -> None:
        """Table name return check"""
        assert data.Order.table_name() == "orders"

    def test_id_column(self) -> None:
        """Id column name return check"""
        assert data.Order.id_column() == "OrderID"


def test_validate_types() -> None:
    """Checks function used to confirm datatypes returns None if correct"""
    item = data.MenuItem(ItemName="Coronation Chicken",
                         Price=5.99,
                         Vegetarian=0,
                         DairyFree=0)
    assert data.validate_types(item) is None
