# run.py
import webbrowser
from threading import Timer
from Registros5s import create_app  # Importa tu función de creación de app

HOST = "127.0.0.1"  # Mejor usar localhost para un ejecutable personal
PORT = 8000
URL = f"http://{HOST}:{PORT}"


# Función que abre el navegador
def open_browser():
    # Espera un breve momento para asegurar que el servidor está listo
    webbrowser.open_new_tab(URL)


if __name__ == "__main__":
    app = create_app()

    # Inicia el temporizador para abrir el navegador en 1 segundo
    Timer(1, open_browser).start()

    # Inicia el servidor Flask
    # CRUCIAL: Usamos threaded=True para que el servidor no bloquee el hilo principal
    # y el temporizador pueda ejecutarse.
    app.run(host=HOST, port=PORT, threaded=True)
