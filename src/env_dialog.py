import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pymysql
from consultas_sql import ConexionDB

class EnvaseDialog:
    def __init__(self, parent, parent_env, item=None, callback=None):
        self.parent = parent
        self.parent_env = parent_env
        self.callback = callback
        self.dialog = tk.Toplevel(self.parent.parent)
        self.dialog.title("Agregar/Editar Envases")
        self.dialog.geometry("350x300")
        self.dialog.columnconfigure(0, weight=2)
        self.dialog.columnconfigure(1, weight=2)
    
        tk.Label(self.dialog, text="Número de ENV:").grid(row=0, column=0, sticky=tk.NS, pady=(50,0))
        self.NumEnvases = tk.Entry(self.dialog, width=15)
        self.NumEnvases.grid(row=0, column=1, sticky=tk.W, pady=(60,0))
        
        tk.Label(self.dialog, text="Nombre:").grid(row=1, column=0, sticky=tk.NS, pady=(20,0))
        self.nombre = tk.Entry(self.dialog, width=15)
        self.nombre.grid(row=1, column=1, sticky=tk.W, pady=(20,0))
        
        tk.Label(self.dialog, text="Proveedor ID:").grid(row=2, column=0, sticky=tk.NS, pady=(20,0))
        
        self.proveedorNum = ttk.Combobox(self.dialog, width=12)
        self.proveedorNum.grid(row=2, column=1, sticky=tk.W, pady=(20,0))
        self.proveedorNum['values'] = self.combo_input() 

        if item:
            self.values = self.parent_env.trv.item(item, 'values')
            self.NumEnvases.insert(tk.END, self.values[0])
            self.nombre.insert(tk.END, self.values[1])
            self.proveedorNum.insert(tk.END, self.values[2])

            tk.Button(self.dialog, text="Actualizar", command=self.modificar_datos).grid(row=3, column=0, sticky=tk.E, padx=15,pady=(50,0))
        else:
            tk.Button(self.dialog, text="Agregar", command=self.guardar_datos).grid(row=3, column=0, sticky=tk.E, padx=15, pady=(50,0))

        tk.Button(self.dialog, text="Cancelar", command=self.dialog.destroy).grid(row=3, column=1, sticky=tk.W, padx=15, pady=(50,0))
      
    def combo_input(self):
        self.conexion= pymysql.connect(host="localhost", user="root", password="123456", database="Krausebbdd")
        self.cursor= self.conexion.cursor()
        self.cursor.execute('SELECT nroProvee, nombre FROM proveedores')
        self.conexion.commit()
        self.conexion.close()
        
        data = []

        for row in self.cursor.fetchall():
            #data.append(row[0])
            data.append(f"{row[0]} - {row[1]}") 
        return data
    
    def verify_id_ENV(self):
        numeroEnv = self.values[0]
        conexion = pymysql.connect(host="localhost", user="root", password="123456", database="Krausebbdd")
        cursor = conexion.cursor()
        cursor.execute("SELECT ID_Envases, nombre FROM envases WHERE nroEnvases=%s", (numeroEnv,))
        result = cursor.fetchone()[0]
        conexion.close()
        if result:
            return result
    
    def new_id(self):
        conexion = pymysql.connect(host="localhost", user="root", password="123456", database="Krausebbdd")
        cursor = conexion.cursor()
        cursor.execute("SELECT COUNT(*) FROM envases WHERE nroEnvases=%s", (self.NumEnvases.get(),))
        count = cursor.fetchone()[0]
        if count > 0:
            return True
            
    def guardar_datos(self):
        if self.NumEnvases.get() == "" or self.nombre.get() == "":
            messagebox.showerror("Control de Stock", "Ingrese información en todos los campos")
        else:
            Nro_proveedor = self.proveedorNum.get()
            codigo_proveedor = ConexionDB.exist_id_PR(self, Nro_proveedor)
            
            conexion = pymysql.connect(host="localhost", user="root", password="123456", database="Krausebbdd")
            cursor = conexion.cursor()

            if self.new_id():
                conexion.close()
            else:
                cursor.execute("INSERT INTO envases (nroEnvases, nombre, proveedor_id) VALUES (%s, %s, %s)", (
                    self.NumEnvases.get(),
                    self.nombre.get(),
                    codigo_proveedor,
                ))
                messagebox.showinfo("Datos Completados", "Se agregaron correctamente")

                conexion.commit()
                conexion.close()

                if self.callback:
                    self.callback()

                self.parent_env.actualizar()
                self.dialog.destroy()
    
    def modificar_datos(self):
        if self.NumEnvases.get() == "" or self.nombre.get() == "":
            messagebox.showerror("Control de Stock", "Ingrese información en todos los campos")
        else:
            Nro_proveedor = self.proveedorNum.get()
            codigo_proveedor = ConexionDB.exist_id_PR(self, Nro_proveedor)
            
            conexion = pymysql.connect(host="localhost", user="root", password="123456", database="Krausebbdd")
            cursor = conexion.cursor()
            
            if self.values[0] != self.NumEnvases.get():
                if self.new_id():
                    self.dialog.after(0, lambda: messagebox.showerror("Control de Stock", "Ese número de producto ya existe actualmente."))
                    return
            
            cursor.execute("UPDATE envases SET nroEnvases=%s, nombre=%s, proveedor_id=%s WHERE ID_Envases=%s", (
                self.NumEnvases.get(),
                self.nombre.get(),
                codigo_proveedor,
                self.verify_id_ENV(),
            ))
            messagebox.showinfo("Datos Completados", "Se actualizaron correctamente")
                
            conexion.commit()
            conexion.close()

            if self.callback:
                self.callback()

            self.parent_env.actualizar()
            self.dialog.destroy()           

