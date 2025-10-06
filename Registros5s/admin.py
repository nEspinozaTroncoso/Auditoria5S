from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from .models import Auditoria
from Registros5s import db

bp = Blueprint("admin", __name__, url_prefix="/admin")

ADMIN_USER = "admin"
ADMIN_PASS = "adminpass123456789"


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form.get("usuario")
        clave = request.form.get("clave")
        if usuario == ADMIN_USER and clave == ADMIN_PASS:
            session["admin"] = True
            return redirect(url_for("admin.panel"))
        else:
            flash("Usuario o contraseña incorrectos", "danger")
    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("admin.login"))


@bp.route("/panel", methods=["GET", "POST"])
def panel():
    if not session.get("admin"):
        return redirect(url_for("admin.login"))

    # Importa las listas desde forms.py
    from .forms import RESPONSABLES, AREAS

    # Modificar listas (ejemplo: agregar responsable)
    if request.method == "POST":
        nuevo_resp = request.form.get("nuevo_responsable")
        if nuevo_resp and nuevo_resp not in RESPONSABLES:
            RESPONSABLES.append(nuevo_resp)
        nuevo_area = request.form.get("nuevo_area")
        if nuevo_area and nuevo_area not in AREAS:
            AREAS.append(nuevo_area)
        # Para eliminar, puedes recibir el nombre y hacer RESPONSABLES.remove(nombre)

    # Mostrar registros y permitir eliminar/modificar
    auditorias = Auditoria.query.order_by(Auditoria.fecha.desc()).all()
    return render_template(
        "auth/panel.html",
        RESPONSABLES=RESPONSABLES,
        AREAS=AREAS,
        auditorias=auditorias,
    )


@bp.route("/eliminar_responsable/<nombre>")
def eliminar_responsable(nombre):
    if not session.get("admin"):
        return redirect(url_for("admin.login"))
    from .forms import RESPONSABLES

    if nombre in RESPONSABLES:
        RESPONSABLES.remove(nombre)
    return redirect(url_for("admin.panel"))


@bp.route("/eliminar_area/<nombre>")
def eliminar_area(nombre):
    if not session.get("admin"):
        return redirect(url_for("admin.login"))
    from .forms import AREAS

    if nombre in AREAS:
        AREAS.remove(nombre)
    return redirect(url_for("admin.panel"))


@bp.route("/eliminar_auditoria/<int:id>")
def eliminar_auditoria(id):
    if not session.get("admin"):
        return redirect(url_for("admin.login"))
    auditoria = Auditoria.query.get_or_404(id)
    db.session.delete(auditoria)
    db.session.commit()
    return redirect(url_for("admin.panel"))
