import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from vistas.principal import Frame
from tkinter import *
from datetime import datetime

import re
import sqlite3

def abrir_vista_libros(root):
    vista_libros = tk.Toplevel(root,width=800,height=800)
    vista_libros.title('Biblioteca - Libros')
    vista_libros.iconbitmap('image/biblioteca.ico')
    vista_libros.resizable(0,0)

    app = Frame_libros(root = vista_libros)
    app.config(background='grey')

class Frame_libros(Frame):

    nombre_bd = 'biblioteca.db'    

    def __init__(self, root = None):
        super().__init__(root,width=800,height=800)
        self.root = root
        self.grid()

        self.frame_form()
        self.elementos_form()
        self.botones_principales()
        self.tabla_registros()
        self.bloquear_campos()

    def frame_form(self):
        self.marco = LabelFrame(self,text='Ingreso Libro')
        self.marco.grid(row=0,column=0,columnspan=2,padx=20,pady=20)

    def elementos_form(self):
        # Nombre_libro
        Label(self.marco, text='Título: ').grid(row=1,column=0)
        self.nombre_libro = Entry(self.marco)
        self.nombre_libro.grid(row=1, column=1,padx=10)

        # Genero
        self.opciones = ["Fantasia","Terror","Thriller","Suspenso","Drama"]
        self.genero_seleccion = tk.StringVar()
        self.genero_seleccion.set(self.opciones[0])
        Label(self.marco, text='Genero: ').grid(row=2,column=0)
        self.genero =  OptionMenu(self.marco,self.genero_seleccion,*self.opciones)
        self.genero.grid(row=2, column=1)

        # Autor
        Label(self.marco, text='Autor: ').grid(row=3,column=0)
        self.autor = Entry(self.marco)
        self.autor.grid(row=3, column=1,padx=10)

    def validar_campos(self):
        return len(self.nombre_libro.get()) != 0 and len(self.autor.get()) != 0 and self.genero_seleccion.get() != "SELECCIONAR"
    
    def botones_principales(self):
        # boton nuevo
        self.btn_nuevo = tk.Button(self.marco, text='Nuevo',command=self.habilitar_campos)
        self.btn_nuevo.config(width= 20,font=('Arial', 10,'bold'),fg ='#FFFFFF' ,bg='blue',cursor='hand2',activebackground='darkblue',activeforeground='white')
        self.btn_nuevo.grid(row=9,columnspan=2,padx=10,pady=3,sticky= W + E,)

        # boton guardar
        self.btn_guardar = tk.Button(self.marco, text='Guardar',command=self.agregar_libro)
        self.btn_guardar.config(width= 20,font=('Arial', 10,'bold'),fg ='#FFFFFF' ,bg='grey',cursor='hand2',activebackground='#3FD83F',activeforeground='#000000')
        self.btn_guardar.grid(row=10,columnspan=2,padx=10,pady=3,sticky= W + E)

        # boton editar
        self.btn_editar = tk.Button(self.marco, text='Editar',command=lambda:self.editar_libro(self.nombre_libro.get(),self.genero_seleccion.get(),self.autor.get()))
        self.btn_editar.config(width= 20,font=('Arial', 10,'bold'),fg ='#FFFFFF' ,bg='grey',cursor='hand2',activebackground='#3FD83F',activeforeground='#000000')
        self.btn_editar.grid(row=11,columnspan=2,padx=10,pady=3,sticky= W + E)

        # boton eliminar
        self.btn_eliminar = tk.Button(self.marco, text='Eliminar',command=self.eliminar_libro)
        self.btn_eliminar.config(width= 20,font=('Arial', 10,'bold'),fg ='#FFFFFF' ,bg='grey',cursor='hand2',activebackground='#3FD83F',activeforeground='#000000')
        self.btn_eliminar.grid(row=12,columnspan=2,padx=10,pady=3,sticky= W + E)

        # boton cancelar
        self.btn_cancelar = tk.Button(self.marco, text='Cancelar',command=self.bloquear_campos)
        self.btn_cancelar.config(width= 20,font=('Arial', 10,'bold'),fg ='#FFFFFF' ,bg='grey',cursor='hand2',activebackground='#3FD83F',activeforeground='#000000')
        self.btn_cancelar.grid(row=13,columnspan=2,padx=10,pady=3,sticky= W + E)


    def tabla_registros(self):
        # Tabla    
        self.tree = ttk.Treeview(self,height=12,columns=('col0',"col1","col2","col3"))
        self.tree.grid(row=0,column=2,padx=20)

        # Columnas
        self.tree.heading('#0', text="")
        self.tree.heading('col0', text="Id")
        self.tree.heading('col1', text="Titulo")        
        self.tree.heading('col2', text="Genero")
        self.tree.heading('col3', text="Autor")

        self.tree.column('#0',width=0,stretch=tk.NO)
        self.tree.column("col0", width=0,stretch=tk.NO)
        self.tree.column("col1", width=100)
        self.tree.column("col2", width=100)
        self.tree.column("col3", width=100)

        #eventos
        self.tree.bind('<<TreeviewSelect>>',self.eventos_seleccion)


        self.listar_libros()

    #manejo de campos
    def habilitar_campos(self):
        
        self.nombre_libro.delete(0, tk.END)
        self.nombre_libro.config(state='normal')

        self.genero_seleccion.set("SELECCIONAR")
        self.genero.config(state='normal')

        self.autor.delete(0, tk.END)
        self.autor.config(state='normal')

        self.btn_nuevo.config(state='disabled')
        self.btn_guardar.config(state='normal')
        self.btn_cancelar.config(state='normal')
        self.btn_editar.config(state='disabled')
        self.btn_eliminar.config(state='disabled')

    def bloquear_campos(self):
        self.nombre_libro.delete(0, tk.END)
        self.nombre_libro.config(state="disabled")
        self.genero_seleccion.set("SELECCIONAR")
        self.genero.config(state='disabled')
        self.autor.delete(0, tk.END)
        self.autor.config(state='disabled')

        self.btn_nuevo.config(state='normal')
        self.btn_guardar.config(state='disabled')
        self.btn_cancelar.config(state='disabled')
        self.btn_editar.config(state='disabled')
        self.btn_eliminar.config(state='disabled')

    def habilitar_edicion(self):
        item = self.tree.item(self.tree.selection())
        self.btn_editar.config(state='normal')

        self.nombre_libro.config(state='normal')
        self.nombre_libro.delete(0, tk.END)
        self.nombre_libro.insert(0, item['values'][1])

        self.genero.config(state='normal')
        self.genero_seleccion.set(item['values'][2])

        self.autor.config(state='normal')
        self.autor.delete(0, tk.END)
        self.autor.insert(0, item['values'][3])

    def habilitar_eliminar(self):
        self.btn_eliminar.config(state='normal')


    def eventos_seleccion(self, event):
        selected_item = self.tree.selection()

        if selected_item:
            self.habilitar_eliminar() 
            self.habilitar_edicion()  
        else:
            self.bloquear_campos()

    # FUNCIONES PARA EL CRUD

    def listar_libros(self):
        #limpiar tabla
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        
        #consulta 
        query = 'SELECT * FROM libros ORDER BY id_libro DESC'
        db_rows= self.ejecutar_consulta(query)
                
        for row in db_rows:
            self.tree.insert('', 0, text=row[1], values=(row[0],row[1],row[2],row[3]))

    def ejecutar_consulta(self, query, parameters = ()):
        with sqlite3.connect(self.nombre_bd) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result
    
    def agregar_libro(self):
        if self.validar_campos():
            query = 'INSERT INTO libros VALUES(NULL,?,?,?)'
            parametros = (self.nombre_libro.get(),self.genero_seleccion.get(),self.autor.get())
            self.ejecutar_consulta(query, parametros)
            messagebox.showinfo('Resultado!','Se ingreso el Libro correctamente.')
            self.bloquear_campos()
        else:
            messagebox.showerror('Error!','Uno o mas campos incompletos')
        self.listar_libros()

    def eliminar_libro(self):
        try:
            item = self.tree.item(self.tree.selection())
            id_libro = item['values'][0]
            query = 'DELETE FROM libros WHERE id_libro= ?'
            self.ejecutar_consulta(query, (id_libro, ) )
            messagebox.showinfo('Resultado!','Se elimino el registro correctamente.')
            self.tree.selection_remove(self.tree.selection())
        except:
            self.bloquear_campos()
            return
        
        finally:
            self.bloquear_campos()
            self.listar_libros()

    def editar_libro(self,nombre_nuevo,genero_nuevo,autor_nuevo):
        try:
            item = self.tree.item(self.tree.selection())
            id_libro = item['values'][0]
            query = 'UPDATE libros SET nombre = ?, genero= ?, autor= ? WHERE id_libro= ?'
            parametros = (nombre_nuevo,genero_nuevo,autor_nuevo,id_libro)
            self.ejecutar_consulta(query,parametros)
            messagebox.showinfo('Resultado!','Se edito el registro correctamente.')
            self.tree.selection_remove(self.tree.selection())
        except:
            self.bloquear_campos()
            return
        
        finally:
            self.bloquear_campos()
            self.listar_libros()