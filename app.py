from flask import Flask, render_template, jsonify, request
# from flask_login import LoginManager
import json

app = Flask(__name__)

# login_manager = LoginManager(app)

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

@app.route("/login", methods=["POST", "GET"])
def login():
    #Recordad que request.form "password" toma un string, y el json tiene que estar en formato string
    if request.method == "POST":
        for usuarios in (datos_user):
            if usuarios["nombre"] == request.form["usuario"] and usuarios["password"] == request.form["password"]:
                return render_template("main.html")
        
    return render_template("ingresar.html")

@app.route("/formulario")
def formulario():
    return render_template("formulario.html")


@app.route("/directores")
def devolverDirectores():
    listaAux = ["directores que tenemos en la plataforma actualmente : "]
    numAux = 0
    for directores in datos_peliculas:
        aux = datos_peliculas[numAux]["director"]
        if aux not in listaAux:
            listaAux.append(aux)
        numAux += 1
    return listaAux, 200

@app.route("/director/<director>")
def devolverPeliDeDirector(director):
    listaAux = []
    directorAux = director
    for director in datos_peliculas:
        if director["director"] == directorAux:
            if director not in listaAux:
                listaAux.append(director)
    return jsonify({f"peliculas dirigidas por este director": listaAux}), 200

@app.route("/peliculas/<nombre>")
def devolverPeli(nombre):
    # if "username" not in session:
    #     return jsonify({"error": "Necesitas estar logueado para ver el contenido"}), 401
    # else:      LO DEJO COMENTADO POR QUE ES PARA CUANDO HAGAN EL SISTEMA DE LOGIN, SI LO DEJO NORMAL TE TIRA ERROR
        peliAux = nombre
        for pelicula in datos_peliculas:
            if pelicula["nombre"] == peliAux:
                return jsonify(pelicula)
        return jsonify(pelicula)

@app.route("/generos")
def devolverGeneros():
    listaAux = ["generos que tenemos en la plataforma actualmente : "]
    numAux = 0
    for generos in datos_peliculas:
        aux = datos_peliculas[numAux]["genero"]
        if aux not in listaAux:
            listaAux.append(aux)
        numAux += 1
    return listaAux, 200

@app.route("/pelisconimagenes")
def devolverPelis():
    listaAux = []
    numAux = 0
    for peliculas in datos_peliculas:
        aux = datos_peliculas[numAux]
        if datos_peliculas[numAux]["imagen"] != "":
            if aux not in listaAux:
                listaAux.append(aux)
                numAux += 1
        else:
            numAux += 1
            continue
    return jsonify({f"peliculas que tienen imagenes agregadas son": listaAux}), 200

if __name__ =="__main__":
    app.run(debug=True)