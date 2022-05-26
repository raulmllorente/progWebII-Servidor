from flask import Flask, render_template
from datetime import date
app = Flask(__name__)

@app.route("/")
def index():
        return'''
        <!DOCTYPE html>
        
        <html>
        
        <body>
        
        <h1> Programación Web II-Servidor </h1>
        
        <p> Raúl </p>
        
        <p> 2022-02-08 </p> </body>
        
        </html>
'''