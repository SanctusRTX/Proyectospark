from flask import Flask, render_template, request, redirect,url_for,flash
from flask_mysqldb import MySQL
from config import config
from models.ModelUser import ModelUser
from models.entities.User import User


app = Flask(__name__)

app.config.from_object('config.Config')

db = MySQL(app)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])    
def login():
    if request.method == 'POST':
        user = User(0, request.form['username'], request.form['password'])
        logged_user = ModelUser.login(db,user)
        if logged_user != None:
            if logged_user.password:
                return redirect(url_for('home'))
            else:
                flash('Contraseña incorrecta...')
                return render_template('auth/login.html')             
        else:
            flash('usuario no encontrado...')
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')
    
@app.route('/home')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()