import tkinter as tk
from tkinter import ttk
from materia_prima import MateriaPrimaApp

class App:
    def __init__(self, root):
        self.wind = root
        self.wind.title("LOGIN")
        self.wind.config(bg="grey")
        self.wind.geometry("550x350")
        self.wind.resizable(False, False)

        frame = tk.Frame(self.wind) 
        frame.pack(pady=60)
        frame.config(bg="grey")
        
        tk.Label(frame, text="Usuario: ", background="grey" , font=("calibri", 18) ).grid(row=0, column=0, sticky="e")
        ent_user = tk.Entry(frame)
        ent_user.grid(row=0, column=1, pady=20, padx=20)

        
        tk.Label(frame, text="Contraseña: ", background="grey" ,font=("calibri", 18)).grid(row=1, column=0, sticky="e")
        
        ent_passw = tk.Entry(frame)
        ent_passw.grid(row=1, column=1, pady=20, padx=20)
        
        btn = tk.Button(self.wind, text="Iniciar", font=("calibri", 15), command= self.abrir_programa_general )
        btn.pack(pady=10)   
        
    def abrir_programa_general(self):
        self.wind.withdraw()   # Cierra la ventana de inicio
        main_window = tk.Toplevel()  # Crea una nueva ventana
        main_window.title("Programa Principal")
        main_window.geometry("950x500")
        notebook = ttk.Notebook(main_window)  # Crea un cuaderno para pestañas
        MateriaPrimaApp(main_window, notebook)  # Inicializa el programa general en la nueva ventana
        notebook.pack(fill="both", expand=True, padx=20, pady=20)  # Empaqueta el cuaderno
        
        
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
