from flask import Blueprint, jsonify, redirect
from sqlalchemy import text
from datetime import datetime
from app import db  # ✅ Importación global para evitar overhead

home_routes = Blueprint('home_routes', __name__)

@home_routes.route('/server-time', methods=['GET'])
def server_time():
    now = datetime.now()
    return jsonify({"server_time": now.strftime("%Y-%m-%d %H:%M:%S")})

@home_routes.route('/', methods=['GET'])
def home():
    """Ruta principal que da la bienvenida a la API."""
    return jsonify({"message": "Bienvenido a la API de Guzmán Corretaje"})

@home_routes.route('/favicon.ico')
def favicon():
    """Redirige a un ícono externo para el favicon."""
    return redirect("https://www.google.com/favicon.ico", code=302)

@home_routes.route('/db-check', methods=['GET'])
def db_check():
    """Verifica la conexión con la base de datos."""
    try:
        db.session.execute(text('SELECT 1'))  # ✅ Verificación de la conexión
        return jsonify({"message": "Conexión exitosa a la base de datos"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.session.close()  # ✅ Cierra la sesión para evitar conexiones abiertas
