from Registros5s import create_app  # Importa tu función de creación de app
import webview
import os
from Registros5s import create_app

HOST = "127.0.0.1"  # CRUCIAL: Solo escuchar peticiones locales
PORT = 5000
WINDOW_TITLE = "Auditoria 5S App"
WINDOW_URL = f"http://{HOST}:{PORT}"


def start_server():
    """Función que inicia el servidor Flask."""
    app = create_app()
    # Ejecutamos el servidor de forma silenciosa.
    # CRUCIAL: threaded=True permite que el servidor y la ventana se ejecuten
    app.run(host=HOST, port=PORT, threaded=True)


def start_ui():
    """Función que inicia la ventana de webview."""
    # Crea y abre la ventana.
    # Asegúrate de que esta función se llame DESPUÉS de que Flask haya arrancado (o casi al mismo tiempo)
    webview.create_window(
        WINDOW_TITLE,
        url=WINDOW_URL,
        width=1200,
        height=800,
        resizable=True,
    )
    # Bloquea la ejecución hasta que la ventana se cierre
    webview.start()

    # Después de cerrar la ventana de webview, forzamos el apagado del servidor.
    # Esto es similar a lo que hiciste con la ruta /shutdown, pero más directo.
    # NOTA: Esto no es el método más limpio, pero es efectivo con PyInstaller.
    os._exit(0)


if __name__ == "__main__":
    # 1. Inicia el servidor Flask en un hilo separado.
    from threading import Thread

    server_thread = Thread(target=start_server)
    server_thread.daemon = True  # El hilo muere si el programa principal muere
    server_thread.start()

    # 2. Inicia la interfaz de usuario (webview) en el hilo principal.
    #    webview esperará un momento antes de conectarse a la URL.
    start_ui()
