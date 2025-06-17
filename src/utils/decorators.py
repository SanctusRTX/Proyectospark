from functools import wraps
from flask import session, redirect, url_for, flash
import time

def login_required(f):
    """Decorador para verificar si el usuario ha iniciado sesión y si la sesión es válida"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Verificar si el usuario ha iniciado sesión
        if 'user_id' not in session:
            flash('Por favor inicia sesión para acceder', 'warning')
            return redirect(url_for('auth.login'))
        
        # Verificar si la sesión tiene una marca de tiempo
        if 'timestamp' not in session:
            session.clear()
            flash('Tu sesión ha caducado. Por favor, inicia sesión nuevamente.', 'warning')
            return redirect(url_for('auth.login'))
        
        # Verificar si la sesión ha expirado (1 hora = 3600 segundos)
        current_time = int(time.time())
        session_age = current_time - session['timestamp']
        if session_age > 3600:
            session.clear()
            flash('Tu sesión ha expirado por inactividad. Por favor, inicia sesión nuevamente.', 'warning')
            return redirect(url_for('auth.login'))
        
        # Actualizar la marca de tiempo para extender la sesión
        session['timestamp'] = current_time
        
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorador para verificar si el usuario tiene permisos de administrador"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Verificar si el usuario ha iniciado sesión
        if 'user_id' not in session:
            flash('Por favor inicia sesión para acceder', 'warning')
            return redirect(url_for('auth.login'))
            
        # Verificar si la sesión tiene una marca de tiempo
        if 'timestamp' not in session:
            session.clear()
            flash('Tu sesión ha caducado. Por favor, inicia sesión nuevamente.', 'warning')
            return redirect(url_for('auth.login'))
        
        # Verificar si la sesión ha expirado (1 hora = 3600 segundos)
        current_time = int(time.time())
        session_age = current_time - session['timestamp']
        if session_age > 3600:
            session.clear()
            flash('Tu sesión ha expirado por inactividad. Por favor, inicia sesión nuevamente.', 'warning')
            return redirect(url_for('auth.login'))
        
        # Verificar si el usuario tiene permisos de administrador
        if 'user_role' not in session or session['user_role'] != 'profesor':
            flash('Acceso denegado. Se requieren permisos de profesor.', 'danger')
            return redirect(url_for('main.home'))
        
        # Actualizar la marca de tiempo para extender la sesión
        session['timestamp'] = current_time
        
        return f(*args, **kwargs)
    return decorated_function
