from flask import current_app, jsonify
import os
from werkzeug.utils import secure_filename
from utils.helpers import allowed_file, save_file

class MediaController:
    @staticmethod
    def upload_media(file):
        """Maneja la carga de archivos multimedia (imágenes y videos)"""
        try:
            # Validaciones iniciales
            if not file or file.filename == '':
                return False, "No se seleccionó ningún archivo", None
            
            # Verificar tamaño del archivo
            file.seek(0, os.SEEK_END)
            file_size = file.tell()
            file.seek(0)
            
            # Límite de 16 MB
            max_file_size = 16 * 1024 * 1024  # 16 MB
            if file_size > max_file_size:
                return False, f"El archivo es demasiado grande. Máximo {max_file_size / (1024 * 1024)} MB", None
            
            # Verificar extensión del archivo
            if not allowed_file(file.filename):
                return False, "Tipo de archivo no permitido", None
            
            # Generar nombre de archivo seguro
            filename = secure_filename(file.filename)
            
            # Determinar carpeta de destino según el tipo de archivo
            if filename.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'svg', 'webp')):
                folder = current_app.config['UPLOAD_FOLDER']
                relative_path = f'img/courses/{filename}'
            elif filename.lower().endswith(('mp4', 'webm', 'ogg')):
                folder = current_app.config['VIDEO_FOLDER']
                relative_path = f'videos/courses/{filename}'
            else:
                return False, "Tipo de archivo no soportado", None
            
            # Crear carpeta si no existe
            os.makedirs(folder, exist_ok=True)
            
            # Ruta completa del archivo
            full_path = os.path.join(folder, filename)
            
            # Verificar si ya existe un archivo con el mismo nombre
            counter = 1
            base_filename, ext = os.path.splitext(filename)
            while os.path.exists(full_path):
                filename = f"{base_filename}_{counter}{ext}"
                full_path = os.path.join(folder, filename)
                relative_path = relative_path.replace(base_filename + ext, filename)
                counter += 1
            
            try:
                # Guardar archivo
                file.save(full_path)
                
                # Verificar que el archivo se haya guardado
                if not os.path.exists(full_path):
                    return False, f"No se pudo guardar el archivo {filename}", None
                
                # Generar URL para el archivo
                file_url = f'/static/{relative_path}'
                
                return True, "Archivo subido exitosamente", file_url
            
            except Exception as save_error:
                print(f"Error al guardar el archivo: {save_error}")
                return False, f"Error al guardar el archivo: {save_error}", None
        
        except Exception as e:
            # Registro de errores
            print(f"Error al procesar la carga de archivo: {str(e)}")
            return False, f"Error al procesar la carga de archivo: {str(e)}", None
