import os
import tkinter as tk
from tkinter import messagebox
# Importamos la interfaz que creamos anteriormente
from ABB import ABB
import PickleParser
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
        self.costum_ele = False
        self.ntop = 0
        self.element_list = {1:"",2:"",3:"",4:"",5:"",6:"",7:"",8:"",9:"",-1:" "}

        #Usuario y partidas
        self.json = JsonParser()
        self.json.nombre_archivo = "usuarios.json"
        file = self.json.read()   

        data = file["1"]
        #print(data)

        #Recordar que el usuario se crea según lo que pase el login al iniciar sesión
        self.usuario = User(1,data["correo"],data["codigo_ingreso"],data["nombre"],data["fecha_creacion"],data["costum_elements"]) #Revisar lo de la id
        self.partida = Partida(self.usuario.nombre,-1,"2026-06-25 00:55:55")

        self.gestor = PickleParser.PickleParser()
        datos = {
            "Facil": [
                {
                    "name": "Bruno",
                    "time": "00:00:48",
                    "fecha": "2026-06-05 - 19:02:15"
                },
                {
                    "name": "Ana_Gomez",
                    "time": "00:01:15",
                    "fecha": "2026-06-05 - 09:00:00"   
                },
                {
                    "name": "Sofia_Dev",
                    "time": "00:01:05",
                    "fecha": "2026-06-05 - 21:15:45"
                },
                {
                    "name": "Valeria",
                    "time": "00:00:59",
                    "fecha": "2026-06-05 - 10:15:30"
                },
                {
                    "name": "Tomas",
                    "time": "00:02:10",
                    "fecha": "2026-06-03 - 22:11:05"
                },
                {
                    "name": "Diego_K",
                    "time": "00:03:08",
                    "fecha": "2026-06-05 - 13:40:19"                
                },
                {
                    "name": "Eze",
                    "time": "00:01:37",
                    "fecha": "2026-06-05 - 16:00:01"
                },
                {
                    "name": "Elena_99",
                    "time": "00:02:15",
                    "fecha": "2026-06-04 - 12:00:35"
                },
                {
                    "name": "Mateo",
                    "time": "00:01:42",
                    "fecha": "2026-06-05 - 08:30:22"
                },
                {
                    "name": "Lucia_M",
                    "time": "00:05:34",
                    "fecha": "2026-06-05 - 15:50:22"
                },
                {
                    "name": "Carlos",
                    "time": "00:03:20",
                    "fecha": "2026-06-05 - 14:05:11"
                }
            ],
            "Intermedio":[
            {
                "name": "Ana_Gomez",
                "time": "00:02:55",
                "fecha": "2026-06-05 - 09:45:18"
            },
            {
                "name": "Valeria",
                "time": "00:04:12",
                "fecha": "2026-06-05 - 11:22:45"
            },
            {
                "name": "Eze",
                "time": "00:04:21",
                "fecha": "2026-06-25 - 00:55:55"
            },
            {
                "name": "Mateo",
                "time": "00:04:50",
                "fecha": "2026-06-05 - 11:15:00"
            }
        ],
            "Dificil": [
            {
                "name": "Eze",
                "time": "00:01:51",
                "fecha": "2026-06-05 - 21:34:51"
            },
            {
                "name": "Sofia_Dev",
                "time": "00:04:39",
                "fecha": "2026-06-05 - 21:00:05"
            },
            {
                "name": "Bruno",
                "time": "00:05:14",
                "fecha": "2026-06-05 - 20:40:59"
            },
            {
                "name": "Ana_Gomez",
                "time": "00:06:12",
                "fecha": "2026-06-05 - 13:20:40"
            },
            {
                "name": "Diego_K",
                "time": "00:07:52",
                "fecha": "2026-06-05 - 14:55:31"
            },
            {
                "name": "Carlos",
                "time": "00:08:45",
                "fecha": "2026-06-04 - 18:30:12"
            },
            {
                "name": "Mateo",
                "time": "00:10:23",
                "fecha": "2026-06-05 - 19:55:12"
            },
            {
                "name": "Lucia_M",
                "time": "00:12:01",
                "fecha": "2026-06-05 - 17:10:03"
            }
        ],"Multi":[
            {
                "name": "Eze",
                "time": "00:09:41",
                "fecha": "2026-06-25 19:23:47"
            }
        ]
        }
        #self.gestor.saveZ(datos)
        
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
        
        
        if self.costum_ele:
            lista_ele = self.element_list
        else:
            lista_ele = self.MAPEO_NUMEROS

        Pdata = {"dif":self.dificultad, "clk": self.clk, "ele":lista_ele,
            "top":self.ntop,"time": self.segundos_totales, "partida": self.partida}
        print(Pdata["partida"].get_partida())

        historial_recuperado = self.gestor.read()
        arbolFacil = historial_recuperado["Facil"]
        arbolIntermedio = historial_recuperado["Intermedio"]
        arbolDificil = historial_recuperado["Dificil"]
        arbolMulti = historial_recuperado["Multi"]
           
        estructuras_a_guardar = {
            "Facil": arbolFacil,
            "Intermedio": arbolIntermedio,
            "Dificil": arbolDificil,
            "Multi": arbolMulti
        }     

        ventana_juego = gameWindow(self,self.elementos,Pdata)
        ventana_juego.protocol("WM_DELETE_WINDOW", self.quit)

    def abrir_configuracion(self):
        self.withdraw() 

        ventana_juego = configWindow(self,self.element_list)
        ventana_juego.protocol("WM_DELETE_WINDOW", self.quit)

    def abrir_ayuda(self):
        os.startfile('Docs\Manual de usuario Sudoku V2.0.pdf')

    def abrir_acerca_de(self):
        messagebox.showinfo("Acerca de", "Sudoku 2026\nVersión: 2.0\nTaller de Programación\nDesarrollado por: Ezequiel Bonilla V.\nInstituto Tecnológico de Costa Rica")
    
    def recibir_login(self,user):
        self.usuario = user
        self.partida.name = user.nombre
        self.element_list = user.costum_elements
        print(self.usuario.costum_elements)

    def recibir_configuracion(self, datos):
        #Recibe datos de configuración
        self.clk = datos["type"]
        self.segundos_totales = datos["reloj_tiempo"]
        self.dificultad = datos["dificultad"]
        self.ntop = datos["cantidad_top"] 
        self.usuario.costum_elements = datos["element_list"]
        #print(datos["element_list"]) #Guardar aquí la ref al user
        self.json.salvar_user(self.usuario)

        if  datos["elementos"] == "num":
            self.element_list = self.MAPEO_NUMEROS
            self.elementos = True
            self.costum_ele = False
        elif datos["elementos"] == "let":
            self.element_list = self.MAPEO_LETRAS
            self.elementos = False
            self.costum_ele = False
        else:
            self.element_list = datos["element_list"]
            self.costum_ele = True

        self.partida.difficulty = self.dificultad

if __name__ == "__main__":
    app = MenuPrincipal()
    app.abrir_login()
    app.mainloop()    
