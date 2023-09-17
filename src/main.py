import tkinter as tk
from tkinter import *
from app import App

if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    img = PhotoImage(file='C:/Users/Ana/Desktop/CRUD OttoK/filtroclinok.png')
    root.iconphoto(False, img)
    root.mainloop()