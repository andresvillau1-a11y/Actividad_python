class estudiante:
    def __init__(self, nombre, nota):
        self._nombre = nombre
        self._nota = nota
        
    def get__nota (self):
        return self._nota
    
    def set__nota (self, nueva_nota):
        if nueva_nota >= 0 and nueva_nota <= 5:
            self._nota = nueva_nota
        else:
            print("La nota debe estar entre 0 y 5")
            
            
estudiantes = []

for i in range(3):
    
    nombre = input("Ingrese el nombre del estudiante: ")
    
    while True:
        nota = float(input("Ingrese la nota del estudiante (0.0 - 5.0): "))
        
        if 0 <= nota <= 5:
            break
        else:
            print("La nota debe estar entre 0 y 5")
            
            
    e = estudiante(nombre, nota)
    estudiantes.append(e)
    
    print("lista de estudiantes registrados:")
    
    for est in estudiantes:
        print(f"Nombre: ", est.nombre)
        print(f"Nota: ", est.get__nota())