import tkinter
import customtkinter
import tkinter as tk
from tkinter import ttk
from tkinter import *
from materia_prima import MateriaPrimaApp
from PIL import ImageTk, Image

customtkinter.set_appearance_mode("dark") 
#customtkinter.set_default_color_theme("blue")
#self.wind.config(bg="#303030")

class App:
    def __init__(self,root):
        self.wind = root
        self.wind.title("Login")
        #self.wind.config(bg="grey")
        self.wind.geometry("700x560")
        self.wind.resizable(False, False)
        
        customtkinter.set_appearance_mode("dark") 
        #customtkinter.set_default_color_theme("blue")
        
        #app = customtkinter.CTk()
        
        icon_image = Image.open("icon/mouse.ico")
        icon_image1 = ImageTk.PhotoImage(icon_image)
        self.wind.iconphoto(True, icon_image1)
        img1=ImageTk.PhotoImage(Image.open("img/log.jpg"))

        l1=customtkinter.CTkLabel(self.wind, text=" ", image=img1)
        l1.pack()

        #frame=customtkinter.CTkFrame(master=l1, width=500, height=360)
        #frame.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)

        #l2=customtkinter.CTkLabel(self.wind, text="Login", font=('Century Gothic', 50,'bold')) 
        #l2.place(x=200, y=305)

        entry1=customtkinter.CTkEntry(self.wind, width=220, height=40,border_color="#df3538", fg_color="white", text_color="#df3538", bg_color="#df3538", placeholder_text="Username", placeholder_text_color="#df3538", font=('Century Gothic', 15,'bold'))
        entry1.place(x=240, y=230)

        entry2=customtkinter.CTkEntry(self.wind, width=220, height=40, border_color="#df3538", fg_color="white", text_color="#df3538", bg_color="#df3538", placeholder_text="Password", placeholder_text_color="#df3538", font=('Century Gothic', 15,'bold'))
        entry2.place(x=240, y=300)

        #l3=customtkinter.CTkLabel(self.wind, text="Forget password", text_color="white", bg_color="#df3538",font=('Century Gothic', 15,'bold')) 
        #l3.place(x=270, y=340)

        button1=customtkinter.CTkButton(self.wind, text="Ingresar", text_color="#df3538", hover_color="#FF6B6B",fg_color="white", bg_color="#df3538", corner_radius=6, border_color="red", font=('Century Gothic', 15,'bold'),width=200, height=40, command=self.button_function) #, hover_color="red"
        button1.place(x=250, y=380)

        #app.mainloop()
    
    def button_function(self):
        #self.btn.configure(bg="#D82C2C")
        self.wind.withdraw()   # Cierra la ventana de inicio
        main_window = tk.Toplevel()  # Crea una nueva ventana
        main_window.title("Programa Principal")
        main_window.config(bg="#6f6f6f")
        img = PhotoImage(file='C:/Users/Ana/Desktop/CRUD OttoK/img/Logo CLINOK.png')
        main_window.iconphoto(False, img)
        notebook_style = ttk.Style()
        notebook_style.configure("TNotebook.Tab", font=("calibri", 13), padding=[10, 5])
        notebook = ttk.Notebook(main_window)  # Crea un cuaderno para pestañas
        MateriaPrimaApp(main_window, notebook)  # Inicializa el programa general en la nueva ventana
        notebook.pack(fill="both", expand=True, padx=20, pady=20)  # Empaqueta el cuaderno
        
if __name__ == "__main__":
    root = customtkinter.CTk()
    #app = App(root)
    root.mainloop()
