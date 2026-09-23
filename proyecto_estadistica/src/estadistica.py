def validar_lista(lista):
    if not lista:
        raise ValueError("La lista no puede estar vacía") 

def calcular_promedio(lista):
    validar_lista(lista)
    suma = sum(lista)
    cantidad= len(lista)
    promedio = suma/cantidad
    return promedio 

def promedio_diccionario(diccionario):
    valores = diccionario.values()
    suma = sum(valores)
    cantidad= len(valores)
    promedio = suma/cantidad
    return promedio 

def contar_aprobados (diccionario, nota_minima):
    valores = diccionario.values()
    contador = 0
    for nota in valores:
        if nota >= nota_minima:
            contador += 1
    return contador

def clasificar_notas(diccionario):
    valores = diccionario.values()
    resultado = {
        "bajas": 0,
        "medias": 0,
        "altas": 0
    }
    
    for nota in valores:
        if nota < 3.0:
            resultado["bajas"] += 1
        elif nota < 4.0:
            resultado["medias"] += 1
        else:
            resultado["altas"] += 1
            return resultado
