from flask import Flask, render_template, request,redirect, url_for, flash, session
from functools import wraps
from database.conexion import obtener_conexion

app = Flask(__name__)
app.secret_key = "adso2026"

def requiere_rol(*roles_permitidos):
    """Protege una ruta """
    def decorador(ruta):
        @wraps(ruta)
        def envoltura(*args, **kwargs):
            if "usuario" not in session:
                flash("Debes iniciar sesión", "danger")
                return redirect(url_for("inicio"))
            if session.get("rol") not in roles_permitidos:
                flash("No tienes permiso para acceder a esa página", "danger")
                if session.get("rol") == "Administrador":
                    return redirect(url_for("productos"))
                return redirect(url_for("panel_cliente"))
            return ruta(*args, **kwargs)
        return envoltura
    return decorador

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
@requiere_rol("Administrador")
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
@requiere_rol("Administrador")
def registro_producto():
    return render_template("registro_producto.html")


@app.route("/guardar_producto",methods=["POST"])
@requiere_rol("Administrador")
def guardar_producto():

        import re
        import os
        from werkzeug.utils import secure_filename

        # b. Eliminar espacios innecesarios al inicio y al final
        codigo = request.form["codigo"].strip()
        nombre = request.form["nombre"].strip()
        precio_texto = request.form["precio"].strip()
        categoria = request.form["categoria"].strip()
        imagen = request.files.get("imagen")

        errores = []

        # a. Ningún campo puede quedar vacío
        if not codigo or not nombre or not precio_texto or not categoria:
            errores.append("Ningún campo puede quedar vacío")

        # e. Código: comienza con P seguido de mínimo 3 números (ej: P001, P0001)
        if codigo and not re.fullmatch(r"P\d{3,}", codigo):
            errores.append("El código debe comenzar con la letra P seguida de mínimo 3 números (ej: P001). No acepta letras, espacios ni otros caracteres")

        # g. y h. Nombre: mínimo 5 y máximo 100 caracteres
        if nombre and len(nombre) < 5:
            errores.append("El nombre del producto debe tener al menos 5 caracteres")
        if nombre and len(nombre) > 100:
            errores.append("El nombre del producto no puede superar los 100 caracteres")

        # c. e i. Precio: mayor que cero y máximo 50000000
        precio = None
        try:
            precio = float(precio_texto)
            if precio <= 0:
                errores.append("El precio debe ser mayor que cero")
            if precio > 50000000:
                errores.append("El precio no puede ser mayor a 50.000.000")
        except ValueError:
            errores.append("El precio debe ser un número válido")

        # j. El formulario debe solicitar una imagen del producto
        nombre_archivo = None
        if not imagen or imagen.filename == "":
            errores.append("Debe seleccionar una imagen del producto")
        else:
            extensiones_permitidas = {"png", "jpg", "jpeg", "gif", "webp"}
            extension = imagen.filename.rsplit(".", 1)[-1].lower()
            if extension not in extensiones_permitidas:
                errores.append("La imagen debe ser formato png, jpg, jpeg, gif o webp")

        # d. Código duplicado: validar contra la base de datos
        if codigo and not errores:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("SELECT codigo FROM productos WHERE codigo=%s", (codigo,))
            if cursor.fetchone():
                errores.append(f"El código {codigo} ya está registrado")
            cursor.close()
            conexion.close()

        # Mostrar todos los errores y no guardar nada
        if errores:
            for error in errores:
                flash(error, "danger")
            return redirect(url_for("registro_producto"))

        # Guardar la imagen en static/img/productos
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        nombre_archivo = secure_filename(f"{codigo}.{extension}")
        ruta_carpeta = os.path.join("static", "img", "productos")
        os.makedirs(ruta_carpeta, exist_ok=True)
        imagen.save(os.path.join(ruta_carpeta, nombre_archivo))

        sql = """ INSERT INTO productos (codigo,nombre,precio,categoria,imagen) VALUES (%s,%s,%s,%s,%s) """

        cursor.execute(
        sql,
        (
            codigo,
            nombre,
            precio,
            categoria,
            nombre_archivo
         )
        ) 

        conexion.commit()

        flash("Producto registrado correctamente", "success")
        
        cursor.close()
        conexion.close()

        return redirect(url_for("productos"))


@app.route("/editar_producto/<codigo>")
@requiere_rol("Administrador")
def editar_producto(codigo):

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
@requiere_rol("Administrador")
def actualizar_producto():

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
@requiere_rol("Administrador")
def eliminar_producto(codigo):

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
        session["id_usuario"] = usuario["id"]

        flash(f"¡Bienvenido {usuario['nombre']}! Sesión iniciada correctamente", "success")

        # Redirigir según el rol del usuario
        if usuario["rol"] == "Administrador":
            return redirect(url_for("productos"))
        return redirect(url_for("panel_cliente"))
    else:
        flash("Correo o contraseña incorrectos","danger")

        return redirect(url_for("inicio"))
    

@app.route("/admin")
@requiere_rol("Administrador")
def admin():

    return render_template("admin.html")


@app.route("/cliente")
@requiere_rol("Cliente")
def panel_cliente():

    # Consultar los datos personales del usuario en sesión
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT id, nombre, correo, telefono, rol, estado FROM usuarios WHERE id=%s", (session["id_usuario"],))
    datos = cursor.fetchone()
    cursor.close()
    conexion.close()

    return render_template("cliente.html", usuario=datos)


@app.route("/actualizar_datos", methods=["POST"])
@requiere_rol("Cliente", "Administrador")
def actualizar_datos():

    id_sesion = session["id_usuario"]
    nombre = request.form["nombre"].strip()
    telefono = request.form.get("telefono", "").strip()

    if not nombre:
        flash("El nombre no puede quedar vacío", "danger")
        return redirect(url_for("panel_cliente"))

    if telefono and not telefono.replace("+", "").isdigit():
        flash("El teléfono solo debe contener números", "danger")
        return redirect(url_for("panel_cliente"))

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # El cliente solo puede actualizar SUS PROPIOS datos (id de sesión)
    sql = "UPDATE usuarios SET nombre=%s, telefono=%s WHERE id=%s"
    cursor.execute(sql, (nombre, telefono or None, id_sesion))
    conexion.commit()

    cursor.close()
    conexion.close()

    # Mantener la sesión con el nombre nuevo
    session["usuario"] = nombre

    flash("Datos actualizados correctamente", "success")
    return redirect(url_for("panel_cliente"))


@app.route("/reporte_pdf")
@requiere_rol("Administrador")
def reporte_pdf():

    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    from io import BytesIO

    # Consultar los productos
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT codigo, nombre, precio, categoria FROM productos ORDER BY codigo")
    productos = cursor.fetchall()
    cursor.close()
    conexion.close()

    # Crear el PDF en memoria
    buffer = BytesIO()
    documento = SimpleDocTemplate(buffer, pagesize=letter,
                                  title="Reporte de Productos - TechStore")

    estilos = getSampleStyleSheet()
    elementos = []

    titulo = Paragraph("<b>TECHSTORE - Listado de Productos</b>", estilos["Title"])
    elementos.append(titulo)
    elementos.append(Paragraph("Reporte generado por: " + session["usuario"], estilos["Normal"]))
    elementos.append(Spacer(1, 0.5 * cm))

    # Encabezado de la tabla
    datos = [["Código", "Nombre", "Precio", "Categoría"]]
    for producto in productos:
        datos.append([producto[0], producto[1], f"$ {producto[2]:,.0f}", producto[3]])

    tabla = Table(datos, colWidths=[3 * cm, 7 * cm, 4 * cm, 4 * cm])
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a1d20")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 11),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f2f2f2")]),
        ("FONTSIZE", (0, 1), (-1, -1), 10),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    elementos.append(tabla)

    elementos.append(Spacer(1, 0.5 * cm))
    elementos.append(Paragraph(f"Total de productos: {len(productos)}", estilos["Normal"]))

    documento.build(elementos)

    buffer.seek(0)

    from flask import send_file
    return send_file(buffer, as_attachment=True,
                     download_name="reporte_productos.pdf", mimetype="application/pdf")

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