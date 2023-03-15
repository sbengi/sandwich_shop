"""Widgets and functionality for editing recorded orders"""
from tkinter import Frame

from .create_order import CreateOrder
from model.data import MenuItem, Order
from model.utils import what3words_converter, location_converter
from model.db_controller import DatabaseController


class EditOrder(CreateOrder):
    ORDER_COLUMNS = ("Customer Name", "Location", "Items", "Total(£)")
    SPECS = {
            "view": {
                "table_name": "Select order to edit",
                "table_view": {"columns": ORDER_COLUMNS,
                               "table": "orders"}},
            "input_widgets": {
                    "input": {
                            "CustomerName": {"label": "Customer name:",
                                             "type": "entry"},
                            "Location": {"label": "Location (lat,long):",
                                         "type": "entry"},
                            "Items": {"label": "Items in order:",
                                      "type": "frame"},
                            "Total": {"label": "Total £ (when ordered): ",
                                      "type": "label"}},
                    "buttons": ["Update", "Delete record"]
                        }}

    def __init__(self, db_display: Frame, input_frame: Frame) -> None:
        """
        Overwrites init with specs for edit order interface

        Args:
            db_display (Frame): database viewer frame
            input_frame (Frame): input widgets frame
        """
        self.DB = DatabaseController()
        self.db_display = db_display
        self.input_frame = input_frame
        self.create_db_viewer(db_display, EditOrder.SPECS["view"])
        self.create_input_widgets(input_frame, EditOrder.SPECS["input_widgets"])

        # tracking items added
        self.items_added = {}  # item name: labels list
        self.row_no = 0
        # create titles for selected items viewer
        self.items_selected(["Item", "Quantity", "Price"], bg_color="lightyellow")
        # bind delete button to relevant function
        self.widgets["Delete record"].configure(command=self.delete_record)

    def selection_action(self, values: list) -> None:
        """
        Maps values to widgets, re-creates ordered items list

        Args:
            values (list): row of selected data
        """
        self.clearing()
        self.widgets["CustomerName"]["data_widget"].insert(0, values[0])
        lat_long = what3words_converter(values[1])
        self.widgets["Location"]["data_widget"].insert(0, lat_long)
        # map values to variables
        item = values[2].split(", ")
        total = float(values[3])
        # update widgets
        for itm in item:
            i_list = [t.strip() for t in itm.replace("}", "").split("{")[1:]]
            for i in i_list:
                if i in self.items_added.keys():
                    # set quantity
                    quantity = int(self.items_added[i][1]["text"])+1
                    self.items_added[i][1].configure(text=quantity)
                    # set price
                    self.DB.set_row(MenuItem("", 0., 0, 0))
                    unit_price = self.items_added[i][-1]
                    self.items_added[i][2].configure(text=round(unit_price*quantity, 2))
                else:
                    self.items_selected([i, 1, total])
        self.update_total(total, "+")

    def id_list_converter(self, items: list) -> list:
        """
        Conversts list of item ids to names for display

        Args:
            items (list): _description_

        Returns:
            list: list of names of ordered items
        """
        names = [self.DB.get_value("ItemName", "menu", "SandwichID", int(i)) for i in items]
        return names

    def alter_table_data(self, table_data: tuple | list) -> tuple:
        """
        Alters Treeview to show item names rather than ids

        Args:
            table_data (tuple | list): orders table data fetched from database

        Returns:
            tuple: all data with items lsit converted to item names list
        """
        alter = [list(data) for data in list(table_data)]
        for data in alter:
            items = eval(data[3])
            data[3] = self.id_list_converter(items)
        return tuple(alter)

    def set_data_row(self) -> object:
        """
        Maps data in input widgets to Order dataclass

        Returns:
            object: Order dataclass
        """
        lat_long = self.widgets["Location"]["data_widget"].get()
        data_row = [self.widgets['CustomerName']['data_widget'].get(),
                    location_converter(lat_long),
                    self.item_list_converter(),
                    float(self.widgets["Total"]["data_widget"]["text"])]
        return Order(*data_row)

    def set_for_save(self):
        lat_long = [float(i) for i in self.widgets["Location"]["data_widget"].get().split(",")]
        data_row = [f"{self.widgets['CustomerName']['data_widget'].get()}",
                    f"'{location_converter(lat_long)}'",
                    f"'{self.item_list_converter()}'",
                    float(self.widgets["Total"]["data_widget"]["text"])]
        return Order(*data_row)

    def save_to_db(self) -> None:
        """
        Updates data or saves to database, updates database viewer
        """
        data_row = self.set_for_save()
        self.DB.set_row(data_row)
        # update record instead of saving new if record exists
        try:
            self.update_existing(data_row)
        except IndexError:
            self.invalid_popup()
        self.clear_recreate()
