precios = [2500,3000,1500,5000]

precios_con_iva = []

for precio in precios:
        impuesto = precio + (precio * 0.19)
        precios_con_iva.append(impuesto)
print("Precios con IVA:", precios_con_iva)