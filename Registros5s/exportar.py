import os
from flask import Blueprint, current_app, send_file
from .models import Auditoria, Respuesta
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from io import BytesIO
from openpyxl.drawing.image import Image as XLImage

bp = Blueprint("exportar", __name__, url_prefix="/exportar")


@bp.route("/exportar_excel/<int:auditoria_id>")
def exportar_excel(auditoria_id):
    auditoria = Auditoria.query.get_or_404(auditoria_id)
    respuestas = Respuesta.query.filter_by(auditoria_id=auditoria.id).all()

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Auditoría 5S"

    # --- Logo ---
    logo_path = os.path.join(current_app.static_folder, "img", "Sun_logo.png")
    if os.path.exists(logo_path):
        img_logo = XLImage(logo_path)
        img_logo.width = 180
        img_logo.height = 126
        ws.add_image(img_logo, "A1")
        ws.row_dimensions[1].height = 126

    # --- Título y datos principales ---
    ws.merge_cells("A2:C2")
    cell_title = ws["A2"]
    cell_title.value = "Auditoría 5S"
    cell_title.font = Font(bold=True, size=18)
    cell_title.alignment = Alignment(horizontal="center", vertical="center")

    # fecha
    ws.merge_cells("A3:C3")
    cell_nombre = ws["A3"]
    cell_nombre.value = f"Fecha: {auditoria.fecha.strftime('%Y-%m-%d %H:%M')} | Responsable: {auditoria.responsable}"
    cell_nombre.font = Font(size=12)
    cell_nombre.alignment = Alignment(horizontal="center", vertical="center")

    # responsable
    ws.merge_cells("A4:C4")
    cell_nombre = ws["A4"]
    cell_nombre.value = f"Responsable: {auditoria.responsable}"
    cell_nombre.font = Font(size=12)
    cell_nombre.alignment = Alignment(horizontal="center", vertical="center")

    start_row = 6  # Comienza después del logo y los datos principales

    # Estilos
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill("solid", fgColor="4F81BD")
    section_fill = PatternFill("solid", fgColor="A9D08E")
    section_font = Font(bold=True, color="000000")
    center_align = Alignment(horizontal="center", vertical="center")
    thin_border = Border(
        left=Side(style="thin"),
        right=Side(style="thin"),
        top=Side(style="thin"),
        bottom=Side(style="thin"),
    )

    secciones_respuestas = {}
    for respuesta in respuestas:
        secciones_respuestas.setdefault(respuesta.seccion, []).append(respuesta)

    row_num = start_row
    img_col = 3  # Columna donde van las imágenes

    for seccion, respuestas_seccion in secciones_respuestas.items():
        # Fila de sección
        ws.merge_cells(start_row=row_num, start_column=1, end_row=row_num, end_column=3)
        cell = ws.cell(row=row_num, column=1)
        cell.value = seccion
        cell.font = section_font
        cell.fill = section_fill
        cell.alignment = center_align
        cell.border = thin_border
        # Aplica estilos a todas las celdas del rango mergeado (excepto value)
        for col in range(2, 4):  # Columnas 2 y 3
            merged_cell = ws.cell(row=row_num, column=col)
            merged_cell.font = section_font
            merged_cell.fill = section_fill
            merged_cell.alignment = center_align
            merged_cell.border = thin_border
        row_num += 1

        # Encabezados
        headers = ["Pregunta", "Puntaje (%)", "Imagen"]
        for col_num, header in enumerate(headers, start=1):
            cell = ws.cell(row=row_num, column=col_num)
            cell.value = header
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = center_align
            cell.border = thin_border
        row_num += 1

        # Datos de la sección
        seccion_puntos = 0
        seccion_max = len(respuestas_seccion) * 100
        for respuesta in respuestas_seccion:
            cell_pregunta = ws.cell(row=row_num, column=1, value=respuesta.pregunta)
            cell_pregunta.alignment = center_align
            cell_pregunta.border = thin_border

            percent = f"{respuesta.puntaje}%" if respuesta.puntaje is not None else ""
            cell_puntaje = ws.cell(row=row_num, column=2, value=percent)
            cell_puntaje.alignment = center_align
            cell_puntaje.border = thin_border

            seccion_puntos += respuesta.puntaje if respuesta.puntaje else 0

            # Insertar imagen si existe
            if respuesta.imagen_path:
                img_path = os.path.join(
                    current_app.static_folder, respuesta.imagen_path
                )
                if os.path.exists(img_path):
                    img = XLImage(img_path)
                    img.width = 100
                    img.height = 100
                    img_cell = f"{get_column_letter(img_col)}{row_num}"
                    ws.add_image(img, img_cell)
                    ws.row_dimensions[row_num].height = 80
                ws.cell(row=row_num, column=img_col).border = thin_border
            else:
                ws.cell(row=row_num, column=img_col, value="").border = thin_border

            row_num += 1

        # Porcentaje total de la sección
        seccion_porcentaje = (
            round((seccion_puntos / seccion_max) * 100, 2) if seccion_max else 0
        )
        ws.merge_cells(start_row=row_num, start_column=1, end_row=row_num, end_column=3)
        for col in range(1, 4):  # Columnas 1 a 3
            cell_seccion_total = ws.cell(row=row_num, column=col)
            if col == 1:
                cell_seccion_total.value = (
                    f"Porcentaje total de la sección: {seccion_porcentaje}%"
                )
            cell_seccion_total.font = Font(bold=True)
            cell_seccion_total.alignment = center_align
            cell_seccion_total.border = thin_border
        row_num += 2  # Fila vacía entre secciones

    # Porcentaje total al final
    ws.merge_cells(start_row=row_num, start_column=1, end_row=row_num, end_column=3)
    for col in range(1, 4):  # Columnas 1 a 3
        cell_total = ws.cell(row=row_num, column=col)
        if col == 1:
            cell_total.value = f"Porcentaje Total General: {auditoria.total}%"
        cell_total.font = Font(bold=True, size=16)
        cell_total.alignment = center_align
        cell_total.border = thin_border

    # Ajustar ancho de columnas
    ws.column_dimensions["A"].width = 50
    ws.column_dimensions["B"].width = 15
    ws.column_dimensions["C"].width = 18

    # Guardar en memoria y enviar
    output = BytesIO()
    wb.save(output)
    output.seek(0)
    nombre_archivo = f"auditoria_{auditoria.id}.xlsx"
    return send_file(
        output,
        download_name=nombre_archivo,
        as_attachment=True,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
