import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog

class loginWindow(tk.Toplevel):
    def __init__(self,parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Sudoku")
        self.geometry("600x450")
        self.resizable(False, False)

        self.createIGU()

    def createIGU(self):
        frame_top = tk.Frame(self,bd=2)
        frame_top.pack(fill="x", padx=15, pady=10)

        label_titulo = tk.Label(frame_top, text="Sudoku",fg="red")
        label_titulo.pack(pady=10)  

        frame_medium = tk.Frame(self,bd=1)
        frame_medium.pack(fill="both", expand=True, padx=15, pady=5)

        # Fila para el Correo (Label a la izquierda, Entry a la derecha)
        label_correo = tk.Label(frame_medium, text="Correo:")
        label_correo.grid(row=0, column=0, sticky="e", padx=15, pady=15)

        entry_correo = tk.Entry(frame_medium, font=("Arial", 11), width=22, bd=2)
        entry_correo.grid(row=0, column=1, padx=15, pady=15, sticky="w")
        
        label_codigo = tk.Label(frame_medium, text="Código:")
        label_codigo.grid(row=1, column=0, sticky="e", padx=15, pady=10)

        entry_codigo = tk.Entry(frame_medium, font=("Arial", 11), width=22, bd=2, show="*") # Oculta caracteres
        entry_codigo.grid(row=1, column=1, padx=15, pady=10, sticky="w")

        btn_iniciar = tk.Button(frame_medium, text="Iniciar sesión",padx=10, pady=5)
        btn_iniciar.grid(row=2, column=0, columnspan=2, pady=15)

        # Centrar las columnas dentro del Frame Medio para que no se recuesten a un lado
        frame_medium.grid_columnconfigure(0, weight=1)
        frame_medium.grid_columnconfigure(1, weight=1)

        frame_bottom = tk.Frame(self,bg="#f0f4f8")
        frame_bottom.pack(fill="x", padx=15, pady=10)

        # El botón salir se alinea a la derecha (side="right")
        btn_salir = tk.Button(frame_bottom, text="Salir", padx=15, pady=4, command= self.salir)
        btn_salir.pack(side="right")
        nombre = simpledialog.askstring("Registro", "¿Cuál es tu nombre?")
        print(nombre)

    def salir(self):
        #Regresar a la pantalla principal
        self.parent.deiconify()
        self.destroy()