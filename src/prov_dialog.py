import tkinter as tk
from tkinter import ttk
import pymysql
from tkinter import messagebox
from consultas_sql import ConexionDB

class ProveedorDialog:
    def __init__(self, parent, parent_prov, item=None, callback=None):
        self.parent = parent
        self.parent_prov = parent_prov
        self.callback = callback
        self.dialog = tk.Toplevel(self.parent.parent)
        self.dialog.title("Agregar/Editar Proveedor")
        self.dialog.geometry("350x300")
        self.dialog.columnconfigure(0, weight=2)
        self.dialog.columnconfigure(1, weight=2)
        
        tk.Label(self.dialog, text="ID de PR").grid(row=0, column=0, sticky=tk.NS, pady=(50,0))
        self.NumProvee = tk.Entry(self.dialog)
        self.NumProvee.grid(row=0, column=1, sticky=tk.W, pady=(60,0))
        
        tk.Label(self.dialog, text="Nombre:").grid(row=1, column=0, sticky=tk.NS, pady=(20,0))
        self.nombre = tk.Entry(self.dialog)
        self.nombre.grid(row=1, column=1, sticky=tk.W, pady=(20,0))
        
        tk.Label(self.dialog, text="Contacto:").grid(row=2, column=0, sticky=tk.NS, pady=(20,0))
        self.contacto = tk.Entry(self.dialog)
        self.contacto.grid(row=2, column=1, sticky=tk.W, pady=(20,0))
        
        if item:
            self.values = self.parent_prov.trv.item(item, 'values')
            self.NumProvee.insert(tk.END, self.values[0])
            self.nombre.insert(tk.END, self.values[1])
            self.contacto.insert(tk.END, self.values[2])

            tk.Button(self.dialog, text="Actualizar", command=self.modificar_datos).grid(row=3, column=0, sticky=tk.E, padx=15,pady=(50,0))
        else:
            tk.Button(self.dialog, text="Agregar", command=self.guardar_datos).grid(row=3, column=0, sticky=tk.E, padx=15, pady=(50,0))

        tk.Button(self.dialog, text="Cancelar", command=self.dialog.destroy).grid(row=3, column=1, sticky=tk.W, padx=15, pady=(50,0))
    
    
    def verify_id_PR(self):
        numeroProvee = self.values[0]
        conexion = pymysql.connect(host="localhost", user="root", password="123456", database="Krausebbdd")
        cursor = conexion.cursor()
        cursor.execute("SELECT ID_Provee FROM proveedores WHERE proveedores.nroProvee=%s", (numeroProvee,))
        result = cursor.fetchone()[0]
        conexion.close()
        if result:
            return result
    
    def new_id(self):
        conexion = pymysql.connect(host="localhost", user="root", password="123456", database="Krausebbdd")
        cursor = conexion.cursor()
        cursor.execute("SELECT COUNT(*) FROM proveedores WHERE nroProvee=%s", (self.NumProvee,))
        count = cursor.fetchone()[0]
        if count > 0:
            return True
    
    def guardar_datos(self):
        if self.NumProvee.get() == "" or self.nombre.get() == "":
            messagebox.showerror("Control de Stock", "Ingrese información en todos los campos")
        else:
            conexion = pymysql.connect(host="localhost", user="root", password="123456", database="Krausebbdd")
            cursor = conexion.cursor()
            
            if self.new_id():
                conexion.close()
            else:
                cursor.execute("INSERT INTO proveedores (nroProvee, nombre, contacto) VALUES (%s, %s, %s)", (
                    self.NumProvee.get(),
                    self.nombre.get(),
                    self.contacto.get(),
                ))
                messagebox.showinfo("Datos Completados", "Se agregaron correctamente")

                conexion.commit()
                conexion.close()

                if self.callback:
                    self.callback()

                self.parent_prov.actualizar()
                self.dialog.destroy()
    
    
    def modificar_datos(self):
        if self.NumProvee.get() == "" or self.nombre.get() == "":
            messagebox.showerror("Control de Stock", "Ingrese información en todos los campos")
        else:
            conexion = pymysql.connect(host="localhost", user="root", password="123456", database="Krausebbdd")
            cursor = conexion.cursor()
            
            if self.values[0] != self.NumProvee.get():
                if self.new_id():
                    self.dialog.after(0, lambda: messagebox.showerror("Control de Stock", "Ese número de producto ya existe actualmente."))
                    return
                    
            cursor.execute("UPDATE proveedores SET nroProvee=%s, nombre=%s, contacto=%s WHERE ID_Provee=%s", (
                self.NumProvee.get(),
                self.nombre.get(),
                self.contacto.get(),
                self.verify_id_PR(),
            ))
            messagebox.showinfo("Datos Completados", "Se actualizaron correctamente")
                
            conexion.commit()
            conexion.close()

            if self.callback:
                self.callback()

            self.parent_prov.actualizar()
            self.dialog.destroy()         

        
        
        
        
        
        
        