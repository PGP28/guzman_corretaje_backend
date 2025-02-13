from flask import Blueprint, jsonify
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

folder_routes = Blueprint('folder_routes', __name__)
CREDENTIALS_FILE = 'instance/corretaje-guzman.json'

def conectar_google_drive():
    SCOPES = ['https://www.googleapis.com/auth/drive']
    creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
    return build('drive', 'v3', credentials=creds)

@folder_routes.route('/folders/sync', methods=['POST'])
def sync_folders():
    from app import db
    from models.models import Categoria

    drive_service = conectar_google_drive()
    carpetas = ['casas', 'departamentos', 'terrenos', 'Arriendo de Departamentos', 'Arriendo de Casas', 'Venta de Casas', 'Venta de Terrenos' ]
    resultados = {}

    for nombre_carpeta in carpetas:
        query = f"name='{nombre_carpeta}' and mimeType='application/vnd.google-apps.folder'"
        response = drive_service.files().list(q=query, fields="files(id, name)").execute()
        carpetas_encontradas = response.get('files', [])

        if not carpetas_encontradas:
            resultados[nombre_carpeta] = 'No encontrada'
        else:
            folder_id = carpetas_encontradas[0]['id']
            resultados[nombre_carpeta] = folder_id

            categoria = Categoria.query.filter_by(nombre=nombre_carpeta).first()
            if categoria:
                categoria.folder_id = folder_id
            else:
                nueva_categoria = Categoria(nombre=nombre_carpeta, folder_id=folder_id)
                db.session.add(nueva_categoria)

    db.session.commit()
    return jsonify({"message": "Folders sincronizados", "data": resultados})
