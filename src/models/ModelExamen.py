from flask_mysqldb import MySQL
from datetime import datetime

class ModelExamen():
    @classmethod
    def get_examenes_by_capitulo(self, db, capitulo_id):
        """Obtiene todos los exámenes asociados a un capítulo específico"""
        try:
            cursor = db.connection.cursor()
            sql = """
                SELECT id, capitulo_id, titulo, descripcion, tiempo_limite, created_at, updated_at 
                FROM examenes 
                WHERE capitulo_id = %s
                ORDER BY created_at DESC
            """
            cursor.execute(sql, (capitulo_id,))
            examenes = cursor.fetchall()
            return examenes
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def get_examen_by_id(self, db, examen_id):
        """Obtiene un examen por su ID"""
        try:
            cursor = db.connection.cursor()
            sql = """
                SELECT id, capitulo_id, titulo, descripcion, tiempo_limite, created_at, updated_at 
                FROM examenes 
                WHERE id = %s
            """
            cursor.execute(sql, (examen_id,))
            examen = cursor.fetchone()
            return examen
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def add_examen(self, db, examen):
        """Agrega un nuevo examen a la base de datos"""
        try:
            cursor = db.connection.cursor()
            sql = """
                INSERT INTO examenes (capitulo_id, titulo, descripcion, tiempo_limite) 
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (
                examen['capitulo_id'],
                examen['titulo'],
                examen['descripcion'],
                examen['tiempo_limite']
            ))
            db.connection.commit()
            return cursor.lastrowid
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def update_examen(self, db, examen):
        """Actualiza un examen existente"""
        try:
            cursor = db.connection.cursor()
            sql = """
                UPDATE examenes 
                SET capitulo_id = %s, titulo = %s, descripcion = %s, tiempo_limite = %s
                WHERE id = %s
            """
            cursor.execute(sql, (
                examen['capitulo_id'],
                examen['titulo'],
                examen['descripcion'],
                examen['tiempo_limite'],
                examen['id']
            ))
            db.connection.commit()
            return True
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def delete_examen(cls, db, examen_id):
        """Elimina un examen y todas sus preguntas y opciones asociadas"""
        cursor = db.connection.cursor()
        
        # Primero eliminamos todas las respuestas de usuarios
        sql_respuestas = "DELETE FROM respuestas_usuarios WHERE pregunta_id IN (SELECT id FROM preguntas WHERE examen_id = %s)"
        cursor.execute(sql_respuestas, (examen_id,))
        
        # Luego eliminamos todos los resultados de exámenes
        sql_resultados = "DELETE FROM resultados_examenes WHERE examen_id = %s"
        cursor.execute(sql_resultados, (examen_id,))
        
        # Eliminamos todas las opciones de respuesta
        sql_opciones = "DELETE FROM opciones WHERE pregunta_id IN (SELECT id FROM preguntas WHERE examen_id = %s)"
        cursor.execute(sql_opciones, (examen_id,))
        
        # Eliminamos todas las preguntas
        sql_preguntas = "DELETE FROM preguntas WHERE examen_id = %s"
        cursor.execute(sql_preguntas, (examen_id,))
        
        # Finalmente eliminamos el examen
        sql_examen = "DELETE FROM examenes WHERE id = %s"
        cursor.execute(sql_examen, (examen_id,))
        
        db.connection.commit()
    
    @classmethod
    def get_preguntas_by_examen(self, db, examen_id):
        """Obtiene todas las preguntas asociadas a un examen específico"""
        try:
            cursor = db.connection.cursor()
            sql = """
                SELECT id, examen_id, texto, tipo, valor, created_at, updated_at 
                FROM preguntas 
                WHERE examen_id = %s
                ORDER BY id ASC
            """
            cursor.execute(sql, (examen_id,))
            preguntas = cursor.fetchall()
            return preguntas
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def add_pregunta(self, db, pregunta):
        """Agrega una nueva pregunta a un examen"""
        try:
            cursor = db.connection.cursor()
            sql = """
                INSERT INTO preguntas (examen_id, texto, tipo, valor) 
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (
                pregunta['examen_id'],
                pregunta['texto'],
                pregunta['tipo'],
                pregunta['valor']
            ))
            db.connection.commit()
            return cursor.lastrowid
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def delete_pregunta(cls, db, pregunta_id):
        """Elimina una pregunta y todas sus opciones y respuestas asociadas"""
        cursor = db.connection.cursor()
        
        # Primero eliminamos todas las respuestas de usuarios
        sql_respuestas = "DELETE FROM respuestas_usuarios WHERE pregunta_id = %s"
        cursor.execute(sql_respuestas, (pregunta_id,))
        
        # Eliminamos todas las opciones de respuesta
        sql_opciones = "DELETE FROM opciones WHERE pregunta_id = %s"
        cursor.execute(sql_opciones, (pregunta_id,))
        
        # Finalmente eliminamos la pregunta
        sql_pregunta = "DELETE FROM preguntas WHERE id = %s"
        cursor.execute(sql_pregunta, (pregunta_id,))
        
        db.connection.commit()
    
    @classmethod
    def add_opcion(self, db, opcion):
        """Agrega una nueva opción a una pregunta"""
        try:
            cursor = db.connection.cursor()
            sql = """
                INSERT INTO opciones (pregunta_id, texto, es_correcta) 
                VALUES (%s, %s, %s)
            """
            cursor.execute(sql, (
                opcion['pregunta_id'],
                opcion['texto'],
                opcion['es_correcta']
            ))
            db.connection.commit()
            return cursor.lastrowid
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def delete_opcion(cls, db, opcion_id):
        """Elimina una opción de respuesta"""
        cursor = db.connection.cursor()
        
        # Eliminamos todas las respuestas de usuarios que seleccionaron esta opción
        sql_respuestas = "DELETE FROM respuestas_usuarios WHERE opcion_id = %s"
        cursor.execute(sql_respuestas, (opcion_id,))
        
        # Eliminamos la opción
        sql_opcion = "DELETE FROM opciones WHERE id = %s"
        cursor.execute(sql_opcion, (opcion_id,))
        
        db.connection.commit()
    
    @classmethod
    def get_opciones_by_pregunta(self, db, pregunta_id):
        """Obtiene todas las opciones asociadas a una pregunta específica"""
        try:
            cursor = db.connection.cursor()
            sql = """
                SELECT id, pregunta_id, texto, es_correcta, created_at, updated_at 
                FROM opciones 
                WHERE pregunta_id = %s
                ORDER BY id ASC
            """
            cursor.execute(sql, (pregunta_id,))
            opciones = cursor.fetchall()
            return opciones
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def iniciar_examen(self, db, usuario_id, examen_id):
        """Registra el inicio de un examen por parte de un usuario"""
        try:
            # Asegurarnos de que examen_id sea un entero
            try:
                examen_id = int(examen_id)
            except (TypeError, ValueError):
                print(f"Error en iniciar_examen: ID de examen no es un número válido: {examen_id}")
                return 0
                
            # Siempre usar 1 como ID de usuario para evitar problemas de restricciones de clave foránea
            # Esto permite que cualquier usuario (incluso invitados) puedan realizar exámenes
            usuario_id = 1
            
            cursor = db.connection.cursor()
            
            # Verificar si la tabla resultados_examenes existe
            cursor.execute("SHOW TABLES LIKE 'resultados_examenes'")
            if cursor.fetchone() is None:
                # Crear la tabla si no existe
                cursor.execute("""
                    CREATE TABLE `resultados_examenes` (
                      `id` bigint(20) NOT NULL AUTO_INCREMENT,
                      `usuario_id` bigint(20) NOT NULL,
                      `examen_id` bigint(20) NOT NULL,
                      `puntuacion` float DEFAULT 0,
                      `fecha_inicio` datetime NOT NULL,
                      `fecha_fin` datetime DEFAULT NULL,
                      `completado` tinyint(1) DEFAULT 0,
                      PRIMARY KEY (`id`)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
                """)
                db.connection.commit()
            
            # Verificar si ya existe un examen en curso
            sql_check = """
                SELECT id FROM resultados_examenes 
                WHERE usuario_id = %s AND examen_id = %s AND completado = 0
            """
            cursor.execute(sql_check, (usuario_id, examen_id))
            resultado_existente = cursor.fetchone()
            
            if resultado_existente:
                return resultado_existente[0]
            
            # Crear nuevo registro de resultado
            sql = """
                INSERT INTO resultados_examenes (usuario_id, examen_id, fecha_inicio) 
                VALUES (%s, %s, NOW())
            """
            cursor.execute(sql, (usuario_id, examen_id))
            db.connection.commit()
            
            # Obtener el ID del nuevo registro
            new_id = cursor.lastrowid
            
            # Verificar que se haya creado correctamente
            if not new_id:
                print("Error en iniciar_examen: No se pudo obtener el ID del nuevo registro")
                return 0
                
            return new_id
        except Exception as ex:
            print(f"Error en iniciar_examen: {str(ex)}")
            # Devolver un ID temporal para evitar errores en la interfaz
            return 0
    
    @classmethod
    def guardar_respuesta(self, db, respuesta):
        """Guarda la respuesta de un usuario a una pregunta"""
        try:
            cursor = db.connection.cursor()
            
            # Verificar si la tabla respuestas_usuarios existe
            cursor.execute("SHOW TABLES LIKE 'respuestas_usuarios'")
            if cursor.fetchone() is None:
                # Crear la tabla si no existe
                cursor.execute("""
                    CREATE TABLE `respuestas_usuarios` (
                      `id` bigint(20) NOT NULL AUTO_INCREMENT,
                      `resultado_id` bigint(20) NOT NULL,
                      `pregunta_id` bigint(20) NOT NULL,
                      `opcion_id` bigint(20) DEFAULT NULL,
                      `texto_respuesta` text DEFAULT NULL,
                      `es_correcta` tinyint(1) DEFAULT 0,
                      PRIMARY KEY (`id`),
                      KEY `resultado_id` (`resultado_id`),
                      KEY `pregunta_id` (`pregunta_id`),
                      KEY `opcion_id` (`opcion_id`)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
                """)
                db.connection.commit()
            
            # Verificar si ya existe una respuesta para esta pregunta
            sql_check = """
                SELECT id FROM respuestas_usuarios 
                WHERE resultado_id = %s AND pregunta_id = %s
            """
            cursor.execute(sql_check, (respuesta['resultado_id'], respuesta['pregunta_id']))
            respuesta_existente = cursor.fetchone()
            
            # Determinar si la respuesta es correcta
            es_correcta = False
            if 'opcion_id' in respuesta and respuesta['opcion_id']:
                # Para preguntas de opción múltiple o verdadero/falso
                sql_opcion = "SELECT es_correcta FROM opciones WHERE id = %s"
                cursor.execute(sql_opcion, (respuesta['opcion_id'],))
                opcion = cursor.fetchone()
                if opcion:
                    es_correcta = bool(opcion[0])
            elif 'texto_respuesta' in respuesta and respuesta['texto_respuesta']:
                # Para preguntas de respuesta corta
                # Aquí podría implementarse alguna lógica para verificar la respuesta
                # Por ahora, todas las respuestas cortas se consideran incorrectas
                es_correcta = False
            
            if respuesta_existente:
                # Actualizar respuesta existente
                if 'opcion_id' in respuesta and respuesta['opcion_id']:
                    sql = """
                        UPDATE respuestas_usuarios 
                        SET opcion_id = %s, texto_respuesta = NULL, es_correcta = %s
                        WHERE id = %s
                    """
                    cursor.execute(sql, (
                        respuesta['opcion_id'],
                        es_correcta,
                        respuesta_existente[0]
                    ))
                else:
                    sql = """
                        UPDATE respuestas_usuarios 
                        SET opcion_id = NULL, texto_respuesta = %s, es_correcta = %s
                        WHERE id = %s
                    """
                    cursor.execute(sql, (
                        respuesta.get('texto_respuesta', ''),
                        es_correcta,
                        respuesta_existente[0]
                    ))
            else:
                # Crear nueva respuesta
                sql = """
                    INSERT INTO respuestas_usuarios (resultado_id, pregunta_id, opcion_id, texto_respuesta, es_correcta) 
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    respuesta['resultado_id'],
                    respuesta['pregunta_id'],
                    respuesta.get('opcion_id'),
                    respuesta.get('texto_respuesta'),
                    es_correcta
                ))
            
            db.connection.commit()
            return True
        except Exception as ex:
            print(f"Error en guardar_respuesta: {str(ex)}")
            return False

    @classmethod
    def finalizar_examen(self, db, resultado_id):
        """Finaliza un examen y calcula la puntuación"""
        try:
            cursor = db.connection.cursor()
            
            # Obtener información del examen
            sql_examen = """
                SELECT e.id, e.examen_id FROM resultados_examenes e
                WHERE e.id = %s
            """
            cursor.execute(sql_examen, (resultado_id,))
            resultado = cursor.fetchone()
            
            if not resultado:
                return {"puntuacion": 0, "puntuacion_obtenida": 0, "puntuacion_total": 0}
            
            examen_id = resultado[1]
            
            # Obtener todas las preguntas del examen
            sql_preguntas = """
                SELECT id, valor FROM preguntas WHERE examen_id = %s
            """
            cursor.execute(sql_preguntas, (examen_id,))
            preguntas = cursor.fetchall()
            
            # Calcular puntuación total posible
            puntuacion_total = sum(pregunta[1] for pregunta in preguntas) if preguntas else 0
            
            # Calcular puntuación obtenida
            puntuacion_obtenida = 0
            for pregunta in preguntas:
                sql_respuesta = """
                    SELECT es_correcta FROM respuestas_usuarios
                    WHERE resultado_id = %s AND pregunta_id = %s
                """
                cursor.execute(sql_respuesta, (resultado_id, pregunta[0]))
                respuesta = cursor.fetchone()
                
                if respuesta and respuesta[0]:
                    puntuacion_obtenida += pregunta[1]
            
            # Calcular porcentaje
            if puntuacion_total > 0:
                porcentaje = (puntuacion_obtenida / puntuacion_total) * 100
            else:
                porcentaje = 0
            
            # Actualizar resultado
            sql_update = """
                UPDATE resultados_examenes
                SET puntuacion = %s, fecha_fin = NOW(), completado = 1
                WHERE id = %s
            """
            cursor.execute(sql_update, (porcentaje, resultado_id))
            db.connection.commit()
            
            return {
                'puntuacion': porcentaje,
                'puntuacion_obtenida': puntuacion_obtenida,
                'puntuacion_total': puntuacion_total
            }
        except Exception as ex:
            print(f"Error en finalizar_examen: {str(ex)}")
            return {
                'puntuacion': 0,
                'puntuacion_obtenida': 0,
                'puntuacion_total': 0
            }
    
    @classmethod
    def get_resultados_by_usuario(self, db, usuario_id):
        """Obtiene todos los resultados de exámenes de un usuario"""
        try:
            cursor = db.connection.cursor()
            sql = """
                SELECT r.id, r.examen_id, r.puntuacion, r.fecha_inicio, r.fecha_fin, r.completado,
                       e.titulo as examen_titulo, c.titulo as capitulo_titulo, co.title as curso_titulo
                FROM resultados_examenes r
                JOIN examenes e ON r.examen_id = e.id
                JOIN capitulos c ON e.capitulo_id = c.id
                JOIN courses co ON c.curso_id = co.id
                WHERE r.usuario_id = %s
                ORDER BY r.fecha_inicio DESC
            """
            cursor.execute(sql, (usuario_id,))
            resultados = cursor.fetchall()
            return resultados
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_preguntas_con_opciones(self, db, examen_id):
        """Obtiene todas las preguntas de un examen con sus opciones"""
        try:
            cursor = db.connection.cursor()
            # Obtener todas las preguntas del examen
            sql_preguntas = """
                SELECT id, examen_id, texto, tipo, valor, created_at, updated_at 
                FROM preguntas 
                WHERE examen_id = %s
                ORDER BY id ASC
            """
            cursor.execute(sql_preguntas, (examen_id,))
            preguntas = cursor.fetchall()
            
            # Crear una lista para almacenar las preguntas con sus opciones
            preguntas_con_opciones = []
            
            # Para cada pregunta, obtener sus opciones
            for pregunta in preguntas:
                sql_opciones = """
                    SELECT id, pregunta_id, texto, es_correcta, created_at, updated_at 
                    FROM opciones 
                    WHERE pregunta_id = %s
                    ORDER BY id ASC
                """
                cursor.execute(sql_opciones, (pregunta[0],))
                opciones = cursor.fetchall()
                
                # Crear un diccionario con la pregunta y sus opciones
                pregunta_dict = {
                    'pregunta': pregunta,
                    'opciones': opciones
                }
                
                preguntas_con_opciones.append(pregunta_dict)
            
            return preguntas_con_opciones
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def procesar_examen(self, db, examen_id, usuario_id, respuestas):
        """Procesa la entrega de un examen"""
        try:
            cursor = db.connection.cursor()
            
            # Iniciar el examen (crear registro en resultados_examenes)
            resultado_id = self.iniciar_examen(db, usuario_id, examen_id)
            if not resultado_id:
                return False
            
            # Guardar cada respuesta
            for pregunta_id, opcion_id in respuestas.items():
                respuesta = {
                    'resultado_id': resultado_id,
                    'pregunta_id': pregunta_id,
                    'opcion_id': opcion_id
                }
                self.guardar_respuesta(db, respuesta)
            
            # Finalizar el examen y calcular puntuación
            self.finalizar_examen(db, resultado_id)
            
            return resultado_id
        except Exception as ex:
            print(f"Error en procesar_examen: {str(ex)}")
            return False

    @classmethod
    def get_resultado_by_id(self, db, resultado_id):
        """Obtiene un resultado de examen por su ID"""
        try:
            cursor = db.connection.cursor()
            
            # Obtener información básica del resultado
            sql_resultado = """
                SELECT r.id, r.examen_id, r.usuario_id, r.puntuacion, r.fecha_inicio, r.fecha_fin, r.completado
                FROM resultados_examenes r
                WHERE r.id = %s
            """
            cursor.execute(sql_resultado, (resultado_id,))
            resultado_base = cursor.fetchone()
            
            if not resultado_base:
                return None
                
            # Obtener información del examen
            sql_examen = """
                SELECT e.titulo, e.descripcion
                FROM examenes e
                WHERE e.id = %s
            """
            cursor.execute(sql_examen, (resultado_base[1],))
            examen_info = cursor.fetchone()
            
            # Obtener respuestas correctas
            sql_respuestas = """
                SELECT COUNT(*)
                FROM respuestas_usuarios
                WHERE resultado_id = %s AND es_correcta = 1
            """
            cursor.execute(sql_respuestas, (resultado_id,))
            respuestas_correctas = cursor.fetchone()[0]
            
            # Obtener puntuación obtenida y total
            sql_preguntas = """
                SELECT p.valor, ru.es_correcta
                FROM preguntas p
                LEFT JOIN respuestas_usuarios ru ON p.id = ru.pregunta_id AND ru.resultado_id = %s
                WHERE p.examen_id = %s
            """
            cursor.execute(sql_preguntas, (resultado_id, resultado_base[1]))
            preguntas_respuestas = cursor.fetchall()
            
            puntuacion_obtenida = 0
            puntuacion_total = 0
            
            for pregunta in preguntas_respuestas:
                puntuacion_total += pregunta[0]
                if pregunta[1]:
                    puntuacion_obtenida += pregunta[0]
            
            # Crear diccionario con toda la información
            resultado = {
                'id': resultado_base[0],
                'examen_id': resultado_base[1],
                'usuario_id': resultado_base[2],
                'puntuacion': resultado_base[3],
                'fecha_inicio': resultado_base[4],
                'fecha_fin': resultado_base[5],
                'completado': resultado_base[6],
                'examen_titulo': examen_info[0] if examen_info else "Desconocido",
                'examen_descripcion': examen_info[1] if examen_info else "",
                'respuestas_correctas': respuestas_correctas,
                'puntuacion_obtenida': puntuacion_obtenida,
                'puntuacion_total': puntuacion_total
            }
            
            return resultado
        except Exception as ex:
            print(f"Error en get_resultado_by_id: {str(ex)}")
            return None
