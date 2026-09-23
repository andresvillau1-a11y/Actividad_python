from flask import Flask, render_template, request,redirect, url_for, flash, session
from database.conexion import obtener_conexion

app = Flask(__name__)
app.secret_key = "adso2026"

@app.route("/")
def inicio():
     conexion = obtener_conexion()
     cursor = conexion.cursor(dictionary=True)
     cursor.execute("SELECT * FROM productos")
     productos = cursor.fetchall()
     cursor.close()
     conexion.close()
     return render_template("index1.html", productos = productos)

@app.route("/productos")
def productos():
    conexion = obtener_conexion()

    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT * FROM productos")

    productos = cursor.fetchall()

    cursor.close()

    conexion.close()

    return render_template("productos.html",productos=productos)

@app.route("/contacto")
def contacto():
    return render_template("contacto.html")

@app.route("/nosotros")
def nosotros():
    return render_template("nosotros.html")

@app.route("/servicios")
def servicios():
    return render_template("servicios.html")

@app.route("/catalogo")
def catalogo():
    return render_template("catalogo.html")

#Proteccion de rutas

@app.route("/registro_producto")
def registro_producto():
    if "usuario" not in session:

        return redirect(url_for("inicio"))
    return render_template("registro_producto.html")


@app.route("/guardar_producto",methods=["POST"])
def guardar_producto():

        if "usuario" not in session:
            return redirect(url_for("inicio"))
        
        codigo = request.form["codigo"].strip()
        nombre = request.form["nombre"].strip()
        precio = request.form["precio"]
        categoria = request.form["categoria"].strip()


    # return render_template(
    #     "respuesta.html",
    #     codigo=codigo,
    #     nombre=nombre,
    #     precio=precio,
    #     categoria=categoria
    # )
        conexion = obtener_conexion()

        cursor = conexion.cursor()

        sql = """ INSERT INTO productos (codigo,nombre,precio,categoria) VALUES (%s,%s,%s,%s) """

        cursor.execute(
        sql,
        (
            codigo,
            nombre,
            precio,
            categoria
         )
        ) 

        conexion.commit()

        flash("Producto registrado correctamente", "success")
        
        cursor.close()
        conexion.close()

        return redirect(url_for("productos"))


@app.route("/editar_producto/<codigo>")
def editar_producto(codigo):

    # Verificar si existe una sesión activa
    if "usuario" not in session:
        return redirect(url_for("inicio"))

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    sql = """
    SELECT *
    FROM productos
    WHERE codigo=%s
    """

    cursor.execute(sql, (codigo,))

    producto = cursor.fetchone()

    cursor.close()
    conexion.close()

    return render_template(
        "editar_producto.html",
        producto=producto
    )

@app.route("/actualizar_producto", methods=["POST"])
def actualizar_producto():

    if "usuario" not in session:
        return redirect(url_for("inicio"))

    codigo = request.form["codigo"]
    nombre = request.form["nombre"]
    precio = request.form["precio"]
    categoria = request.form["categoria"]

    # Obtener la conexión
    conexion = obtener_conexion()

    # Crear el cursor
    cursor = conexion.cursor()

    # Consulta SQL
    sql = """UPDATE productos SET nombre = %s,precio = %s,categoria = %s  WHERE codigo = %s """

    cursor.execute(
        sql,
        (
            nombre,
            precio,
            categoria,
            codigo
        )
    )

    # Guardar los cambios
    conexion.commit()

    # Cerrar recursos
    cursor.close()
    conexion.close()

    # Mensaje de éxito
    flash("Producto actualizado correctamente", "success")

    # Redireccionar al listado
    return redirect(url_for("productos"))

@app.route("/eliminar_producto/<codigo>")
def eliminar_producto(codigo):


    if "usuario" not in session:
        return redirect(url_for("inicio"))
    
    conexion = obtener_conexion()
    
    cursor = conexion.cursor()

    sql = """DELETE FROM productos WHERE codigo=%s"""

    cursor.execute(sql,(codigo,))

    conexion.commit()
   
    flash("Producto eliminado correctamente", "success")

    cursor.close()
    conexion.close()

    return redirect(url_for("productos"))

@app.route("/registrar_usuario", methods=["POST"])
def registrar_usuario():
    nombre = request.form["nombre"].strip()
    correo = request.form["correo"].strip().lower()
    telefono = request.form.get("telefono", "").strip()
    password = request.form["password"]
    password2 = request.form.get("password2", "")

    # Validaciones básicas
    if not nombre or not correo or not password:
        flash("Todos los campos son obligatorios", "danger")
        return redirect(url_for("inicio"))

    if telefono and not telefono.replace("+", "").isdigit():
        flash("El teléfono solo debe contener números", "danger")
        return redirect(url_for("inicio"))

    if password != password2:
        flash("Las contraseñas no coinciden", "danger")
        return redirect(url_for("inicio"))

    if len(password) < 6:
        flash("La contraseña debe tener al menos 6 caracteres", "danger")
        return redirect(url_for("inicio"))

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    # Verificar que el correo no esté registrado
    cursor.execute("SELECT id FROM usuarios WHERE correo=%s", (correo,))
    if cursor.fetchone():
        cursor.close()
        conexion.close()
        flash("Ese correo ya está registrado", "danger")
        return redirect(url_for("inicio"))

    # Guardar la contraseña como HASH (nunca en texto plano)
    from werkzeug.security import generate_password_hash
    password_hash = generate_password_hash(password)

    # El rol se asigna SIEMPRE automáticamente como Cliente.
    # Nunca se toma del formulario: un usuario no puede autoasignarse
    # un rol privilegiado como Administrador.
    rol_automatico = "Cliente"

    sql = """INSERT INTO usuarios (nombre, correo, telefono, password, rol) VALUES (%s, %s, %s, %s, %s)"""
    cursor.execute(sql, (nombre, correo, telefono or None, password_hash, rol_automatico))
    conexion.commit()

    cursor.close()
    conexion.close()

    flash("¡Cuenta creada correctamente! Ahora puedes iniciar sesión", "success")
    return redirect(url_for("inicio"))


@app.route("/login", methods=["POST"])
def login():
    correo = request.form["correo"].strip().lower()
    password = request.form["password"]

    conexion = obtener_conexion()

    cursor = conexion.cursor(dictionary=True)

    sql = """ 
    SELECT * FROM usuarios WHERE correo=%s AND estado='Activo' 
    """

    cursor.execute(sql,(correo,))

    usuario = cursor.fetchone()

    cursor.close()
    conexion.close()

    from werkzeug.security import check_password_hash

    # Usuario nuevo (contraseña con hash) o antiguo (texto plano, ej: juan)
    if usuario and (check_password_hash(usuario["password"], password)
                    or usuario["password"] == password):
        session["usuario"]= usuario["nombre"]
        session["rol"] = usuario["rol"]

        flash(f"¡Bienvenido {usuario['nombre']}! Sesión iniciada correctamente", "success")

        return redirect(url_for("admin"))
    else:
        flash("Correo o contraseña incorrectos","danger")

        return redirect(url_for("inicio"))
    

@app.route("/admin")
def admin():

    if "usuario" not in session:

        return redirect(url_for("inicio"))

    return render_template("admin.html")

@app.route("/logout")
def logout():

    session.clear()

    flash("Sesión cerrada correctamente", "info")

    return redirect(url_for("inicio"))

app.run(debug=True)

# TechStore/
# │
# ├── app.py
# │
# ├── templates/
# │   ├── index.html
# │   ├── registro_producto.html
# │   └── respuesta.html
# │
# └── static/