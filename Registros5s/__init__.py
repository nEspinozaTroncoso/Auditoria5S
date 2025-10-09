import os
from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config.from_object("config.Config")
    db.init_app(app)

    # --- LÓGICA DE CREACIÓN DE CARPETAS PERSISTENTES ---

    # 1. Crea el directorio base (ej: .../Auditoria_5S_Datos)
    os.makedirs(Config.APP_DATA_DIR, exist_ok=True)

    # 2. Crea la carpeta específica de uploads (ej: .../Auditoria_5S_Datos/uploads)
    #    CORRECCIÓN: Se usa Config.UPLOAD_FOLDER_PATH (que es el objeto Path)
    os.makedirs(Config.UPLOAD_FOLDER_PATH, exist_ok=True)  # <--- ¡ESTE ES EL CAMBIO!
    # ----------------------------------------------------
    app.add_url_rule(
        "/user_uploads/<path:filename>",  # URL que verá el navegador (ej: /user_uploads/imagen.jpg)
        endpoint="user_uploads_route",  # Nombre interno para url_for
        view_func=lambda filename: send_from_directory(
            app.config["UPLOAD_FOLDER"], filename  # La ruta EXTERNA de tu disco duro
        ),
    )
    from Registros5s import home, registro, exportar, admin

    app.register_blueprint(home.bp)
    app.register_blueprint(registro.bp)
    app.register_blueprint(exportar.bp)
    app.register_blueprint(admin.bp)

    from .models import Auditoria, Respuesta

    with app.app_context():
        db.create_all()

    return app
