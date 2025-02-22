from flask import Blueprint, jsonify, redirect

home_routes = Blueprint('home_routes', __name__)

@home_routes.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Bienvenido a la API de Guzmán Corretaje"})

# Ruta para redirigir favicon.ico a un ícono externo
@home_routes.route('/favicon.ico')
def favicon():
    return redirect("https://www.google.com/favicon.ico", code=302)

from sqlalchemy import text

@home_routes.route('/db-check', methods=['GET'])
def db_check():
    try:
        from app import db
        db.session.execute(text('USE cco93507_corretaje_db;'))  # Envuelve la consulta con text()
        return jsonify({"message": "Conexión exitosa a la base de datos"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

