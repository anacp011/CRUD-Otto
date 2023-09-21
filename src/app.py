import tkinter
import customtkinter
import tkinter as tk
from tkinter import ttk
from tkinter import *
from materia_prima import MateriaPrimaApp
from PIL import ImageTk, Image

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("700x560")
app.title('Login')
icon_image = Image.open("icon/mouse.ico")
icon_image1 = ImageTk.PhotoImage(icon_image)
app.iconphoto(True, icon_image1)
img1=ImageTk.PhotoImage(Image.open("img/log.jpg"))

l1=customtkinter.CTkLabel(master=app, text=" ", image=img1)
l1.pack()

#frame=customtkinter.CTkFrame(master=l1, width=500, height=360)
#frame.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)

#l2=customtkinter.CTkLabel(master=app, text="Login", font=('Century Gothic', 50,'bold')) 
#l2.place(x=200, y=305)

entry1=customtkinter.CTkEntry(master=app, width=220, height=40,border_color="#df3538", fg_color="white", text_color="#df3538", bg_color="#df3538", placeholder_text="Username", placeholder_text_color="#df3538", font=('Century Gothic', 15,'bold'))
entry1.place(x=230, y=230)

entry2=customtkinter.CTkEntry(master=app, width=220, height=40, border_color="#df3538", fg_color="white", text_color="#df3538", bg_color="#df3538", placeholder_text="Password", placeholder_text_color="#df3538", font=('Century Gothic', 15,'bold'))
entry2.place(x=230, y=300)

l3=customtkinter.CTkLabel(master=app, text="Forget password", text_color="white", bg_color="#df3538",font=('Century Gothic', 15,'bold')) 
l3.place(x=270, y=340)

def button_function():
    #self.btn.configure(bg="#D82C2C")
    app.withdraw()   # Cierra la ventana de inicio
    main_window = tk.Toplevel()  # Crea una nueva ventana
    main_window.title("Programa Principal")
    main_window.geometry("950x500")
    main_window.config(bg="#6f6f6f")
    img = PhotoImage(file='C:/Users/Ana/Desktop/CRUD OttoK/img/Logo CLINOK.png')
    main_window.iconphoto(False, img)
    notebook_style = ttk.Style()
    notebook_style.configure("TNotebook.Tab", font=("calibri", 13), padding=[10, 5])
    notebook = ttk.Notebook(main_window)  # Crea un cuaderno para pestañas
    MateriaPrimaApp(main_window, notebook)  # Inicializa el programa general en la nueva ventana
    notebook.pack(fill="both", expand=True, padx=20, pady=20)  # Empaqueta el cuaderno

button1=customtkinter.CTkButton(master=app, text="Ingresar", text_color="#df3538", hover_color="#FF6B6B",fg_color="white", bg_color="#df3538", corner_radius=6, border_color="red", font=('Century Gothic', 15,'bold'),width=200, height=40, command=button_function) #, hover_color="red"
button1.place(x=230, y=380)

app.mainloop()