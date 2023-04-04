"""User interface and functionality for editing Menu saved in the database"""

from tkinter import *

from .gui_base import GuiBase
from model.data import MenuItem


class EditMenu(GuiBase):
    MENU_COLUMNS = ("Item Name", "Price(£)", "Vegetarian", "Dairy Free")
    SPECS = {
            "view": {
                "table_name": "Select menu item to edit",
                "table_view": {"columns": MENU_COLUMNS,
                               "table": "menu"}},
                "input_widgets": {
                            "input": {
                                "ItemName": {"label": "Item Name:",
                                             "type": "entry"},
                                "Price": {"label": "Price £:",
                                          "type": "entry"},
                                "Vegetarian": {"label": "Vegetarian:",
                                               "type": "checkbox"},
                                "DairyFree": {"label": "DairyFree:",
                                              "type": "checkbox"}
                                            },
                            "buttons": ["Add/Update", "Delete record"]
                            }}

    def __init__(self, db_display: Frame, input_frame: Frame) -> None:
        """
        Uses GuiBase base class initiation, assigns specific function to delete button

        Args:
            db_display (Frame): database displaye frame
            input_frame (Frame): input widgets and buttons frame
        """
        super().__init__(db_display, input_frame, EditMenu.SPECS)
        self.widgets["Delete record"].configure(command=self.delete_record)

    def custom_widgets(self, row: int) -> None:
        """
        Adds custom widgets to those defined in base class GuiBase

        Args:
            row (int): row number for placement in UI grid
        """
        self.vegi = IntVar()
        self.vegi.set(0)
        self.ndairy = IntVar()
        self.ndairy.set(0)
        self.widgets["Vegetarian"]["check"] = Checkbutton(master=self.input_frame,
                                                          variable=self.vegi)
        self.widgets["Vegetarian"]["check"].grid(column=6,
                                                 row=row-2,
                                                 padx=5,
                                                 pady=10,
                                                 ipadx=5,
                                                 sticky="NW")
        self.widgets["DairyFree"]["check"] = Checkbutton(master=self.input_frame,
                                                         variable=self.ndairy)
        self.widgets["DairyFree"]["check"].grid(column=6, row=row-1,
                                                padx=5,
                                                pady=10,
                                                ipadx=5,
                                                sticky="NW")

    def correct_input_format(self) -> None:
        """Checks correct format of input values

        Returns:
            bool: True if all formats are correct, else False
        """
        return ((len(self.widgets["ItemName"]["data_widget"].get().split(" ")) > 1) &
                all([s.isalpha() for s
                     in self.widgets["ItemName"]["data_widget"].get().split(" ")]) &
                (float(self.widgets["Price"]["data_widget"].get()) > 0.))

    def selection_action(self, values: list) -> None:
        """
        Parses selected row in table view to populate in input widgets

        Args:
            values (list): values from the selected row
        """
        self.widgets["ItemName"]["data_widget"].delete(0, END)
        self.widgets["Price"]["data_widget"].delete(0, END)
        self.widgets["ItemName"]["data_widget"].insert(0, values[1])
        self.widgets["Price"]["data_widget"].insert(0, values[2])
        self.vegi.set(1) if values[3] == "Yes" else self.vegi.set(0)
        self.ndairy.set(1) if values[4] == "Yes" else self.ndairy.set(0)
        self.selected_id = int(values[0])

    def set_data_row(self) -> None:
        """Turns input data into dataclass if datatypes are as expected

        Returns:
            MenuItem: dataclass from input values
        """
        data_row = [self.widgets['ItemName']['data_widget'].get(),
                    float(self.widgets["Price"]["data_widget"].get()),
                    self.vegi.get(),
                    self.ndairy.get()
                    ]
        try:
            return MenuItem(*data_row)
        except ValueError or TypeError:
            self.invalid_popup()

    def save_to_db(self):
        super().save_to_db(self.selected_id)

    def clearing(self) -> None:
        """
        Sets input widgets to empty values
        """
        self.widgets["ItemName"]["data_widget"].delete(0, END)
        self.widgets["Price"]["data_widget"].delete(0, END)
        self.vegi.set(0)
        self.ndairy.set(0)
