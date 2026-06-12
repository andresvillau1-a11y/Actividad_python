from flask import flask 

app = Flask(__name__)

@app.route('/contacto')
def contacto():
    return 'Información de contacto'
@app.route('/usuario/<nombre>')
def usuario(nombre):
    return f'Hola, {nombre}! Bienvenido a nuestro sitio web'

app.run(debug=True)