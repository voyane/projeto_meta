#Cria a aplicação Flask

import secrets
from flask import Flask, abort, jsonify, request, session
from flask_login import current_user
from config import Config
from .extensions import db, login_manager, migrate, mail
from .admin.routes import admin


def get_csrf_token():
    token = session.get("_csrf_token")

    if not token:
        token = secrets.token_urlsafe(32)
        session["_csrf_token"] = token

    return token


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

    @app.before_request
    def protect_csrf():
        if app.config.get("TESTING"):
            return None

        if request.method not in ("POST", "PUT", "PATCH", "DELETE"):
            return None

        json_data = request.get_json(silent=True) or {}
        sent_token = (
            request.headers.get("X-CSRFToken")
            or request.form.get("csrf_token")
            or json_data.get("csrf_token")
        )

        if not sent_token or sent_token != session.get("_csrf_token"):
            if request.is_json or request.path.startswith("/api/"):
                return jsonify({
                    "success": False,
                    "message": (
                        "Sessão expirada. Atualize a página e tente novamente."
                    )
                }), 400

            abort(400)

        return None

    @app.context_processor
    def inject_globals():
        pending_orders_count = 0

        try:
            if current_user.is_authenticated and current_user.is_admin:
                pending_orders_count = models.Pedido.query.filter(
                    models.Pedido.status.in_([
                        "aguardando_comprovativo",
                        "comprovativo_enviado",
                        "em_contacto"
                    ])
                ).count()
        except Exception:
            pending_orders_count = 0

        return {
            "csrf_token": get_csrf_token,
            "pending_orders_count": pending_orders_count
        }

    # registrar rotas
    from .routes import main
    app.register_blueprint(main)
    app.register_blueprint(cart_bp)
    app.register_blueprint(admin)

    return app
