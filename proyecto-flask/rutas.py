from flask import flask 

app = Flask(__name__)

@app.route('/')
def inicio():
    return 'Hola, Mundo!'

@app.route('/productos')
def productos():
    return 'Aquí puedes ver nuestros productos'

app.run(debug=True)