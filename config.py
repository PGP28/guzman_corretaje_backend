import os
import json

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URI",
        "mysql+pymysql://cco93507_api:6102.,pgp@srv25.cpanelhost.cl/cco93507_corretaje_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuración del pool de conexión (keep-alive)
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,           # Verifica si la conexión está viva
        "pool_recycle": 280,             # Recicla conexiones cada 280 segundos
        "pool_timeout": 30,              # Tiempo de espera para obtener una conexión
        "pool_size": 10,                 # Número máximo de conexiones en el pool
        "max_overflow": 5,               # Conexiones extra cuando el pool está lleno
        "connect_args": {
            "keepalives": 1,             # Activa el TCP Keep-Alive
            "keepalives_idle": 60,       # Tiempo antes de enviar keep-alives
            "keepalives_interval": 30,   # Intervalo entre keep-alives
            "keepalives_count": 5        # Intentos antes de cerrar la conexión
        }
    }

    # Detectar entorno
    ENV = os.getenv("FLASK_ENV", "development")

    if ENV == "production":
        # Producción: credenciales desde variables de entorno
        GOOGLE_DRIVE_CREDENTIALS = json.loads(os.getenv("GOOGLE_DRIVE_CREDENTIALS"))
    else:
        # Local: credenciales desde archivo
        with open("./instance/corretaje-guzman.json") as f:
            GOOGLE_DRIVE_CREDENTIALS = json.load(f)import os
import json

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URI",
        "mysql+pymysql://cco93507_api:6102.,pgp@srv25.cpanelhost.cl/cco93507_corretaje_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuración de conexión y pool (sin connect_args para pymysql)
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,    # Verifica si la conexión está activa
        "pool_recycle": 280,      # Recicla conexiones antes de que se cierren
        "pool_timeout": 30,       # Tiempo de espera para obtener una conexión
        "pool_size": 10,          # Máximo número de conexiones en el pool
        "max_overflow": 5         # Conexiones extra permitidas
    }

    # Detectar entorno
    ENV = os.getenv("FLASK_ENV", "development")

    if ENV == "production":
        # Producción: credenciales desde variables de entorno
        GOOGLE_DRIVE_CREDENTIALS = json.loads(os.getenv("GOOGLE_DRIVE_CREDENTIALS"))
    else:
        # Local: credenciales desde archivo
        with open("./instance/corretaje-guzman.json") as f:
            GOOGLE_DRIVE_CREDENTIALS = json.load(f)

