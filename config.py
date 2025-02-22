import os
import json

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URI",
        "mysql+pymysql://cco93507_api:6102.,pgp@srv25.cpanelhost.cl/cco93507_corretaje_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuración de conexión y pool
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 280,
        "pool_timeout": 30,
        "pool_size": 10,
        "max_overflow": 5
    }

    # Detectar entorno
    ENV = os.getenv("FLASK_ENV", "development")

    if ENV == "production":
        # Producción: credenciales desde variable de entorno
        GOOGLE_DRIVE_CREDENTIALS = json.loads(os.getenv("GOOGLE_DRIVE_CREDENTIALS"))
    else:
        # Local: credenciales desde archivo
        with open("./instance/corretaje-guzman.json") as f:
            GOOGLE_DRIVE_CREDENTIALS = json.load(f)  # ✅ Línea corregida
