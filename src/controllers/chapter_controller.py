from extensions.extensions import db
from models.ModelChapter import ModelChapter

class ChapterController:
    @staticmethod
    def get_chapters_by_course(course_id):
        """Obtiene todos los capítulos de un curso"""
        return ModelChapter.get_chapters_by_course(db, course_id)
    
    @staticmethod
    def get_chapter_by_id(chapter_id):
        """Obtiene un capítulo por su ID"""
        return ModelChapter.get_chapter_by_id(db, chapter_id)
    
    @staticmethod
    def create_chapter(title, content, course_id):
        """Crea un nuevo capítulo"""
        try:
            chapter = {
                'titulo': title,
                'contenido': content,
                'curso_id': course_id
            }
            
            return ModelChapter.add_chapter(db, chapter), None
        except Exception as ex:
            return False, str(ex)
    
    @staticmethod
    def update_chapter(chapter_id, title, content):
        """Actualiza un capítulo existente"""
        try:
            updated_chapter = {
                'id': chapter_id,
                'titulo': title,
                'contenido': content
            }
            
            return ModelChapter.update_chapter(db, updated_chapter), None
        except Exception as ex:
            return False, str(ex)
    
    @staticmethod
    def delete_chapter(chapter_id):
        """Elimina un capítulo"""
        try:
            return ModelChapter.delete_chapter(db, chapter_id), None
        except Exception as ex:
            return False, str(ex)
    
    @staticmethod
    def validate_chapter_belongs_to_course(chapter, course_id):
        """Valida que un capítulo pertenezca a un curso"""
        if not chapter:
            return False, "Capítulo no encontrado"
        
        # El curso_id está en la posición 3 del tuple que devuelve get_chapter_by_id
        if chapter[3] != course_id:
            return False, "El capítulo no pertenece a este curso"
        
        return True, None

    @staticmethod
    def get_next_chapter(db, course_id, current_chapter_id):
        """Obtiene el siguiente capítulo en un curso"""
        try:
            cursor = db.connection.cursor()
            sql = """
            SELECT id, titulo 
            FROM capitulos 
            WHERE curso_id = %s AND id > %s 
            ORDER BY id ASC 
            LIMIT 1
            """
            cursor.execute(sql, (course_id, current_chapter_id))
            next_chapter = cursor.fetchone()
            return next_chapter
        except Exception as ex:
            print(f"Error al obtener siguiente capítulo: {ex}")
            return None
    
    @staticmethod
    def get_previous_chapter(db, course_id, current_chapter_id):
        """Obtiene el capítulo anterior en un curso"""
        try:
            cursor = db.connection.cursor()
            sql = """
            SELECT id, titulo 
            FROM capitulos 
            WHERE curso_id = %s AND id < %s 
            ORDER BY id DESC 
            LIMIT 1
            """
            cursor.execute(sql, (course_id, current_chapter_id))
            prev_chapter = cursor.fetchone()
            return prev_chapter
        except Exception as ex:
            print(f"Error al obtener capítulo anterior: {ex}")
            return None
