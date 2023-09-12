import tkinter as tk
from tkinter import messagebox
from tkcalendar import *
from tkcalendar import DateEntry
import pymysql
from consultas_sql import ConexionDB

class LoteDialog:
    def __init__(self, parent, parent_lot, item=None, callback=None):
        self.parent = parent
        self.parent_lot = parent_lot
        self.callback = callback
        self.dialog = tk.Toplevel(self.parent.parent)
        self.dialog.title("Agregar/Editar lotes")
        self.dialog.geometry("340x350")

        frame = tk.Frame(self.dialog)
        frame.pack(pady=50)

        tk.Label(frame, text="Nro Lotes:").grid(row=0, column=0, sticky=tk.NS, pady=(10,0))
        self.NumLotes = tk.Entry(frame, width=15)
        self.NumLotes.grid(row=0, column=1, sticky=tk.W, pady=(10,0))
        
        tk.Label(frame, text="Cantidad:").grid(row=1, column=0, sticky=tk.NS, pady=(20,0))
        self.cantidad = tk.Entry(frame, width=15)
        self.cantidad.grid(row=1, column=1, sticky=tk.W, pady=(20,0))
        
        tk.Label(frame, text="Fecha de inicio:").grid(row=2, column=0, sticky=tk.NS, pady=(30,0))
        tk.Label(frame, text="Fecha de Fin:").grid(row=2, column=1, sticky=tk.NS, pady=(30,0))
         
        self.fecha_inicio = DateEntry(frame,date_pattern='yyyy-mm-dd')
        self.fecha_fin = DateEntry(frame, date_pattern='yyyy-mm-dd')
        self.fecha_inicio = DateEntry(frame, date_pattern='yyyy/mm/dd')
        self.fecha_fin = DateEntry(frame, date_pattern='yyyy/mm/dd')
            
        self.fecha_inicio.grid(row=3, column=0, sticky=tk.E, padx=15,pady=(10,0))
        self.fecha_fin.grid(row=3, column=1, sticky=tk.W, padx=15,pady=(10,0))
        
        btn_frame = tk.Frame(self.dialog)
        btn_frame.pack(pady=20)

        if item:
            self.values = self.parent_lot.trv.item(item, 'values')
            self.NumLotes.insert(tk.END, self.values[0])
            self.cantidad.insert(tk.END, self.values[1])
            self.fecha_inicio.delete(0, tk.END)
            self.fecha_inicio.insert(tk.END, self.values[2])
            self.fecha_fin.delete(0, tk.END)
            self.fecha_fin.insert(tk.END, self.values[3])
        
            tk.Button(frame, text="Actualizar", command=self.modificar_datos).grid(row=4, column=0, sticky=tk.E, padx=15,pady=(50,0))
        else:
            tk.Button(frame, text="Agregar", command=self.guardar_datos).grid(row=4, column=0, sticky=tk.E, padx=15, pady=(50,0))

        tk.Button(frame, text="Cancelar", command=self.dialog.destroy).grid(row=4, column=1, sticky=tk.W, padx=15, pady=(50,0))
    
    def verify_id_LOT(self):
        numeroLot = self.values[0]
        conexion = pymysql.connect(host="localhost", user="root", password="123456", database="Krausebbdd")
        cursor = conexion.cursor()
        cursor.execute("SELECT ID_Lotes FROM lotes WHERE nroLotes=%s", (numeroLot,))
        result = cursor.fetchone()[0]
        conexion.close()
        if result:
            return result
    
    def new_id(self):
        conexion = pymysql.connect(host="localhost", user="root", password="123456", database="Krausebbdd")
        cursor = conexion.cursor()
        cursor.execute("SELECT COUNT(*) FROM lotes WHERE nroLotes=%s", (self.NumLotes.get(),))
        count = cursor.fetchone()[0]
        if count > 0:
            return True
        
    def guardar_datos(self):
        if self.NumLotes.get() == "" or self.fecha_inicio.get() == "" or self.fecha_fin.get() == "":
            messagebox.showerror("Control de Stock", "Ingrese información en todos los campos")
        else:

            fecha_sel_inicio = self.fecha_inicio.get_date()
            fecha_sel_fin = self.fecha_fin.get_date()
            fecha_mysql_inicio = fecha_sel_inicio.strftime('%Y-%m-%d')
            fecha_mysql_fin = fecha_sel_fin.strftime('%Y-%m-%d')
            
            conexion = pymysql.connect(host="localhost", user="root", password="123456", database="Krausebbdd")
            cursor = conexion.cursor()
            if self.new_id():
                conexion.close()
            else:
                cursor.execute("INSERT INTO lotes (nroLotes, cantidad, fecha_inicio, fecha_fin) VALUES (%s, %s, %s, %s)", (
                    self.NumLotes.get(),
                    self.cantidad.get(),
                    fecha_mysql_inicio,
                    fecha_mysql_fin,
                ))
                messagebox.showinfo("Datos Completados", "Se agregaron correctamente")

                conexion.commit()
                conexion.close()

                if self.callback:
                    self.callback()

                self.parent_lot.actualizar()
                self.dialog.destroy()
    
    
    def modificar_datos(self):
        if self.NumLotes.get() == "" or self.cantidad.get() == "":
            messagebox.showerror("Control de Stock", "Ingrese información en todos los campos")
        else:
            fecha_sel_inicio = self.fecha_inicio.get_date()
            fecha_sel_fin = self.fecha_fin.get_date()
            fecha_mysql_inicio = fecha_sel_inicio.strftime('%Y-%m-%d')
            fecha_mysql_fin = fecha_sel_fin.strftime('%Y-%m-%d')
            
            conexion = pymysql.connect(host="localhost", user="root", password="123456", database="Krausebbdd")
            cursor = conexion.cursor()
            if self.values[0] != self.NumLotes.get():
                if self.new_id():
                    self.dialog.after(0, lambda: messagebox.showerror("Control de Stock", "Ese número de etiqueta ya existe actualmente."))
                    return
                
            cursor.execute("UPDATE lotes SET nroLotes=%s, cantidad=%s,  fecha_inicio=%s,  fecha_fin=%s WHERE ID_Lotes=%s", (
                self.NumLotes.get(),
                self.cantidad.get(),
                fecha_mysql_inicio,
                fecha_mysql_fin,
                self.verify_id_LOT(),
            ))
            messagebox.showinfo("Datos Completados", "Se actualizaron correctamente")
    
            conexion.commit()
            conexion.close()

            if self.callback:
                self.callback()

            self.parent_lot.actualizar()
            self.dialog.destroy()           
