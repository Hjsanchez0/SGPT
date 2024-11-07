from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from datetime import datetime
import pytz
from django.contrib.staticfiles import finders

def generar_carta_alumno(pdf_file_path, context):
    alumnos = context['alumnos']

    doc = SimpleDocTemplate(pdf_file_path, pagesize=letter)
    elements = []

    styles = getSampleStyleSheet()

    estilo_subtitulo = ParagraphStyle('Subtitulo', parent=styles['Title'], fontSize=15, fontName='Times-Bold', alignment=1)

    estilo_normal = ParagraphStyle('Normal', fontSize=12,fontName='Times-Roman', spaceAfter=6)

    estilo_normal_centrado = ParagraphStyle('Normal', fontSize=12, fontName='Times-Roman', spaceAfter=6, alignment=1)
    
    estilo_negrita_centrado = ParagraphStyle('Normal', fontSize=12, fontName='Times-Bold', alignment=1)

    estilo_negrita = ParagraphStyle('Normal', fontSize=12, fontName='Times-Bold', alignment=0)

    estilo_footer = ParagraphStyle('Normal', fontSize=9, fontName='Times-Bold', spaceAfter=6, alignment=1)

    estilo_subtitulo_subrayado = ParagraphStyle('Normal', fontSize=12, fontName='Times-Bold', alignment=0, underline=True)

    titulo = "FACULTAD DE CIENCIAS FISICAS Y MATEMÁTICAS<br/> Escuela Profesional de Ingeniería Informática"
    # Agregar un título al PDF

    imagen_path = finders.find("images/logo-unt.png")
    imagen_path2 = finders.find("images/logo-bicentenario.png")

    imagen = Image(imagen_path, width=inch/1.5, height=inch/2.5)
    imagen2 = Image(imagen_path2, width=inch, height=inch)

    header_data = [
        [imagen, Paragraph(titulo, estilo_subtitulo), imagen2], 
    ]

    header_table = Table(header_data, colWidths=[inch/1.2, 5.5*inch, 1*inch])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  
        ('ALIGN', (1, 0), (1, 0), 'CENTER'), 
    ]))

    elements.append(header_table)
    elements.append(Paragraph("<u>_____________________________________________________________________________________________________</u>", estilo_footer))

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
    estilo_fecha = ParagraphStyle('Fecha', fontSize=12, fontName='Times-Roman', alignment=2)

    elements.append(Paragraph(fecha_formateada, estilo_fecha))

    elements.append(Paragraph("<u>CARTA N° 020-2023-EPInf</u>", estilo_subtitulo_subrayado))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("Señor(a)", estilo_negrita))
    elements.append(Spacer(1, 2))

    director_unico = alumnos[0]['proyecto']['director'] if alumnos else None
    mismo_director = all(alumno_info['proyecto']['director'] == director_unico for alumno_info in alumnos)

    if mismo_director and director_unico:
        elements.append(Paragraph(director_unico, estilo_negrita))
        elements.append(Spacer(1, 2))

    cargo_unico = alumnos[0]['proyecto']['cargo'] if alumnos else None
    mismo_cargo = all(alumno_info['proyecto']['cargo'] == cargo_unico for alumno_info in alumnos)

    if mismo_cargo and cargo_unico:
        elements.append(Paragraph(cargo_unico, estilo_negrita))
        elements.append(Spacer(1, 2))

    institucion_unica = alumnos[0]['proyecto']['institucion'] if alumnos else None
    misma_institucion = all(alumno_info['proyecto']['institucion'] == institucion_unica for alumno_info in alumnos)

    if misma_institucion and institucion_unica:
        elements.append(Paragraph(institucion_unica, estilo_negrita))
        elements.append(Spacer(1, 2))

    elements.append(Paragraph("<u>Presente.-</u>", estilo_negrita))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("ASUNTO: SOLICITA AUTORIZACIÓN PARA ACCESO A INFORMACION", estilo_negrita_centrado))
    elements.append(Spacer(1, 10))

    titulo_unico = alumnos[0]['proyecto']['titulo'] if alumnos else None
    mismo_titulo = all(alumno_info['proyecto']['titulo'] == titulo_unico for alumno_info in alumnos)

    if mismo_titulo and titulo_unico:
        info_text = f"Tengo a bien dirigirme a usted, para saludarle muy cordialmente y, a la vez hacer de su conocimiento, que los estudiantes del IX Cliclo de la Escuela de Ingeniería Informática, se encuentran realizando el curso de Proyecto de Tesis titulado: <b>{titulo_unico}</b>."
        elements.append(Paragraph(info_text, estilo_normal))
        elements.append(Spacer(1, 10))

    info_text2 = ["En tal sentido esta Dirección, solicita a través de su Despacho ordenar a quien corresponda, se sirva brindar autorización, para acceso a información para la elaboración del Proyecto de Tesis solicitados por los estudiantes: "]
    alumnos_info = []

    for alumno_info in alumnos:
        alumno = alumno_info['alumno']
        # Concatenar información del estudiante con el nombre en negrita
        alumno_line = f"<b>{alumno['nombre']}</b>, con DNI N° {alumno['dni']}, N° de Matrícula {alumno['codMatricula']}"
        alumnos_info.append(alumno_line)

    # Unir la información de los alumnos en una sola línea
    alumnos_line = ', '.join(alumnos_info)

    # Combinar el encabezado con la información de los alumnos
    combined_line = info_text2[0] + alumnos_line

    # Agregar la información de los alumnos al documento
    elements.append(Paragraph(combined_line, estilo_normal))
    elements.append(Spacer(1, 10))

    info_text3 = ["Asimismo los referidos estudiantes, se comprometen a cumplir con las normas éticas y legales en la utilización de la información recopilada la cual garantiza la confidencialidad, respeto por la privacidad de datos y además debo indicar que toda información proporcionada será para uso exclusivamente académico."]
    
    for line in info_text3:
        elements.append(line if isinstance(line, Paragraph) else Paragraph(line, estilo_normal))
        elements.append(Spacer(1, 10))

    info_text4 = ["Agradezco a usted la atención al presente y hago propicia la ocasión para expresarle mi consideración y estima."]
    
    for line in info_text4:
        elements.append(line if isinstance(line, Paragraph) else Paragraph(line, estilo_normal))
        elements.append(Spacer(1, 10))

    elements.append(Paragraph("Atentamente,", estilo_normal_centrado))

    imagen_path3 = "static/images/firma-sello.png"

    imagen3 = Image(imagen_path3, width=1.5*inch, height=inch/1.5)

    header_data1 = [
        [imagen3], 
    ]

    header_table2 = Table(header_data1)
    header_table2.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  
        ('ALIGN', (1, 0), (1, 0), 'CENTER'), 
    ]))

    elements.append(header_table2)

    elements.append(Paragraph("Ms. JOSÉ GABRIEL CRUZ SILVA", estilo_negrita_centrado))
    elements.append(Paragraph("Director de la Escuela Profesional de Informática", estilo_normal_centrado))

    elements.append(Paragraph("<u>_____________________________________________________________________________________________________</u>", estilo_footer))

    footer_info = [
        "Correo: informatica@unitru.edu.pe | Ciudad Universitaria: Av. Juan Pablo II s/n  "
    ]

    for line in footer_info:
        elements.append(Paragraph(line, estilo_footer))

    doc.build(elements)
