from flask import Blueprint, jsonify
from models.models import Region, Ciudad, Comuna

ubicaciones_routes = Blueprint('ubicaciones_routes', __name__)

@ubicaciones_routes.route('/', methods=['GET'])
def get_ubicaciones():
    regiones = Region.query.all()
    resultado = {}

    for region in regiones:
        resultado[region.nombre] = {
            ciudad.nombre: [comuna.nombre for comuna in ciudad.comunas]
            for ciudad in region.ciudades
        }

    return jsonify(resultado)
