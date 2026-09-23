class persona:
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad
        
persona1 = persona("omar", 12)
persona2 = persona("ana", 15)
        
       
print("Nombre y edad de la primera persona es ", persona1.nombre, " y ", persona1.edad)
print("Nombre y edad de la segunda persona es ", persona2.nombre, " y ", persona2.edad)
