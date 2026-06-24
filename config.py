import tkinter as tk
from tkinter import messagebox

class configWindow(tk.Toplevel):
    def __init__(self,parent):
        super().__init__(parent)
        self.parent = parent
        
        self.title("Sudoku")
        self.geometry("600x450")
        self.resizable(False, False)
        
        self.var_reloj = tk.StringVar(self) 

        self.crear_interfaz()

    def crear_interfaz(self):
        #Configuramos las columnas y filas
        self.rowconfigure(0, weight=1) 
        self.rowconfigure(1, weight=1)        
        self.rowconfigure(2, weight=4) 
        self.rowconfigure(3, weight=1) 
        self.rowconfigure(4, weight=1) 
        self.rowconfigure(5, weight=1)
        self.columnconfigure(0, weight=1)

        #Configuración del título
        title_frame  = tk.Frame(self)
        lbl_titulo = tk.Label(title_frame, text="CONFIGURACIÓN DEL JUEGO", fg="black", font=("Arial", 12, "bold"))
        lbl_titulo.pack()
        title_frame.grid(row=0, column=0, sticky="nsew")

        #Configuración del nivel de dificultad
        level_frame = tk.Frame(self)
        lbl_level = tk.Label(level_frame, text="Nivel", fg="black", font=("Arial", 12, "bold"))
        self.var_dificultad = tk.StringVar(value="Facil")
        rb_facil = tk.Radiobutton(level_frame,text="Facil", variable=self.var_dificultad,value="Facil")
        rb_intermedio = tk.Radiobutton(level_frame,text="Intermedio", variable=self.var_dificultad,value="Intermedio")
        rb_dificil = tk.Radiobutton(level_frame,text="Dificil", variable=self.var_dificultad,value="Dificil")

        lbl_level.pack(side=tk.LEFT, padx=10)
        rb_facil.pack(side=tk.LEFT, padx=10)
        rb_intermedio.pack(side=tk.LEFT, padx=10)
        rb_dificil.pack(side=tk.LEFT, padx=10)
        rb_facil.select()
        rb_intermedio.deselect()
        rb_dificil.deselect()
        level_frame.grid(row=1, column=0, sticky="nsew")

        #Configuración del relog y cronómetro
        crono_frame = tk.Frame(self)

        #region Elementos del frame
        label_clk = tk.Label(crono_frame, text="Reloj:",fg="black", font=("Arial", 12, "bold"))
        label_clk.pack(side=tk.LEFT, padx=10)

        #Frame para guardar los radio buttons
        frm_radios = tk.Frame(crono_frame, bd=1, relief="solid")
        rb_crono = tk.Radiobutton(frm_radios, text="Cronómetro", variable=self.var_reloj, value="crono",command=self.activate_timer)
        rb_timer = tk.Radiobutton(frm_radios, text="Timer", variable=self.var_reloj, value="timer",command=lambda:self.activate_timer(True))
        rb_none = tk.Radiobutton(frm_radios, text="Ninguno", variable=self.var_reloj, value="none",command=self.activate_timer)

        frm_radios.pack(side=tk.LEFT, padx=15, pady=5)
        rb_crono.pack(anchor=tk.W, padx=5, pady=2)
        rb_timer.pack(anchor=tk.W, padx=5, pady=2)
        rb_none.pack(anchor=tk.W, padx=5, pady=2)
        rb_crono.select()
        rb_timer.deselect()
        rb_none.deselect()

        #Validación de números para entry
        configuracion = (self.register(self.validar_numeros), "%P")

        #Frame para guardar los entry/text_lbl
        frm_entradas_tiempo = tk.Frame(crono_frame, bd=1, relief="solid")
        col_h = tk.Frame(frm_entradas_tiempo)
        lbl_h = tk.Label(col_h, text="lbl_h")
        self.entry_h = tk.Entry(col_h, width=4, justify="center", highlightthickness=1,state="disabled",validate="key", validatecommand=configuracion)
        col_m = tk.Frame(frm_entradas_tiempo)
        lbl_m = tk.Label(col_m, text="lbl_m")
        self.entry_m = tk.Entry(col_m, width=4, justify="center",highlightthickness=1,state="disabled",validate="key", validatecommand=configuracion)
        col_s = tk.Frame(frm_entradas_tiempo)
        lbl_s = tk.Label(col_s, text="lbl_s")
        self.entry_s = tk.Entry(col_s, width=4, justify="center", highlightthickness=1,state="disabled",validate="key", validatecommand=configuracion)
        
        col_h.pack(side=tk.LEFT, padx=10, pady=10)
        lbl_h.pack()
        self.entry_h.pack(pady=2)
        col_m.pack(side=tk.LEFT, padx=10, pady=10)
        lbl_m.pack()
        self.entry_m.pack(pady=2)
        col_s.pack(side=tk.LEFT, padx=10, pady=10)
        lbl_s.pack()
        self.entry_s.pack(pady=2)
        frm_entradas_tiempo.pack(side=tk.LEFT, padx=15, pady=5)
        #endregion

        crono_frame.grid(row=2, column=0, sticky="nsew")

        #Configuración del top y elementos.
        top_frame = tk.Frame(self)
        lbl_cantP = tk.Label(top_frame,text="Cantidad de jugadas desplegadas en el TOP X:",fg="black", font=("Arial", 12, "bold"))
        self.valor_spinner = tk.IntVar(value=0)
        self.spinner = tk.Spinbox(top_frame, from_=0, to=10, textvariable=self.valor_spinner,width=5)
        
        lbl_cantP.pack(side=tk.LEFT, padx=10, pady=10)
        self.spinner.pack(side=tk.LEFT, padx=10, pady=10)
        top_frame.grid(row=3, column=0, sticky="nsew")

        element_frame = tk.Frame(self)
        lbl_element= tk.Label(element_frame, text="Panel de elementos:", fg="black", font=("Arial", 12, "bold"))
        lbl_element.pack(side=tk.LEFT, padx=10)
        self.var_elementos = tk.StringVar(value="num")
        rb_num = tk.Radiobutton(element_frame,text="Números", variable=self.var_elementos,value="num")
        rb_num.pack(side=tk.LEFT, padx=10)
        rb_let = tk.Radiobutton(element_frame,text="Letras", variable=self.var_elementos,value="let")
        rb_let.pack(side=tk.LEFT, padx=10)
        rb_num.select()
        rb_let.deselect()
        element_frame.grid(row=4, column=0, sticky="nsew")

        btn_frame = tk.Frame(self)
        self.btn_salvar = tk.Button(btn_frame, text="Salvar configuración",command=self.aceptar_cambios)
        self.btn_salir = tk.Button(btn_frame, text="Salir sin guardar",command=self.regresar_a_principal)

        self.btn_salvar.pack(side="right", expand=False, fill="none", padx=2, pady=2)
        self.btn_salir.pack(side="right", expand=False, fill="none", padx=2, pady=2)
        btn_frame.grid(row=5, column=0, sticky="nsew")
        self.update_idletasks()

    def validar_numeros(self, text):
        #Por si no hay nada en el texto
        if text == "":
            return True

        #Rechaza el texto si no son números
        if not text.isdigit():
            return False

        #Limita a dos caracteres
        if len(text) > 2:
            return False

        return True
    
    def aceptar_cambios(self):
        #Obtenemos los parámetros
        type_sel =self.var_reloj.get()
        dificultad_sel = self.var_dificultad.get()
        elementos_sel = self.var_elementos.get()
        tiempo_en_segundos =  0

        #Configuración del tiempo
        if (type_sel == "timer"):
            time_seg = self.entry_s.get()
            time_min = self.entry_m.get()
            time_hor = self.entry_h.get()

            if (time_seg=="" or time_min=="" or time_hor==""):
                messagebox.showinfo("Sudoku","INGRESE VALORES PARA EL TIMER")
                return

            time_seg = int(time_seg)
            if(time_seg<0 or time_seg>59):
                messagebox.showinfo("Sudoku","SEGUNDOS DEBEN SER MAYORES A 0 Y MENORES A 59")
                return
            
            time_min = int(time_min)
            if(time_min<0 or time_min>59):
                messagebox.showinfo("Sudoku","MINUTOS DEBEN SER MAYORES A 0 Y MENORES A 59")
                return
            
            time_hor = int(time_hor)
            if(time_hor<0 or time_hor>4):
                messagebox.showinfo("Sudoku","HORAS DEBEN SER MAYORES A 0 Y MENORES A 4")
                return
            
            tiempo_en_segundos = (int(time_hor) * 3600) + (int(time_min) * 60) + int(time_seg)

        #Diccionario con los datos
        datos_config = {
            "type": type_sel,
            "dificultad": dificultad_sel,
            "elementos": elementos_sel,
            "reloj_tiempo": tiempo_en_segundos,
            "cantidad_top": int(self.valor_spinner.get())
        }
        
        self.parent.recibir_configuracion(datos_config)
        self.regresar_a_principal()

    def regresar_a_principal(self):
        #Vuelve a la pantalla principal
        self.parent.deiconify()
        self.destroy()
    
    def activate_timer(self,active=False):
        #Desactivar/activar el apartado del timer según esté seleccionado o no
        if active:
            self.entry_h.config(state="normal")
            self.entry_m.config(state="normal")
            self.entry_s.config(state="normal")
        else:
            self.entry_h.config(state="disabled")
            self.entry_m.config(state="disabled")
            self.entry_s.config(state="disabled")

if __name__ == "__main__":
    app = configWindow()
    app.mainloop()