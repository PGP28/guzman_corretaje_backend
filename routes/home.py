from flask import Blueprint, jsonify, redirect

home_routes = Blueprint('home_routes', __name__)

@home_routes.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Bienvenido a la API de Guzmán Corretaje"})

# Ruta para redirigir favicon.ico a un ícono externo
@home_routes.route('/favicon.ico')
def favicon():
    return redirect("https://www.google.com/favicon.ico", code=302)