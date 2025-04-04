from .entities.User import User


class ModelUser():

    @classmethod
    def login(self, db, user):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT id, nombre_usuario, contraseña, tipo_usuario FROM usuarios 
                    WHERE nombre_usuario = '{}'""".format(user.username)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                # Determinar el rol basado en tipo_usuario
                role = "profesor" if row[3] == 'profesor' else "user"
                # Verificar la contraseña
                if User.check_password(row[2], user.password):
                    user = User(row[0], row[1], True, row[1], role)
                    return user
                else:
                    user = User(row[0], row[1], False, row[1], role)
                    return user
            else:
                return None
        except Exception as ex:
            print(f"Error en login: {ex}")
            return None

    @classmethod
    def get_by_id(self, db, id):
        try:
            # Si es un invitado (id=0), devolvemos un usuario especial
            if id == 0:
                return User(0, "Invitado", None, "Invitado", "guest")
                
            cursor = db.connection.cursor()
            sql = "SELECT id, nombre_usuario, tipo_usuario FROM usuarios WHERE id = {}".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                # Determinar el rol basado en tipo_usuario
                role = "profesor" if row[2] == 'profesor' else "user"
                return User(row[0], row[1], None, row[1], role)
            else:
                return None
        except Exception as ex:
            print(f"Error en get_by_id: {ex}")
            return None
