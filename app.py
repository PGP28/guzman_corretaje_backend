import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_cors import CORS

# --------------------------------------------
# 📝 Configuración básica de logs
# --------------------------------------------
log_level = os.getenv("LOG_LEVEL", "INFO").upper()  # Puedes cambiar "INFO" a "DEBUG" si quieres más detalle

logging.basicConfig(
    level=log_level,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# --------------------------------------------
# 💾 Rotación de logs (evita archivos enormes)
# --------------------------------------------
if not os.path.exists('logs'):
    os.makedirs('logs')

file_handler = RotatingFileHandler('logs/app.log', maxBytes=1_000_000, backupCount=3)
file_handler.setLevel(log_level)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# Añadir el manejador de archivo al logger raíz
logging.getLogger().addHandler(file_handler)

# --------------------------------------------
# 🌎 Logs en consola para Render
# --------------------------------------------
console_handler = logging.StreamHandler()
console_handler.setLevel(log_level)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logging.getLogger().addHandler(console_handler)


# Inicializar Flask y extensiones
app = Flask(__name__)
# Habilitar CORS para todas las rutas
CORS(app)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Importar y registrar Blueprints
from routes.properties import property_routes
from routes.folders import folder_routes
from routes.home import home_routes
from routes.ubicaciones import ubicaciones_routes

app.register_blueprint(property_routes, url_prefix='/api')
app.register_blueprint(folder_routes, url_prefix='/api')
app.register_blueprint(ubicaciones_routes, url_prefix='/api')
app.register_blueprint(home_routes)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
