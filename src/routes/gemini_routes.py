from flask import Blueprint, request, jsonify, session, render_template, flash, redirect, url_for
from controllers.gemini_controller import GeminiController
from controllers.course_controller import CourseController
from controllers.chapter_controller import ChapterController
from utils.decorators import login_required
import os

# Configurar la clave API de Sparky
GEMINI_API_KEY = "AIzaSyChhjSyqtCr8BVM6MEY10YEmIVvqpuzqT0"

# Crear el blueprint para las rutas de Sparky
gemini_bp = Blueprint('gemini', __name__, url_prefix='/gemini')

@gemini_bp.route('/<int:course_id>/<int:chapter_id>', methods=['GET'])
@login_required
def gemini_chat(course_id, chapter_id):
    """Endpoint para mostrar la interfaz de chat con Sparky"""
    try:
        # Obtener información del curso
        course = CourseController.get_course_by_id(course_id)
        
        if not course:
            return jsonify({
                'success': False,
                'error': 'Curso no encontrado'
            }), 404
        
        # Obtener información del capítulo
        chapter = ChapterController.get_chapter_by_id(chapter_id)
        
        if not chapter:
            return jsonify({
                'success': False,
                'error': 'Capítulo no encontrado'
            }), 404
        
        # Obtener todos los capítulos del curso para la navegación
        chapters = ChapterController.get_chapters_by_course(course_id)
        
        # Verificar si hay un prompt inicial en la URL
        initial_prompt = request.args.get('prompt')
        
        # Renderizar la plantilla con los datos
        return render_template('gemini/gemini_chat.html', 
                               course=course, 
                               chapter=chapter, 
                               chapters=chapters,
                               initial_prompt=initial_prompt,
                               course_id=course_id,
                               chapter_id=chapter_id)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@gemini_bp.route('/generate', methods=['POST'])
@login_required
def generate_content():
    """Endpoint para generar contenido con Sparky"""
    try:
        # Obtener datos de la solicitud
        data = request.json
        prompt = data.get('prompt')
        course_id = data.get('course_id')
        chapter_id = data.get('chapter_id')
        
        if not prompt:
            return jsonify({
                'success': False,
                'error': 'No se proporcionó un prompt'
            }), 400
        
        # Generar contenido con Sparky usando el ID del curso y capítulo
        result = GeminiController.generate_content(prompt, GEMINI_API_KEY, course_id, chapter_id)
        
        # Devolver la respuesta
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@gemini_bp.route('/images', methods=['GET'])
@login_required
def gemini_images():
    """Endpoint para la interfaz de generación de imágenes con Sparky"""
    try:
        # Obtener el ID del curso y capítulo si se proporcionan en la URL
        course_id = request.args.get('course_id', type=int)
        chapter_id = request.args.get('chapter_id', type=int)
        
        # Obtener información del curso si se proporciona un ID
        course = None
        if course_id:
            course = CourseController.get_course_by_id(course_id)
        
        # Obtener información del capítulo si se proporciona un ID
        chapter = None
        if chapter_id:
            chapter = ChapterController.get_chapter_by_id(chapter_id)
        
        # Renderizar la plantilla de generación de imágenes
        return render_template('gemini/sparky_images.html',
                              course=course,
                              chapter=chapter,
                              api_key=GEMINI_API_KEY)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@gemini_bp.route('/generate-image', methods=['POST'])
@login_required
def generate_image():
    """Endpoint para generar imágenes con Sparky"""
    try:
        # Implementación básica para manejar la solicitud
        return jsonify({
            'success': True,
            'message': 'Funcionalidad de generación de imágenes en desarrollo'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@gemini_bp.route('/activities/<int:course_id>', methods=['GET'])
@login_required
def get_activities(course_id):
    """Obtiene actividades predefinidas para un curso específico"""
    try:
        # Obtener información del curso
        course = CourseController.get_course_by_id(course_id)
        
        if not course:
            return jsonify({
                'success': False,
                'error': 'Curso no encontrado'
            }), 404
        
        # Obtener el ID del capítulo si se proporciona en la URL
        chapter_id = request.args.get('chapter_id', type=int)
        
        # Obtener actividades del controlador de Gemini
        activities = GeminiController.get_activities(course_id, chapter_id)
        
        return jsonify({
            'success': True,
            'activities': activities
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@gemini_bp.route('/context/<int:course_id>', methods=['GET'])
@login_required
def get_course_context(course_id):
    """Obtiene el contexto para un curso específico"""
    try:
        # Obtener información del curso
        course = CourseController.get_course_by_id(course_id)
        
        if not course:
            return jsonify({
                'success': False,
                'error': 'Curso no encontrado'
            }), 404
        
        # Obtener el ID del capítulo si se proporciona en la URL
        chapter_id = request.args.get('chapter_id', type=int)
        
        # Obtener el contexto del curso
        course_context = GeminiController.get_course_context(course_id)
        
        # Obtener el contexto del capítulo si se proporciona un ID de capítulo
        chapter_context = None
        if chapter_id:
            chapter_context = GeminiController.get_chapter_context(course_id, chapter_id)
        
        return jsonify({
            'success': True,
            'course_context': course_context,
            'chapter_context': chapter_context
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500 