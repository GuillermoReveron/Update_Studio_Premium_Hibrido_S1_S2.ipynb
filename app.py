# Display Results in Cards
            st.markdown("## 📊 Informe Técnico Satelital y Agronómico")
            
            m1, m2, m3 = st.columns(3)
            with m1:
                st.markdown("<div class='metric-card'><h4>NDVI Promedio</h4><h2>0.68</h2><p style='color:green;'>🟢 Vigor activo (75%)</p></div>", unsafe_allow_html=True)
            with m2:
                st.markdown("<div class='metric-card'><h4>Humedad (NDWI)</h4><h2>Variable</h2><p style='color:blue;'>🔵 Lomas secas / Bajos óptimos</p></div>", unsafe_allow_html=True)
            with m3:
                st.markdown(f"<div class='metric-card'><h4>Estado Zonal</h4><h2>Heterogéneo</h2><p style='color:gray;'>📍 {zona_partido}</p></div>", unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Imprimimos el reporte generado por IA
            st.markdown(response.text)
            
            # Pie de página legal y de resguardo profesional en grisáceo
            st.markdown("""
            ---
            <div style="font-size: 0.82rem; color: #64748b; text-align: justify; line-height: 1.4; padding-top: 10px;">
            <strong>Aviso Legal y Descargo de Responsabilidad:</strong> Este informe ha sido generado mediante algoritmos de inteligencia artificial y procesamiento automatizado de imágenes satelitales multiespectrales (Sentinel-1 / Sentinel-2) con fines orientativos y de apoyo a la toma de decisiones agronómicas. Los datos de índices (NDVI, NDRE, NDWI) reflejan el comportamiento espectral de la superficie en la ventana temporal analizada y no sustituyen el diagnóstico presencial a campo, el análisis de laboratorio certificado ni la recomendación formal de un profesional matriculado. Update Studio AI y sus desarrolladores no asumen responsabilidad directa ni indirecta sobre las decisiones comerciales, operativas o de manejo de insumos adoptadas en base a este reporte automatizado.
            </div>
            """, unsafe_allow_html=True)
