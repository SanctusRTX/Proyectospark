# Guía para Desplegar Proyecto Spark en PythonAnywhere

Esta guía te ayudará a desplegar tu aplicación Flask de Spark en PythonAnywhere, un servicio de hosting especializado en aplicaciones Python.

## Paso 1: Crear una cuenta en PythonAnywhere

1. Ve a [PythonAnywhere](https://www.pythonanywhere.com) y regístrate para obtener una cuenta gratuita.
2. Una vez registrado, accede a tu dashboard.

## Paso 2: Preparar el código para el despliegue

Antes de subir el código a PythonAnywhere, asegúrate de que tu proyecto esté listo:

1. Verifica que tienes un archivo `requirements.txt` actualizado con todas las dependencias:
   ```
   Flask==2.3.3
   Werkzeug==2.3.7
   Jinja2==3.1.2
   MarkupSafe==2.1.3
   click==8.1.7
   itsdangerous==2.1.2
   blinker==1.6.2
   flask-mysqldb==1.0.1
   mysqlclient==2.2.0
   mysql-connector-python==8.1.0
   python-dotenv==1.0.0
   flask-sqlalchemy==3.1.1
   ```

2. Asegúrate de que tu estructura de archivos esté organizada correctamente.

## Paso 3: Subir el código a PythonAnywhere

Hay varias formas de subir tu código:

### Opción 1: Usar Git (recomendado)

1. Si tu código está en un repositorio Git (GitHub, GitLab, etc.):
   - En el dashboard de PythonAnywhere, abre una consola Bash.
   - Clona tu repositorio:
     ```bash
     git clone https://github.com/tu-usuario/Proyectospark.git
     ```

### Opción 2: Subir archivos manualmente

1. En el dashboard de PythonAnywhere, ve a la pestaña "Files".
2. Crea un directorio para tu proyecto:
   ```bash
   mkdir Proyectospark
   ```
3. Navega a ese directorio y sube tus archivos usando la opción "Upload a file".
4. Asegúrate de mantener la misma estructura de directorios que tienes localmente.

## Paso 4: Crear una base de datos MySQL

1. En el dashboard de PythonAnywhere, ve a la pestaña "Databases".
2. En la sección "MySQL", establece una contraseña para tu base de datos.
3. Una vez inicializada, crea una nueva base de datos:
   - En el campo "Create a new database", escribe un nombre (por ejemplo, "proyectox").
   - Haz clic en "Create".
4. Toma nota de los detalles de conexión que se muestran:
   - Nombre de usuario: tu_usuario
   - Nombre de la base de datos: tu_usuario$proyectox
   - Host: tu_usuario.mysql.pythonanywhere-services.com

## Paso 5: Configurar la base de datos

1. Abre una consola MySQL desde la pestaña "Databases".
2. Si tienes un archivo SQL con la estructura de tu base de datos:
   - Sube el archivo a PythonAnywhere
   - Importa el esquema:
     ```sql
     USE tu_usuario$proyectox;
     SOURCE ruta/al/archivo.sql;
     ```
3. Modifica el archivo `src/config.py` en tu proyecto para usar los datos de conexión de PythonAnywhere:

```python
class Config:
    SECRET_KEY = 'Tutankamon'

class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST = 'tu_usuario.mysql.pythonanywhere-services.com'
    MYSQL_USER = 'tu_usuario'
    MYSQL_PASSWORD = 'tu_contraseña_mysql'
    MYSQL_DB = 'tu_usuario$proyectox'

config = {
    'development': DevelopmentConfig
}
```

## Paso 6: Configurar el entorno virtual

1. En el dashboard de PythonAnywhere, abre una consola Bash.
2. Crea un entorno virtual:
   ```bash
   mkvirtualenv --python=python3.10 spark_env
   ```
3. Activa el entorno virtual:
   ```bash
   workon spark_env
   ```
4. Instala las dependencias:
   ```bash
   cd ~/Proyectospark
   pip install -r requirements.txt
   ```

## Paso 7: Configurar la aplicación web

1. En el dashboard de PythonAnywhere, ve a la pestaña "Web".
2. Haz clic en "Add a new web app".
3. Selecciona tu dominio (será username.pythonanywhere.com para cuentas gratuitas).
4. En la página de selección de framework, elige "Manual Configuration".
5. Selecciona la versión de Python que estás utilizando (Python 3.10).
6. En la sección "Virtualenv", ingresa la ruta a tu entorno virtual:
   ```
   /home/tu_usuario/.virtualenvs/spark_env
   ```
7. En la sección "Code", establece la ruta a tu código:
   ```
   /home/tu_usuario/Proyectospark
   ```

## Paso 8: Configurar el archivo WSGI

1. Haz clic en el enlace al archivo WSGI en la pestaña "Web".
2. Reemplaza el contenido con lo siguiente:

```python
import sys
import os

# Añadir la ruta del proyecto al path de Python
path = '/home/tu_usuario/Proyectospark'
if path not in sys.path:
    sys.path.append(path)

# Añadir la ruta del directorio src al path de Python
src_path = os.path.join(path, 'src')
if src_path not in sys.path:
    sys.path.append(src_path)

# Cambiar al directorio src
os.chdir(src_path)

# Importar la aplicación Flask
from app import create_app

# Crear la aplicación con la configuración de desarrollo
application = create_app('development')
```

## Paso 9: Configurar archivos estáticos

1. En la pestaña "Web", en la sección "Static files", añade:
   - URL: /static/
   - Path: /home/tu_usuario/Proyectospark/src/static/

## Paso 10: Inicializar la base de datos

1. Abre una consola Bash.
2. Activa tu entorno virtual:
   ```bash
   workon spark_env
   ```
3. Navega al directorio src:
   ```bash
   cd ~/Proyectospark/src
   ```
4. Inicia una sesión de Python:
   ```bash
   python
   ```
5. Ejecuta el siguiente código para inicializar la base de datos:
   ```python
   from app import create_app
   from extensions.extensions import db, init_db
   
   app = create_app('development')
   with app.app_context():
       init_db()
   ```

## Paso 11: Reiniciar la aplicación web

1. En la pestaña "Web", haz clic en el botón "Reload" para reiniciar tu aplicación.
2. Espera unos segundos y luego visita tu sitio en tu_usuario.pythonanywhere.com.

## Solución de problemas comunes

### Error de importación de módulos
- Verifica que la ruta en el archivo WSGI sea correcta.
- Asegúrate de que todos los módulos necesarios estén instalados en tu entorno virtual.
- Comprueba los logs de error en la pestaña "Web" para ver mensajes específicos.

### Error de conexión a la base de datos
- Verifica que los datos de conexión en `config.py` sean correctos.
- Asegúrate de que la base de datos exista y tenga las tablas necesarias.
- Comprueba que el usuario tenga permisos para acceder a la base de datos.

### Error 500
- Revisa los logs de error en la pestaña "Web" para identificar el problema específico.
- Verifica que todas las dependencias estén instaladas correctamente.

### Archivos estáticos no se cargan
- Verifica que la configuración de archivos estáticos sea correcta.
- Asegúrate de que las rutas en tus plantillas HTML usen `url_for('static', filename='...')`.

### Problemas con el archivo WSGI
- Asegúrate de que la ruta al archivo `app.py` sea correcta.
- Verifica que la función `create_app()` esté siendo llamada correctamente.

## Mantenimiento

- Tu aplicación gratuita en PythonAnywhere se desactivará después de 3 meses de inactividad. Para mantenerla activa, inicia sesión y haz clic en "Extend" en la pestaña "Web".
- Para actualizar tu aplicación después de hacer cambios:
  1. Si usas Git, haz un pull de los cambios.
  2. Si subiste manualmente, actualiza los archivos necesarios.
  3. Haz clic en "Reload" en la pestaña "Web".

¡Listo! Tu aplicación Spark debería estar funcionando correctamente en PythonAnywhere. 