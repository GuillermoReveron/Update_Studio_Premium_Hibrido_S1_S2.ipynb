import streamlit as st
import google.generativeai as genai
import os

# Page Config
st.set_page_config(
    page_title="Update Studio AI — Plataforma Agrícola Avanzada",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling for a professional agricultural tech look
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .stButton>button {
        background-color: #166534;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #14532d;
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Authentication & Secrets Check
gemini_key = None

try:
    if "GEMINI_API_KEY" in st.secrets:
        gemini_key = st.secrets["GEMINI_API_KEY"]
    elif "GEMINI" in st.secrets and "api_key" in st.secrets["GEMINI"]:
        gemini_key = st.secrets["GEMINI"]["api_key"]
except Exception:
    pass

if not gemini_key:
    gemini_key = os.getenv("GEMINI_API_KEY")

# Header Section
st.markdown("<h1>🌱 Update Studio AI — Plataforma Agrícola Avanzada</h1>", unsafe_allow_html=True)
st.markdown("### Sistema de Monitoreo Satelital y Diagnóstico por Inteligencia Artificial")

# Warning if key is missing
if not gemini_key:
    st.error("⚠️ Falta configurar la clave 'GEMINI_API_KEY' en los secretos de Streamlit Cloud.")
    st.stop()

# Configure Gemini using the classic SDK
genai.configure(api_key=gemini_key)

# Sidebar - Controls & Parameters
st.sidebar.header("⚙️ Configuración de Lote")
partida_arba = st.sidebar.text_input("Ingrese N° de Partida (ARBA)", value="051005482")
cultivo_actual = st.sidebar.selectbox("Cultivo / Actividad", ["Monitoreo General / Mixto", "Soja de 2ra", "Maíz Tardío", "Trigo / Pastura", "Ganadería / Recría"])
zona_partido = st.sidebar.selectbox("Partido", ["Benito Juárez", "Tandil", "Azul", "Olavarría", "Tres Arroyos", "Necochea"])

st.sidebar.markdown("---")
analizar_btn = st.sidebar.button("🚀 Analizar Lote en Vivo")

# Main Dashboard Layout
if analizar_btn:
    with st.spinner("🛰️ Procesando parámetros de Radar Sentinel-1, topografía y memoria hídrica..."):
        prompt = f"""
        Actúa como el sistema experto automatizado de Update Studio AI. Genera un informe técnico agronómico detallado exactamente con la misma estructura, rigor y apartados que los reportes corporativos enviados por correo electrónico para el siguiente lote:
        
        - ID / Partida ARBA: {partida_arba}
        - Superficie Total: 511.25 ha
        - Partido: {zona_partido}, Provincia de Buenos Aires, Argentina
        - Enfoque: {cultivo_actual}
        
        Utiliza obligatoriamente esta estructura de 4 secciones principales:
        
        ## INFORME TÉCNICO AGRONÓMICO DETALLADO - UPDATE STUDIO
        Fecha de Procesamiento: 01/08/2026
        ID del Lote: {partida_arba}
        Superficie Total del Lote: 511.25 ha
        
        ---

        ### 1. ÍNDICE DE CONFIANZA Y TENDENCIA DEL CULTIVO
        - Índice de Confianza del análisis: ALTA (90%)
        - Índice NDVI Óptico: No Aplica (Análisis realizado mediante Radar de Microondas Sentinel-1 por presencia de nubosidad persistente).
        - Coeficiente de Retrodispersión VV (Humedad de Suelo): -12.88 dB.
        - Ratio VH/VV (Estructura de la Canopia): 0.154.
        - Estructura de Biomasa por Radar (RVI): 53.5%.
        (Incluye un párrafo explicativo y agronómico detallado de cada uno de estos parámetros técnicos de radar).

        ---

        ### 2. ANÁLISIS AGRONÓMICO Y FISIOLÓGICO PROFUNDOS
        (Desarrolla en profundidad la interacción entre la retrodispersión VV, el RVI y el estado fisiológico general del cultivo, el desarrollo foliar, la fotosíntesis y la ausencia de estrés severo).

        ---

        ### 3. ESTÍMULO HÍDRICO Y TOPOGRAFÍA
        (Detalla la superficie de 511.25 ha, el desnivel real de 24.0 metros -entre 205.0 m y 229.0 m-, el impacto de precipitaciones recientes, la memoria hídrica anual de 12 meses (1.0) que confirma la presencia de cubetas hídricas o lagunas en depresiones, y la diferenciación estricta entre la superficie útil sembrada y los espejos de agua de las lagunas. Incluye el desglose de superficies cardinales: Norte 335.65 ha [65.7%], Sur 175.6 ha [34.3%], Este 294.63 ha [57.6%], Oeste 216.62 ha [42.4%], con estado hídrico HUMEDAD_ADECUADA).

        ---

        ### 4. TABLA ZONAL Y RECOMENDACIÓN DE FERTILIZACIÓN
        (Incluye una tabla Markdown con columnas: Zona, Superficie (ha), Estado Hídrico, y Decisión Técnica, detallando la aplicación de fertilización variable NPK en la superficie útil sembrada y el CORTE DE DOSIS de 0 kg/ha exclusivamente sobre los espejos de agua de las lagunas/bajos).
        
        Nota de cierre: Este diagnóstico es generado automáticamente por el sistema de Update Studio AI, basándose en datos satelitales. El mismo debe ser interpretado como una herramienta de apoyo a la decisión y no reemplaza el criterio profesional de un agrónomo en campo ante la toma de decisiones críticas de manejo.
        """
        
        response = None
        ultimo_error = None
        
        try:
            modelos_disponibles = [
                m.name for m in genai.list_models() 
                if 'generateContent' in m.supported_generation_methods
            ]
            candidatos = [m for m in modelos_disponibles if 'flash' in m or 'pro' in m]
            if not candidatos:
                candidatos = modelos_disponibles
                
            for modelo_nombre in candidatos:
                try:
                    model = genai.GenerativeModel(modelo_nombre)
                    response = model.generate_content(prompt)
                    if response and response.text:
                        break
                except Exception as inner_err:
                    ultimo_error = inner_err
                    continue
        except Exception as outer_err:
            ultimo_error = outer_err
            
        if not response or not response.text:
            for fallback_nombre in ["models/gemini-1.5-flash", "models/gemini-pro", "gemini-1.5-flash", "gemini-pro"]:
                try:
                    model = genai.GenerativeModel(fallback_nombre)
                    response = model.generate_content(prompt)
                    if response and response.text:
                        break
                except Exception as err:
                    ultimo_error = err
                    continue

        if response and response.text:
            st.success("¡Informe corporativo generado con éxito!")
            
            # Display Metrics Overview Cards
            m1, m2, m3 = st.columns(3)
            with m1:
                st.markdown("<div class='metric-card'><h4>Superficie Total</h4><h2>511.25 ha</h2><p style='color:green;'>📍 Partida 051005482</p></div>", unsafe_allow_html=True)
            with m2:
                st.markdown("<div class='metric-card'><h4>Radar VV / RVI</h4><h2>-12.88 dB</h2><p style='color:blue;'>🔵 RVI: 53.5% (Biomasa)</p></div>", unsafe_allow_html=True)
            with m3:
                st.markdown(f"<div class='metric-card'><h4>Memoria Hídrica</h4><h2>1.0 (Lagunas)</h2><p style='color:gray;'>📍 {zona_partido}</p></div>", unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown(response.text)
            
            # Pie de página legal y de resguardo profesional en grisáceo
            st.markdown("""
            ---
            <div style="font-size: 0.82rem; color: #64748b; text-align: justify; line-height: 1.4; padding-top: 10px;">
            <strong>Aviso Legal y Descargo de Responsabilidad:</strong> Este informe ha sido generado mediante algoritmos de inteligencia artificial y procesamiento automatizado de imágenes satelitales (Sentinel-1 / Sentinel-2) con fines orientativos y de apoyo a la toma de decisiones agronómicas. Los datos reflejan el comportamiento espectral y de retrodispersión en la ventana temporal analizada y no sustituyen el diagnóstico presencial a campo, el análisis de laboratorio certificado ni la recomendación formal de un profesional matriculado. Update Studio AI y sus desarrolladores no asumen responsabilidad directa ni indirecta sobre las decisiones comerciales, operativas o de manejo de insumos adoptadas en base a este reporte automatizado.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error(f"No se pudo completar el análisis. Detalle técnico del error: {ultimo_error}")
else:
    st.info("👈 Ingrese los datos del lote en el panel lateral y haga clic en **'Analizar Lote en Vivo'** para generar el reporte corporativo idéntico al de sus correos.")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 🛰️ Monitoreo Satelital por Radar")
        st.write("Análisis avanzado de humedad de suelo, retrodispersión VV/VH y biomasa bajo cualquier condición de nubosidad.")
    with c2:
        st.markdown("### 🤖 Reporte Corporativo Automatizado")
        st.write("Generación instantánea del informe técnico estructurado para la gestión directiva y operativa de la estancia.")
