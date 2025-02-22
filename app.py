import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_cors import CORS

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

logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
