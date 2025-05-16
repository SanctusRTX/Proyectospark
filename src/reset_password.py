from flask import Flask
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash
import random
import string
import sys
from config import config

# Función para generar una contraseña aleatoria
def generar_password(longitud=12):
    letras = string.ascii_letters
    digitos = string.digits
    especiales = "!@#$%^&*"
    # Asegurar al menos un carácter de cada tipo
    pwd = [
        random.choice(letras.lower()),
        random.choice(letras.upper()),
        random.choice(digitos),
        random.choice(especiales)
    ]
    # Completar el resto de la contraseña
    caracteres = letras + digitos + especiales
    pwd.extend(random.choice(caracteres) for _ in range(longitud - 4))
    # Mezclar todos los caracteres
    random.shuffle(pwd)
    return ''.join(pwd)

# Función para actualizar la contraseña de un usuario específico
def reset_password(nombre_usuario=None):
    try:
        # Inicializar Flask y configurar la conexión a la base de datos
        app = Flask(__name__)
        app.config.from_object(config['development'])
        mysql = MySQL(app)
        
        # Si no se especifica un usuario, mostrar la lista de usuarios
        if nombre_usuario is None:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT id, nombre_usuario, tipo_usuario FROM usuarios")
            usuarios = cursor.fetchall()
            
            if not usuarios:
                print("No hay usuarios en la base de datos.")
                return
                
            print("\nUsuarios disponibles:")
            print("ID | Nombre de Usuario | Tipo")
            print("-" * 40)
            
            for usuario in usuarios:
                print(f"{usuario[0]} | {usuario[1]} | {usuario[2]}")
                
            print("\nUso: python reset_password.py <nombre_usuario>")
            return
        
        # Verificar si el usuario existe
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id FROM usuarios WHERE nombre_usuario = %s", (nombre_usuario,))
        usuario = cursor.fetchone()
        
        if not usuario:
            print(f"Error: El usuario '{nombre_usuario}' no existe en la base de datos.")
            return
        
        # Generar nueva contraseña
        nueva_password = generar_password()
        
        # Generar hash de la contraseña
        password_hash = generate_password_hash(nueva_password)
        
        # Actualizar la contraseña en la base de datos
        cursor.execute("UPDATE usuarios SET contraseña = %s WHERE nombre_usuario = %s", 
                      (password_hash, nombre_usuario))
        mysql.connection.commit()
        
        print(f"\n¡Contraseña actualizada exitosamente!")
        print(f"Usuario: {nombre_usuario}")
        print(f"Nueva contraseña: {nueva_password}")
        print("\nGuarde esta información en un lugar seguro.")
        
        cursor.close()
        
    except Exception as e:
        print(f"Error al actualizar la contraseña: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        reset_password()  # Mostrar lista de usuarios
    else:
        reset_password(sys.argv[1])  # Resetear contraseña del usuario especificado
