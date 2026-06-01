productos = {
    "arroz" : 2500,
    "leche" : 3000,             
    "pan" : 1500,
    "huevos" : 5000
}

mayor = 0
producto_mayor = ""

for nombre, precio in productos.items():
    if precio > mayor:
        mayor = precio
        producto_mayor = nombre
print("Producto más caro:", producto_mayor, "Precio:", mayor)