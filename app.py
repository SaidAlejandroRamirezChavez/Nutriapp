from flask import  Flask, render_template
import tkinter as tk

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("Registro.html")

@app.route("/inicio")
def inicio():
    return render_template("inicio.html")  


if __name__ == "__main__":
    app.run(debug = True)
