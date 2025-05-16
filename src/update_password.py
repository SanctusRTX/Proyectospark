from flask_mysqldb import MySQL
from flask import Flask
from config import config
from models.entities.User import User
import sys

app = Flask(__name__)
app.config.from_object(config['development'])
db = MySQL(app)

def update_user_password(username, new_password):
    try:
        # Generar hash de la nueva contraseña
        hashed_password = User.generate_password(new_password)
        
        cursor = db.connection.cursor()
        
        # Verificar si el usuario existe
        sql_check = "SELECT id FROM usuarios WHERE nombre_usuario = %s"
        cursor.execute(sql_check, (username,))
        user = cursor.fetchone()
        
        if not user:
            print(f"Error: El usuario '{username}' no existe en la base de datos.")
            return False
            
        # Actualizar la contraseña
        sql_update = "UPDATE usuarios SET contraseña = %s WHERE nombre_usuario = %s"
        cursor.execute(sql_update, (hashed_password, username))
        db.connection.commit()
        
        print(f"Contraseña actualizada exitosamente para el usuario '{username}'")
        return True
        
    except Exception as ex:
        print(f"Error al actualizar la contraseña: {ex}")
        return False

def list_users():
    try:
        cursor = db.connection.cursor()
        cursor.execute("SELECT id, nombre_usuario, tipo_usuario FROM usuarios")
        users = cursor.fetchall()
        
        if not users:
            print("No hay usuarios en la base de datos.")
            return
            
        print("\nUsuarios disponibles:")
        print("ID | Nombre de Usuario | Tipo")
        print("-" * 40)
        for user in users:
            print(f"{user[0]} | {user[1]} | {user[2]}")
            
    except Exception as ex:
        print(f"Error al listar usuarios: {ex}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python update_password.py [list|update]")
        print("  - list: Muestra la lista de usuarios disponibles")
        print("  - update <username> <new_password>: Actualiza la contraseña del usuario especificado")
        sys.exit(1)
        
    command = sys.argv[1]
    
    if command == "list":
        list_users()
    elif command == "update" and len(sys.argv) == 4:
        username = sys.argv[2]
        new_password = sys.argv[3]
        update_user_password(username, new_password)
    else:
        print("Comando no válido o faltan argumentos.")
        print("Uso: python update_password.py [list|update]")
        print("  - list: Muestra la lista de usuarios disponibles")
        print("  - update <username> <new_password>: Actualiza la contraseña del usuario especificado")
