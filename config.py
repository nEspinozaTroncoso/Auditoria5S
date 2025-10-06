SQLITE = "sqlite:///blog-post.db"
POSTGRESQL = ""


class Config:
    DEBUG = True
    SECRET_KEY = "dev"
    SQLALCHEMY_DATABASE_URI = SQLITE
    UPLOAD_FOLDER = "Registros5s/static/uploads"
