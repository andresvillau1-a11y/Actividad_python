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
            
            
e1 = estudiante("Omar", 4.5)
print(e1.get__nota())

e1.set__nota(-2)
            