from flask_mysqldb import MySQL

# Inicialización de extensiones
db = MySQL()

def init_extensions(app):
    """Inicializa todas las extensiones de Flask"""
    db.init_app(app)
