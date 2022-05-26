from flask import Flask, render_template


#from paquete.codigo import objeto
#from carperta.codigopython import objeto
from module001.module001 import module001

app = Flask(__name__)
app.register_blueprint(module001, url_prefix="/login")


@app.route('/')
def index():
    return render_template('index.html')

