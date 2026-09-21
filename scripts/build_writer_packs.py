#!/usr/bin/env python3
"""Build the bilingual judicial-control writer packs for the public notebook."""

from pathlib import Path
from shutil import copyfile

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf"
PUBLIC = ROOT / "assets" / "docs"

NAVY = colors.HexColor("#13252D")
INK = colors.HexColor("#1D2930")
TEAL = colors.HexColor("#25766E")
GOLD = colors.HexColor("#C89545")
CREAM = colors.HexColor("#F4EFE5")
PALE = colors.HexColor("#E8F0EE")
MIST = colors.HexColor("#F4F7F6")
MUTED = colors.HexColor("#5E6A70")
RULE = colors.HexColor("#CBD6D2")
WHITE = colors.white


pdfmetrics.registerFont(TTFont("DejaVu", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DejaVu-Bold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))


def para(text, style):
    return Paragraph(text, style)


def card(title, body, styles, label=None, tone="plain"):
    bg = PALE if tone == "teal" else CREAM if tone == "gold" else MIST
    content = []
    if label:
        content.append(para(label.upper(), styles["label"]))
        content.append(Spacer(1, 1.5 * mm))
    content.append(para(title, styles["card_title"]))
    content.append(Spacer(1, 1.5 * mm))
    content.append(para(body, styles["card_body"]))
    table = Table([[content]], colWidths=[174 * mm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("BOX", (0, 0), (-1, -1), 0.6, RULE),
        ("LEFTPADDING", (0, 0), (-1, -1), 5 * mm),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5 * mm),
        ("TOPPADDING", (0, 0), (-1, -1), 4 * mm),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4 * mm),
    ]))
    return KeepTogether([table, Spacer(1, 3 * mm)])


def mini_grid(items, styles):
    cells = []
    for label, body in items:
        cells.append([
            para(label.upper(), styles["label"]),
            Spacer(1, 1.5 * mm),
            para(body, styles["small"]),
        ])
    rows = []
    for index in range(0, len(cells), 2):
        pair = cells[index:index + 2]
        if len(pair) == 1:
            pair.append("")
        rows.append(pair)
    table = Table(rows, colWidths=[86 * mm, 86 * mm], hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), MIST),
        ("BOX", (0, 0), (-1, -1), 0.6, RULE),
        ("INNERGRID", (0, 0), (-1, -1), 0.4, RULE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4 * mm),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4 * mm),
        ("TOPPADDING", (0, 0), (-1, -1), 4 * mm),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4 * mm),
    ]))
    return table


def source_item(number, title, url, note, styles):
    link = f'<link href="{url}" color="#25766E"><u>{title}</u></link>'
    text = f'<font color="#C89545"><b>{number:02d}</b></font>  {link}<br/><font color="#5E6A70">{note}</font>'
    return para(text, styles["source"])


def make_styles():
    base = getSampleStyleSheet()
    return {
        "cover_kicker": ParagraphStyle("cover_kicker", parent=base["Normal"], fontName="DejaVu-Bold", fontSize=9, leading=12, textColor=GOLD, tracking=1.1, spaceAfter=8),
        "cover_title": ParagraphStyle("cover_title", parent=base["Title"], fontName="DejaVu-Bold", fontSize=28, leading=33, textColor=WHITE, alignment=TA_LEFT, spaceAfter=11),
        "cover_deck": ParagraphStyle("cover_deck", parent=base["Normal"], fontName="DejaVu", fontSize=12, leading=18, textColor=colors.HexColor("#DCE7E3"), spaceAfter=16),
        "cover_meta": ParagraphStyle("cover_meta", parent=base["Normal"], fontName="DejaVu", fontSize=8, leading=12, textColor=colors.HexColor("#DCE7E3")),
        "section_no": ParagraphStyle("section_no", parent=base["Normal"], fontName="DejaVu-Bold", fontSize=8, leading=10, textColor=GOLD, tracking=1.2, spaceAfter=4),
        "h1": ParagraphStyle("h1", parent=base["Heading1"], fontName="DejaVu-Bold", fontSize=19, leading=24, textColor=NAVY, spaceAfter=7),
        "deck": ParagraphStyle("deck", parent=base["Normal"], fontName="DejaVu", fontSize=10.2, leading=15.5, textColor=MUTED, spaceAfter=10),
        "h2": ParagraphStyle("h2", parent=base["Heading2"], fontName="DejaVu-Bold", fontSize=13, leading=17, textColor=NAVY, spaceBefore=5, spaceAfter=5),
        "body": ParagraphStyle("body", parent=base["BodyText"], fontName="DejaVu", fontSize=9, leading=13.2, textColor=INK, spaceAfter=6),
        "small": ParagraphStyle("small", parent=base["BodyText"], fontName="DejaVu", fontSize=7.7, leading=11, textColor=INK),
        "label": ParagraphStyle("label", parent=base["Normal"], fontName="DejaVu-Bold", fontSize=6.8, leading=8.5, textColor=TEAL, tracking=0.7),
        "card_title": ParagraphStyle("card_title", parent=base["Heading3"], fontName="DejaVu-Bold", fontSize=10.2, leading=13, textColor=NAVY),
        "card_body": ParagraphStyle("card_body", parent=base["BodyText"], fontName="DejaVu", fontSize=8.2, leading=12, textColor=INK),
        "table_head": ParagraphStyle("table_head", parent=base["Normal"], fontName="DejaVu-Bold", fontSize=7.2, leading=9.2, textColor=WHITE),
        "table_cell": ParagraphStyle("table_cell", parent=base["Normal"], fontName="DejaVu", fontSize=6.8, leading=9.4, textColor=INK),
        "source": ParagraphStyle("source", parent=base["BodyText"], fontName="DejaVu", fontSize=7.3, leading=10.5, textColor=INK, spaceAfter=4.5),
        "footer": ParagraphStyle("footer", parent=base["Normal"], fontName="DejaVu", fontSize=6.6, leading=8, textColor=MUTED),
        "quote": ParagraphStyle("quote", parent=base["BodyText"], fontName="DejaVu", fontSize=10, leading=15, textColor=NAVY, leftIndent=5 * mm, borderColor=GOLD, borderWidth=0, borderPadding=4 * mm, spaceAfter=8),
    }


def page_decorator(canvas, doc, language):
    canvas.saveState()
    width, height = A4
    if doc.page == 1:
        canvas.setFillColor(NAVY)
        canvas.rect(0, 0, width, height, fill=1, stroke=0)
        canvas.setFillColor(GOLD)
        canvas.rect(18 * mm, 23 * mm, 30 * mm, 1.2 * mm, fill=1, stroke=0)
    else:
        canvas.setStrokeColor(RULE)
        canvas.setLineWidth(0.5)
        canvas.line(18 * mm, height - 16 * mm, width - 18 * mm, height - 16 * mm)
        canvas.setFont("DejaVu-Bold", 6.5)
        canvas.setFillColor(TEAL)
        canvas.drawString(18 * mm, height - 12.5 * mm, "PROJECT SUN ROCK  /  WRITER PACK" if language == "en" else "PROJECT SUN ROCK  /  PAQUETE PARA AUTORES")
        canvas.setFont("DejaVu", 6.5)
        canvas.setFillColor(MUTED)
        canvas.drawRightString(width - 18 * mm, 10 * mm, f"{doc.page:02d}  /  13 AUG 2026")
    canvas.restoreState()


def add_heading(story, number, title, deck, styles):
    story.extend([
        para(number, styles["section_no"]),
        para(title, styles["h1"]),
        para(deck, styles["deck"]),
    ])


def evidence_table(rows, headers, styles, widths):
    data = [[para(h, styles["table_head"]) for h in headers]]
    for row in rows:
        data.append([para(cell, styles["table_cell"]) for cell in row])
    table = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, MIST]),
        ("GRID", (0, 0), (-1, -1), 0.4, RULE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 2.4 * mm),
        ("RIGHTPADDING", (0, 0), (-1, -1), 2.4 * mm),
        ("TOPPADDING", (0, 0), (-1, -1), 2.3 * mm),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.3 * mm),
    ]))
    return table


def spanish_story(styles):
    s = []
    s.extend([
        Spacer(1, 36 * mm),
        para("CONTROL JUDICIAL  /  INSOLVENCIA  /  PRUEBA PENAL", styles["cover_kicker"]),
        para("¿Cuándo deja un resultado mercantil de ser meramente adverso?", styles["cover_title"]),
        para("Paquete documental para juristas, periodistas y autores independientes. Sun Park se contrasta con Inparsa / Hoteles Beatriz únicamente como comparador metodológico.", styles["cover_deck"]),
        Spacer(1, 76 * mm),
        para("Edición 1  /  Control de fuentes: 13 de agosto de 2026<br/>Project Sun Rock - Cuaderno jurídico<br/>Lectura estimada: 18 minutos", styles["cover_meta"]),
        PageBreak(),
    ])

    add_heading(s, "01  /  REGLAS DE LECTURA", "Un caso abre la pregunta; solo el otro expediente puede responderla.", "Este paquete no pide adhesión. Separa resultado, fuente, alegación, inferencia, dato discutido y laguna para que un tercero pueda confirmar, refutar o reformular la tesis.", styles)
    s.append(mini_grid([
        ("Inparsa", "La prensa informó el 13 de febrero de 2026 de una admisión o examen provisional por el TSJC. La propia noticia decía que aún debía decidirse la apertura de investigación. No se localizó el auto primario ni un resultado público posterior."),
        ("Sun Park", "Gil Marer sostiene formalmente que una secuencia atribuida al magistrado Alberto López Villarrubia exige investigación penal. No existe resolución judicial publicada que declare culpabilidad."),
        ("Relación", "Son casos, jueces, partes y mecanismos distintos. No se afirma red común, concierto ni patrón institucional."),
        ("Disciplina / delito", "El CGPJ y la jurisdicción penal tienen objetos y umbrales distintos. Una actuación disciplinaria no decide los elementos de los artículos 446 a 449 CP."),
    ], styles))
    s.append(Spacer(1, 5 * mm))
    s.append(card("La regla central", "Una querella contra otro juez no convierte una denuncia propia en verdadera. Su utilidad es más limitada: muestra que el control penal de la función judicial tiene una vía jurídica real y obliga a formular la pregunta con prueba individualizada.", styles, "Límite del comparador", "gold"))
    s.append(card("Posición atribuida", "Gil Marer mantiene que determinados actos, omisiones y resoluciones, leídos como secuencia, cruzan el umbral que exige investigación penal. Es una alegación bajo su responsabilidad, no una condena ni una declaración judicial de culpabilidad.", styles, "Sun Park", "teal"))
    s.append(PageBreak())

    add_heading(s, "02  /  CRONOLOGÍA DE CONTROL", "Siete nodos que una investigación puede confirmar o desmentir.", "La cronología no prueba dolo por acumulación. Cada nodo exige conocimiento, competencia, remedio disponible, decisión u omisión, efecto y explicación jurídica propia.", styles)
    chronology = [
        ("16 ABR 2018", "Auto y alcance", "El dossier sostiene que el auto concernía a LPB y no entregó a CAM la posesión de CEXP, Matkator ni activos de terceros."),
        ("7 JUN 2018", "Control material", "Prueba contemporánea describe rotura de acceso, cadenas, bombines y exclusión. La autoría y el conocimiento judicial deben probarse por separado."),
        ("13 JUN 2018", "Salida ONA", "Informe de Daniel Irigoyen relata reuniones con juez y administrador sobre financiador, operador, pago o consignación. No es acta judicial."),
        ("2018-2019", "OB REM", "Operación de 28 noviembre de 2018; no convalidación posterior de 24 octubre de 2019 según el expediente público. Restitución y cuentas siguen abiertas."),
        ("2020-2021", "Activo y prueba", "Demolición/restricción alegada, solicitudes de inspección y pericial, y narrativa RIC anterior al título formal."),
        ("15 OCT 2021", "Premisa contradictoria", "El dossier identifica dos autos: uno dijo que la subasta se celebró y otro que no. Se necesita el texto certificado y el contexto completo."),
        ("26 ENE-21 FEB 2022", "Adjudicación", "El expediente dice que se tuvo documentación por aportada pero irrelevante; siguieron copias operativas, escritura y registro a CAM."),
    ]
    s.append(evidence_table(chronology, ["Fecha", "Nodo", "Registro y límite probatorio"], styles, [27 * mm, 38 * mm, 109 * mm]))
    s.append(Spacer(1, 5 * mm))
    s.append(card("Lectura correcta", "La cronología organiza la prueba; no convierte duración o acumulación en finalidad ilícita. Cada transición requiere el documento contemporáneo, el deber aplicable y una explicación causal.", styles, "Control de inferencia", "gold"))
    s.append(PageBreak())

    add_heading(s, "03  /  MATRIZ ACTO-PRUEBA", "Lo que debe cerrarse nodo por nodo.", "La columna 'prueba a localizar' es tan importante como la acusación: identifica qué documento podría cerrar el debate en un sentido u otro.", styles)
    rows = [
        ("16 abr 2018", "Alcance del auto y límites sobre LPB / terceros.", "¿Cómo se produjo un control material más amplio?", "Auto, instrucciones, mapa de ejecución."),
        ("7 jun 2018", "Toma material contemporáneamente documentada.", "Tutela urgente de acceso, prueba y perímetro.", "Avisos, agenda, escritos, decisiones y autoría."),
        ("13 jun 2018", "Alternativa financiada relatada por Irigoyen.", "Tutela útil mientras se verificaba pago/consignación.", "Agenda, acta, escrito, traslado, informe AC."),
        ("2018-2019", "OB REM y no convalidación alegada.", "Restauración registral, material y contable.", "Cancelación, restitución, frutos y cuentas."),
        ("2020-2021", "Obras, acceso, pericial y narrativa RIC.", "Preservar activo, prueba y concurrencia.", "Cronología certificada de petición/oposición/decisión."),
        ("15 oct 2021", "Dos premisas públicas incompatibles.", "Aclarar antes de efectos irreversibles.", "Autos completos y expediente de subsanación."),
        ("ene-feb 2022", "Adjudicación, escritura y registro oficiales.", "Conciliar deuda, valor, alternativa y terceros.", "Cuenta crédito-intereses-locales-valor-sobrante."),
    ]
    s.append(evidence_table(rows, ["Nodo", "Conocimiento / registro", "Remedio o pregunta", "Prueba a localizar"], styles, [25 * mm, 50 * mm, 50 * mm, 49 * mm]))
    s.append(Spacer(1, 5 * mm))
    s.append(card("Prueba capaz de cerrar el debate", "Expediente judicial certificado completo; agenda y registro del 13 de junio; instrucciones del administrador concursal; escritos y resoluciones sobre inspección/pericial; cuenta de crédito, intereses, locales, adjudicación y sobrante; restauración OB REM; mapa finca-posesión-uso-ingreso.", styles, "Lista de verificación", "gold"))
    s.append(PageBreak())

    add_heading(s, "04  /  COMPARADOR INPARSA", "Preguntas compartidas; hechos que no deben fusionarse.", "Inparsa es útil para estudiar cómo insolvencia, valoración, alternativa financiada y legalidad societaria pueden decidir un cambio de control. No prueba nada sobre Sun Park.", styles)
    comp = [
        ("Mecanismo", "Plan de reestructuración, capitalización y nueva financiación.", "Concurso prolongado, control material discutido y adjudicación al acreedor."),
        ("Premisa", "Vencimiento por cambio de control e insolvencia, discutidos por Inparsa.", "Crédito, responsabilidad máxima, intereses y sobrante discutidos."),
        ("Valor", "Valor de empresa, capital y activos con cifras contrapuestas.", "Tasaciones 2018, operación, cambio físico y valor posterior."),
        ("Alternativa", "Financiación para pago completo alegada por Inparsa.", "Salida ONA de 2018 con operador y dos vías financieras, sujeta a cierre."),
        ("Control", "Aproximadamente 71% post-reestructuración para Meru según sentencia publicada.", "Control material alegado en 2018; título formal en 2022; HNT/MYND después."),
        ("Ruta penal", "Examen provisional publicado; auto primario y resultado posterior no localizados.", "Alegaciones formales; ninguna decisión de culpabilidad."),
    ]
    s.append(evidence_table(comp, ["Dimensión", "Inparsa / Hoteles Beatriz", "Sun Park"], styles, [31 * mm, 71.5 * mm, 71.5 * mm]))
    s.append(Spacer(1, 5 * mm))
    s.append(card("Control negativo", "No se afirma el mismo juez, las mismas partes, el mismo plan ni una red común. La aparición de Cuatrecasas como asesor en Inparsa, y cualquier relación profesional histórica con el perímetro Sun Park acreditada por separado, no demostrarían un método ilícito común. Todo análisis de asesores exige encargo, deber, conocimiento, acto y efecto propios.", styles, "No asociación por proximidad", "gold"))
    s.append(PageBreak())

    add_heading(s, "05  /  UMBRAL PENAL", "Cuatro tipos; cuatro pruebas diferentes.", "La discrepancia, incluso intensa, no basta cuando una resolución permanece dentro de una interpretación jurídicamente defendible. El expediente no debe forzarse dentro de todos los tipos.", styles)
    thresholds = [
        ("CP 446", "Resolución injusta a sabiendas", "Exige resolución, injusticia en sentido penal y conocimiento. Falta decisiva: excluir una interpretación defendible y probar el nexo entre conocimiento y decisión."),
        ("CP 447", "Imprudencia grave / ignorancia inexcusable", "Exige resolución manifiestamente injusta causada por ese grado cualificado. No es sustituto de la apelación."),
        ("CP 448", "Negativa injustificada a juzgar", "Exige asunto concreto, deber de resolver y negativa sin causa legal. Una protección generalmente insuficiente no basta."),
        ("CP 449", "Retardo malicioso", "Exige demora provocada para obtener una finalidad ilegítima. La duración por sí sola no prueba finalidad."),
    ]
    for label, title, body in thresholds:
        s.append(card(title, body, styles, label, "teal"))
    s.append(card("Competencia y cauce", "El artículo 73.3.b LOPJ atribuye a la Sala de lo Civil y Penal del TSJ determinadas causas contra jueces y magistrados por actos en el ejercicio del cargo, salvo competencia del Tribunal Supremo. Los artículos 405 a 410 LOPJ regulan la responsabilidad penal judicial. El cauce exacto debe verificarse por un profesional con el expediente completo.", styles, "LOPJ", "gold"))
    s.append(PageBreak())

    add_heading(s, "06  /  LIBRO MAYOR DE AFIRMACIONES", "No todo tiene el mismo estado probatorio.", "Esta clasificación evita que una narración fuerte borre la diferencia entre documento, posición atribuida, controversia e información aún no localizada.", styles)
    s.append(mini_grid([
        ("Hechos documentados", "Hay un auto de 16 abril de 2018; una toma material está documentada el 7 junio; existe informe Irigoyen de 13 junio; hay decisiones y escritura/adjudicación de 2021-2022; DIP 2/2026 fue archivada; DI 169/2026 fue cerrada por el CGPJ."),
        ("Alegaciones atribuidas", "Marer atribuye conocimiento, tutela insuficiente, tratamiento incompatible de premisas, omisiones de prueba y una secuencia patrimonial que requiere investigación penal."),
        ("Discutido", "Autoría del acceso; conocimiento judicial preciso; viabilidad/cierre ONA; alcance OB REM; tratamiento de pericial; deuda, valor, sobrante y perímetro de terceros; significado de la contradicción de 2021."),
        ("No localizado", "Expediente certificado completo; acta/agenda 13 junio; instrucciones AC; cuenta reconciliada; auto primario TSJC en Inparsa; resultado público posterior; resolución de fondo sobre la alegación Sun Park."),
    ], styles))
    s.append(Spacer(1, 5 * mm))
    s.append(para("La pregunta más productiva no es '¿quién tiene razón?', sino: <b>¿qué documento contemporáneo permitiría excluir una explicación jurídica defendible o, por el contrario, hacer necesaria una investigación?</b>", styles["quote"]))
    s.append(card("Falsabilidad", "Una tesis seria debe poder perder. Un auto que delimitara y justificara el alcance; órdenes protectoras eficaces; una cuenta reconciliada; o una explicación documentada de la contradicción de 2021 podrían debilitarla. Un registro de conocimiento, remedio disponible y decisión incompatible sin explicación podría reforzarla.", styles, "Prueba negativa", "gold"))
    s.append(PageBreak())

    add_heading(s, "07  /  GUÍA PARA AUTORES", "Cinco historias que no exigen adoptar la acusación.", "El propósito editorial es reducir fricción, no obtener respaldo. Cada ángulo admite una conclusión crítica con Sun Park.", styles)
    angles = [
        ("01", "De resolución adversa a posible prevaricación", "Qué debe contener la prueba para cruzar el umbral sin criminalizar el recurso."),
        ("02", "Cuando la deuda se convierte en control", "Valoración, alternativas financiadas y supervisión en activos hoteleros canarios."),
        ("03", "Tutela mientras cambia el activo", "Posesión, acceso, prueba y valor de empresa durante el procedimiento."),
        ("04", "El límite de la masa", "Por qué el concurso de una sociedad no decide silenciosamente título y autoridad de terceros."),
        ("05", "Tres vías no equivalentes", "CGPJ, Fiscalía y querella judicial: objeto, umbral y resultado de cada una."),
    ]
    s.append(mini_grid([(no, f"<b>{title}</b><br/>{body}") for no, title, body in angles], styles))
    s.append(Spacer(1, 5 * mm))
    s.append(card("Por qué José Carlos González Vázquez es un lector natural", "Es socio mercantil/concursal de CECA Magán, profesor titular de Derecho Mercantil y autor de tres análisis públicos sobre Inparsa. Su método - secuencia procesal, insolvencia, valoración, alternativa financiada y control societario - señala las preguntas que un paquete serio debe permitir contestar. No se afirma que conozca, represente, respalde o comparta la tesis Sun Park.", styles, "Pista editorial", "teal"))
    s.append(PageBreak())

    add_heading(s, "08  /  GLOSARIO Y PREGUNTAS", "Términos que un artículo debe fijar antes de opinar.", "El mismo término puede describir cosas distintas en documentos distintos. La definición operacional debe acompañar a cada afirmación.", styles)
    s.append(mini_grid([
        ("CEXP", "Vehículo colectivo con procedencia dominical alegada desde 2008; su perímetro, contratos y autoridad no se presumen por el concurso de LPB."),
        ("CAM", "Acreedor y adjudicatario formal posterior. El dossier distingue el alcance del auto de abril de 2018 del título formal de 2022."),
        ("OB REM", "Operación registral/patrimonial de 28 noviembre 2018 cuya no convalidación posterior y restauración deben reconstruirse documentalmente."),
        ("Salida ONA", "Alternativa de operador y financiación relatada en junio de 2018; su viabilidad, condiciones y cierre siguen siendo cuestiones probatorias."),
        ("Prevaricación", "No equivale a error ni a revocación. Requiere el tipo aplicable, injusticia penal y el elemento subjetivo correspondiente."),
        ("Admisión provisional", "Descripción periodística del estado Inparsa; no equivale a apertura definitiva, procesamiento ni condena."),
    ], styles))
    s.append(Spacer(1, 5 * mm))
    s.append(para("Preguntas mínimas: ¿cuál era el perímetro judicial? ¿qué sabía el órgano y cuándo? ¿qué remedio concreto se pidió? ¿qué respuesta se dio? ¿qué explicación jurídica consta? ¿qué efecto material y patrimonial siguió? ¿qué prueba contemporánea permite una explicación alternativa?", styles["body"]))
    s.append(PageBreak())

    add_heading(s, "09  /  FUENTES Y DERECHO DE RESPUESTA", "Índice mínimo para comenzar la verificación.", "Los enlaces son puntos de entrada, no sustitutos del expediente certificado. Las fuentes de parte se identifican como tales.", styles)
    sources = [
        ("Código Penal, arts. 446-449", "https://www.boe.es/buscar/act.php?id=BOE-A-1995-25444", "BOE, texto consolidado; tipos penales."),
        ("LOPJ, arts. 73.3.b y 405-410", "https://www.boe.es/eli/es/lo/1985/07/01/6", "BOE, competencia y responsabilidad penal judicial."),
        ("CENDOJ - control negativo", "https://www.poderjudicial.es/search/sentencias/Prevaricacion/71/PUB", "La discrepancia y alegaciones nominativas no sustituyen indicios."),
        ("Nota Inparsa / Hoteles Beatriz", "https://sbu001monterecco.github.io/por-derecho/es/cuaderno-juridico/inparsa-hoteles-beatriz/", "Expediente público, versiones y preguntas abiertas."),
        ("La Razón, 13 febrero 2026", "https://www.larazon.es/economia/tsj-canarias-admite-tramite-provisional-querella-prevaricacion-juez-que-pretende-entregar-beatriz-hoteles-blantyre-capital_20260213698ed0459243cc133c45dc67.html", "Fuente secundaria sobre examen provisional TSJC."),
        ("Dossier toma material / ONA", "https://sbu001monterecco.github.io/por-derecho/es/toma-control-sun-park-7-junio-2018/", "Fuente de parte con documentos y estados probatorios."),
        ("DIP 2/2026", "https://sbu001monterecco.github.io/por-derecho/es/fiscalia-dip-2-2026/", "Documentos oficiales de incoación/archivo y error documental sobre estado de apelación."),
        ("Perfil CECA Magán", "https://www.cecamagan.com/abogados-socios/jose-carlos-gonzalez-vazquez", "Trayectoria pública de José Carlos González Vázquez."),
        ("González Vázquez - análisis 2024", "https://es.linkedin.com/pulse/la-denegaci%C3%B3n-de-homologaci%C3%B3n-del-plan-beatriz-ajmer-jos%C3%A9-carlos-wjulf", "Denegación inicial del plan Inparsa."),
        ("González Vázquez - partes I y II, 2026", "https://es.linkedin.com/pulse/el-caso-inparsa-hoteles-beatriz-ii-dudas-y-procesales-jos%C3%A9-carlos-zd98e", "Secuencia, insolvencia, valoración y control societario."),
    ]
    for i, (title, url, note) in enumerate(sources, 1):
        s.append(source_item(i, title, url, note, styles))
    s.append(Spacer(1, 4 * mm))
    s.append(card("Correcciones y respuesta", "Toda persona o entidad mencionada puede aportar documento, contexto, réplica o corrección. Se pide identificar la proposición concreta, la fuente, la fecha, el estado procesal y el alcance. Correo: <link href='mailto:sbu001@monterecco.com' color='#25766E'>sbu001@monterecco.com</link>. Hilo público moderado: <link href='https://github.com/sbu001monterecco/por-derecho/issues/7' color='#25766E'>GitHub issue 7</link>.", styles, "Derecho equivalente", "gold"))
    return s


def english_story(styles):
    s = []
    s.extend([
        Spacer(1, 36 * mm),
        para("JUDICIAL CONTROL  /  INSOLVENCY  /  CRIMINAL EVIDENCE", styles["cover_kicker"]),
        para("When does an adverse commercial result become more than merely adverse?", styles["cover_title"]),
        para("A documentary pack for lawyers, journalists and independent writers. Sun Park is tested against Inparsa / Hoteles Beatriz only as a methodological comparator.", styles["cover_deck"]),
        Spacer(1, 76 * mm),
        para("Edition 1  /  Sources checked: 13 August 2026<br/>Project Sun Rock - Legal Notebook<br/>Estimated reading time: 18 minutes", styles["cover_meta"]),
        PageBreak(),
    ])

    add_heading(s, "01  /  READING RULES", "One case opens the question; only the other case file can answer it.", "This pack does not seek endorsement. It separates outcome, source, allegation, inference, disputed point and missing evidence so a third party can confirm, refute or reframe the thesis.", styles)
    s.append(mini_grid([
        ("Inparsa", "On 13 February 2026, press reporting described provisional TSJC admission or examination. The report itself said a decision on opening an investigation was still required. No primary order or later public outcome was located."),
        ("Sun Park", "Gil Marer formally maintains that a sequence attributed to Judge Alberto López Villarrubia requires criminal investigation. No published judicial decision establishes guilt."),
        ("Relationship", "The cases involve different judges, parties and mechanisms. No common network, concerted action or institutional pattern is alleged."),
        ("Discipline / crime", "CGPJ discipline and criminal jurisdiction have different objects and thresholds. A disciplinary outcome does not decide Penal Code articles 446-449."),
    ], styles))
    s.append(Spacer(1, 5 * mm))
    s.append(card("The central rule", "A criminal complaint against another judge does not make one's own allegation true. Its narrower relevance is that criminal control of judicial conduct is a real legal route, requiring individualised evidence.", styles, "Comparator limit", "gold"))
    s.append(card("Attributed position", "Gil Marer maintains that specified acts, omissions and rulings, read as a sequence, cross the threshold requiring criminal investigation. This is his formally advanced allegation, not a conviction or judicial finding of guilt.", styles, "Sun Park", "teal"))
    s.append(PageBreak())

    add_heading(s, "02  /  CONTROL CHRONOLOGY", "Seven nodes an investigation could confirm or disprove.", "Accumulation does not prove intent. Each node requires its own evidence of knowledge, jurisdiction, available remedy, act or omission, effect and legal explanation.", styles)
    chronology = [
        ("16 APR 2018", "Order and scope", "The dossier says the order concerned LPB and did not confer possession of CEXP, Matkator or third-party assets on CAM."),
        ("7 JUN 2018", "Material control", "Contemporary evidence records broken access, chains, locks and exclusion. Authorship and judicial knowledge require separate proof."),
        ("13 JUN 2018", "ONA exit", "Daniel Irigoyen's report records meetings with judge and administrator about funder, operator and payment or deposit. It is not a court minute."),
        ("2018-2019", "OB REM", "28 November 2018 operation; later non-validation on 24 October 2019 according to the public dossier. Restitution and accounts remain open."),
        ("2020-2021", "Asset and evidence", "Alleged demolition/restriction, inspection and expert requests, and the RIC narrative before formal title."),
        ("15 OCT 2021", "Conflicting premise", "The dossier identifies two orders: one said an auction occurred, the other that it had not. Certified text and full context are required."),
        ("26 JAN-21 FEB 2022", "Adjudication", "The dossier says July material was admitted but treated as irrelevant; operational copies, deed and registration to CAM followed."),
    ]
    s.append(evidence_table(chronology, ["Date", "Node", "Record and evidential limit"], styles, [27 * mm, 38 * mm, 109 * mm]))
    s.append(Spacer(1, 5 * mm))
    s.append(card("Correct reading", "The chronology organises evidence; duration or accumulation does not itself establish illegitimate purpose. Each transition requires the contemporary record, applicable duty and causal explanation.", styles, "Inference control", "gold"))
    s.append(PageBreak())

    add_heading(s, "03  /  ACT-EVIDENCE MATRIX", "What must be closed node by node.", "The 'evidence to locate' column matters as much as the allegation: it identifies material capable of closing the issue either way.", styles)
    rows = [
        ("16 Apr 2018", "Order scope and LPB / third-party limits.", "How did wider material control arise?", "Order, instructions, execution map."),
        ("7 Jun 2018", "Contemporaneously documented takeover.", "Urgent protection of access, evidence and perimeter.", "Notices, calendar, filings, decisions, authorship."),
        ("13 Jun 2018", "Funded alternative reported by Irigoyen.", "Useful protection while payment/deposit was tested.", "Calendar, minute, filing, service, administrator report."),
        ("2018-2019", "OB REM and alleged non-validation.", "Registry, material and accounting restoration.", "Cancellation, restitution, proceeds and accounts."),
        ("2020-2021", "Works, access, expert evidence, RIC narrative.", "Preserve asset, evidence and bidding conditions.", "Certified request/objection/decision chronology."),
        ("15 Oct 2021", "Two incompatible public premises.", "Clarify before irreversible effects.", "Complete orders and correction record."),
        ("Jan-Feb 2022", "Official adjudication, deed and registry.", "Reconcile debt, value, alternative and third parties.", "Credit-interest-units-value-surplus account."),
    ]
    s.append(evidence_table(rows, ["Node", "Knowledge / record", "Remedy or question", "Evidence to locate"], styles, [25 * mm, 50 * mm, 50 * mm, 49 * mm]))
    s.append(Spacer(1, 5 * mm))
    s.append(card("Evidence capable of closing the debate", "Complete certified court file; 13 June calendar and record; insolvency administrator instructions; filings and rulings on inspection/expert evidence; credit, interest, units, adjudication and surplus account; OB REM restoration; property-possession-use-income map.", styles, "Verification list", "gold"))
    s.append(PageBreak())

    add_heading(s, "04  /  INPARSA COMPARATOR", "Shared questions; facts that must not be merged.", "Inparsa is useful for studying how insolvency, valuation, funded alternatives and corporate legality can determine a transfer of control. It proves nothing about Sun Park.", styles)
    comp = [
        ("Mechanism", "Restructuring plan, capitalisation and new financing.", "Long insolvency, disputed material control and creditor adjudication."),
        ("Premise", "Change-of-control maturity and insolvency disputed by Inparsa.", "Credit, maximum mortgage liability, interest and surplus disputed."),
        ("Value", "Enterprise, equity and asset values with competing figures.", "2018 valuations, operation, physical change and later value."),
        ("Alternative", "Full-payment financing alleged by Inparsa.", "2018 ONA operator and two financing routes, subject to conditions and close."),
        ("Control", "About 71% post-restructuring for Meru in the published judgment.", "Alleged material control in 2018; formal title in 2022; later HNT/MYND."),
        ("Criminal route", "Provisional examination reported; primary order and later outcome not located.", "Formal allegations; no finding of guilt."),
    ]
    s.append(evidence_table(comp, ["Dimension", "Inparsa / Hoteles Beatriz", "Sun Park"], styles, [31 * mm, 71.5 * mm, 71.5 * mm]))
    s.append(Spacer(1, 5 * mm))
    s.append(card("Negative control", "No common judge, parties, plan or network is alleged. Cuatrecasas appearing as adviser in Inparsa, and any separately evidenced historical professional relationship with the Sun Park perimeter, would not establish a shared unlawful method. Any adviser analysis requires its own retainer, duty, knowledge, act and effect.", styles, "No guilt by proximity", "gold"))
    s.append(PageBreak())

    add_heading(s, "05  /  CRIMINAL THRESHOLD", "Four offences; four different evidential tests.", "Even intense disagreement is insufficient where a decision remains within a legally tenable interpretation. The record should not be forced into every offence.", styles)
    thresholds = [
        ("PC 446", "Knowingly unjust judgment or decision", "Requires a decision, criminal-law injustice and knowledge. Critical gap: exclude a tenable legal interpretation and prove the link between knowledge and decision."),
        ("PC 447", "Gross negligence / inexcusable ignorance", "Requires a manifestly unjust decision caused by that qualified degree of fault. It is not a substitute for appeal."),
        ("PC 448", "Unjustified refusal to adjudicate", "Requires a specific matter, a duty to decide and refusal without lawful reason. Generally inadequate protection is insufficient."),
        ("PC 449", "Malicious delay", "Requires delay caused to achieve an illegitimate purpose. Duration alone does not prove purpose."),
    ]
    for label, title, body in thresholds:
        s.append(card(title, body, styles, label, "teal"))
    s.append(card("Jurisdiction and route", "LOPJ article 73.3(b) assigns certain criminal proceedings against judges and magistrates for acts in office to the TSJ Civil and Criminal Chamber, without prejudice to Supreme Court jurisdiction. Articles 405-410 address judicial criminal responsibility. Counsel must verify the exact route against the complete file.", styles, "LOPJ", "gold"))
    s.append(PageBreak())

    add_heading(s, "06  /  CLAIMS LEDGER", "Not every statement has the same evidential status.", "This classification prevents a strong narrative from erasing the difference between document, attributed position, disputed issue and material not yet located.", styles)
    s.append(mini_grid([
        ("Documented facts", "There is a 16 April 2018 order; a 7 June material takeover is documented; the Irigoyen 13 June report exists; 2021-2022 decisions and deed/adjudication exist; DIP 2/2026 was archived; CGPJ DI 169/2026 was closed."),
        ("Attributed allegations", "Marer alleges knowledge, inadequate protection, incompatible treatment of premises, evidential omissions and a property sequence requiring criminal investigation."),
        ("Disputed", "Takeover authorship; exact judicial knowledge; ONA viability/close; OB REM effect; expert-evidence treatment; debt, value, surplus and third-party perimeter; meaning of the 2021 contradiction."),
        ("Not located", "Complete certified file; 13 June minute/calendar; administrator instructions; reconciled account; primary TSJC Inparsa order; later public result; merits ruling on the Sun Park allegation."),
    ], styles))
    s.append(Spacer(1, 5 * mm))
    s.append(para("The productive question is not 'who is right?' but: <b>what contemporary document would exclude a tenable legal explanation or, conversely, make an investigation necessary?</b>", styles["quote"]))
    s.append(card("Falsifiability", "A reasoned order defining scope; effective protective directions; a reconciled account; or a documented explanation for the 2021 contradiction could weaken the thesis. A record of knowledge, available remedy and incompatible unexplained decision could strengthen it.", styles, "Negative evidence", "gold"))
    s.append(PageBreak())

    add_heading(s, "07  /  WRITER'S GUIDE", "Five stories that do not require adopting the allegation.", "The editorial aim is to reduce friction, not secure support. Every angle permits a conclusion critical of Sun Park.", styles)
    angles = [
        ("01", "From adverse decision to possible prevaricación", "What evidence must cross the threshold without criminalising an appeal."),
        ("02", "When debt becomes control", "Valuation, funded alternatives and supervision of Canary hotel assets."),
        ("03", "Protection while the asset changes", "Possession, access, evidence and going-concern value during proceedings."),
        ("04", "The boundary of the insolvency estate", "Why one company's insolvency does not silently decide third-party title and authority."),
        ("05", "Three non-equivalent routes", "CGPJ, prosecution service and judicial complaint: object, threshold and outcome."),
    ]
    s.append(mini_grid([(no, f"<b>{title}</b><br/>{body}") for no, title, body in angles], styles))
    s.append(Spacer(1, 5 * mm))
    s.append(card("Why José Carlos González Vázquez is a natural reader", "He is a CECA Magán corporate/insolvency partner, Commercial Law professor and author of three public Inparsa analyses. His method - procedural sequence, insolvency, valuation, funded alternative and corporate control - defines the questions a serious pack should answer. This does not suggest that he knows, represents, endorses or shares the Sun Park position.", styles, "Editorial lead", "teal"))
    s.append(PageBreak())

    add_heading(s, "08  /  GLOSSARY AND QUESTIONS", "Terms a writer should fix before reaching a view.", "The same label can describe different things in different records. Every claim needs an operational definition.", styles)
    s.append(mini_grid([
        ("CEXP", "Collective vehicle with an owner-derived provenance asserted from 2008; its perimeter, contracts and authority are not presumed from LPB's insolvency."),
        ("CAM", "Creditor and later formal adjudicatee. The dossier distinguishes the April 2018 order from formal 2022 title."),
        ("OB REM", "28 November 2018 registry/property operation whose alleged later non-validation and restoration require a documentary chain."),
        ("ONA exit", "Operator and financing alternative reported in June 2018; viability, conditions and closing remain evidential questions."),
        ("Prevaricación", "Not synonymous with error or reversal. It requires the applicable offence, criminal-law injustice and corresponding mental element."),
        ("Provisional admission", "A press description of Inparsa's status; not equivalent to definitive opening, charge or conviction."),
    ], styles))
    s.append(Spacer(1, 5 * mm))
    s.append(para("Minimum questions: what was the judicial perimeter? What did the court know and when? What specific remedy was sought? What response followed? What legal explanation is recorded? What material and property effect followed? What contemporary evidence supports an alternative explanation?", styles["body"]))
    s.append(PageBreak())

    add_heading(s, "09  /  SOURCES AND RIGHT OF REPLY", "A minimum index for independent verification.", "Links are entry points, not substitutes for the certified file. Party sources are identified as such.", styles)
    sources = [
        ("Spanish Penal Code, arts. 446-449", "https://www.boe.es/buscar/act.php?id=BOE-A-1995-25444", "BOE consolidated text; offences."),
        ("LOPJ, arts. 73.3(b) and 405-410", "https://www.boe.es/eli/es/lo/1985/07/01/6", "BOE; jurisdiction and judicial criminal responsibility."),
        ("CENDOJ negative control", "https://www.poderjudicial.es/search/sentencias/Prevaricacion/71/PUB", "Disagreement and named assertions do not replace evidence."),
        ("Inparsa / Hoteles Beatriz note", "https://sbu001monterecco.github.io/por-derecho/en/legal-notebook/inparsa-hoteles-beatriz/", "Public record, competing accounts and open questions."),
        ("La Razón, 13 February 2026", "https://www.larazon.es/economia/tsj-canarias-admite-tramite-provisional-querella-prevaricacion-juez-que-pretende-entregar-beatriz-hoteles-blantyre-capital_20260213698ed0459243cc133c45dc67.html", "Secondary report on provisional TSJC examination."),
        ("Material takeover / ONA dossier", "https://sbu001monterecco.github.io/por-derecho/en/sun-park-takeover-7-june-2018/", "Party source with documents and evidence labels."),
        ("DIP 2/2026", "https://sbu001monterecco.github.io/por-derecho/en/fiscalia-dip-2-2026/", "Official opening/closure records and documented appeal-status error."),
        ("CECA Magán profile", "https://www.cecamagan.com/abogados-socios/jose-carlos-gonzalez-vazquez", "José Carlos González Vázquez's public professional profile."),
        ("González Vázquez - 2024 analysis", "https://es.linkedin.com/pulse/la-denegaci%C3%B3n-de-homologaci%C3%B3n-del-plan-beatriz-ajmer-jos%C3%A9-carlos-wjulf", "Initial Inparsa plan refusal."),
        ("González Vázquez - 2026 parts I and II", "https://es.linkedin.com/pulse/el-caso-inparsa-hoteles-beatriz-ii-dudas-y-procesales-jos%C3%A9-carlos-zd98e", "Sequence, insolvency, valuation and corporate control."),
    ]
    for i, (title, url, note) in enumerate(sources, 1):
        s.append(source_item(i, title, url, note, styles))
    s.append(Spacer(1, 4 * mm))
    s.append(card("Corrections and response", "Every named person or entity may submit a document, context, reply or correction. Please identify the exact proposition, source, date, procedural status and scope. Email: <link href='mailto:sbu001@monterecco.com' color='#25766E'>sbu001@monterecco.com</link>. Moderated public thread: <link href='https://github.com/sbu001monterecco/por-derecho/issues/7' color='#25766E'>GitHub issue 7</link>.", styles, "Equal right", "gold"))
    return s


def build(filename, language, story_factory):
    styles = make_styles()
    output = OUT / filename
    frame = Frame(18 * mm, 17 * mm, 174 * mm, 260 * mm, leftPadding=0, rightPadding=0, topPadding=3 * mm, bottomPadding=2 * mm)
    template = PageTemplate(id="main", frames=[frame], onPage=lambda c, d: page_decorator(c, d, language))
    doc = BaseDocTemplate(
        str(output),
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=20 * mm,
        bottomMargin=17 * mm,
        title="Project Sun Rock - Judicial control writer pack",
        author="Project Sun Rock",
        subject="Documentary pack for independent legal analysis",
        creator="Project Sun Rock Legal Notebook",
    )
    doc.addPageTemplates([template])
    doc.build(story_factory(styles))
    copyfile(output, PUBLIC / filename)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    PUBLIC.mkdir(parents=True, exist_ok=True)
    build("paquete-autores-control-judicial-sun-park-inparsa-es.pdf", "es", spanish_story)
    build("legal-writer-pack-judicial-control-sun-park-inparsa-en.pdf", "en", english_story)


if __name__ == "__main__":
    main()
