from flask import Blueprint, request, render_template, url_for
from .models import Auditoria, Respuesta
from Registros5s import db
import os

bp = Blueprint("registro", __name__, url_prefix="/registro")

secciones = {
    "Seiri": [
        "¿Los materiales innecesarios están eliminados?",
        "¿Las herramientas están ordenadas?",
    ],
    "Seiton": [
        "¿Cada objeto tiene un lugar definido?",
        "¿Es fácil encontrar lo que se necesita?",
    ],
    "Seiso": [
        "¿El área está limpia?",
        "¿Se detectan problemas de limpieza?",
    ],
    "Seiketsu": [
        "¿Se mantienen estándares visuales?",
        "¿Existen reglas claras para mantener el orden?",
    ],
    "Shitsuke": [
        "¿Se cumple con la disciplina de las 5S?",
        "¿El personal sigue los procedimientos?",
    ],
    "Seguridad": [
        "¿Se usan los EPP correctamente?",
        "¿Existen riesgos visibles?",
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
            seccion_max = len(preguntas) * 4

            for idx, pregunta in enumerate(preguntas):
                key = f"{seccion}_{idx}"
                valor = int(request.form.get(key, 0))
                seccion_puntos += valor

                # Guardar imagen
                imagen = request.files.get(f"{key}_img")
                imagen_path = None
                if imagen and imagen.filename != "":
                    if not os.path.exists(bp.config["UPLOAD_FOLDER"]):
                        os.makedirs(bp.config["UPLOAD_FOLDER"])
                    imagen_path = os.path.join(
                        bp.config["UPLOAD_FOLDER"], imagen.filename
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
