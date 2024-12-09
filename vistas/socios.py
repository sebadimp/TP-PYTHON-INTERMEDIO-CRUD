import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from vistas.principal import Frame
from tkinter import *
from datetime import datetime

import re
import sqlite3

def abrir_vista_socios(root):
    vista_socios = tk.Toplevel(root,width=800,height=800)
    vista_socios.title('Biblioteca - Socios')
    vista_socios.iconbitmap('image/biblioteca.ico')
    vista_socios.resizable(0,0)

    app = Frame_socios(root = vista_socios)
    app.config(background='grey')


class Frame_socios(Frame):

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
        self.marco = LabelFrame(self,text='Alta nueva')
        self.marco.grid(row=0,column=0,columnspan=2,padx=20,pady=20)


    def elementos_form(self):
        # # nombre
        Label(self.marco, text='Nombre: ').grid(row=1,column=0)
        self.nombre = Entry(self.marco)
        self.nombre.grid(row=1, column=1,padx=10)
        self.nombre.focus()

        # apellido
        Label(self.marco, text='Apellido: ').grid(row=2,column=0)
        self.apellido = Entry(self.marco)
        self.apellido.grid(row=2, column=1)

        # dni
        Label(self.marco, text='Dni: ').grid(row=3,column=0)
        self.dni = Entry(self.marco)
        self.dni.grid(row=3, column=1)

        # genero
        self.genero_var = tk.StringVar()
        self.genero_var.set("")  # Valor predeterminado
        Label(self.marco, text='Genero: ').grid(row=4,column=0)
        self.genero_masculino = Radiobutton(self.marco,text='Masculino', variable=self.genero_var, value="Masculino")
        self.genero_masculino.grid(row=4, column=1,sticky=W,padx=10)

        self.genero_femenino = Radiobutton(self.marco,text='Femenino', variable=self.genero_var, value="Femenino")
        self.genero_femenino.grid(row=5, column=1,sticky=W,padx=10)
        
        self.genero_otro = Radiobutton(self.marco,text='Otro', variable=self.genero_var, value="Otro")
        self.genero_otro.grid(row=6, column=1,sticky=W,padx=10)

        # email
        Label(self.marco, text='Email: ').grid(row=7,column=0)
        self.email = Entry(self.marco)
        self.email.grid(row=7, column=1)

        # fecha_alta
        Label(self.marco, text='Fecha Alta: ').grid(row=8,column=0)
        self.fecha_alta = Entry(self.marco)
        self.fecha_alta.grid(row=8, column=1)

    def validar_fecha(self):
        fecha = self.fecha_alta.get()
        # Expresión regular para el formato dd/mm/yyyy
        patron = r"^([0-2][0-9]|(3)[0-1])/(0[1-9]|1[0-2])/\d{4}$"

        if re.match(patron, fecha):
            try:
                datetime.strptime(fecha, "%d/%m/%Y")
                return True
            except ValueError:
                messagebox.showerror('Error!',"La fecha no es válida. Use dd/mm/yyyy.")
        else:
            messagebox.showerror('Error!',"El formato de la fecha es incorrecto. Use dd/mm/yyyy.")

    def validar_datos(self):
        return len(self.nombre.get()) != 0 and len(self.apellido.get()) != 0 and len(self.dni.get()) != 0 and len(self.email.get()) != 0 and self.validar_fecha() and len(self.genero_var.get()) != 0

    def botones_principales(self):
        # boton nuevo
        self.btn_nuevo = tk.Button(self.marco, text='Nuevo',command=self.habilitar_campos)
        self.btn_nuevo.config(width= 20,font=('Arial', 10,'bold'),fg ='#FFFFFF' ,bg='blue',cursor='hand2',activebackground='darkblue',activeforeground='white')
        self.btn_nuevo.grid(row=9,columnspan=2,padx=10,pady=3,sticky= W + E,)

        # boton guardar
        self.btn_guardar = tk.Button(self.marco, text='Guardar',command=self.agregar_socio)
        self.btn_guardar.config(width= 20,font=('Arial', 10,'bold'),fg ='#FFFFFF' ,bg='grey',cursor='hand2',activebackground='#3FD83F',activeforeground='#000000')
        self.btn_guardar.grid(row=10,columnspan=2,padx=10,pady=3,sticky= W + E)

        # boton editar
        self.btn_editar = tk.Button(self.marco, text='Editar',command=lambda:self.editar_socio(self.nombre.get(),self.apellido.get(),self.dni.get(),self.genero_var.get(),self.email.get(),self.fecha_alta.get()))
        self.btn_editar.config(width= 20,font=('Arial', 10,'bold'),fg ='#FFFFFF' ,bg='grey',cursor='hand2',activebackground='#3FD83F',activeforeground='#000000')
        self.btn_editar.grid(row=11,columnspan=2,padx=10,pady=3,sticky= W + E)

        # boton eliminar
        self.btn_eliminar = tk.Button(self.marco, text='Eliminar',command=self.eliminar_socio)
        self.btn_eliminar.config(width= 20,font=('Arial', 10,'bold'),fg ='#FFFFFF' ,bg='grey',cursor='hand2',activebackground='#3FD83F',activeforeground='#000000')
        self.btn_eliminar.grid(row=12,columnspan=2,padx=10,pady=3,sticky= W + E)

        # boton cancelar
        self.btn_cancelar = tk.Button(self.marco, text='Cancelar',command=self.bloquear_campos)
        self.btn_cancelar.config(width= 20,font=('Arial', 10,'bold'),fg ='#FFFFFF' ,bg='grey',cursor='hand2',activebackground='#3FD83F',activeforeground='#000000')
        self.btn_cancelar.grid(row=13,columnspan=2,padx=10,pady=3,sticky= W + E)

    def tabla_registros(self):
        # Tabla
        self.tree = ttk.Treeview(self,height=16,columns=('col0',"col1","col2","col3","col4","col5","col6"))
        self.tree.grid(row=0,column=2,padx=20)

        # Columnas
        self.tree.heading('#0', text="")
        self.tree.heading('col0', text="Id")        
        self.tree.heading('col1', text="Nombre")
        self.tree.heading('col2', text="Apellido")
        self.tree.heading('col3', text="Dni")
        self.tree.heading('col4', text="Genero")
        self.tree.heading('col5', text="Email")
        self.tree.heading('col6', text="Fecha Alta")

        self.tree.column('#0',width=0,stretch=tk.NO)
        self.tree.column("col0", width=0,stretch=tk.NO)
        self.tree.column("col1", width=150)
        self.tree.column("col2", width=150)
        self.tree.column("col3", width=100)
        self.tree.column("col4", width=100)
        self.tree.column("col5", width=150)
        self.tree.column("col6", width=100)

        #eventos
        self.tree.bind('<<TreeviewSelect>>',self.eventos_seleccion)


        self.listar_socios()

    #manejo de campos
    def habilitar_campos(self):
        self.nombre.delete(0, tk.END) 
        self.nombre.config(state='normal')
        self.apellido.delete(0, tk.END)
        self.apellido.config(state='normal')
        self.dni.delete(0, tk.END)
        self.dni.config(state='normal')
        self.genero_var.set(None)
        self.genero_masculino.config(state='normal')
        self.genero_femenino.config(state='normal')
        self.genero_otro.config(state='normal')
        self.email.delete(0, tk.END)
        self.email.config(state='normal')
        self.fecha_alta.delete(0, tk.END)
        self.fecha_alta.config(state='normal')
        self.btn_nuevo.config(state='disabled')
        self.btn_guardar.config(state='normal')
        self.btn_cancelar.config(state='normal')
        self.btn_editar.config(state='disabled')
        self.btn_eliminar.config(state='disabled')

    def bloquear_campos(self):
        self.nombre.delete(0, tk.END) 
        self.nombre.config(state='disabled')
        self.apellido.delete(0, tk.END)
        self.apellido.config(state='disabled')
        self.dni.delete(0, tk.END)
        self.dni.config(state='disabled')
        self.genero_var.set(None)
        self.genero_masculino.config(state='disabled')
        self.genero_femenino.config(state='disabled')
        self.genero_otro.config(state='disabled')
        self.email.delete(0, tk.END)
        self.email.config(state='disabled')
        self.fecha_alta.delete(0, tk.END)
        self.fecha_alta.config(state='disabled')
        self.btn_nuevo.config(state='normal')
        self.btn_guardar.config(state='disabled')
        self.btn_cancelar.config(state='disabled')
        self.btn_editar.config(state='disabled')
        self.btn_eliminar.config(state='disabled')

    def habilitar_edicion(self):
        item = self.tree.item(self.tree.selection())
        self.btn_editar.config(state='normal')

        
        self.nombre.config(state='normal')
        self.nombre.delete(0, tk.END)
        self.nombre.insert(0, item['values'][1])

        self.apellido.config(state='normal')
        self.apellido.delete(0, tk.END)
        self.apellido.insert(0, item['values'][2])

        self.dni.config(state='normal')
        self.dni.delete(0, tk.END)
        self.dni.insert(0, item['values'][3])

        self.genero_masculino.config(state='normal')
        self.genero_femenino.config(state='normal')
        self.genero_otro.config(state='normal')

        if item['values'][4] == "Masculino":
            self.genero_masculino.select()
        elif item['values'][4] == "Femenino":
            self.genero_femenino.select()
        else:
            self.genero_otro.select()
            
        self.email.config(state='normal')
        self.email.delete(0, tk.END)
        self.email.insert(0, item['values'][5])

        self.fecha_alta.config(state='normal')
        self.fecha_alta.delete(0, tk.END)
        self.fecha_alta.insert(0, item['values'][6]) 

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

    def listar_socios(self):
        #limpiar tabla
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        
        #consulta 
        query = 'SELECT * FROM socios ORDER BY id_socio DESC'
        db_rows= self.ejecutar_consulta(query)
                
        for row in db_rows:
            self.tree.insert('', 0, text=row[1], values=(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))

    def ejecutar_consulta(self, query, parameters = ()):
        with sqlite3.connect(self.nombre_bd) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def agregar_socio(self):
        if self.validar_datos():
            query = 'INSERT INTO socios VALUES(NULL,?,?,?,?,?,?)'
            parametros = (self.nombre.get(),self.apellido.get(),self.dni.get(),self.genero_var.get(),self.email.get(),self.fecha_alta.get())
            self.ejecutar_consulta(query, parametros)
            messagebox.showinfo('Resultado!','Se dio de alta al socio correctamente.')
            self.bloquear_campos()
        else:
            messagebox.showerror('Error!','Uno o mas campos incompletos')
        self.listar_socios()

    def eliminar_socio(self):
        try:
            item = self.tree.item(self.tree.selection())
            id_socio = item['values'][0]
            query = 'DELETE FROM socios WHERE id_socio= ?'
            self.ejecutar_consulta(query, (id_socio, ) )
            messagebox.showinfo('Resultado!','Se elimino el registro correctamente.')
            self.tree.selection_remove(self.tree.selection())
        except:
            self.bloquear_campos()
            return
        
        finally:
            self.bloquear_campos()
            self.listar_socios()

    def editar_socio(self,nombre_nuevo,apellido_nuevo,dni_nuevo,genero_nuevo,email_nuevo,fecha_alta_nuevo):
        try:
            item = self.tree.item(self.tree.selection())
            id_socio = item['values'][0]
            query = 'UPDATE socios SET nombre = ?, apellido= ?, dni= ?, genero= ?, email= ?,fecha_alta= ? WHERE id_socio= ?'
            parametros = (nombre_nuevo,apellido_nuevo,dni_nuevo,genero_nuevo,email_nuevo,fecha_alta_nuevo,id_socio)
            self.ejecutar_consulta(query,parametros)
            messagebox.showinfo('Resultado!','Se edito el registro correctamente.')
            self.tree.selection_remove(self.tree.selection())
        except:
            self.bloquear_campos()
            return
        
        finally:
            self.bloquear_campos()
            self.listar_socios()



