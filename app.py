import streamlit as st
import ee
import folium
from streamlit_folium import st_folium

# Configuración de la página
st.set_page_config(
    page_title="Update Studio AI",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 Update Studio AI — Plataforma Agrícola Avanzada")
st.markdown("### Sistema de Monitoreo Satelital (Sentinel-1 / Sentinel-2) y Diagnóstico por Inteligencia Artificial")

# Panel lateral para ingresar la partida de ARBA
st.sidebar.header("🚜 Panel de Consulta")
partida_input = st.sidebar.text_input("Ingrese N° de Partida (ARBA):", value="051005482")

if st.sidebar.button("🔍 Iniciar Análisis", type="primary"):
    st.info(f"Conectando con Google Earth Engine para procesar la partida {partida_input}...")
    
    # Mensaje de prueba interactivo
    st.success("¡Estructura de la aplicación web conectada correctamente! Próximamente integraremos la visualización completa de mapas y reportes de IA aquí mismo.")
