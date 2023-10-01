import tkinter as tk
from tkinter import ttk
import pymysql
from tkinter import messagebox
from consultas_sql import ConexionDB
from dialog.prov_dialog import ProveedorDialog

class ProveedorApp:
    def __init__(self, parent, cuaderno1):
        self.parent = parent
        self.cuaderno1 = cuaderno1
        pestana_proveedores = ttk.Frame(self.cuaderno1)
        self.cuaderno1.add(pestana_proveedores, text="Proveedores")
        self.cuaderno1.pack(fill="both", expand=True, padx=10, pady=15)
        self.top_open = False
        
        ## Contenedor
        frame1 = tk.LabelFrame(pestana_proveedores)
        frame1.pack(fill="both", expand="yes", pady=(40,0))
        frame1['relief'] = 'flat'
        frame2 = tk.LabelFrame(pestana_proveedores)
        frame2.pack(fill="both", expand="yes", padx=20, pady=10)
        frame2['relief'] = 'flat'
        pestana_proveedores.bind('<Double-Button-1>', self.deseleccionar_fila)
        
        self.NumeroProvee = tk.StringVar()
        self.nombre = tk.StringVar() 
        self.contacto = tk.StringVar()

        # Crear un nuevo frame para el Treeview y el Scrollbar
        tree_frame = tk.Frame(frame2)
        tree_frame.pack(padx=(20, 0), pady=(40,0), fill="both")
        
        self.trv = ttk.Treeview(tree_frame,  columns=(1, 2, 3), show="headings", height="9")
        self.trv.pack(side=tk.LEFT, fill="both", expand=True)
        self.trv.heading('#1', text="ID Proveedor", command= lambda col=1: self.heading_order(col))
        self.trv.heading('#2', text="Nombre", command= lambda col=2: self.heading_order(col))
        self.trv.heading('#3', text="Contacto")
        self.trv.column('#1', anchor=tk.CENTER)
        self.trv.column('#2', anchor=tk.CENTER)
        self.trv.column('#3', anchor=tk.CENTER)
        self.trv.bind("<Double-Button-1>", self.abrir_ventana_editar)
        
        self.scrollbar = tk.Scrollbar(tree_frame, orient="vertical", command=self.trv.yview)
        self.trv.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill="y")
        
        self.opciones_columnas = {
            '  ID Proveedor': 'nroProvee',
            '  Nombre': 'nombre'
        }
        
        ## Boton
        btn = tk.Button(frame1, text="Restablecer", command=self.restablecer, width=10, font=("Cardana",9), bg="#dcdcdc")
        btn.pack(side=tk.RIGHT, padx=(0,50))
        btn = tk.Button(frame1, text="Buscar", command=self.buscar,  width=6, font=("Cardana",9), bg="#dcdcdc")
        btn.pack(side=tk.RIGHT, padx=(10,20))

        ## CONSULTA        
        self.entry = tk.Entry(frame1, width=15, font=("Cardana",10))
        self.entry.pack(side=tk.RIGHT, ipady=1.5, padx=30)
        self.combo = ttk.Combobox(frame1, values=['', '  ID Proveedor', '  Nombre'], state='readonly', width=20, font=("Calibri",11))
        self.combo.pack(side=tk.RIGHT)
        self.combo.set("Seleccione una opción")
        
        btn = tk.Button(frame2, text="Agregar", width=8, font=("Cardana",9), bg="#dcdcdc", command=self.abrir_ventana_agregar)
        btn.pack(side=tk.LEFT, padx=250)
        btn = tk.Button(frame2, text="Eliminar",  width=8, font=("Cardana",9), bg="#dcdcdc", command=self.eliminar)
        btn.pack(side=tk.LEFT)

        self.actualizar()
    
    def abrir_ventana_agregar(self):
        if not self.top_open:
            self.top_open = True
            ProveedorDialog(self.parent, self)
    
    def abrir_ventana_editar(self, item):
        if not self.top_open:
            self.top_open = True
            item = self.trv.focus()
            if item:
                ProveedorDialog(self.parent, self, item)
    
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
                query = f"SELECT nroProvee, nombre, contacto FROM proveedores WHERE {columna} = %s"
                self.conexion.cursor.execute(query, (valor,))
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
        else:
            self.actualizar()
            messagebox.showerror("Error", f"Contenedor de consulta vacio")

    def heading_order(self, col):
        
        self.col_op = {
            1: 'nroProvee',
            2: 'nombre'
        }
        
        columna = self.col_op[col]
        self.trv.delete(*self.trv.get_children())
        try:
            self.conexion = ConexionDB(self)
            query = f"SELECT nroProvee, nombre, contacto FROM proveedores ORDER BY {columna} ASC"
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
            query = "SELECT nroProvee, nombre, contacto FROM proveedores"
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
            
            confirmation = messagebox.askyesno("Eliminar proveedor", "¿Está seguro que desea eliminar este proveedor?")
            if confirmation:
                try:
                    conexion = ConexionDB(self)  
                    conexion.eliminar_proveedor(values)  
                    conexion.close() 
                    self.actualizar()
                except pymysql.Error as e:
                    error_message = str(e)
                    if "foreign key constraint" in error_message.lower():
                        messagebox.showerror("Error", "No se puede eliminar el proveedor, tiene un registro hecho.")
                    else:
                        messagebox.showerror("Error", f"No se pudo eliminar el proveedor: {error_message}")
        else:
            messagebox.showerror("Eliminar proveedor", "No ha seleccionado ningun proveedor")
    
    def deseleccionar_fila(self, event):
        self.trv.selection_remove(self.trv.selection())