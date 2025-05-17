from flask import current_app
from utils.helpers import allowed_file, save_file

class MediaController:
    @staticmethod
    def upload_media(file):
        """Maneja la carga de archivos multimedia (imágenes y videos)"""
        try:
            if not file or file.filename == '':
                return False, "No se seleccionó ningún archivo", None
            
            if not allowed_file(file.filename):
                return False, "Tipo de archivo no permitido", None
            
            file_url = save_file(file, current_app.config['UPLOAD_FOLDER'], current_app)
            
            if file_url:
                return True, None, file_url
            else:
                return False, "Error al guardar el archivo", None
        except Exception as ex:
            return False, str(ex), None
