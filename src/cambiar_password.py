import mysql.connector
from werkzeug.security import generate_password_hash
import random
import string

# Función para generar una contraseña aleatoria
def generar_password(longitud=10):
    caracteres = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(caracteres) for i in range(longitud))

# Función para actualizar la contraseña de un usuario
def actualizar_password(usuario, nueva_password=None):
    try:
        # Conectar a la base de datos
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="proyectox"
        )
        
        cursor = conexion.cursor()
        
        # Si no se proporciona una contraseña, generar una aleatoria
        if nueva_password is None:
            nueva_password = generar_password(12)
        
        # Generar el hash de la contraseña
        password_hash = generate_password_hash(nueva_password)
        
        # Verificar si el usuario existe
        cursor.execute("SELECT id FROM usuarios WHERE nombre_usuario = %s", (usuario,))
        resultado = cursor.fetchone()
        
        if resultado is None:
            print(f"El usuario '{usuario}' no existe en la base de datos.")
            return None
        
        # Actualizar la contraseña
        cursor.execute("UPDATE usuarios SET contraseña = %s WHERE nombre_usuario = %s", 
                      (password_hash, usuario))
        conexion.commit()
        
        print(f"Contraseña actualizada exitosamente para el usuario '{usuario}'")
        print(f"Nueva contraseña: {nueva_password}")
        
        cursor.close()
        conexion.close()
        
        return nueva_password
        
    except Exception as e:
        print(f"Error al actualizar la contraseña: {e}")
        return None

# Función para listar todos los usuarios
def listar_usuarios():
    try:
        # Conectar a la base de datos
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="proyectox"
        )
        
        cursor = conexion.cursor()
        
        # Obtener la lista de usuarios
        cursor.execute("SELECT id, nombre_usuario, tipo_usuario FROM usuarios")
        usuarios = cursor.fetchall()
        
        print("\nUsuarios disponibles:")
        print("ID | Nombre de Usuario | Tipo")
        print("-" * 40)
        
        for usuario in usuarios:
            print(f"{usuario[0]} | {usuario[1]} | {usuario[2]}")
        
        cursor.close()
        conexion.close()
        
    except Exception as e:
        print(f"Error al listar usuarios: {e}")

# Ejecutar el script
if __name__ == "__main__":
    print("Script para cambiar contraseñas de usuarios")
    print("===========================================")
    
    # Listar usuarios disponibles
    listar_usuarios()
    
    # Solicitar nombre de usuario
    usuario = input("\nIngrese el nombre de usuario para cambiar la contraseña (o presione Enter para salir): ")
    
    if usuario:
        # Preguntar si desea una contraseña aleatoria o personalizada
        opcion = input("¿Desea una contraseña aleatoria? (s/n): ").lower()
        
        if opcion == 's' or opcion == '':
            # Generar y actualizar con contraseña aleatoria
            actualizar_password(usuario)
        else:
            # Solicitar nueva contraseña
            nueva_password = input("Ingrese la nueva contraseña: ")
            if nueva_password:
                actualizar_password(usuario, nueva_password)
            else:
                print("La contraseña no puede estar vacía.")
    else:
        print("Operación cancelada.")
