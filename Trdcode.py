import streamlit as st
import io
import os
from PIL import Image

# Librerías para generación de PDF con ReportLab
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

# ==========================================
# 1. CONFIGURACIÓN DE PÁGINA Y COLORES ERGO SOLAR
# ==========================================
st.set_page_config(
    page_title="Reportes de Mantenimiento | Ergo Solar",
    page_icon="☀️",
    layout="wide"
)

# Definición Hexadecimal de Colores Corporativos
COLOR_NARANJA = "#ff5e00"
COLOR_NARANJA_CLARO = "#ffae7f"
COLOR_AZUL = "#001489"
COLOR_GRIS_OSCURO = "#686666"
COLOR_GRIS_CLARO = "#e0e0e0"

# Inyección de estilos CSS para la app de Streamlit (Sin uso de negro)
st.markdown(f"""
    <style>
    /* Estilos generales */
    body, .stApp {{
        background-color: #e0e0e0;
        color: {COLOR_AZUL};
    }}
    h1, h2, h3, h4, h5, h6 {{
        color: {COLOR_AZUL} !important;
        font-weight: 700;
    }}
    /*Color de etiquetas de ingreso*/
    .stWidgetLabel p, label, .stWidgetLabel label {{
        color: {COLOR_GRIS_OSCURO} !important;  
        font-weight: bold !important;
        font-size: 15px !important;
    }}
    /* Botones primarios y secundarios */
    .stButton>button {{
        background-color: {COLOR_NARANJA};
        color:  white !important;
        border-radius: 6px;
        border: none;
        font-weight: bold;
    }}
    .stButton>button:hover {{
        background-color: {COLOR_NARANJA_CLARO};
        color: {COLOR_AZUL} !important;
    }}
     /* Encabezados de secciones */ 
    .section-header 
    {{ 
        border-left: 5px solid {COLOR_NARANJA}; 
        padding-left: 15px !important; 
        margin-top: 30px !important;  
        margin-bottom: 30px;
    }}
    /* Tarjetas de registro */
    .card {{
        background-color: white;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid {COLOR_GRIS_CLARO};
        margin-bottom: 15px;
    }}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. LOGIC Y PLANTILLAS DE PDF (REPORTLAB)
# ==========================================

class NumberedCanvas(canvas.Canvas):
    """
    Canvas personalizado para controlar encabezados, pies de página
    y numeración de páginas según los requerimientos de Ergo Solar.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        
        # --- ENCABEZADO ---
        if self._pageNumber > 1:
            # Logo en la esquina superior izquierda
            if os.path.exists("ErgoSolar_logo.png"):
                self.drawImage("ErgoSolar_logo.png", 36, 740, width=120, height=40, preserveAspectRatio=True, mask='auto')
            
            # Texto "Asset Management" en la esquina superior derecha
            self.setFont("Helvetica-Bold", 11)
            self.setFillColor(colors.HexColor(COLOR_AZUL))
            self.drawRightString(576, 755, "Asset Management")
            
            # Línea divisoria
            self.setStrokeColor(colors.HexColor(COLOR_NARANJA))
            self.setLineWidth(1)
            self.line(36, 730, 576, 730)

        # --- PIE DE PÁGINA (Todas las páginas) ---
        if os.path.exists("ErgoPieReporte.png"):
            self.drawImage("ErgoPieReporte.png", 36, 15, width=540, height=35, preserveAspectRatio=True, mask='auto')
        else:
            # Pie alternativo en caso de no existir la imagen
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor(COLOR_GRIS_OSCURO))
            self.drawString(36, 20, "Ergo Solar - Soluciones en Energía Fotovoltaica y Eficiencia Energética")
            self.drawRightString(576, 20, f"Página {self._pageNumber} de {page_count}")
            
        self.restoreState()


def generar_pdf_reporte(datos):
    """Genera el documento PDF basado en los datos ingresados en la App."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=54,
        bottomMargin=54
    )
    
    story = []
    
    # Estilos
    styles = getSampleStyleSheet()
    
    style_titulo = ParagraphStyle(
        'TituloCustom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=colors.HexColor(COLOR_AZUL),
        spaceAfter=10
    )
    
    style_subtitulo = ParagraphStyle(
        'SubtituloCustom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor(COLOR_AZUL),
        spaceBefore=12,
        spaceAfter=6
    )
    
    style_body = ParagraphStyle(
        'BodyCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor(COLOR_GRIS_OSCURO)
    )
    
    style_caption = ParagraphStyle(
        'CaptionCustom',
        parent=styles['Italic'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=10,
        alignment=1, # Centrado
        textColor=colors.HexColor(COLOR_GRIS_OSCURO),
        spaceBefore=4,
        spaceAfter=8
    )

    # Contador global de ilustraciones para rotulado automático
    contador_ilustraciones = 1

    # --- PÁGINA 1: BANNER DE ENCABEZADO ---
    if os.path.exists("BannerMantenimiento.png"):
        story.append(RLImage("BannerMantenimiento.png", width=540, height=100, preserveAspectRatio=True))
        story.append(Spacer(1, 15))

    # --- 1. INFORMACIÓN DEL CLIENTE ---
    story.append(Paragraph("REPORTE DE MANTENIMIENTO PREVENTIVO / CORRECTIVO", style_titulo))
    
    data_cliente = [
        [Paragraph("<b>Planta:</b>", style_body), Paragraph(datos['info_cliente']['planta'], style_body),
         Paragraph("<b>Fecha:</b>", style_body), Paragraph(str(datos['info_cliente']['fecha']), style_body)],
        [Paragraph("<b>Dirección:</b>", style_body), Paragraph(datos['info_cliente']['direccion'], style_body),
         Paragraph("<b>Técnico:</b>", style_body), Paragraph(datos['info_cliente']['tecnico'], style_body)]
    ]
    
    tabla_cliente = Table(data_cliente, colWidths=[1.1*inch, 2.7*inch, 0.9*inch, 2.8*inch])
    tabla_cliente.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FFFFFF")),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.HexColor(COLOR_GRIS_OSCURO)),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor(COLOR_GRIS_CLARO)),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor(COLOR_GRIS_CLARO)),
    ]))
    story.append(tabla_cliente)
    story.append(Spacer(1, 15))

    # --- 2. INSPECCIÓN INICIAL DEL SISTEMA ---
    story.append(Paragraph("1. Inspección Inicial del Sistema", style_subtitulo))
    if datos['inspecciones']:
        for idx, obs in enumerate(datos['inspecciones']):
            texto_obs = f"<b>Observación {idx+1}: {obs['titulo']}</b><br/>{obs['descripcion']}"
            story.append(Paragraph(texto_obs, style_body))
            story.append(Spacer(1, 4))
            
            if obs['foto'] is not None:
                img_temp = Image.open(obs['foto'])
                img_temp.thumbnail((350, 250))
                img_buffer = io.BytesIO()
                img_temp.save(img_buffer, format='PNG')
                img_buffer.seek(0)
                
                story.append(RLImage(img_buffer, width=img_temp.width * 0.7, height=img_temp.height * 0.7))
                
                # Rotulado de la Ilustración
                caption_text = f"Ilustración #{contador_ilustraciones}"
                if obs['pie']:
                    caption_text += f": {obs['pie']}"
                story.append(Paragraph(caption_text, style_caption))
                contador_ilustraciones += 1
            story.append(Spacer(1, 8))
    else:
        story.append(Paragraph("No se registraron observaciones iniciales.", style_body))

    story.append(Spacer(1, 10))

    # --- 3. ACTIVIDADES REALIZADAS ---
    story.append(Paragraph("2. Actividades Realizadas", style_subtitulo))
    if datos['actividades']:
        for idx, act in enumerate(datos['actividades']):
            texto_act = f"<b>Actividad {idx+1}: {act['titulo']}</b><br/>{act['descripcion']}"
            story.append(Paragraph(texto_act, style_body))
            story.append(Spacer(1, 4))
            
            # Galería de fotos para actividades (máximo 10)
            if act['fotos']:
                for foto_item in act['fotos']:
                    if foto_item['archivo'] is not None:
                        img_temp = Image.open(foto_item['archivo'])
                        img_temp.thumbnail((350, 250))
                        img_buffer = io.BytesIO()
                        img_temp.save(img_buffer, format='PNG')
                        img_buffer.seek(0)
                        
                        story.append(RLImage(img_buffer, width=img_temp.width * 0.7, height=img_temp.height * 0.7))
                        
                        # Rotulado
                        caption_text = f"Ilustración #{contador_ilustraciones}"
                        if foto_item['pie']:
                            caption_text += f": {foto_item['pie']}"
                        story.append(Paragraph(caption_text, style_caption))
                        contador_ilustraciones += 1
            story.append(Spacer(1, 8))
    else:
        story.append(Paragraph("No se registraron actividades adicionales.", style_body))

    story.append(Spacer(1, 10))

    # --- 4. RESULTADOS ---
    story.append(Paragraph("3. Resultados de Mediciones", style_subtitulo))
    tabla_res_data = [
        [Paragraph("<b>Medición</b>", style_body), Paragraph("<b>Valor</b>", style_body), 
         Paragraph("<b>Criterio</b>", style_body), Paragraph("<b>Conclusión</b>", style_body)]
    ]
    
    for row in datos['resultados']:
        tabla_res_data.append([
            Paragraph(row['medicion'], style_body),
            Paragraph(row['valor'], style_body),
            Paragraph(row['criterio'], style_body),
            Paragraph(row['conclusion'], style_body)
        ])
        
    tabla_resultados = Table(tabla_res_data, colWidths=[2.2*inch, 1.5*inch, 1.8*inch, 2.0*inch])
    tabla_resultados.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor(COLOR_AZUL)),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor(COLOR_GRIS_CLARO)),
    ]))
    
    # Cambiar texto del encabezado de la tabla a color blanco
    style_header_table = ParagraphStyle('HeaderTable', parent=style_body, textColor=colors.white, fontName='Helvetica-Bold')
    tabla_res_data[0] = [
        Paragraph("Medición", style_header_table),
        Paragraph("Valor", style_header_table),
        Paragraph("Criterio", style_header_table),
        Paragraph("Conclusión", style_header_table)
    ]
    
    story.append(tabla_resultados)
    story.append(Spacer(1, 15))

    # --- 5. CONCLUSIÓN ---
    story.append(Paragraph("4. Dictamen y Conclusión Final", style_subtitulo))
    story.append(Paragraph(datos['dictamen'] if datos['dictamen'] else "Sin dictamen registrado.", style_body))

    # Construir PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    buffer.seek(0)
    return buffer


# ==========================================
# 3. INTERFAZ EN STREAMLIT
# ==========================================

# Logo superior en Streamlit
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(SCRIPT_DIR, "Ergologo.png")

# Logo superior en Streamlit
col_logo, col_vacia = st.columns([2, 3])
with col_logo:
    st.image(LOGO_PATH, use_container_width=True)

st.title("GENERADOR AUTOMÁTICO DE REPORTES DE MANTENIMIENTO")
st.markdown("<p style='color: #686666;'>Captura de información en tiempo real para la generación del reporte técnico.</p>", unsafe_allow_html=True)

# Inicializar Estados del Formulario (Session State)
if 'num_observaciones' not in st.session_state:
    st.session_state.num_observaciones = 1

if 'num_actividades' not in st.session_state:
    st.session_state.num_actividades = 1

# --- SECCIÓN 1: INFORMACIÓN DEL CLIENTE ---
st.markdown("<h3 class='section-header'>1. Información del Cliente</h3>", unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    planta = st.text_input("Nombre de la Planta", placeholder="Ej. Planta Solar Metales")
    direccion = st.text_area("Dirección", placeholder="Ej. Av. De las Industrias #102, C.P. 72000")

with col2:
    fecha = st.date_input("Fecha de Mantenimiento")
    tecnico = st.text_input("Nombre del Técnico", placeholder="Ej. Ing. Carlos Pérez")

# --- SECCIÓN 2: INSPECCIÓN INICIAL DEL SISTEMA ---
st.markdown("<h3 class='section-header'>2. Inspección Inicial del Sistema</h3>", unsafe_allow_html=True)
st.info("Agrega las observaciones detectadas al inicio del mantenimiento.")

inspecciones_data = []

for i in range(st.session_state.num_observaciones):
    with st.container():
        st.markdown(f"**Observación #{i+1}**")
        col_obs1, col_obs2 = st.columns([2, 1])
        
        with col_obs1:
            tit_obs = st.text_input(f"Observación #{i+1}", key=f"obs_title_{i}")
            desc_obs = st.text_area(f"Descripción #{i+1}", key=f"obs_desc_{i}")
        
        with col_obs2:
            foto_obs = st.file_uploader(f"Fotografía / Evidencia #{i+1}", type=["jpg", "png", "jpeg"], key=f"obs_foto_{i}")
            pie_obs = st.text_input(f"Pie de Foto #{i+1}", key=f"obs_pie_{i}")
            
        inspecciones_data.append({
            'titulo': tit_obs,
            'descripcion': desc_obs,
            'foto': foto_obs,
            'pie': pie_obs
        })
        st.container()

if st.button("➕ Agregar Otra Observación", key="add_obs"):
    st.session_state.num_observaciones += 1
    st.rerun()

# --- SECCIÓN 3: ACTIVIDADES REALIZADAS ---
st.markdown("<h3 class='section-header'>3. Actividades Realizadas</h3>", unsafe_allow_html=True)

actividades_data = []

for j in range(st.session_state.num_actividades):
    with st.container():
        st.markdown(f"**Actividad #{j+1}**")
        tit_act = st.text_input(f"Actividad Realizada #{j+1}", key=f"act_title_{j}")
        desc_act = st.text_area(f"Descripción de la Actividad #{j+1}", key=f"act_desc_{j}")
        
        st.markdown("*Evidencias Fotográficas (Máximo 10 por actividad)*")
        fotos_actividad = []
        
        cols_fotos = st.columns(2)
        for k in range(10):
            col_target = cols_fotos[k % 2]
            with col_target:
                foto_file = st.file_uploader(f"Foto {k+1} para Actividad #{j+1}", type=["jpg", "png", "jpeg"], key=f"act_foto_{j}_{k}")
                pie_file = st.text_input(f"Pie de Foto {k+1} (Act. #{j+1})", key=f"act_pie_{j}_{k}")
                if foto_file is not None:
                    fotos_actividad.append({'archivo': foto_file, 'pie': pie_file})
        
        actividades_data.append({
            'titulo': tit_act,
            'descripcion': desc_act,
            'fotos': fotos_actividad
        })
        st.container()

if st.button("➕ Agregar Otra Actividad", key="add_act"):
    st.session_state.num_actividades += 1
    st.rerun()

# --- SECCIÓN 4: RESULTADOS ---
st.markdown("<h3 class='section-header'>4. Resultados</h3>", unsafe_allow_html=True)
st.caption("Completa los valores medidos en campo y tus conclusiones técnicas.")

# Filas predefinidas requeridas
filas_medicion = [
    "Voltaje de circuito en corriente alterna",
    "Voltaje de circuito abierto por cadena",
    "Voltaje de fallo a tierra"
]

resultados_data = []

for idx, medicion_nombre in enumerate(filas_medicion):
    st.markdown(f"**{medicion_nombre}**")
    c1, c2, c3 = st.columns(3)
    with c1:
        val = st.text_input("Valor", key=f"val_{idx}")
    with c2:
        crit = st.text_input("Criterio", key=f"crit_{idx}")
    with c3:
        conc = st.text_input("Conclusión", key=f"conc_{idx}")
        
    resultados_data.append({
        'medicion': medicion_nombre,
        'valor': val,
        'criterio': crit,
        'conclusion': conc
    })

# --- SECCIÓN 5: CONCLUSIÓN ---
st.markdown("<h3 class='section-header'>5. Conclusión</h3>", unsafe_allow_html=True)
dictamen = st.text_area("Dictamen del Mantenimiento", placeholder="Escribe aquí el dictamen técnico final...")

# --- GENERACIÓN DEL REPORT PDF ---
st.divider()

col_btn1, col_btn2 = st.columns([1, 2])

with col_btn1:
    if st.button("GENERAR PDF", type="primary", use_container_width=True):
        if not planta or not tecnico:
            st.error("Por favor completa al menos el nombre de la planta y del técnico.")
        else:
            # Estructurar todo el objeto de datos
            datos_totales = {
                'info_cliente': {
                    'planta': planta,
                    'direccion': direccion,
                    'fecha': fecha,
                    'tecnico': tecnico
                },
                'inspecciones': inspecciones_data,
                'actividades': actividades_data,
                'resultados': resultados_data,
                'dictamen': dictamen
            }
            
            # Procesar el archivo en memoria
            pdf_bytes = generar_pdf_reporte(datos_totales)
            
            st.success("¡Reporte generado con éxito!")
            st.download_button(
                label="📥 Descargar Reporte en PDF",
                data=pdf_bytes,
                file_name=f"Reporte_Mantenimiento_{planta.replace(' ', '_')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )