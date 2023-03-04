from tkinter import *

from view_edit_db import ViewEditDb
from data import Order

class EditOrder(ViewEditDb):
    ORDER_COLUMNS = ("Item Name", "Price(£)", "Vegetarian", "Dairy Free")
    SPECS = {
            "view": {
                "table_name": "Select order to edit",
                "table_view": {"columns": ORDER_COLUMNS,
                            "table": "menu"}},
            "input_widgets": {"input": {"ItemName": {"label": "Item Name:", "type": "entry"},
                                        "Price": {"label": "Price £:", "type": "entry"},
                                        "Vegetarian": {"label": "Vegetarian:", "type": "check"},
                                        "DairyFree": {"label": "DairyFree:", "type": "check"}},
                              "buttons": ["Add/Update", "Delete"]}
                              }

    def __init__(self, db_display, input_frame) -> None:
        super().__init__(db_display, input_frame, EditOrder.SPECS)