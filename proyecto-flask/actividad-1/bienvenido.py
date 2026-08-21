from flask import Flask 

app = Flask(__name__)

@app.route('/')
def inicio():
    return 'bienvenido al sistema'

@app.route('/saludo')
def saludo():
    return "hola aprendiz ADSO"

@app.route('/inventario')
def inventario():
    return "sistema de inventario"

@app.route('/usuario')
def usuario():
    return "sistema usuario activo"

app.run(debug=True)