import tkinter as tk
from vistas.principal import Frame_principal

def main():
    ventana = tk.Tk()
    ventana.title('Sistema de Prestamos')
    ventana.iconbitmap('image/biblioteca.ico')
    ventana.resizable(0,0)

    app = Frame_principal(root = ventana)

    ventana.mainloop()

if __name__ == '__main__':
    main()