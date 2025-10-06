from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config.from_object("config.Config")
    db.init_app(app)

    from Registros5s import home, registro, exportar

    app.register_blueprint(home.bp)
    app.register_blueprint(registro.bp)
    app.register_blueprint(exportar.bp)

    from .models import Auditoria, Respuesta

    with app.app_context():
        db.create_all()

    return app
