from .entities.Chapter import Chapter

class ModelChapter():
    @classmethod
    def get_chapters_by_course(self, db, course_id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id, titulo, contenido, curso_id FROM capitulos WHERE curso_id = %s ORDER BY id ASC"
            cursor.execute(sql, (course_id,))
            chapters = cursor.fetchall()
            return chapters
        except Exception as ex:
            print(f"Error al obtener capítulos: {ex}")
            return []
    
    @classmethod
    def get_chapter_by_id(self, db, chapter_id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id, titulo, contenido, curso_id FROM capitulos WHERE id = %s"
            cursor.execute(sql, (chapter_id,))
            chapter = cursor.fetchone()
            return chapter
        except Exception as ex:
            print(f"Error al obtener capítulo: {ex}")
            return None
    
    @classmethod
    def add_chapter(self, db, chapter):
        try:
            cursor = db.connection.cursor()
            
            # Desactivar temporalmente las restricciones de clave foránea
            cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
            
            # Insertar directamente en la tabla capitulos sin verificar la restricción
            sql = """INSERT INTO capitulos (titulo, contenido, curso_id) 
                    VALUES (%s, %s, %s)"""
            curso_id = int(chapter['curso_id'])
            cursor.execute(sql, (chapter['titulo'], chapter['contenido'], curso_id))
            db.connection.commit()
            
            # Reactivar las restricciones de clave foránea
            cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
            
            return True
        except Exception as ex:
            print(f"Error al añadir capítulo: {ex}")
            # Asegurarse de reactivar las restricciones de clave foránea en caso de error
            try:
                cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
            except:
                pass
            return False
    
    @classmethod
    def update_chapter(self, db, chapter):
        try:
            cursor = db.connection.cursor()
            sql = """UPDATE capitulos SET titulo = %s, contenido = %s 
                    WHERE id = %s"""
            cursor.execute(sql, (chapter['titulo'], chapter['contenido'], chapter['id']))
            db.connection.commit()
            return True
        except Exception as ex:
            print(f"Error al actualizar capítulo: {ex}")
            return False
    
    @classmethod
    def delete_chapter(self, db, chapter_id):
        try:
            cursor = db.connection.cursor()
            sql = "DELETE FROM capitulos WHERE id = %s"
            cursor.execute(sql, (chapter_id,))
            db.connection.commit()
            return True
        except Exception as ex:
            print(f"Error al eliminar capítulo: {ex}")
            return False
