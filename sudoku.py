import os
import tkinter as tk
from tkinter import messagebox
# Importamos la interfaz que creamos anteriormente
from config import configWindow
from game import gameWindow
from login import loginWindow
from partida import Partida
from user import User
from JSONParser import JsonParser

class MenuPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sudoku")
        self.geometry("600x450")
        self.resizable(False, False)
        self.MAPEO_NUMEROS = {1:1,2:2,3:3,4:4,5:5,6:6,7:7,8:8,9:9,-1:" "}
        self.MAPEO_LETRAS = {1: "A", 2: "B", 3: "C",4: "D", 5: "E", 6: "F",7: "G", 8: "H", 9: "I", -1: " "}

        #Datos de configuración
        self.clk = "crono"
        self.segundos_totales = 0
        self.dificultad = "Facil"
        self.elementos = True
        self.ntop = 0
        self.element_list = {1:"",2:"",3:"",4:"",5:"",6:"",7:"",8:"",9:"",-1:" "}

        #Usuario y partidas
        json = JsonParser()
        json.nombre_archivo = "usuarios.json"
        file = json.read()   

        data = file["1"]
        #print(data)

        #Recordar que el usuario se crea según lo que pase el login al iniciar sesión
        self.usuario = User(1,data["correo"],data["codigo_ingreso"],data["nombre"],data["fecha_creacion"],data["costum_elements"]) #Revisar lo de la id
        self.partida = Partida(self.usuario.nombre,-1,"dificil")
        """
        self.pIntermedia = Partida(self.usuario)
        self.pFacil = Partida()
        """
        self.crear_interfaz()

    def crear_interfaz(self):
        #Título
        frame_titulo = tk.Frame(self, padx=20, pady=10,)
        frame_titulo.pack(pady=40)
        
        lbl_title = tk.Label(frame_titulo, text="SUDOKU",fg="#e31b1b")
        lbl_title.pack()

        #Botones
        frame_botones = tk.Frame(self, bg="#f0f0f0")
        frame_botones.pack(pady=10)

        btn_jugar = tk.Button(frame_botones, text="JUGAR",command=self.abrir_juego)
        btn_jugar.pack(pady=10)

        btn_configurar = tk.Button(frame_botones, text="CONFIGURAR", command=self.abrir_configuracion)
        btn_configurar.pack(pady=10)

        btn_ayuda = tk.Button(frame_botones, text="AYUDA",command=self.abrir_ayuda)
        btn_ayuda.pack(pady=10)

        btn_acerca_de = tk.Button(frame_botones, text="ACERCA DE",command=self.abrir_acerca_de)
        btn_acerca_de.pack(pady=10)

        btn_salir = tk.Button(frame_botones, text="SALIR",command=self.quit)
        btn_salir.pack(pady=10)
    
    def abrir_login(self):
        self.withdraw() 

        ventana_login = loginWindow(self)
        ventana_login.protocol("WM_DELETE_WINDOW", self.quit)

    def abrir_juego(self):
        self.withdraw()
        
        lista_ele = self.element_list
        if any(valor == "" for valor in self.element_list.values()):
            lista_ele = self.MAPEO_NUMEROS

        Pdata = {"dif":self.dificultad, "clk": self.clk, "ele":lista_ele,
            "top":self.ntop,"time": self.segundos_totales, "partida": self.partida}
        print(Pdata)

        ventana_juego = gameWindow(self,self.elementos,Pdata)
        ventana_juego.protocol("WM_DELETE_WINDOW", self.quit)

    def abrir_configuracion(self):
        self.withdraw() 

        ventana_juego = configWindow(self,self.element_list)
        ventana_juego.protocol("WM_DELETE_WINDOW", self.quit)

    def abrir_ayuda(self):
        os.startfile('Manual de usuario Sudoku.pdf')

    def abrir_acerca_de(self):
        messagebox.showinfo("Acerca de", "Sudoku 2026\nVersión: 1.0\nTaller de Programación\nDesarrollado por: Ezequiel Bonilla V.\nInstituto Tecnológico de Costa Rica")

    def recibir_configuracion(self, datos):
        #Recibe datos de configuración
        self.clk = datos["type"]
        self.segundos_totales = datos["reloj_tiempo"]
        self.dificultad = datos["dificultad"]
        self.ntop = datos["cantidad_top"] 
        self.usuario.costum_elements = datos["element_list"] #Guardar aquí la ref al user

        if  datos["elementos"] == "num":
            self.element_list = self.MAPEO_NUMEROS
            self.elementos = True
        elif datos["elementos"] == "let":
            self.element_list = self.MAPEO_LETRAS
            self.elementos = False
        else:
            self.element_list = datos["element_list"]

        self.partida.difficulty = self.dificultad

if __name__ == "__main__":
    app = MenuPrincipal()
    #app.abrir_login()
    app.mainloop()    
