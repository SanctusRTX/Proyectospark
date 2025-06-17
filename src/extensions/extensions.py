from flask_mysqldb import MySQL

# Inicialización de extensiones
db = MySQL()

def init_extensions(app):
    """Inicializa todas las extensiones de Flask"""
    db.init_app(app)

def init_db():
    """Inicializa la base de datos si es necesario"""
    # Esta función puede ser usada para crear tablas o insertar datos iniciales
    # En este caso, la base de datos ya debe estar creada en PythonAnywhere
    pass
