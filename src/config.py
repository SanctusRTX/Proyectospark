class Config:
    SECRET_KEY = 'Tutankamon'


class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'proyectox'


config = {
    'development': DevelopmentConfig
}
