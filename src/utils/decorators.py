from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    """Decorador para verificar si el usuario ha iniciado sesión"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Por favor inicia sesión para acceder', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorador para verificar si el usuario tiene permisos de administrador"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or 'user_role' not in session or session['user_role'] != 'profesor':
            flash('Acceso denegado. Se requieren permisos de profesor.', 'danger')
            return redirect(url_for('main.home'))
        return f(*args, **kwargs)
    return decorated_function
