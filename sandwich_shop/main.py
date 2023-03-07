from tkinter import *
import sys
sys.path.append("/../sandwich_shop")

from sandwich_shop.user_interface import main_menu

if __name__ == "__main__":
    master = Tk()
    main_menu.MainWindow(master)
    master.mainloop()