from tkinter import *

from view_edit import ViewEdit
from data import MenuItem

class EditMenu(ViewEdit):
    MENU_COLUMNS = ("Item Name", "Price(£)", "Vegetarian", "Dairy Free")
    SPECS = {
            "view": {
                "table_name": "Select menu item to edit",
                "table_view": {"columns": MENU_COLUMNS,
                            "table": "menu"}},
            "input_widgets": {"input": {"ItemName": {"label": "Item Name:", "type": "entry"},
                                        "Price": {"label": "Price £:", "type": "entry"},
                                        "Vegetarian": {"label": "Vegetarian:", "type": "checkbox"},
                                        "DairyFree": {"label": "DairyFree:", "type": "checkbox"}},
                              "buttons": ["Add/Update", "Delete record"]}
                              }

    def __init__(self, db_display, input_frame) -> None:
        super().__init__(db_display, input_frame, EditMenu.SPECS)

        self.widgets["Delete record"].configure(command=self.delete_record)

    def custom_widgets(self, row):
        self.vegi = IntVar()
        self.vegi.set(0)
        self.ndairy = IntVar()
        self.ndairy.set(0)
        self.widgets["Vegetarian"]["check"] = Checkbutton(master=self.input_frame, variable=self.vegi)
        self.widgets["Vegetarian"]["check"].grid(column=6, row=row-2, padx=5, pady=10, ipadx=5, sticky="NW")
        self.widgets["DairyFree"]["check"] = Checkbutton(master=self.input_frame, variable=self.ndairy)
        self.widgets["DairyFree"]["check"].grid(column=6, row=row-1, padx=5, pady=10, ipadx=5, sticky="NW")

    def correct_input_format(self):
        # define function for checking correct format of input values
        return ((len(self.widgets["ItemName"]["data_widget"].get().split(" ")) > 1) &
            (float(self.widgets["Price"]["data_widget"].get()) > 0.))
    
    def selection_action(self, values):
        # map values to widgets
        self.widgets["ItemName"]["data_widget"].delete(0, END)
        self.widgets["Price"]["data_widget"].delete(0, END)
        self.widgets["ItemName"]["data_widget"].insert(0, values[0])
        self.widgets["Price"]["data_widget"].insert(0, values[1])
        self.vegi.set(1) if values[2] == "Yes" else self.vegi.set(0)
        self.ndairy.set(1) if values[3] == "Yes" else self.ndairy.set(0)

    def update_existing(self, data_row):
        row_id = self.DB.get_value(
            data_row.id_column(), data_row.table_name(), list(data_row.__dict__.values())[0].replace("'", ""))
        self.DB.update_row(row_id)

    def save_to_db(self):
        data_row = self.set_data_row()
        self.DB.set_row(data_row)
        # update record instead of saving new if record exists
        try:
            self.update_existing(data_row)
        except IndexError:
            self.DB.insert_new()
        self.clear_recreate()

    def set_data_row(self):
        data_row = [f"'{self.widgets['ItemName']['data_widget'].get()}'",
                    float(self.widgets["Price"]["data_widget"].get()),
                    self.vegi.get(),
                    self.ndairy.get()
                    ]
        return MenuItem(*data_row)

    def delete_record(self):
        data_row = self.set_data_row()
        self.DB.set_row(data_row)
        try:
            self.DB.delete_row()
            self.create_db_viewer(self.db_display, self.view_specs)
        except IndexError:
            pass
        
    def clearing(self):
        self.widgets["ItemName"]["data_widget"].delete(0, END)
        self.widgets["Price"]["data_widget"].delete(0, END)
        self.vegi.set(0)
        self.ndairy.set(0)