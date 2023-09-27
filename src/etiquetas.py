import tkinter as tk
from tkinter import ttk
import pymysql
from tkinter import messagebox
from consultas_sql import ConexionDB
from etq_dialog import EtiquetaDialog

class EtiquetaApp:
    def __init__(self, parent, cuaderno1):
        self.parent = parent
        self.cuaderno1 = cuaderno1
        pestana_Etiquetas = tk.Frame(self.cuaderno1)
        self.cuaderno1.add(pestana_Etiquetas, text="Etiqueta")
        style = ttk.Style()
        style.configure("TNotebook.Tab", font=("calibri", 12))
        self.cuaderno1.pack(fill="both", expand=True, padx=10, pady=15)
        
        # Contenedores
        frame1 = tk.LabelFrame(pestana_Etiquetas)
        frame1.pack(fill="both", expand="yes", ipady=10, padx=20, pady=20)
        frame1['relief'] = 'flat'
        frame2 = tk.LabelFrame(pestana_Etiquetas)
        frame2.pack(fill="both", expand="yes", padx=20, pady=20)
        frame2['relief'] = 'flat'
        pestana_Etiquetas.bind('<Double-Button-1>', self.deseleccionar_fila)
    
        #   Variables
        self.numEtiquetas = tk.StringVar()
        self.nombre = tk.StringVar()
        self.proveedor_id = tk.StringVar()
        
        self.opciones_columnas = {
            '  Nro Etiquetas': 'etq.nroEtiquetas',
            '  Nombre': 'etq.nombre',
            '  Nro Proveedor': 'pr.nroProvee'
        }
        ## Botón
        btn = tk.Button(frame1, text="Restablecer", width=10, font=("Cardana",9), bg="#dcdcdc", command=self.restablecer)
        btn.pack(side=tk.RIGHT, padx=(0,50))
        buscar_button = tk.Button(frame1, text="Buscar", width=6, font=("Cardana",9), bg="#dcdcdc", command=self.buscar)
        buscar_button.pack(side=tk.RIGHT, padx=(10,20))
        
        ## Filtro
        self.entry = tk.Entry(frame1, width=15, font=("Cardana",10))
        self.entry.pack(side=tk.RIGHT, ipady=1.5, padx=30)
        self.combo = ttk.Combobox(frame1, values=['', '  Nro Etiquetas', '  Nombre', '  Nro Proveedor'], state='readonly', width=20, font=("Calibri",11))
        self.combo.pack(side=tk.RIGHT)
        self.combo.set("Seleccione una opción")
        
        ## Tablas
        tree_frame = tk.Frame(frame2)
        tree_frame.pack(padx=(20, 0), pady=20, fill="both")
        
        self.trv = ttk.Treeview(tree_frame, columns=(1, 2, 3), show="headings", height="9")
        self.trv.pack(side=tk.LEFT, fill="both", expand=True)
        self.trv.heading('#1', text="Nro Etiqueta")
        self.trv.heading('#2', text="Nombre")
        self.trv.heading('#3', text="Nro Proveedor")
        self.trv.column('#1', anchor=tk.CENTER)
        self.trv.column('#2', anchor=tk.CENTER)
        self.trv.column('#3', anchor=tk.CENTER)
        self.trv.bind("<Double-Button-1>", self.abrir_ventana_editar)
        
        
        self.scrollbar = tk.Scrollbar(tree_frame, orient="vertical", command=self.trv.yview)
        self.trv.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill="y")
        
        btn = tk.Button(frame2, text="Agregar", width=10, font=("Cardana",9), bg="#dcdcdc", command=self.abrir_ventana_agregar)
        btn.pack(side=tk.LEFT, padx=250)
        btn = tk.Button(frame2, text="Eliminar", width=10, font=("Cardana",9), bg="#dcdcdc", command=self.eliminar)
        btn.pack(side=tk.LEFT)
        
        self.actualizar()
        
    def abrir_ventana_agregar(self):
        EtiquetaDialog(self.parent, self)
    
    def abrir_ventana_editar(self, item):
        item = self.trv.focus()
        EtiquetaDialog(self.parent, self, item)
    
    def buscar(self):
        opcion = self.combo.get()
        valor = self.entry.get()
        self.trv.delete(*self.trv.get_children())  # Limpiar la Treeview
        
        if opcion in self.opciones_columnas:
            columna = self.opciones_columnas[opcion]
            try:
                self.conexion = ConexionDB(self)
                query = f"SELECT etq.nroEtiquetas, etq.nombre, pr.nroProvee FROM etiquetas etq INNER JOIN proveedores pr ON etq.proveedor_id = pr.ID_Provee WHERE {columna} = %s"
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
            messagebox.showerror("Búsqueda", f"Contenedor de consulta vacio")
            
        
    def actualizar(self):
        self.trv.delete(*self.trv.get_children())
        try:
            self.conexion = ConexionDB(self)
            query = "SELECT etq.nroEtiquetas, etq.nombre, pr.nroProvee FROM etiquetas etq INNER JOIN proveedores pr ON etq.proveedor_id = pr.ID_Provee"
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
            
            confirmation = messagebox.askyesno("Eliminar Etiqueta", "¿Está seguro que desea eliminar esta Etiqueta?")
            if confirmation:
                try:
                    conexion = ConexionDB(self) 
                    conexion.eliminar_etiquetas(values)  
                    conexion.close() 
                    self.actualizar()
                except pymysql.Error as e:
                    messagebox.showerror("Error", f"No se pudo eliminar el Etiqueta: {str(e)}")
        else:
            messagebox.showerror("Eliminar Etiqueta", "No ha seleccionado ningun Etiqueta")
    
    def deseleccionar_fila(self, event):
        self.trv.selection_remove(self.trv.selection())