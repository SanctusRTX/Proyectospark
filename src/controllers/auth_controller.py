from flask import session, flash
from extensions.extensions import db
from models.ModelUser import ModelUser
from models.entities.User import User
import time

class AuthController:
    @staticmethod
    def login(username, password):
        """Maneja el proceso de inicio de sesión"""
        if not username or not password:
            return False, "Por favor, introduce usuario y contraseña"
            
        user = User(0, username, password, None)
        logged_user = ModelUser.login(db, user)
        
        if logged_user is not None:
            if logged_user.password:
                session['user_id'] = logged_user.id
                session['username'] = logged_user.username
                session['fullname'] = logged_user.fullname
                session['user_role'] = logged_user.role
                session['timestamp'] = int(time.time())
                return True, None
            else:
                return False, "Contraseña incorrecta"
        else:
            return False, "Usuario no encontrado"
    
    @staticmethod
    def guest_login(guest_name):
        """Maneja el inicio de sesión como invitado"""
        if guest_name:
            session['user_id'] = 0
            session['username'] = f"Invitado: {guest_name}"
            session['fullname'] = f"Invitado: {guest_name}"
            session['user_role'] = 'guest'
            session['timestamp'] = int(time.time())
            return True, f"Bienvenido, {guest_name}! Has accedido como invitado."
        else:
            return False, "Por favor, introduce tu nombre para acceder como invitado."
    
    @staticmethod
    def logout():
        """Cierra la sesión del usuario"""
        session.clear()
        return True
