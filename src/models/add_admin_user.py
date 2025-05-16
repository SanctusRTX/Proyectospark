from flask import Flask
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash
import sys
import os

# Añadir la ruta del directorio padre (src) al path para poder importar config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import config

# Configuración de la aplicación
app = Flask(__name__)
app.config.from_object(config['development'])

# Inicializar MySQL
mysql = MySQL(app)

def add_admin_user(username, password):
    try:
        with app.app_context():
            # Generar hash de la contraseña
            hashed_password = generate_password_hash(password)
            
            # Crear cursor
            cursor = mysql.connection.cursor()
            
            # Verificar si el usuario ya existe
            cursor.execute("SELECT id FROM usuarios WHERE nombre_usuario = %s", (username,))
            existing_user = cursor.fetchone()
            
            if existing_user:
                # Actualizar usuario existente
                cursor.execute("""
                    UPDATE usuarios 
                    SET contraseña = %s, tipo_usuario = 'profesor' 
                    WHERE nombre_usuario = %s
                """, (hashed_password, username))
                print(f"Usuario '{username}' actualizado con éxito.")
            else:
                # Insertar nuevo usuario
                cursor.execute("""
                    INSERT INTO usuarios (nombre_usuario, contraseña, tipo_usuario) 
                    VALUES (%s, %s, 'profesor')
                """, (username, hashed_password))
                print(f"Usuario '{username}' creado con éxito.")
            
            # Confirmar cambios
            mysql.connection.commit()
            
            # Cerrar cursor
            cursor.close()
            
            return True
    except Exception as e:
        print(f"Error al crear/actualizar usuario: {e}")
        return False

if __name__ == "__main__":
    username = "sanctusrtx"
    password = "admin123"  # Puedes cambiar esto por la contraseña que prefieras
    
    if len(sys.argv) > 1:
        password = sys.argv[1]
    
    add_admin_user(username, password)
    print(f"Contraseña para '{username}': {password}")
