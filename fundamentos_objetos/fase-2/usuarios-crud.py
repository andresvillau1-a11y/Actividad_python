class Usuario:
 def __init__(self, documento, nombre, correo, rol, estado):
    self.documento = documento
    self.nombre = nombre
    self.correo = correo
    self.rol = rol
    self.estado = estado

def mostrar_info(self):

        return f"""
Documento: {self.documento}
Nombre: {self.nombre}
Correo: {self.correo}
Rol: {self.rol}
Estado: {self.estado}
-------------------------
"""
class SistemaUsuarios:
    def __init__(self):
        self.usuarios = []
    def registrar_usuario(self):
        documento = input("Ingrese el documento: ").strip()

        if documento == "":
            print("ingresar el documento es obligatorio")
            return
        for user in self.usuarios:
            if user.documento == documento:
                print("El documento ya existe")
                return
        nombre = input("Ingrese nombre: ").strip()
        if nombre == "":
            print("Debe ingresar algun nombre")
            return
        
        correo = input("Ingrese correo: ").strip()
        if "@" not in correo or "." not in correo:
            print("el Correo  esta invalido")
            return
        for user in self.usuarios:
            if user.correo == correo:
                print("Ese correo ya esta registrado")
                return
        roles = ["Administrador", "Aprendiz", "Instructor"]
        print("\nRoles disponibles:")

        for rol in roles:
            print("-", rol)
        rol = input("Ingrese rol: ").strip()
        if rol not in roles:
            print("Rol incorrecto")
            return

        estados = ["Activo", "Inactivo"]
        estado = input("Ingrese estado: ").strip()

        if estado not in estados:
            print("Estado no valido")
            return
        nuevo = Usuario(
            documento,
            nombre,
            correo,
            rol,
            estado
        )

        self.usuarios.append(nuevo)
        print("Usuario agregado correctamente")
    def mostrar_usuarios(self):
        if len(self.usuarios) == 0:
            print("No hay usuarios registrados")
            
        else:
            print("\n--- Lista de usuarios ---")
            for user in self.usuarios:
                print(user.mostrar_info())
    def buscar_usuario(self):
        print("""
1. Buscar por documento
2. Buscar por correo
""")

        opcion = input("Seleccione una opcion: ")
        if opcion == "1":
            buscar_doc = input("Ingrese documento: ")
            for user in self.usuarios:
                
                if user.documento == buscar_doc:
                    print("\nUsuario encontrado")
                    print(user.mostrar_info())
                    return

            print("No existe el usuario")
        elif opcion == "2":
            buscar_correo = input("Ingrese correo: ")
            for user in self.usuarios:

                if user.correo == buscar_correo:
                    print("\nUsuario encontrado")
                    print(user.mostrar_info())
                    return
            print("No existe el usuario")
        else:
            print("Opcion incorrecta")

   
    def actualizar_usuario(self):
        buscar_doc = input("Documento del usuario: ")
        for user in self.usuarios:
            if user.documento == buscar_doc:
                print("\nUsuario encontrado")
                nuevo_nombre = input("Nuevo nombre: ").strip()
                if nuevo_nombre != "":
                    user.nombre = nuevo_nombre
                nuevo_correo = input("Nuevo correo: ").strip()
                if "@" in nuevo_correo and "." in nuevo_correo:
                    user.correo = nuevo_correo
                else:
                    print("Correo invalido")

                roles = ["Administrador", "Aprendiz", "Instructor"]
                nuevo_rol = input("Nuevo rol: ").strip()

                if nuevo_rol in roles:
                    user.rol = nuevo_rol
                else:
                    print("Rol no valido")
                estados = ["Activo", "Inactivo"]
                nuevo_estado = input("Nuevo estado: ").strip()

                if nuevo_estado in estados:
                    user.estado = nuevo_estado

                else:
                    print("Estado incorrecto")

                print("Datos actualizados")
                return

        print("Usuario no encontrado")

    
    def eliminar_usuario(self):
        doc_eliminar = input("Ingrese documento del usuario: ")
        for user in self.usuarios:
            if user.documento == doc_eliminar:
                self.usuarios.remove(user)

                print("Usuario eliminado")
                return
        print("No se encontro el usuario")

    def mostrar_activos(self):
        activos = False
        print("\n Usuarios activos ")

        for user in self.usuarios:

            if user.estado == "Activo":

                print(user.mostrar_info())
                activos = True

        if not activos:
            print("No hay usuarios activos")


    def contar_roles(self):

        admins = 0
        aprendices = 0
        instructores = 0

        for user in self.usuarios:

            if user.rol == "Administrador":
                admins += 1

            elif user.rol == "Aprendiz":
                aprendices += 1

            elif user.rol == "Instructor":
                instructores += 1

        print("\n--- Usuarios por rol ---")
        print("Administradores:", admins)
        print("Aprendices:", aprendices)
        print("Instructores:", instructores)

    def guardar_archivo(self):
        with open("usuarios.txt", "w") as archivo:
            for user in self.usuarios:
                archivo.write(user.mostrar_info())
                archivo.write("\n")
        print("Archivo guardado")


    def menu(self):
        while True:
            print("""
======= MENU =======

1. Registrar usuario
2. Mostrar usuarios
3. Buscar usuario
4. Actualizar usuario
5. Eliminar usuario
6. Usuarios activos
7. Contar roles
8. Guardar archivo
9. Salir

====================
""")
            opcion = input("Seleccione una opcion: ")
            if opcion == "1":
                self.registrar_usuario()
            elif opcion == "2":
                self.mostrar_usuarios()
            elif opcion == "3":
                self.buscar_usuario()
            elif opcion == "4":
                self.actualizar_usuario()
            elif opcion == "5":
                self.eliminar_usuario()
            elif opcion == "6":
                self.mostrar_activos()
            elif opcion == "7":
                self.contar_roles()
            elif opcion == "8":
                self.guardar_archivo()
            elif opcion == "9":
                print("Salir")
                break
            else:
                print("Opcion invalida")
sistema = SistemaUsuarios()
sistema.menu()