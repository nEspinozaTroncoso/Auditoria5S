import os
from pathlib import Path

# --- Definiciones de Rutas Base ---
HOME_DIR = Path.home()
APP_DATA_DIR_BASE = HOME_DIR / "Auditoria_5S_Datos"  # Usamos una variable temporal aquí
UPLOAD_FOLDER_BASE = APP_DATA_DIR_BASE / "uploads"

# Rutas para DB
DB_PATH = APP_DATA_DIR_BASE / "blog-post.db"
SQLITE = f"sqlite:///{DB_PATH}"

# --- Clases de Configuración ---

POSTGRESQL = ""


class Config:
    # --- ¡ATRIBUTOS CLAVE AÑADIDOS! ---
    # Esto soluciona el AttributeError
    APP_DATA_DIR = APP_DATA_DIR_BASE
    UPLOAD_FOLDER_PATH = UPLOAD_FOLDER_BASE
    # ------------------------------------

    DEBUG = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev")

    # Rutas usadas por Flask y SQLAlchemy
    SQLALCHEMY_DATABASE_URI = SQLITE
    UPLOAD_FOLDER = str(UPLOAD_FOLDER_PATH)  # Flask necesita la ruta como string
    HOST = "127.0.0.1"
    PORT = 5000
    SERVER_NAME = "127.0.0.1:5000"
