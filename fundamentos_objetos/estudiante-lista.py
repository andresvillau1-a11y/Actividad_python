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
    
estudent= []
    
for i in range(3):
    print(f"\n  Estudiante {i+1}:")
    nombre = input("Ingrese el nombre del estudiante: ")
    nota = float(input("Ingrese la nota del estudiante: "))
    e = estudiante(nombre, nota)
    estudent.append(e)

print(f"\n  lista de estudiantes:")
for e in estudent:
    print(e.mostrar_informacion())