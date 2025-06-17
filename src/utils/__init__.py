# Este archivo permite que Python reconozca la carpeta como un paquete

"""
Utilidades y herramientas para la aplicación Spark
"""

from .decorators import login_required, admin_required
from .helpers import allowed_file, generate_unique_filename
# Las utilidades de diagnóstico no se importan por defecto
# Para usarlas, importar directamente:
# from utils.check_exams import check_exams
# from utils.debug_exams import debug_exams
