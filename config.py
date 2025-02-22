import os
import json

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URI",
        "mysql+pymysql://cco93507_api:6102.,pgp@srv25.cpanelhost.cl/cco93507_corretaje_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ✅ Opciones para mejorar el manejo de conexiones
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,    # Verifica conexiones antes de usarlas (evita conexiones rotas)
        "pool_size": 5,           # Número máximo de conexiones en el pool
        "max_overflow": 10,       # Conexiones adicionales si se llena el pool
        "pool_timeout": 10        # Tiempo máximo de espera para obtener una conexión
    }

    # Detectar entorno
    ENV = os.getenv("FLASK_ENV", "development")

    if ENV == "production":
        # En producción (Vercel) cargamos desde la variable de entorno
        GOOGLE_DRIVE_CREDENTIALS = json.loads(os.getenv("GOOGLE_DRIVE_CREDENTIALS"))
    else:
        # En local cargamos desde el archivo
        with open("./instance/corretaje-guzman.json") as f:
            GOOGLE_DRIVE_CREDENTIALS = json.load(f)
