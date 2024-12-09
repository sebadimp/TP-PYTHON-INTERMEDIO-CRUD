import tkinter as tk
from tkinter import ttk
from vistas.frame import Frame
from .socios import abrir_vista_socios
from .prestamos import abrir_vista_prestamos
from .libros import abrir_vista_libros

class Frame_principal(Frame):
    def __init__(self, root = None):
        super().__init__(root)
        self.root = root
        self.grid()

        self.label_principal()
        self.opciones_principal(root)

    def label_principal(self):
        self.label_titulo = tk.Label(self, text="Biblioteca 3F")
        self.label_titulo.config(font=('Arial',15,'bold'))
        self.label_titulo.grid(row= 1, column=0,padx=10,pady=10, columnspan=4)
    
    def opciones_principal(self,root):
        self.btn_cliente = tk.Button(self, text='Socios',command=lambda: abrir_vista_socios(root))
        self.btn_cliente.config(width= 20,font=('Arial', 12,'bold'),fg ='#FFFFFF' , bg='blue',cursor='hand2',activebackground='#3FD83F',activeforeground='#000000')
        self.btn_cliente.grid(row= 2, column=0,padx=10,pady=10)

        self.btn_libros = tk.Button(self, text='Libros',command=lambda: abrir_vista_libros(root))
        self.btn_libros.config(width= 20,font=('Arial', 12,'bold'),fg ='#FFFFFF' , bg='red',cursor='hand2',activebackground='#3FD83F',activeforeground='#000000')
        self.btn_libros.grid(row= 2, column=1,padx=10,pady=10)

        self.btn_prestamos = tk.Button(self, text='Prestamos',command=lambda: abrir_vista_prestamos(root))
        self.btn_prestamos.config(width= 20,font=('Arial', 12,'bold'),fg ='#FFFFFF' , bg='#1C500B',cursor='hand2',activebackground='#3FD83F',activeforeground='#000000')
        self.btn_prestamos.grid(row= 2, column=2,padx=10,pady=10)