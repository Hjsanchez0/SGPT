from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from io import BytesIO
from datetime import datetime
import pytz 
from django.contrib.staticfiles import finders

def generar_pdf_alumno(response, alumnos, contenido, firma):
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    styles = getSampleStyleSheet()

    estilo_titulo = ParagraphStyle('Titulo', parent=styles['Title'], fontSize=16, fontName='Times-Bold', alignment=1)

    estilo_subtitulo = ParagraphStyle('Subtitulo', parent=styles['Title'], fontSize=18, fontName='Times-Bold', alignment=0)

    estilo_normal = ParagraphStyle('Normal', fontSize=12, fontName='Times-Roman', spaceAfter=6,)

    estilo_tabla = ParagraphStyle('Normal', fontSize=10, fontName='Times-Roman', alignment=1, spaceAfter=6 )

    estilo_footer = ParagraphStyle('Normal', fontSize=9, fontName='Times-Bold', spaceAfter=6, alignment=1)

    elements.append(Paragraph("UNIVERSIDAD NACIONAL DE TRUJILLO", estilo_titulo))

    imagen_path = finders.find("images/logo-unt.png")

    imagen = Image(imagen_path, width=inch/2, height=inch/2)
    header_data = [
        [imagen, Paragraph("FORMATO UNICO DE TRAMITE - F.U.T.", estilo_subtitulo)], 
    ]
    
    header_table = Table(header_data, colWidths=[inch, 5.8*inch])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'), 
    ]))

    elements.append(header_table)
    elements.append(Spacer(1, 5))
    timezone = pytz.timezone('America/Lima')
    fecha_actual = datetime.now(timezone)

    # Diccionario para los nombres de los meses en español
    meses = {1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"}

    # Formatear la fecha
    dia = fecha_actual.day
    mes = meses[fecha_actual.month]
    año = fecha_actual.year
    fecha_formateada = f"Trujillo, {dia:02d} de {mes} de {año}"

    # Crear el estilo para la fecha
    estilo_fecha = ParagraphStyle('Fecha', fontSize=12, fontName='Times-Roman', alignment=2, spaceAfter=6)

    # Agregar la fecha al documento
    elements.append(Spacer(1, 10))
    elements.append(Paragraph(fecha_formateada, estilo_fecha))
    elements.append(Paragraph("Dirigido a: Ms. Jose Gabriel Cruz Silva", estilo_normal))
    elements.append(Paragraph("Información de los Alumnos: ", estilo_normal))
    elements.append(Spacer(1, 5))

    data = [['Apellidos y Nombres', 'DNI', 'Cod. Matrícula']]
    for alumno in alumnos:
        data.append([
            Paragraph(f"{alumno.apellidoPat} {alumno.apellidoMat} {alumno.nombres}", estilo_tabla),
            Paragraph(alumno.dni, estilo_tabla),
            Paragraph(alumno.codMatricula, estilo_tabla)
        ])

    table1 = Table(data, colWidths=[4.3 * inch, 0.8 * inch, 1.2 * inch])

    table1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 4),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(table1)
    elements.append(Spacer(1, 10))

    data2 = [['Teléfono', 'E-Mail', 'Dirección']]
    
    for alumno in alumnos:
        data2.append([
            Paragraph(alumno.celular, estilo_tabla),
            Paragraph(alumno.email, estilo_tabla),
            Paragraph(alumno.domicilio, estilo_tabla)
        ])

    table2 = Table(data2, colWidths=[1 * inch, 2.6 * inch, 2.7 * inch])

    table2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), 
        ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 4),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(table2)
    elements.append(Spacer(1, 5))

    info_text2 = ["De la Facultad(u Oficina) de: Facultad de Ciencias Físicas y Matemáticas", "Escuela o Dpto: Escuela de Informática", "Ciclo o Año: 9"]

    for line in info_text2:
            elements.append(line if isinstance(line, Paragraph) else Paragraph(line, estilo_normal))

    elements.append(Paragraph("Objeto de la Solicitud:", estilo_normal))
    elements.append(Paragraph(contenido, estilo_normal))

    if firma:
        firma_image = firma.read()
        firma_path = BytesIO(firma_image)
        elements.append(Spacer(1, 5))
        elements.append(Paragraph("Firma del Solicitante:", estilo_normal))
        elements.append(Image(firma_path, width=1.7 * inch, height=0.7 * inch))

    elements.append(Spacer(1, 5))

    info_text3 = ["Los datos consignados en e presente formulario y la información contenida en los documentos que acompaño son verdaderos y tienen de carácter de DECLARACIÓN JURADA, los mismos que están sujetos a fiscalización posterior, que en caso de acreditarse falsedad o fraude, me someto a las sanciones establecidas en la ley 27444."]
    
    for line in info_text3:
        elements.append(line if isinstance(line, Paragraph) else Paragraph(line, estilo_normal))


    elements.append(Spacer(1, 5))
    elements.append(Paragraph("<u>_____________________________________________________________________________________________________</u>", estilo_footer))

    footer_info = [
        "Universidad Nacional de Trujillo | Jr. Juan Pablo II s/n Ciudad Universitaria - Telf. 239239 | Dirección de Registro Técnico - Telf. 205377"
    ]

    for line in footer_info:
        elements.append(Paragraph(line, estilo_footer))

    doc.build(elements)