from app import db

class Categoria(db.Model):
    __tablename__ = 'categorias'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)
    folder_id = db.Column(db.String(255), nullable=False)
    
    propiedades = db.relationship('Propiedad', back_populates='categoria_relacion', lazy=True)

    def __repr__(self):
        return f'<Categoria {self.nombre}>'

class Propiedad(db.Model):
    __tablename__ = 'propiedades'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    ubicacion = db.Column(db.String(255), nullable=False)
    precio = db.Column(db.String(50), nullable=False)
    unidad_medida = db.Column(db.String(5), nullable=False, default='CLP')
    categoria = db.Column(db.String(100), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    region = db.Column(db.String(100), nullable=False)
    ciudad = db.Column(db.String(100), nullable=False)
    comuna = db.Column(db.String(100), nullable=False)
    fecha_entrega = db.Column(db.Date, nullable=True)  # ⚠️ Nuevo campo
    constructora = db.Column(db.String(255), nullable=True)  # ⚠️ Nuevo campo

    detalles = db.relationship('DetallePropiedad', backref='propiedad', uselist=False, cascade="all, delete")
    imagenes = db.relationship('ImagenPropiedad', backref='propiedad', lazy=True, cascade="all, delete")

    categoria_relacion = db.relationship('Categoria', back_populates='propiedades')

    def __repr__(self):
        return f'<Propiedad {self.nombre}, {self.ubicacion}, {self.ciudad}, {self.comuna}, {self.unidad_medida}>'

class DetallePropiedad(db.Model):
    __tablename__ = 'detalles_propiedades'

    id = db.Column(db.Integer, primary_key=True)
    dormitorios = db.Column(db.Integer, nullable=False)
    banos = db.Column(db.Integer, nullable=False)
    metros_cuadrados = db.Column(db.Float, nullable=False)
    gastos_comunes = db.Column(db.String(50), nullable=False)
    estacionamientos = db.Column(db.Integer, nullable=False, default=0)
    bodega = db.Column(db.Integer, nullable=False, default=0)
    descripcion = db.Column(db.Text, nullable=False)
    superficie_util = db.Column(db.Float, nullable=True)  # ⚠️ Nuevo campo
    superficie_total = db.Column(db.Float, nullable=True)  # ⚠️ Nuevo campo
    propiedad_id = db.Column(db.Integer, db.ForeignKey('propiedades.id'), nullable=False)

    def __repr__(self):
        return f'<DetallePropiedad {self.dormitorios} dorm, {self.banos} baños>'

class ImagenPropiedad(db.Model):
    __tablename__ = 'imagenes_propiedades'

    id = db.Column(db.Integer, primary_key=True)
    propiedad_id = db.Column(db.Integer, db.ForeignKey('propiedades.id'), nullable=False)
    url = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<ImagenPropiedad {self.id} id, {self.propiedad_id} propiedad_id, {self.url}> url'
    
class Region(db.Model):
    __tablename__ = 'regiones'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    ciudades = db.relationship('Ciudad', backref='region', lazy=True)

class Ciudad(db.Model):
    __tablename__ = 'ciudades'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    region_id = db.Column(db.Integer, db.ForeignKey('regiones.id'), nullable=False)
    comunas = db.relationship('Comuna', backref='ciudad', lazy=True)

class Comuna(db.Model):
    __tablename__ = 'comunas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    ciudad_id = db.Column(db.Integer, db.ForeignKey('ciudades.id'), nullable=False)    
