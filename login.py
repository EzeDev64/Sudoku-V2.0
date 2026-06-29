import hashlib
import random
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog

from JSONParser import JsonParser
from mail import EnvioCorreo
from user import User

class loginWindow(tk.Toplevel):
    def __init__(self,parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Sudoku")
        self.geometry("600x450")
        self.resizable(False, False)

        self.json = JsonParser()
        self.usuario = None

        self.createIGU()

    def createIGU(self):
        frame_top = tk.Frame(self,bd=2)
        frame_top.pack(fill="x", padx=15, pady=10)

        label_titulo = tk.Label(frame_top, text="Sudoku",fg="red")
        label_titulo.pack(pady=10)  

        frame_medium = tk.Frame(self,bd=1)
        frame_medium.pack(fill="both", expand=True, padx=15, pady=5)

        # Fila para el Correo (Label a la izquierda, Entry a la derecha)
        lbl_correo = tk.Label(frame_medium, text="Correo:")
        lbl_correo.grid(row=0, column=0, sticky="e", padx=15, pady=15)

        self.entry_correo = tk.Entry(frame_medium, font=("Arial", 11), width=22, bd=2)
        self.entry_correo.grid(row=0, column=1, padx=15, pady=15, sticky="w")
        
        lbl_codigo = tk.Label(frame_medium, text="Código:")
        lbl_codigo.grid(row=1, column=0, sticky="e", padx=15, pady=10)

        self.entry_codigo = tk.Entry(frame_medium, font=("Arial", 11), width=22, bd=2, state="disabled") #show="*") # Oculta caracteres
        self.entry_codigo.grid(row=1, column=1, padx=15, pady=10, sticky="w")

        btn_cod = tk.Button(frame_medium, text="Solicitar código", padx=10, pady=5,command=self.verificar_correo)
        btn_cod.grid(row=2, column=0, columnspan=2, pady=15)
        self.btn_iniciar = tk.Button(frame_medium, text="Iniciar sesión",padx=10, pady=5,state="disabled",command=self.verificar_codigo)
        self.btn_iniciar.grid(row=3, column=0, columnspan=2, pady=15)

        # Centrar las columnas dentro del Frame Medio para que no se recuesten a un lado
        frame_medium.grid_columnconfigure(0, weight=1)
        frame_medium.grid_columnconfigure(1, weight=1)

        frame_bottom = tk.Frame(self,bg="#f0f4f8")
        frame_bottom.pack(fill="x", padx=15, pady=10)

        # El botón salir se alinea a la derecha (side="right")
        btn_salir = tk.Button(frame_bottom, text="Salir", padx=15, pady=4, command= self.salir)
        btn_salir.pack(side="right")
        #nombre = simpledialog.askstring("Registro", "¿Cuál es tu nombre?")
        #print(nombre)

    def verificar_correo(self):
        correo = self.entry_correo.get()
        if correo.find("@gmail.com") == -1:
            messagebox.showinfo("Sudoku","Ingrese una dirección de correo válida")
            return            

        self.json.nombre_archivo = "usuarios.json"
        data = self.json.cargar_user(correo)
        if data == None:
            anwser = messagebox.askyesno("Sudoku","Correo no registrado, ¿desea crear una cuenta?")
            if anwser:
                self.crear_usuario()
        else:
            self.btn_iniciar.config(state="normal")
            self.entry_codigo.config(state="normal")

            codigo = str(random.randint(0, 999999)).zfill(6)
            texto_en_bytes = codigo.encode('utf-8')
            objeto_hash = hashlib.sha256(texto_en_bytes)
            
            self.usuario = User(data["id"],data["correo"],objeto_hash.hexdigest(),data["nombre"],data["fecha"],data["elements"])
            correo = EnvioCorreo(codigo,data["correo"])

    def verificar_codigo(self):
        codigo = self.entry_codigo.get()
        coded = codigo.encode('utf-8')
        hashObj = hashlib.sha256(coded)

        if hashObj.hexdigest() != self.usuario.codigo_ingreso:
            messagebox.showinfo("Sudoku","Código de ingreso incorrecto, verifique su correo e intente nuevamente")
        else:
            messagebox.showinfo("Sudoku",f"Bienvenido {self.usuario.nombre}")
            self.aceptar_cambios()

    def crear_usuario(self):
        correo = simpledialog.askstring("Sudoku", "Ingrese su correo")
        if correo == None:
            correo = ""

        if correo.find("@gmail.com") == -1:
            messagebox.showinfo("Sudoku","Ingrese una dirección de correo válida")
            return
        
        nombre = simpledialog.askstring("Sudoku", "Ingrese su nombre de usuario")
        if nombre == "" or nombre == None:
            messagebox.showinfo("Sudoku","Ingrese un username válido")
            return
        
        id_user = 0
        data = self.json.read()
        for id in data:
            id_user = id
        id_user = int(id_user)+1

        print(id_user)
        self.entry_correo.config(textvariable=tk.StringVar(value=correo))
        self.json.salvar_user(User(id_user,correo,0,nombre,"26/6/2026",{}))
        self.verificar_correo()        

    def aceptar_cambios(self):
        self.parent.recibir_login(self.usuario)
        self.salir()

    def salir(self):
        #Regresar a la pantalla principal
        self.parent.deiconify()
        self.destroy()