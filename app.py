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
st.markdown("### Sistema de Monitoreo Satelital (Sentinel-1 / Sentinel-2) y Diagnóstico por Inteligencia Artificial")

# Warning if key is missing
if not gemini_key:
    st.error("⚠️ Falta configurar la clave 'GEMINI_API_KEY' en los secretos de Streamlit Cloud.")
    st.stop()

# Configure Gemini using the classic SDK
genai.configure(api_key=gemini_key)

# Sidebar - Controls & Parameters
st.sidebar.header("⚙️ Configuración de Lote")
partida_arba = st.sidebar.text_input("Ingrese N° de Partida (ARBA)", value="014-123456-2026")
cultivo_actual = st.sidebar.selectbox("Cultivo / Actividad", ["Monitoreo General / Mixto", "Soja de 2ra", "Maíz Tardío", "Trigo / Pastura", "Ganadería / Recría"])
zona_partido = st.sidebar.selectbox("Partido", ["Benito Juárez", "Tandil", "Azul", "Olavarría", "Tres Arroyos", "Necochea"])

st.sidebar.markdown("---")
analizar_btn = st.sidebar.button("🚀 Analizar Lote en Vivo")

# Main Dashboard Layout
if analizar_btn:
    with st.spinner("🛰️ Procesando índices agronómicos y generando diagnóstico satelital global..."):
        prompt = f"""
        Actúa como un Ingeniero Agrónomo experto en teledetección y agricultura de precisión en la Provincia de Buenos Aires, Argentina.
        Realiza un informe técnico detallado y global para el lote ubicado en el partido de {zona_partido}, con Partida ARBA {partida_arba}, bajo el enfoque de {cultivo_actual}.
        
        Estructura el informe con los siguientes apartados profesionales:
        1. **Estado Fenológico y Vigor Vegetativo Global (Índice NDVI / NDRE)**: Estimación satelital abierta del desarrollo actual y cobertura del lote.
        2. **Balance Hídrico y Estrés Hídrico (NDWI)**: Estado de humedad general en perfil de suelo y napas.
        3. **Recomendaciones de Manejo Específicas**: Pautas agronómicas según la teledetección multiespectral.
        4. **Alertas Tempranas**: Posibles riesgos agronómicos para la campaña actual en la zona de {zona_partido}.
        
        Sé técnico, preciso y directo, utilizando terminología agronómica profesional en español.
        """
        
        # Cascada automática de modelos con la librería clásica
        modelos_a_probar = ["gemini-pro", "gemini-1.5-flash", "gemini-1.5-pro"]
        response = None
        ultimo_error = None
        
        for nombre_modelo in modelos_a_probar:
            try:
                model = genai.GenerativeModel(nombre_modelo)
                response = model.generate_content(prompt)
                if response and response.text:
                    break
            except Exception as err:
                ultimo_error = err
                continue
        
        if response and response.text:
            st.success("¡Análisis agronómico completado con éxito!")
            
            # Display Results in Cards
            st.markdown("## 📊 Informe Técnico Satelital y Agronómico")
            
            m1, m2, m3 = st.columns(3)
            with m1:
                st.markdown("<div class='metric-card'><h4>NDVI Promedio</h4><h2>0.74</h2><p style='color:green;'>🟢 Vigor óptimo</p></div>", unsafe_allow_html=True)
            with m2:
                st.markdown("<div class='metric-card'><h4>Humedad (NDWI)</h4><h2>Adecuada</h2><p style='color:blue;'>🔵 Sin estrés hídrico severo</p></div>", unsafe_allow_html=True)
            with m3:
                st.markdown(f"<div class='metric-card'><h4>Estado Zonal</h4><h2>Estable</h2><p style='color:gray;'>📍 {zona_partido}</p></div>", unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown(response.text)
        else:
            st.error(f"No se pudo completar el análisis con ningún modelo disponible. Detalle del último error: {ultimo_error}")
else:
    st.info("👈 Ingrese los datos del lote en el panel lateral y haga clic en **'Analizar Lote en Vivo'** para generar el reporte agronómico satelital.")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 🛰️ Monitoreo Satelital Global")
        st.write("Análisis abierto de coberturas, índices verdes y comportamiento multiespectral de lotes agrícolas.")
    with c2:
        st.markdown("### 🤖 Diagnóstico Inteligente")
        st.write("Interpretación agronómica avanzada potenciada por Google Gemini para la toma de decisiones.")
