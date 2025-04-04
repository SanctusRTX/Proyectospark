from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from config import config
from models.ModelUser import ModelUser
from models.ModelCourse import ModelCourse
from models.ModelChapter import ModelChapter
from models.entities.User import User
from models.entities.Course import Course
from models.entities.Chapter import Chapter
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
            
    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")

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
                image_url = os.path.join('img', 'courses', filename)
        
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
                image_url = os.path.join('img', 'courses', filename)
        
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

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run()