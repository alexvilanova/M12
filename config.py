from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config:
    """Base config."""
    SECRET_KEY = environ.get('SECRET_KEY')
    SESSION_COOKIE_NAME = environ.get('SESSION_COOKIE_NAME')
    DEBUG = environ.get('DEBUG', False)

    DATABASE_TYPE = environ.get('DATABASE_TYPE')
    if DATABASE_TYPE == 'mysql':
        DB_USER = environ.get('DB_USER')
        DB_PASSWORD = environ.get('DB_PASSWORD')
        DB_HOST = environ.get('DB_HOST')
        DB_NAME = environ.get('DB_NAME')
        DB_PORT = environ.get('DB_PORT', '3306')
        SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    elif DATABASE_TYPE == 'sqlite':
        SQLALCHEMY_DATABASE_URI = "sqlite:///" + path.join(basedir, environ.get('SQLITE_FILE_RELATIVE_PATH'))
    else:
        raise ValueError("Tipo de base de datos no soportado")

    SQLALCHEMY_ECHO = environ.get('SQLALCHEMY_ECHO')
    MAIL_SUBJECT_PREFIX = environ.get('MAIL_SUBJECT_PREFIX')
    MAIL_SENDER_NAME = environ.get('MAIL_SENDER_NAME')
    MAIL_SENDER_ADDR = environ.get('MAIL_SENDER_ADDR')
    MAIL_SENDER_PASSWORD = environ.get('MAIL_SENDER_PASSWORD')
    MAIL_SMTP_SERVER = environ.get('MAIL_SMTP_SERVER')
    MAIL_SMTP_PORT = int(environ.get('MAIL_SMTP_PORT'))

    EXTERNAL_URL = environ.get('EXTERNAL_URL')
    
    LOG_LEVEL = environ.get('LOG_LEVEL', 'DEBUG').upper()
