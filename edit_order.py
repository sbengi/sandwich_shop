from tkinter import *

from view_edit import ViewEdit
from data import Order

class EditOrder(ViewEdit):
    ORDER_COLUMNS = ("Customer Name", "Location", "Items", "Total(£)")
    SPECS = {
            "view": {
                "table_name": "Select order to edit",
                "table_view": {"columns": ORDER_COLUMNS,
                            "table": "orders"}},
            "input_widgets": {"input": {"CustomerName": {"label": "Item Name:", "type": "entry"},
                                        "Location": {"label": "Price £:", "type": "entry"},
                                        "Items": {"label": "Vegetarian:", "type": "label"},
                                        "Total(£)": {"label": "DairyFree:", "type": "label"}},
                              "buttons": ["Update", "Delete record"]}
                              }

    def __init__(self, db_display, input_frame) -> None:
        super().__init__(db_display, input_frame, EditOrder.SPECS)
