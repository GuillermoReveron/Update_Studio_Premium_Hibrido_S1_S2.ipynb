import streamlit as st
import ee
import folium
from streamlit_folium import st_folium
import json
from google.oauth2 import service_account
from google import genai
from datetime import datetime, timedelta
import pandas as pd
import requests

# =====================================================================
# CONFIGURACIÓN DE PÁGINA (DASHBOARD UPDATE STUDIO)
# =====================================================================
st.set_page_config(
    page_title="Update Studio AI - Plataforma Agrícola",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 Update Studio AI — Plataforma Agrícola Avanzada")
st.markdown("### Sistema de Monitoreo Satelital (Sentinel-1 / Sentinel-2) y Diagnóstico por Inteligencia Artificial")

# =====================================================================
# INICIALIZACIÓN DE SERVICIOS BACKEND (GEE + GEMINI)
# =====================================================================
@st.cache_resource
def inicializar_servicios():
    try:
        # Nota: Las credenciales se configuran de forma segura en los Secretos de Streamlit
        key_dict = json.loads(st.secrets["GEE_JSON"])
        creds = service_account.Credentials.from_service_account_info(key_dict)
        ee.Initialize(creds, project='global-satellite-ai')
        
        client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
        return True, client
    except Exception as e:
        return False, str(e)

servicios_ok, client = inicializar_servicios()

# =====================================================================
# PANEL DE CONSULTA LATERAL
# =====================================================================
st.sidebar.header("🚜 Panel de Consulta de Lotes")
partida_input = st.sidebar.text_input("Ingrese N° de Partida (ARBA):", value="051005482")
boton_analizar = st.sidebar.button("🔍 Analizar Lote en Vivo", type="primary")

if boton_analizar:
    if not servicios_ok:
        st.error(f"⚠️ Error de autenticación en los servicios backend: {client}")
        st.info("Verificá que los secretos 'GEE_JSON' y 'GEMINI_API_KEY' estén cargados en la configuración de Streamlit Cloud.")
    else:
        with st.spinner(f"🛰️ Consultando catastro ARBA y procesando telemetría para la partida {partida_input}..."):
            try:
                ruta_catastro = 'projects/global-satellite-ai/assets/catastro_pba_limpio'
                catastro = ee.FeatureCollection(ruta_catastro)
                lote_filtrado = catastro.filter(ee.Filter.eq('PDA', partida_input.strip()))
                
                if lote_filtrado.size().getInfo() == 0:
                    st.warning(f"❌ La partida '{partida_input}' no se encontró en el catastro provincial de ARBA.")
                else:
                    lote_feat = lote_filtrado.first()
                    geometria_lote = lote_feat.geometry()
                    superficie_total_ha = round(geometria_lote.area().divide(10000).getInfo(), 2)
                    centro = geometria_lote.centroid().coordinates().getInfo()[::-1]
                    
                    # Panel de Métricas Superiores
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Lote ID (ARBA)", partida_input)
                    col2.metric("Superficie Total", f"{superficie_total_ha} ha")
                    col3.metric("Estado Satelital", "Online (Google Earth Engine)")
                    col4.metric("Tecnología", "Híbrido (Sentinel-1 / Sentinel-2)")
                    
                    st.divider()
                    
                    # Mapa Interactivo y Vigor
                    col_mapa, col_info = st.columns([1.2, 1])
                    
                    with col_mapa:
                        st.subheader("🗺️ Delimitación del Lote (Google Satellite)")
                        m = folium.Map(location=centro, zoom_start=15, tiles='OpenStreetMap')
                        folium.TileLayer('https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', attr='Google', name='Google Satellite').add_to(m)
                        folium.GeoJson(geometria_lote.getInfo(), style_function=lambda x: {'color': '#1a73e8', 'weight': 3, 'fillOpacity': 0.1}).add_to(m)
                        st_folium(m, width=600, height=450)
                        
                    with col_info:
                        st.subheader("📊 Diagnóstico de Telemetría Web")
                        st.success("✅ Geometría del lote procesada correctamente desde la base catastral.")
                        st.markdown(f"""
                        - **Centroide:** Lat: `{round(centro[0], 5)}`, Lon: `{round(centro[1], 5)}`
                        - **Plataforma:** Conectada a Google Cloud.
                        - **Próximo paso:** Se habilitará la ejecución masiva de IA y generación de reportes corporativos en PDF directamente desde esta interfaz web.
                        """)
            except Exception as e:
                st.error(f"❌ Error procesando el lote: {e}")
