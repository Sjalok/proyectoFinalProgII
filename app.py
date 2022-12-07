from flask import Flask

#variable app es un objeto nuevo de tipo flask
app = Flask(__name__)
 
#desde aca empiesan los enrutamientos
@app.route("/")
def index():
    return "Bienvenidos al servicio de recomendacion de peliculas!"

#si el nombre del objeto flask es el main, ejecutalo.
if __name__ =="__main__":
    app.run(debug=True)
     
