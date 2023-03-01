from tkinter import *
from create_order import CreateOrder

DEFAULT_FONT = ("OpenSans", 12)

class MainWindow():

    def __init__(self, master) -> None:
        self.master = master
        self.master.title("Sandwich Shop")
        #self.bind("<Configure>", self.on_resize)
        #self.height = self.winfo_reqheight()
        #self.width = self.winfo_reqwidth()

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
            )
        self.view_orders.grid(column=2, 
                        row=1,
                        pady=20,
                        padx=10,
                        ipadx=5)

        # empty database table display
        self.db_display = Frame()
        self.db_display.grid(column=0, columnspan=5, row=2, rowspan=12, padx=45, pady=20, sticky="NW")

        self.input_widgets = Frame()
        self.input_widgets.grid(column=5, columnspan=4, row=2, rowspan=12, padx=30, pady=20, sticky="NSEW")

    def order_menu(self):
        CreateOrder(self.db_display, self.input_widgets)
    
    def on_resize(self, event):
        # determine the ratio of old width/height to new width/height
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas 
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all",0,0,wscale,hscale)

if __name__ == "__main__":
    master = Tk()
    MainWindow(master)
    """canvas= Canvas(master, width=100, height=100)
    canvas.bind("<Key>", key)
    canvas.bind("<Button-1>", callback)
    canvas.pack()"""
    master.mainloop()
