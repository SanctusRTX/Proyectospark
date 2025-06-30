from flask import current_app
from extensions.extensions import db
from models.ModelCourse import ModelCourse
from utils.helpers import save_file

class CourseController:
    @staticmethod
    def get_all_courses(active_only=True):
        """Obtiene todos los cursos"""
        return ModelCourse.get_courses(db, active_only)
    
    @staticmethod
    def get_course_by_id(course_id):
        """Obtiene un curso por su ID"""
        return ModelCourse.get_course_by_id(db, course_id)
    
    @staticmethod
    def create_course(title, description, external_url, image, active):
        """Crea un nuevo curso"""
        try:
            # Manejo de la imagen
            image_url = ''
            if image and image.filename != '':
                print(f"Imagen recibida: {image.filename}")
                image_url = save_file(image, current_app.config['UPLOAD_FOLDER'], current_app)
                print(f"URL de imagen generada: {image_url}")
            
            course = {
                'title': title,
                'description': description,
                'external_url': external_url,
                'image_url': image_url,
                'active': active
            }
            
            return ModelCourse.add_course(db, course), None
        except Exception as ex:
            print(f"Error al crear curso: {ex}")
            return False, str(ex)
    
    @staticmethod
    def update_course(course_id, title, description, external_url, image, active):
        """Actualiza un curso existente"""
        try:
            # Obtener el curso actual para mantener la imagen si no se sube una nueva
            current_course = ModelCourse.get_course_by_id(db, course_id)
            if not current_course:
                return False, "Curso no encontrado"
            
            # Mantener la imagen actual si no se sube una nueva
            image_url = current_course[2]  # image_url está en la posición 2
            if image and image.filename != '':
                print(f"Imagen recibida: {image.filename}")
                image_url = save_file(image, current_app.config['UPLOAD_FOLDER'], current_app)
                print(f"URL de imagen generada: {image_url}")
            
            updated_course = {
                'id': course_id,
                'title': title,
                'description': description,
                'external_url': external_url,
                'image_url': image_url,
                'active': active
            }
            
            return ModelCourse.update_course(db, updated_course), None
        except Exception as ex:
            print(f"Error al actualizar curso: {ex}")
            return False, str(ex)
    
    @staticmethod
    def delete_course(course_id):
        """Elimina un curso"""
        try:
            return ModelCourse.delete_course(db, course_id), None
        except Exception as ex:
            return False, str(ex)
    
    @staticmethod
    def fix_image_paths():
        """Corrige las rutas de imágenes en la base de datos"""
        try:
            cursor = db.connection.cursor()
            # Actualizar directamente todas las rutas de imágenes con una sola consulta SQL
            cursor.execute(
                "UPDATE courses SET image_url = REPLACE(image_url, '\\\\', '/') WHERE image_url LIKE '%\\\\%'"
            )
            rows_affected = cursor.rowcount
            db.connection.commit()
            
            return True, rows_affected
        except Exception as ex:
            return False, str(ex)
