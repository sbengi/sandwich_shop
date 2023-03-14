"""Base class for view, edit, create user interfaces and functionalities"""

from tkinter import *
from tkinter import ttk
from abc import abstractmethod
from sqlite3 import OperationalError

from code.model.db_controller import DatabaseController


class ViewEdit:
    DEFAULT_FONT = ("OpenSans", 12)

    def __init__(self, db_display: Frame, input_frame: Frame, specs: dict) -> None:
        """
        Creates database displayer, editor widgets, action buttons from given specs

        Args:
            db_display (Frame): Tkinter frame for the database display table
            input_frame (Frame): Tkinter frame for all input widgets and buttons
            specs (dict): SAMPLE_SPECS = {
                "view": {"table_name": "",
                        "table_view": {"columns": (),
                                        "table": ""}},
                "input_widgets": {"input": {"Column1": {"label": "", "type": ""},
                                            "Column2": {"label": "", "type": ""},
                "buttons": []}}
        """
        self.DB = DatabaseController()
        self.db_display = db_display
        self.input_frame = input_frame
        self.create_db_viewer(db_display, specs["view"])
        self.create_input_widgets(input_frame, specs["input_widgets"])

    def create_db_viewer(self, db_display: Frame, view_specs: dict) -> None:
        """
        Creates Treeview table for viewing database tables

        Args:
            db_display (Frame)
            view_specs (dict): SAMPLE_SPECS["view"] view related configurations
        """
        self.view_specs = view_specs
        self.table_name = Label(master=db_display,
                                text=view_specs["table_name"],
                                font=("Open Sans", 15))
        self.table_name.grid(column=1, row=0, columnspan=3, pady=10, sticky="W")
        table_frame = Frame(master=db_display)
        table_frame.grid(column=1, row=1, columnspan=3, rowspan=10, pady=10, sticky="W")

        table_scroll = Scrollbar(table_frame)
        table_scroll.pack(side=RIGHT, fill=Y)
        table_xscroll = Scrollbar(table_frame, orient="horizontal")
        table_xscroll.pack(side=BOTTOM, fill=X)

        self.table_view = ttk.Treeview(table_frame, yscrollcommand=table_scroll.set,
                                       xscrollcommand=table_xscroll.set)
        self.table_view["columns"] = view_specs["table_view"]["columns"]
        self.table_view.column("#0", width=0)
        table_data = self.DB.display_table(view_specs["table_view"]["table"])
        table_data = self.alter_table_data(table_data)
        for col in view_specs["table_view"]["columns"]:
            self.table_view.column(col, width=150, anchor=W, minwidth=25)
            self.table_view.heading(col, text=col, anchor=W)
        for i, data in enumerate(table_data):
            table_items = list(data)
            table_items = ["Yes" if n == 1 else n for n in
                           ["No" if e == 0 else e for e in table_items]][1:]
            if i % 2 == 0:
                self.table_view.insert(parent="",
                                       index="end",
                                       iid=i,
                                       values=table_items,
                                       tags=("even",))
            else:
                self.table_view.insert(parent="",
                                       index="end",
                                       iid=i,
                                       values=table_items,
                                       tags=("odd",))

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

    def create_input_widgets(self, input_frame: Frame, input_specs: dict) -> None:
        """
        Creates all input widgets

        Args:
            input_frame (Frame)
            input_specs (dict): SAMPLE_SPECS["input_widgets"] widget related configurations
        """
        self.input_specs = input_specs
        create = {"entry": lambda: Entry(master=input_frame, width=30, font=self.DEFAULT_FONT),
                  "label": lambda: Label(master=input_frame, font=self.DEFAULT_FONT),
                  "text": lambda: Text(master=input_frame, width=34, height=5),
                  "frame": lambda: Frame(master=input_frame, width=200, height=150, bg="white")}

        self.labels = input_specs["input"]

        self.widgets = {}
        for key, val in self.labels.items():
            self.widgets[key] = {
                "label": Label(master=input_frame,
                               text=val["label"],
                               anchor=E,
                               font=self.DEFAULT_FONT),
                "data_widget": Label() if val["type"] == "checkbox" else create[val["type"]]()}
        row = 2
        for d in self.widgets.values():
            d["label"].grid(column=5, row=row, padx=5, pady=10, ipadx=5, sticky="NW")
            d["data_widget"].grid(column=6, columnspan=3, row=row, padx=5, pady=10, sticky="W")
            row += 1

        self.custom_widgets(row)

        col = 6
        for b in input_specs["buttons"]:
            action = Button(master=input_frame,
                            text=b,
                            command=self.confirming,
                            font=self.DEFAULT_FONT,
                            bg="lightgrey")
            action.grid(column=col, row=row+1, sticky="SW")
            self.widgets[b] = action
            col += 1
        self.clear = Button(master=input_frame,
                            text="Clear selection",
                            command=self.clearing,
                            font=self.DEFAULT_FONT,
                            bg="lightgrey")
        self.clear.grid(column=col, row=row+1, sticky="SW")

    def selected_row_action(self, event) -> list:
        """
        Gets values of the selected row in Treeview, processes custom to each child class

        Args:
            event (click): listens for click on any row

        Returns:
            list: values of data in the seleced row
        """
        selected = self.table_view.focus()
        values = self.table_view.item(selected, 'values')
        self.selection_action(values)
        return values

    def check_input(self) -> bool | None:
        """Checks correct input format as implemented by each child class

        Returns:
            bool|None: True if all input values are in expected format and datatype, else False
        """
        try:
            return self.correct_input_format()
        except ValueError or AttributeError:
            self.invalid_popup()

    def invalid_popup(self) -> None:
        """
        Creates pop-up message box indicating invalid input
        """
        invalid = Toplevel()
        invalid.title("Invalid input")
        invalid.geometry("450x150")
        summary = Label(master=invalid,
                        text="Invalid input: Please correct before confirming",
                        font=("Open Sans", 15))
        summary.pack(ipady=10)
        ok = Button(master=invalid, text="Ok", command=invalid.destroy)
        ok.pack()

    def confirming(self) -> None:
        """
        Saves to database, creates pop-up message confirming completion
        for correctly formatted input, clears all input widgets.
        """
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
        else:
            self.invalid_popup()

    def clear_recreate(self) -> None:
        """
        Destroys database viewer and recreates it so that any changes are reflected
        """
        for widget in self.db_display.winfo_children():
            widget.destroy()
        self.DB.end_session()
        self.DB = DatabaseController()
        self.create_db_viewer(self.db_display, self.view_specs)

    def update_existing(self, data_row: object) -> None:
        """Updates existing record in the database by name

        Args:
            data_row (dataclass): MenuItem or Order
        """
        row_id = self.DB.get_value_from_name(
            data_row.id_column(), data_row.table_name(), list(data_row.__dict__.values())[0])
        self.DB.update_row(row_id)

    def save_to_db(self) -> None:
        """
        Updates data or saves to database, updates database viewer
        """
        data_row = self.set_data_row()
        self.DB.set_row(data_row)
        # update record instead of saving new if record exists
        try:
            self.update_existing(data_row)
        except IndexError:
            self.DB.insert_new()
        self.clear_recreate()

    def delete_record(self) -> None:
        """
        Deletes record from the database
        """
        data_row = self.set_data_row()
        self.DB.set_row(data_row)
        print(self.DB.data)
        try:
            self.DB.delete_row()
            self.clear_recreate()
            self.confirming()
        except IndexError or OperationalError:
            self.invalid_popup()

    def set_data_row(self):
        """
        Gets data from input widgets into dataclass
        """
        pass

    def custom_widgets(self, row: int):
        """Additional widgets for child classes to specify

        Args:
            row (int): row number to place custom widgets on the UI
        """
        pass

    def alter_table_data(self, table_data: list | tuple):
        """Alters table data to display user-friendly format

        Args:
            table_data (list|tuple): list or tuple of lists of data in rows

        Returns:
            list: list of lists of rows of altered data
        """
        return table_data

    @abstractmethod
    def correct_input_format(self):
        """
        Child class specific input checker
        """
        pass

    @abstractmethod
    def selection_action(self, values: list | tuple):
        """
        Parses and operates on data from selected row in table view

        Args:
            values (list|tuple): values from the selected row
        """
        pass

    @abstractmethod
    def clearing(self):
        """
        Clears all input widgets
        """
        pass
