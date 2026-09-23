productos = {
    "arroz": 2500,
    "leche": 3000,
    "pan": 1500,
    "huevos": 5000
}

for nombre, precio in productos.items():
    if precio > 3000:
        print("Producto con precio mayor a 3000:", nombre, "Precio:", precio)