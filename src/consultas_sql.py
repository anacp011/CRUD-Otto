from tkinter import messagebox
import pymysql

class ConexionDB:
    def __init__(self,parent):
        self.parent = parent
        self.conexion= pymysql.connect(host="localhost", user="root", password="123456", database="Krausebbdd")
        self.cursor= self.conexion.cursor()
        
    def close(self):
        self.conexion.commit()
        self.conexion.close()
        
    def eliminar_MatPrim(self, values):
        numeroMatPrim = values[0]  # Accede al primer elemento de la tupla 'values'
        self.cursor.execute("SELECT ID_MatPrim FROM materias_primas WHERE nroMatPrim = %s", (numeroMatPrim,))
        result = self.cursor.fetchone()  # Obtiene el resultado de la consulta

        if result:
            Id_MatPrim = result[0]  # Obtiene el valor de ID_MatPrim del resultado de la consulta

            self.cursor.execute("DELETE FROM materias_primas WHERE ID_MatPrim = %s", (Id_MatPrim,))
            self.conexion.commit()  # Realiza el commit después de la operación de eliminación
            messagebox.showinfo("Producto Eliminado", "El producto ha sido eliminado exitosamente.")
        else:
            messagebox.showerror("Error", "No se encontró el producto para eliminarlo.")

    def eliminar_proveedor(self, values):
        numeroProvee = values[0]  # Accede al primer elemento de la tupla 'values'
        self.cursor.execute("SELECT ID_Provee FROM proveedores WHERE nroProvee = %s", (numeroProvee,))
        result = self.cursor.fetchone()  # Obtiene el resultado de la consulta

        if result:
            Id_Provee = result[0]  # Obtiene el valor de ID_Provee del resultado de la consulta

            self.cursor.execute("DELETE FROM proveedores WHERE ID_Provee = %s", (Id_Provee,))
            self.conexion.commit()  # Realiza el commit después de la operación de eliminación
            messagebox.showinfo("Proveedor Eliminado", "El proveedor ha sido eliminado exitosamente.")
        else:
            messagebox.showerror("Error", "No se encontró el proveedor para eliminarlo.")
    
    def eliminar_producto(self, values):
        numeroProd = values[0]  # Accede al primer elemento de la tupla 'values'
        self.cursor.execute("SELECT ID_Prod FROM productos WHERE nroProd = %s", (numeroProd,))
        result = self.cursor.fetchone()  # Obtiene el resultado de la consulta

        if result:
            Id_Prod = result[0]  # Obtiene el valor de ID_Prod del resultado de la consulta

            self.cursor.execute("DELETE FROM productos WHERE ID_Prod = %s", (Id_Prod,))
            self.conexion.commit()  # Realiza el commit después de la operación de eliminación
            messagebox.showinfo("Producto Eliminado", "El producto ha sido eliminado exitosamente.")
        else:
            messagebox.showerror("Error", "No se encontró el producto para eliminarlo.")
    
    def actualizar_proveedor(self):
        query = "SELECT nroProvee, nombre, contacto FROM proveedores"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        self.parent.vista(rows)
    
    def consulta_proveedor(self, q2):
        query = "SELECT nroProvee, nombre, contacto FROM proveedores WHERE nroProvee LIKE '%" + q2 + "%' OR nombre LIKE '%" + q2 + "%' "
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        self.parent.vista(rows)
        if not rows:
            messagebox.showerror("Error", f"No se pudo realizar la búsqueda")
        
    def exist_id_PR (self, Nro_proveedor):
        conexion = pymysql.connect(host="localhost", user="root", password="123456", database="Krausebbdd")
        cursor = conexion.cursor()
        
        cursor.execute("SELECT ID_Provee FROM proveedores WHERE nroProvee = %s", (Nro_proveedor,))
        result = cursor.fetchone()  # Obtiene el resultado de la consulta
        conexion.commit() 
        conexion.close()
        
        if result:
            codigo_proveedor = result[0]
            return codigo_proveedor
        else:
            messagebox.showerror("Control de Stock", "No existe ese ID de producto")
            return
    
    def exist_id_LOT (self, Nro_lotes):
        conexion = pymysql.connect(host="localhost", user="root", password="123456", database="Krausebbdd")
        cursor = conexion.cursor()
        
        cursor.execute("SELECT ID_Lotes FROM lotes WHERE nroLotes = %s", (Nro_lotes,))
        result = cursor.fetchone()  # Obtiene el resultado de la consulta
        conexion.commit() 
        conexion.close()
        
        if result:
            codigo_proveedor = result[0]
            return codigo_proveedor
        else:
            messagebox.showerror("Control de Stock", "No existe ese ID de lotes")
            return
        
    def eliminar_envases(self, values):
        numeroEnvases = values[0]  # Accede al primer elemento de la tupla 'values'
        self.cursor.execute("SELECT ID_Envases FROM envases WHERE nroEnvases = %s", (numeroEnvases,))
        result = self.cursor.fetchone()  # Obtiene el resultado de la consulta

        if result:
            Id_Envases = result[0]  # Obtiene el valor de ID_Provee del resultado de la consulta

            self.cursor.execute("DELETE FROM envases WHERE ID_Envases = %s", (Id_Envases,))
            self.conexion.commit()  # Realiza el commit después de la operación de eliminación
            messagebox.showinfo("Envase Eliminado", "El Envase ha sido eliminado exitosamente.")
        else:
            messagebox.showerror("Error", "No se encontró el Envase para eliminarlo.")

    def eliminar_etiquetas(self, values):
        numeroEtiquetas = values[0]  # Accede al primer elemento de la tupla 'values'
        self.cursor.execute("SELECT ID_Etiquetas FROM etiquetas WHERE nroEtiquetas = %s", (numeroEtiquetas,))
        result = self.cursor.fetchone()  # Obtiene el resultado de la consulta

        if result:
            Id_Etiquetas = result[0]  # Obtiene el valor de ID_Provee del resultado de la consulta

            self.cursor.execute("DELETE FROM etiquetas WHERE ID_Etiquetas = %s", (Id_Etiquetas,))
            self.conexion.commit()  # Realiza el commit después de la operación de eliminación
            messagebox.showinfo("Envase Eliminado", "El Envase ha sido eliminado exitosamente.")
        else:
            messagebox.showerror("Error", "No se encontró el Envase para eliminarlo.")
    
    def eliminar_lotes(self, values):
        numeroLotes = values[0]  # Accede al primer elemento de la tupla 'values'
        self.cursor.execute("SELECT ID_Lotes FROM lotes WHERE nroLotes = %s", (numeroLotes,))
        result = self.cursor.fetchone()  # Obtiene el resultado de la consulta

        if result:
            Id_Lotes = result[0]  # Obtiene el valor de ID_Provee del resultado de la consulta

            self.cursor.execute("DELETE FROM lotes WHERE ID_Lotes = %s", (Id_Lotes,))
            self.conexion.commit()  # Realiza el commit después de la operación de eliminación
            messagebox.showinfo("Envase Eliminado", "El Envase ha sido eliminado exitosamente.")
        else:
            messagebox.showerror("Error", "No se encontró el Envase para eliminarlo.")
    
    def actualizar_lotes(self):
        query = "SELECT nroLotes, cantidad, fecha_inicio, fecha_fin FROM lotes"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        self.parent.vista(rows)
    
    def consulta_lotes(self, q2):
        query = "SELECT nroLotes, cantidad, fecha_inicio, fecha_fin FROM lotes WHERE nroLotes LIKE '%" + q2 + "%' "
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        self.parent.vista(rows)
        if not rows:
            messagebox.showerror("Error", f"No se pudo realizar la búsqueda")