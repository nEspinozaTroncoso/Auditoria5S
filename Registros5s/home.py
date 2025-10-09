from flask import Blueprint, render_template, request
import os

bp = Blueprint("home", __name__)


@bp.route("/")
def index():
    return render_template("index.html")


# Coloca esta función en un lugar accesible por tu app (e.g., Registros5s/__init__.py o home.py)


@bp.route("/shutdown", methods=["GET", "POST"])
def shutdown():
    """Ruta para apagar el servidor Flask y el proceso del .exe."""

    # 1. Devolver la respuesta inmediatamente para que el navegador no espere
    response = "Servidor Flask y aplicación cerrados correctamente. Ahora puedes cerrar esta ventana."

    # 2. Programar el cierre del proceso
    #    Usamos una función interna que llama a os._exit(0)
    #    para matar el proceso del .exe, garantizando que el archivo se libere.
    def kill_process():
        # Damos 0.5 segundos al navegador para recibir la respuesta antes de matar el proceso
        import time

        time.sleep(0.5)
        os._exit(0)

    # 3. Iniciar el hilo de cierre
    from threading import Thread  # Necesitas importar Thread

    closer = Thread(target=kill_process)
    closer.start()

    return response
