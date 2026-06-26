import pickle
import os

class PickleParser:
    def __init__(self, nombre_archivo="sudoku2026_bitácora_jugadas.pkl"):
        self.nombre_archivo = nombre_archivo

    #Guarda la información
    def save(self, datos):
        try:
            with open(self.nombre_archivo, "wb") as archivo:
                pickle.dump(datos, archivo)
            print(f"Datos guardados exitosamente en '{self.nombre_archivo}'.")
        except Exception as e:
            print(f"Error al guardar en el archivo: {e}")


    def read(self):
        if not os.path.exists(self.nombre_archivo):
            print(f"El archivo '{self.nombre_archivo}' no existe todavía. Devolviendo estructura vacía.")
            return {}
        
        try:
            with open(self.nombre_archivo, "rb") as archivo:
                datos_cargados = pickle.load(archivo)
            return datos_cargados
        except Exception as e:
            print(f"Error al leer el archivo: {e}")
            return {}