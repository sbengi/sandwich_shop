from tkinter import *
import sys
sys.path.append("/../sandwich_shop")

from main_menu import MainWindow

if __name__ == "__main__":
    master = Tk()
    MainWindow(master)
    master.mainloop()