from flask import Flask
import os
import sys

# Añadir el directorio raíz al path para poder importar correctamente
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from extensions.extensions import db, init_extensions
from config import config

def debug_exams():
    """
    Herramienta de diagnóstico para examinar la estructura y contenido de los exámenes en la base de datos.
    """
    app = Flask(__name__)
    app.config.from_object(config['development'])
    init_extensions(app)
    
    with app.app_context():
        cursor = db.connection.cursor()
        
        print("=== DIAGNÓSTICO DE EXÁMENES ===")
        
        # Verificar estructura de la tabla examenes
        try:
            cursor.execute("DESCRIBE examenes")
            columns = cursor.fetchall()
            print("\nEstructura de la tabla 'examenes':")
            for col in columns:
                print(f"  - {col[0]}: {col[1]}")
        except Exception as ex:
            print(f"Error al verificar estructura de tabla examenes: {ex}")
        
        # Contar exámenes por capítulo
        try:
            cursor.execute("""
                SELECT c.id, c.titulo, COUNT(e.id) as num_examenes
                FROM capitulos c
                LEFT JOIN examenes e ON c.id = e.capitulo_id
                GROUP BY c.id
                ORDER BY c.id
            """)
            results = cursor.fetchall()
            print("\nExámenes por capítulo:")
            for row in results:
                print(f"  - Capítulo {row[0]} ({row[1]}): {row[2]} exámenes")
        except Exception as ex:
            print(f"Error al contar exámenes por capítulo: {ex}")
        
        # Verificar específicamente el capítulo 5
        try:
            cursor.execute("SELECT * FROM capitulos WHERE id = 5")
            chapter = cursor.fetchone()
            print("\nDetalles del capítulo 5:")
            if chapter:
                print(f"  - ID: {chapter[0]}")
                print(f"  - Curso ID: {chapter[1]}")
                print(f"  - Título: {chapter[2]}")
                
                # Verificar si hay exámenes para este capítulo
                cursor.execute("SELECT * FROM examenes WHERE capitulo_id = 5")
                exams = cursor.fetchall()
                print(f"\nExámenes para el capítulo 5 ({len(exams)}):")
                for exam in exams:
                    print(f"  - ID: {exam[0]}, Título: {exam[2]}")
            else:
                print("  - No se encontró el capítulo 5")
        except Exception as ex:
            print(f"Error al verificar el capítulo 5: {ex}")
        
        # Verificar la ruta de plantillas
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        template_path = os.path.join(base_path, 'templates', 'course', 'exams', 'index.html')
        print(f"\nVerificando plantilla de exámenes:")
        print(f"  - Ruta: {template_path}")
        print(f"  - Existe: {os.path.exists(template_path)}")

if __name__ == '__main__':
    debug_exams() 