from tkinter import Tk
from vista import GUI
from modelo import *

if  __name__ == '__main__' :
    ventana = Tk()
    app=GUI(ventana)
    ventana.mainloop()