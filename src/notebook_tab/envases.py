import tkinter as tk
from tkinter import ttk
import pymysql
from tkinter import messagebox
from consultas_sql import ConexionDB
from dialog.env_dialog import EnvaseDialog

class EnvaseApp:
    def __init__(self, parent, cuaderno1):
        self.parent = parent
        self.cuaderno1 = cuaderno1
        pestana_Envases = tk.Frame(self.cuaderno1)
        self.cuaderno1.add(pestana_Envases, text="Envase")
        style = ttk.Style()
        style.configure("TNotebook.Tab", font=("calibri", 12))
        self.cuaderno1.pack(fill="both", expand=True, padx=10, pady=15)
        self.top_open = False
        
        ## Contenedores
        frame1 = tk.LabelFrame(pestana_Envases)
        frame1.pack(fill="both", expand="yes", ipady=10, padx=20, pady=20)
        frame1['relief'] = 'flat'
        frame2 = tk.LabelFrame(pestana_Envases)
        frame2.pack(fill="both", expand="yes", padx=20, pady=20)
        frame2['relief'] = 'flat'
        pestana_Envases.bind('<Double-Button-1>', self.deseleccionar_fila)
        frame1.bind('<Double-Button-1>', self.deseleccionar_fila)
        frame2.bind('<Double-Button-1>', self.deseleccionar_fila)
    
        #   Variables
        self.numEnvases = tk.StringVar()
        self.nombre = tk.StringVar()
        self.proveedor_id = tk.StringVar()
        
        self.opciones_columnas = {
            '  ID Envases': 'env.nroEnvases',
            '  Nombre': 'env.nombre',
            '  ID Proveedor': 'pr.nroProvee'
        }
        ## Botón
        btn = tk.Button(frame1, text="Restablecer", command=self.restablecer, width=10, font=("Cardana",9), bg="#dcdcdc")
        btn.pack(side=tk.RIGHT, padx=(0,50))
        buscar_button = tk.Button(frame1, text="Buscar", command=self.buscar, width=6, font=("Cardana",9), bg="#dcdcdc")
        buscar_button.pack(side=tk.RIGHT, padx=(10,20))
        
        ## Filtro
        self.entry = tk.Entry(frame1, width=15, font=("Cardana",10))
        self.entry.pack(side=tk.RIGHT, ipady=1.5, padx=30)
        self.combo = ttk.Combobox(frame1, values=['', '  ID Envases', '  Nombre', '  ID Proveedor'], state='readonly', width=20, font=("Calibri",11))
        self.combo.pack(side=tk.RIGHT)
        self.combo.set("Seleccione una opción")
        
        ## Tablas
        tree_frame = tk.Frame(frame2)
        tree_frame.pack(padx=(20, 0), pady=20, fill="both")
        
        self.trv = ttk.Treeview(tree_frame, columns=(1, 2, 3), show="headings", height="9")
        self.trv.pack(side=tk.LEFT, fill="both", expand=True)
        self.trv.heading('#1', text="ID Envase", command= lambda col=1: self.heading_order(col))
        self.trv.heading('#2', text="Nombre", command= lambda col=2: self.heading_order(col))
        self.trv.heading('#3', text="ID Proveedor", command= lambda col=3: self.heading_order(col))
        self.trv.column('#1', anchor=tk.CENTER)
        self.trv.column('#2', anchor=tk.CENTER)
        self.trv.column('#3', anchor=tk.CENTER)
        self.trv.bind("<Double-Button-1>", self.abrir_ventana_editar)
        
        self.scrollbar = tk.Scrollbar(tree_frame, orient="vertical", command=self.trv.yview)
        self.trv.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill="y")
        
        btn = tk.Button(frame2, text="Agregar", command=self.abrir_ventana_agregar, width=8, font=("Cardana",9), bg="#dcdcdc")
        btn.pack(side=tk.LEFT, padx=250)
        btn = tk.Button(frame2, text="Eliminar", command=self.eliminar, width=8, font=("Cardana",9), bg="#dcdcdc")
        btn.pack(side=tk.LEFT)
        
        self.actualizar()
        
    def abrir_ventana_agregar(self):
        if not self.top_open:
            self.top_open = True
            EnvaseDialog(self.parent, self)
    
    def abrir_ventana_editar(self, item):
        if not self.top_open:
            self.top_open = True
            item = self.trv.focus()
            if item:
                EnvaseDialog(self.parent, self, item)
    
    def top_close(self):
        self.top_open = False
    
    def buscar(self):
        opcion = self.combo.get()
        valor = self.entry.get()
        self.trv.delete(*self.trv.get_children())  # Limpiar la Treeview
        
        if opcion in self.opciones_columnas:
            columna = self.opciones_columnas[opcion]
            try:
                self.conexion = ConexionDB(self)
                query = f"SELECT env.nroEnvases, env.nombre, pr.nroProvee FROM envases env INNER JOIN proveedores pr ON env.proveedor_id = pr.ID_Provee WHERE {columna} = %s"
                self.conexion.cursor.execute(query, (valor,))
                resultados = self.conexion.cursor.fetchall()

                if resultados:
                    for registro in resultados:
                        self.trv.insert('', 'end', values=registro)
                else:
                    messagebox.showerror("Error", "No existen resultados para la búsqueda.")
            except pymysql.Error as e:
                messagebox.showerror("Error", f"No se pudo realizar la búsqueda: {str(e)}")
            finally:
                if self.conexion:
                    self.conexion.close()
        else:
            self.actualizar()
            messagebox.showerror("Búsqueda", f"Contenedor de consulta vacio")
            
    def heading_order(self, col):
        
        self.col_op = {
            1: 'env.nroEnvases',
            2: 'env.nombre',
            3: 'pr.nroProvee'
        }
        
        columna = self.col_op[col]
        self.trv.delete(*self.trv.get_children())
        try:
            self.conexion = ConexionDB(self)
            query = f"SELECT env.nroEnvases, env.nombre, pr.nroProvee FROM envases env INNER JOIN proveedores pr ON env.proveedor_id = pr.ID_Provee ORDER BY {columna} ASC"
            self.conexion.cursor.execute(query)
            resultados = self.conexion.cursor.fetchall()

            if resultados:
                for registro in resultados:
                    self.trv.insert('', 'end', values=registro)
            else:
                messagebox.showerror("Error", "No se encontraron resultados para la búsqueda.")
        except pymysql.Error as e:
                messagebox.showerror("Error", f"No se pudo realizar la búsqueda: {str(e)}")
        finally:
            if self.conexion:
                self.conexion.close()
    
    def actualizar(self):
        self.trv.delete(*self.trv.get_children())
        try:
            self.conexion = ConexionDB(self)
            query = "SELECT env.nroEnvases, env.nombre, pr.nroProvee FROM envases env INNER JOIN proveedores pr ON env.proveedor_id = pr.ID_Provee  "
            self.conexion.cursor.execute(query)
            rows = self.conexion.cursor.fetchall()
            for i in rows:
                self.trv.insert("", "end", values=i)
        except pymysql.Error as e:
            messagebox.showerror("Error", f"No se pudo obtener los datos: {str(e)}")
        finally:
            if self.conexion:
                self.conexion.close()

    def restablecer(self):
        self.combo.set("Seleccione una opción")  # Restablece el Combobox a una cadena vacía
        self.entry.delete(0, tk.END)  # Borra el contenido del Entry
        self.actualizar()
    
    def eliminar(self):
        selected_item = self.trv.focus()
        if selected_item:
            values = self.trv.item(selected_item)["values"]
            
            confirmation = messagebox.askyesno("Eliminar Envase", "¿Está seguro que desea eliminar este envase?")
            if confirmation:
                try:
                    conexion = ConexionDB(self) 
                    conexion.eliminar_envases(values)  
                    conexion.close() 
                    self.actualizar()
                except pymysql.Error as e:
                    messagebox.showerror("Error", f"No se pudo eliminar el Envase: {str(e)}")
        else:
            messagebox.showerror("Eliminar Envase", "No ha seleccionado ningun Envase")
    
    def deseleccionar_fila(self, event):
        self.trv.selection_remove(self.trv.selection())