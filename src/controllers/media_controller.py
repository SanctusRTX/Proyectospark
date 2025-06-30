from flask import current_app
import os
from utils.helpers import allowed_file, save_file

class MediaController:
    @staticmethod
    def upload_media(file):
        """Maneja la carga de archivos multimedia (imágenes y videos)"""
        try:
            if not file or file.filename == '':
                print("Error: No se seleccionó ningún archivo")
                return False, "No se seleccionó ningún archivo", None
            
            # Verificar extensión del archivo
            if not allowed_file(file.filename):
                print(f"Error: Tipo de archivo no permitido - {file.filename}")
                return False, "Tipo de archivo no permitido", None
            
            # Depuración adicional
            print(f"Archivo recibido: {file.filename}")
            print(f"Ruta de carga configurada: {current_app.config['UPLOAD_FOLDER']}")
            print(f"Ruta raíz de la aplicación: {current_app.root_path}")
            
            # Intentar guardar el archivo
            file_url = save_file(file, current_app.config['UPLOAD_FOLDER'], current_app)
            
            if file_url:
                print(f"Archivo guardado exitosamente. URL: {file_url}")
                return True, None, file_url
            else:
                print("Error: No se pudo guardar el archivo")
                return False, "Error al guardar el archivo", None
        except Exception as ex:
            print(f"Excepción en upload_media: {ex}")
            import traceback
            traceback.print_exc()
            return False, str(ex), None
