from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_principal import Principal
from .helper_mail import MailManager

db_manager = SQLAlchemy()
login_manager = LoginManager()
principal_manager = Principal()
mail_manager = MailManager()

def create_app():
    # Construct the core app object
    app = Flask(__name__)

    # Llegeixo la configuració del config.py de l'arrel
    app.config.from_object('config.Config')

    # Inicialitza els plugins
    login_manager.init_app(app)
    db_manager.init_app(app)
    principal_manager.init_app(app)
    mail_manager.init_app(app)
    
    with app.app_context():
        from . import commands, routes_main, routes_auth, routes_admin, routes_products, routes_category, routes_status

        # Registra els blueprints
        app.register_blueprint(routes_main.main_bp)
        app.register_blueprint(routes_auth.auth_bp)
        app.register_blueprint(routes_admin.admin_bp)
        app.register_blueprint(routes_products.products_bp)
        app.register_blueprint(routes_category.category_bp)
        app.register_blueprint(routes_status.status_bp)
        
        # Registra comandes
        app.cli.add_command(commands.db_cli)

    app.logger.info("Aplicació iniciada")

    return app