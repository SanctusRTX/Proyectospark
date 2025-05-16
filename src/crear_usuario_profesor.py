from flask import Flask
from flask_mysqldb import MySQL
from config import config
import sys

app = Flask(__name__)
app.config.from_object(config['development'])
mysql = MySQL(app)

def ejecutar_sql():
    try:
        with app.app_context():
            cursor = mysql.connection.cursor()
            
            # Mostrar usuarios actuales
            print("Usuarios actuales:")
            cursor.execute("SELECT id, nombre_usuario, tipo_usuario FROM usuarios")
            usuarios = cursor.fetchall()
            for usuario in usuarios:
                print(f"ID: {usuario[0]}, Usuario: {usuario[1]}, Tipo: {usuario[2]}")
            
            # Crear nuevo usuario profesor
            nuevo_usuario = "admin_profesor"
            nueva_password = "Admin2025!"
            
            # Verificar si el usuario ya existe
            cursor.execute("SELECT id FROM usuarios WHERE nombre_usuario = %s", (nuevo_usuario,))
            usuario_existente = cursor.fetchone()
            
            if usuario_existente:
                # Si existe, actualizar contraseña
                cursor.execute("UPDATE usuarios SET contraseña = %s WHERE nombre_usuario = %s", 
                            (nueva_password, nuevo_usuario))
                print(f"\nUsuario '{nuevo_usuario}' actualizado con nueva contraseña.")
            else:
                # Si no existe, crear nuevo usuario
                cursor.execute("""
                    INSERT INTO usuarios (nombre_usuario, contraseña, tipo_usuario) 
                    VALUES (%s, %s, %s)
                """, (nuevo_usuario, nueva_password, 'profesor'))
                print(f"\nNuevo usuario profesor creado:")
                print(f"Usuario: {nuevo_usuario}")
                print(f"Contraseña: {nueva_password}")
            
            mysql.connection.commit()
            cursor.close()
            
            print("\nOperación completada exitosamente.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    ejecutar_sql()
