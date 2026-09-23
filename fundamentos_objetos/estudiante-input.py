class estudiante:
    def __init__(self, nombre, nota):
        self.nombre = nombre
        self.nota = nota

    def mostrar_informacion(self):
        if self.nota >= 3.0:
            estado = "Aprobado"
        else:
            estado = "Reprobado"
        return f"Nombre del estudiante: {self.nombre}, Nota: {self.nota}, Estado: {estado}"    
nombre = input("Ingrese el nombre del estudiante: ")
nota = float(input("Ingrese la nota del estudiante: "))    

e1 = estudiante(nombre, nota)
print(e1.mostrar_informacion())