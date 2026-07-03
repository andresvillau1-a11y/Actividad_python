from flask import Flask, render_template, request, redirect, url_for, flash
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
    return render_template("index1.html",productos=productos)

@app.route("/productos")
def productos():
    #Llamar conexión
    conexion = obtener_conexion()
    #Crear mensajero que enviara y recibira las consultas - Hace que el resultado de la consulta se guarde en un diccionario, no una lista.
    cursor = conexion.cursor(dictionary=True)
    #Grabar consulta en el mensajero
    cursor.execute("SELECT * FROM productos")
    #Guardar todos los resultados de la consulta en una variable/lista/diccionario
    productos = cursor.fetchall()
    longitud = len(productos)
    #Cerrar cursor y conexión
    cursor.close()
    conexion.close()
    return render_template("productos.html",productos=productos,longitud=longitud)

@app.route("/catalogo")
def catalogo():
    return render_template("catalogo.html")

@app.route("/contacto")
def contacto():
    return render_template("contacto.html")

@app.route("/nosotros")
def nosotros():
    return render_template("nosotros.html")

@app.route("/servicios")
def servicios():
    return render_template("servicios.html")

@app.route("/registro_producto")
def registro_producto():
    return render_template("registro_producto.html")

@app.route("/guardar_producto", methods=["POST"])
def guardar_producto():
    codigo = request.form["codigo"]
    nombre = request.form["nombre"]
    precio = request.form["precio"]
    categoria = request.form["categoria"]

    #return render_template(
    #    "respuesta.html",
    #    codigo=codigo,
    #    nombre=nombre,
    #    precio=precio,
    #    categoria=categoria
    #)

    conexion = obtener_conexion()
    cursor = conexion.cursor()
    #Definir sentencia con marcadores anonimos
    sql = """ INSERT INTO productos VALUES (%s,%s,%s,%s) """
    #Ejecutamos la consulta de manera indirecta, primero la estructura base y llenamos cada una de las incognitas.
    cursor.execute(
    sql,
        (
            codigo,
            nombre,
            precio,
            categoria
        )
    )
    #Guardan los cambios realizados por la consulta
    conexion.commit()
    #Mensaje de exito:
    flash ("Producto registrado exitosamente", "success")
    cursor.close()
    conexion.close()

    #Regreso a la tabla
    return redirect(url_for("productos"))

@app.route("/editar_producto/<codigo>")
def editar_producto(codigo):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    sql = """ SELECT * FROM productos WHERE codigo = %s ;"""
    cursor.execute(sql,(codigo,))
    producto = cursor.fetchone()
    cursor.close()
    conexion.close()
    return render_template("editar_producto.html",producto=producto)

@app.route("/actualizar_producto",methods=["POST"])
def actualizar_producto():
    codigo = request.form["codigo"]
    nombre = request.form["nombre"]
    precio = request.form["precio"]
    categoria = request.form["categoria"]

    if len(nombre.strip()) == 0 or len(categoria.strip()) == 0:
        flash("Error: Todos los campos son obligatorios.", "error")
        return redirect(url_for("editar_producto", codigo=codigo))
    
    if len(precio.strip()) == 0 or not precio.replace('.', '', 1).isdigit() or float(precio) < 0:
        flash("Error: El precio debe ser un número válido mayor o igual a cero.", "error")
        return redirect(url_for("editar_producto", codigo=codigo))

    conexion = obtener_conexion()
    cursor = conexion.cursor()
    sql = """ UPDATE productos SET nombre = %s, precio = %s, categoria = %s WHERE codigo = %s """
    cursor.execute(
        sql,
        (
            nombre,
            precio,
            categoria,
            codigo
        )
    )
    conexion.commit() 
    flash ("Producto actualizado exitosamente", "success")
    cursor.close()
    conexion.close()
    return redirect(url_for("productos"))

@app.route("/eliminar_producto/<codigo>")
def eliminar_producto(codigo):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    sql = "DELETE FROM productos WHERE codigo = %s"
    cursor.execute(sql,(codigo,))
    conexion.commit()
    producto = cursor.fetchone()
    flash ("Producto eliminado correctamente", "success")
    cursor.close()
    conexion.close
    return redirect(url_for("productos"))

app.run(debug=True)