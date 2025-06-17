from flask import Flask
import os
import sys

# Añadir el directorio raíz al path para poder importar correctamente
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from extensions.extensions import db, init_extensions
from config import config

def check_exams():
    """
    Herramienta simple para verificar la existencia y relaciones de exámenes en la base de datos.
    """
    app = Flask(__name__)
    app.config.from_object(config['development'])
    init_extensions(app)
    
    with app.app_context():
        cursor = db.connection.cursor()
        
        # Verificar si hay exámenes para el capítulo 5
        cursor.execute('SELECT * FROM examenes WHERE capitulo_id = 5')
        exams_cap5 = cursor.fetchall()
        print(f"Exámenes para capítulo 5: {exams_cap5}")
        
        # Verificar si el capítulo 5 pertenece al curso 4
        cursor.execute('SELECT * FROM capitulos WHERE id = 5')
        chapter = cursor.fetchone()
        print(f"Capítulo 5: {chapter}")
        
        if chapter:
            course_id = chapter[1]  # Suponiendo que el ID del curso está en la posición 1
            print(f"El capítulo 5 pertenece al curso: {course_id}")
            
            # Verificar que el curso existe
            cursor.execute('SELECT * FROM courses WHERE id = %s', (course_id,))
            course = cursor.fetchone()
            print(f"Curso {course_id}: {course}")

if __name__ == '__main__':
    check_exams() 