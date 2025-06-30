from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_from_directory
import os
import time
import secrets
from datetime import timedelta
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
from routes.gemini_routes import gemini_bp

# Nota: Para herramientas de diagnóstico, utilizar:
# from utils.check_exams import check_exams
# from utils.debug_exams import debug_exams

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
    
    # Configuración de sesión para mejorar la seguridad
    # Para sesiones normales: 1 hora (controlado por middleware). 
    # Para sesiones con "Recuérdame" activado: 30 días
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)
    app.config['SESSION_COOKIE_HTTPONLY'] = True  # Evitar acceso a cookies por JavaScript
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Protección contra CSRF
    
    # Asegurarse de que la clave secreta sea única en cada inicio de la aplicación
    app.secret_key = secrets.token_hex(32)
    
    # Asegurarse de que las carpetas existan
    os.makedirs(os.path.join(app.root_path, UPLOAD_FOLDER), exist_ok=True)
    os.makedirs(os.path.join(app.root_path, VIDEO_FOLDER), exist_ok=True)
    
    # Imprimir rutas de carpetas para depuración
    print(f"Ruta de carpeta de imágenes: {os.path.join(app.root_path, UPLOAD_FOLDER)}")
    print(f"Ruta de carpeta de videos: {os.path.join(app.root_path, VIDEO_FOLDER)}")
    
    # Definir rutas absolutas para carpetas estáticas
    STATIC_FOLDER = os.path.join(app.root_path, 'static')
    UPLOAD_FOLDER_FULL = os.path.join(STATIC_FOLDER, 'img', 'courses')
    VIDEO_FOLDER_FULL = os.path.join(STATIC_FOLDER, 'videos', 'courses')
    
    # Configuraciones de la aplicación
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER_FULL
    app.config['VIDEO_FOLDER'] = VIDEO_FOLDER_FULL
    app.config['STATIC_FOLDER'] = STATIC_FOLDER
    
    # Asegurarse de que las carpetas existan
    os.makedirs(UPLOAD_FOLDER_FULL, exist_ok=True)
    os.makedirs(VIDEO_FOLDER_FULL, exist_ok=True)
    
    # Imprimir rutas de carpetas para depuración
    print(f"Ruta de carpeta estática: {STATIC_FOLDER}")
    print(f"Ruta de carpeta de imágenes: {UPLOAD_FOLDER_FULL}")
    print(f"Ruta de carpeta de videos: {VIDEO_FOLDER_FULL}")
    
    # Configurar la ruta de archivos estáticos
    app.static_folder = STATIC_FOLDER
    
    # Inicializar extensiones
    init_extensions(app)
    
    # Registrar blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(course_bp)
    app.register_blueprint(media_bp)
    app.register_blueprint(gemini_bp)
    
    # Middleware para verificar la validez de la sesión en cada solicitud
    @app.before_request
    def validate_session():
        # Ignorar rutas estáticas y de autenticación para evitar redirecciones infinitas
        if request.endpoint and (request.endpoint.startswith('static') or 
                                request.endpoint == 'auth.login' or 
                                request.endpoint == 'auth.logout'):
            return
            
        # Verificar si hay una sesión iniciada
        if 'user_id' in session:
            # Verificar si la sesión tiene una marca de tiempo
            if 'timestamp' not in session:
                # Si no tiene marca de tiempo, es una sesión antigua o inválida, limpiarla
                session.clear()
                flash('Tu sesión ha caducado. Por favor, inicia sesión nuevamente.', 'warning')
                return redirect(url_for('auth.login'))
                
            # Si session.permanent es True (remember me), extender la sesión
            # Si no, verificar si ha expirado (1 hora = 3600 segundos)
            current_time = int(time.time())
            if not session.get('permanent', False):
                session_age = current_time - session['timestamp']
                if session_age > 3600:
                    session.clear()
                    flash('Tu sesión ha expirado por inactividad. Por favor, inicia sesión nuevamente.', 'warning')
                    return redirect(url_for('auth.login'))
                
            # Actualizar la marca de tiempo para extender la sesión
            session['timestamp'] = current_time
    
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
