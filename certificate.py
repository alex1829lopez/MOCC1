from fpdf import FPDF
import uuid
from datetime import datetime
import os


def generar_certificado(nombre, curso, score):

    # =========================
    # RUTA BASE
    # =========================
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # =========================
    # DATOS DEL CERTIFICADO
    # =========================
    folio = str(uuid.uuid4())[:8].upper()
    fecha = datetime.now().strftime("%d/%m/%Y")

    # =========================
    # CREAR PDF
    # =========================
    pdf = FPDF(
        orientation="L",
        unit="mm",
        format="A4"
    )

    pdf.add_page()
    pdf.set_auto_page_break(False)

    # =========================
    # IMAGEN DE FONDO
    # =========================
    plantilla = os.path.join(
        BASE_DIR,
        "assets",
        "plantilla_certificado.jpg"
    )

    if os.path.exists(plantilla):
        pdf.image(
            plantilla,
            x=0,
            y=0,
            w=297,
            h=210
        )

    # =========================
    # TITULO
    # =========================
    pdf.set_text_color(120, 90, 40)
    pdf.set_font("Times", "B", 30)

    pdf.set_y(25)

    pdf.cell(
        0,
        10,
        "CERTIFICADO DE FINALIZACION",
        align="C"
    )

    # =========================
    # ACADEMIA
    # =========================
    pdf.set_font("Times", "", 18)

    pdf.set_y(42)

    pdf.cell(
        0,
        10,
        "SkillForge Academy",
        align="C"
    )

    # =========================
    # TEXTO
    # =========================
    pdf.set_font("Arial", "", 14)

    pdf.set_y(65)

    pdf.cell(
        0,
        10,
        "Este certificado se otorga a:",
        align="C"
    )

    # =========================
    # NOMBRE
    # =========================
    pdf.set_font("Times", "B", 26)

    pdf.set_y(82)

    pdf.cell(
        0,
        10,
        nombre.upper(),
        align="C"
    )

    pdf.line(90, 95, 205, 95)

    # =========================
    # DESCRIPCION
    # =========================
    pdf.set_font("Arial", "", 14)

    pdf.set_y(103)

    pdf.cell(
        0,
        10,
        "Por haber completado satisfactoriamente el curso de:",
        align="C"
    )

    # =========================
    # CURSO
    # =========================
    pdf.set_font("Arial", "B", 18)

    pdf.set_y(118)

    pdf.cell(
        0,
        10,
        curso.upper(),
        align="C"
    )

    # =========================
    # CALIFICACION
    # =========================
    pdf.set_font("Arial", "", 14)

    pdf.set_y(132)

    pdf.cell(
        0,
        10,
        f"Calificacion obtenida: {score:.0f}/100",
        align="C"
    )

    # =========================
    # FECHA
    # =========================
    pdf.set_y(144)

    pdf.cell(
        0,
        10,
        f"Fecha de emision: {fecha}",
        align="C"
    )

    # =========================
    # FOLIO
    # =========================
    pdf.set_font("Arial", "B", 12)

    pdf.set_y(175)

    pdf.cell(
        0,
        8,
        f"Folio: {folio}",
        align="C"
    )

    # =========================
    # GUARDAR PDF
    # =========================
    file_path = os.path.join(
        BASE_DIR,
        f"certificado_{folio}.pdf"
    )

    pdf.output(file_path)

    return file_path