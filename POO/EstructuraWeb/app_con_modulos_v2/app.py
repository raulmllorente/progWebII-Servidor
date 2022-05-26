from flask import Flask, render_template


#from paquete.codigo import objeto
#from carperta.codigopython import objeto
from module001.module001 import module001
from module002.module002 import module002
from module003.module003 import module003

app = Flask(__name__)

# EJERCICIO - CREAR OTROS 2 MODULOS module002 y module003 - VOLVEMOS A LAS
# 12:00.
app.register_blueprint(module001, url_prefix="/module001")
app.register_blueprint(module002, url_prefix="/module002")
app.register_blueprint(module003, url_prefix="/module003")


@app.route('/')
def index():
    return render_template('index.html')

