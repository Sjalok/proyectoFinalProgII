from flask import Flask, render_template
import json
#instancimiento de flas
    #variable app es un objeto nuevo de tipo flask
app = Flask(__name__)

#tratamiento de json
def obtener_usuarios():
    with open("users.json") as data:
        datos_user = json.load(data)
    return datos_user

#enrrutamientos de la app
    #desde aca empiesan los enrutamientos
@app.route("/")
def index():
    return render_template("/plantilla.html")


#si el nombre del objeto flask es el main, ejecutalo.
if __name__ =="__main__":
    app.run(debug=True)
#no poner nada despues de esto, sino no se muestra.