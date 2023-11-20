import tkinter as tk
from tkinter import ttk
import pymysql
from tkinter import messagebox
from consultas_sql import ConexionDB
from dialog.prod_dialog import ProdDialog

class ProductoApp:
    def __init__(self, parent, cuaderno1):
        self.parent = parent
        self.cuaderno1 = cuaderno1
        pestana_productos = ttk.Frame(self.cuaderno1)
        self.cuaderno1.add(pestana_productos, text="Productos")
        self.cuaderno1.pack(fill="both", expand=True, padx=10)
        self.top_open = False

        ## Contenedores
        frame1 = tk.LabelFrame(pestana_productos, relief=tk.SUNKEN)
        frame1.pack(fill="both", expand="yes", ipady=10, padx=30, pady=(20,30))
        frame1['relief'] = 'flat'
        frame2 = tk.LabelFrame(pestana_productos, relief=tk.SUNKEN)
        frame2.pack(fill="both", expand="yes",padx=10, pady=(10,10))
        frame2['relief'] = 'flat'
        pestana_productos.bind('<Double-Button-1>', self.deseleccionar_fila)
        frame1.bind('<Double-Button-1>', self.deseleccionar_fila)
        frame2.bind('<Double-Button-1>', self.deseleccionar_fila)
        
        #   Variables
        self.NumeroProd = tk.StringVar()
        self.nombre = tk.StringVar()
        self.cantidad = tk.StringVar()
        self.precio = tk.StringVar()
        self.lote_id = tk.StringVar()
        self.estado_id = tk.StringVar()
        
        self.opciones_columnas1 = {
            '  ID Producto': 'prod.nroProd',
            '  Nombre': 'prod.nombre',
            '  ID Lote': 'lot.nroLotes'
        }
        self.opciones_columnas2 = {
            '  Todos': 'Todos',
            '  Finales': 'Finales',
            '  Descarte': 'Descarte',
            '  Cuarentena': 'Cuarentena'
        }
        
        ## Botón
        btn = tk.Button(frame1, text="Restablecer",command=self.restablecer, width=10, font=("Cardana",9), bg="#dcdcdc") 
        btn.pack(side=tk.RIGHT, padx=(0,50))
        buscar_button = tk.Button(frame1, text="Buscar", command=self.buscar, width=6, font=("Cardana",9), bg="#dcdcdc") 
        buscar_button.pack(side=tk.RIGHT, padx=(10,20))
        
        ## Filtro
        self.entry = tk.Entry(frame1, width=15, font=("Cardana",10))
        self.entry.pack(side=tk.RIGHT, ipady=1.5, padx=30)
        self.combo = ttk.Combobox(frame1, values=['', '  ID Producto', '  Nombre', '  ID Lote'], state='readonly', width=20, font=("Calibri",11))
        self.combo.pack(side=tk.RIGHT)
        self.combo.set("Seleccione una opción")

        self.combo_state = ttk.Combobox(frame1, values=['  Todos', '  Finales', '  Descarte', '  Cuarentena'], state='readonly', width=15, font=("Calibri",11))
        self.combo_state.pack(side=tk.LEFT)
        self.combo_state.set("  Todos")
        self.combo_state.bind("<<ComboboxSelected>>", self.estado_seleccionado)
       
        ## Tablas
        tree_frame = tk.Frame(frame2)
        tree_frame.pack(padx=(20, 0), pady=10,fill="both") 
        
        self.trv = ttk.Treeview(tree_frame, columns=(1, 2, 3, 4, 5, 6), show="headings", height="9")
        self.trv.pack(side=tk.LEFT, fill="both", expand=True)
        self.trv.heading('#1', text="ID Productos", command= lambda col=1: self.heading_order(col))
        self.trv.heading('#2', text="Nombre", command= lambda col=2: self.heading_order(col))
        self.trv.heading('#3', text="Cantidad", command= lambda col=3: self.heading_order(col))
        self.trv.heading('#4', text="Precio", command= lambda col=4: self.heading_order(col))
        self.trv.heading('#5', text="ID Lote", command= lambda col=5: self.heading_order(col))
        self.trv.heading('#6', text="Estado")
       
        self.trv.column('#1', anchor=tk.CENTER, width=140)
        self.trv.column('#2', anchor=tk.CENTER, width=140)
        self.trv.column('#3', anchor=tk.CENTER, width=140)
        self.trv.column('#4', anchor=tk.CENTER, width=140)
        self.trv.column('#5', anchor=tk.CENTER, width=140)
        self.trv.column('#6', anchor=tk.CENTER, width=140)
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
            ProdDialog(self.parent, self)
    
    def abrir_ventana_editar(self, item):
        if not self.top_open:
            self.top_open = True
            item = self.trv.focus()
            if item:
                ProdDialog(self.parent, self, item)
    
    def top_close(self):
        self.top_open = False
    
    def actualizar(self):
        self.trv.delete(*self.trv.get_children())
        try:
            self.conexion = ConexionDB(self)
            query = "SELECT prod.nroProd, prod.nombre, prod.cantidad, prod.precio, lot.nroLotes, est.nombre_est FROM productos prod INNER JOIN lotes lot ON prod.lote_id = lot.ID_Lotes INNER JOIN estado est ON prod.est_id = est.ID_Estados ORDER BY  prod.ID_Prod ASC"
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
        self.combo_state.set("Todos")
        self.entry.delete(0, tk.END)  # Borra el contenido del Entry
        self.actualizar()
    
    def buscar(self):
        opcion = self.combo.get()
        valor = self.entry.get()
        self.trv.delete(*self.trv.get_children())  # Limpiar la Treeview
       
        if opcion in self.opciones_columnas1:
            columna = self.opciones_columnas1[opcion]
            try:
                self.conexion = ConexionDB(self)
                query = f"SELECT prod.nroProd, prod.nombre, prod.cantidad, prod.precio, lot.nroLotes, est.nombre_est FROM productos prod INNER JOIN lotes lot ON prod.lote_id = lot.ID_Lotes INNER JOIN estado est ON prod.est_id = est.ID_Estados WHERE {columna} = %s"
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
            messagebox.showerror("Error", f"Contenedor de consulta vacio")
    
    def heading_order(self, col):
        
        self.col_op = {
            1: 'prod.nroProd',
            2: 'prod.nombre',
            3: 'prod.cantidad',
            4: 'prod.precio',
            5: 'lot.nroLotes'
        }
        
        columna = self.col_op[col]
        self.trv.delete(*self.trv.get_children())
        try:
            self.conexion = ConexionDB(self)
            query = f"SELECT prod.nroProd, prod.nombre, prod.cantidad, prod.precio, lot.nroLotes, est.nombre_est FROM productos prod INNER JOIN lotes lot ON prod.lote_id = lot.ID_Lotes INNER JOIN estado est ON prod.est_id = est.ID_Estados ORDER BY {columna} ASC"
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
    
    def estado_seleccionado(self, event):
        select= self.combo_state.get()
        opcion = self.opciones_columnas2[select]
        
        if opcion == "Todos":
            self.actualizar()
        else:
            
            self.trv.delete(*self.trv.get_children())  # Limpiar la Treeview
            
            try:
                self.conexion = ConexionDB(self)
                query = f"SELECT prod.nroProd, prod.nombre, prod.cantidad, prod.precio, lot.nroLotes, est.nombre_est FROM productos prod INNER JOIN lotes lot ON prod.lote_id = lot.ID_Lotes INNER JOIN estado est ON prod.est_id = est.ID_Estados WHERE est.nombre_est = %s"
                self.conexion.cursor.execute(query, (opcion,))
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
            
    def eliminar(self):
        selected_item = self.trv.focus()
        if selected_item:
            values = self.trv.item(selected_item)["values"]
           
            confirmation = messagebox.askyesno("Eliminar Producto", "¿Está seguro que desea eliminar este Producto?")
            if confirmation:
                try:
                    conexion = ConexionDB(self)
                    conexion.eliminar_producto(values)  
                    conexion.close()
                    self.actualizar()
                except pymysql.Error as e:
                    messagebox.showerror("Error", f"No se pudo eliminar el Producto: {str(e)}")
        else:
            messagebox.showerror("Eliminar Producto", "No ha seleccionado ningun Producto")
   
    def deseleccionar_fila(self, event):
        self.trv.selection_remove(self.trv.selection())   