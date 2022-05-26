from flask import Flask, render_template, request
from datetime import date
import calendar
app = Flask(__name__)

@app.route("/")
def index():
        nombre = request.args.get('nombre')
        apellido = request.args.get('apellido')
        return render_template('index.html', nombre=nombre, apellido=apellido)

@app.route("/gato")
def gato():
        return render_template('gato.html')

@app.route("/calendario")
def calendario():
        calendario = calendar.HTMLCalendar(firstweekday = 0)
        anio = request.args.get('anio')
        mes = request.args.get('mes')

        if anio == None and mes == None:
                mes, anio = date.today().month, date.today().year
        return render_template('calendario.html',calendario = calendario.formatmonth(int(anio), int(mes)))