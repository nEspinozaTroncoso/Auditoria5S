import os  # Necesitas esto para crear directorios
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Importa tu clase de configuración para acceder a las rutas
from config import Config  # Asumo que tu config.py está en el directorio superior

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # Carga la configuración (que ya apunta a las rutas externas)
    app.config.from_object("config.Config")
    db.init_app(app)

    # --- LÓGICA DE CREACIÓN DE CARPETAS PERSISTENTES ---
    # La ruta APP_DATA_DIR y UPLOAD_FOLDER deben estar definidas en tu config.py

    # 1. Crea el directorio base de datos (e.g., C:\Users\...\Auditoria_5S_Datos)
    #    Usamos os.makedirs y exist_ok=True para que no falle si ya existe.
    os.makedirs(Config.APP_DATA_DIR, exist_ok=True)

    # 2. Crea la carpeta específica de uploads (e.g., ...\Auditoria_5S_Datos\uploads)
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
    # ----------------------------------------------------

    from Registros5s import home, registro, exportar, admin

    app.register_blueprint(home.bp)
    app.register_blueprint(registro.bp)
    app.register_blueprint(exportar.bp)
    app.register_blueprint(admin.bp)

    from .models import Auditoria, Respuesta

    with app.app_context():
        # Esto crea la DB en la ruta externa si no existe (la ruta fue definida en config.py)
        db.create_all()

    return app
