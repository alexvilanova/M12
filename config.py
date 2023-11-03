"""Flask App configuration."""
import os
from os import environ, path
from dotenv import load_dotenv

# ruta absoluta dde la carpeta
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

# General Config
class Config:
    ENVIRONMENT = environ.get("ENVIRONMENT")
    FLASK_APP = environ.get("FLASK_APP")
    FLASK_DEBUG = environ.get("FLASK_DEBUG")
    SECRET_KEY = environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + basedir  + "/" + environ.get("DATABASE_NAME")
    SQLALCHEMY_ECHO = environ.get("SQLALCHEMY_ECHO")

    UPLOADS_FOLDER = basedir + environ.get("UPLOADS_FOLDER")
    ALLOWED_EXTENSIONS= environ.get("ALLOWED_EXTENSIONS")
