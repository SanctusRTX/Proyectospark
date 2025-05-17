
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_from_directory
import os
import time
from werkzeug.utils import secure_filename
from config import config

# Importar extensiones
from extensions.extensions import init_extensions, db

# Importar blueprints
from routes.auth_routes import auth_bp
from routes.main_routes import main_bp
from routes.admin_routes import admin_bp
from routes.course_routes import course_bp
from routes.media_routes import media_bp

# Definir constantes
UPLOAD_FOLDER = os.path.join('static', 'img', 'courses')
VIDEO_FOLDER = os.path.join('static', 'videos', 'courses')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'svg', 'mp4', 'webm', 'ogg'}

def create_app(config_name='development'):
    """Crea y configura la aplicación Flask"""
    app = Flask(__name__)
    
    # Configuración de la aplicación
    app.config.from_object(config[config_name])
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['VIDEO_FOLDER'] = VIDEO_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB
    
    # Asegurarse de que las carpetas existan
    os.makedirs(os.path.join(app.root_path, UPLOAD_FOLDER), exist_ok=True)
    os.makedirs(os.path.join(app.root_path, VIDEO_FOLDER), exist_ok=True)
    
    # Inicializar extensiones
    init_extensions(app)
    
    # Registrar blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(course_bp)
    app.register_blueprint(media_bp)
    
    # Manejadores de errores
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500
    
    return app

# Función para inicializar la base de datos
def init_db():
    try:
        # Verificar la conexión a la base de datos
        cursor = db.connection.cursor()
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        print(f"Tablas existentes: {tables}")
        print("Base de datos inicializada correctamente")
    except Exception as ex:
        print(f"Error al inicializar la base de datos: {ex}")

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        init_db()
    app.run(debug=True)
