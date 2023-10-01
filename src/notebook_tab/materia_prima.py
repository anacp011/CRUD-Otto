import tkinter as tk
from tkinter import ttk
import pymysql
from tkinter import messagebox
from consultas_sql import ConexionDB
from notebook_tab.proveedores import ProveedorApp
from notebook_tab.envases import EnvaseApp
from notebook_tab.etiquetas import EtiquetaApp
from notebook_tab.lotes import LoteApp
from notebook_tab.productos import ProductoApp
from dialog.matprim_dialog import MatPrimDialog

class MateriaPrimaApp:
    def __init__(self, parent, cuaderno1):
        self.parent = parent
        self.cuaderno1 = cuaderno1
        pestana_MatPrim = tk.Frame(self.cuaderno1)
        self.cuaderno1.add(pestana_MatPrim, text="Materia Prima")
        self.cuaderno1.pack(fill="both", expand=True, padx=10)
        self.top_open = False
        
        style1 = ttk.Style()
        style1.configure("Treeview", background="#d3d3d3", fieldbackground="green", foreground="black", font=("Helvetica", 9))
        style1.configure("Treeview.Heading", background="Blackd3d3d3", font=("Helvetica", 10, 'bold'))
        
        ## Pestañas
        self.abrir_pestana_producto()
        self.abrir_pestana_proveedor()
        self.abrir_pestana_envase()
        self.abrir_pestana_etiqueta()
        self.abrir_pestana_lote()
        
        
        ## Contenedores
        frame1 = tk.LabelFrame(pestana_MatPrim)
        frame1.pack(fill="both", expand="yes", ipady=10, padx=20,pady=20)
        frame1['relief'] = 'flat'
        frame2 = tk.LabelFrame(pestana_MatPrim)
        frame2.pack(fill="both", expand="yes", padx=20, pady=20)
        frame2['relief'] = 'flat'
        pestana_MatPrim.bind('<Double-Button-1>', self.deseleccionar_fila)
        frame1.bind('<Double-Button-1>', self.deseleccionar_fila)
        
        #   Variables
        self.NumMatPrim = tk.StringVar()
        self.nombre = tk.StringVar()
        self.cantidad = tk.StringVar()
        self.proveedor_id = tk.StringVar()
        
        self.opciones_columnas = {
            '  ID MateriaPrima': 'mp.nroMatPrim',
            '  Nombre': 'mp.nombre',
            '  ID Proveedor': 'pr.nroProvee'
        }
        
        ## Botón
        btn = tk.Button(frame1, text="Restablecer", command=self.restablecer, width=10, font=("Cardana",9), bg="#dcdcdc")
        btn.pack(side=tk.RIGHT, padx=(0,50), ipady=2)
        buscar_button = tk.Button(frame1, text="Buscar", command=self.buscar, width=6, font=("Cardana",9), bg="#dcdcdc")
        buscar_button.pack(side=tk.RIGHT, padx=(10,20), ipady=2)
        
        ## Filtro
        self.entry = tk.Entry(frame1, width=15, font=("Cardana",10))
        self.entry.pack(side=tk.RIGHT, ipady=1.5, padx=30)
        self.combo = ttk.Combobox(frame1, values=['', '  ID MateriaPrima', '  Nombre', '  ID Proveedor'], state='readonly', width=20, font=("Calibri",11))
        self.combo.pack(side=tk.RIGHT)
        self.combo.set("Seleccione una opción")
       
        ## Tablas
        tree_frame = tk.Frame(frame2)
        tree_frame.pack(padx=(20, 0), pady=10,fill="both")
       
        self.trv = ttk.Treeview(tree_frame, columns=(1, 2, 3, 4), show="headings", height="9")
        self.trv.pack(side=tk.LEFT, fill="both", expand=True)
        self.trv.heading('#1', text="ID Materia Prima", command= lambda col=1: self.heading_order(col))
        self.trv.heading('#2', text="Nombre", command= lambda col=2: self.heading_order(col))
        self.trv.heading('#3', text="Cantidad", command= lambda col=3: self.heading_order(col))
        self.trv.heading('#4', text="ID Proveedor", command= lambda col=4: self.heading_order(col))
       
        self.trv.column('#1', anchor=tk.CENTER)
        self.trv.column('#2', anchor=tk.CENTER)
        self.trv.column('#3', anchor=tk.CENTER)
        self.trv.column('#4', anchor=tk.CENTER)
        self.trv.bind("<Double-Button-1>", self.abrir_ventana_editar)
       
        self.scrollbar = tk.Scrollbar(tree_frame, orient="vertical", command=self.trv.yview)
        self.trv.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill="y")
       
        btn = tk.Button(frame2, text="Agregar", command=self.abrir_ventana_agregar, width=8, font=("Cardana",9), bg="#dcdcdc")
        btn.pack(side=tk.LEFT, padx=250, ipady=2)
        btn = tk.Button(frame2, text="Eliminar", command=self.eliminar, width=8, font=("Cardana",9), bg="#dcdcdc")
        btn.pack(side=tk.LEFT, ipady=2)

        self.actualizar()
    
    def abrir_pestana_proveedor(self):
        ProveedorApp(self, self.cuaderno1)
   
    def abrir_pestana_envase(self):
        EnvaseApp(self, self.cuaderno1)
   
    def abrir_pestana_etiqueta(self):
        EtiquetaApp(self, self.cuaderno1)
   
    def abrir_pestana_lote(self):
        LoteApp(self, self.cuaderno1)
    
    def abrir_pestana_producto(self):
        ProductoApp(self, self.cuaderno1)
   
    def abrir_ventana_agregar(self):
        if not self.top_open:
            self.top_open = True
            MatPrimDialog(self.parent, self)
    
    def abrir_ventana_editar(self, item):
        if not self.top_open:
            self.top_open = True
            item = self.trv.focus()
            if item:
                MatPrimDialog(self.parent, self, item)
    
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
                query = f"SELECT mp.nroMatPrim, mp.nombre, mp.cantidad, pr.nroProvee FROM materias_primas mp INNER JOIN proveedores pr ON mp.proveedor_id = pr.ID_Provee WHERE {columna} = %s"
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
            1: 'mp.nroMatPrim',
            2: 'mp.nombre',
            3: 'mp.cantidad',
            4: 'pr.nroProvee'
        }
        
        columna = self.col_op[col]
        self.trv.delete(*self.trv.get_children())
        try:
            self.conexion = ConexionDB(self)
            query = f"SELECT mp.nroMatPrim, mp.nombre, mp.cantidad, pr.nroProvee FROM materias_primas mp INNER JOIN proveedores pr ON mp.proveedor_id = pr.ID_Provee ORDER BY {columna} ASC"
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
            query = "SELECT mp.nroMatPrim, mp.nombre, mp.cantidad, pr.nroProvee FROM materias_primas mp INNER JOIN proveedores pr ON mp.proveedor_id = pr.ID_Provee "
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
           
            confirmation = messagebox.askyesno("Eliminar Materia Prima", "¿Está seguro que desea eliminar esta materia prima?")
            if confirmation:
                try:
                    conexion = ConexionDB(self)
                    conexion.eliminar_MatPrim(values)  
                    conexion.close()
                    self.actualizar()
                except pymysql.Error as e:
                    messagebox.showerror("Error", f"No se pudo eliminar la Materia Prima: {str(e)}")
        else:
            messagebox.showerror("Eliminar Materia Prima", "No ha seleccionado ningun Materia Prima")
   
    def deseleccionar_fila(self, event):
        self.trv.selection_remove(self.trv.selection()) 