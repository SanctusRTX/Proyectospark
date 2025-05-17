import os
from werkzeug.utils import secure_filename
import time

def allowed_file(filename, allowed_extensions=None):
    """Verifica si un archivo tiene una extensión permitida"""
    if allowed_extensions is None:
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'svg', 'mp4', 'webm', 'ogg'}
    
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def save_file(file, folder, app):
    """Guarda un archivo en la carpeta especificada y devuelve la URL"""
    if file and file.filename:
        filename = secure_filename(file.filename)
        # Generar nombre único para evitar colisiones
        unique_filename = f"{int(time.time())}_{filename}"
        
        # Determinar si es imagen o video por la extensión
        ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        
        if ext in {'mp4', 'webm', 'ogg'}:
            filepath = os.path.join(app.root_path, app.config['VIDEO_FOLDER'], unique_filename)
            file.save(filepath)
            file_url = f'videos/courses/{unique_filename}'
        else:
            filepath = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(filepath)
            file_url = f'img/courses/{unique_filename}'
        
        return file_url
    
    return None
