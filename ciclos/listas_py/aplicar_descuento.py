precios = [2500,3000,1500,5000]

for precio in precios:
    descuento = precio * 0.10
    precio_con_descuento = precio - descuento
    print("Precio original:", precio, "Precio con descuento:", precio_con_descuento)