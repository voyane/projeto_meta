#Cria a aplicação Flask

from flask import Flask
from config import Config
from .extensions import db, login_manager, migrate, mail


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # mensagens do login
    login_manager.login_message = "Faça login para acessar esta página."
    login_manager.login_view = "main.login"

    # iniciar extensões
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    from . import models
    from .routes import main, cart_bp

    # registrar rotas
    from .routes import main
    app.register_blueprint(main)
    app.register_blueprint(cart_bp)

    return app

