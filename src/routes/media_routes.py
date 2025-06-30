from flask import Blueprint, request, jsonify
from controllers.media_controller import MediaController
from utils.decorators import login_required, admin_required
import os

# Crear el blueprint
media_bp = Blueprint('media', __name__)

@media_bp.route('/upload-media', methods=['POST'])
@login_required
@admin_required
def upload_media():
    """Maneja la carga de archivos multimedia (imágenes y videos)"""
    try:
        # Verificar límite de tamaño de archivo
        if request.content_length and request.content_length > 16 * 1024 * 1024:  # 16 MB
            print(f"Error: Archivo demasiado grande. Tamaño recibido: {request.content_length} bytes")
            return jsonify({
                'error': 'El archivo es demasiado grande. Máximo 16 MB.',
                'max_size': 16 * 1024 * 1024,
                'received_size': request.content_length
            }), 413  # Payload Too Large
        
        # Depuración de archivos recibidos
        print("Solicitud de carga de archivo recibida")
        print(f"Archivos en la solicitud: {list(request.files.keys())}")
        print(f"Formulario en la solicitud: {list(request.form.keys())}")
        
        # Identificar el archivo
        if 'file' not in request.files:
            # Intentar buscar el archivo con otro nombre
            if len(request.files) > 0:
                file_key = list(request.files.keys())[0]
                file = request.files[file_key]
                print(f"Archivo encontrado con clave alternativa: {file_key}")
            else:
                print("No se encontró ningún archivo en la solicitud")
                return jsonify({'error': 'No se encontró el archivo'}), 400
        else:
            file = request.files['file']
        
        # Información adicional del archivo
        print(f"Nombre del archivo: {file.filename}")
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        print(f"Tamaño del archivo: {file_size} bytes")
        
        # Límite de tamaño de archivo
        max_file_size = 16 * 1024 * 1024  # 16 MB
        if file_size > max_file_size:
            print(f"Error: Archivo demasiado grande. Máximo {max_file_size} bytes")
            return jsonify({
                'error': f'El archivo es demasiado grande. Máximo {max_file_size / (1024 * 1024)} MB',
                'max_size': max_file_size,
                'received_size': file_size
            }), 413  # Payload Too Large
        
        # Procesar la carga del archivo
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
