from tkinter import *

from view_edit_db import ViewEditDb
from data import MenuItem

class EditMenu(ViewEditDb):
    MENU_COLUMNS = ("Item Name", "Price(£)", "Vegetarian", "Dairy Free")
    SPECS = {
            "view": {
                "table_name": "Select menu item to edit",
                "table_view": {"columns": MENU_COLUMNS,
                            "table": "menu"}},
            "input_widgets": {"input": {"ItemName": {"label": "Item Name:", "type": "entry"},
                                        "Price": {"label": "Price £:", "type": "entry"},
                                        "Vegetarian": {"label": "Vegetarian:", "type": "check"},
                                        "DairyFree": {"label": "DairyFree:", "type": "check"}},
                              "buttons": ["Add/Update", "Delete"]}
                              }

    def __init__(self, db_display, input_frame) -> None:
        super().__init__(db_display, input_frame, EditMenu.SPECS)

    def correct_input_format(self):
        # define function for checking correct format of input values
        return ((len(self.widgets["ItemName"]["data_widget"].get().split(" ")) > 1) &
            (float(self.widgets["Price"]["data_widget"]["text"]) > 0.))
    
    def selection_action(self, values):
        # map values to widgets
        self.widgets["ItemName"]["data_widget"].delete(0, END)
        self.widgets["Price"]["data_widget"].delete(0, END)
        self.widgets["ItemName"]["data_widget"].insert(0, values[0])
        self.widgets["Price"]["data_widget"].insert(0, values[1])
        self.widgets["Vegetarian"]["data_widget"].select() if values[2] == "Yes" else self.widgets["Vegetarian"]["data_widget"].deselect()
        self.widgets["DairyFree"]["data_widget"].select() if values[3] == "Yes" else self.widgets["DairyFree"]["data_widget"].deselect()

    def save_to_db(self):
        data_row = [self.widgets["ItemName"]["data_widget"]["text"],
                    float(self.widgets["Price"]["data_widget"]["text"]),
                    self.widgets["Vegetarian"]["data_widget"].get(),
                    self.widgets["DairyFree"]["data_widget"].get()
                    ]

        self.DB.set_row(MenuItem(*data_row))
        self.DB.insert_new()
        
    def clearing(self):
        self.widgets["ItemName"]["data_widget"].delete(0, END)
        self.widgets["Price"]["data_widget"].delete(0, END)
        self.widgets["Vegetarian"]["data_widget"].deselect()
        self.widgets["DairyFree"]["data_widget"].deselect()