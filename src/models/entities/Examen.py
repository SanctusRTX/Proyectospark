class Examen():
    def __init__(self, id, capitulo_id, titulo, descripcion=None, tiempo_limite=0, created_at=None, updated_at=None):
        self.id = id
        self.capitulo_id = capitulo_id
        self.titulo = titulo
        self.descripcion = descripcion
        self.tiempo_limite = tiempo_limite
        self.created_at = created_at
        self.updated_at = updated_at

class Pregunta():
    def __init__(self, id, examen_id, texto, tipo='opcion_multiple', valor=1, created_at=None, updated_at=None):
        self.id = id
        self.examen_id = examen_id
        self.texto = texto
        self.tipo = tipo
        self.valor = valor
        self.created_at = created_at
        self.updated_at = updated_at

class Opcion():
    def __init__(self, id, pregunta_id, texto, es_correcta=False, created_at=None, updated_at=None):
        self.id = id
        self.pregunta_id = pregunta_id
        self.texto = texto
        self.es_correcta = es_correcta
        self.created_at = created_at
        self.updated_at = updated_at

class ResultadoExamen():
    def __init__(self, id, usuario_id, examen_id, puntuacion=0, fecha_inicio=None, fecha_fin=None, completado=False, created_at=None, updated_at=None):
        self.id = id
        self.usuario_id = usuario_id
        self.examen_id = examen_id
        self.puntuacion = puntuacion
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.completado = completado
        self.created_at = created_at
        self.updated_at = updated_at
