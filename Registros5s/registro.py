from flask import Blueprint, request, render_template, url_for, current_app
from .models import Auditoria, Respuesta
from Registros5s import db
import os

bp = Blueprint("registro", __name__, url_prefix="/registro")

secciones = {
    "Seiri": [
        {
            "pregunta": "¿Los materiales innecesarios están eliminados?",
            "opciones": [
                {"texto": "0", "valor": 0},
                {"texto": "1", "valor": 25},
                {"texto": "2", "valor": 50},
                {"texto": "3", "valor": 75},
                {"texto": "4", "valor": 100},
            ],
        },
        {
            "pregunta": "¿Las herramientas están ordenadas?",
            "opciones": [
                {"texto": "Cumple", "valor": 100},
                {"texto": "No cumple", "valor": 0},
            ],
        },
    ],
    "Seiton": [
        {
            "pregunta": "¿Cada objeto tiene un lugar definido?",
            "opciones": [
                {"texto": "0", "valor": 0},
                {"texto": "1", "valor": 25},
                {"texto": "2", "valor": 50},
                {"texto": "3", "valor": 75},
                {"texto": "4", "valor": 100},
            ],
        },
        {
            "pregunta": "¿Es fácil encontrar lo que se necesita?",
            "opciones": [
                {"texto": "Sí", "valor": 100},
                {"texto": "No", "valor": 0},
            ],
        },
    ],
    "Seiso": [
        {
            "pregunta": "¿El área está limpia?",
            "opciones": [
                {"texto": "0", "valor": 0},
                {"texto": "1", "valor": 25},
                {"texto": "2", "valor": 50},
                {"texto": "3", "valor": 75},
                {"texto": "4", "valor": 100},
            ],
        },
        {
            "pregunta": "¿Se detectan problemas de limpieza?",
            "opciones": [
                {"texto": "Cumple", "valor": 100},
                {"texto": "No cumple", "valor": 0},
            ],
        },
    ],
    "Seiketsu": [
        {
            "pregunta": "¿Se mantienen estándares visuales?",
            "opciones": [
                {"texto": "0", "valor": 0},
                {"texto": "1", "valor": 25},
                {"texto": "2", "valor": 50},
                {"texto": "3", "valor": 75},
                {"texto": "4", "valor": 100},
            ],
        },
        {
            "pregunta": "¿Existen reglas claras para mantener el orden?",
            "opciones": [
                {"texto": "Sí", "valor": 100},
                {"texto": "No", "valor": 0},
            ],
        },
    ],
    "Shitsuke": [
        {
            "pregunta": "¿Se cumple con la disciplina de las 5S?",
            "opciones": [
                {"texto": "0", "valor": 0},
                {"texto": "1", "valor": 25},
                {"texto": "2", "valor": 50},
                {"texto": "3", "valor": 75},
                {"texto": "4", "valor": 100},
            ],
        },
        {
            "pregunta": "¿El personal sigue los procedimientos?",
            "opciones": [
                {"texto": "Cumple", "valor": 100},
                {"texto": "No cumple", "valor": 0},
            ],
        },
    ],
    "Seguridad": [
        {
            "pregunta": "¿Se usan los EPP correctamente?",
            "opciones": [
                {"texto": "0", "valor": 0},
                {"texto": "1", "valor": 25},
                {"texto": "2", "valor": 50},
                {"texto": "3", "valor": 75},
                {"texto": "4", "valor": 100},
            ],
        },
        {
            "pregunta": "¿Existen riesgos visibles?",
            "opciones": [
                {"texto": "Sí", "valor": 0},
                {"texto": "No", "valor": 100},
            ],
        },
    ],
}


@bp.route("/formulario", methods=("GET", "POST"))
def formulario():
    if request.method == "POST":
        responsable = request.form.get("responsable", "No indicado")
        resultados = {}
        total_puntos = 0
        total_max = 0

        # Crear auditoria
        auditoria = Auditoria(responsable=responsable, total=0)
        db.session.add(auditoria)
        db.session.commit()

        for seccion, preguntas in secciones.items():
            seccion_puntos = 0
            seccion_max = (
                len(preguntas) * 100
            )  # Ahora cada pregunta puede valer hasta 100

            for idx, pregunta_obj in enumerate(preguntas):
                pregunta = pregunta_obj["pregunta"]
                opciones = pregunta_obj["opciones"]

                key = f"{seccion}_{idx}"
                valor = int(
                    request.form.get(key, 0)
                )  # El value será el valor ponderado
                seccion_puntos += valor

                # Guardar imagen
                imagen = request.files.get(f"{key}_img")
                imagen_path = None
                if imagen and imagen.filename != "":
                    if not os.path.exists(current_app.config["UPLOAD_FOLDER"]):
                        os.makedirs(current_app.config["UPLOAD_FOLDER"])
                    imagen_path = os.path.join(
                        current_app.config["UPLOAD_FOLDER"], imagen.filename
                    )
                    imagen_path = imagen_path.replace("\\", "/")

                    imagen.save(imagen_path)

                # Guardar respuesta en DB
                respuesta = Respuesta(
                    auditoria_id=auditoria.id,
                    seccion=seccion,
                    pregunta=pregunta,
                    puntaje=valor,
                    imagen_path=imagen_path,
                )
                db.session.add(respuesta)
            resultados[seccion] = round((seccion_puntos / seccion_max) * 100, 2)
            total_puntos += seccion_puntos
            total_max += seccion_max

        # Guardar total en auditoria
        auditoria.total = round((total_puntos / total_max) * 100, 2)
        db.session.commit()

        return render_template(
            "registro/resultado.html", resultados=resultados, total=auditoria.total
        )
    return render_template("registro/formulario.html", secciones=secciones)
