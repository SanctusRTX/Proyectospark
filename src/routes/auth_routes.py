from flask import Blueprint, render_template, request, redirect, url_for, flash
from controllers.auth_controller import AuthController

# Crear el blueprint
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        success, message = AuthController.login(username, password)
        
        if success:
            flash("Inicio de sesión exitoso", "success")
            return redirect(url_for('main.index'))
        else:
            flash(message, "danger")
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')

@auth_bp.route('/guest-login', methods=['POST'])
def guest_login():
    if request.method == 'POST':
        guest_name = request.form.get('guest_name')
        
        success, message = AuthController.guest_login(guest_name)
        
        if success:
            flash(message, "success")
            return redirect(url_for('main.index'))
        else:
            flash(message, "warning")
            return redirect(url_for('auth.login'))
    
    return redirect(url_for('auth.login'))

@auth_bp.route('/logout')
def logout():
    AuthController.logout()
    flash("Has cerrado sesión correctamente", "info")
    return redirect(url_for('main.index'))
