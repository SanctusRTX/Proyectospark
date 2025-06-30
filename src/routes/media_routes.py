from flask import Blueprint, request, jsonify
from controllers.media_controller import MediaController
from utils.decorators import login_required, admin_required

# Crear el blueprint
media_bp = Blueprint('media', __name__)

@media_bp.route('/upload-media', methods=['POST'])
@login_required
@admin_required
def upload_media():
    """Maneja la carga de archivos multimedia (imágenes y videos)"""
    try:
        print("Solicitud de carga de archivo recibida")
        print(f"Archivos en la solicitud: {list(request.files.keys())}")
        print(f"Formulario en la solicitud: {list(request.form.keys())}")
        
        # Depuración adicional del entorno
        import os
        print(f"Directorio de trabajo actual: {os.getcwd()}")
        print(f"Ruta raíz de la aplicación: {current_app.root_path}")
        print(f"Carpeta de carga configurada: {current_app.config['UPLOAD_FOLDER']}")
        
        if 'file' not in request.files:
            # Intentar buscar el archivo con otro nombre
            if len(request.files) > 0:
                # Usar el primer archivo que encontremos
                file_key = list(request.files.keys())[0]
                file = request.files[file_key]
                print(f"Archivo encontrado con clave alternativa: {file_key}")
            else:
                print("No se encontró ningún archivo en la solicitud")
                return jsonify({'error': 'No se encontró el archivo'}), 400
        else:
            file = request.files['file']
        
        print(f"Nombre del archivo: {file.filename}")
        print(f"Tamaño del archivo: {len(file.read())} bytes")
        file.seek(0)  # Reiniciar el puntero del archivo después de leerlo
        
        success, error, file_url = MediaController.upload_media(file)
        
        if success:
            print(f"Archivo subido exitosamente: {file_url}")
            return jsonify({'location': file_url})
        else:
            print(f"Error al subir archivo: {error}")
            return jsonify({'error': error}), 400
    except Exception as ex:
        print(f"Error en upload_media: {str(ex)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(ex)}), 500
