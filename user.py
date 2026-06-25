class User:
    def __init__(self,id,correo,codigo_ingreso, nombre,fecha_creacion,costum_elements=None):
        self.id = id 
        self.correo = correo
        self.codigo_ingreso = codigo_ingreso
        self.nombre = nombre
        self.fecha_creacion = fecha_creacion
        self.costum_elements = costum_elements

    