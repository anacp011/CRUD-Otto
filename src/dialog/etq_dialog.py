import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pymysql
from consultas_sql import ConexionDB

class EtiquetaDialog:
    def __init__(self, parent, parent_etq, item=None, callback=None):
        self.parent = parent
        self.parent_etq = parent_etq
        self.callback = callback
        self.dialog = tk.Toplevel(self.parent.parent)
        self.dialog.attributes('-topmost', True)
        self.dialog.title("Agregar/Editar Etiquetas")
        self.dialog.geometry("350x265")
        self.dialog.resizable(False, False)
        self.dialog.configure(bg="#A5A5A5")
        self.dialog.columnconfigure(0, weight=2)
        self.dialog.columnconfigure(1, weight=2)
    
        tk.Label(self.dialog, text="Nro Etiqueta:", background="#A5A5A5", font=("Helvetica", 10)).grid(row=0, column=0, sticky=tk.NS, pady=(50,0))
        self.NumEtiquetas = tk.Entry(self.dialog, width=15)
        self.NumEtiquetas.grid(row=0, column=1, sticky=tk.W, pady=(60,0))
        
        tk.Label(self.dialog, text="Nombre:", background="#A5A5A5", font=("Helvetica", 10)).grid(row=1, column=0, sticky=tk.NS, pady=(20,0))
        self.nombre = tk.Entry(self.dialog, width=15)
        self.nombre.grid(row=1, column=1, sticky=tk.W, pady=(20,0))
        
        tk.Label(self.dialog, text="Nro Proveedor:", background="#A5A5A5", font=("Helvetica", 10)).grid(row=2, column=0, sticky=tk.NS, pady=(20,0))
        
        self.proveedorNum = ttk.Combobox(self.dialog, width=12, height=5)
        self.proveedorNum.grid(row=2, column=1, sticky=tk.W, pady=(20,0))
        self.proveedorNum['values'] = self.combo_input() 

        if item:
            self.values = self.parent_etq.trv.item(item, 'values')
            self.NumEtiquetas.insert(tk.END, self.values[0])
            self.nombre.insert(tk.END, self.values[1])
            self.proveedorNum.insert(tk.END, self.values[2])

            tk.Button(self.dialog, text="Actualizar", command=self.modificar_datos, font=("Helvetica", 9)).grid(row=3, column=0, sticky=tk.E, padx=15,pady=(50,0))
        else:
            tk.Button(self.dialog, text="Agregar", command=self.guardar_datos, font=("Helvetica", 9)).grid(row=3, column=0, sticky=tk.E, padx=15, pady=(50,0))

        tk.Button(self.dialog, text="Cancelar", command=self.on_close, font=("Helvetica", 9)).grid(row=3, column=1, sticky=tk.W, padx=15, pady=(50,0))
    
        self.dialog.protocol("WM_DELETE_WINDOW", self.on_close)
        
    def on_close(self):
        self.dialog.destroy()
        self.parent_etq.top_close()
    
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
    
    def verify_id_ETQ(self):
        numeroEtq = self.values[0]
        conexion = pymysql.connect(host="localhost", user="root", password="123456", database="Krausebbdd")
        cursor = conexion.cursor()
        cursor.execute("SELECT ID_Etiquetas FROM etiquetas WHERE nroEtiquetas=%s", (numeroEtq,))
        result = cursor.fetchone()[0]
        conexion.close()
        if result:
            return result
    
    def new_id(self):
        Netq = self.NumEtiquetas.get() 
        Netq = int(Netq)
        if Netq <= 0 :
            self.dialog.after(0, lambda: messagebox.showerror("Error", "Ingreso incorrecto. El formato de entrada debe ser un número apropiado.")) # Muestra el messagebox de error de manera asincrónica
            return True
        else:
            conexion = pymysql.connect(host="localhost", user="root", password="123456", database="Krausebbdd")
            cursor = conexion.cursor()
            cursor.execute("SELECT COUNT(*) FROM etiquetas WHERE nroEtiquetas=%s", (self.NumEtiquetas.get(),))
            count = cursor.fetchone()[0]
            conexion.close()
            if count > 0:
                self.dialog.after(0, lambda: messagebox.showerror("Control de Stock", "Ese número de etiqueta ya existe actualmente."))
                return True
            
    def guardar_datos(self):
        if self.NumEtiquetas.get() == "" or self.nombre.get() == "":
            messagebox.showerror("Control de Stock", "Ingrese información en todos los campos")
        else:
            Nro_proveedor = self.proveedorNum.get()
            codigo_proveedor = ConexionDB.exist_id_PR(self, Nro_proveedor)
            
            conexion = pymysql.connect(host="localhost", user="root", password="123456", database="Krausebbdd")
            cursor = conexion.cursor()
            
            if self.new_id():
                return
            else:
                cursor.execute("INSERT INTO etiquetas (nroEtiquetas, nombre, proveedor_id) VALUES (%s, %s, %s)", (
                    self.NumEtiquetas.get(),
                    self.nombre.get(),
                    codigo_proveedor,
                ))
                messagebox.showinfo("Datos Completados", "Se agregaron correctamente")

                conexion.commit()
                conexion.close()

                if self.callback:
                    self.callback()

                self.parent_etq.actualizar()
                self.on_close()

    def modificar_datos(self):
        if self.NumEtiquetas.get() == "" or self.nombre.get() == "":
            messagebox.showerror("Control de Stock", "Ingrese información en todos los campos")
        else:
            Nro_proveedor = self.proveedorNum.get()
            codigo_proveedor = ConexionDB.exist_id_PR(self, Nro_proveedor)
            
            conexion = pymysql.connect(host="localhost", user="root", password="123456", database="Krausebbdd")
            cursor = conexion.cursor()
            if self.values[0] != self.NumEtiquetas.get():
                if self.new_id():
                    return
                
            cursor.execute("UPDATE etiquetas SET nroEtiquetas=%s, nombre=%s, proveedor_id=%s WHERE ID_Etiquetas=%s", (
                self.NumEtiquetas.get(),
                self.nombre.get(),
                codigo_proveedor,
                self.verify_id_ETQ(),
            ))
            messagebox.showinfo("Datos Completados", "Se actualizaron correctamente")
                    
            conexion.commit()
            conexion.close()

            if self.callback:
                self.callback()

            self.parent_etq.actualizar()
            self.on_close()           

