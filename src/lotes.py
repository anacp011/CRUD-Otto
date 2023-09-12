import tkinter as tk
from tkinter import ttk
import pymysql
from consultas_sql import ConexionDB
from tkinter import messagebox
from lotes_dialog import LoteDialog

class LoteApp:
    def __init__(self, parent, cuaderno1):
        self.parent = parent
        self.cuaderno1 = cuaderno1
        pestana_lotes = ttk.Frame(self.cuaderno1)
        self.cuaderno1.add(pestana_lotes, text="Lotes")
        self.cuaderno1.pack(fill="both", expand=True, padx=10, pady=15)

        #Contenedores
        frame1 = tk.LabelFrame(pestana_lotes, text="Consulta", font=("calibri", 12), relief=tk.SUNKEN)
        frame1.pack(fill="both", expand="yes", padx=20, pady=(20,5))
        frame1['relief'] = 'flat'
        frame2 = tk.LabelFrame(pestana_lotes, text="Informacion de Lotes", font=("calibri", 12), relief=tk.SUNKEN)
        frame2.pack(fill="both", expand="yes", padx=20, pady=20)
        frame2['relief'] = 'flat'
        pestana_lotes.bind('<Double-Button-1>', self.deseleccionar_fila)
        
         ## Variables
        self.nroLotes = tk.StringVar()
        self.cantidad = tk.StringVar()
        self.fecha_inicio = tk.StringVar()
        self.fecha_fin = tk.StringVar()

        ## CONSULTA
        self.q = tk.StringVar()
        ent = tk.Entry(frame1, width=15,textvariable=self.q)
        ent.pack(side=tk.LEFT, padx=20, ipady=2)
        

        # Botón
        btn = tk.Button(frame1, text="Buscar", command=self.consulta, width=6)
        btn.pack(side=tk.LEFT, padx=(15,10))
        btn = tk.Button(frame1, text="Restablecer", command=self.restablecer, width=10)
        btn.pack(side=tk.LEFT, padx=6)
        
        ## Tablas
        tree_frame = tk.Frame(frame2)
        tree_frame.pack(padx=(20, 0), pady=20, fill="both", expand=True)
        
        self.trv = ttk.Treeview(tree_frame, columns=(1,2,3,4), show="headings", height="8", selectmode = "extended")
        self.trv.pack(side=tk.LEFT, fill="both", expand=True)
        self.trv.heading('#1', text='Nro Lotes')
        self.trv.heading('#2', text='cantidad')
        self.trv.heading('#3', text='fecha_inicio')
        self.trv.heading('#4', text='fecha_fin')
        self.trv.column('#1', anchor=tk.CENTER)
        self.trv.column('#2', anchor=tk.CENTER)
        self.trv.column('#3', anchor=tk.CENTER)
        self.trv.column('#4', anchor=tk.CENTER)
        self.trv.bind("<Double-Button-1>", self.abrir_ventana_editar)
        
        self.scrollbar = tk.Scrollbar(tree_frame, orient="vertical", command=self.trv.yview)
        self.trv.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill="y")
        
        btn = tk.Button(frame2, text="Agregar", command=self.abrir_ventana_agregar)
        btn.pack(side=tk.LEFT, padx=250)
        btn = tk.Button(frame2, text="Eliminar", command=self.eliminar)
        btn.pack(side=tk.LEFT)
        
        self.actualizar()
            
    def abrir_ventana_agregar(self):
        LoteDialog(self.parent, self)
    
    def abrir_ventana_editar(self, item):
        item = self.trv.focus()
        LoteDialog(self.parent, self, item)
    
    def vista(self, rows):
        self.trv.delete(*self.trv.get_children())
        for i in rows:
            self.trv.insert("", "end", values=i)
    
    def actualizar(self):
        try:
            conexion = ConexionDB(self)  # Crea una instancia de la clase ConexionDB
            conexion.actualizar_lotes()
        except pymysql.Error as e:
            messagebox.showerror("Error", f"No se pudo actualizar la tabla de lotess: {str(e)}")
        finally:
            conexion.close()
            
    def consulta(self):
        conexion = ConexionDB(self)  
        if self.q.get() == "":
            messagebox.showerror("Búsqueda", f"Contenedor de consulta vacio")
            conexion.close()
        else:
            try:
                q2 = self.q.get()
                conexion.consulta_lotes(q2)
            except pymysql.Error as e:
                messagebox.showerror("Error", f"No se pudo realizar la consulta de lotes: {str(e)}")
            finally:
                conexion.close()
            
    def restablecer(self):
        self.q.set("")
        self.actualizar()
    
    def eliminar(self):
        selected_item = self.trv.focus()
        if selected_item:
            values = self.trv.item(selected_item)["values"]
            
            confirmation = messagebox.askyesno("Eliminar lotes", "¿Está seguro que desea eliminar este lotes?")
            if confirmation:
                try:
                    conexion = ConexionDB(self)  # Conexión con la BBDD
                    conexion.eliminar_lotes(values)  # Consulta en SQL 
                    conexion.close()   # Cierre de conexión 
                    self.actualizar()
                except pymysql.Error as e:
                    error_message = str(e)
                    if "foreign key constraint" in error_message.lower():
                        messagebox.showerror("Error", "No se puede eliminar el lotes, tiene una compra registrada.")
                    else:
                        messagebox.showerror("Error", f"No se pudo eliminar el lotes: {error_message}")
        else:
            messagebox.showerror("Eliminar lotes", "No ha seleccionado ningún lotes")

    def deseleccionar_fila(self, event):
        self.trv.selection_remove(self.trv.selection())