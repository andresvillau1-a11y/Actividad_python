class Estudiante:
    def __init__(self, nombre,nota):
        self.nombre = nombre
        self.nota = nota


e1 = Estudiante("Juan", 4.2)
print("Nombre del estudiante:", e1.nombre)

e2 = Estudiante("Ana", 3.8)
print("Nombre del estudiante:", e2.nombre)