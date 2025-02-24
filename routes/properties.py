import os
import uuid
from flask import Blueprint, request, jsonify
from models.models import Propiedad, DetallePropiedad, ImagenPropiedad, Categoria
from app import db
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from googleapiclient.http import MediaFileUpload

property_routes = Blueprint('property_routes', __name__)

# Configuración de Google Drive
CREDENTIALS_FILE = "instance/corretaje-guzman.json"

# Mapeo de categorías a carpetas de Google Drive
CARPETAS_DRIVE = {
    "Arriendo de Casas": "1OHUEbq6hnh3coxAj9KjH9naQYRDn8xkq",
    "Arriendo de Departamentos": "13cvFzpWwwBU0cJkW6oIP4GR7E0mSwECz",
    "Venta de Casas": "1ky7EWCIQEBowe7DL7iJlFigmkYKSemYD",
    "Venta de Terrenos": "1OnL4fsGL8GNSBiVVD3p1bZUMxjEXbwrv",
    "casas": "1SnLk0UFEzyfyGz2zo4-FoY7BG8cq5Wlq",
    "departamentos": "1cmvFF4tpnk3ho4Imlv7LWvRzFFZlxNNR",
    "terrenos": "1riwA0QagCXFweGXxOXUOUllWeLqiEJ0Y"
}

# Mapeo de IDs para `categoria_id`
CATEGORIA_ID_MAP = {
    "Arriendo de Departamentos": 2,
    "Arriendo de Casas": 1,
    "Venta de Casas": 1,
    "Venta de Terrenos": 3
}

# Carpeta donde se almacenarán temporalmente los archivos
UPLOAD_FOLDER = "/tmp/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def conectar_google_drive():
    SCOPES = ["https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
    return build("drive", "v3", credentials=creds)

def subir_imagen_a_drive(file, categoria):
    drive_service = conectar_google_drive()
    
    folder_id = CARPETAS_DRIVE.get(categoria)
    if not folder_id:
        print(f"❌ Error: No se encontró carpeta en Drive para la categoría '{categoria}'")
        return None  

    unique_filename = f"{uuid.uuid4().hex}_{file.filename}"
    temp_path = os.path.join(UPLOAD_FOLDER, unique_filename)

    try:
        file.save(temp_path)

        media = MediaFileUpload(temp_path, mimetype=file.mimetype)
        file_metadata = {"name": file.filename, "parents": [folder_id]}
        file_drive = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields="id"
        ).execute()

        file_id = file_drive.get("id")
        url_publica = f"https://drive.google.com/uc?id={file_id}"

        return url_publica

    except Exception as e:
        print(f"❌ Error al subir la imagen a Drive: {e}")
        return None

@property_routes.route('/properties', methods=['GET'])
def get_properties():
    categoria_id = request.args.get('categoria_id', type=int)
    propiedades = Propiedad.query.filter_by(categoria_id=categoria_id).all() if categoria_id else Propiedad.query.all()

    return jsonify([
        {
            "id": p.id,
            "nombre": p.nombre,
            "ubicacion": p.ubicacion,
            "precio": p.precio,
            "unidad_medida": p.unidad_medida,
            "region": p.region,
            "comuna": p.comuna,
            "categoria": p.categoria,
            "categoria_id": p.categoria_id,
            "fecha_entrega": p.fecha_entrega,
            "constructora": p.constructora,
            "detalles": {
                "dormitorios": p.detalles.dormitorios if p.detalles else None,
                "banos": p.detalles.banos if p.detalles else None,
                "metros_cuadrados": p.detalles.metros_cuadrados if p.detalles else None,
                "gastos_comunes": p.detalles.gastos_comunes if p.detalles else None,
                "estacionamientos": p.detalles.estacionamientos if p.detalles else None,
                "bodega": p.detalles.bodega if p.detalles else None,
                "descripcion": p.detalles.descripcion if p.detalles else None,
                "superficie_util": p.detalles.superficie_util if p.detalles else None,
                "superficie_total": p.detalles.superficie_total if p.detalles else None
            },
            "imagenes": [i.url for i in p.imagenes]
        } for p in propiedades
    ])

@property_routes.route('/properties/create', methods=['POST'])
def create_property():
    try:
        imagenes = request.files.getlist("imagenes")

        if not imagenes or all(imagen.filename == "" for imagen in imagenes):
            return jsonify({"error": "Debe subir al menos una imagen."}), 400

        nombre = request.form.get("nombre")
        ubicacion = request.form.get("ubicacion")
        precio = request.form.get("precio")
        unidad_medida = request.form.get("unidad_medida")
        categoria_nombre = request.form.get("categoria")
        region = request.form.get("region")
        ciudad = request.form.get("ciudad")  # ✅ Corrección
        comuna = request.form.get("comuna")
        fecha_entrega = request.form.get("fecha_entrega")
        constructora = request.form.get("constructora")

        # 📌 Validar y obtener `categoria_id`
        categoria_id = CATEGORIA_ID_MAP.get(categoria_nombre, None)
        if not categoria_id:
            return jsonify({"error": "Categoría inválida."}), 400

        # 📌 Verificar si la categoría ya existe en la BD, si no, agregarla
        categoria = Categoria.query.filter_by(nombre=categoria_nombre).first()
        if not categoria:
            categoria = Categoria(nombre=categoria_nombre, folder_id=CARPETAS_DRIVE.get(categoria_nombre))
            db.session.add(categoria)
            db.session.commit()

        # 📌 Crear la propiedad con `categoria` y `categoria_id`
        propiedad = Propiedad(
            nombre=nombre,
            ubicacion=ubicacion,
            precio=precio,
            unidad_medida=unidad_medida,
            categoria=categoria_nombre,
            categoria_id=categoria_id,
            region=region,
            ciudad=ciudad,
            comuna=comuna,
            fecha_entrega=fecha_entrega,
            constructora=constructora
        )
        db.session.add(propiedad)
        db.session.commit()

        # 📌 Asegurar que se registre en la tabla `detalles_propiedades`
        detalles = DetallePropiedad(
            propiedad_id=propiedad.id,
            dormitorios=request.form.get("dormitorios", type=int, default=0),
            banos=request.form.get("banos", type=int, default=0),
            metros_cuadrados=request.form.get("metros_cuadrados", type=float, default=0.0),
            gastos_comunes=request.form.get("gastos_comunes", default="0"),
            estacionamientos=request.form.get("estacionamientos", type=int, default=0),
            bodega=request.form.get("bodega", type=int, default=0),
            descripcion=request.form.get("descripcion", default="Sin descripción"),
            superficie_util=request.form.get("superficie_util", type=float, default=0.0),
            superficie_total=request.form.get("superficie_total", type=float, default=0.0)
        )
        db.session.add(detalles)
        db.session.commit()

        # 📌 Subir imágenes a Google Drive y guardar URLs en la BD
        imagenes_urls = []
        for imagen in imagenes:
            if imagen.filename:
                url_imagen = subir_imagen_a_drive(imagen, categoria_nombre)
                if url_imagen:
                    imagenes_urls.append(url_imagen)
                    imagen_bd = ImagenPropiedad(propiedad_id=propiedad.id, url=url_imagen)
                    db.session.add(imagen_bd)

        db.session.commit()

        return jsonify({
            "message": "Propiedad creada exitosamente",
            "propiedad_id": propiedad.id,
            "imagenes": imagenes_urls
        }), 201

    except Exception as e:
        print(f"❌ Error al subir la imagen a Drive: {e}")
        return jsonify({"error": f"Error al subir imagen: {str(e)}"}), 500

