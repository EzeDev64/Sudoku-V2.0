import os
import random
import fpdf
from JSONParser import JsonParser
import tkinter as tk
from tkinter import messagebox

class gameWindow(tk.Toplevel):
    def __init__(self, parent, nivel,clk,elementos,ntop,time = 0,data=None):
        super().__init__(parent)

        self.parent = parent
        self.title("Sudoku")
        self.geometry("600x450")
        self.resizable(False, False)
        
        #Configuraciones de la interfaz
        self.segundos_totales = data["time"] #time
        self.dificultad = data["dif"] #nivel      
        self.timerTime = data["time"] #time 
        self.clk = data["clk"] #clk    
        self.elementos = elementos    
        print(elementos)
        self.ntop = data["top"] #ntop
        self.partida = data["partida"]        

        self.js = JsonParser()               
        self.crono = False
        self.tablero = None
        self.crono_id = None
        self.MAPEO_LETRAS = {1: "A", 2: "B", 3: "C",4: "D", 5: "E", 6: "F",7: "G", 8: "H", 9: "I", -1: " "}

        self.createIGU()

    def createIGU(self):
        # La barra para el título:
        titleFrame = tk.Frame(self, height=50,bg="white")
        titleFrame.pack(side="top", fill="x")
        #-Componentes-
        lbl_title = tk.Label(titleFrame,text="Sudoku")
        lbl_title.pack()
        titleFrame.pack_propagate(False)
        
        #region  Frame que lo de abajo cronómetro y botones de configuración
        fila_base = tk.Frame(self, height=50)
        fila_base.pack(side="bottom", fill="x")
        fila_base.pack_propagate(False)

        # Frame del cronómetro y nivel
        cronoFrame = tk.Frame(fila_base, bg="white")
        #-Componentes-
        self.lbl_reloj = tk.Label(cronoFrame, text="00:00:00", bg="black", fg="#00ff00")  # Color verde tipo cronómetro digital
        self.lbl_nivel = tk.Label(cronoFrame, text="Nivel: "+self.dificultad)

        self.lbl_reloj.pack(side="left", padx=5)
        self.lbl_nivel.pack(side="left")
        cronoFrame.pack(side="left", fill="both", expand=True)

        # Frame de los botones de configuración
        configFrame = tk.Frame(fila_base, bg="white")
        configFrame.pack(side="right", fill="both", expand=True)
        #-Componentes-
        self.btn_guardar = tk.Button(configFrame, text="Guardar juego",state="disabled",command=self.guardar_juego)
        self.btn_cargar = tk.Button(configFrame, text="Cargar juego",state="disabled",command=self.cargar_juego)
        self.btn_salir = tk.Button(configFrame, text="Regresar",command=self.salir)
        self.btn_salir.pack(side="left", expand=True, fill="both", padx=2, pady=2)
        self.btn_guardar.pack(side="left", expand=True, fill="both", padx=2, pady=2)
        self.btn_cargar.pack(side="left", expand=True, fill="both", padx=2, pady=2)

        # Sección de botones
        btnFrame = tk.Frame(self, height=50)
        #-Componentes-
        self.btn_iniciar = tk.Button(btnFrame, text="Iniciar juego",command=self.iniciar_juego)
        self.btn_deshacer = tk.Button(btnFrame, text="Deshacer jugada",state="disabled",command=self.deshacer_jugada)
        self.btn_rehacer = tk.Button(btnFrame, text="Rehacer jugada",state="disabled",command=self.rehacer_jugada)
        self.btn_terminar = tk.Button(btnFrame, text="Terminar juego",state="disabled",command=self.terminar_juego)
        self.btn_borrar = tk.Button(btnFrame, text="Borrar juego",state="disabled", command=self.borrar_juego)
        self.btn_top = tk.Button(btnFrame, text="Top X",command=self.generar_top)

        self.btn_iniciar.pack(side="left", expand=True, fill="both", padx=2, pady=2)
        self.btn_deshacer.pack(side="left", expand=True, fill="both", padx=2, pady=2)
        self.btn_rehacer.pack(side="left", expand=True, fill="both", padx=2, pady=2)
        self.btn_terminar.pack(side="left", expand=True, fill="both", padx=2, pady=2)
        self.btn_borrar.pack(side="left", expand=True, fill="both", padx=2, pady=2)
        self.btn_top.pack(side="left", expand=True, fill="both", padx=2, pady=2)

        btnFrame.pack(side="bottom", fill="x")
        btnFrame.pack_propagate(False)
        #endregion

        #region Frame que contiene el del juego y misc
        frame_central = tk.Frame(self)
        frame_central.pack(side="top", fill="both", expand=True)

        # Configuración de las filas
        frame_central.columnconfigure(0, weight=1)
        frame_central.columnconfigure(1, weight=1)
        frame_central.rowconfigure(0, weight=1)

        # Creación de los páneles de juego y misc respectivamente
        frame_rojo = tk.Frame(frame_central, bg="#e31b1b")
        frame_rojo.grid(row=0, column=0, sticky="nsew")
        frame_azul = tk.Frame(frame_central, bg="white")
        frame_azul.grid(row=0, column=1, sticky="nsew")
        frame_azul.pack_propagate(False)

        #Creación de los paneles misc
        name = tk.StringVar(self,value=self.partida.name)
        self.lbl_jugador = tk.Label(frame_azul, text="Jugador:", font=("Arial", 12, "bold"),bg=frame_azul.cget("bg"),fg="black",anchor="w")  # Alinea el texto a la izquierda)
        self.txt_nombre = tk.Entry(frame_azul,font=("Arial", 12),state="disabled",textvariable=name)
        self.numbersFrame = tk.Frame(frame_azul, bg="black", height=200,width=200)
        self.botones_numericos = {}

        #region Creación botones numéricos:
        # Configuramos las 3 filas y 3 columnas del panel negro para que se estiren por igual
        for i in range(3):
            self.numbersFrame.rowconfigure(i, weight=1)
            self.numbersFrame.columnconfigure(i, weight=1)

        # Creamos y posicionamos los botones del 1 al 9 en un grid de 3x3
        contador = 1
        for fila in range(3):
            for col in range(3):
                text = str(contador)
                if not (self.elementos):
                    text = self.MAPEO_LETRAS.get(int(text), "")

                btn_num = tk.Button(self.numbersFrame, text=text, command=lambda num= contador:self.colocar_numero(str(num)),state="disabled")
                btn_num.grid(row=fila, column=col, padx=2, pady=2, sticky="nsew")
                self.botones_numericos[contador]= btn_num
                contador += 1

        #endregion

        self.lbl_jugador.pack(side="top")
        self.txt_nombre.pack(side="top")
        self.numbersFrame.pack(side="top")
        self.numbersFrame.pack_propagate(False)

        #region Creación del tablero
        frame_tablero = tk.Frame(frame_rojo, bg="black", bd=2)
        frame_tablero.place(relx=0.5, rely=0.5, anchor="center") 

        self.casillas_interfaz = [[None for _ in range(9)] for _ in range(9)]
        self.casilla = None

        for fila_sub in range(3):
            for col_sub in range(3):
                subcuadricula = tk.Frame(frame_tablero, bg="black", highlightbackground="black", highlightthickness=1)
                subcuadricula.grid(row=fila_sub, column=col_sub, padx=1, pady=1)
                
                # Crear las casillas internas de 40x40 píxeles reales
                for f in range(3):
                    for c in range(3):
                        fila_real = fila_sub * 3 + f
                        col_real = col_sub * 3 + c
                            
                        contenedor_casilla = tk.Frame(subcuadricula, width=30, height=30)
                        contenedor_casilla.grid(row=f, column=c, padx=1, pady=1)
                        contenedor_casilla.pack_propagate(False) 
                        
                        casilla = tk.Label(contenedor_casilla, font=("Arial", 16, "bold"),bg="white",relief="groove",bd=1,state="disabled")
                        casilla.pack(fill="both", expand=True)
                        
                        self.casillas_interfaz[fila_real][col_real] = casilla
        #endregion
        #endregion

    def iniciar_juego(self):
        #Validaciones nombre jugador
        player_name = self.txt_nombre.get()
        if len(player_name) < 1 or len(player_name)>30:
            messagebox.showinfo("Sudoku","El nombre debe tener entre 1 a 30 caracteres")
            return
        if player_name.replace(" ","") == "":
             messagebox.showinfo("Sudoku","Se debe ingresar un nombre para continuar")
             return
        
        #Activamos el resto de componentes
        self.btn_guardar.config(state="normal")
        self.btn_cargar.config(state="normal")
        self.btn_deshacer.config(state="normal")
        self.btn_rehacer.config(state="normal")
        self.btn_terminar.config(state="normal")
        self.btn_borrar.config(state="normal")      
        self.btn_iniciar.config(state="disabled")
        
        for boton in self.botones_numericos.values():
            boton.config(state="normal")

        #Generamos el tablero según @crear_juego()
        if (self.tablero == None):
            self.tablero = self.crear_juego()

        text=" "
        for fila in range(9):
            for col in range(9):
                text = str(self.tablero[fila][col])
                
                if not (self.elementos):
                    text = self.MAPEO_LETRAS.get(int(text), "")
                
                if text == "-1":
                    text = " "
                    
                self.casillas_interfaz[fila][col].fila_colum= [fila,col]
                self.casillas_interfaz[fila][col].bind("<Button-1>", lambda event, r=fila, c=col: self.fijar_casilla(r, c))

                self.casillas_interfaz[fila][col].config(text=text, bg="white",state="normal")

        #Sección del tiempo:
        if (self.clk =="crono"):
            self.iniciar_crono()
        elif (self.clk == "timer"):
            self.iniciar_timer()

        #Actualizamos la interfaz
        self.update_idletasks()
    
    def fijar_casilla(self,r, c):
        #En caso que ya exista otra casilla seleccionada
        if self.casilla != None:
            self.casilla.config(bg="white")

        #Apuntamos a la nueva
        self.casilla = self.casillas_interfaz[r][c]
        self.casilla.config(bg="gray")

    def colocar_numero(self,numero):
        #Validamos el dato
        if self.casilla ==  None:
            messagebox.showinfo("Sudoku","FALTA SELECCIONAR UN ELEMENTO.")
            return

        #Capturar el texto y cambiar el color de la casilla.
        texto= self.casilla.cget("text")
        self.casilla.config(bg="red")

        #region Búsqueda de el mismo valor en filas y columnas
        for f in self.tablero[self.casilla.fila_colum[0]]:
            if f == int(numero):
                messagebox.showinfo("Sudoku","JUGADA NO ES VÁLIDA PORQUE EL ELEMENTO YA ESTÁ EN LA FILA ")
                self.casilla.config(bg="white")
                return
        for c in self.tablero:
            if c[self.casilla.fila_colum[1]] == int(numero):
                messagebox.showinfo("Sudoku"," JUGADA NO ES VÁLIDA PORQUE EL ELEMENTO YA ESTÁ EN LA COLUMNA")
                self.casilla.config(bg="white")
                return
        #endregion

        #region Búsqueda de el mismo valor en el cuadro 3*3
        fila_cuadro = (self.casilla.fila_colum[0]// 3) * 3
        columna_cuadro = (self.casilla.fila_colum[1]// 3) * 3
        for f in range(fila_cuadro, fila_cuadro + 3):
            for c in range(columna_cuadro, columna_cuadro + 3):
                if self.tablero[f][c] == int(numero):
                    # ¡AQUÍ SE DISPARA EL ERROR!
                    messagebox.showinfo("Sudoku","JUGADA NO ES VÁLIDA PORQUE EL ELEMENTO YA ESTÁ EN LA CUADRÍCULA")
                    self.casilla.config(bg="white")
                    return
        #endregion

        #En caso que esa casilla ya esté ocupada
        if texto != " ":
            messagebox.showinfo("Sudoku","JUGADA NO ES VÁLIDA PORQUE ESTE ES UN ELEMENTO FIJO")
            self.casilla.config(bg="white")
            return

        #Si todo está en orden, cambia el color de la casilla, y coloca el nuevo número
        text = str(numero)
        if not self.elementos:
            text = self.MAPEO_LETRAS.get(int(text), "")

        self.casilla.config(bg="white")
        self.casilla.config(text=text)
        self.tablero[self.casilla.fila_colum[0]][self.casilla.fila_colum[1]]= int(numero)
        self.pilaUltimasJ.append([numero,(self.casilla.fila_colum[0],self.casilla.fila_colum[1])])
        self.pilaEliminadasJ = []
        
        #Verificamos si el juego está completo
        if self.verificar_juego():
            messagebox.showinfo("Sudoku","¡EXCELENTE! JUEGO COMPLETADO")
            self.pausar_crono()
            self.js.nombre_archivo = "sudoku2026_bitácora_jugadas.json"
            message = self.js.registrar_partida(self.txt_nombre.get(),self.dificultad,self.lbl_reloj.cget("text"))
            if message:
                messagebox.showinfo("Sudoku","Partida guardada con éxito")

    def verificar_juego(self):
        #Retorna True si el juego está completo, False de lo contrario
        for f in self.tablero:
            for c in f:
                if c == -1:
                    return False
        
        return True
        
    def deshacer_jugada(self):
        #Validación de la pila
        if self.pilaUltimasJ == []:
            messagebox.showinfo("Sudoku","NO HAY JUGADAS PARA DESHACER")
            return

        #Obtenemos parámetros y modificamos listas
        position = len(self.pilaUltimasJ)-1
        ultimaJugada = self.pilaUltimasJ[position]
        self.pilaEliminadasJ.append(ultimaJugada)
        self.pilaUltimasJ.pop(position)

        #Aplicamos el cambio
        self.tablero[ultimaJugada[1][0]][ultimaJugada[1][1]]= int(-1)
        self.casillas_interfaz[ultimaJugada[1][0]][ultimaJugada[1][1]].config(text=" ", bg="white",state="normal")

    def rehacer_jugada(self):
        #Validación de la pila
        if self.pilaEliminadasJ == []:
            messagebox.showinfo("Sudoku","NO HAY JUGADAS PARA REHACER")
            return

        #Obtenemos parámetros y modificamos listas
        position = len(self.pilaEliminadasJ)-1
        ultimaJugada = self.pilaEliminadasJ[position]
        self.pilaEliminadasJ.pop(position)

        self.tablero[ultimaJugada[1][0]][ultimaJugada[1][1]]= int(ultimaJugada[0])
        self.pilaUltimasJ.append([int(ultimaJugada[0]),(ultimaJugada[1][0],ultimaJugada[1][1])])

        #Caso en el que la opción de elementos sean letras
        text = str(ultimaJugada[0])
        if not (self.elementos):
            text = self.MAPEO_LETRAS.get(int(text), "")

        #Aplicamos el cambio
        self.casillas_interfaz[ultimaJugada[1][0]][ultimaJugada[1][1]].config(text=text, bg="white",state="normal")
        return

    def crear_juego(self):
        #Obtenemos las partidas de pruebas
        self.js.nombre_archivo = "sudoku2026partidas.json"
        partidas = self.js.read()

        if str.lower(self.dificultad) not in partidas:
            messagebox.showinfo("Sudoku","NO EXISTE NINGUN JUEGO CON ESTA DIFICULTAD")
            return

        #Creamos las pilas de jugadas
        self.pilaUltimasJ=[]
        self.pilaEliminadasJ=[]

        #Inicializamos el tablero con uno escogido del json al azar
        tablero = [[],[],[],[],[],[],[],[],[]]

        numero_partida = str(random.randint(1, 4))
        partida_seleccionada = partidas[str.lower(self.dificultad)][numero_partida]
        tablero = [[-1 for _ in range(9)] for _ in range(9)]

        for coordenada, valor in partida_seleccionada.items():
            #Map nos ayuda a iterar sobre la cordenada (f,c)
            f, c = map(int, coordenada.split(","))
            tablero[f][c] = valor

        return tablero

    def borrar_juego(self):
        respuesta = messagebox.askyesno("Confirmar", "¿ESTÁ SEGURO DE BORRAR EL JUEGO (SI o NO)?")
    
        if respuesta:
            print("El usuario seleccionó SÍ. Limpiando el tablero...")
            for i in range(0,len(self.pilaUltimasJ)):
                self.deshacer_jugada()
            self.pilaEliminadasJ.clear()
            self.pilaUltimasJ.clear()

    def terminar_juego(self):
        respuesta = messagebox.askyesno("Confirmar", "¿ESTÁ SEGURO DE TERMINAR EL JUEGO (SI o NO)?")
    
        if respuesta:
            #Desactivamos los botones correspondientes
            self.btn_guardar.config(state="disabled")
            self.btn_cargar.config(state="disabled")
            self.btn_deshacer.config(state="disabled")
            self.btn_rehacer.config(state="disabled")
            self.btn_terminar.config(state="disabled")
            self.btn_borrar.config(state="disabled")
            self.btn_iniciar.config(state="normal")
            
            #Sección del tiempo:
            if (self.clk =="crono"):
                self.reiniciar_crono()
            elif (self.clk == "timer"):
                self.reiniciar_timer()
            self.limpiar_tablero()

    def limpiar_tablero(self):
        #Limpiamos el tablero
        for f in self.casillas_interfaz:
            for c in f:
                c.config(text=" ", bg="white",state="normal")

        self.tablero = None

    def iniciar_crono(self):
        #Iniciamos el cronometro (Cuenta ascendente)
        if not self.crono and self.clk == "crono":
            if self.crono_id is not None:
                self.after_cancel(self.crono_id)
            
            self.crono = True
            self.actualizar_crono()

    def actualizar_crono(self):
        #En caso que el crono no esté habilitado
        if self.clk != "crono" or not self.crono:
            self.crono = False
            return
        
        #Dividimos el tiempo en hhmmss
        horas = self.segundos_totales // 3600
        minutos = (self.segundos_totales % 3600) // 60
        segundos = self.segundos_totales % 60
        #Le damos formato
        tiempo_formateado = f"{horas:02d}:{minutos:02d}:{segundos:02d}"

        #Agregamos al campo y sumamos los segundos
        self.lbl_reloj.config(text=tiempo_formateado)
        self.segundos_totales += 1
        self.crono_id = self.after(1000, self.actualizar_crono)
    
    def pausar_crono(self):
        #Detiene el cronómetro sin borrar el tiempo actual.
        self.crono = False

    def reiniciar_crono(self):
        #Pone el cronómetro a cero y actualiza la pantalla inmediatamente.
        self.crono = False
        if self.crono_id is not None:
            self.after_cancel(self.crono_id)
            self.crono_id = None

        self.segundos_totales = 0
        if hasattr(self, 'lbl_reloj'):
            self.lbl_reloj.config(text="00:00:00")
    
    def iniciar_timer(self):
        #Iniciamos el cronometro (Cuenta descendente)
        if not self.crono and self.clk == "timer":
            if self.crono_id is not None:
                self.after_cancel(self.crono_id)

            #En caso que el tiempo esté en 0 desde antes
            if self.segundos_totales <= 0:
                messagebox.showinfo("Sudoku", "El tiempo ya ha terminado o no se ha configurado.")
                return
                
            self.crono = True
            self.actualizar_timer()

    def actualizar_timer(self):
            if self.clk != "timer" or not self.crono:
                self.crono = False
                return
        
        #if self.crono:
            # 1. Si el contador llega a cero, el tiempo se acabó
            if self.segundos_totales <= 0:
                self.crono = False
                self.lbl_reloj.config(text="00:00:00")

                respuesta = messagebox.askyesno("Confirmar", "¿DESEA CONTINUAR EL MISMO JUEGO (SI O NO)?")
                if respuesta: # Es lo mismo que decir: if respuesta == True:
                    self.reiniciar_timer()
                    self.clk = "crono"
                    self.iniciar_crono()
                else:
                    self.btn_guardar.config(state="disabled")
                    self.btn_cargar.config(state="disabled")
                    self.btn_deshacer.config(state="disabled")
                    self.btn_rehacer.config(state="disabled")
                    self.btn_terminar.config(state="disabled")
                    self.btn_borrar.config(state="disabled")
                    self.btn_iniciar.config(state="normal")
                    
                    self.reiniciar_timer()
                    self.limpiar_tablero()

                return

            # 2. Calculamos horas, minutos y segundos usando división entera y residuo
            horas = self.segundos_totales // 3600
            minutos = (self.segundos_totales % 3600) // 60
            segundos = self.segundos_totales % 60

            # 3. Le damos el formato HH:MM:SS
            tiempo_formateado = f"{horas:02d}:{minutos:02d}:{segundos:02d}"

            # 4. Actualizamos el texto del Label en la interfaz gráfica
            self.lbl_reloj.config(text=tiempo_formateado)

            # 5. Restamos un segundo para la cuenta regresiva
            self.segundos_totales -= 1

            # 6. Le decimos a Tkinter que vuelva a llamar a esta función en 1 segundo
            self.crono_id = self.after(1000, self.actualizar_timer)

    def pausar_timer(self):
        # Detiene la cuenta regresiva del temporizador sin borrar los segundos actuales.
        self.crono = False

    def reiniciar_timer(self):
        #Pone el cronómetro a cero y actualiza la pantalla inmediatamente.
        self.crono = False

        if self.crono_id is not None:
            self.after_cancel(self.crono_id)
            self.crono_id = None
        
        self.segundos_totales =  self.timerTime

        #Hacemos el cálculo de hhmmss
        horas = self.segundos_totales // 3600
        minutos = (self.segundos_totales % 3600) // 60
        segundos = self.segundos_totales % 60
        
        #Actualización de la interfaz
        self.lbl_reloj.config(text=f"{horas:02d}:{minutos:02d}:{segundos:02d}")
    
    def generar_top(self):        
        #Generamos el top según las configuraciones del usuario
        self.crear_pdf()
        messagebox.showinfo("Sudoku","Se generó el pdf Top jugadores, abriendo en el navegador...")

    def guardar_juego(self):
        #Guardamos la partida actual
        self.js.nombre_archivo = "sudoku2026juegoactual.json"
        message = self.js.guardar_partida(self.tablero,self.dificultad,False,True,self.txt_nombre.get(),self.lbl_reloj.cget("text"),self.pilaUltimasJ,self.pilaEliminadasJ)
        if message:
            messagebox.showinfo("Sudoku","Partida guardada con éxito")

    def cargar_juego(self):
        #Cargamos la partida actual
        self.js.nombre_archivo = "sudoku2026juegoactual.json"
        a = self.js.cargar_partida(self.txt_nombre.get(),self.dificultad)
        if (a == None):
            messagebox.showinfo("Sudoku","NO TIENE UN JUEGO GUARDADO CON ESTA DIFICULTAD")
            return
        self.tablero = a["tablero"]
        
        #region Parte de configuración 
        #Tiempo
        self.reiniciar_crono()
        self.reiniciar_timer()
        #Datos
        self.pilaUltimasJ = a["ultimas_jugadas"]
        self.pilaEliminadasJ = a["jugadas_eliminadas"]
        self.clk = a["type"]
        tiempo_texto = a["tiempo"]
        partes = tiempo_texto.split(":")
        
        #Converción del tiempo formato hhmmss
        horas = int(partes[0])
        minutos = int(partes[1])
        segundos = int(partes[2])
        
        #Calculo tiempos totales
        self.segundos_totales = (horas * 3600) + (minutos * 60) + segundos
        self.timerTime = self.segundos_totales
        self.lbl_reloj.configure(text=a["tiempo"])
        #endregion

        messagebox.showinfo("Sudoku","Juego cargado")
        self.iniciar_juego()
    
    def crear_pdf(self):
        #Creamos el pdf del top
        #Leemos el json
        self.js.nombre_archivo = "sudoku2026_bitácora_jugadas.json"
        datos_json = self.js.read()
        
        #Inicializamos la clase para conversión
        pdf = fpdf.FPDF(orientation='P', unit='mm', format='letter')
        pdf.add_page()
        
        #Título
        pdf.set_font("Arial", style="B", size=16)
        titulo = "BITÁCORA DE JUGADAS - SUDOKU 2026"
        pdf.cell(w=0, h=12, txt=titulo.encode('latin-1', 'ignore').decode('latin-1'), ln=1, align='C')
        
        #Subtítulo
        pdf.set_font("Arial", style="I", size=10)
        txt_top = f"Mostrando: Todos los registros" if self.ntop == 0 else f"Mostrando: Top {self.ntop} mejores tiempos"
        pdf.cell(w=0, h=6, txt=txt_top.encode('latin-1', 'ignore').decode('latin-1'), ln=1, align='C')
        pdf.ln(10)

        
        niveles = ["Facil", "Intermedio", "Dificil"]
        #Ancho columnas
        ancho_col1 = 60
        ancho_col2 = 60
        ancho_col3 = 60

        for nivel in niveles:
            #Encabezado del nivel
            pdf.set_font("Arial", style="B", size=12)
            nivel_encabezado = f"NIVEL: {nivel.upper()}"
            pdf.cell(w=0, h=8, txt=nivel_encabezado.encode('latin-1', 'ignore').decode('latin-1'), ln=1, align='L')
            
            #Títulos de las 3 columnas
            pdf.set_font("Arial", style="B", size=10)
            pdf.cell(w=ancho_col1, h=6, txt="JUGADOR".encode('latin-1').decode('latin-1'), ln=0, align='L')
            pdf.cell(w=ancho_col2, h=6, txt="TIEMPO JUGADO".encode('latin-1').decode('latin-1'), ln=0, align='L')
            pdf.cell(w=ancho_col3, h=6, txt="EL".encode('latin-1').decode('latin-1'), ln=1, align='L')
            
            #Línea divisoria
            pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + 180, pdf.get_y())
            pdf.ln(2)

            #Recolección de datos
            jugadas_nivel = []
            
            for jugador, partidas in datos_json.items():
                for partida in partidas:
                    nivel_partida = partida.get("dificultad") or partida.get("nivel") or ""
                    
                    if str(nivel_partida).lower() == nivel.lower():
                        tiempo = partida.get("tiempo") or partida.get("reloj_tiempo") or "00:00:00"
                        fecha = partida.get("fecha_hora") or partida.get("fecha") or "--/--/----"
                        
                        jugadas_nivel.append({"jugador": jugador,"tiempo": tiempo,"fecha": fecha})

            #Ordenamos las jugadas de mejor a peor
            jugadas_nivel.sort(key=lambda x: x["tiempo"])

            #Tomamos elementos hasta la cantidad definida por el usuario
            if self.ntop > 0:
                jugadas_nivel = jugadas_nivel[:self.ntop]

            #Escribimos los datos
            pdf.set_font("Arial", style="", size=10)
            if len(jugadas_nivel) > 0:
                for j in jugadas_nivel:
                    pdf.cell(w=ancho_col1, h=6, txt=str(j["jugador"]).encode('latin-1', 'ignore').decode('latin-1'), ln=0, align='L')
                    pdf.cell(w=ancho_col2, h=6, txt=str(j["tiempo"]).encode('latin-1', 'ignore').decode('latin-1'), ln=0, align='L')
                    pdf.cell(w=ancho_col3, h=6, txt=str(j["fecha"]).encode('latin-1', 'ignore').decode('latin-1'), ln=1, align='L')
            else:
                pdf.set_font("Arial", style="I", size=10)
                pdf.cell(w=0, h=6, txt="No hay jugadas registradas en este nivel.".encode('latin-1', 'ignore').decode('latin-1'), ln=1, align='L')

            # Espacio entre bloques
            pdf.ln(10)

        # Guardar el PDF final
        try:
            pdf.output("reporte_bitacora_sudoku.pdf")
            os.startfile('reporte_bitacora_sudoku.pdf')
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el PDF.\nError: {e}")

    def salir(self):
        #Regresar a la pantalla principal
        self.parent.deiconify()
        self.destroy()

if __name__ == "__main__":
    app = gameWindow("Facil","crono",False,0,0)
    app.mainloop()