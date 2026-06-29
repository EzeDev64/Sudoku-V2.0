import copy
import json
import os
from datetime import datetime

class JsonParser:
    def __init__(self, nombre_archivo="sudoku2026_bitácora_jugadas.json"):
        self.nombre_archivo = nombre_archivo

        #Verificamos que exista el doc, en caso contrario creamos uno nuevo.
        if not os.path.exists(self.nombre_archivo):
            estructura_inicial = {}
            self.save(estructura_inicial)

    def read(self):
        #Leemos el archivo
        try:
            with open(self.nombre_archivo, "r", encoding="utf-8") as archivo:
                return json.load(archivo)
        except (json.JSONDecodeError, FileNotFoundError):
            #En caso que esté corrupto
            return {}

    def save(self, datos):
        #Se copia el doc para evitar errores
        datos_copia = copy.deepcopy(datos)

        #Se salvan los datos y se da formato.
        for jugador, partidas in datos_copia.items():
            for partida in partidas:
                if "tablero" in partida:
                    filas_compactas = [json.dumps(fila) for fila in partida["tablero"]]
                    partida["tablero"] = filas_compactas

                if "ultimas_jugadas" in partida:
                    partida["ultimas_jugadas"] = [json.dumps(jugada) for jugada in partida["ultimas_jugadas"]]
                    
                if "jugadas_eliminadas" in partida:
                    partida["jugadas_eliminadas"] = [json.dumps(jugada) for jugada in partida["jugadas_eliminadas"]]

        json_texto = json.dumps(datos_copia, ensure_ascii=False, indent=4)
        json_texto = json_texto.replace('"[', '[').replace(']"', ']').replace('\\"', '')

        #Sobre-escribimos los datos
        with open(self.nombre_archivo, "w", encoding="utf-8") as archivo:
            archivo.write(json_texto)
            
        return True
    
    def registrar_partida(self, nombre, dificultad, tiempo):
        #Crea un diccionario con los datos de la partida ganada
        fecha_hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        game = {
            "dificultad": dificultad,
            "tiempo": tiempo,
            "fecha_hora": fecha_hora_actual
        }

        #Lee el json
        datos = self.read()
        if nombre not in datos:
            datos[nombre] = []
        
        #Envía los datos empaquetados para guardarlos
        datos[nombre].append(game)

        return self.save(datos)

    def guardar_partida(self,tablero,nivel,crono,timer,nombre,time,elementos,pila_ultimas,pila_eliminadas):
        #Adapta el dato clk
        print(f"crono: {crono} timer: {timer}")
        clk_type = ""
        if crono and timer:
            clk_type = "none"
        else:
            if crono:
                clk_type = "crono"
            else:
                clk_type = "timer"

        #Genera diccionario con los datos de la partida
        game = {
            "tablero":tablero,
            "nivel": nivel,
            "type": clk_type,
            "tiempo": time,
            "elementos": elementos,
            "ultimas_jugadas": pila_ultimas,
            "jugadas_eliminadas": pila_eliminadas
        }

        #Lee los datos del json
        datos = self.read()
        if nombre not in datos:
            datos[nombre] = []
            
        partidas_jugador = datos[nombre]
        partida_dificultad = False

        #Guarda la partida, sobreescribe en caso de otra partida del mismo nivel o crea una nueva en caso que no exista
        for i in range(len(partidas_jugador)):
            base_guardada = partidas_jugador[i]["nivel"].split("-")[0]
            base_actual = nivel.split("-")[0]

            if base_guardada ==  base_actual:
                partidas_jugador[i] = game
                partida_dificultad = True
                print(f"Se ha sobreescrito la partida guardada en nivel: {nivel}")
                break

        if not partida_dificultad:
            partidas_jugador.append(game)
            print(f"Se ha creado un nuevo espacio para el nivel: {nivel}")

        return self.save(datos)
    
    def cargar_partida(self, nombre, nivel):
        #Lee los datos almacenados en el json
        datos = self.read()

        #Reccorre la estructura en busca de los datos
        if nombre in datos:
            partidas_jugador = datos[nombre]

            for partida in partidas_jugador:
                base_guardada = partida["nivel"].split("-")[0]
                base_actual = nivel.split("-")[0]

                if base_guardada ==  base_actual:
                    tablero_file = partida["tablero"]
                    
                    #Convertimos el tipo de dato en caso de errores
                    tablero = [json.loads(fila) if isinstance(fila, str) else fila for fila in tablero_file]
                    ultimas_cargadas = [[jugada, (pos[0], pos[1])] for jugada, pos in partida.get("ultimas_jugadas", [])]
                    eliminadas_cargadas = [[jugada, (pos[0], pos[1])] for jugada, pos in partida.get("jugadas_eliminadas", [])]
                    
                    #Devuelve diccionario con los datos 
                    return {
                        "tablero": tablero,
                        "nivel": partida["nivel"],
                        "type": partida["type"],
                        "tiempo": partida["tiempo"],
                        "elementos": partida["elementos"],
                        "ultimas_jugadas": ultimas_cargadas,
                        "jugadas_eliminadas": eliminadas_cargadas
                    }

        return None
    
    def cargar_user(self,correo):
        datos = self.read()
        
        for id_usuario, data in datos.items():
            # Verificamos si el correo del archivo coincide con el que digita el usuario
            if data["correo"] == correo:
                elementos_int = {int(k): v for k, v in data["costum_elements"].items()}
                print(f"Datos: {elementos_int}")

                return {
                    "id": id_usuario,
                    "correo": data["correo"],
                    "codigo": data["codigo_ingreso"],
                    "nombre": data["nombre"],
                    "fecha": data["fecha_creacion"],
                    "elements": elementos_int
                }
                

    def salvar_user(self, user):
        elementos_programa = user.costum_elements if user.costum_elements else {}
        #elementos_string = {}
        #for clave in elementos_programa.items():

        elementos_string = {str(clave): valor for clave, valor in elementos_programa.items()}
        print(f"elementos string {elementos_string}")

        # 1. Empaquetamos los datos puros que vienen de la clase del usuario
        datos_usuario = {
            "correo": user.correo,
            "codigo_ingreso": user.codigo_ingreso,
            "nombre": user.nombre,
            "fecha_creacion": user.fecha_creacion,
            "costum_elements": elementos_string
        }

        # 2. Leemos el JSON actual (si no existe o está vacío, inicializamos dict vacío)
        users = self.read()
        if not users:
            users = {}

        # 3. Forzamos el ID a STRING de una vez por todas. 
        # En el JSON la llave DEBE ser un string ("1", "2", etc.)
        id_user_str = str(user.id)

        # 4. Validamos si existe o es nuevo usando la llave en string
        if id_user_str in users:
            print(f"Actualizando datos del usuario existente. ID: {id_user_str}")
        else:
            print(f"Creando nuevo registro de usuario. ID: {id_user_str}")

        # 5. Insertamos o reemplazamos directamente en el diccionario con la llave string
        users[id_user_str] = datos_usuario

        # 6. Mandamos el diccionario directo a guardarse sin clonaciones raras
        self.save(users)
        print("¡Datos guardados exitosamente en el archivo JSON!")
            


        