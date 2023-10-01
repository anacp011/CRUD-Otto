import tkinter as tk
from tkinter import ttk
import pymysql
from consultas_sql import ConexionDB
from tkinter import messagebox
from dialog.lotes_dialog import LoteDialog

class LoteApp:
    def __init__(self, parent, cuaderno1):
        self.parent = parent
        self.cuaderno1 = cuaderno1
        pestana_lotes = ttk.Frame(self.cuaderno1)
        self.cuaderno1.add(pestana_lotes, text="Lotes")
        self.cuaderno1.pack(fill="both", expand=True, padx=10, pady=15)
        self.top_open = False

        #Contenedores
        frame1 = tk.LabelFrame(pestana_lotes)
        frame1.pack(fill="both", expand="yes", pady=(40,0))
        frame1['relief'] = 'flat'
        frame2 = tk.LabelFrame(pestana_lotes)
        frame2.pack(fill="both", expand="yes", padx=20, pady=10)
        frame2['relief'] = 'flat'
        pestana_lotes.bind('<Double-Button-1>', self.deseleccionar_fila)
        
         ## Variables
        self.nroLotes = tk.StringVar()
        self.cantidad = tk.StringVar()
        self.fecha_inicio = tk.StringVar()
        self.fecha_fin = tk.StringVar()
        
        self.opciones_columnas = {
            '  ID Lote': 'nroLotes',
            '  Cantidad': 'cantidad',
            '  Fecha Inicio': 'fecha_inicio',
            '  Fecha Fin': 'fecha_fin'
        }
        
        # Botón
        btn = tk.Button(frame1, text="Restablecer", command=self.restablecer, width=10, font=("Cardana",9), bg="#dcdcdc")
        btn.pack(side=tk.RIGHT, padx=(0,50))
        btn = tk.Button(frame1, text="Buscar", command=self.buscar, width=6, font=("Cardana",9), bg="#dcdcdc")
        btn.pack(side=tk.RIGHT, padx=(10,20))
        
        ## CONSULTA
        self.entry = tk.Entry(frame1, width=15, font=("Cardana",10))
        self.entry.pack(side=tk.RIGHT, ipady=1.5, padx=30)
        self.combo = ttk.Combobox(frame1, values=['', '  ID Lote', '  Cantidad', '  Fecha Inicio', '  Fecha Fin'], state='readonly', width=20, font=("Calibri",11))
        self.combo.pack(side=tk.RIGHT)
        self.combo.set("Seleccione una opción")
        
        ## Tablas
        tree_frame = tk.Frame(frame2)
        tree_frame.pack(padx=(20, 0), pady=(40,0), fill="both")
        
        self.trv = ttk.Treeview(tree_frame, columns=(1,2,3,4), show="headings", height="9")
        self.trv.pack(side=tk.LEFT, fill="both", expand=True)
        self.trv.heading('#1', text='ID Lotes', command= lambda col=1: self.heading_order(col))
        self.trv.heading('#2', text='Cantidad', command= lambda col=2: self.heading_order(col))
        self.trv.heading('#3', text='Fecha inicio', command= lambda col=3: self.heading_order(col))
        self.trv.heading('#4', text='Fecha fin', command= lambda col=4: self.heading_order(col))
        self.trv.column('#1', anchor=tk.CENTER)
        self.trv.column('#2', anchor=tk.CENTER)
        self.trv.column('#3', anchor=tk.CENTER)
        self.trv.column('#4', anchor=tk.CENTER)
        self.trv.bind("<Double-Button-1>", self.abrir_ventana_editar)
        
        self.scrollbar = tk.Scrollbar(tree_frame, orient="vertical", command=self.trv.yview)
        self.trv.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill="y")
        
        btn = tk.Button(frame2, text="Agregar", width=8, font=("Cardana",9), bg="#dcdcdc", command=self.abrir_ventana_agregar)
        btn.pack(side=tk.LEFT, padx=250)
        btn = tk.Button(frame2, text="Eliminar", width=8, font=("Cardana",9), bg="#dcdcdc", command=self.eliminar)
        btn.pack(side=tk.LEFT)
        
        self.actualizar()
            
    def abrir_ventana_agregar(self):
        if not self.top_open:
            self.top_open = True
            LoteDialog(self.parent, self)
    
    def abrir_ventana_editar(self, item):
        if not self.top_open:
            self.top_open = True
            item = self.trv.focus()
            if item:
                LoteDialog(self.parent, self, item)
    
    def top_close(self):
        self.top_open = False
    
    def vista(self, rows):
        self.trv.delete(*self.trv.get_children())
        for i in rows:
            self.trv.insert("", "end", values=i)
    
    def buscar(self):
        opcion = self.combo.get()
        valor = self.entry.get()
        self.trv.delete(*self.trv.get_children())  # Limpiar la Treeview
       
        if opcion in self.opciones_columnas:
            columna = self.opciones_columnas[opcion]
            try:
                self.conexion = ConexionDB(self)
                query = f"SELECT nroLotes, cantidad, fecha_inicio, fecha_fin FROM Lotes WHERE {columna} = %s"
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
            1: 'nroLotes',
            2: 'cantidad',
            3: 'fecha_inicio',
            4: 'fecha_fin'
        }
        
        columna = self.col_op[col]
        self.trv.delete(*self.trv.get_children())
        try:
            self.conexion = ConexionDB(self)
            query = f"SELECT nroLotes, cantidad, fecha_inicio, fecha_fin FROM lotes ORDER BY {columna} ASC"
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
            query = "SELECT nroLotes, cantidad, fecha_inicio, fecha_fin FROM lotes"
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