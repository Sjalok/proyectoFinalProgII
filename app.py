from flask import Flask, render_template, jsonify
from flask_login import LoginManager
import json

app = Flask(__name__)

login_manager = LoginManager(app)

#tratamiento de json
with open("users.json", encoding='utf-8') as usuarios:
    datos_user = json.load(usuarios)

with open("data.json", encoding='utf-8') as dataPelis:
    datos_peliculas = json.load(dataPelis)

#enrrutamientos de la app
    #desde aca empiesan los enrutamientos

@app.route("/")
def index():
    return render_template("main.html")

@app.route("/login")
def login():

    return render_template("ingresar.html")

if __name__ =="__main__":
    app.run(debug=True)