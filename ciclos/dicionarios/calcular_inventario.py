productos = {
    "arroz" : 2500,
    "leche" : 3000,
    "pan" : 1500,
    "huevos" : 5000
}

total = 0

for precio in productos.values():
    total += precio
print("Valor total del inventario:", total)