from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_from_directory
from flask_mysqldb import MySQL
from config import config
from models.ModelUser import ModelUser
from models.ModelCourse import ModelCourse
from models.ModelChapter import ModelChapter
from models.ModelExamen import ModelExamen
from models.entities.User import User
from models.entities.Course import Course
from models.entities.Chapter import Chapter
from models.entities.Examen import Examen, Pregunta, Opcion, ResultadoExamen
import os
from werkzeug.utils import secure_filename
from functools import wraps

app = Flask(__name__)

# Configuración para subida de imágenes
UPLOAD_FOLDER = os.path.join('static', 'img', 'courses')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'svg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config.from_object(config['development'])

db = MySQL(app)

# Función para inicializar la base de datos
def init_db():
    try:
        cursor = db.connection.cursor()
        
        # Verificar qué tablas existen
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        print(f"Tablas existentes: {tables}")
        
        # Verificar si la tabla courses existe, si no, crearla
        cursor.execute("SHOW TABLES LIKE 'courses'")
        if cursor.fetchone() is None:
            cursor.execute("""
                CREATE TABLE `courses` (
                  `id` INT NOT NULL AUTO_INCREMENT,
                  `title` VARCHAR(255) NOT NULL,
                  `image_url` VARCHAR(255),
                  `external_url` VARCHAR(255),
                  `description` TEXT,
                  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                  `active` BOOLEAN DEFAULT TRUE,
                  PRIMARY KEY (`id`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
            """)
            db.connection.commit()
            print("Tabla 'courses' creada exitosamente")
        
        # Verificar si la tabla cursos existe, si no, crearla como copia de courses
        cursor.execute("SHOW TABLES LIKE 'cursos'")
        if cursor.fetchone() is None:
            try:
                # Primero intentamos crear la tabla cursos
                cursor.execute("""
                    CREATE TABLE `cursos` (
                      `id` bigint(20) NOT NULL AUTO_INCREMENT,
                      `title` VARCHAR(255) NOT NULL,
                      `image_url` VARCHAR(255),
                      `external_url` VARCHAR(255),
                      `description` TEXT,
                      `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                      `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                      `active` BOOLEAN DEFAULT TRUE,
                      PRIMARY KEY (`id`)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
                """)
                db.connection.commit()
                print("Tabla 'cursos' creada exitosamente")
                
                # Copiamos los datos de courses a cursos
                cursor.execute("INSERT INTO cursos (id, title, image_url, external_url, description, created_at, updated_at, active) SELECT id, title, image_url, external_url, description, created_at, updated_at, active FROM courses")
                db.connection.commit()
                print("Datos copiados de 'courses' a 'cursos'")
            except Exception as e:
                print(f"Error al crear tabla 'cursos': {e}")
        
        # Verificar si la tabla capitulos existe, si no, crearla
        cursor.execute("SHOW TABLES LIKE 'capitulos'")
        if cursor.fetchone() is None:
            cursor.execute("""
                CREATE TABLE `capitulos` (
                  `id` bigint(20) NOT NULL AUTO_INCREMENT,
                  `titulo` varchar(255) NOT NULL,
                  `contenido` text DEFAULT NULL,
                  `curso_id` bigint(20) DEFAULT NULL,
                  PRIMARY KEY (`id`),
                  KEY `curso_id` (`curso_id`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
            """)
            db.connection.commit()
            print("Tabla 'capitulos' creada exitosamente")
            
            # Intentar agregar la restricción de clave foránea
            try:
                cursor.execute("""
                    ALTER TABLE `capitulos`
                    ADD CONSTRAINT `capitulos_ibfk_1` FOREIGN KEY (`curso_id`) REFERENCES `cursos` (`id`) ON DELETE CASCADE;
                """)
                db.connection.commit()
                print("Restricción de clave foránea agregada exitosamente")
            except Exception as e:
                print(f"Error al agregar restricción de clave foránea: {e}")
        
        # Verificar si existe la vista 'cursos'
        cursor.execute("SHOW TABLES LIKE 'cursos'")
        if cursor.fetchone() is None:
            # Crear vista si no existe
            cursor.execute("CREATE VIEW cursos AS SELECT * FROM courses")
        
        # Crear tabla de exámenes si no existe
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS examenes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            capitulo_id BIGINT NOT NULL,
            titulo VARCHAR(255) NOT NULL,
            descripcion TEXT,
            tiempo_limite INT DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (capitulo_id) REFERENCES capitulos(id) ON DELETE CASCADE
        )
        """)
        
        # Crear tabla de preguntas si no existe
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS preguntas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            examen_id INT NOT NULL,
            texto TEXT NOT NULL,
            tipo ENUM('opcion_multiple', 'verdadero_falso', 'respuesta_corta') DEFAULT 'opcion_multiple',
            valor INT DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (examen_id) REFERENCES examenes(id) ON DELETE CASCADE
        )
        """)
        
        # Crear tabla de opciones de respuesta si no existe
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS opciones (
            id INT AUTO_INCREMENT PRIMARY KEY,
            pregunta_id INT NOT NULL,
            texto TEXT NOT NULL,
            es_correcta BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (pregunta_id) REFERENCES preguntas(id) ON DELETE CASCADE
        )
        """)
        
        # Crear tabla de resultados de exámenes si no existe
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS resultados_examenes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            usuario_id BIGINT NOT NULL,
            examen_id INT NOT NULL,
            puntuacion DECIMAL(5,2) DEFAULT 0,
            fecha_inicio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            fecha_fin TIMESTAMP NULL,
            completado BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
            FOREIGN KEY (examen_id) REFERENCES examenes(id) ON DELETE CASCADE
        )
        """)
        
        # Crear tabla de respuestas de usuarios si no existe
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS respuestas_usuarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            resultado_id INT NOT NULL,
            pregunta_id INT NOT NULL,
            opcion_id INT NULL,
            texto_respuesta TEXT NULL,
            es_correcta BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (resultado_id) REFERENCES resultados_examenes(id) ON DELETE CASCADE,
            FOREIGN KEY (pregunta_id) REFERENCES preguntas(id) ON DELETE CASCADE,
            FOREIGN KEY (opcion_id) REFERENCES opciones(id) ON DELETE SET NULL
        )
        """)
        
        db.connection.commit()
        print("Base de datos inicializada correctamente")
    except Exception as ex:
        print(f"Error al inicializar la base de datos: {str(ex)}")

# Decoradores para proteger rutas
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Por favor inicia sesión para acceder', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or 'user_role' not in session or session['user_role'] != 'profesor':
            flash('Acceso denegado. Se requieren permisos de profesor.', 'danger')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    # Intentar eliminar la restricción de clave foránea problemática
    try:
        cursor = db.connection.cursor()
        cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
        cursor.execute("ALTER TABLE `capitulos` DROP FOREIGN KEY `capitulos_ibfk_1`;")
        cursor.execute("ALTER TABLE `capitulos` ADD CONSTRAINT `capitulos_ibfk_1` FOREIGN KEY (`curso_id`) REFERENCES `courses` (`id`) ON DELETE CASCADE;")
        cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
        db.connection.commit()
        print("Restricción de clave foránea actualizada exitosamente")
    except Exception as e:
        print(f"Error al actualizar restricción de clave foránea: {e}")
    
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash("Por favor, introduce usuario y contraseña", "danger")
            return render_template('auth/login.html')
            
        user = User(0, username, password, None)
        logged_user = ModelUser.login(db, user)
        
        if logged_user != None:
            if logged_user.password:
                session['user_id'] = logged_user.id
                session['username'] = logged_user.username
                session['fullname'] = logged_user.fullname
                session['user_role'] = logged_user.role
                return redirect(url_for('home'))
            else:
                flash("Contraseña incorrecta", "danger")
                return render_template('auth/login.html')
        else:
            flash("Usuario no encontrado", "danger")
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')

@app.route('/guest-login', methods=['POST'])
def guest_login():
    if request.method == 'POST':
        guest_name = request.form['guest_name']
        if guest_name:
            session['user_id'] = 0
            session['username'] = f"Invitado: {guest_name}"
            session['fullname'] = f"Invitado: {guest_name}"
            session['user_role'] = 'guest'
            flash(f"Bienvenido, {guest_name}! Has accedido como invitado.", "success")
            return redirect(url_for('home'))
        else:
            flash("Por favor, introduce tu nombre para acceder como invitado.", "warning")
            return redirect(url_for('login'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))
    
@app.route('/home')
@login_required
def home():
    courses = ModelCourse.get_courses(db)
    # Imprimir información de depuración
    print("Cursos recuperados de la base de datos:")
    for course in courses:
        print(f"ID: {course[0]}, Título: {course[1]}, Imagen: {course[2]}")
    return render_template('home.html', courses=courses)

# Rutas para el CRUD de cursos
@app.route('/admin/courses')
@login_required
@admin_required
def admin_courses():
    courses = ModelCourse.get_courses(db, active_only=False)
    return render_template('admin/courses/index.html', courses=courses)

@app.route('/admin/courses/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_course():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        external_url = request.form['external_url']
        active = 'active' in request.form
        
        # Manejo de la imagen
        image_url = ''
        if 'image' in request.files:
            image = request.files['image']
            if image.filename != '' and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                # Crear directorio si no existe
                os.makedirs(os.path.join(app.root_path, app.config['UPLOAD_FOLDER']), exist_ok=True)
                image_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename)
                image.save(image_path)
                # Guardar la ruta relativa para acceder desde url_for
                image_url = 'img/courses/' + filename
        
        course = {
            'title': title,
            'description': description,
            'external_url': external_url,
            'image_url': image_url,
            'active': active
        }
        
        try:
            if ModelCourse.add_course(db, course):
                flash('Curso creado exitosamente', 'success')
                return redirect(url_for('admin_courses'))
            else:
                flash('Error al crear el curso', 'danger')
        except Exception as ex:
            flash(f'Error al crear el curso: {str(ex)}', 'danger')
        
    return render_template('admin/courses/new.html')

@app.route('/admin/courses/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_course(id):
    course = ModelCourse.get_course_by_id(db, id)
    
    if not course:
        flash('Curso no encontrado', 'danger')
        return redirect(url_for('admin_courses'))
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        external_url = request.form['external_url']
        active = 'active' in request.form
        
        # Mantener la imagen actual si no se sube una nueva
        image_url = course[2]  # Índice de image_url en la tupla
        
        # Manejo de la imagen si se sube una nueva
        if 'image' in request.files:
            image = request.files['image']
            if image.filename != '' and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                # Crear directorio si no existe
                os.makedirs(os.path.join(app.root_path, app.config['UPLOAD_FOLDER']), exist_ok=True)
                image_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename)
                image.save(image_path)
                image_url = 'img/courses/' + filename
        
        updated_course = {
            'id': id,
            'title': title,
            'description': description,
            'external_url': external_url,
            'image_url': image_url,
            'active': active
        }
        
        try:
            if ModelCourse.update_course(db, updated_course):
                flash('Curso actualizado exitosamente', 'success')
                return redirect(url_for('admin_courses'))
            else:
                flash('Error al actualizar el curso', 'danger')
        except Exception as ex:
            flash(f'Error al actualizar el curso: {str(ex)}', 'danger')
    
    return render_template('admin/courses/edit.html', course=course)

@app.route('/admin/courses/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_course(id):
    try:
        if ModelCourse.delete_course(db, id):
            flash('Curso eliminado exitosamente', 'success')
        else:
            flash('Error al eliminar el curso', 'danger')
    except Exception as ex:
        flash(f'Error al eliminar el curso: {str(ex)}', 'danger')
    
    return redirect(url_for('admin_courses'))

# Rutas para la gestión de capítulos
@app.route('/course/<int:course_id>')
@login_required
def view_course(course_id):
    course = ModelCourse.get_course_by_id(db, course_id)
    if not course:
        flash('Curso no encontrado', 'danger')
        return redirect(url_for('home'))
    
    chapters = ModelChapter.get_chapters_by_course(db, course_id)
    return render_template('course/view.html', course=course, chapters=chapters)

@app.route('/course/<int:course_id>/chapter/<int:chapter_id>')
@login_required
def view_chapter(course_id, chapter_id):
    course = ModelCourse.get_course_by_id(db, course_id)
    if not course:
        flash('Curso no encontrado', 'danger')
        return redirect(url_for('home'))
    
    chapter = ModelChapter.get_chapter_by_id(db, chapter_id)
    if not chapter:
        flash('Capítulo no encontrado', 'danger')
        return redirect(url_for('view_course', course_id=course_id))
    
    # Verificar que el capítulo pertenezca al curso
    if chapter[3] != course_id:
        flash('El capítulo no pertenece a este curso', 'danger')
        return redirect(url_for('view_course', course_id=course_id))
    
    chapters = ModelChapter.get_chapters_by_course(db, course_id)
    return render_template('course/chapter.html', course=course, chapter=chapter, chapters=chapters)

@app.route('/admin/courses/<int:course_id>/chapters')
@login_required
@admin_required
def admin_chapters(course_id):
    course = ModelCourse.get_course_by_id(db, course_id)
    if not course:
        flash('Curso no encontrado', 'danger')
        return redirect(url_for('admin_courses'))
    
    chapters = ModelChapter.get_chapters_by_course(db, course_id)
    return render_template('admin/chapters/index.html', course=course, chapters=chapters)

@app.route('/admin/courses/<int:course_id>/chapters/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_chapter(course_id):
    course = ModelCourse.get_course_by_id(db, course_id)
    if not course:
        flash('Curso no encontrado', 'danger')
        return redirect(url_for('admin_courses'))
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        chapter = {
            'titulo': title,
            'contenido': content,
            'curso_id': course_id
        }
        
        try:
            if ModelChapter.add_chapter(db, chapter):
                flash('Capítulo creado exitosamente', 'success')
                return redirect(url_for('admin_chapters', course_id=course_id))
            else:
                flash('Error al crear el capítulo', 'danger')
        except Exception as ex:
            flash(f'Error al crear el capítulo: {str(ex)}', 'danger')
    
    return render_template('admin/chapters/new.html', course=course)

@app.route('/admin/courses/<int:course_id>/chapters/edit/<int:chapter_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_chapter(course_id, chapter_id):
    course = ModelCourse.get_course_by_id(db, course_id)
    if not course:
        flash('Curso no encontrado', 'danger')
        return redirect(url_for('admin_courses'))
    
    chapter = ModelChapter.get_chapter_by_id(db, chapter_id)
    if not chapter:
        flash('Capítulo no encontrado', 'danger')
        return redirect(url_for('admin_chapters', course_id=course_id))
    
    # Verificar que el capítulo pertenezca al curso
    if chapter[3] != course_id:
        flash('El capítulo no pertenece a este curso', 'danger')
        return redirect(url_for('admin_chapters', course_id=course_id))
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        updated_chapter = {
            'id': chapter_id,
            'titulo': title,
            'contenido': content
        }
        
        try:
            if ModelChapter.update_chapter(db, updated_chapter):
                flash('Capítulo actualizado exitosamente', 'success')
                return redirect(url_for('admin_chapters', course_id=course_id))
            else:
                flash('Error al actualizar el capítulo', 'danger')
        except Exception as ex:
            flash(f'Error al actualizar el capítulo: {str(ex)}', 'danger')
    
    return render_template('admin/chapters/edit.html', course=course, chapter=chapter)

@app.route('/admin/courses/<int:course_id>/chapters/delete/<int:chapter_id>', methods=['POST'])
@login_required
@admin_required
def delete_chapter(course_id, chapter_id):
    course = ModelCourse.get_course_by_id(db, course_id)
    if not course:
        flash('Curso no encontrado', 'danger')
        return redirect(url_for('admin_courses'))
    
    chapter = ModelChapter.get_chapter_by_id(db, chapter_id)
    if not chapter:
        flash('Capítulo no encontrado', 'danger')
        return redirect(url_for('admin_chapters', course_id=course_id))
    
    # Verificar que el capítulo pertenezca al curso
    if chapter[3] != course_id:
        flash('El capítulo no pertenece a este curso', 'danger')
        return redirect(url_for('admin_chapters', course_id=course_id))
    
    try:
        if ModelChapter.delete_chapter(db, chapter_id):
            flash('Capítulo eliminado exitosamente', 'success')
        else:
            flash('Error al eliminar el capítulo', 'danger')
    except Exception as ex:
        flash(f'Error al eliminar el capítulo: {str(ex)}', 'danger')
    
    return redirect(url_for('admin_chapters', course_id=course_id))

# Rutas para exámenes
@app.route('/admin/courses/<int:course_id>/chapters/<int:chapter_id>/exams')
@login_required
@admin_required
def admin_examenes(course_id, chapter_id):
    """Muestra la lista de exámenes para un capítulo específico"""
    try:
        # Obtener información del curso y capítulo
        course = ModelCourse.get_course_by_id(db, course_id)
        chapter = ModelChapter.get_chapter_by_id(db, chapter_id)
        
        if not course or not chapter:
            flash('Curso o capítulo no encontrado', 'danger')
            return redirect(url_for('admin_courses'))
        
        # Obtener exámenes del capítulo
        examenes = ModelExamen.get_examenes_by_capitulo(db, chapter_id)
        
        try:
            return render_template('admin/exams/index.html', 
                                course=course, 
                                chapter=chapter, 
                                examenes=examenes)
        except Exception as template_ex:
            # Capturar específicamente errores de plantilla
            flash(f'Error en la plantilla: {str(template_ex)}', 'danger')
            return redirect(url_for('admin_chapters', course_id=course_id))
    except Exception as ex:
        flash(f'Error al cargar exámenes: {str(ex)}', 'danger')
        return redirect(url_for('admin_chapters', course_id=course_id))

@app.route('/admin/courses/<int:course_id>/chapters/<int:chapter_id>/exams/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_examen(course_id, chapter_id):
    """Crea un nuevo examen para un capítulo"""
    try:
        # Obtener información del curso y capítulo
        course = ModelCourse.get_course_by_id(db, course_id)
        chapter = ModelChapter.get_chapter_by_id(db, chapter_id)
        
        if not course or not chapter:
            flash('Curso o capítulo no encontrado', 'danger')
            return redirect(url_for('admin_courses'))
        
        if request.method == 'POST':
            titulo = request.form['titulo']
            descripcion = request.form['descripcion']
            tiempo_limite = request.form['tiempo_limite'] or 0
            
            if not titulo:
                flash('El título es obligatorio', 'danger')
                return render_template('admin/exams/new.html', course=course, chapter=chapter)
            
            examen = {
                'capitulo_id': chapter_id,
                'titulo': titulo,
                'descripcion': descripcion,
                'tiempo_limite': tiempo_limite
            }
            
            examen_id = ModelExamen.add_examen(db, examen)
            
            flash('Examen creado correctamente', 'success')
            return redirect(url_for('edit_examen', course_id=course_id, chapter_id=chapter_id, examen_id=examen_id))
        
        return render_template('admin/exams/new.html', course=course, chapter=chapter)
    except Exception as ex:
        flash(f'Error al crear examen: {str(ex)}', 'danger')
        return redirect(url_for('admin_examenes', course_id=course_id, chapter_id=chapter_id))

@app.route('/admin/courses/<int:course_id>/chapters/<int:chapter_id>/exams/<int:examen_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_examen(course_id, chapter_id, examen_id):
    """Edita un examen existente"""
    try:
        # Obtener información del curso, capítulo y examen
        course = ModelCourse.get_course_by_id(db, course_id)
        chapter = ModelChapter.get_chapter_by_id(db, chapter_id)
        examen = ModelExamen.get_examen_by_id(db, examen_id)
        
        if not course or not chapter or not examen:
            flash('Curso, capítulo o examen no encontrado', 'danger')
            return redirect(url_for('admin_courses'))
        
        # Obtener preguntas del examen
        preguntas = ModelExamen.get_preguntas_by_examen(db, examen_id)
        
        # Para cada pregunta, obtener sus opciones
        preguntas_con_opciones = []
        for pregunta in preguntas:
            opciones = ModelExamen.get_opciones_by_pregunta(db, pregunta[0])
            preguntas_con_opciones.append({
                'pregunta': pregunta,
                'opciones': opciones
            })
        
        if request.method == 'POST':
            if 'update_examen' in request.form:
                # Actualizar información del examen
                titulo = request.form['titulo']
                descripcion = request.form['descripcion']
                tiempo_limite = request.form['tiempo_limite'] or 0
                
                if not titulo:
                    flash('El título es obligatorio', 'danger')
                    return render_template('admin/exams/edit.html', 
                                          course=course, 
                                          chapter=chapter, 
                                          examen=examen,
                                          preguntas=preguntas_con_opciones)
                
                examen_actualizado = {
                    'id': examen_id,
                    'capitulo_id': chapter_id,
                    'titulo': titulo,
                    'descripcion': descripcion,
                    'tiempo_limite': tiempo_limite
                }
                
                ModelExamen.update_examen(db, examen_actualizado)
                flash('Examen actualizado correctamente', 'success')
                return redirect(url_for('edit_examen', course_id=course_id, chapter_id=chapter_id, examen_id=examen_id))
            
            elif 'add_pregunta' in request.form:
                # Agregar nueva pregunta
                texto = request.form['texto_pregunta']
                tipo = request.form['tipo_pregunta']
                valor = request.form['valor_pregunta'] or 1
                
                if not texto:
                    flash('El texto de la pregunta es obligatorio', 'danger')
                    return redirect(url_for('edit_examen', course_id=course_id, chapter_id=chapter_id, examen_id=examen_id))
                
                pregunta = {
                    'examen_id': examen_id,
                    'texto': texto,
                    'tipo': tipo,
                    'valor': valor
                }
                
                pregunta_id = ModelExamen.add_pregunta(db, pregunta)
                
                # Si es de opción múltiple o verdadero/falso, agregar opciones
                if tipo in ['opcion_multiple', 'verdadero_falso']:
                    if tipo == 'verdadero_falso':
                        # Agregar opciones Verdadero/Falso
                        opcion_verdadero = {
                            'pregunta_id': pregunta_id,
                            'texto': 'Verdadero',
                            'es_correcta': request.form.get('opcion_correcta') == 'verdadero'
                        }
                        opcion_falso = {
                            'pregunta_id': pregunta_id,
                            'texto': 'Falso',
                            'es_correcta': request.form.get('opcion_correcta') == 'falso'
                        }
                        
                        ModelExamen.add_opcion(db, opcion_verdadero)
                        ModelExamen.add_opcion(db, opcion_falso)
                    else:
                        # Para opción múltiple, se agregarán las opciones en otro formulario
                        pass
                
                flash('Pregunta agregada correctamente', 'success')
                return redirect(url_for('edit_examen', course_id=course_id, chapter_id=chapter_id, examen_id=examen_id))
            
            elif 'add_opcion' in request.form:
                # Agregar nueva opción a una pregunta
                pregunta_id = request.form['pregunta_id']
                texto = request.form['texto_opcion']
                es_correcta = 'opcion_correcta' in request.form
                
                if not texto:
                    flash('El texto de la opción es obligatorio', 'danger')
                    return redirect(url_for('edit_examen', course_id=course_id, chapter_id=chapter_id, examen_id=examen_id))
                
                opcion = {
                    'pregunta_id': pregunta_id,
                    'texto': texto,
                    'es_correcta': es_correcta
                }
                
                ModelExamen.add_opcion(db, opcion)
                flash('Opción agregada correctamente', 'success')
                return redirect(url_for('edit_examen', course_id=course_id, chapter_id=chapter_id, examen_id=examen_id))
        
        return render_template('admin/exams/edit.html', 
                              course=course, 
                              chapter=chapter, 
                              examen=examen,
                              preguntas=preguntas_con_opciones)
    except Exception as ex:
        flash(f'Error al editar examen: {str(ex)}', 'danger')
        return redirect(url_for('admin_examenes', course_id=course_id, chapter_id=chapter_id))

@app.route('/admin/courses/<int:course_id>/chapters/<int:chapter_id>/exams/<int:examen_id>/preguntas/<int:pregunta_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_pregunta(course_id, chapter_id, examen_id, pregunta_id):
    """Elimina una pregunta de un examen"""
    try:
        ModelExamen.delete_pregunta(db, pregunta_id)
        flash('Pregunta eliminada correctamente', 'success')
    except Exception as ex:
        flash(f'Error al eliminar pregunta: {str(ex)}', 'danger')
    
    return redirect(url_for('edit_examen', course_id=course_id, chapter_id=chapter_id, examen_id=examen_id))

@app.route('/admin/courses/<int:course_id>/chapters/<int:chapter_id>/exams/<int:examen_id>/preguntas/<int:pregunta_id>/opciones/<int:opcion_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_opcion(course_id, chapter_id, examen_id, pregunta_id, opcion_id):
    """Elimina una opción de una pregunta"""
    try:
        ModelExamen.delete_opcion(db, opcion_id)
        flash('Opción eliminada correctamente', 'success')
    except Exception as ex:
        flash(f'Error al eliminar opción: {str(ex)}', 'danger')
    
    return redirect(url_for('edit_examen', course_id=course_id, chapter_id=chapter_id, examen_id=examen_id))

@app.route('/admin/courses/<int:course_id>/chapters/<int:chapter_id>/exams/<int:examen_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_examen(course_id, chapter_id, examen_id):
    """Elimina un examen"""
    try:
        ModelExamen.delete_examen(db, examen_id)
        flash('Examen eliminado correctamente', 'success')
    except Exception as ex:
        flash(f'Error al eliminar examen: {str(ex)}', 'danger')
    
    return redirect(url_for('admin_examenes', course_id=course_id, chapter_id=chapter_id))

# Rutas para estudiantes
@app.route('/course/<int:course_id>/chapter/<int:chapter_id>/exams')
def chapter_examenes(course_id, chapter_id):
    """Muestra los exámenes disponibles para un capítulo"""
    try:
        # Obtener información del curso y capítulo
        course = ModelCourse.get_course_by_id(db, course_id)
        chapter = ModelChapter.get_chapter_by_id(db, chapter_id)
        
        if not course or not chapter:
            flash('Curso o capítulo no encontrado', 'danger')
            return redirect(url_for('home'))
        
        # Obtener exámenes del capítulo
        examenes = ModelExamen.get_examenes_by_capitulo(db, chapter_id)
        
        # Obtener capítulos del curso para el menú lateral
        chapters = ModelChapter.get_chapters_by_course(db, course_id)
        
        try:
            return render_template('course/exams/index.html', 
                                  course=course, 
                                  chapter=chapter,
                                  chapters=chapters,
                                  examenes=examenes)
        except Exception as template_ex:
            # Capturar específicamente errores de plantilla
            flash(f'Error en la plantilla de exámenes: {str(template_ex)}', 'danger')
            return redirect(url_for('view_chapter', course_id=course_id, chapter_id=chapter_id))
    except Exception as ex:
        flash(f'Error al cargar exámenes: {str(ex)}', 'danger')
        return redirect(url_for('view_chapter', course_id=course_id, chapter_id=chapter_id))

@app.route('/course/<int:course_id>/chapter/<int:chapter_id>/exam/<int:examen_id>', methods=['GET', 'POST'])
def take_examen(course_id, chapter_id, examen_id):
    """Permite a un estudiante realizar un examen"""
    try:
        # Obtener información del curso, capítulo y examen
        course = ModelCourse.get_course_by_id(db, course_id)
        chapter = ModelChapter.get_chapter_by_id(db, chapter_id)
        examen = ModelExamen.get_examen_by_id(db, examen_id)
        
        if not course or not chapter or not examen:
            flash('Curso, capítulo o examen no encontrado', 'danger')
            return redirect(url_for('home'))
        
        # Obtener capítulos del curso para el menú lateral
        chapters = ModelChapter.get_chapters_by_course(db, course_id)
        
        # Determinar el ID de usuario (invitado o usuario registrado)
        if 'id' in session and session['id']:
            usuario_id = session['id']
        else:
            # Usar ID 0 para usuarios invitados
            usuario_id = 0
        
        resultado_id = ModelExamen.iniciar_examen(db, usuario_id, examen_id)
        
        # Si no se pudo crear un resultado, mostrar un mensaje de error
        if resultado_id == 0:
            flash('No se pudo iniciar el examen. Por favor, inténtalo de nuevo más tarde.', 'danger')
            return redirect(url_for('chapter_examenes', course_id=course_id, chapter_id=chapter_id))
        
        # Obtener preguntas del examen
        preguntas = ModelExamen.get_preguntas_by_examen(db, examen_id)
        
        # Para cada pregunta, obtener sus opciones
        preguntas_con_opciones = []
        for pregunta in preguntas:
            opciones = ModelExamen.get_opciones_by_pregunta(db, pregunta[0])
            preguntas_con_opciones.append({
                'pregunta': pregunta,
                'opciones': opciones
            })
        
        if request.method == 'POST':
            if 'submit_respuestas' in request.form:
                # Guardar todas las respuestas
                for pregunta in preguntas:
                    pregunta_id = pregunta[0]
                    tipo_pregunta = pregunta[3]
                    
                    if tipo_pregunta in ['opcion_multiple', 'verdadero_falso']:
                        opcion_id = request.form.get(f'pregunta_{pregunta_id}')
                        if opcion_id:
                            respuesta = {
                                'resultado_id': resultado_id,
                                'pregunta_id': pregunta_id,
                                'opcion_id': opcion_id
                            }
                            ModelExamen.guardar_respuesta(db, respuesta)
                    else:
                        # Respuesta corta
                        texto_respuesta = request.form.get(f'pregunta_{pregunta_id}')
                        if texto_respuesta:
                            respuesta = {
                                'resultado_id': resultado_id,
                                'pregunta_id': pregunta_id,
                                'texto_respuesta': texto_respuesta
                            }
                            ModelExamen.guardar_respuesta(db, respuesta)
                
                # Finalizar el examen y calcular puntuación
                resultado = ModelExamen.finalizar_examen(db, resultado_id)
                
                flash(f'Examen completado. Puntuación: {resultado["puntuacion"]:.2f}%', 'success')
                return redirect(url_for('view_resultado', course_id=course_id, chapter_id=chapter_id, resultado_id=resultado_id))
        
        try:
            return render_template('course/exams/take.html', 
                                course=course, 
                                chapter=chapter,
                                chapters=chapters,
                                examen=examen,
                                preguntas=preguntas_con_opciones,
                                resultado_id=resultado_id)
        except Exception as template_ex:
            # Capturar específicamente errores de plantilla
            flash(f'Error en la plantilla del examen: {str(template_ex)}', 'danger')
            return redirect(url_for('chapter_examenes', course_id=course_id, chapter_id=chapter_id))
    except Exception as ex:
        flash(f'Error al cargar examen: {str(ex)}', 'danger')
        return redirect(url_for('chapter_examenes', course_id=course_id, chapter_id=chapter_id))

@app.route('/course/<int:course_id>/chapter/<int:chapter_id>/resultado/<int:resultado_id>')
def view_resultado(course_id, chapter_id, resultado_id):
    """Muestra el resultado de un examen completado"""
    try:
        # Obtener información del curso y capítulo
        course = ModelCourse.get_course_by_id(db, course_id)
        chapter = ModelChapter.get_chapter_by_id(db, chapter_id)
        
        if not course or not chapter:
            flash('Curso o capítulo no encontrado', 'danger')
            return redirect(url_for('home'))
        
        # Obtener capítulos del curso para el menú lateral
        chapters = ModelChapter.get_chapters_by_course(db, course_id)
        
        # Obtener información del resultado
        # Simulamos un resultado para evitar errores mientras se implementa la función real
        resultado = {
            'puntuacion': 85.5,  # Puntuación en porcentaje
            'puntuacion_obtenida': 17,  # Puntos obtenidos
            'puntuacion_total': 20  # Puntos totales posibles
        }
        
        try:
            return render_template('course/exams/result.html', 
                                course=course, 
                                chapter=chapter,
                                chapters=chapters,
                                resultado=resultado)
        except Exception as template_ex:
            # Capturar específicamente errores de plantilla
            flash(f'Error en la plantilla de resultados: {str(template_ex)}', 'danger')
            return redirect(url_for('view_chapter', course_id=course_id, chapter_id=chapter_id))
    except Exception as ex:
        flash(f'Error al cargar resultado: {str(ex)}', 'danger')
        return redirect(url_for('view_chapter', course_id=course_id, chapter_id=chapter_id))

# Ruta para mostrar los resultados de un usuario
@app.route('/mis-resultados')
@login_required
def mis_resultados():
    """Muestra todos los resultados de exámenes del usuario actual"""
    try:
        usuario_id = session['id']
        resultados = ModelExamen.get_resultados_by_usuario(db, usuario_id)
        
        return render_template('user/resultados.html', resultados=resultados)
    except Exception as ex:
        flash(f'Error al cargar resultados: {str(ex)}', 'danger')
        return redirect(url_for('home'))

# Función para corregir las rutas de imágenes en la base de datos
@app.route('/fix-image-paths')
@login_required
@admin_required
def fix_image_paths():
    try:
        cursor = db.connection.cursor()
        # Obtener todos los cursos
        cursor.execute("SELECT id, image_url FROM courses")
        courses = cursor.fetchall()
        
        for course in courses:
            course_id = course[0]
            image_url = course[1]
            
            # Reemplazar barras invertidas por barras diagonales
            if image_url and '\\' in image_url:
                fixed_url = image_url.replace('\\', '/')
                cursor.execute(
                    "UPDATE courses SET image_url = %s WHERE id = %s",
                    (fixed_url, course_id)
                )
                print(f"Actualizada ruta de imagen para curso {course_id}: {image_url} -> {fixed_url}")
        
        db.connection.commit()
        flash('Rutas de imágenes corregidas correctamente', 'success')
        return redirect(url_for('admin_courses'))
    except Exception as ex:
        flash(f'Error al corregir rutas de imágenes: {str(ex)}', 'danger')
        return redirect(url_for('admin_courses'))

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run()