from werkzeug.security import check_password_hash, generate_password_hash

class User():

    def __init__(self, id, username, password, fullname="", role="user") -> None:
        self.id = id
        self.username = username
        self.password = password
        self.fullname = fullname
        self.role = role
        
    @classmethod
    def check_password(cls, hashed_password, password):
        # Si las contraseñas están almacenadas en texto plano en la base de datos
        if hashed_password == password:
            return True
        # Intenta verificar con hash si no coincide en texto plano
        try:
            return check_password_hash(hashed_password, password)
        except:
            return False
    
    def is_admin(self):
        return self.role == 'admin'
    
    @classmethod
    def generate_password(cls, password):
        return generate_password_hash(password)
