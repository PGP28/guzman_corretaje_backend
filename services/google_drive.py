from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.service_account import Credentials
from config import Config

def initialize_drive_api():
    # Crea las credenciales desde el diccionario cargado
    creds = Credentials.from_service_account_info(Config.GOOGLE_DRIVE_CREDENTIALS)
    return build('drive', 'v3', credentials=creds)

def get_image_urls_from_folder(folder_id):
    try:
        service = initialize_drive_api()
        query = f"'{folder_id}' in parents and mimeType contains 'image/' and trashed = false"
        results = service.files().list(q=query, fields="files(id, name)").execute()
        return [{"name": f['name'], "url": f"https://drive.google.com/uc?id={f['id']}"} for f in results.get('files', [])]
    except HttpError as e:
        print(f"Error HTTP al obtener imágenes: {e}")
        raise
