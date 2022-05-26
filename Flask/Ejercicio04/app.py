from flask import Flask, render_template, request
from datetime import date
app = Flask(__name__)

@app.route("/")
def index():
        nombre = request.args.get('nombre')
        apellido = request.args.get('apellido')
        return render_template('index.html', nombre=nombre, apellido=apellido)

@app.route("/gato")
def gato():
        return render_template('gato.html')