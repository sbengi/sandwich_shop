from tkinter import Tk
import sys
sys.path.append([0, "..//code//"])
from code.view.main_menu import MainWindow



if __name__ == "__main__":
    master = Tk()
    MainWindow(master)
    master.mainloop()
