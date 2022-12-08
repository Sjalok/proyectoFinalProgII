from flask import Flask, render_template
import json
#instancimiento de flas
    #variable app es un objeto nuevo de tipo flask
app = Flask(__name__)

#tratamiento de json
with open("users.json") as data1:
    datos_user = json.load(data1)

with open("data.json") as data2:
    datos_peliculas = json.load(data2)

#enrrutamientos de la app
    #desde aca empiesan los enrutamientos
@app.route("/")
def index():
    return render_template("main.html", data=datos_peliculas)

@app.route("/login")
def login():
    return render_template("ngresar.html")

#si el nombre del objeto flask es el main, ejecutalo.
if __name__ =="__main__":
    app.run(debug=True)
#no poner nada despues de esto, sino no se muestra.