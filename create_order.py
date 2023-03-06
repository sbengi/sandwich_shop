from tkinter import *
import what3words

from view_edit import ViewEdit
from data import Order, MenuItem

class CreateOrder(ViewEdit):
    MENU_COLUMNS = ("Item Name", "Price(£)", "Vegetarian", "Dairy Free")
    SPECS = {
            "view": {
                "table_name": "Select items from the menu",
                "table_view": {"columns": MENU_COLUMNS,
                            "table": "menu"}},
            "input_widgets": {"input": {"CustomerName": {"label": "Customer name:", "type": "entry"},
                                "Location": {"label": "Location (lat,long):", "type": "entry"},
                                "Items": {"label": "Items in order:", "type": "frame"},
                                "Total": {"label": "Total £ ", "type": "label"}},
                              "buttons": ["Confirm order"]}
                              }

    def __init__(self, db_display, input_frame) -> None:
        super().__init__(db_display, input_frame, CreateOrder.SPECS)

        
        # tracking items added
        self.items_added = {} # item name: labels list
        self.row_no = 0
        # create titles for selected items viewer
        self.items_selected(["Item", "Quantity", "Price"], bg_color="lightyellow")
        
    def correct_input_format(self):
        # define function for checking correct format of input values
        return ((len(self.widgets["CustomerName"]["data_widget"].get().split(" ")) > 1) &
            (len([float(i) for i in self.widgets["Location"]["data_widget"].get().split(",")]) == 2) &
            (float(self.widgets["Total"]["data_widget"]["text"]) > 0.) &
            (len(self.items_added) >= 1))

    def items_selected(self, name_list:list, bg_color:str="white"):
        frame = self.widgets["Items"]["data_widget"]
        item_quantity_price = []
        for t in name_list:
            item_quantity_price.append(Label(text=t, 
                                            master=frame, 
                                            font=self.DEFAULT_FONT,
                                            bg=bg_color))
        for i, label in enumerate(item_quantity_price):
            label.grid(column=i, row=self.row_no, ipadx=22, ipady=5, sticky="NSEW")
        
        if bg_color == "white":
            # add plus minus buttons to row
            plus = Button(master=frame, text="+", font=self.DEFAULT_FONT,
                          command=lambda b=name_list[0]: self.plus_item(b), bg="lightgrey")
            plus.grid(column=3, row=self.row_no, ipadx=5, sticky="W")
            minus = Button(master=frame, text="-", font=self.DEFAULT_FONT,
                           command=lambda b=name_list[0]: self.minus_item(b), bg="lightgrey")
            # get and save unit price for calculations
            self.DB.set_row(MenuItem("", 0. , 0, 0))
            unit_price = self.DB.get_value("Price", "menu", name_list[0])
            # update dict of added items and labels 
            self.items_added[name_list[0]] = item_quantity_price + [plus, minus, unit_price]
            minus.grid(column=4, row=self.row_no, ipadx=5, sticky="E")
        self.row_no += 1

    def plus_item(self, b_name):
        quantity = int(self.items_added[b_name][1]["text"])
        unit_price = self.items_added[b_name][-1]
        self.items_added[b_name][1].configure(text=quantity+1)
        self.items_added[b_name][2].configure(text=round(float(unit_price*(quantity+1)),2))
        self.update_total(unit_price, "+")

    def minus_item(self, b_name):
        quantity = int(self.items_added[b_name][1]["text"])
        unit_price = self.items_added[b_name][-1]
        if quantity > 1:
            self.items_added[b_name][1].configure(text=quantity-1)
            self.items_added[b_name][2].configure(text=round(float(unit_price*(quantity-1)),2))
        else:
            self.delete_order_item(b_name)
        self.update_total(unit_price, "-")
        
    def delete_order_item(self, b_name):
        for wdg in self.items_added[b_name][:-1]:
            wdg.destroy()
            wdg.pack_forget()
        del self.items_added[b_name]
    
    def selection_action(self, values):
        # map values to variables
        item = values[0]
        total = float(values[1])
        # update widgets
        if item in self.items_added.keys():
            quantity=int(self.items_added[item][1]["text"])+1
            self.items_added[item][1].configure(text=quantity)
            self.items_added[item][2].configure(text=round(total*quantity, 2))
        else:
            self.items_selected([item, 1, total])
        self.update_total(total, "+")

    def update_total(self, value:float, operation:str="+"):
        old_total = self.widgets["Total"]["data_widget"]["text"]
        operate = {"+": lambda x: round(old_total + x, 2),
                   "-": lambda x: round(old_total - x, 2)}
        if old_total != "":
            old_total = float(old_total)
            value = operate[operation](value)
        self.widgets["Total"]["data_widget"].configure(text=value)

    def location_converter(self):
        geocoder = what3words.Geocoder("N1N5YKSR")
        lat_long = [float(i) for i in self.widgets["Location"]["data_widget"].get().split(",")]
        res = geocoder.convert_to_3wa(what3words.Coordinates(*lat_long))
        location = res["words"]
        return location
    
    def item_list_converter(self):
        ids = {k:self.DB.get_value("SandwichID", "menu", k) for k in self.items_added.keys()}
        item_list = []
        for k, v in self.items_added.items():
            for i in range(int(v[1]["text"])):
                item_list.append(ids[k])
        return str(item_list)

    def save_to_db(self):
        data_row = [self.widgets["CustomerName"]["data_widget"].get(),
                    self.location_converter(),
                    self.item_list_converter(),
                    float(self.widgets["Total"]["data_widget"]["text"])]

        self.DB.set_row(Order(*data_row))
        self.DB.insert_new()
        
    def clearing(self):
        self.widgets["CustomerName"]["data_widget"].delete(0, END)
        self.widgets["Location"]["data_widget"].delete(0, END)
        keys = list(self.items_added.keys())
        for b in keys:
            self.delete_order_item(b)
        self.widgets["Total"]["data_widget"].configure(text="")
