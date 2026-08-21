from src.estadistica import calcular_promedio
from src.estadistica import promedio_diccionario
from src.estadistica import contar_aprobados
from src.estadistica import clasificar_notas
datos = [10,15,20,25,30]

resultado = calcular_promedio(datos)

print ("el promedio de la lista es:", resultado)

notas = {
    "Juan": 3.3,
    "Ana": 4.2,
    "Pedro": 4.6,
    "laura": 3.9
}
promedio_notas = promedio_diccionario(notas)
print("El promedio de las notas es:", promedio_notas)

aprobados = contar_aprobados(notas, 3.5)
print("El número de aprobados es:", aprobados)

clasificacion = clasificar_notas(notas)
print("La clasificación de las notas es:", clasificacion)