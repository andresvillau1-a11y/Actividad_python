class estudiantes:
    contadorAprobados = 0
    contadorNoAprobados = 0
    
    def __init__(self, nombre, nota):
        self.nombre = nombre
        self.nota = nota
        
        if self.nota >= 3.0:
            estudiantes.contadorAprobados += 1
        else:
            estudiantes.contadorNoAprobados += 1
            
    def mostrar_informacion(self):
        if self.nota >= 3.0:
            estado = "Aprobado"
        else:
            estado = "No Aprobado"
        return f"Nombre del estudiante: {self.nombre}, Nota: {self.nota}, Estado: {estado}"
    
estudent = []
    
for i in range(3):
    print(f"\n  Estudiante {i+1}:")
    nombre = input(" nombre  ")
        
    while True:
        nota = float (input(" ingrese la nota (0.0 - 5.0)  "))
        if nota >= 0.0 and nota <= 5.0:
            break
        else:          
            print("nota o valida ")        
            e = estudiantes(nombre, nota)
            estudent.append(e)
                    
        print(f"\n  lista de estudiantes:")
        for e in estudent:
            print(e.mostrar_informacion())
        
print(f"\nTotal de estudiantes aprobados: {estudiantes.contadorAprobados}")
print(f"Total de estudiantes no aprobados: {estudiantes.contadorNoAprobados}")