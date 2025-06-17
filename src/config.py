import os
import secrets

class Config:
    # Generar una clave secreta aleatoria cada vez que se inicia la aplicación
    SECRET_KEY = secrets.token_hex(32)


class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'proyectox'


config = {
    'development': DevelopmentConfig
}
