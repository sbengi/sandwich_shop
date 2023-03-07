"""Creates app window and the initial view, initiates relevant interfaces"""

from tkinter import *
from create_order import CreateOrder
from edit_menu import EditMenu
from edit_order import EditOrder

DEFAULT_FONT = ("OpenSans", 12)

class MainWindow:
    def __init__(self, master:Tk)->None:
        """Creates all main window and all widgets in initial view

        Args:
            master Tk: tkinter window
        """
        self.master = master
        self.master.title("Sandwich Shop")

        # Set window size
        screen_width = self.master.winfo_screenwidth()               
        screen_height = self.master.winfo_screenheight()               
        self.master.geometry("%dx%d" % (screen_width/1.5, screen_height))
        self.master.state('zoomed')
        self.master.minsize(500,500)

        # Set sandwich icon
        self.icon = PhotoImage(file="icon.png")
        self.master.iconphoto(True, self.icon)

        # Frame of page label and action selection buttons
        top_frame = Frame()
        top_frame.grid(column=0, row=0, pady=30, padx=30, sticky="NW")

        # logo
        self.shop_name = Label(
            master=top_frame,
            text=" Sandwich Shop",
            font=("OpenSans", 30),
            anchor=W
            ).grid(column=0, 
                row=0, 
                columnspan=2,
                sticky="W")

        # Menu option buttons
        self.create_order = Button(
            master=top_frame,
            text="Create order",
            bg="lightgrey",
            font=DEFAULT_FONT,
            command=self.order_menu
            )
        self.create_order.grid(column=0, 
                            row=1,
                            pady=20,
                            ipadx=10,)

        self.edit_menu = Button(
            master=top_frame,
            text="Edit menu",
            bg="lightgrey",
            font=DEFAULT_FONT,
            command=self.menu_editor
            )
        self.edit_menu.grid(column=1, 
                        row=1,
                        pady=20,
                        ipadx=15)

        self.view_orders = Button(
            master=top_frame,
            text="View orders",
            bg="lightgrey",
            font=DEFAULT_FONT,
            command=self.order_editor
            )
        self.view_orders.grid(column=2, 
                        row=1,
                        pady=20,
                        padx=10,
                        ipadx=5)

        # empty frames for use in editor interfaces
        self.db_display = Frame()
        self.db_display.grid(column=0, columnspan=5, row=2, rowspan=12, padx=45, pady=20, sticky="NW")

        self.input_widgets = Frame()
        self.input_widgets.grid(column=5, columnspan=4, row=2, rowspan=12, padx=30, pady=20, sticky="NSEW")

    def clear_frame(self)->None:
        """
        Delete all elements in editor interface frames
        """
        for widget in self.db_display.winfo_children():
            widget.destroy()
        for widget in self.input_widgets.winfo_children():
            widget.destroy()

    def order_menu(self)->None:
        """
        Clears frames, recreates interface for creating order
        """
        self.clear_frame()
        CreateOrder(self.db_display, self.input_widgets)

    def menu_editor(self)->None:
        """
        Clears frames, recreates interface for editing the menu
        """
        self.clear_frame()
        EditMenu(self.db_display, self.input_widgets)
    
    def order_editor(self)->None:
        """
        Clears frames, recreates interface for editing orders
        """
        self.clear_frame()
        EditOrder(self.db_display, self.input_widgets)

if __name__ == "__main__":
    master = Tk()
    MainWindow(master)
    master.mainloop()
