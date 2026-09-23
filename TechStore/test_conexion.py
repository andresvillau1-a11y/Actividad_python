"""Script de prueba: verifica la conexion a MySQL usando config.py"""
import mysql.connector
from config import *

try:
    conexion = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )
    cursor = conexion.cursor()
    cursor.execute("SELECT COUNT(*) FROM productos")
    total_productos = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    total_usuarios = cursor.fetchone()[0]
    cursor.close()
    conexion.close()
    print(f"CONEXION EXITOSA a '{MYSQL_DATABASE}' en {MYSQL_HOST}")
    print(f"Productos: {total_productos} | Usuarios: {total_usuarios}")
except mysql.connector.Error as e:
    print(f"ERROR DE CONEXION: {e}")
