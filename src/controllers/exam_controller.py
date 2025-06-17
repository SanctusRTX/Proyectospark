from extensions.extensions import db
from models.ModelExamen import ModelExamen

class ExamController:
    @staticmethod
    def get_exams_by_chapter(chapter_id):
        """Obtiene todos los exámenes de un capítulo"""
        return ModelExamen.get_examenes_by_capitulo(db, chapter_id)
        
    @staticmethod
    def get_questions_by_exam(exam_id):
        """Obtiene todas las preguntas de un examen con sus opciones"""
        return ModelExamen.get_preguntas_by_examen(db, exam_id)
        
    @staticmethod
    def get_questions_with_options(exam_id):
        """Obtiene todas las preguntas de un examen con sus opciones"""
        return ModelExamen.get_preguntas_con_opciones(db, exam_id)
    
    @staticmethod
    def get_exam_by_id(exam_id):
        """Obtiene un examen por su ID"""
        return ModelExamen.get_examen_by_id(db, exam_id)
    
    @staticmethod
    def create_exam(titulo, descripcion, tiempo_limite, chapter_id):
        """Crea un nuevo examen"""
        try:
            examen = {
                'titulo': titulo,
                'descripcion': descripcion,
                'capitulo_id': chapter_id,
                'tiempo_limite': tiempo_limite
            }
            
            return ModelExamen.add_examen(db, examen), None
        except Exception as ex:
            return False, str(ex)
    
    @staticmethod
    def update_exam(exam_id, titulo, descripcion, tiempo_limite):
        """Actualiza un examen existente"""
        try:
            examen = {
                'id': exam_id,
                'titulo': titulo,
                'descripcion': descripcion,
                'tiempo_limite': tiempo_limite
            }
            
            return ModelExamen.update_examen(db, examen), None
        except Exception as ex:
            return False, str(ex)
    
    @staticmethod
    def delete_exam(exam_id):
        """Elimina un examen"""
        try:
            return ModelExamen.delete_examen(db, exam_id), None
        except Exception as ex:
            return False, str(ex)
    
    @staticmethod
    def add_question(exam_id, texto, tipo, valor):
        """Añade una pregunta a un examen"""
        try:
            pregunta = {
                'examen_id': exam_id,
                'texto': texto,
                'tipo': tipo,
                'valor': valor
            }
            
            return ModelExamen.add_pregunta(db, pregunta), None
        except Exception as ex:
            return False, str(ex)
    
    @staticmethod
    def delete_question(question_id):
        """Elimina una pregunta"""
        try:
            return ModelExamen.delete_pregunta(db, question_id), None
        except Exception as ex:
            return False, str(ex)
    
    @staticmethod
    def add_option(question_id, texto, es_correcta):
        """Añade una opción a una pregunta"""
        try:
            opcion = {
                'pregunta_id': question_id,
                'texto': texto,
                'es_correcta': es_correcta
            }
            
            return ModelExamen.add_opcion(db, opcion), None
        except Exception as ex:
            return False, str(ex)
    
    @staticmethod
    def delete_option(option_id):
        """Elimina una opción"""
        try:
            return ModelExamen.delete_opcion(db, option_id), None
        except Exception as ex:
            return False, str(ex)
    
    @staticmethod
    def submit_exam(examen_id, usuario_id, respuestas):
        """Procesa la entrega de un examen"""
        try:
            resultado_id = ModelExamen.procesar_examen(db, examen_id, usuario_id, respuestas)
            if resultado_id:
                return True, resultado_id
            else:
                return False, "No se pudo procesar el examen"
        except Exception as ex:
            return False, str(ex)
    
    @staticmethod
    def get_result_by_id(resultado_id):
        """Obtiene un resultado de examen por su ID"""
        return ModelExamen.get_resultado_by_id(db, resultado_id)
    
    @staticmethod
    def get_results_by_user(usuario_id):
        """Obtiene todos los resultados de exámenes de un usuario"""
        return ModelExamen.get_resultados_by_usuario(db, usuario_id)
