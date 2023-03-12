from dataclasses import dataclass

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
    Vegetarian:int = 0
    DairyFree:int = 0

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
        Items (list): list of item IDs as found in menu table
        Total (float): total price paid at time of order
    Returns:
        Order(CustomerName='', Location='', Items=[], Total=0.)
    """
    CustomerName: str
    Location: str
    Items: list
    Total: float

    @staticmethod
    def table_name()->str:
        """Gets name of associate table in the database

        Returns:
            str: table name
        """
        return "orders"
    
    @staticmethod
    def id_column()->str:
        """Gets name of ID column in database

        Returns:
            str: ID column name
        """
        return "OrderID"

