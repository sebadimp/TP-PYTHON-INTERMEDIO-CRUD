import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from vistas.principal import Frame
from tkinter import *
from datetime import datetime

import re
import sqlite3 as sq3



def abrir_vista_prestamos(root):
    vista_prestamos = tk.Toplevel(root,width=800,height=800)
    vista_prestamos.title('Biblioteca - Prestamos')
    vista_prestamos.iconbitmap('image/biblioteca.ico')
    vista_prestamos.resizable(0,0)

    app = Frame_prestamos(root = vista_prestamos)
    app.config(background='grey')

class Frame_prestamos(Frame):

    nombre_bd = 'biblioteca.db'    

    def __init__(self, root = None):
        super().__init__(root,width=800,height=800)
        self.root = root
        self.grid()
        self.id_socio = None
        self.id_libro = None

        self.frame_form()
        self.elementos_form()
        self.botones_principales()
        self.tabla_registros()
        self.bloquear_campos()

    def frame_form(self):
        self.marco = LabelFrame(self,text='Prestamos')
        self.marco.grid(row=0,column=0,columnspan=2,padx=20,pady=20)


    def elementos_form(self):
        # Id Prestamo
        Label(self.marco, text='Id Prestamo: ').grid(row=1,column=0)
        self.id_prestamo = Entry(self.marco)
        self.id_prestamo.grid(row=1, column=1,padx=10)

        # Id socio
        self.socio_seleccion = tk.StringVar()
        opciones_socio = self.buscar_socios()        
        Label(self.marco, text='Socio: ').grid(row=2,column=0)
        self.socio = OptionMenu(self.marco,self.socio_seleccion,*opciones_socio)
        self.socio.grid(row=2, column=1)
        try:
            self.id_socio = self.socio_seleccion.get().split(' -')[0]
        except:
            pass

        # Id libro
        self.libro_seleccion = tk.StringVar()
        opciones_libro = self.buscar_libros()
        Label(self.marco, text='Libro: ').grid(row=3,column=0)
        self.libro = OptionMenu(self.marco,self.libro_seleccion,*opciones_libro)
        self.libro.grid(row=3, column=1)


        # fecha_prestamo
        Label(self.marco, text='Fecha Prestamo: ').grid(row=4,column=0)
        self.fecha_prestamo = Entry(self.marco)
        self.fecha_prestamo.grid(row=4, column=1)

        # fecha_devolucion
        Label(self.marco, text='Fecha Devolución: ').grid(row=5,column=0)
        self.fecha_devolucion = Entry(self.marco)
        self.fecha_devolucion.grid(row=5, column=1)

        # estado
        self.opciones = ["PENDIENTE","DEVUELTO"]
        self.estado_variable = tk.StringVar()
        self.estado_variable.set(self.opciones[0])
        Label(self.marco, text='Estado: ').grid(row=6,column=0)
        self.estado =  OptionMenu(self.marco,self.estado_variable,*self.opciones)
        self.estado.grid(row=6, column=1)




    def validar_fecha(self, fecha):
        self.fecha = fecha

        patron = r"^([0-2][0-9]|(3)[0-1])/(0[1-9]|1[0-2])/\d{4}$"

        if re.match(patron, fecha):
            try:
                datetime.strptime(fecha, "%d/%m/%Y")
                return True
            except ValueError:
                messagebox.showerror('Error!',"La fecha no es válida. Use dd/mm/yyyy.")
        else:
            messagebox.showerror('Error!',"El formato de la fecha es incorrecto. Use dd/mm/yyyy.")        



    def validar_campos(self):
        return len(self.socio_seleccion.get()) != 0 and len(self.libro_seleccion.get()) != 0 and self.validar_fecha(self.fecha_prestamo.get()) and self.estado_variable.get() != "SELECCIONAR"        

    def botones_principales(self):
        # boton nuevo
        self.btn_nuevo = tk.Button(self.marco, text='Nuevo',command=self.habilitar_campos)
        self.btn_nuevo.config(width= 20,font=('Arial', 10,'bold'),fg ='#FFFFFF' ,bg='blue',cursor='hand2',activebackground='darkblue',activeforeground='white')
        self.btn_nuevo.grid(row=9,columnspan=2,padx=10,pady=3,sticky= W + E,)

        # boton guardar
        self.btn_guardar = tk.Button(self.marco, text='Guardar',command=self.agregar_prestamo)
        self.btn_guardar.config(width= 20,font=('Arial', 10,'bold'),fg ='#FFFFFF' ,bg='grey',cursor='hand2',activebackground='#3FD83F',activeforeground='#000000')
        self.btn_guardar.grid(row=10,columnspan=2,padx=10,pady=3,sticky= W + E)

        # boton editar
        self.btn_editar = tk.Button(self.marco, text='Editar',command=lambda:self.editar_prestamo(self.socio_seleccion.get().split(' -')[0],self.libro_seleccion.get().split(' -')[0],self.fecha_prestamo.get(),self.fecha_devolucion.get(),self.estado_variable.get()))
        self.btn_editar.config(width= 20,font=('Arial', 10,'bold'),fg ='#FFFFFF' ,bg='grey',cursor='hand2',activebackground='#3FD83F',activeforeground='#000000')
        self.btn_editar.grid(row=11,columnspan=2,padx=10,pady=3,sticky= W + E)

        # boton eliminar
        self.btn_eliminar = tk.Button(self.marco, text='Eliminar',command=self.eliminar_prestamo)
        self.btn_eliminar.config(width= 20,font=('Arial', 10,'bold'),fg ='#FFFFFF' ,bg='grey',cursor='hand2',activebackground='#3FD83F',activeforeground='#000000')
        self.btn_eliminar.grid(row=12,columnspan=2,padx=10,pady=3,sticky= W + E)

        # boton cancelar
        self.btn_cancelar = tk.Button(self.marco, text='Cancelar',command=self.bloquear_campos)
        self.btn_cancelar.config(width= 20,font=('Arial', 10,'bold'),fg ='#FFFFFF' ,bg='grey',cursor='hand2',activebackground='#3FD83F',activeforeground='#000000')
        self.btn_cancelar.grid(row=13,columnspan=2,padx=10,pady=3,sticky= W + E)

    def tabla_registros(self):
        # Tabla
        self.tree = ttk.Treeview(self,height=16,columns=('col0',"col1","col2","col3","col4","col5","col6","col7","col8"))
        self.tree.grid(row=0,column=2,padx=20)

        # Columnas
        self.tree.heading('#0', text="")
        self.tree.heading('col0', text="Id Prestamo")        
        self.tree.heading('col1', text="Id Socio")
        self.tree.heading('col2', text="Nombre")
        self.tree.heading('col3', text="Apellido")
        self.tree.heading('col4', text="Id Libro")
        self.tree.heading('col5', text="Libro")
        self.tree.heading('col6', text="Fecha Prestamo")
        self.tree.heading('col7', text="Fecha Devolución")
        self.tree.heading('col8', text="Estado")

        self.tree.column('#0',width=0,stretch=tk.NO)
        self.tree.column("col0", width=80)
        self.tree.column("col1", width=50)
        self.tree.column("col2", width=100)
        self.tree.column("col3", width=100)
        self.tree.column("col4", width=50)
        self.tree.column("col5", width=100)
        self.tree.column("col6", width=100)
        self.tree.column("col7", width=120)
        self.tree.column("col8", width=80)


        #eventos
        self.tree.bind('<<TreeviewSelect>>',self.eventos_seleccion)

        self.listar_prestamos()

    #manejo de campos
    def habilitar_campos(self):
        self.id_prestamo.config(state="normal")
        self.id_prestamo.delete(0, tk.END)
        self.id_prestamo.config(state="readonly")
        self.socio_seleccion.set("SELECCIONAR")
        self.socio.config(state='normal')
        self.libro_seleccion.set("SELECCIONAR")
        self.libro.config(state='normal')
        self.fecha_prestamo.delete(0, tk.END)
        self.fecha_prestamo.config(state='normal')
        self.fecha_devolucion.delete(0, tk.END)
        self.fecha_devolucion.config(state='normal')
        self.estado_variable.set("SELECCIONAR")
        self.estado.config(state='normal')
        self.btn_nuevo.config(state='disabled')
        self.btn_guardar.config(state='normal')
        self.btn_cancelar.config(state='normal')
        self.btn_editar.config(state='disabled')
        self.btn_eliminar.config(state='disabled')

    def bloquear_campos(self):
        self.id_prestamo.config(state="disabled")
        self.socio_seleccion.set("SELECCIONAR")
        self.socio.config(state='disabled')
        self.libro_seleccion.set("SELECCIONAR")
        self.libro.config(state='disabled')
        self.fecha_prestamo.delete(0, tk.END)
        self.fecha_prestamo.config(state='disabled')
        self.fecha_devolucion.delete(0, tk.END)
        self.fecha_devolucion.config(state='disabled')
        self.estado_variable.set("SELECCIONAR")
        self.estado.config(state='disabled')
        self.btn_nuevo.config(state='normal')
        self.btn_guardar.config(state='disabled')
        self.btn_cancelar.config(state='disabled')
        self.btn_editar.config(state='disabled')
        self.btn_eliminar.config(state='disabled')

    def habilitar_edicion(self):
        item = self.tree.item(self.tree.selection())
        self.btn_editar.config(state='normal')
        
        self.id_prestamo.config(state='normal')
        self.id_prestamo.delete(0, tk.END)
        self.id_prestamo.insert(0, item['values'][0])
        self.id_prestamo.config(state='readonly')        

        self.socio.config(state='normal')
        self.socio_seleccion.set(f"{item['values'][1]} - {item['values'][2]} {item['values'][3]}")

        self.libro.config(state='normal')
        self.libro_seleccion.set(f"{item['values'][4]} - {item['values'][5]}")

        self.fecha_prestamo.config(state='normal')
        self.fecha_prestamo.delete(0, tk.END)
        self.fecha_prestamo.insert(0, item['values'][6])

        self.fecha_devolucion.config(state='normal')
        self.fecha_devolucion.delete(0, tk.END)
        self.fecha_devolucion.insert(0, item['values'][7])

        self.estado.config(state='normal')
        self.estado_variable.set(item['values'][8])

    def habilitar_eliminar(self):
        self.btn_eliminar.config(state='normal')


    def eventos_seleccion(self, event):
        selected_item = self.tree.selection()
        
        if selected_item:
            self.habilitar_eliminar() 
            self.habilitar_edicion()   
        else:
            self.bloquear_campos()


#### FUNCIONES CRUD ######

    def listar_prestamos(self):
        #limpiar tabla
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        
        #consulta 
        query = '''SELECT prestamos.id_prestamo, prestamos.id_socio, socios.nombre, socios.apellido, prestamos.id_libro, libros.nombre, prestamos.fecha_prestamo, prestamos.fecha_devolucion, prestamos.estado
        FROM (prestamos INNER JOIN libros ON prestamos.id_libro = libros.id_libro) INNER JOIN socios ON prestamos.id_socio = socios.id_socio ORDER BY prestamos.id_prestamo DESC''' 
        db_rows= self.ejecutar_consulta(query)
                
        for row in db_rows:
            self.tree.insert('', 0, text=row[1], values=(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8]))

    def ejecutar_consulta(self, query, parameters = ()):
        with sq3.connect(self.nombre_bd) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result
    
    def buscar_socios(self):
        query = "SELECT id_socio,nombre,apellido FROM socios ORDER BY id_socio ASC"
        resultado = self.ejecutar_consulta(query)
        lista_socios =[]
        for e in resultado:
            socio = f"{e[0]} - {e[1]} {e[2]}"
            lista_socios.append(socio)

        return lista_socios

    def buscar_libros(self):
        query = "SELECT id_libro,nombre FROM libros ORDER BY id_libro ASC"
        resultado = self.ejecutar_consulta(query)
        lista_libros =[]

        for e in resultado:
            libro = f"{e[0]} - {e[1]}"
            lista_libros.append(libro)

        return lista_libros
        
    def agregar_prestamo(self):
        if self.validar_campos():
            self.id_socio = self.socio_seleccion.get().split(' -')[0]
            self.id_libro = self.libro_seleccion.get().split(' -')[0]
            query = 'INSERT INTO prestamos VALUES(NULL,?,?,?,?,?)'
            parametros = (self.id_socio,self.id_libro,self.fecha_prestamo.get(),self.fecha_devolucion.get(),self.estado_variable.get())
            self.ejecutar_consulta(query, parametros)
            messagebox.showinfo('Resultado!','Prestamo Efectuado.')
            self.bloquear_campos()
        else:
            messagebox.showerror('Error!','Uno o mas campos incompletos')
        self.listar_prestamos()

    def editar_prestamo(self,id_socio_nuevo,id_libro_nuevo,fecha_prestamo_nuevo,fecha_devolucion,estado_nuevo):
        try:
            item = self.tree.item(self.tree.selection())
            id_prestamo = item['values'][0]
            query = 'UPDATE prestamos SET id_socio= ?, id_libro= ?, fecha_prestamo= ?, fecha_devolucion= ?, estado= ? WHERE id_prestamo= ?'
            parametros = (id_socio_nuevo,id_libro_nuevo,fecha_prestamo_nuevo,fecha_devolucion,estado_nuevo,id_prestamo)
            self.ejecutar_consulta(query,parametros)
            messagebox.showinfo('Resultado!','Se Actualizo el prestamo.')
            self.tree.selection_remove(self.tree.selection())
        except:
            self.bloquear_campos()
            return
        
        finally:
            self.bloquear_campos()
            self.listar_prestamos()

    def eliminar_prestamo(self):
        try:
            item = self.tree.item(self.tree.selection())
            id_prestamo = item['values'][0]
            query = 'DELETE FROM prestamos WHERE id_prestamo= ?'
            self.ejecutar_consulta(query, (id_prestamo, ) )
            messagebox.showinfo('Resultado!','Se elimino el registro correctamente.')
            self.tree.selection_remove(self.tree.selection())
        except:
            self.bloquear_campos()
            return
        
        finally:
            self.bloquear_campos()
            self.listar_prestamos()