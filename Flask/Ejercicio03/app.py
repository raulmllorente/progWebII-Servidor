from flask import Flask, render_template
from datetime import date
app = Flask(__name__)

@app.route("/")
def index():
        return render_template('index.html', curso='Programación Web II-Servidor', nombre='Raúl', fecha=date.today())