import os
import json

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URI",
        "mysql+pymysql://cco93507_api:6102.,pgp@srv25.cpanelhost.cl/cco93507_corretaje_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Detectar entorno
    ENV = os.getenv("FLASK_ENV", "development")

    if ENV == "production":
        # En producción (Vercel) cargamos desde la variable de entorno
        GOOGLE_DRIVE_CREDENTIALS = json.loads(os.getenv("GOOGLE_DRIVE_CREDENTIALS"))
    else:
        # En local cargamos desde el archivo
        with open("./instance/corretaje-guzman.json") as f:
            GOOGLE_DRIVE_CREDENTIALS = json.load(f)
