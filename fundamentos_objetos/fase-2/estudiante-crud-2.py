class Estudiante: 
    def __init__(self,codigo,nombre,nota):
        self.codigo = codigo
        self.nombre = nombre
        self.nota = nota
        
    def estado(self):
        if self.nota >= 3.0:
            return "Aprobado"
        else:
            return "Reprobado"
        
    def mostrar_informacion(self):    
        return f"Código: {self.codigo},Nombre: {self.nombre}, Nota: {self.nota}, Estado: {self.estado()}"
        
class SistemaEstudiantes:
    def __init__(self):
        self.estudiantes = []  
        
    def registrar_estudiante(self):
        codigo = input("Ingrese el código del estudiante: ")
        
        for est in self.estudiantes:
            if est.codigo == codigo:
                print("El código ya existe. No se puede registrar el estudiante.")
                return
        nombre = input("Ingrese el nombre del estudiante: ")
        
        while True:
            nota = float(input("Ingrese la nota del estudiante (0.0 - 5.0): "))
            
            if 0.0 <= nota <= 5.0:
                break
            else:
                print("Nota no válida. Por favor, ingrese una nota entre 0.0 y 5.0.")
        nuevo_estudiante = Estudiante(codigo, nombre, nota)
        self.estudiantes.append(nuevo_estudiante)   
        print("Estudiante registrado exitosamente.")
   
    def mostrar_estudiantes(self):
        
        if len(self.estudiantes) == 0:
            print("No hay estudiantes registrados.")
            
        else:
            print("\nLista de estudiantes:")
            
            for est in self.estudiantes:
                print(est.mostrar_informacion())
                
    def buscar_estudiante(self):
        codigo = input("Ingrese el código del estudiante a buscar: ")
        for est in self.estudiantes:
            if est.codigo == codigo:
                print(est.mostrar_informacion())
                return
        print("Estudiante no encontrado.")

    def menu(self):
        while True:
            print("""
                  === Menú de Gestión de Estudiantes ===
                  1. Registrar estudiante
                  2. Mostrar estudiantes
                  3. Buscar estudiante por código
                  4. eliminar estudiante por código
                  5. Actualizar estudiante por código
                  6. Calcular promedio general
                  7. Guardar estudiantes
                  8. Estadísticas
                  9. Salir
                  """)
            opcion = input("Seleccione una opción: ")
            if opcion == "1":
                self.registrar_estudiante()
            elif opcion == "2":
                self.mostrar_estudiantes()
            elif opcion == "3":
                self.buscar_estudiante()
            elif opcion == "4":
                self.eliminar_estudiante() 
            elif opcion == "5":     
                self.actualizar_estudiante()
            elif opcion == "6":
                self.calcular_promedio()
            elif opcion == "7":
                self.guardar_estudiantes()
            elif opcion == "8":
                self.estadistica()
            elif opcion == "9":    
                print("Saliendo del programa. ¡Hasta luego!")
                break
            else:
                print("Opción no válida. Por favor, seleccione una opción del menú.")
            
            
    def eliminar_estudiante(self):
        codigo_eliminar = input("Ingrese el código del estudiante a eliminar: ")
        for est in self.estudiantes:
            if est.codigo == codigo_eliminar:
                self.estudiantes.remove(est)
                print("Estudiante eliminado exitosamente.")
                return
        print("Estudiante no encontrado.")     
        
    def actualizar_estudiante(self):
        codigo_buscar = input("Ingrese el código del estudiante a actualizar: ")
        
        for est in self.estudiantes:
            if est.codigo == codigo_buscar:
                
                while True:
                    nueva_nota = float(input("Ingrese la nueva nota del estudiante (0.0 - 5.0): "))
                    if 0.0 <= nueva_nota <= 5.0:
                        est.nota = nueva_nota
                        print("nota actualizado exitosamente.")
                        return
                    else:
                        print("La nota no es válida. Por favor, ingrese una nota entre 0.0 y 5.0.")
                        
                        
    def calcular_promedio(self):
        
        if len(self.estudiantes) == 0:
            print("No hay estudiantes registrados para calcular el promedio.")
            return
        
        total_notas = sum(est.nota for est in self.estudiantes)
        promedio = total_notas / len(self.estudiantes)
        print(f"El promedio de las notas de los estudiantes es: {promedio:.2f}")
    
    def guardar_estudiantes(self):
        with open("estudiantes.txt", "w") as archivo:
            for est in self.estudiantes:
                archivo.write(f"{est.codigo},{est.nombre},{est.nota}\n")
        print("Estudiantes guardados en estudiantes.txt exitosamente.")
    
    def estadistica (self):
        
        aprobados = 0
        reprobados = 0
        
        for est in self.estudiantes:
            if est.nota >= 3.0:
                aprobados += 1
            else:
                reprobados += 1
        print(f"Total de estudiantes aprobados: {aprobados}")
        print(f"Total de estudiantes reprobados: {reprobados}")    
        
sitema = SistemaEstudiantes()
sitema.menu()     
           