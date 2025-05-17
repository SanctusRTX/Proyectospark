from flask import Blueprint, render_template, redirect, url_for
from controllers.course_controller import CourseController
from utils.decorators import login_required

# Crear el blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return redirect(url_for('auth.login'))

@main_bp.route('/home')
@login_required
def home():
    courses = CourseController.get_all_courses()
    # Imprimir información de depuración
    print("Cursos recuperados de la base de datos:")
    for course in courses:
        print(f"ID: {course[0]}, Título: {course[1]}, Imagen: {course[2]}")
    return render_template('home.html', courses=courses)
