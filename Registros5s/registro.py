from flask import Blueprint, request, render_template, current_app
from .models import Auditoria, Respuesta
from .forms import secciones
from Registros5s import db
import os
from datetime import datetime


bp = Blueprint("registro", __name__, url_prefix="/registro")


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

        respuestas = []

        for seccion, preguntas in secciones.items():
            seccion_puntos = 0
            seccion_max = len(preguntas) * 100  # Cada pregunta puede valer hasta 100

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
                respuestas.append(respuesta)
            resultados[seccion] = round((seccion_puntos / seccion_max) * 100, 2)
            total_puntos += seccion_puntos
            total_max += seccion_max

        # Guardar total en auditoria
        auditoria.total = round((total_puntos / total_max) * 100, 2)
        db.session.commit()

        return render_template(
            "registro/resultado.html",
            resultados=resultados,
            total=auditoria.total,
            respuestas=respuestas,
        )
    return render_template("registro/formulario.html", secciones=secciones)


@bp.route("/historial")
def historial():
    page = request.args.get("page", 1, type=int)
    fecha_filtro = request.args.get("fecha", "")

    query = Auditoria.query
    if fecha_filtro:
        try:
            fecha_dt = datetime.strptime(fecha_filtro, "%Y-%m-%d")
            query = query.filter(db.func.date(Auditoria.fecha) == fecha_dt.date())
        except ValueError:
            pass

    auditorias = query.order_by(Auditoria.fecha.desc()).paginate(page=page, per_page=20)
    return render_template(
        "registro/historial.html",
        auditorias=auditorias,
        fecha_filtro=fecha_filtro,
    )


@bp.route("/detalle/<int:auditoria_id>")
def detalle(auditoria_id):
    auditoria = Auditoria.query.get_or_404(auditoria_id)
    respuestas = Respuesta.query.filter_by(auditoria_id=auditoria.id).all()

    # Agrupar respuestas por sección
    secciones_respuestas = {}
    for respuesta in respuestas:
        secciones_respuestas.setdefault(respuesta.seccion, []).append(respuesta)

    return render_template(
        "registro/detalle.html",
        auditoria=auditoria,
        secciones_respuestas=secciones_respuestas,
    )
