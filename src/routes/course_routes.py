from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from controllers.course_controller import CourseController
from controllers.chapter_controller import ChapterController
from controllers.exam_controller import ExamController
from utils.decorators import login_required

# Crear el blueprint
course_bp = Blueprint('course', __name__, url_prefix='/course')

@course_bp.route('/<int:course_id>')
@login_required
def view_course(course_id):
    course = CourseController.get_course_by_id(course_id)
    if not course:
        flash('Curso no encontrado', 'danger')
        return redirect(url_for('main.home'))
    
    chapters = ChapterController.get_chapters_by_course(course_id)
    return render_template('course/view.html', course=course, chapters=chapters)

@course_bp.route('/<int:course_id>/chapter/<int:chapter_id>')
@login_required
def view_chapter(course_id, chapter_id):
    # Logs de depuración detallados
    print(f"DEBUG: Solicitando capítulo {chapter_id} para el curso {course_id}")
    
    course = CourseController.get_course_by_id(course_id)
    if not course:
        print(f"DEBUG: Curso {course_id} no encontrado")
        flash('Curso no encontrado', 'danger')
        return redirect(url_for('main.home'))
    
    # Obtener el capítulo actual
    chapter = ChapterController.get_chapter_by_id(chapter_id)
    if not chapter or chapter[3] != course_id:
        print(f"DEBUG: Capítulo {chapter_id} no encontrado o no pertenece al curso")
        flash('Capítulo no encontrado', 'danger')
        return redirect(url_for('course.view_course', course_id=course_id))
    
    # Obtener capítulos anterior y siguiente
    from extensions.extensions import db
    next_chapter = ChapterController.get_next_chapter(db, course_id, chapter_id)
    prev_chapter = ChapterController.get_previous_chapter(db, course_id, chapter_id)
    
    # Obtener todos los capítulos del curso para la navegación
    chapters = ChapterController.get_chapters_by_course(course_id)
    
    # Logs de depuración
    print(f"DEBUG: Capítulo actual: {chapter}")
    print(f"DEBUG: Capítulo siguiente: {next_chapter}")
    print(f"DEBUG: Capítulo anterior: {prev_chapter}")
    
    return render_template('course/chapter.html', 
                           course=course, 
                           chapter=chapter, 
                           chapters=chapters,
                           next_chapter=next_chapter,
                           prev_chapter=prev_chapter)

@course_bp.route('/<int:course_id>/chapter/<int:chapter_id>/exams')
@login_required
def chapter_examenes(course_id, chapter_id):
    """Muestra los exámenes disponibles para un capítulo"""
    try:
        # Obtener información del curso y capítulo
        course = CourseController.get_course_by_id(course_id)
        chapter = ChapterController.get_chapter_by_id(chapter_id)
        
        if not course or not chapter:
            flash('Curso o capítulo no encontrado', 'danger')
            return redirect(url_for('main.home'))
        
        # Obtener exámenes del capítulo
        try:
            examenes = ExamController.get_exams_by_chapter(chapter_id)
            print(f"DEBUG - Exámenes encontrados para capítulo {chapter_id}: {len(examenes) if examenes else 0}")
        except Exception as ex:
            print(f"DEBUG - Error al obtener exámenes: {str(ex)}")
            examenes = []
        
        # Obtener capítulos del curso para el menú lateral
        chapters = ChapterController.get_chapters_by_course(course_id)
        
        # Siempre mostrar la plantilla, incluso si no hay exámenes
        print(f"DEBUG - Renderizando plantilla de exámenes para curso {course_id}, capítulo {chapter_id}")
        return render_template('course/exams/index.html', 
                              course=course, 
                              chapter=chapter, 
                              chapters=chapters,
                              examenes=examenes)
                              
    except Exception as ex:
        print(f"DEBUG - Error general en chapter_examenes: {str(ex)}")
        flash(f'Error al cargar exámenes: {str(ex)}', 'danger')
        return redirect(url_for('course.view_chapter', course_id=course_id, chapter_id=chapter_id))

@course_bp.route('/<int:course_id>/chapter/<int:chapter_id>/exam/<int:examen_id>', methods=['GET', 'POST'])
@login_required
def take_examen(course_id, chapter_id, examen_id):
    """Permite a un estudiante realizar un examen"""
    try:
        # Obtener información del curso, capítulo y examen
        course = CourseController.get_course_by_id(course_id)
        chapter = ChapterController.get_chapter_by_id(chapter_id)
        examen = ExamController.get_exam_by_id(examen_id)
        
        if not course or not chapter or not examen:
            flash('Curso, capítulo o examen no encontrado', 'danger')
            return redirect(url_for('main.home'))
        
        # Obtener capítulos del curso para el menú lateral
        chapters = ChapterController.get_chapters_by_course(course_id)
        
        # Obtener preguntas del examen con sus opciones
        preguntas_con_opciones = ExamController.get_questions_with_options(examen_id)
        
        if request.method == 'POST':
            # Procesar las respuestas del examen
            respuestas = {}
            for key, value in request.form.items():
                if key.startswith('pregunta_'):
                    pregunta_id = int(key.split('_')[1])
                    respuestas[pregunta_id] = int(value)
            
            # Guardar las respuestas y calcular resultado
            usuario_id = session.get('user_id', 0)
            success, resultado_id = ExamController.submit_exam(examen_id, usuario_id, respuestas)
            
            if success:
                flash('Examen completado correctamente', 'success')
                return redirect(url_for('course.view_resultado', course_id=course_id, chapter_id=chapter_id, resultado_id=resultado_id))
            else:
                flash(f'Error al procesar el examen: {resultado_id}', 'danger')
                return redirect(url_for('course.chapter_examenes', course_id=course_id, chapter_id=chapter_id))
        
        try:
            return render_template('course/exams/take.html', 
                                course=course, 
                                chapter=chapter, 
                                chapters=chapters,
                                examen=examen, 
                                preguntas=preguntas_con_opciones)
        except Exception as template_ex:
            # Capturar específicamente errores de plantilla
            flash(f'Error en la plantilla del examen: {str(template_ex)}', 'danger')
            return redirect(url_for('course.chapter_examenes', course_id=course_id, chapter_id=chapter_id))
    except Exception as ex:
        flash(f'Error al cargar examen: {str(ex)}', 'danger')
        return redirect(url_for('course.chapter_examenes', course_id=course_id, chapter_id=chapter_id))

@course_bp.route('/<int:course_id>/chapter/<int:chapter_id>/resultado/<int:resultado_id>')
@login_required
def view_resultado(course_id, chapter_id, resultado_id):
    """Muestra el resultado de un examen completado"""
    try:
        # Obtener información del curso y capítulo
        course = CourseController.get_course_by_id(course_id)
        chapter = ChapterController.get_chapter_by_id(chapter_id)
        
        if not course or not chapter:
            flash('Curso o capítulo no encontrado', 'danger')
            return redirect(url_for('main.home'))
        
        # Obtener capítulos del curso para el menú lateral
        chapters = ChapterController.get_chapters_by_course(course_id)
        
        # Obtener resultado del examen
        resultado = ExamController.get_result_by_id(resultado_id)
        
        if not resultado:
            flash('Resultado no encontrado', 'danger')
            return redirect(url_for('course.chapter_examenes', course_id=course_id, chapter_id=chapter_id))
        
        try:
            return render_template('course/exams/result.html', 
                                course=course, 
                                chapter=chapter, 
                                chapters=chapters,
                                resultado=resultado)
        except Exception as template_ex:
            # Capturar específicamente errores de plantilla
            flash(f'Error en la plantilla de resultados: {str(template_ex)}', 'danger')
            return redirect(url_for('course.view_chapter', course_id=course_id, chapter_id=chapter_id))
    except Exception as ex:
        flash(f'Error al cargar resultado: {str(ex)}', 'danger')
        return redirect(url_for('course.view_chapter', course_id=course_id, chapter_id=chapter_id))

@course_bp.route('/mis-resultados')
@login_required
def mis_resultados():
    """Muestra todos los resultados de exámenes del usuario actual"""
    try:
        usuario_id = session.get('user_id', 0)
        resultados = ExamController.get_results_by_user(usuario_id)
        
        return render_template('user/resultados.html', resultados=resultados)
    except Exception as ex:
        flash(f'Error al cargar resultados: {str(ex)}', 'danger')
        return redirect(url_for('main.home'))
