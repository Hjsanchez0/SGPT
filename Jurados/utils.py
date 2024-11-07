from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from datetime import datetime
import pytz

def generar_observacion(pdf_file_path, data):
    doc = SimpleDocTemplate(pdf_file_path, pagesize=letter)
    elements = []

    styles = getSampleStyleSheet()
    
    estilo_titulo = ParagraphStyle('Subtitulo', parent=styles['Title'], fontSize=15, fontName='Times-Bold', alignment=1)
    estilo_normal = ParagraphStyle('Normal', fontSize=11, fontName='Times-Roman', spaceAfter=6)
    estilo_normal_centrado = ParagraphStyle('Normal', fontSize=11, fontName='Times-Roman', spaceAfter=6, alignment=1)
    estilo_normal_tam10 = ParagraphStyle('Normal', fontSize=10, fontName='Times-Roman')
    estilo_negrita_centrado = ParagraphStyle('Normal', fontSize=12, fontName='Times-Bold', alignment=1)
    estilo_subtitulo = ParagraphStyle('Normal', fontSize=12, fontName='Times-Bold', alignment=0, underline=True)

    elements.append(Paragraph("FACULTAD DE CIENCIAS FISICAS Y MATEMÁTICAS<br/> ESCUELA PROFESIONAL DE INGENIERÍA INFORMÁTICA", estilo_titulo))
    elements.append(Paragraph("RECOMENDACIONES / OBSERVACIONES SEGÚN LA RÚBRICA DE EVALUACIÓN DE PROYECTOS DE INVESTIGACIÓN", estilo_negrita_centrado))
    elements.append(Spacer(1, 10))

    timezone = pytz.timezone('America/Lima')
    fecha_actual = datetime.now(timezone)
    meses = {1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"}
    dia = fecha_actual.day
    mes = meses[fecha_actual.month]
    año = fecha_actual.year
    fecha_formateada = f"Trujillo, {dia:02d} de {mes} de {año}"
    estilo_fecha = ParagraphStyle('Fecha', fontSize=12, fontName='Times-Roman', alignment=2)
    elements.append(Paragraph(fecha_formateada, estilo_fecha))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("I. ASPECTOS GENERALES", estilo_subtitulo))
    elements.append(Spacer(1, 10))

    data_tabla1 = [
        ['Ítems', 'Puntaje', 'Criterio', 'Calificación'],
        [
            Paragraph('Introducción', estilo_normal),
            Paragraph('3', estilo_normal_centrado),
            Paragraph('*Se menciona el problema de investigación de forma coherente y con un enfoque de lo general a lo particular (tener en cuenta que el objeto de estudio de la escuela de informática es el binomio software / sistema). Se coloca la justificación teórica, metodológica, práctica y social. Se detalla los objetivos de la investigación (general y específicos).', estilo_normal),
            Paragraph(data.get('calificacion_introduccion'), estilo_normal_centrado)
        ],
    ]

    col_widths = [73, 40, 300, 55]
    tabla1 = Table(data_tabla1, colWidths=col_widths) 
    tabla1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), '#A7C6ED'), 
        ('TEXTCOLOR', (0, 0), (-1, 0), '#000000'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, '#000000'),
    ]))

    elements.append(tabla1)

    data_tabla2 = [
        [Paragraph(f'Observación:<br />{data.get("observacion_introduccion")}', estilo_normal)],
    ]

    tabla2 = Table(data_tabla2, colWidths=[doc.width])
    tabla2.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, '#000000'),
    ]))

    elements.append(tabla2)

    data_tabla3 = [
        [
            Paragraph('Antecedentes', estilo_normal),
            Paragraph('3', estilo_normal_centrado),
            Paragraph('*La estructura de la redacción del antecedente comprende: Cita, Objetivo, Resultados, Conclusión y Aporte.', estilo_normal),
            Paragraph(data.get('calificacion_antecedentes'), estilo_normal_centrado)
        ],
    ]

    tabla3 = Table(data_tabla3, colWidths=col_widths) 
    tabla3.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, 0), '#000000'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, '#000000'),
    ]))

    elements.append(tabla3)

    data_tabla4 = [
        [Paragraph(f'Observación:<br />{data.get("observacion_antecedentes")}', estilo_normal)],
    ]

    tabla4 = Table(data_tabla4, colWidths=[doc.width])
    tabla4.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, '#000000'),
    ]))

    elements.append(tabla4)

    data_tabla5 = [
        [
            Paragraph('Marco Teórico', estilo_normal),
            Paragraph('3', estilo_normal_centrado),
            Paragraph('*Se menciona la información (extraída de base de datos reconocidas y/o libros) de las variables de estudio y de la metodología de desarrollo de software (si es el caso).', estilo_normal),
            Paragraph(data.get('calificacion_marco_teorico'), estilo_normal_centrado)
        ],
    ]

    tabla5 = Table(data_tabla5, colWidths=col_widths) 
    tabla5.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, 0), '#000000'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, '#000000'),
    ]))

    elements.append(tabla5)

    data_tabla6 = [
        [Paragraph(f'Observación:<br />{data.get("observacion_marco_teorico")}', estilo_normal)],
    ]

    tabla6 = Table(data_tabla6, colWidths=[doc.width])
    tabla6.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, '#000000'),
    ]))

    elements.append(tabla6)

    data_tabla7 = [
        [
            Paragraph('Hipótesis', estilo_normal),
            Paragraph('1', estilo_normal_centrado),
            Paragraph('*Se detallan la hipótesis general y específicas de la investigación.', estilo_normal),
            Paragraph(data.get('calificacion_hipotesis'), estilo_normal_centrado)
        ],
    ]

    tabla7 = Table(data_tabla7, colWidths=col_widths)  
    tabla7.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, 0), '#000000'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, '#000000'),
    ]))

    elements.append(tabla7)

    data_tabla8 = [
        [Paragraph(f'Observación:<br />{data.get("observacion_hipotesis")}', estilo_normal)],
    ]

    tabla8 = Table(data_tabla8, colWidths=[doc.width]) 
    tabla8.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, '#000000'),
    ]))

    elements.append(tabla8)

    data_tabla9 = [
        [
            Paragraph('Metodología', estilo_normal),
            Paragraph('3', estilo_normal_centrado),
            Paragraph('*Se especifica el enfoque de investigación, el tipo de investigación, el diseño de investigación, la población y/o muestra, técnicas e instrumentos que utilizó. Sobre la validez y confiabilidad eso solo aplica para las encuestas elaboradas por el investigador.', estilo_normal),
            Paragraph(data.get('calificacion_metodologia'), estilo_normal_centrado)
        ],
    ]

    tabla9 = Table(data_tabla9, colWidths=col_widths) 
    tabla9.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, 0), '#000000'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, '#000000'),
    ]))

    elements.append(tabla9)

    data_tabla10 = [
        [Paragraph(f'Observación:<br />{data.get("observacion_metodologia")}', estilo_normal)],
    ]

    tabla10 = Table(data_tabla10, colWidths=[doc.width])
    tabla10.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, '#000000'),
    ]))

    elements.append(tabla10)

    data_tabla11 = [
        [
            Paragraph('Aspectos administrativos', estilo_normal),
            Paragraph('3', estilo_normal_centrado),
            Paragraph('*Se detalla los recursos humanos (estudiantes y asesores), servicios de terceros, equipos y bienes duraderos, pasajes y viáticos, materiales e insumos. Se coloca el financiamiento de la investigación y el cronograma del proyecto.', estilo_normal),
            Paragraph(data.get('calificacion_aspectos_administrativos'), estilo_normal_centrado)
        ],
    ]

    tabla11 = Table(data_tabla11, colWidths=col_widths)
    tabla11.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, 0), '#000000'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, '#000000'),
    ]))

    elements.append(tabla11)

    data_tabla12 = [
        [Paragraph(f'Observación:<br />{data.get("observacion_aspectos_administrativos")}', estilo_normal)],
    ]

    tabla12 = Table(data_tabla12, colWidths=[doc.width])
    tabla12.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, '#000000'),
    ]))

    elements.append(tabla12)
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("II. ASPECTOS DE FORMA", estilo_subtitulo))
    elements.append(Spacer(1, 10))

    data_tabla13 = [
        ['Ítems', 'Puntaje', 'Criterio', 'Calificación'],
        [
            Paragraph('Redacción', estilo_normal),
            Paragraph('2', estilo_normal_centrado),
            Paragraph('*La redacción se encuentra en tercera persona y en futuro (si corresponde).', estilo_normal),
            Paragraph(data.get('calificacion_redaccion'), estilo_normal_centrado)
        ],
    ]

    tabla13 = Table(data_tabla13, colWidths=col_widths) 
    tabla13.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), '#A7C6ED'), 
        ('TEXTCOLOR', (0, 0), (-1, 0), '#000000'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, '#000000'),
    ]))

    elements.append(tabla13)

    data_tabla14 = [
        [Paragraph(f'Observación:<br />{data.get("observacion_redaccion")}', estilo_normal)],
    ]

    tabla14 = Table(data_tabla14, colWidths=[doc.width])
    tabla14.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, '#000000'),
    ]))

    elements.append(tabla14)

    data_tabla15 = [
        [
            Paragraph('Uso de citas y referencias', estilo_normal),
            Paragraph('2', estilo_normal_centrado),
            Paragraph('*Complementa su redacción con citas en estilo IEE y las referencias han sido generadas correctamente. La cantidad de citas utilizadas en el documento deben ser 25.', estilo_normal),
            Paragraph(data.get('calificacion_citayreferencia'), estilo_normal_centrado)
        ],
    ]

    tabla15 = Table(data_tabla15, colWidths=col_widths) 
    tabla15.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, 0), '#000000'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, '#000000'),
    ]))

    elements.append(tabla15)

    data_tabla16 = [
        [Paragraph(f'Observación:<br />{data.get("observacion_citayreferencia")}', estilo_normal)],
    ]

    tabla16 = Table(data_tabla16, colWidths=[doc.width])
    tabla16.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, '#000000'),
    ]))

    elements.append(tabla16)

    elements.append(Paragraph("* Las base de datos a utilizar son: Scopus, WOS, IEEE, ACM, SpringerLink (Puede utilizar otras, pero con aprobación del docente) y no se puede utilizar infromación de informes de tesis.", estilo_normal_tam10))

    doc.build(elements)