
productos = {
    "arroz" : 2500,
    "leche" : 3000,
    "pan" : 1500,
    "huevos" : 5000
}
contador = 0
for precio in productos.values():
    if precio < 2000:
        contador += 1
print("Número de productos con precio bajo:", contador)
