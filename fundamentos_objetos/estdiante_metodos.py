class Estudiante:
    def __init__(self,nombre,nota):
        self.nombre = nombre
        self.nota = nota

def mostrar_informacion(self):
    if self.nota >= 3.0:
        estado = "Aprobado"
    else:
        estado = "Reprobado"
    return f"Nombre del estudiante: {self.nombre}, Nota: {self.nota}, Estado: {estado}"



    def mostrar_informacion(self):
        return f"Nombre del estudiante: {self.nombre}, Nota: {self.nota}"
e1 = Estudiante("Juan", 4.2)
