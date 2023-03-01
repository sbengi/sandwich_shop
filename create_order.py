from tkinter import *
from tkinter import ttk
import what3words

from db_controller import DatabaseController
from data import Order

DEFAULT_FONT = ("OpenSans", 12)
MENU_COLUMNS = ("Item Name", "Price(£)", "Vegetarian", "Dairy Free")
MENU = DatabaseController().display_table("menu")

class CreateOrder():

    db = DatabaseController()

    def __init__(self, db_display, input_frame) -> None:

        # Menu database display
        self.table_name = Label(master=db_display, text="Select items from the menu", font=("Open Sans", 15))
        self.table_name.grid(column=1, row=0, columnspan=3, pady=10, sticky="W")
        table_frame = Frame(master=db_display)
        table_frame.grid(column=1, row=1, columnspan=3, rowspan=10, pady=10, sticky="W")
        
        table_scroll = Scrollbar(table_frame)
        table_scroll.pack(side=RIGHT, fill=Y)

        self.table_view = ttk.Treeview(table_frame, yscrollcommand=table_scroll.set)
        self.table_view["columns"] = MENU_COLUMNS
        self.table_view.column("#0", width=0)
        for i, col in enumerate(MENU_COLUMNS):
            self.table_view.column(col, width=150, anchor=W, minwidth=25)
            self.table_view.heading(col, text=col, anchor=W)
            menu_items = list(MENU[i])
            menu_items = ["Yes" if n == 1 else n for n in 
                          ["No" if e == 0 else e for e in menu_items]][1:]
            if i % 2 == 0:
                self.table_view.insert(parent="", index="end", iid=i, values=menu_items, tags=("even",))
            else:
                self.table_view.insert(parent="", index="end", iid=i, values=menu_items, tags=("odd",))

        table_scroll.config(command=self.table_view.yview)
        self.table_view.tag_configure("odd", background="white")
        self.table_view.tag_configure("even", background="lightyellow")

        style = ttk.Style()
        style.configure("Treeview", font=DEFAULT_FONT)
        style.configure("Treeview.Heading", font=DEFAULT_FONT)
        style.configure("Treeview", rowheight=40)
        self.table_view.pack()

        # data input widgets        
        self.labels = {"CustomerName": {"label": "Customer name:", "type": "entry"},
                "Location": {"label": "Location (lat,long):", "type": "entry"},
                "Items": {"label": "Items in order:", "type": "frame"},
                "Total": {"label": "Total £ ", "type": "label"}}
        
        create = {"entry": lambda: Entry(master=input_frame, width=30, font=DEFAULT_FONT),
                  "label": lambda: Label(master=input_frame, font=DEFAULT_FONT),
                  "text": lambda: Text(master=input_frame, width=34, height=5),
                  "frame": lambda: Frame(master=input_frame, width=200, height=150, bg="white")}
        
        self.widgets = {}
        for key, val in self.labels.items():
            self.widgets[key] = {"label": Label(master=input_frame, text=val["label"], anchor=E, font=DEFAULT_FONT),
                                 "data_widget": create[val["type"]]()}
        row = 2
        for d in self.widgets.values():
            d["label"].grid(column=5, row=row, padx=5, pady=10, ipadx=5, sticky="NW")
            d["data_widget"].grid(column=6, columnspan=3, row=row, padx=5, pady=10, sticky="W")
            row += 1

        # tracking items added
        self.items_added = {} # item name: labels list
        self.row_no = 0
        # create titles for selected items viewer
        self.items_selected(["Item", "Quantity", "Price"], bg_color="lightyellow")
        
        # action buttons
        self.confirm = Button(master=input_frame, text="Confirm order", command=self.confirming, font=DEFAULT_FONT, bg="lightgrey")
        self.confirm.grid(column=6, row=row+1, sticky="SW")
        self.clear = Button(master=input_frame, text="Clear", command=self.clearing, font=DEFAULT_FONT, bg="lightgrey")
        self.clear.grid(column=7, row=row+1, sticky="SW")
        
        self.table_view.bind('<ButtonRelease-1>',self.add_to_order)

    def items_selected(self, name_list:list, bg_color:str="white"):
        frame = self.widgets["Items"]["data_widget"]
        item_quantity_price = []
        for t in name_list:
            item_quantity_price.append(Label(text=t, 
                                            master=frame, 
                                            font=DEFAULT_FONT,
                                            bg=bg_color))
        for i, label in enumerate(item_quantity_price):
            label.grid(column=i, row=self.row_no, ipadx=22, ipady=5, sticky="NSEW")
        
        if bg_color == "white":
            # add plus minus buttons to row
            plus = Button(master=frame, text="+", font=DEFAULT_FONT,
                          command=lambda b=name_list[0]: self.plus_item(b), bg="lightgrey")
            plus.grid(column=3, row=self.row_no, ipadx=5, sticky="W")
            minus = Button(master=frame, text="-", font=DEFAULT_FONT,
                           command=lambda b=name_list[0]: self.minus_item(b), bg="lightgrey")
            # get and save unit price for calculations
            unit_price = self.db.get_value("Price", "menu", name_list[0])
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
    
    def add_to_order(self, event):
        # get selection data
        selected = self.table_view.focus()
        values = self.table_view.item(selected, 'values')
        item = values[0]
        total = float(values[1])

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
        ids = {k:self.db.get_value("SandwichID", "menu", k) for k in self.items_added.keys()}
        item_list = []
        for k, v in self.items_added.items():
            for i in range(int(v[1]["text"])):
                item_list.append(ids[k])
        return str(item_list)

    def save_order(self):
        data_row = [self.widgets["CustomerName"]["data_widget"].get(),
                    self.location_converter(),
                    self.item_list_converter(),
                    float(self.widgets["Total"]["data_widget"]["text"])]

        self.db.set_row(Order(*data_row))
        self.db.insert_new()

    def check_input(self):
        defaults = ((self.widgets["CustomerName"]["data_widget"].get() == "") &
                    (self.widgets["Location"]["data_widget"].get() == "") &
                    (self.widgets["Total"]["data_widget"]["text"] == "") &
                    (len(self.items_added) < 1))
        
        correct = lambda: ((len(self.widgets["CustomerName"]["data_widget"].get().split(" ")) > 1) &
                    (len([float(i) for i in self.widgets["Location"]["data_widget"].get().split(",")]) == 2) &
                    (float(self.widgets["Total"]["data_widget"]["text"]) > 0.) &
                    (len(self.items_added) >= 1))
        try:
            correct()
            return True
        except ValueError or AttributeError:
            invalid = Toplevel()
            invalid.title("Invalid input")
            invalid.geometry("450x150")
            summary = Label(master=invalid, text="Invalid input: Please correct before confirming", font=("Open Sans", 15))
            summary.pack(ipady=10)
            ok = Button(master=invalid, text="Ok", command=invalid.destroy)
            ok.pack()

        
    def confirming(self):
        if self.check_input() is True:
            # save order to db
            self.save_order()
            # confirmation pop-up
            confirm_order = Toplevel()
            confirm_order.title("Order Summary")
            confirm_order.geometry("300x300")

            summary = Label(master=confirm_order, text="Order complete!", font=("Open Sans", 15))
            summary.pack(ipady=10)
            
            ok = Button(master=confirm_order, text="Ok", command=confirm_order.destroy)
            ok.pack()
            # clear inputs
            self.clearing()
        
    def clearing(self):
        self.widgets["CustomerName"]["data_widget"].delete(0, END)
        self.widgets["Location"]["data_widget"].delete(0, END)
        keys = list(self.items_added.keys())
        for b in keys:
            self.delete_order_item(b)
        self.widgets["Total"]["data_widget"].configure(text="")
