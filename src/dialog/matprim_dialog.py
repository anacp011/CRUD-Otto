import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pymysql
from consultas_sql import ConexionDB
import re

class MatPrimDialog:
    def __init__(self, parent, parent_matprim, item=None, callback=None):
        self.parent = parent
        self.parent_matprim = parent_matprim
        self.callback = callback
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.attributes('-topmost', True)
        self.dialog.title("Agregar/Editar Materias Primas")
        self.dialog.geometry("350x300")
        self.dialog.resizable(False, False)
        self.dialog.configure(bg="#A5A5A5")
        self.dialog.columnconfigure(0, weight=2)
        self.dialog.columnconfigure(1, weight=2)
        
        self.cantidad_var = tk.StringVar()
        self.cantidad = tk.IntVar()
        
        tk.Label(self.dialog, text="Nro Materia Prima:", background="#A5A5A5", font=("Helvetica", 10)).grid(row=0, column=0, sticky=tk.NS, pady=(50,0))
        self.NumMatPrim = tk.Entry(self.dialog, width=15)
        self.NumMatPrim.grid(row=0, column=1, sticky=tk.W, pady=(60,0))
        
        tk.Label(self.dialog, text="Nombre:", background="#A5A5A5", font=("Helvetica", 10)).grid(row=1, column=0, sticky=tk.NS, pady=(20,0))
        self.nombre = tk.Entry(self.dialog, width=15)
        self.nombre.grid(row=1, column=1, sticky=tk.W, pady=(20,0))
        
        tk.Label(self.dialog, text="Cantidad:", foreground="black", background="#A5A5A5", font=("Helvetica", 10)).grid(row=2, column=0, sticky=tk.NS, pady=(20,0))
        
        self.cantidad = tk.Entry(self.dialog, width=6)
        self.cantidad.grid(row=2, column=1, sticky=tk.W, pady=(20,0))
        
        self.combo_Unidad= ttk.Combobox(self.dialog, width=4, font=("Helvetica", 10), state='readonly')
        self.combo_Unidad.grid(row=2, column=1, sticky=tk.W, pady=(20,0), padx=(50,0))
        self.combo_Unidad['values']= [ '  kg','  g','  l','  ml']
        
        tk.Label(self.dialog, text="Nro Proveedor", background="#A5A5A5", font=("Helvetica", 10)).grid(row=3, column=0, sticky=tk.NS, pady=(20,0))
        self.proveedorNum = ttk.Combobox(self.dialog, width=12, height=5)
        self.proveedorNum.grid(row=3, column=1, sticky=tk.W, pady=(20,0))
        self.proveedorNum['values'] = self.combo_input() 

        if item:
            self.values = self.parent_matprim.trv.item(item, 'values')
            self.NumMatPrim.insert(tk.END, self.values[0])
            self.nombre.insert(tk.END, self.values[1])

            # Separar la cantidad y la unidad
            cantidad_unidad = self.values[2].strip()  # Elimina espacios en blanco
            match = re.match(r"(\d+)\s*(\w+)", cantidad_unidad)
            if match:
                cantidad, unidad = match.groups()
                self.cantidad.insert(tk.END, cantidad)
                self.combo_Unidad.set(unidad)

            self.proveedorNum.insert(tk.END, self.values[3])

            tk.Button(self.dialog, text="Actualizar", command=self.modificar_datos, font=("Helvetica", 9)).grid(row=4, column=0, sticky=tk.E, padx=(0,25),pady=(50,0))
        else:
            tk.Button(self.dialog, text="Agregar", command=self.guardar_datos, font=("Helvetica", 9)).grid(row=4, column=0, sticky=tk.E, padx=(0,25), pady=(50,0))

        tk.Button(self.dialog, text="Cancelar", command=self.on_close, font=("Helvetica", 9)).grid(row=4, column=1, sticky=tk.W, padx=5, pady=(50,0))
    
        self.dialog.protocol("WM_DELETE_WINDOW", self.on_close)
        
    def on_close(self):
        self.dialog.destroy()
        self.parent_matprim.top_close()
    
    def split_cantidad(self):
        cantidad = self.cantidad.get()
        try:
            cantidad = int(cantidad)
            if cantidad < 0:
                return None
            else:
                unidad = self.combo_Unidad.get()
                cant_uni = str(cantidad) + unidad  # Convertir nuevamente a cadena para concatenar
                return cant_uni
        except ValueError:
            return None  # Puedes devolver None u otro valor que indique un error

    
    def combo_input(self):
        self.conexion= pymysql.connect(host="localhost", user="root", password="123456", database="Krausebbdd")
        self.cursor= self.conexion.cursor()
        self.cursor.execute('SELECT nroProvee, nombre FROM proveedores')
        self.conexion.commit()
        self.conexion.close()
        
        data = []

        for row in self.cursor.fetchall():
            data.append(f"{row[0]} - {row[1]}") 
        return data
      
    
    def verify_id_MP(self):
        numeroMatPrim = self.values[0]
        conexion = pymysql.connect(host="localhost", user="root", password="123456", database="Krausebbdd")
        cursor = conexion.cursor()
        cursor.execute("SELECT ID_MatPrim, nombre FROM materias_primas WHERE nroMatPrim=%s", (numeroMatPrim,))
        result = cursor.fetchone()[0]
        if result:
            return result
        
    def new_id(self):
        Nmp = self.NumMatPrim.get() 
        Nmp = int(Nmp)
        if Nmp <= 0 :
            self.dialog.after(0, lambda: messagebox.showerror("Error", "Ingreso incorrecto. El formato de entrada debe ser un número apropiado.")) # Muestra el messagebox de error de manera asincrónica
            return True
        else:
            conexion = pymysql.connect(host="localhost", user="root", password="123456", database="Krausebbdd")
            cursor = conexion.cursor()
            cursor.execute("SELECT COUNT(*) FROM materias_primas WHERE nroMatPrim=%s", (self.NumMatPrim.get(),))
            count = cursor.fetchone()[0]
            if count > 0:
                self.dialog.after(0, lambda: messagebox.showerror("Control de Stock", "Ese número de Producto ya existe actualmente.")) # Muestra el messagebox de error de manera asincrónica
                return True
            
    def guardar_datos(self):
        if self.NumMatPrim.get() == "" or self.nombre.get() == "" or self.cantidad.get() == "":
            messagebox.showerror("Control de Stock", "Ingrese información en todos los campos")
        else:
            Nro_proveedor = self.proveedorNum.get()
            codigo_proveedor = ConexionDB.exist_id_PR(self, Nro_proveedor)
            
            conexion = pymysql.connect(host="localhost", user="root", password="123456", database="Krausebbdd")
            cursor = conexion.cursor()
            
            if not self.split_cantidad():
                self.dialog.after(0, lambda: messagebox.showerror("Error", "Ingreso incorrecto. El formato de entrada debe ser un número seguido de una unidad (por ejemplo, '14kg')."))  
                return
            else: 
                if self.new_id():
                    return  # No sigue con la ejecución
                else:
                    cursor.execute("INSERT INTO materias_primas (nroMatPrim, nombre, cantidad, proveedor_id) VALUES (%s, %s, %s, %s)", (
                        self.NumMatPrim.get(),
                        self.nombre.get(),
                        self.split_cantidad(),
                        codigo_proveedor,
                    ))
                    messagebox.showinfo("Datos Completados", "Se agregaron correctamente")

                    conexion.commit()
                    conexion.close()

                    if self.callback:
                        self.callback()

                    self.parent_matprim.actualizar()
                    self.on_close()

    
    def modificar_datos(self):
        if self.NumMatPrim.get() == "" or self.nombre.get() == "" or self.cantidad.get() == "":
            messagebox.showerror("Control de Stock", "Ingrese información en todos los campos")
        else:
            Nro_proveedor = self.proveedorNum.get()
            codigo_proveedor = ConexionDB.exist_id_PR(self, Nro_proveedor)
            
            conexion = pymysql.connect(host="localhost", user="root", password="123456", database="Krausebbdd")
            cursor = conexion.cursor()
            
            # Verifica si el número de materia prima ya existe
            if self.values[0] !=  self.NumMatPrim.get():
                if self.new_id():
                    return  # No sigue con la ejecución
                
            if not self.split_cantidad():
                self.dialog.after(0, lambda: messagebox.showerror("Error", "Ingreso incorrecto. El formato de entrada debe ser un número seguido de una unidad (por ejemplo, '14kg')."))  
                return

            cursor.execute("UPDATE materias_primas SET nroMatPrim=%s, nombre=%s, cantidad=%s, proveedor_id=%s WHERE ID_MatPrim=%s", (
                self.NumMatPrim.get(),
                self.nombre.get(),
                self.split_cantidad(),
                codigo_proveedor,
                self.verify_id_MP(),
            ))
            messagebox.showinfo("Datos Completados", "Se actualizaron correctamente")
            
            conexion.commit()
            conexion.close()

            if self.callback:
                self.callback()

            self.parent_matprim.actualizar()
            self.on_close()



