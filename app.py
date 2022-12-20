from flask import Flask, render_template, jsonify, request,session,redirect
# from flask_login import LoginManager
import json

app = Flask(__name__)

app.secret_key=b'_5#y2L"F4Q8z\n\xec]/'

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
                session["usuario"] = request.form["usuario"]
                return redirect("/log")
        else:
            return "El usuario y la contraseña no coinciden con ninguno de nuestros usuarios en la base de datos, por favor, vuelve a intentar"
    return render_template("ingresar.html")

@app.route("/nuevapeli", methods=["GET","POST"])
def formulario():
    if "usuario" not in session:
        return jsonify({"error": "Necesitas estar logueado para ver el contenido"}), 401
    else:
        diccAux = {}
        comentador = session["usuario"]
        nombreAux = request.form.get("pelicula")
        anioAux = request.form.get("anio")
        directorAux = request.form.get("director")
        generoAux = request.form.get("genero")
        sinopsisAux = request.form.get("sinopsis")
        imagenAux = request.form.get("imagen")
        coment = request.form.get("comentario")
        diccAux2 = [{comentador:coment}]
        if request.method == "POST":
            for peliculas in datos_peliculas:
                if request.form["pelicula"] == peliculas["nombre"]:
                    return "Esa pelicula ya existe en el sistema, por favor intente con otra pelicula"
            diccAux["nombre"] = nombreAux
            diccAux["anio"] = anioAux
            diccAux["director"] = directorAux
            diccAux["genero"] = generoAux
            diccAux["sinopsis"] = sinopsisAux
            diccAux["imagen"] = imagenAux
            if request.form.get("comentario") != "":
                diccAux["comentarios"] = diccAux2
            else:
                diccAux["comentarios"] = [{}]
            datos_peliculas.append(diccAux)
            return "Su pelicula ha sido agregada con exito! ya se puede ver en nuestro sistema, para corroborarlo busque http://127.0.0.1:5000/peliculas/" + nombreAux + "."
    return render_template("formulario.html")

@app.route("/registro", methods=["GET","POST"])
def registro():
    diccAux = {}
    nombreAux = request.form.get("name")
    passAux = request.form.get("contrasenia")
    if request.method == "POST":
        for nombres in datos_user:
            if request.form["name"] == nombres["nombre"]:
                return "Ese nombre de usuario ya existe en nuestro registro, por favor, intente con otro!"
        diccAux["nombre"] = nombreAux
        diccAux["password"] = passAux
        datos_user.append(diccAux)
        return "Su usuario se ha registrado con exito! por favor ve a la pantalla de logeo y entre con su nueva cuenta. El link: http://127.0.0.1:5000/login"
    return render_template("registro.html")

@app.route("/borrarpeli", methods=["GET","POST"])
def borrarPeli():
    if "usuario" not in session:
        return jsonify({"error": "Necesitas estar logueado para ver el contenido"}), 401
    else:
        if request.method == "POST":
            for pelicula in (datos_peliculas):
                if pelicula["nombre"] == request.form["peli"] and pelicula["comentarios"] == [{}]:
                    datos_peliculas.remove(pelicula)
    return render_template("borrar.html"), 200

@app.route("/eliminarpeli", methods=["GET","DELETE"]) #METODO para postman para eliminar una pelicula ( para usar el metodo DELETE en vez de post por html )
def eliminarPeli(pelicula):
    if "usuario" not in session:
        return jsonify({"error": "Necesitas estar logueado para ver el contenido"}), 401
    else:
        listaAux = []
        nombre = pelicula
        if request.method == "DELETE":
            for pelicula in (datos_peliculas):
                for nombre in datos_peliculas:
                    listaAux.append(nombre[0])
                if pelicula["nombre"] == request.form["peli"] and pelicula["comentarios"] == [{}]:
                    datos_peliculas.remove(pelicula)
                    return "Tu pelicula ha sido removida con exito!", 200
                if nombre not in listaAux:
                    return "No existe una pelicula con ese nombre!", 401
                if pelicula["comentarios"] != [{}]:
                    return "No seas pillin, esa pelicula tiene comentarios", 401
    return ""

@app.route("/comentar", methods=["GET","POST"])
def comentarPeli():
    if "usuario" not in session:
        return jsonify({"error": "Necesitas estar logueado para ver el contenido"}), 401
    else:
        if request.method == "POST":
            comentador = session["usuario"]
            coment = request.form.get("comentario")
            listaAux = []
            diccAux = {comentador:coment}
            numAux = 0
            for pelicula in (datos_peliculas):
                if pelicula["nombre"] == request.form["nombre"]:
                    auxiliar = datos_peliculas[numAux]["comentarios"]
                    for comentario in auxiliar:
                        listaAux.append(comentario)
                    if comentador not in listaAux:
                        datos_peliculas[numAux]["comentarios"].update(diccAux)
                        listaAux = []
                        return f"Tu comentario se ha agregado correctamente!", 200
                    if comentador in listaAux:
                        listaAux = []
                        return f"Ya habias comentado esa pelicula, por favor, intenta con otra", 200
                numAux += 1
            return f"Esa pelicula no esta en el sistema, por favor chequea de vuelta!"
    return render_template("comentar.html"), 200

@app.route("/10pelis", methods=["GET"])
def ultimasPelis():
    numAux = len(datos_peliculas)
    numAux2 = numAux - 10
    listaAux = []
    for pelicula in datos_peliculas[numAux2:numAux]:
        listaAux.append(pelicula)
    return jsonify(listaAux), 200

@app.route("/modificarpeli", methods=["GET","POST"])
def modificarPeli():
    if "usuario" not in session:
        return jsonify({"error": "Necesitas estar logueado para ver el contenido"}), 401
    else:
        numAux = 0
        coment = request.form.get("comentario")
        nombreAux = request.form.get("pelicula")
        anioAux = request.form.get("anio")
        directorAux = request.form.get("director")
        generoAux = request.form.get("genero")
        sinopsisAux = request.form.get("sinopsis")
        imagenAux = request.form.get("imagen")
        if request.method == "POST":
            for peliculas in datos_peliculas:
                if nombreAux == datos_peliculas[numAux]["nombre"]:
                    if anioAux != "":
                        datos_peliculas[numAux]["anio"] = anioAux
                    if directorAux != "":
                        datos_peliculas[numAux]["director"] = directorAux
                    if generoAux != "":
                        datos_peliculas[numAux]["genero"] = generoAux
                    if sinopsisAux != "":
                        datos_peliculas[numAux]["sinopsis"] = sinopsisAux
                    if imagenAux != "":
                        datos_peliculas[numAux]["imagen"] = imagenAux
                    return "La pelicula se ha modificado correctamente!", 200
                numAux += 1
            return "Esa pelicula no existe en nuestro sistema!", 401
    return render_template("Modificar.html")
                    
@app.route("/modificarpelipostman", methods=["GET","POST","PUT"]) # METODO PUT PARA MODIFICAR LA PELI PARA USAR EN POSTMAN MANDANDO UN JSON
def eliminarPeli():
    if "usuario" not in session:
        jsonify({"error": "Necesitas estar logueado para ver el contenido"}), 401
    else:
        numAux = 0
        jsoneando = request.get_json()
        nombreAux = jsoneando["nombre"]
        anioAux = jsoneando["anio"]
        directorAux = jsoneando["director"]
        generoAux = jsoneando["genero"]
        sinopsisAux = jsoneando["sinopsis"]
        imagenAux = jsoneando["imagen"]
        if request.method == "PUT":
             for peliculas in datos_peliculas:
                if nombreAux == datos_peliculas[numAux]["nombre"]:
                    if anioAux != "":
                        datos_peliculas[anioAux]["anio"] = anioAux
                    if directorAux != "":
                        datos_peliculas[directorAux]["director"] = directorAux
                    if generoAux != "":
                        datos_peliculas[generoAux]["genero"] = generoAux
                    if sinopsisAux != "":
                        datos_peliculas[sinopsisAux]["sinopsis"] = sinopsisAux
                    if imagenAux != "":
                        datos_peliculas[imagenAux]["imagen"] = imagenAux
                    return jsonify({"error":"La pelicula se ha modificado correctamente!"}), 200
                numAux += 1
                return "Esa pelicula no existe en nuestro sistema!", 401

    

@app.route("/log")
def pagUsuario():
    if "usuario" not in session:
        jsonify({"error": "Necesitas estar logueado para ver el contenido"}), 401
    else:
        return render_template("logueado.html")

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

@app.route("/peliculas")
def devolverPeliculas():
    return jsonify(datos_peliculas)

@app.route("/peliculas/<nombre>")
def devolverPeli(nombre):
    if "username" not in session:
        return jsonify({"error": "Necesitas estar logueado para ver el contenido"}), 401
    else:
        peliAux = nombre
        for pelicula in datos_peliculas:
            if pelicula["nombre"] == peliAux:
                return jsonify(pelicula)
        return jsonify(pelicula) , 200

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