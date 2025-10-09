import os
from pathlib import Path

# --- Definiciones de Rutas Persistentes ---

# 1. Encuentra el directorio base del usuario (e.g., C:\Users\nombre\)
HOME_DIR = Path.home()

# 2. Define una carpeta central para guardar TODOS los datos de la aplicación
#    Usamos una ubicación común como 'Documentos' o el Home Dir para accesibilidad.
APP_DATA_DIR = HOME_DIR / "Auditoria_5S_Datos"

# 3. Rutas específicas para DB y Archivos Subidos
#    La DB y la carpeta de uploads se crean dentro de esta carpeta de datos.
DB_PATH = APP_DATA_DIR / "blog-post.db"
SQLITE = f"sqlite:///{DB_PATH}"

UPLOAD_FOLDER_PATH = APP_DATA_DIR / "uploads"

# --- Clases de Configuración ---

# POSTGRESQL (Se mantiene vacío si no se usa)
POSTGRESQL = ""


class Config:
    DEBUG = False  # Cambiar a False para el ejecutable final
    SECRET_KEY = os.environ.get(
        "SECRET_KEY", "dev"
    )  # Usar variable de entorno o fallback

    # Rutas para SQLAlchemy y UPLOAD_FOLDER
    SQLALCHEMY_DATABASE_URI = SQLITE
    UPLOAD_FOLDER = str(UPLOAD_FOLDER_PATH)  # Convertir a string para Flask

    # Necesitas que tu aplicación CREE estas carpetas al inicio (ver paso 2)
