class Producto:
    def __init__(self, codigo, nombre, precio, cantidad, categoria):
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad
        self.categoria = categoria

    def mostrar_info(self):
     return f"""
Codigo: {self.codigo}
Nombre: {self.nombre}
Precio: {self.precio}
Cantidad: {self.cantidad}
Categoria: {self.categoria}
---------------------------
"""

class SistemaInventario:
    def __init__(self):
        self.productos = []

    
    def registrar_producto(self):
        codigo = input("Ingrese codigo de el producto").strip()
        if codigo == "":
            print("El codigo no puede estar vacio")
            return

        for prod in self.productos:
            if prod.codigo == codigo:
                print("Error: El codigo ya existe")
                return
        nombre = input("Ingrese nombre del producto: ").strip()

        if nombre == "":
            print("El nombre no puede estar vacio")
            return

        while True:
            precio = float(input("Ingrese precio: "))
            if precio >= 0:
                break
            else:
                print(" El precio no puede ser negativo")

        while True:
            cantidad = int(input("Ingrese cantidad : "))
            if cantidad >= 0:
                break
            else:
                print("La cantidad no puede ser negativa")
        categoria = input("Ingrese categoria: ").strip()

        if categoria == "":
            print("Error: La categoria no puede estar vacia")
            return
        nuevo_producto = Producto(
            codigo,
            nombre,
            precio,
            cantidad,
            categoria
        )
        self.productos.append(nuevo_producto)
        print("Producto registrado ")

    def mostrar_productos(self):

        if len(self.productos) == 0:
            print("No hay productos registrados")
        else:
            print("\n Lista de productos ")
            for prod in self.productos:
                print(prod.mostrar_info())

    def buscar_producto(self):
        print("""
1. Buscar por codigo
2. Buscar por nombre""")

        opcion = input("Seleccione una opcion: ")
        if opcion == "1":
            codigo_buscar = input("Ingrese codigo: ")
            for prod in self.productos:
                if prod.codigo == codigo_buscar:
                    print("\nProducto encontrado")
                    print(prod.mostrar_info())
                    return

            print("Producto no encontrado")
        elif opcion == "2":
            nombre_buscar = input("Ingrese nombre: ").lower()
            for prod in self.productos:
                if prod.nombre.lower() == nombre_buscar:
                    print("\nProducto encontrado")
                    print(prod.mostrar_info())
                    return
                print("Producto no encontrado")
        else:
            print("Opcion invalida")
    def actualizar_producto(self):
        codigo_buscar = input("Ingrese codigo del producto: ")

        for prod in self.productos:
            if prod.codigo == codigo_buscar:
                print("\nProducto encontrado")

                while True:
                    nuevo_precio = float(input("Nuevo precio: "))
                    if nuevo_precio >= 0:
                        prod.precio = nuevo_precio
                        break
                    else:
                        print("Precio invalido")
                while True:
                    nueva_cantidad = int(input("Nueva cantidad: "))
                    if nueva_cantidad >= 0:
                        prod.cantidad = nueva_cantidad
                        break
                    else:
                        print("Cantidad invalida")

                nueva_categoria = input("Nueva categoria: ").strip()
                if nueva_categoria != "":
                    prod.categoria = nueva_categoria
                else:
                    print("Categoria vacia, no se actualizo")
                print("Producto actualizado correctamente")
                return
        print("Producto no encontrado")

    def eliminar_producto(self):
        codigo_eliminar = input("Ingrese codigo del producto a eliminar: ")
        for prod in self.productos:
            if prod.codigo == codigo_eliminar:
                self.productos.remove(prod)
                print("Producto eliminado correctamente")
                return
        print("Producto no encontrado")

    def calcular_total_inventario(self):
        total = 0
        for prod in self.productos:
            total += prod.precio * prod.cantidad
        print(f"\nValor total del inventario: {total}")

    def mostrar_agotados(self):
        agotados = False
        print("\n productos agotados: ")

        for prod in self.productos:
            if prod.cantidad == 0:
                print(prod.mostrar_info())
                agotados = True
        if agotados == False:
            print("No hay productos agotados")

    def guardar_archivo(self):
        with open("inventario.txt", "w") as archivo:
            for prod in self.productos:
                archivo.write(prod.mostrar_info() + "\n")
        print("Archivo guardado correctamente")

    def menu(self):
        while True:
            print("""
========== MENU INVENTARIO ==========
1 Registrar producto
2 Mostrar productos
3 Buscar producto
4 Actualizar producto
5 Eliminar producto
6 Calcular total inventario
7 Mostrar productos agotados
8 Guardar archivo
9 Salir
=====================================
""")

            opcion = input("Seleccione una opcion: ")
            if opcion == "1":
                self.registrar_producto()

            elif opcion == "2":
                self.mostrar_productos()

            elif opcion == "3":
                self.buscar_producto()

            elif opcion == "4":
                self.actualizar_producto()

            elif opcion == "5":
                self.eliminar_producto()

            elif opcion == "6":
                self.calcular_total_inventario()

            elif opcion == "7":
                self.mostrar_agotados()

            elif opcion == "8":
                self.guardar_archivo()

            elif opcion == "9":
                print("Saliendo del sistema...")
                break

            else:
                print("Opcion invalida")
sistema = SistemaInventario()
sistema.menu()