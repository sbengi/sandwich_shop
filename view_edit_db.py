from tkinter import *
from tkinter import ttk
from abc import abstractmethod

from db_controller import DatabaseController

class ViewEditDb:
    DEFAULT_FONT = ("OpenSans", 12)
    DB = DatabaseController()

    def __init__(self, db_display:Frame, input_frame:Frame, specs:dict) -> None:
        self.create_db_viewer(db_display, specs["view"])
        self.create_input_widgets(input_frame, specs["input_widgets"])

    def create_db_viewer(self, db_display:Frame, view_specs:dict):
        self.table_name = Label(master=db_display, text=view_specs["table_name"], font=("Open Sans", 15))
        self.table_name.grid(column=1, row=0, columnspan=3, pady=10, sticky="W")
        table_frame = Frame(master=db_display)
        table_frame.grid(column=1, row=1, columnspan=3, rowspan=10, pady=10, sticky="W")
        
        table_scroll = Scrollbar(table_frame)
        table_scroll.pack(side=RIGHT, fill=Y)

        self.table_view = ttk.Treeview(table_frame, yscrollcommand=table_scroll.set)
        self.table_view["columns"] = view_specs["table_view"]["columns"]
        self.table_view.column("#0", width=0)
        for i, col in enumerate(view_specs["table_view"]["columns"]):
            self.table_view.column(col, width=150, anchor=W, minwidth=25)
            self.table_view.heading(col, text=col, anchor=W)
            table_items = list(self.DB.display_table(view_specs["table_view"]["table"])[i])
            table_items = ["Yes" if n == 1 else n for n in 
                          ["No" if e == 0 else e for e in table_items]][1:]
            if i % 2 == 0:
                self.table_view.insert(parent="", index="end", iid=i, values=table_items, tags=("even",))
            else:
                self.table_view.insert(parent="", index="end", iid=i, values=table_items, tags=("odd",))

        table_scroll.config(command=self.table_view.yview)
        self.table_view.tag_configure("odd", background="white")
        self.table_view.tag_configure("even", background="lightyellow")

        style = ttk.Style()
        style.configure("Treeview", font=self.DEFAULT_FONT)
        style.configure("Treeview.Heading", font=self.DEFAULT_FONT)
        style.configure("Treeview", rowheight=40)
        self.table_view.pack()

        # bind row selection from table to abstract action
        self.table_view.bind('<ButtonRelease-1>', self.selected_row_action)

    def create_input_widgets(self, input_frame:Frame, input_specs:dict):    
        create = {"entry": lambda: Entry(master=input_frame, width=30, font=self.DEFAULT_FONT),
                  "label": lambda: Label(master=input_frame, font=self.DEFAULT_FONT),
                  "text": lambda: Text(master=input_frame, width=34, height=5),
                  "frame": lambda: Frame(master=input_frame, width=200, height=150, bg="white"),
                  "check": lambda: Checkbutton(master=input_frame)}
        
        self.labels = input_specs["input"]
        
        self.widgets = {}
        for key, val in self.labels.items():
            self.widgets[key] = {"label": Label(master=input_frame, text=val["label"], anchor=E, font=self.DEFAULT_FONT),
                                 "data_widget": create[val["type"]]()}
        row = 2
        for d in self.widgets.values():
            d["label"].grid(column=5, row=row, padx=5, pady=10, ipadx=5, sticky="NW")
            d["data_widget"].grid(column=6, columnspan=3, row=row, padx=5, pady=10, sticky="W")
            row += 1

        col = 6
        for b in input_specs["buttons"]:
            action = Button(master=input_frame, text=b, command=self.confirming, font=self.DEFAULT_FONT, bg="lightgrey")
            action.grid(column=col, row=row+1, sticky="SW")
            col += 1
        self.clear = Button(master=input_frame, text="Clear selection", command=self.clearing, font=self.DEFAULT_FONT, bg="lightgrey")
        self.clear.grid(column=col, row=row+1, sticky="SW")

    def selected_row_action(self, event):
        selected = self.table_view.focus()
        values = self.table_view.item(selected, 'values')
        self.selection_action(values)
        return values

    def check_input(self):
        try:
            self.correct_input_format()
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
            self.save_to_db()
            # confirmation pop-up
            confirm_order = Toplevel()
            confirm_order.title("Successful")
            confirm_order.geometry("300x300")

            message = Label(master=confirm_order, text="Action complete!", font=("Open Sans", 15))
            message.pack(ipady=10)
            
            ok = Button(master=confirm_order, text="Ok", command=confirm_order.destroy)
            ok.pack()
            # clear inputs
            self.clearing()

    @abstractmethod
    def correct_input_format(self):
        pass
    
    @abstractmethod
    def selection_action(self, values):
        pass

    @abstractmethod
    def save_to_db(self):
        pass

    @abstractmethod
    def clearing(self):
        pass
