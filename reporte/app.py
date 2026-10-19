"""
Punto de entrada del reporte interactivo: Triciclos La Habana.
Ejecución: streamlit run reporte/app.py
"""

import streamlit as st

# Configuración de página (debe ser lo primero)
st.set_page_config(
    page_title="Triciclos La Habana — Reporte Interactivo",
    page_icon="🛺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sidebar con info del proyecto
with st.sidebar:
    st.markdown("## 🛺 Triciclos La Habana")
    st.caption("Investigación de mercado (15 municipios)")
    st.markdown("---")
    st.markdown("**Pregunta central:**")
    st.info("¿Cuál es el triciclo más común en La Habana?, ¿por qué es ese?, ¿existe una mejor opción?")
    st.markdown("---")
    st.markdown("**Fuentes de datos:**")
    st.markdown("- Anuncios online (6 fuentes)")
    st.markdown("- Catálogos de empresas (4 empresas)")
    st.markdown("- Trabajo de campo (15 municipios)")
    st.markdown("---")
    st.caption("Corte de datos: 2026-10-19")
    st.caption("Stack: Streamlit + Matplotlib + Pandas")

# La navegación multipágina de Streamlit usa la carpeta pages/ automáticamente
# No hay código adicional necesario aquí; las páginas en reporte/pages/ se cargan solas.

# Página de portada (esta es la que se ve al entrar)
st.title("🛺 Triciclos en La Habana: Reporte Interactivo")
st.markdown("""
Este reporte presenta el análisis del mercado de triciclos en los 15 municipios de La Habana,
integrando **tres fuentes de evidencia**:

| Fuente | Qué mide | Registros | Modelos únicos |
|--------|----------|-----------|----------------|
| **Anuncios online** | Oferta y competencia de precios | 70 | 42 |
| **Catálogos de empresas** | Oferta formal y disponibilidad | 22 | 22 |
| **Trabajo de campo** | Circulación real (inventario municipal) | 0* | 0* |

*Pendiente de ejecución (3 rutas × 5 municipios, ~8h).

---

### 🎯 Navegación del reporte
Usa el **menú lateral** (☰) para ir a cada sección:

1. **📋 Resumen** — La pregunta y los 3 titulares clave
2. **🔬 Método** — Pesos, normalización, reglas de decisión
3. **📊 Mercado** — KPIs, mix por propulsión y fuentes
4. **🏆 Ranking** — Filtro por grupo, tabla ordenable, comparador
5. **💰 Precio / Autonomía / Carga** — Burbuja y frontera eficiente
6. **🎯 Contendientes** — Top por grupo + radar de criterios
7. **✅ Mejor opción** — Recomendación por escenario
8. **🗺️ Trabajo de campo** — Protocolo y placeholders
9. **🏢 Empresas** — 22 fichas de catálogos
10. **⚠️ Limitaciones** — Qué no sabemos y por qué

---

### 🔄 Cómo se actualiza
```bash
# 1. Scraping + análisis
python3 codes/scrape_triciclos.py
python3 codes/parse_fb.py
python3 codes/scrape_empresas.py
python3 codes/analisis.py

# 2. El reporte lee Data/clean_data/ en vivo → refresca y listo
streamlit run reporte/app.py
```
""")

st.markdown("---")
st.caption("💡 Consejo: usa el filtro de propulsión (eléctrico / híbrido / gasolina) en las páginas de Ranking y Contendientes.")