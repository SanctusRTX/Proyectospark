class ModelCourse():
    @classmethod
    def get_courses(self, db, active_only=True):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id, title, image_url, external_url, description, active FROM courses"
            if active_only:
                sql += " WHERE active = 1"
            cursor.execute(sql)
            courses = cursor.fetchall()
            # Imprimir las rutas de las imágenes para depuración
            for course in courses:
                print(f"Curso ID: {course[0]}, Título: {course[1]}, Ruta de imagen: {course[2]}")
            return courses
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def get_course_by_id(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id, title, image_url, external_url, description, active FROM courses WHERE id = %s"
            cursor.execute(sql, (id,))
            course = cursor.fetchone()
            return course
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def add_course(self, db, course):
        try:
            cursor = db.connection.cursor()
            sql = """INSERT INTO courses (title, image_url, external_url, description, active) 
                    VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(sql, (course['title'], course['image_url'], 
                                course['external_url'], course['description'], 
                                course['active']))
            db.connection.commit()
            return True
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def update_course(self, db, course):
        try:
            cursor = db.connection.cursor()
            sql = """UPDATE courses SET title = %s, image_url = %s, 
                    external_url = %s, description = %s, active = %s 
                    WHERE id = %s"""
            cursor.execute(sql, (course['title'], course['image_url'], 
                                course['external_url'], course['description'], 
                                course['active'], course['id']))
            db.connection.commit()
            return True
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def delete_course(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "DELETE FROM courses WHERE id = %s"
            cursor.execute(sql, (id,))
            db.connection.commit()
            return True
        except Exception as ex:
            raise Exception(ex)
