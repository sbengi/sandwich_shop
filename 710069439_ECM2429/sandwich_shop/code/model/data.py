"""
Defines dataclasses in line with the database setup\n
Sources:\n
https://docs.python.org/3/library/dataclasses.html\n
https://www.youtube.com/watch?v=CvQ7e6yUtnw
"""

from dataclasses import dataclass, asdict
from typing import get_type_hints


@dataclass
class MenuItem:
    """Creates dataclass instance containing all data for a row in the Menu table in database

    Args:
        ItemName (str): name of sandwich
        Price (float): price in £
        Vegetarian (int): binary value indicator, 1 means yes. Defaults to 0
        DairyFree (int): binary value indicator, 1 means yes. Defaults to 0
    Returns:
        MenuItem(ItemName='', Price=0., Vegetarian=0, DairyFree=0)
    """
    ItemName: str
    Price: float
    Vegetarian: int = 0
    DairyFree: int = 0

    def __post_init__(self):
        validate_types(self)

    @staticmethod
    def table_name() -> str:
        """Gets name of associate table in the database

        Returns:
            str: table name
        """
        return "menu"

    @staticmethod
    def id_column() -> str:
        """Gets name of ID column in database

        Returns:
            str: ID column name
        """
        return "SandwichID"


@dataclass
class Order:
    """Creates dataclass instance containing all data for a row in Orders table in the database

    Args:
        CustomerName (str)
        Location (str): what3words address
        Items (str): string of list of item IDs as found in menu table
        Total (float): total price paid at time of order
    Returns:
        Order(CustomerName='', Location='', Items=[], Total=0.)
    """
    CustomerName: str
    Location: str
    Items: str
    Total: float

    def __post_init__(self):
        validate_types(self)

    @staticmethod
    def table_name() -> str:
        """
        Gets name of associate table in the database

        Returns:
            str: table name
        """
        return "orders"

    @staticmethod
    def id_column() -> str:
        """
        Gets name of ID column in database

        Returns:
            str: ID column name
        """
        return "OrderID"


def validate_types(obj: object) -> None:
    """
    Gets type hints defined in dataclasses to confirm input

    Args:
        obj (dataclass): MenuItem or Order

    Raises:
        TypeError: if incorrect data type input, else None
    """
    types = get_type_hints(obj)
    for k, v in asdict(obj).items():
        if types[k] != type(v):
            raise TypeError("Incorrect data types for input values")
