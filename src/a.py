#Importaciones
import tkinter as tk

#---VENTANA PRINCIPAL----> root

#Creación de la ventana principal
root = tk.Tk()
#Título de la ventana
root.title("Curso de Tkinter de Programación Fácil")

root.geometry()

#Ajustes de ventana y pantalla
root.eval('tk::PlaceWindow . center')

#---WIDGETS----> root

#Entrada de datos
entrada = tk.Entry(root).pack()

#Botón de enviar
boton = tk.Button(root, text="Enviar").pack()

#Bucle de ejecución
root.mainloop()