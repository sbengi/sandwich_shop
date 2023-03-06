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
    
    @staticmethod
    def id_column():
        return "SandwichID"


@dataclass
class Order:
    CustomerName: str
    Location: str
    Items: list
    Total: float

    @staticmethod
    def table_name():
        return "orders"
    
    @staticmethod
    def id_column():
        return "OrderID"

