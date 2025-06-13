from flask import Blueprint, render_template, redirect, url_for, session
from controllers.course_controller import CourseController
from utils.decorators import login_required

# Crear el blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # La ruta principal muestra home.html sin requerir autenticación
    courses = CourseController.get_all_courses()
    is_authenticated = 'user_id' in session
    return render_template('home.html', courses=courses, is_authenticated=is_authenticated)

# Mantener la ruta /home para compatibilidad con el código existente
@main_bp.route('/home')
def home():
    # Redirigir a la página principal
    return redirect(url_for('main.index'))
