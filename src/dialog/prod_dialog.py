import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pymysql
from consultas_sql import ConexionDB

class ProdDialog:
    def __init__(self, parent, parent_prod, item=None, callback=None):
        self.parent = parent
        self.parent_prod = parent_prod
        self.callback = callback
        self.dialog = tk.Toplevel(self.parent.parent)
        self.dialog.title("Agregar/Editar Productos")
        self.dialog.geometry("350x420")
        self.dialog.columnconfigure(0, weight=2)
        self.dialog.columnconfigure(1, weight=2)
    
        tk.Label(self.dialog, text="Nro Producto:").grid(row=0, column=0, sticky=tk.NS, pady=(50,0))
        self.NumeroProd = tk.Entry(self.dialog, width=15)
        self.NumeroProd.grid(row=0, column=1, sticky=tk.W, pady=(60,0))
        
        tk.Label(self.dialog, text="Nombre:").grid(row=1, column=0, sticky=tk.NS, pady=(20,0))
        self.nombre = tk.Entry(self.dialog, width=15)
        self.nombre.grid(row=1, column=1, sticky=tk.W, pady=(20,0))
        
        tk.Label(self.dialog, text="Cantidad:").grid(row=2, column=0, sticky=tk.NS, pady=(20,0))
        self.cantidad = tk.Entry(self.dialog, width=15)
        self.cantidad.grid(row=2, column=1, sticky=tk.W, pady=(20,0))
        
        tk.Label(self.dialog, text="Precio:").grid(row=3, column=0, sticky=tk.NS, pady=(20,0))
        self.precio = tk.Entry(self.dialog, width=15)
        self.precio.grid(row=3, column=1, sticky=tk.W, pady=(20,0))
        
        tk.Label(self.dialog, text="Nro lote").grid(row=4, column=0, sticky=tk.NS, pady=(20,0))
        self.loteNum = ttk.Combobox(self.dialog, width=12, height=5)
        self.loteNum.grid(row=4, column=1, sticky=tk.W, pady=(20,0))
        self.loteNum['values'] = self.combo_input_LOT() 
        
        tk.Label(self.dialog, text="Estado").grid(row=5, column=0, sticky=tk.NS, pady=(20,0))
        self.estado = ttk.Combobox(self.dialog, width=12, state="readonly")
        self.estado.grid(row=5, column=1, sticky=tk.W, pady=(30,0))
        self.estado['values'] = self.combo_input_EST() 

        if item:
            self.values = self.parent_prod.trv.item(item, 'values')
            self.NumeroProd.insert(tk.END, self.values[0])
            self.nombre.insert(tk.END, self.values[1])
            self.cantidad.insert(tk.END, self.values[2])
            self.precio.insert(tk.END, self.values[3])
            self.loteNum.insert(tk.END, self.values[4])
            self.estado.set(self.values[5])

            tk.Button(self.dialog, text="Actualizar", command=self.modificar_datos).grid(row=6, column=0, sticky=tk.E, padx=15,pady=(60,0))
        else:
            tk.Button(self.dialog, text="Agregar", command=self.guardar_datos).grid(row=6, column=0, sticky=tk.E, padx=15, pady=(60,0))

        tk.Button(self.dialog, text="Cancelar", command=self.on_close).grid(row=6, column=1, sticky=tk.W, padx=15, pady=(60,0))

        self.dialog.protocol("WM_DELETE_WINDOW", self.on_close)
        
    def on_close(self):
        self.dialog.destroy()
        self.parent_prod.top_close()
      
    def combo_input_LOT(self):
        self.conexion= pymysql.connect(host="localhost", user="root", password="123456", database="Krausebbdd")
        self.cursor= self.conexion.cursor()
        self.cursor.execute('SELECT nroLotes FROM lotes')
        self.conexion.commit()
        self.conexion.close()
        
        data = []

        for row in self.cursor.fetchall():
            data.append(f"{row[0]} ") 
        return data
    
    def combo_input_EST(self):
        self.conexion= pymysql.connect(host="localhost", user="root", password="123456", database="Krausebbdd")
        self.cursor= self.conexion.cursor()
        self.cursor.execute('SELECT ID_Estados, nombre_est FROM estado')
        self.conexion.commit()
        self.conexion.close()
        
        data = []

        for row in self.cursor.fetchall():
            data.append(f"{row[0]} - {row[1]}") 
        return data
      
    
    def verify_id_PROD(self):
        numeroProd = self.values[0]
        conexion = pymysql.connect(host="localhost", user="root", password="123456", database="Krausebbdd")
        cursor = conexion.cursor()
        cursor.execute("SELECT ID_Prod FROM productos WHERE nroProd=%s", (numeroProd,))
        result = cursor.fetchone()[0]
        if result:
            return result
        
    def new_id(self):
        conexion = pymysql.connect(host="localhost", user="root", password="123456", database="Krausebbdd")
        cursor = conexion.cursor()
        cursor.execute("SELECT COUNT(*) FROM productos WHERE nroProd=%s", (self.NumeroProd.get(),))
        count = cursor.fetchone()[0]
        if count > 0:
            return True
        
    def guardar_datos(self):
        if self.NumeroProd.get() == "" or self.nombre.get() == "" or self.loteNum.get() == "" or self.estado.get() == "":
            messagebox.showerror("Control de Stock", "Ingrese información en todos los campos")
        else:
            Nro_lote = self.loteNum.get()
            codigo_lote = ConexionDB.exist_id_LOT(self, Nro_lote)
            id_est = self.estado.get()[0]
            
            conexion = pymysql.connect(host="localhost", user="root", password="123456", database="Krausebbdd")
            cursor = conexion.cursor()
            
            if self.new_id(): # verifica si ya existe el NroProd
                self.dialog.after(0, lambda: messagebox.showerror("Control de Stock", "Ese número de Producto ya existe actualmente.")) # Muestra el messagebox de error de manera asincrónica
                return  # No sigue con la ejecución
            
            cursor.execute("INSERT INTO productos (nroProd, nombre, cantidad, precio, lote_id, est_id) VALUES (%s, %s, %s, %s, %s, %s)", (
                self.NumeroProd.get(),
                self.nombre.get(),
                self.cantidad.get(),
                self.precio.get(),
                codigo_lote,
                id_est,
            ))
            messagebox.showinfo("Datos Completados", "Se agregaron correctamente")

            conexion.commit()
            conexion.close()

            if self.callback:
                self.callback()

            self.parent_prod.actualizar()
            self.on_close()

    def map_estado_to_id(self, nombre_estado):
        estados = {
            "Finales": 1,
            "Cuarentena": 2,
            "Descarte": 3
        }
        return estados.get(nombre_estado, None)
    
    def modificar_datos(self):
        if self.NumeroProd.get() == "" or self.nombre.get() == "" or self.loteNum.get() == "" or self.estado.get() == "":
            messagebox.showerror("Control de Stock", "Ingrese información en todos los campos")
        else:
            Nro_lote = self.loteNum.get()
            codigo_lote = ConexionDB.exist_id_LOT(self, Nro_lote)
            #id_est = self.estado.get()[0]
            nombre_estado = self.estado.get()
            id_estado = self.map_estado_to_id(nombre_estado)
            
            # Verifica si el número de Producto fue modificado
            if self.values[0] !=  self.NumeroProd.get():
                if self.new_id(): # Verifica si ya existe el NroProd
                    # Muestra el messagebox de error de manera asincrónica
                    self.dialog.after(0, lambda: messagebox.showerror("Control de Stock", "Ese número de Producto ya existe actualmente."))
                    return  # No sigue con la ejecución

            conexion = pymysql.connect(host="localhost", user="root", password="123456", database="Krausebbdd")
            cursor = conexion.cursor()

            cursor.execute("UPDATE productos SET nroProd=%s, nombre=%s, cantidad=%s, precio=%s, lote_id=%s, est_id=%s WHERE ID_Prod=%s", (
                self.NumeroProd.get(),
                self.nombre.get(),
                self.cantidad.get(),
                self.precio.get(),
                codigo_lote,
                id_estado,  # El valor seleccionado del combobox de estado
                self.verify_id_PROD(),
            ))
            messagebox.showinfo("Datos Completados", "Se actualizaron correctamente")
            
            conexion.commit()
            conexion.close()

            if self.callback:
                self.callback()

            self.parent_prod.actualizar()
            self.on_close()
