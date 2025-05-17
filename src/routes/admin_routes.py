from flask import Blueprint, render_template, request, redirect, url_for, flash
from controllers.course_controller import CourseController
from controllers.chapter_controller import ChapterController
from controllers.exam_controller import ExamController
from utils.decorators import login_required, admin_required

# Crear el blueprint
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Rutas para administración de cursos
@admin_bp.route('/courses')
@login_required
@admin_required
def admin_courses():
    courses = CourseController.get_all_courses(active_only=False)
    return render_template('admin/courses/index.html', courses=courses)

@admin_bp.route('/courses/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_course():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        external_url = request.form['external_url']
        active = 'active' in request.form
        image = request.files['image'] if 'image' in request.files else None
        
        success, error = CourseController.create_course(title, description, external_url, image, active)
        
        if success:
            flash('Curso creado exitosamente', 'success')
            return redirect(url_for('admin.admin_courses'))
        else:
            flash(f'Error al crear el curso: {error}', 'danger')
    
    return render_template('admin/courses/new.html')

@admin_bp.route('/courses/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_course(id):
    course = CourseController.get_course_by_id(id)
    
    if not course:
        flash('Curso no encontrado', 'danger')
        return redirect(url_for('admin.admin_courses'))
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        external_url = request.form['external_url']
        active = 'active' in request.form
        image = request.files['image'] if 'image' in request.files and request.files['image'].filename != '' else None
        
        success, error = CourseController.update_course(id, title, description, external_url, image, active)
        
        if success:
            flash('Curso actualizado exitosamente', 'success')
            return redirect(url_for('admin.admin_courses'))
        else:
            flash(f'Error al actualizar el curso: {error}', 'danger')
    
    return render_template('admin/courses/edit.html', course=course)

@admin_bp.route('/courses/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_course(id):
    success, error = CourseController.delete_course(id)
    
    if success:
        flash('Curso eliminado exitosamente', 'success')
    else:
        flash(f'Error al eliminar el curso: {error}', 'danger')
    
    return redirect(url_for('admin.admin_courses'))

@admin_bp.route('/fix-image-paths')
@login_required
@admin_required
def fix_image_paths():
    success, rows_affected = CourseController.fix_image_paths()
    
    if success:
        if rows_affected > 0:
            flash(f'Se corrigieron {rows_affected} rutas de imágenes correctamente', 'success')
        else:
            flash('No se encontraron rutas de imágenes que necesiten corrección', 'info')
    else:
        flash(f'Error al corregir rutas de imágenes: {rows_affected}', 'danger')
    
    return redirect(url_for('admin.admin_courses'))

# Rutas para administración de capítulos
@admin_bp.route('/courses/<int:course_id>/chapters')
@login_required
@admin_required
def admin_chapters(course_id):
    course = CourseController.get_course_by_id(course_id)
    if not course:
        flash('Curso no encontrado', 'danger')
        return redirect(url_for('admin.admin_courses'))
    
    chapters = ChapterController.get_chapters_by_course(course_id)
    return render_template('admin/chapters/index.html', course=course, chapters=chapters)

@admin_bp.route('/courses/<int:course_id>/chapters/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_chapter(course_id):
    course = CourseController.get_course_by_id(course_id)
    if not course:
        flash('Curso no encontrado', 'danger')
        return redirect(url_for('admin.admin_courses'))
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        success, error = ChapterController.create_chapter(title, content, course_id)
        
        if success:
            flash('Capítulo creado exitosamente', 'success')
            return redirect(url_for('admin.admin_chapters', course_id=course_id))
        else:
            flash(f'Error al crear el capítulo: {error}', 'danger')
    
    return render_template('admin/chapters/new.html', course=course)

@admin_bp.route('/courses/<int:course_id>/chapters/edit/<int:chapter_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_chapter(course_id, chapter_id):
    course = CourseController.get_course_by_id(course_id)
    if not course:
        flash('Curso no encontrado', 'danger')
        return redirect(url_for('admin.admin_courses'))
    
    chapter = ChapterController.get_chapter_by_id(chapter_id)
    if not chapter:
        flash('Capítulo no encontrado', 'danger')
        return redirect(url_for('admin.admin_chapters', course_id=course_id))
    
    # Verificar que el capítulo pertenezca al curso
    valid, error = ChapterController.validate_chapter_belongs_to_course(chapter, course_id)
    if not valid:
        flash(error, 'danger')
        return redirect(url_for('admin.admin_chapters', course_id=course_id))
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        success, error = ChapterController.update_chapter(chapter_id, title, content)
        
        if success:
            flash('Capítulo actualizado exitosamente', 'success')
            return redirect(url_for('admin.admin_chapters', course_id=course_id))
        else:
            flash(f'Error al actualizar el capítulo: {error}', 'danger')
    
    return render_template('admin/chapters/edit.html', course=course, chapter=chapter)

@admin_bp.route('/courses/<int:course_id>/chapters/delete/<int:chapter_id>', methods=['POST'])
@login_required
@admin_required
def delete_chapter(course_id, chapter_id):
    course = CourseController.get_course_by_id(course_id)
    if not course:
        flash('Curso no encontrado', 'danger')
        return redirect(url_for('admin.admin_courses'))
    
    chapter = ChapterController.get_chapter_by_id(chapter_id)
    if not chapter:
        flash('Capítulo no encontrado', 'danger')
        return redirect(url_for('admin.admin_chapters', course_id=course_id))
    
    # Verificar que el capítulo pertenezca al curso
    valid, error = ChapterController.validate_chapter_belongs_to_course(chapter, course_id)
    if not valid:
        flash(error, 'danger')
        return redirect(url_for('admin.admin_chapters', course_id=course_id))
    
    success, error = ChapterController.delete_chapter(chapter_id)
    
    if success:
        flash('Capítulo eliminado exitosamente', 'success')
    else:
        flash(f'Error al eliminar el capítulo: {error}', 'danger')
    
    return redirect(url_for('admin.admin_chapters', course_id=course_id))

# Rutas para administración de exámenes
@admin_bp.route('/courses/<int:course_id>/chapters/<int:chapter_id>/exams')
@login_required
@admin_required
def admin_examenes(course_id, chapter_id):
    """Muestra la lista de exámenes para un capítulo específico"""
    try:
        # Obtener información del curso y capítulo
        course = CourseController.get_course_by_id(course_id)
        chapter = ChapterController.get_chapter_by_id(chapter_id)
        
        if not course or not chapter:
            flash('Curso o capítulo no encontrado', 'danger')
            return redirect(url_for('admin.admin_courses'))
        
        # Obtener exámenes del capítulo
        examenes = ExamController.get_exams_by_chapter(chapter_id)
        
        try:
            return render_template('admin/exams/index.html', 
                                course=course, 
                                chapter=chapter, 
                                examenes=examenes)
        except Exception as template_ex:
            # Capturar específicamente errores de plantilla
            flash(f'Error en la plantilla: {str(template_ex)}', 'danger')
            return redirect(url_for('admin.admin_chapters', course_id=course_id))
    except Exception as ex:
        flash(f'Error al cargar exámenes: {str(ex)}', 'danger')
        return redirect(url_for('admin.admin_chapters', course_id=course_id))

@admin_bp.route('/courses/<int:course_id>/chapters/<int:chapter_id>/exams/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_examen(course_id, chapter_id):
    """Crea un nuevo examen para un capítulo"""
    try:
        # Obtener información del curso y capítulo
        course = CourseController.get_course_by_id(course_id)
        chapter = ChapterController.get_chapter_by_id(chapter_id)
        
        if not course or not chapter:
            flash('Curso o capítulo no encontrado', 'danger')
            return redirect(url_for('admin.admin_courses'))
        
        if request.method == 'POST':
            titulo = request.form['titulo']
            descripcion = request.form['descripcion']
            tiempo_limite = int(request.form['tiempo_limite']) if request.form['tiempo_limite'] else 0
            
            success, error_or_id = ExamController.create_exam(titulo, descripcion, tiempo_limite, chapter_id)
            
            if success:
                flash('Examen creado correctamente', 'success')
                return redirect(url_for('admin.edit_examen', course_id=course_id, chapter_id=chapter_id, examen_id=error_or_id))
            else:
                flash(f'Error al crear examen: {error_or_id}', 'danger')
        
        return render_template('admin/exams/new.html', course=course, chapter=chapter)
    except Exception as ex:
        flash(f'Error al crear examen: {str(ex)}', 'danger')
        return redirect(url_for('admin.admin_examenes', course_id=course_id, chapter_id=chapter_id))

@admin_bp.route('/courses/<int:course_id>/chapters/<int:chapter_id>/exams/<int:examen_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_examen(course_id, chapter_id, examen_id):
    """Edita un examen existente"""
    try:
        # Obtener información del curso, capítulo y examen
        course = CourseController.get_course_by_id(course_id)
        chapter = ChapterController.get_chapter_by_id(chapter_id)
        examen = ExamController.get_exam_by_id(examen_id)
        
        if not course or not chapter or not examen:
            flash('Curso, capítulo o examen no encontrado', 'danger')
            return redirect(url_for('admin.admin_courses'))
        
        # Obtener preguntas del examen
        preguntas = ExamController.get_questions_by_exam(examen_id)
        
        if request.method == 'POST':
            if 'update_examen' in request.form:
                # Actualizar información del examen
                titulo = request.form['titulo']
                descripcion = request.form['descripcion']
                tiempo_limite = int(request.form['tiempo_limite']) if request.form['tiempo_limite'] else 0
                
                success, error = ExamController.update_exam(examen_id, titulo, descripcion, tiempo_limite)
                
                if success:
                    flash('Examen actualizado correctamente', 'success')
                else:
                    flash(f'Error al actualizar examen: {error}', 'danger')
                
                return redirect(url_for('admin.edit_examen', course_id=course_id, chapter_id=chapter_id, examen_id=examen_id))
            
            elif 'add_pregunta' in request.form:
                # Agregar nueva pregunta
                texto = request.form['texto_pregunta']
                puntos = int(request.form['puntos']) if request.form['puntos'] else 1
                
                success, error_or_id = ExamController.add_question(examen_id, texto, puntos)
                
                if success:
                    flash('Pregunta agregada correctamente', 'success')
                else:
                    flash(f'Error al agregar pregunta: {error_or_id}', 'danger')
                
                return redirect(url_for('admin.edit_examen', course_id=course_id, chapter_id=chapter_id, examen_id=examen_id))
            
            elif 'add_opcion' in request.form:
                # Agregar nueva opción a una pregunta
                pregunta_id = request.form['pregunta_id']
                texto = request.form['texto_opcion']
                es_correcta = 'opcion_correcta' in request.form
                
                success, error = ExamController.add_option(pregunta_id, texto, es_correcta)
                
                if success:
                    flash('Opción agregada correctamente', 'success')
                else:
                    flash(f'Error al agregar opción: {error}', 'danger')
                
                return redirect(url_for('admin.edit_examen', course_id=course_id, chapter_id=chapter_id, examen_id=examen_id))
        
        return render_template('admin/exams/edit.html', 
                            course=course, 
                            chapter=chapter, 
                            examen=examen, 
                            preguntas=preguntas)
    except Exception as ex:
        flash(f'Error al editar examen: {str(ex)}', 'danger')
        return redirect(url_for('admin.admin_examenes', course_id=course_id, chapter_id=chapter_id))

@admin_bp.route('/courses/<int:course_id>/chapters/<int:chapter_id>/exams/<int:examen_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_examen(course_id, chapter_id, examen_id):
    """Elimina un examen"""
    try:
        success, error = ExamController.delete_exam(examen_id)
        
        if success:
            flash('Examen eliminado correctamente', 'success')
        else:
            flash(f'Error al eliminar examen: {error}', 'danger')
    except Exception as ex:
        flash(f'Error al eliminar examen: {str(ex)}', 'danger')
    
    return redirect(url_for('admin.admin_examenes', course_id=course_id, chapter_id=chapter_id))

@admin_bp.route('/courses/<int:course_id>/chapters/<int:chapter_id>/exams/<int:examen_id>/preguntas/<int:pregunta_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_pregunta(course_id, chapter_id, examen_id, pregunta_id):
    """Elimina una pregunta de un examen"""
    try:
        success, error = ExamController.delete_question(pregunta_id)
        
        if success:
            flash('Pregunta eliminada correctamente', 'success')
        else:
            flash(f'Error al eliminar pregunta: {error}', 'danger')
    except Exception as ex:
        flash(f'Error al eliminar pregunta: {str(ex)}', 'danger')
    
    return redirect(url_for('admin.edit_examen', course_id=course_id, chapter_id=chapter_id, examen_id=examen_id))

@admin_bp.route('/courses/<int:course_id>/chapters/<int:chapter_id>/exams/<int:examen_id>/preguntas/<int:pregunta_id>/opciones/<int:opcion_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_opcion(course_id, chapter_id, examen_id, pregunta_id, opcion_id):
    """Elimina una opción de una pregunta"""
    try:
        success, error = ExamController.delete_option(opcion_id)
        
        if success:
            flash('Opción eliminada correctamente', 'success')
        else:
            flash(f'Error al eliminar opción: {error}', 'danger')
    except Exception as ex:
        flash(f'Error al eliminar opción: {str(ex)}', 'danger')
    
    return redirect(url_for('admin.edit_examen', course_id=course_id, chapter_id=chapter_id, examen_id=examen_id))
