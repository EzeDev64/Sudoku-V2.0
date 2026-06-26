class Partida:
    def __init__(self,name,time,fecha): # recibe cada uno de los atributos (datos) de una partida para crear el objeto
        self.name = name
        self.time = time
        self.fecha = fecha
        return
    
    def get_partida(self): # retorna un string formateado con los datos a desplegar de una partida
        data = f"Tiempo: {self.time} Jugador: {self.name} Fecha: {self.fecha}"
        return data