import os
from werkzeug.utils import secure_filename
import time
from flask import url_for

def allowed_file(filename, allowed_extensions=None):
    """Verifica si un archivo tiene una extensión permitida"""
    if allowed_extensions is None:
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'svg', 'mp4', 'webm', 'ogg'}
    
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def generate_unique_filename(filename):
    """Genera un nombre de archivo único manteniendo el nombre original"""
    if not filename:
        return None
    
    # Asegurarse de que el nombre del archivo sea seguro
    secure_name = secure_filename(filename)
    
    # Si el nombre seguro está vacío, generar un nombre aleatorio
    if not secure_name:
        secure_name = f"file_{int(time.time())}"
    
    return secure_name

def save_file(file, folder, app):
    """Guarda un archivo en la carpeta especificada y devuelve la URL"""
    if file and file.filename:
        # Usar el nombre de archivo original, asegurándolo
        filename = secure_filename(file.filename)
        
        # Determinar si es imagen o video por la extensión
        ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        
        # Rutas específicas para imágenes y videos
        if ext in {'mp4', 'webm', 'ogg'}:
            relative_path = f'videos/courses/{filename}'
            folder_path = os.path.join(app.root_path, 'static', 'videos', 'courses')
        else:
            relative_path = f'img/courses/{filename}'
            folder_path = os.path.join(app.root_path, 'static', 'img', 'courses')
        
        # Crear la carpeta si no existe
        os.makedirs(folder_path, exist_ok=True)
        
        # Ruta completa del archivo
        filepath = os.path.join(folder_path, filename)
        
        try:
            # Guardar el archivo
            file.save(filepath)
            
            # Verificar que el archivo se haya guardado
            if not os.path.exists(filepath):
                print(f"Error: No se pudo guardar el archivo {filepath}")
                return None
            
            # Generar URL usando la ruta relativa
            file_url = url_for('static', filename=relative_path)
            
            print(f"Archivo guardado exitosamente: {filepath}")
            print(f"URL generada: {file_url}")
            
            return relative_path  # Devolver la ruta relativa para guardar en la base de datos
        except Exception as e:
            print(f"Error al guardar el archivo: {e}")
            return None
    
    return None
