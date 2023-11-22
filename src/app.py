import tkinter
import customtkinter
import tkinter as tk
from tkinter import ttk
from tkinter import *
from notebook_tab.materia_prima import MateriaPrimaApp
from PIL import ImageTk, Image

customtkinter.set_appearance_mode("dark") 

class App:
    def __init__(self,root):
        self.wind = root
        self.wind.title("")
        self.wind.geometry("960x540")
        self.wind.resizable(False, False)
        
        icon_image = Image.open("icon/icon30.ico")
        icon_image1 = ImageTk.PhotoImage(icon_image)
        self.wind.iconphoto(True, icon_image1)
        img1=ImageTk.PhotoImage(Image.open("img/Login.jpeg"))

        l1=customtkinter.CTkLabel(self.wind, text=" ", image=img1)
        l1.pack()

        #frame=customtkinter.CTkFrame(master=l1, width=500, height=360)
        #frame.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)

        l2=customtkinter.CTkLabel(self.wind, text="LOGIN", font=('Century Gothic', 30,'bold'), bg_color="#FF3033", text_color="white",) 
        l2.place(x=425, y=225)

        entry1=customtkinter.CTkEntry(self.wind, width=220, height=40,border_color="#FF3033", fg_color="white", text_color="#FF3033", bg_color="#FF3033", placeholder_text="Username", placeholder_text_color="#FF3033", font=('Century Gothic', 15,'bold'))
        entry1.place(x=360, y=280)

        self.entry2=customtkinter.CTkEntry(self.wind, width=220, height=40, border_color="#FF3033", fg_color="white", text_color="#FF3033",bg_color="#FF3033", placeholder_text="Password", placeholder_text_color="#FF3033", font=('Century Gothic', 15,'bold'))
        self.entry2.place(x=360, y=330)
        self.entry2.configure(show="*")
        
        self.check_var = customtkinter.IntVar()
        my_check = customtkinter.CTkCheckBox(self.wind, text="", variable=self.check_var, onvalue=1, offvalue=0, hover_color="#FF3033", border_color="#FF3033", bg_color='white', fg_color="#FF3033", width=0, command = self.show_hide_psd)
        my_check.place(x=547, y=339)

        #l3=customtkinter.CTkLabel(self.wind, text="Forget password", text_color="white", bg_color="#df3538",font=('Century Gothic', 15,'bold')) 
        #l3.place(x=270, y=340)

        button1=customtkinter.CTkButton(self.wind, text="ENTER", text_color="#FF3033", hover_color="#FF6B6B",fg_color="white", bg_color="#FF3033",corner_radius=6, border_color="red", font=('Century Gothic', 15,'bold'),width=100, height=40, command=self.button_function) #, hover_color="red"
        button1.place(x=420, y=390)

        #app.mainloop()
    
    def button_function(self):
        self.wind.withdraw()   # Cierra la ventana de inicio
        main_window = tk.Toplevel()  # Crea una nueva ventana
        main_window.title("Programa Principal")
        main_window.config(bg="#6f6f6f")
        icon_image = Image.open("icon/icon30.ico")
        icon_image1 = ImageTk.PhotoImage(icon_image)
        main_window.iconphoto(True, icon_image1)
        notebook_style = ttk.Style()
        notebook_style.configure("TNotebook.Tab", font=("calibri", 13), padding=[10, 5])
        notebook = ttk.Notebook(main_window)  # Crea un cuaderno para pestañas
        MateriaPrimaApp(main_window, notebook)  # Inicializa el programa general en la nueva ventana
        notebook.pack(fill="both", expand=True, padx=20, pady=20)  # Empaqueta el cuaderno
    
    def show_hide_psd(self):
        if(self.check_var.get()):
            self.entry2.configure(show="")
        else:
            self.entry2.configure(show="*") 
    
if __name__ == "__main__":
    root = customtkinter.CTk()
    #app = App(root)
    root.mainloop()
