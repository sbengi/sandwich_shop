from dataclasses import dataclass

@dataclass
class MenuItem:
    ItemName: str
    Price: float
    Vegetarian:int = 0
    DairyFree:int = 0

    @staticmethod
    def table_name():
        return "menu"


@dataclass
class Order:
    CustomerName: str
    Location: str
    Items: list
    Total: float

    @staticmethod
    def table_name():
        return "orders"

