import os
import tkinter as tk
from tkinter import messagebox
# Importamos la interfaz que creamos anteriormente
from config import configWindow
from game import gameWindow
#from nuevos_cambios.login import loginWindow

class MenuPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sudoku")
        self.geometry("600x450")
        self.resizable(False, False)

        #Datos de configuración
        self.clk = "crono"
        self.segundos_totales = 0
        self.dificultad = "Facil"
        self.elementos = True
        self.ntop = 0

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
        
        ventana_juego = gameWindow(self,self.dificultad,self.clk,self.elementos,self.ntop,self.segundos_totales)
        ventana_juego.protocol("WM_DELETE_WINDOW", self.quit)

    def abrir_configuracion(self):
        self.withdraw() 

        ventana_juego = configWindow(self)
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

        if  datos["elementos"] == "num":
            self.elementos = True
        else:
            self.elementos = False

if __name__ == "__main__":
    app = MenuPrincipal()
    #app.abrir_login()
    app.mainloop()    
