import os
import json

# ✅ Manejo de credenciales desde variables de entorno
credentials_content = os.getenv("GOOGLE_DRIVE_CREDENTIALS_CONTENT")
if credentials_content:
    os.makedirs("instance", exist_ok=True)  # Crear carpeta si no existe
    with open("instance/corretaje-guzman.json", "w") as f:
        json.dump(json.loads(credentials_content), f)

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URI",
        "mysql+pymysql://cco93507_api:6102.,pgp@srv25.cpanelhost.cl/cco93507_corretaje_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GOOGLE_DRIVE_CREDENTIALS = "./instance/corretaje-guzman.json"
