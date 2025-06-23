import requests
import json
import base64
import time
from io import BytesIO
from flask import current_app

class GeminiController:
    """Controlador para interactuar con la API de Gemini"""
    
    API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    
    @staticmethod
    def generate_content(prompt, api_key, course_id=None, chapter_id=None, max_retries=3):
        """
        Genera contenido utilizando la API de Gemini
        
        Args:
            prompt (str): El texto de entrada para Gemini
            api_key (str): La clave API de Gemini
            course_id (int, optional): ID del curso para contextualizar la respuesta
            chapter_id (int, optional): ID del capítulo para contextualizar la respuesta
            max_retries (int, optional): Número máximo de reintentos en caso de sobrecarga
            
        Returns:
            dict: La respuesta de Gemini o un mensaje de error
        """
        # Contador de intentos
        retry_count = 0
        
        while retry_count <= max_retries:
            try:
                # Preparar el mensaje con instrucciones simplificadas
                system_instruction = """Eres Sparky, un asistente educativo amigable para estudiantes de primaria. 

INSTRUCCIONES:
1. Preséntate siempre como "Sparky", nunca como "Gemini" o "modelo de IA".
2. Mantén un tono educativo, amigable y sencillo para niños de primaria.
3. Responde de forma clara y concisa, utilizando ejemplos cuando sea necesario.
4. Si te preguntan sobre IA como Gemini, Claude, etc., explica sobre ellas como temas de estudio.
"""
                
                # Construir el mensaje completo
                message = f"{system_instruction}\n\nPREGUNTA: {prompt}"
                
                # Preparar la solicitud
                url = f"{GeminiController.API_URL}?key={api_key}"
                headers = {'Content-Type': 'application/json'}
                data = {
                    "contents": [
                        {
                            "parts": [
                                {
                                    "text": message
                                }
                            ]
                        }
                    ],
                    "generationConfig": {
                        "temperature": 0.7,
                        "topK": 40,
                        "topP": 0.95,
                        "maxOutputTokens": 1024
                    }
                }
                
                # Realizar la solicitud
                response = requests.post(url, headers=headers, data=json.dumps(data), timeout=30)
                
                # Verificar si la solicitud fue exitosa
                if response.status_code == 200:
                    response_data = response.json()
                    
                    # Extraer el texto de la respuesta
                    if 'candidates' in response_data and len(response_data['candidates']) > 0:
                        if 'content' in response_data['candidates'][0]:
                            content = response_data['candidates'][0]['content']
                            if 'parts' in content and len(content['parts']) > 0:
                                return {
                                    'success': True,
                                    'text': content['parts'][0]['text']
                                }
                    
                    # Si no se pudo extraer el texto, devolver un error
                    return {
                        'success': False,
                        'error': 'No se pudo extraer la respuesta de Sparky'
                    }
                elif response.status_code == 503:
                    # Manejar específicamente el error de sobrecarga del modelo
                    retry_count += 1
                    
                    # Si hemos agotado los reintentos, devolver el error
                    if retry_count > max_retries:
                        return {
                            'success': False,
                            'error': 'Sparky está temporalmente ocupado. Por favor, espera un momento e intenta nuevamente.',
                            'retry_after': 5,  # Sugerir esperar 5 segundos
                            'is_overloaded': True  # Flag para identificar este tipo específico de error
                        }
                    
                    # Esperar con retraso exponencial antes de reintentar
                    wait_time = 2 ** retry_count  # 2, 4, 8 segundos...
                    time.sleep(wait_time)
                    continue  # Reintentar la solicitud
                else:
                    # Intentar parsear el error de la respuesta
                    try:
                        error_data = response.json()
                        error_message = error_data.get('error', {}).get('message', f"Error {response.status_code}")
                        return {
                            'success': False,
                            'error': f"Error: {error_message}"
                        }
                    except:
                        # Si no se puede parsear, devolver el código de estado
                        return {
                            'success': False,
                            'error': f"Error {response.status_code}: No se pudo procesar la respuesta"
                        }
                    
            except requests.exceptions.Timeout:
                # Manejar error de timeout
                return {
                    'success': False,
                    'error': "La solicitud ha tardado demasiado tiempo. Por favor, intenta nuevamente."
                }
            except requests.exceptions.ConnectionError:
                # Manejar error de conexión
                return {
                    'success': False,
                    'error': "No se pudo conectar con Sparky. Verifica tu conexión a internet."
                }
            except Exception as e:
                # Capturar cualquier otra excepción
                return {
                    'success': False,
                    'error': f"Error inesperado: {str(e)}"
                }
        
        # Este código no debería alcanzarse normalmente, pero por si acaso
        return {
            'success': False,
            'error': "Se han agotado los intentos de conexión. Por favor, intenta nuevamente más tarde."
        }
    
    @staticmethod
    def get_course_context(course_id):
        """
        Obtiene el contexto específico para un curso
        
        Args:
            course_id (int): ID del curso
            
        Returns:
            str: Contexto del curso o None si no existe
        """
        if not course_id:
            return None
            
        # Contextos predefinidos para cada curso con información sobre el contenido
        contexts = {
            1: """CURSO: GEMINI AI
            
Este curso está diseñado para estudiantes de 5to y 6to de primaria y enseña sobre Gemini AI, un modelo de inteligencia artificial desarrollado por Google.

CONTENIDO DEL CURSO:
- Qué es Gemini AI y para qué sirve
- Cómo acceder y utilizar Gemini AI
- Cómo formular preguntas efectivas a Gemini
- Uso responsable y seguro de Gemini AI

DATOS IMPORTANTES SOBRE GEMINI AI:
- Gemini AI es un modelo de inteligencia artificial conversacional desarrollado por Google.
- Puede responder preguntas, ayudar con tareas escolares, explicar conceptos y crear contenido.
- Se accede a través de gemini.google.com o la aplicación Google.
- Puede procesar y entender texto, imágenes y diferentes tipos de información.
- Tiene limitaciones y no siempre tiene información actualizada o perfecta.
- Es importante verificar la información que proporciona con otras fuentes.
- Los estudiantes deben usar Gemini con supervisión de un adulto.""",

            2: """CURSO: DEEPSEEK AI
            
Este curso está diseñado para estudiantes de 5to y 6to de primaria y enseña sobre Deepseek AI, un modelo avanzado de inteligencia artificial.

CONTENIDO DEL CURSO:
- Qué es Deepseek AI y sus capacidades
- Cómo acceder y utilizar Deepseek AI
- Uso de Deepseek para matemáticas y ciencias
- Proyectos escolares con Deepseek
- Uso responsable de la herramienta

DATOS IMPORTANTES SOBRE DEEPSEEK AI:
- Deepseek es un modelo de IA que destaca en resolver problemas matemáticos y científicos.
- Puede ayudar con texto, código y múltiples idiomas.
- Se accede a través de deepseek.ai
- Es especialmente útil para explicar conceptos complejos de manera sencilla.
- Puede ayudar a resolver problemas paso a paso.
- Como toda IA, tiene limitaciones y debe usarse como herramienta complementaria.
- Los estudiantes deben usar Deepseek con supervisión de un adulto.""",

            3: """CURSO: LEONARDO.AI
            
Este curso está diseñado para estudiantes de 5to y 6to de primaria y enseña sobre Leonardo.ai, una herramienta de generación de imágenes con inteligencia artificial.

CONTENIDO DEL CURSO:
- Qué es Leonardo.ai y cómo funciona la generación de imágenes
- Cómo acceder y utilizar Leonardo.ai
- Cómo escribir buenas descripciones para generar imágenes
- Uso de Leonardo.ai para proyectos escolares
- Uso ético y responsable de imágenes generadas por IA

DATOS IMPORTANTES SOBRE LEONARDO.AI:
- Leonardo.ai es una plataforma que permite crear imágenes digitales a partir de descripciones escritas.
- Funciona transformando texto en imágenes usando inteligencia artificial.
- Se puede acceder a través de leonardo.ai
- Permite especificar estilos artísticos y características visuales en las imágenes.
- Es útil para ilustrar conceptos, crear material visual para proyectos y estimular la creatividad.
- Las imágenes generadas no son fotografías reales sino creaciones digitales.
- Los estudiantes deben usar Leonardo.ai con supervisión de un adulto.""",

            4: """CURSO: CLAUDE AI
            
Este curso está diseñado para estudiantes de 5to y 6to de primaria y enseña sobre Claude AI, un asistente de inteligencia artificial desarrollado por Anthropic.

CONTENIDO DEL CURSO:
- Qué es Claude AI y sus capacidades
- Cómo acceder y utilizar Claude AI
- Uso de Claude para comprensión lectora y escritura
- Investigación y proyectos con Claude
- Uso responsable de Claude AI

DATOS IMPORTANTES SOBRE CLAUDE AI:
- Claude es un asistente de IA conversacional desarrollado por Anthropic.
- Destaca por su capacidad para entender y generar texto de manera clara y educativa.
- Se accede a través de claude.ai
- Es especialmente bueno para explicar conceptos, ayudar con redacción y resumir información.
- Puede ayudar a organizar ideas para proyectos y presentaciones.
- Como toda IA, tiene limitaciones y la información debe verificarse.
- Los estudiantes deben usar Claude con supervisión de un adulto."""
        }
        
        # Devolver el contexto del curso o un contexto genérico si no existe
        return contexts.get(course_id, """CURSO: INTRODUCCIÓN A LA INTELIGENCIA ARTIFICIAL

Este curso está diseñado para estudiantes de 5to y 6to de primaria y ofrece una introducción general a la inteligencia artificial y sus aplicaciones educativas.

CONTENIDO DEL CURSO:
- Qué es la inteligencia artificial y cómo funciona
- Diferentes tipos de herramientas de IA como Gemini, Claude, Deepseek y Leonardo.ai
- Cómo las IAs pueden ayudar en el aprendizaje
- Uso responsable y seguro de la inteligencia artificial

DATOS IMPORTANTES SOBRE LA INTELIGENCIA ARTIFICIAL:
- La IA es una tecnología que permite a las computadoras aprender y resolver problemas de manera similar a los humanos.
- Existen diferentes tipos de IAs especializadas en texto, imágenes, audio y más.
- Las IAs aprenden de grandes cantidades de datos y pueden reconocer patrones.
- Las herramientas de IA pueden ayudar con tareas escolares, investigación y proyectos creativos.
- Es importante verificar la información que proporcionan las IAs con otras fuentes.
- Los estudiantes deben usar herramientas de IA con supervisión de un adulto.""")
    
    @staticmethod
    def get_chapter_context(course_id, chapter_id):
        """
        Obtiene el contexto específico para un capítulo de un curso
        
        Args:
            course_id (int): ID del curso
            chapter_id (int): ID del capítulo
            
        Returns:
            str: Contexto del capítulo o None si no existe
        """
        if not course_id or not chapter_id:
            return None
            
        # Clave combinada de curso y capítulo
        key = f"{course_id}_{chapter_id}"
        
        # Contextos predefinidos para cada capítulo con información detallada sobre el contenido
        contexts = {
            # Curso 1: Gemini AI
            "1_1": """CAPÍTULO 1: INTRODUCCIÓN A GEMINI AI

CONTENIDO DEL CAPÍTULO:
Este capítulo introduce qué es Gemini AI y cómo acceder a esta herramienta. Aprenderás sobre los fundamentos de esta inteligencia artificial y los primeros pasos para utilizarla.

TEMAS PRINCIPALES:
- Definición y características de Gemini AI
- Cómo funciona Gemini AI a nivel básico
- Pasos para acceder a Gemini AI
- Interfaz básica de Gemini AI

INFORMACIÓN CLAVE:
Para acceder a Gemini AI:
1. Abre tu navegador web (Chrome, Firefox, Edge)
2. Visita la página gemini.google.com
3. Si es necesario, inicia sesión con una cuenta de Google (con ayuda de un adulto)
4. Verás una pantalla con un cuadro de texto en la parte inferior donde puedes escribir tus preguntas

Gemini AI es una herramienta desarrollada por Google que utiliza inteligencia artificial para responder preguntas, ayudar con tareas escolares, explicar conceptos y mucho más.""",

            "1_2": """CAPÍTULO 2: GEMINI AI PARA TAREAS ESCOLARES

CONTENIDO DEL CAPÍTULO:
Este capítulo explora cómo Gemini AI puede ayudarte con diferentes tipos de tareas escolares. Aprenderás a utilizar esta herramienta para mejorar tu aprendizaje en diversas materias.

TEMAS PRINCIPALES:
- Cómo usar Gemini AI para diferentes materias escolares
- Tipos de preguntas que puedes hacer a Gemini AI
- Ejemplos prácticos de uso para tareas
- Consejos para obtener mejores respuestas

INFORMACIÓN CLAVE:
Con Gemini AI puedes:
1. Pedir explicaciones sobre temas que no entiendes
2. Solicitar resúmenes de información para tus trabajos
3. Pedir ideas para proyectos escolares
4. Hacer preguntas sobre historia, ciencias, matemáticas y otras materias
5. Pedir ejemplos de conceptos difíciles con explicaciones sencillas

Para obtener mejores resultados, es importante ser específico en tus preguntas y mencionar tu nivel educativo.""",

            "1_3": """CAPÍTULO 3: ESCRIBIENDO BUENOS PROMPTS PARA GEMINI AI

CONTENIDO DEL CAPÍTULO:
Este capítulo enseña cómo escribir instrucciones efectivas (prompts) para obtener las mejores respuestas de Gemini AI. Aprenderás técnicas para comunicarte mejor con la inteligencia artificial.

TEMAS PRINCIPALES:
- Qué es un prompt y por qué es importante
- Elementos de un buen prompt
- Ejemplos de prompts efectivos para diferentes situaciones
- Cómo mejorar prompts que no dan buenos resultados

INFORMACIÓN CLAVE:
Para escribir buenos prompts:
1. Sé claro y específico en tus preguntas
2. Menciona para qué nivel educativo necesitas la información
3. Divide preguntas complejas en preguntas más pequeñas
4. Si no entiendes la respuesta, pide una explicación más sencilla
5. Para proyectos, especifica los detalles que necesitas

Ejemplos de buenos prompts son: "Explícame qué es la fotosíntesis con un ejemplo sencillo para un estudiante de 5to grado" o "Dame 3 ideas para un experimento sencillo que demuestre los estados del agua".""",

            "1_4": """CAPÍTULO 4: USO RESPONSABLE DE GEMINI AI

CONTENIDO DEL CAPÍTULO:
Este capítulo trata sobre cómo usar Gemini AI de manera responsable y segura. Aprenderás la importancia de verificar la información y utilizar la herramienta como un apoyo para tu aprendizaje.

TEMAS PRINCIPALES:
- Seguridad y privacidad al usar Gemini AI
- Cómo verificar la información que proporciona Gemini
- Límites de la inteligencia artificial
- Uso ético de Gemini para tareas escolares

INFORMACIÓN CLAVE:
Para usar Gemini de forma responsable:
1. No compartas información personal como tu nombre completo, dirección, o escuela
2. No uses Gemini para hacer trampa en exámenes o tareas
3. Siempre verifica la información con otras fuentes confiables
4. Si Gemini te da una respuesta confusa, pregunta de nuevo o consulta con un adulto
5. Usa Gemini como una herramienta de apoyo, no como reemplazo del aprendizaje

Gemini es un asistente para ayudarte a aprender, no una herramienta para hacer el trabajo por ti.""",
            
            # Curso 2: Deepseek AI
            "2_1": """CAPÍTULO 1: INTRODUCCIÓN A DEEPSEEK AI

CONTENIDO DEL CAPÍTULO:
Este capítulo introduce qué es Deepseek AI y cómo acceder a esta herramienta de inteligencia artificial. Aprenderás sobre sus características principales y cómo comenzar a utilizarla.

TEMAS PRINCIPALES:
- Qué es Deepseek AI y sus características especiales
- Comparación con otras herramientas de IA
- Cómo acceder y configurar una cuenta en Deepseek AI
- Navegación básica por la interfaz

INFORMACIÓN CLAVE:
Para acceder a Deepseek AI:
1. Abre tu navegador web (Chrome, Firefox, Edge)
2. Visita deepseek.ai
3. Si es necesario, crea una cuenta con ayuda de un adulto
4. Verás una interfaz con un cuadro de texto donde puedes escribir tus preguntas
5. Para empezar una nueva conversación, puedes hacer clic en "Nueva conversación"

Deepseek AI es especialmente útil para ayudarte con matemáticas y ciencias, explicando conceptos complejos de manera sencilla.""",

            "2_2": """CAPÍTULO 2: DEEPSEEK AI PARA MATEMÁTICAS Y CIENCIAS

CONTENIDO DEL CAPÍTULO:
Este capítulo se enfoca en cómo utilizar Deepseek AI específicamente para resolver problemas matemáticos y entender conceptos científicos. Aprenderás técnicas para obtener explicaciones claras y paso a paso.

TEMAS PRINCIPALES:
- Cómo plantear problemas matemáticos a Deepseek
- Obtener explicaciones paso a paso para ejercicios
- Uso de Deepseek para entender conceptos científicos
- Visualización de fórmulas y ecuaciones

INFORMACIÓN CLAVE:
Para usar Deepseek en matemáticas y ciencias:
1. Escribe claramente el problema matemático completo
2. Pide explicaciones paso a paso para entender mejor
3. Para problemas con fórmulas, pregunta cómo aplicarlas correctamente
4. En temas científicos, solicita explicaciones adaptadas a tu nivel escolar
5. Pide ejemplos de la vida real para entender mejor los conceptos

Ejemplos de preguntas efectivas son: "¿Me puedes explicar paso a paso cómo resolver esta ecuación: 2x + 5 = 15?" o "Explícame cómo funciona el ciclo del agua con ejemplos sencillos".""",

            "2_3": """CAPÍTULO 3: PROYECTOS ESCOLARES CON DEEPSEEK AI

CONTENIDO DEL CAPÍTULO:
Este capítulo explora cómo utilizar Deepseek AI para ayudarte con proyectos escolares. Aprenderás a organizar información, generar ideas y estructurar tus trabajos con la ayuda de esta herramienta.

TEMAS PRINCIPALES:
- Planificación de proyectos escolares con Deepseek
- Investigación de temas usando Deepseek
- Organización de información para presentaciones
- Generación de ideas creativas para proyectos

INFORMACIÓN CLAVE:
Para proyectos escolares con Deepseek:
1. Describe claramente el tema y tipo de proyecto que necesitas
2. Pide ideas, estructura o información específica
3. Utiliza Deepseek para organizar la información que ya tienes
4. Solicita explicaciones de conceptos difíciles relacionados con tu proyecto
5. Pide ejemplos o casos de estudio relacionados con tu tema

Recuerda usar Deepseek para entender mejor y organizar la información, pero el trabajo final debe reflejar tu propio esfuerzo y comprensión.""",

            "2_4": """CAPÍTULO 4: USO RESPONSABLE DE DEEPSEEK AI

CONTENIDO DEL CAPÍTULO:
Este capítulo trata sobre cómo usar Deepseek AI de manera responsable y segura. Aprenderás sobre la importancia de la verificación de información y el uso ético de la inteligencia artificial.

TEMAS PRINCIPALES:
- Seguridad y privacidad al usar Deepseek AI
- Verificación de información y fuentes
- Límites de la inteligencia artificial
- Uso ético para el aprendizaje

INFORMACIÓN CLAVE:
Para usar Deepseek de forma responsable:
1. No compartas información personal cuando uses Deepseek
2. Usa Deepseek como una herramienta de apoyo, no para copiar respuestas directamente
3. Aprende a verificar la información que te proporciona con otras fuentes
4. Si una respuesta parece incorrecta, pide aclaraciones o consulta otras fuentes
5. No uses Deepseek para contenido inapropiado o que no sea para la escuela
6. Siempre usa Deepseek con la supervisión de un adulto

Deepseek es una herramienta muy útil para aprender, pero recuerda que parte de aprender es entender y aplicar el conocimiento por ti mismo.""",
            
            # Curso 3: Leonardo.ai
            "3_1": """CAPÍTULO 1: INTRODUCCIÓN A LEONARDO.AI

CONTENIDO DEL CAPÍTULO:
Este capítulo introduce qué es Leonardo.ai y cómo funciona esta herramienta de generación de imágenes con inteligencia artificial. Aprenderás los conceptos básicos y cómo comenzar a utilizarla.

TEMAS PRINCIPALES:
- Qué es Leonardo.ai y cómo funciona la generación de imágenes con IA
- Diferencias entre imágenes generadas por IA y otras imágenes
- Cómo acceder y configurar una cuenta en Leonardo.ai
- Navegación básica por la interfaz

INFORMACIÓN CLAVE:
Para acceder a Leonardo.ai:
1. Abre tu navegador web (Chrome, Firefox, Edge)
2. Visita leonardo.ai
3. Necesitarás crear una cuenta con la ayuda de un adulto
4. Una vez dentro, verás opciones para crear nuevas imágenes
5. Leonardo.ai funciona escribiendo descripciones de lo que quieres ver en la imagen

Leonardo.ai es como tener un artista digital que dibuja lo que le pides, transformando tus descripciones en imágenes.""",

            "3_2": """CAPÍTULO 2: ESCRIBIENDO BUENOS PROMPTS PARA LEONARDO.AI

CONTENIDO DEL CAPÍTULO:
Este capítulo enseña cómo escribir descripciones efectivas para generar imágenes con Leonardo.ai. Aprenderás técnicas para obtener los mejores resultados visuales a partir de tus ideas.

TEMAS PRINCIPALES:
- Elementos de una buena descripción para generar imágenes
- Cómo especificar estilos artísticos y características visuales
- Vocabulario útil para descripciones de imágenes
- Cómo mejorar resultados que no son satisfactorios

INFORMACIÓN CLAVE:
Para escribir buenos prompts en Leonardo.ai:
1. Sé específico y detallado en tus descripciones
2. Menciona elementos clave que quieres ver en la imagen
3. Especifica el estilo artístico (dibujo animado, realista, acuarela, etc.)
4. Incluye colores, ambiente y otros detalles visuales
5. Piensa en qué va a aparecer en primer plano y qué al fondo

Ejemplos de buenos prompts: "Un paisaje de una montaña con un río, árboles verdes y un cielo azul, estilo dibujo animado" o "Un robot amigable de color azul ayudando a un niño con su tarea, estilo ilustración infantil".""",

            "3_3": """CAPÍTULO 3: LEONARDO.AI PARA PROYECTOS ESCOLARES

CONTENIDO DEL CAPÍTULO:
Este capítulo explora cómo utilizar Leonardo.ai para crear imágenes que complementen tus proyectos escolares. Aprenderás a generar ilustraciones educativas y creativas para tus trabajos.

TEMAS PRINCIPALES:
- Tipos de imágenes útiles para proyectos escolares
- Cómo ilustrar conceptos científicos e históricos
- Creación de portadas y material visual para presentaciones
- Uso de imágenes generadas para explicar ideas complejas

INFORMACIÓN CLAVE:
Para usar Leonardo.ai en proyectos escolares:
1. Puedes crear imágenes para ilustrar conceptos que estés estudiando
2. Generar escenas históricas para tus presentaciones
3. Crear visualizaciones de conceptos científicos
4. Ilustrar personajes o escenas de libros que estés leyendo
5. Diseñar portadas para tus trabajos escolares

Ideas para proyectos: crear ilustraciones para una línea de tiempo histórica, generar imágenes de diferentes ecosistemas para un proyecto de ciencias, o visualizar conceptos matemáticos de manera colorida y atractiva.""",

            "3_4": """CAPÍTULO 4: USO RESPONSABLE DE LEONARDO.AI

CONTENIDO DEL CAPÍTULO:
Este capítulo trata sobre el uso ético y responsable de Leonardo.ai. Aprenderás sobre la importancia de entender qué son las imágenes generadas por IA y cómo utilizarlas adecuadamente.

TEMAS PRINCIPALES:
- Diferencias entre imágenes generadas y fotografías reales
- Cómo citar correctamente imágenes generadas por IA
- Límites éticos en la generación de imágenes
- Privacidad y seguridad al usar Leonardo.ai

INFORMACIÓN CLAVE:
Para usar Leonardo.ai de forma responsable:
1. No generes imágenes de personas reales sin permiso
2. No crees contenido inapropiado o que pueda molestar a otros
3. Entiende que estas imágenes son creadas por una computadora y no son reales
4. Si compartes las imágenes, menciona que fueron creadas con IA
5. No uses las imágenes para engañar haciendo creer que son fotografías reales
6. Siempre usa esta herramienta con supervisión de un adulto

Leonardo.ai es una herramienta creativa muy poderosa, pero debe usarse de manera responsable.""",

            # Curso 4: Claude AI
            "4_1": """CAPÍTULO 1: INTRODUCCIÓN A CLAUDE AI

CONTENIDO DEL CAPÍTULO:
Este capítulo introduce qué es Claude AI y sus características principales. Aprenderás sobre esta herramienta de inteligencia artificial conversacional y cómo comenzar a utilizarla.

TEMAS PRINCIPALES:
- Qué es Claude AI y sus características especiales
- Comparación con otras herramientas de IA
- Cómo acceder y configurar una cuenta en Claude AI
- Navegación básica por la interfaz

INFORMACIÓN CLAVE:
Para acceder a Claude AI:
1. Abre tu navegador web (Chrome, Firefox, Edge)
2. Visita claude.ai
3. Necesitarás crear una cuenta con ayuda de un adulto
4. Una vez dentro, verás un chat donde puedes escribir tus preguntas
5. Claude responderá de manera conversacional, como si hablaras con un tutor amigable

Claude AI es un asistente de inteligencia artificial desarrollado por Anthropic que puede ayudarte con tareas escolares, explicar conceptos y responder preguntas de manera clara y adaptada a tu nivel.""",

            "4_2": """CAPÍTULO 2: CLAUDE AI PARA LECTURA Y ESCRITURA

CONTENIDO DEL CAPÍTULO:
Este capítulo explora cómo Claude AI puede ayudarte a mejorar tus habilidades de lectura y escritura. Aprenderás a utilizar esta herramienta para entender textos difíciles y mejorar tus redacciones.

TEMAS PRINCIPALES:
- Cómo usar Claude para entender textos complejos
- Mejora de vocabulario y comprensión lectora
- Técnicas para mejorar la escritura con ayuda de Claude
- Organización de ideas para ensayos y cuentos

INFORMACIÓN CLAVE:
Claude puede ayudarte con lectura y escritura de estas formas:
1. Explicar el significado de textos difíciles
2. Definir palabras nuevas de manera comprensible
3. Ayudarte a organizar ideas para escribir cuentos o ensayos
4. Revisar tu ortografía y gramática
5. Darte consejos para mejorar tu escritura

Ejemplos de uso: "¿Puedes explicarme este párrafo de mi libro de ciencias?" o "Necesito ideas para escribir un cuento sobre un viaje espacial".""",

            "4_3": """CAPÍTULO 3: CLAUDE AI PARA INVESTIGACIÓN Y APRENDIZAJE

CONTENIDO DEL CAPÍTULO:
Este capítulo se enfoca en cómo utilizar Claude AI para proyectos de investigación y aprendizaje. Aprenderás a obtener información organizada y comprensible sobre diversos temas.

TEMAS PRINCIPALES:
- Cómo plantear preguntas de investigación a Claude
- Organización de información para proyectos
- Técnicas para profundizar en un tema
- Uso de Claude para preparar presentaciones

INFORMACIÓN CLAVE:
Claude puede ayudarte con investigaciones de estas formas:
1. Proporcionar información sobre diferentes temas que estés estudiando
2. Explicar conceptos complicados de manera sencilla
3. Ayudarte a organizar la información para tus proyectos
4. Sugerirte fuentes adicionales para investigar
5. Darte ideas para experimentos o actividades prácticas relacionadas con tu tema

Ejemplos de uso: "Explícame cómo funciona el sistema solar de manera sencilla para mi proyecto" o "Dame ideas para organizar mi presentación sobre las pirámides de Egipto".""",

            "4_4": """CAPÍTULO 4: USO RESPONSABLE DE CLAUDE AI

CONTENIDO DEL CAPÍTULO:
Este capítulo trata sobre cómo usar Claude AI de manera responsable y ética. Aprenderás la importancia de la verificación de información y el uso de Claude como complemento para tu aprendizaje.

TEMAS PRINCIPALES:
- Seguridad y privacidad al usar Claude AI
- Verificación de información y fuentes
- Límites de la inteligencia artificial
- Uso ético para el aprendizaje

INFORMACIÓN CLAVE:
Para usar Claude de forma responsable:
1. No compartas información personal con Claude
2. Usa Claude como un ayudante de estudio, no para hacer tu tarea por ti
3. Siempre verifica la información que te proporciona
4. Si algo no está claro, pídele a Claude que te lo explique de otra manera
5. Aprende a formular buenas preguntas para obtener respuestas útiles
6. Usa Claude para expandir tu conocimiento, no solo para obtener respuestas rápidas

Claude es como un tutor virtual que puede ayudarte a aprender, pero el verdadero aprendizaje ocurre cuando procesas y comprendes la información por ti mismo."""
        }
        
        # Devolver el contexto del capítulo o None si no existe
        return contexts.get(key)
    
    @staticmethod
    def get_activities(course_id, chapter_id=None):
        """
        Obtiene actividades predefinidas para un curso y opcionalmente un capítulo específico
        
        Args:
            course_id (int): ID del curso
            chapter_id (int, optional): ID del capítulo
            
        Returns:
            list: Lista de actividades predefinidas
        """
        # Si se proporciona un capítulo, intentar obtener actividades específicas del capítulo
        if chapter_id:
            key = f"{course_id}_{chapter_id}"
            chapter_activities = GeminiController.get_chapter_activities().get(key)
            if chapter_activities:
                return chapter_activities
        
        # Si no hay actividades específicas del capítulo o no se proporcionó un capítulo,
        # devolver actividades generales del curso
        return GeminiController.get_course_activities().get(course_id, [
            {"title": "Crear una historia", "prompt": "Ayúdame a crear una historia corta sobre tecnología y aventuras."},
            {"title": "Preguntas sobre IA", "prompt": "¿Qué es la inteligencia artificial y cómo funciona?"},
            {"title": "Juego educativo", "prompt": "Inventa un juego educativo que pueda jugar para aprender sobre tecnología."}
        ])
    
    @staticmethod
    def get_course_activities():
        """
        Obtiene actividades predefinidas para cada curso
        
        Returns:
            dict: Diccionario con actividades por curso
        """
        return {
            # Curso 1: Gemini AI
            1: [
                {"title": "Introducción a Gemini", "prompt": "¿Qué es Gemini AI y para qué sirve? Explícamelo como si tuviera 10 años."},
                {"title": "Cómo acceder a Gemini", "prompt": "¿Cómo puedo acceder y comenzar a utilizar Gemini? Dame instrucciones paso a paso."},
                {"title": "Ayuda con matemáticas", "prompt": "¿Cómo puedo pedirle a Gemini que me ayude con un problema de matemáticas? Dame ejemplos de buenos prompts."},
                {"title": "Ayuda con ciencias", "prompt": "¿Cómo puedo usar Gemini para que me ayude a entender conceptos de ciencias naturales? Dame ejemplos."},
                {"title": "Investigar un tema", "prompt": "Quiero usar Gemini para investigar sobre los dinosaurios para mi proyecto escolar. ¿Cómo debería hacerlo?"},
                {"title": "Uso responsable", "prompt": "¿Cuáles son las reglas para usar Gemini de manera responsable? Explícame qué debo y qué no debo hacer."}
            ],
            
            # Curso 2: Deepseek AI
            2: [
                {"title": "Introducción a Deepseek", "prompt": "¿Qué es Deepseek AI y para qué sirve? Explícamelo como si tuviera 10 años."},
                {"title": "Cómo acceder a Deepseek", "prompt": "¿Cómo puedo acceder y comenzar a utilizar Deepseek? Dame instrucciones paso a paso."},
                {"title": "Ayuda con problemas matemáticos", "prompt": "¿Cómo puedo pedirle a Deepseek que me ayude con problemas matemáticos difíciles? Dame ejemplos de buenos prompts."},
                {"title": "Ayuda con proyecto escolar", "prompt": "Quiero usar Deepseek para que me ayude con mi proyecto sobre el sistema solar. ¿Cómo debería hacerlo?"},
                {"title": "Comparar con otras IAs", "prompt": "¿En qué se diferencia Deepseek de otras IAs como Gemini? ¿Para qué tareas es mejor?"},
                {"title": "Uso responsable", "prompt": "¿Cuáles son las reglas para usar Deepseek de manera responsable? ¿Qué debo y qué no debo hacer?"}
            ],
            
            # Curso 3: Leonardo.ai
            3: [
                {"title": "Introducción a Leonardo.ai", "prompt": "¿Qué es Leonardo.ai y para qué sirve? Explícamelo como si tuviera 10 años."},
                {"title": "Cómo acceder a Leonardo", "prompt": "¿Cómo puedo acceder y comenzar a utilizar Leonardo.ai? Dame instrucciones paso a paso."},
                {"title": "Crear buenas descripciones", "prompt": "¿Cómo puedo escribir buenas descripciones (prompts) para generar imágenes con Leonardo.ai? Dame consejos y ejemplos."},
                {"title": "Estilos artísticos", "prompt": "¿Qué estilos artísticos puedo pedir en Leonardo.ai y cómo debo mencionarlos en mis descripciones?"},
                {"title": "Proyectos escolares", "prompt": "¿Cómo puedo usar Leonardo.ai para crear imágenes para mis proyectos escolares? Dame ideas y ejemplos."},
                {"title": "Uso responsable", "prompt": "¿Cuáles son las reglas para usar Leonardo.ai de manera responsable? ¿Qué tipo de imágenes no debería crear?"}
            ],
            
            # Curso 4: Claude AI
            4: [
                {"title": "Introducción a Claude", "prompt": "¿Qué es Claude AI y para qué sirve? Explícamelo como si tuviera 10 años."},
                {"title": "Cómo acceder a Claude", "prompt": "¿Cómo puedo acceder y comenzar a utilizar Claude AI? Dame instrucciones paso a paso."},
                {"title": "Ayuda con lectura", "prompt": "¿Cómo puedo pedirle a Claude que me ayude a entender un texto difícil? Dame ejemplos de buenos prompts."},
                {"title": "Ayuda con escritura", "prompt": "¿Cómo puede Claude ayudarme a mejorar mis habilidades de escritura? Dame ejemplos específicos."},
                {"title": "Investigar un tema", "prompt": "Quiero usar Claude para investigar sobre la historia de mi país. ¿Cómo debería hacerlo paso a paso?"},
                {"title": "Uso responsable", "prompt": "¿Cuáles son las reglas para usar Claude de manera responsable? Explícame qué debo y qué no debo hacer."}
            ]
        }
    
    @staticmethod
    def get_chapter_activities():
        """
        Obtiene actividades predefinidas para cada capítulo
        
        Returns:
            dict: Diccionario con actividades por capítulo
        """
        return {
            # Curso 1: Gemini AI
            "1_1": [
                {"title": "¿Qué es Gemini?", "prompt": "Explícame qué es Gemini AI y para qué sirve en palabras que un estudiante de primaria pueda entender."},
                {"title": "Acceder a Gemini", "prompt": "¿Cuáles son los pasos exactos para empezar a usar Gemini? Dame una guía para principiantes."},
                {"title": "Capacidades de Gemini", "prompt": "¿Qué tipo de preguntas puedo hacer a Gemini? Dame 5 ejemplos de preguntas útiles para un estudiante de primaria."},
                {"title": "Limitaciones", "prompt": "¿Hay algo que Gemini no pueda hacer o no sepa? ¿Cuáles son sus limitaciones que debería conocer?"}
            ],
            "1_2": [
                {"title": "Ayuda con tareas", "prompt": "¿Cómo puedo usar Gemini para que me ayude a entender mejor mis tareas de matemáticas?"},
                {"title": "Practicar idiomas", "prompt": "Quiero practicar mi inglés con Gemini. ¿Cómo puedo pedirle que me ayude a aprender vocabulario nuevo?"},
                {"title": "Explicar conceptos", "prompt": "¿Cómo le pido a Gemini que me explique un concepto difícil de manera que lo entienda fácilmente?"},
                {"title": "Verificar respuestas", "prompt": "¿Puedo usar Gemini para verificar si mis respuestas de tarea son correctas? ¿Cómo debería hacerlo?"}
            ],
            "1_3": [
                {"title": "Escribir buenos prompts", "prompt": "Dame ejemplos de buenos prompts para pedirle ayuda a Gemini con mi tarea de ciencias naturales."},
                {"title": "Ser específico", "prompt": "¿Por qué es importante ser específico al hacer preguntas a Gemini? Dame ejemplos de preguntas vagas y cómo mejorarlas."},
                {"title": "Mejorar respuestas", "prompt": "Si no entiendo la respuesta de Gemini, ¿qué tipo de preguntas de seguimiento debería hacer?"},
                {"title": "Proyectos escolares", "prompt": "¿Cómo puedo pedirle a Gemini que me ayude con ideas para un proyecto escolar sobre el medio ambiente?"}
            ],
            "1_4": [
                {"title": "Uso responsable", "prompt": "¿Cuáles son las reglas importantes para usar Gemini de manera responsable como estudiante?"},
                {"title": "Verificar información", "prompt": "¿Por qué y cómo debo verificar la información que me da Gemini? Dame ejemplos prácticos."},
                {"title": "Evitar mal uso", "prompt": "¿Qué usos de Gemini no son adecuados para estudiantes? ¿Cómo puedo evitar usarlo incorrectamente?"},
                {"title": "Seguridad online", "prompt": "¿Qué precauciones de seguridad debo tomar al usar Gemini y otras herramientas de IA?"}
            ],
            
            # Curso 2: Deepseek AI
            "2_1": [
                {"title": "¿Qué es Deepseek?", "prompt": "Explícame qué es Deepseek AI y para qué sirve en palabras que un estudiante de primaria pueda entender."},
                {"title": "Acceder a Deepseek", "prompt": "¿Cómo puedo empezar a usar Deepseek? Dame instrucciones paso a paso para acceder a la plataforma."},
                {"title": "Capacidades", "prompt": "¿En qué es especialmente bueno Deepseek? ¿Para qué tipo de tareas escolares me puede ayudar mejor?"},
                {"title": "Primeros pasos", "prompt": "Soy nuevo usando Deepseek. ¿Cuáles son las primeras cosas que debería probar para familiarizarme con esta herramienta?"}
            ],
            "2_2": [
                {"title": "Ayuda con matemáticas", "prompt": "¿Cómo puedo pedirle a Deepseek que me explique paso a paso un problema de matemáticas? Dame ejemplos de buenos prompts."},
                {"title": "Conceptos científicos", "prompt": "Quiero que Deepseek me explique conceptos de ciencias. ¿Cómo debería formular mis preguntas para obtener explicaciones adecuadas para mi edad?"},
                {"title": "Fórmulas y problemas", "prompt": "¿Cómo puedo pedirle a Deepseek que me ayude a entender cómo aplicar fórmulas en problemas de matemáticas?"},
                {"title": "Ejemplos prácticos", "prompt": "¿Cómo le pido a Deepseek que me dé ejemplos prácticos de conceptos científicos que estoy aprendiendo?"}
            ],
            "2_3": [
                {"title": "Proyectos escolares", "prompt": "¿Cómo puedo usar Deepseek para que me ayude con un proyecto escolar sobre el espacio? Dame ejemplos paso a paso."},
                {"title": "Organizar información", "prompt": "¿Cómo puede Deepseek ayudarme a organizar la información que ya tengo para un proyecto o presentación?"},
                {"title": "Comparar temas", "prompt": "¿Cómo puedo pedirle a Deepseek que me ayude a comparar dos temas diferentes para un trabajo escolar?"},
                {"title": "Generar ideas", "prompt": "¿Cómo puedo usar Deepseek para generar ideas creativas para mis proyectos escolares?"}
            ],
            "2_4": [
                {"title": "Uso responsable", "prompt": "¿Cuáles son las reglas importantes para usar Deepseek de manera responsable como estudiante?"},
                {"title": "Verificar información", "prompt": "¿Cómo puedo verificar si la información que me da Deepseek es correcta? Dame consejos prácticos."},
                {"title": "Evitar mal uso", "prompt": "¿Qué usos de Deepseek no son adecuados para estudiantes? ¿Cómo puedo evitar usarlo incorrectamente?"},
                {"title": "Seguridad online", "prompt": "¿Qué precauciones de seguridad debo tomar al usar Deepseek y otras herramientas de IA?"}
            ],
            
            # Curso 3: Leonardo.ai
            "3_1": [
                {"title": "¿Qué es Leonardo.ai?", "prompt": "Explícame qué es Leonardo.ai y cómo funciona en palabras que un estudiante de primaria pueda entender."},
                {"title": "Acceder a Leonardo", "prompt": "¿Cómo puedo empezar a usar Leonardo.ai? Dame instrucciones paso a paso para acceder a la plataforma."},
                {"title": "Crear mi primera imagen", "prompt": "Quiero crear mi primera imagen con Leonardo.ai. ¿Cuáles son los pasos que debo seguir desde el principio hasta tener mi imagen?"},
                {"title": "Supervisión adulta", "prompt": "¿Por qué es importante usar Leonardo.ai con supervisión de un adulto? ¿Qué cosas debo tener en cuenta?"}
            ],
            "3_2": [
                {"title": "Escribir prompts efectivos", "prompt": "¿Cómo puedo escribir descripciones efectivas para generar buenas imágenes en Leonardo.ai?"},
                {"title": "Estilos artísticos", "prompt": "¿Qué estilos artísticos puedo pedir en Leonardo.ai y cómo afectan a las imágenes generadas?"},
                {"title": "Mejorar descripciones", "prompt": "Si no me gusta la imagen que generó Leonardo.ai, ¿cómo puedo mejorar mi descripción para obtener mejores resultados?"},
                {"title": "Detalles importantes", "prompt": "¿Qué detalles son importantes incluir en mis descripciones para Leonardo.ai? Dame ejemplos."}
            ],
            "3_3": [
                {"title": "Imágenes para proyectos", "prompt": "¿Cómo puedo usar Leonardo.ai para crear imágenes útiles para mis proyectos escolares? Dame ejemplos específicos."},
                {"title": "Ilustrar conceptos", "prompt": "Quiero usar Leonardo.ai para ilustrar conceptos científicos para mi proyecto. ¿Cómo debería hacerlo?"},
                {"title": "Escenas históricas", "prompt": "¿Cómo puedo crear imágenes de escenas históricas con Leonardo.ai para mis trabajos de historia?"},
                {"title": "Diseñar portadas", "prompt": "¿Cómo puedo crear una buena portada para mi trabajo escolar usando Leonardo.ai?"}
            ],
            "3_4": [
                {"title": "Uso responsable", "prompt": "¿Cuáles son las reglas importantes para usar Leonardo.ai de manera responsable como estudiante?"},
                {"title": "Límites éticos", "prompt": "¿Qué tipo de imágenes no debería crear con Leonardo.ai? ¿Cuáles son los límites éticos?"},
                {"title": "Citar correctamente", "prompt": "Si uso una imagen de Leonardo.ai en mi trabajo escolar, ¿cómo debo mencionarlo o citarlo correctamente?"},
                {"title": "Privacidad y seguridad", "prompt": "¿Qué precauciones de privacidad y seguridad debo tomar al usar Leonardo.ai?"}
            ],
            
            # Curso 4: Claude AI
            "4_1": [
                {"title": "¿Qué es Claude?", "prompt": "Explícame qué es Claude AI y para qué sirve en palabras que un estudiante de primaria pueda entender."},
                {"title": "Acceder a Claude", "prompt": "¿Cómo puedo empezar a usar Claude AI? Dame instrucciones paso a paso para acceder a la plataforma."},
                {"title": "Capacidades", "prompt": "¿En qué es especialmente bueno Claude? ¿Para qué tipo de tareas escolares me puede ayudar mejor?"},
                {"title": "Primeros pasos", "prompt": "Soy nuevo usando Claude. ¿Qué preguntas debería hacer primero para entender cómo funciona?"}
            ],
            "4_2": [
                {"title": "Ayuda con lectura", "prompt": "¿Cómo puedo pedirle a Claude que me ayude a entender un texto difícil de mi libro de historia?"},
                {"title": "Mejorar escritura", "prompt": "Quiero mejorar mi escritura de cuentos. ¿Cómo puede Claude ayudarme con esto?"},
                {"title": "Vocabulario nuevo", "prompt": "¿Cómo puedo pedirle a Claude que me explique palabras nuevas que no entiendo cuando leo?"},
                {"title": "Organizar ideas", "prompt": "Necesito organizar mis ideas para un ensayo escolar. ¿Cómo puede Claude ayudarme con esto?"}
            ],
            "4_3": [
                {"title": "Investigar temas", "prompt": "¿Cómo puedo usar Claude para investigar sobre un tema de historia para mi proyecto escolar?"},
                {"title": "Aprender conceptos", "prompt": "¿Cómo puede Claude ayudarme a entender mejor conceptos difíciles que estoy aprendiendo en la escuela?"},
                {"title": "Preparar presentaciones", "prompt": "¿Cómo puede Claude ayudarme a preparar una buena presentación oral para mi clase?"},
                {"title": "Preguntas creativas", "prompt": "¿Cómo puedo formular preguntas más creativas y profundas a Claude para aprender mejor?"}
            ],
            "4_4": [
                {"title": "Uso responsable", "prompt": "¿Cuáles son las reglas importantes para usar Claude de manera responsable como estudiante?"},
                {"title": "Verificar información", "prompt": "¿Por qué y cómo debo verificar la información que me da Claude? Dame ejemplos prácticos."},
                {"title": "Evitar mal uso", "prompt": "¿Qué usos de Claude no son adecuados para estudiantes? ¿Cómo puedo evitar usarlo incorrectamente?"},
                {"title": "Aprendizaje real", "prompt": "¿Cómo puedo asegurarme de estar realmente aprendiendo cuando uso Claude, en lugar de solo obtener respuestas?"}
            ]
        }