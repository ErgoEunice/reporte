import streamlit as st
import pandas as pd
import io

# Configuración de la página
st.set_page_config(
    page_title="Levantamiento Etapa 3 - ERGOSOLAR",
    page_icon="Ergogo.png",
    layout="wide"
)

st.title("⚡ETAPA 3: Levantamiento Técnico en Techumbre y Eléctrico ")
st.write("Captura los datos técnicos de la visita de campo y genera el archivo Excel para tu expediente.")

# Crear pestañas organizadas para la captura de datos
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏠 1. Techumbre y Estructura",
    "🔋 2. Espacio Baterías",
    "🔌 3. Levantamiento Eléctrico",
    "🎛️ 4. Tableros e Interconexión",
    "⚠️ 5. Análisis de Riesgo"
])

# ---------------------------------------------------------
# PESTAÑA 1: TECHUMBRE Y ESTRUCTURAL
# ---------------------------------------------------------
with tab1:
    st.header("🏠 Levantamiento en Techumbre y Estructural")
    
    with st.expander("📋 Datos de Lámina y Translucida", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            tipo_techumbre = st.text_input("Tipo de Techumbre", value="Lámina engargolada")
            calibre_lamina = st.text_input("Calibre de Lámina", value="cal 24")
        with col2:
            largo_translucida = st.number_input("Largo Translucida (m)", value=0.0)
            ancho_translucida = st.number_input("Ancho Translucida (m)", value=0.0)

    with st.expander("📐 Dimensiones de Cresta"):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            alto_cresta = st.text_input("Alto de Cresta (cm)")
        with col2:
            ancho_cresta = st.text_input("Ancho de Cresta (cm)")
        with col3:
            dist_cresta = st.text_input("Distancia entre Crestas (cm)")
        with col4:
            med_valle = st.text_input("Medida de Valle (cm)")

    with st.expander("🏗️ Levantamiento Estructural"):
        st.subheader("Montenes")
        c1, c2, c3, c4, c5 = st.columns(5)
        dist_montenes = c1.text_input("Distancia montenes (m)")
        tipo_monten = c2.text_input("Tipo de monten", value="Tipo Z")
        largo_monten = c3.text_input("Largo monten (m)")
        ancho_monten = c4.text_input("Ancho monten (cm)")
        num_montenes = c5.number_input("N° de montenes", value=0, step=1)

        st.subheader("Columnas")
        c1, c2, c3, c4, c5 = st.columns(5)
        dist_columnas = c1.text_input("Distancia columnas (m)")
        tipo_columna = c2.text_input("Tipo de columna")
        largo_columna = c3.text_input("Largo columna (m)")
        ancho_columna = c4.text_input("Ancho columna (cm)")
        num_columnas = c5.number_input("N° de columnas", value=0, step=1)

        st.subheader("Vigas")
        c1, c2, c3, c4, c5 = st.columns(5)
        dist_vigas = c1.text_input("Distancia vigas (m)")
        tipo_viga = c2.text_input("Tipo de viga")
        largo_viga = c3.text_input("Largo viga (m)")
        ancho_viga = c4.text_input("Ancho viga (cm)")
        num_vigas = c5.number_input("N° de vigas", value=0, step=1)

# ---------------------------------------------------------
# PESTAÑA 2: ESPACIO PARA BATERÍAS
# ---------------------------------------------------------
with tab2:
    st.header("🔋 Espacio para Baterías (BESS)")
    col1, col2 = st.columns(2)
    with col1:
        temp_ambiente = st.text_input("Temperatura ambiente (°C)")
        tipo_terreno = st.selectbox("Tipo de terreno", ["Asfalto", "Concreto", "Tierra/Pasto", "Otro"])
        desnivel = st.radio("¿El terreno cuenta con deformación o desnivel?", ["No", "Si"])
    with col2:
        espacio_in_out = st.selectbox("Espacio en:", ["Exterior", "Interior"])
        medidas_baterias = st.text_input("Medidas L x A disponibles")
        instalaciones_adicionales = st.text_input("Instalaciones adicionales cercas (gas, agua, etc.)")

    factores_amb = st.multiselect(
        "Factores ambientales presentes:",
        ["Corrosión", "Humedad", "Salinidad", "Polvo", "Ninguno"]
    )

# ---------------------------------------------------------
# PESTAÑA 3: LEVANTAMIENTO ELÉCTRICO
# ---------------------------------------------------------
with tab3:
    st.header("🔌 Subestación, Planta de Emergencia e ITM")
    col1, col2 = st.columns(2)
    with col1:
        tipo_se = st.text_input("Tipo de subestación", value="Encapsulada")
        cap_se = st.text_input("Capacidad de subestación (kVA)")
        voltaje_mt_bt = st.text_input("Voltaje Baja / Media Tensión")
        planta_em = st.radio("¿Cuenta con planta de emergencia?", ["No", "Si"])
        tipo_planta = st.text_input("Tipo de planta de emergencia", value="Diesel")
        cap_planta = st.text_input("Capacidad de planta (kW)")
    
    with col2:
        filtro_arm = st.radio("¿Tiene filtro de armónicos?", ["No", "Si"])
        banco_cap = st.radio("¿Cuenta con banco de capacitores?", ["No", "Si"])
        tablero_respaldo = st.radio("¿Tiene tablero de respaldo?", ["No", "Si"])
        cap_barras = st.text_input("Capacidad de barras del tablero")

    st.subheader("ITM Principal")
    col_itm1, col_itm2 = st.columns(2)
    with col_itm1:
        calibre_itm = st.text_input("Calibre de conductores alimentadores")
        material_itm = st.selectbox("Material del conductor", ["Cobre", "Aluminio"])
    with col_itm2:
        tipo_canalizacion = st.text_input("Tipo de canalización")
        tamano_canalizacion = st.text_input("Tamaño de canalización")

# ---------------------------------------------------------
# PESTAÑA 4: TABLEROS DE INTERCONEXIÓN
# ---------------------------------------------------------
with tab4:
    st.header("🎛️ Opciones de Tableros de Interconexión")
    
    tablero_sel = st.selectbox("Selecciona Tablero a Capturar", ["Tablero 1", "Tablero 2", "Tablero 3"])
    
    col1, col2 = st.columns(2)
    with col1:
        modelo_tab = st.text_input(f"Modelo ({tablero_sel})")
        cap_tab = st.text_input(f"Capacidad ({tablero_sel})")
        voltaje_tab = st.text_input(f"Voltaje ({tablero_sel})")
        fases_hilos = st.text_input(f"Fases e hilos ({tablero_sel})")
        itm_principal_tab = st.text_input(f"ITM Principal ({tablero_sel})")
    with col2:
        proviene_de = st.text_input(f"Proviene de ({tablero_sel})")
        distancia_tab = st.text_input(f"Distancia ({tablero_sel})")
        espacios_disp = st.radio(f"¿Cuenta con espacios disponibles? ({tablero_sel})", ["Si", "No"])
        num_espacios = st.number_input("¿Cuántos espacios?", value=0, step=1)
        
    st.subheader("Normativa y Estado del Tablero")
    cumple_color = st.checkbox("Respeta código de colores", value=True)
    cerrado_correcto = st.checkbox("El tablero está cerrado correctamente", value=True)
    identificado = st.checkbox("Se encuentra debidamente identificado", value=True)
    comentarios_tablero = st.text_area("Comentarios adicionales del tablero")

# ---------------------------------------------------------
# PESTAÑA 5: ANÁLISIS DE RIESGO Y DESCARGA
# ---------------------------------------------------------
with tab5:
    st.header("⚠️ Análisis de Riesgo")
    
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        riesgo_detectado = st.text_input("Material / Actividad / Elemento de riesgo detectado")
        prob_falla = st.slider("Probabilidad de Falla (1 Muy baja - 5 Muy alta)", 1, 5, 1)
    with col_r2:
        impacto_peligro = st.slider("Impacto del Peligro (1 Muy bajo - 5 Muy alto)", 1, 5, 1)
        plan_mitigacion = st.text_area("Plan de mitigación")

    nivel_calculado = prob_falla * impacto_peligro
    
    if nivel_calculado <= 4:
        st.success(f"Nivel de Riesgo Calculado: {nivel_calculado} - BAJO")
    elif nivel_calculado <= 12:
        st.warning(f"Nivel de Riesgo Calculado: {nivel_calculado} - MODERADO")
    else:
        st.error(f"Nivel de Riesgo Calculado: {nivel_calculado} - ALTO")

    st.markdown("---")
    st.subheader("📄 Generar y Descargar Archivo Excel")

    # Función para estructurar y exportar los datos a Excel
    def generar_excel_etapa3():
        output = io.BytesIO()
        
        # Crear estructuras de datos por sección
        data_techumbre = {
            "Concepto": ["Tipo de Techumbre", "Calibre Lámina", "Largo Translucida (m)", "Ancho Translucida (m)", 
                         "Alto Cresta (cm)", "Ancho Cresta (cm)", "Distancia Cresta (cm)", "Medida Valle (cm)"],
            "Valor": [tipo_techumbre, calibre_lamina, largo_translucida, ancho_translucida,
                      alto_cresta, ancho_cresta, dist_cresta, med_valle]
        }
        
        data_estructura = {
            "Elemento": ["Montenes", "Columnas", "Vigas"],
            "Tipo": [tipo_monten, tipo_columna, tipo_viga],
            "Distancia (m)": [dist_montenes, dist_columnas, dist_vigas],
            "Largo (m)": [largo_monten, largo_columna, largo_viga],
            "Ancho (cm)": [ancho_monten, ancho_columna, ancho_viga],
            "Cantidad": [num_montenes, num_columnas, num_vigas]
        }
        
        data_electrico = {
            "Parametro": ["Tipo Subestación", "Capacidad SE", "Voltaje BT/MT", "Planta Emergencia", "Tipo Planta", 
                          "Capacidad Planta", "Calibre Alimentadores ITM", "Material ITM", "Tipo Canalización"],
            "Resultado": [tipo_se, cap_se, voltaje_mt_bt, planta_em, tipo_planta, 
                          cap_planta, calibre_itm, material_itm, tipo_canalizacion]
        }
        
        data_riesgo = {
            "Riesgo Detectado": [riesgo_detectado],
            "Probabilidad (1-5)": [prob_falla],
            "Impacto (1-5)": [impacto_peligro],
            "Nivel de Riesgo": [nivel_calculado],
            "Plan de Mitigación": [plan_mitigacion]
        }

        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            pd.DataFrame(data_techumbre).to_excel(writer, sheet_name='Techumbre', index=False)
            pd.DataFrame(data_estructura).to_excel(writer, sheet_name='Estructura', index=False)
            pd.DataFrame(data_electrico).to_excel(writer, sheet_name='Eléctrico', index=False)
            pd.DataFrame(data_riesgo).to_excel(writer, sheet_name='Análisis de Riesgo', index=False)

        output.seek(0)
        return output

    excel_file = generar_excel_etapa3()

    st.download_button(
        label="📥 Descargar Reporte Etapa 3 en Excel (.xlsx)",
        data=excel_file,
        file_name="Levantamiento_Etapa3_Completado.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        type="primary"
    )
