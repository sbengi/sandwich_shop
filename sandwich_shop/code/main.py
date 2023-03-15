from tkinter import Tk
import sys
import os
sys.path.insert(0, os.path.abspath("..\\sandwich_shop\\"))
# set environment variable what3words API key
os.environ["API_KEY"] = "N1N5YKSR"

from view.main_menu import MainWindow

if __name__ == "__main__":
    master = Tk()
    MainWindow(master)
    master.mainloop()
