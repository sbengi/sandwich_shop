from dataclasses import asdict
from pytest import raises

from .data import MenuItem, Order, validate_types

class TestMenuItem:
    def test_menuitem_data(self):
        item = MenuItem(ItemName="Coronation Chicken",
                        Price=5.99,
                        Vegetarian=0,
                        DairyFree=0)
        assert asdict(item) == {"ItemName": "Coronation Chicken",
                                "Price": 5.99,
                                "Vegetarian": 0,
                                "DairyFree": 0}
    
    def test_menuitem_datatypes(self):
        with raises(TypeError):
            MenuItem(ItemName=1, Price=5.99, Vegetarian=0, DairyFree=0)
            MenuItem(ItemName="Coronation Chicken", Price="not float", Vegetarian=0, DairyFree=0)
            MenuItem(ItemName="Coronation Chicken", Price=5.99, Vegetarian=8, DairyFree=0)

    def test_table_name(self):
        assert MenuItem.table_name() == "menu"

    def test_id_column(self):
        assert MenuItem.id_column() == "SandwichID"


class TestOrder:
    def test_order_data(self):
        item = Order(CustomerName="John Bob",
                        Location="filled.count.soap",
                        Items="[1, 2, 2]",
                        Total=11.70)
        assert asdict(item) == {"CustomerName": "John Bob",
                                "Location": "filled.count.soap",
                                "Items": "[1, 2, 2]",
                                "Total": 11.7}

    def test_menuitem_datatypes(self):
        with raises(TypeError):
            Order(CustomerName=1235, Location="filled.count.soap", Items="[1, 2, 2]", Total=11.70)
            Order(CustomerName="John Bob", Location="filled.count.soap", Items=(1, 2, 2), Total=11.70)
            Order(CustomerName="John Bob", Location="filled.count.soap", Items=4, Total=11.70)
            Order(CustomerName="John Bob", Location="filled.count.soap", Items="[1, 2, 2]", Total="11")
    
    def test_table_name(self):
        assert Order.table_name() == "orders"

    def test_id_column(self):
        assert Order.id_column() == "OrderID"


def test_validate_types():
    item = MenuItem(ItemName="Coronation Chicken",
                        Price=5.99,
                        Vegetarian=0,
                        DairyFree=0)
    assert validate_types(item) is None

