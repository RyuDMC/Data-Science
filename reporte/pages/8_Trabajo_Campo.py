"""
Página 8: Trabajo de Campo — Protocolo + placeholders + comparación.
"""

import os as _os
import sys as _sys
# Permite importar el paquete `reporte` tanto con `streamlit run reporte/app.py`
# (donde sys.path[0] es reporte/) como al ejecutar/testear desde la raíz del repo.
_ROOT = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), "..", ".."))
if _ROOT not in _sys.path:
    _sys.path.insert(0, _ROOT)


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from reporte.data import load_campo, load_comparacion, load_frecuencia_municipio, load_scores
from reporte.theme import apply_style, fig_ax, donut_chart, bar_ranking, color_for_prop, label_for_prop, PROP_COLORS, PROP_LABELS


st.set_page_config(page_title="Trabajo de Campo", page_icon="🗺️", layout="wide")
apply_style()

st.title("🗺️ Trabajo de Campo — Inventario Municipal (15 municipios)")

st.warning("""
⚠️ **ESTADO: PENDIENTE** — No hay datos de campo aún.

Esta sección muestra el **protocolo de captura** y los **placeholders** que se activarán
cuando se ejecute el trabajo de campo (3 rutas × 5 municipios ≈ 8h).
""")

# ======= PROTOCOLO =======
st.subheader("📋 Protocolo de captura")

st.markdown("""
**Objetivo:** Registrar triciclos **en circulación real** (no anuncios) en los 15 municipios de La Habana.

**Metodología:**
- **3 rutas** × **5 municipios** cada una = 15 municipios totales
- **~2.5h por ruta** = ~8h totales
- **Inventario municipal** (espacial), NO conteo horario
- Un observador por ruta, registro en hoja/celular

**15 municipios a cubrir:**
1. Arroyo Naranjo
2. Boyeros
3. Centro Habana
4. Cerro
5. Cotorro
6. Diez de Octubre
7. Guanabacoa
8. Habana del Este
9. Habana Vieja
10. La Lisa
11. Marianao
12. Plaza de la Revolución
13. Playa
14. Regla
15. San Miguel del Padrón
""")

# ======= ESQUEMA DE DATOS =======
st.subheader("📊 Esquema de registro (11 campos)")

schema = pd.DataFrame({
    "Campo": ["fecha", "municipio", "tipo", "uso", "propulsion", "modelo", "marca", "motor", "estado", "observador", "notas"],
    "Tipo": ["date", "categoría", "categoría", "categoría", "categoría", "texto", "texto", "texto", "categoría", "texto", "texto"],
    "Ejemplo": ["2026-11-15", "Boyeros", "triciclo", "carga", "electrico", "KIVITOVA 2026", "KIVITOVA", "1200W", "bueno", "Juan P.", "Carga 600kg visible"],
    "Obligatorio": ["Sí", "Sí", "Sí", "Sí", "Sí", "No", "No", "No", "No", "Sí", "No"]
})
st.dataframe(schema, use_container_width=True, hide_index=True)

st.markdown("""
**Valores permitidos:**
- `tipo`: triciclo | cuatriciclo | motocarro | otro
- `uso`: carga | pasajeros | mixto | ocio_paseo
- `propulsion`: electrico | gasolina | hibrido | indeterminado
- `estado`: nuevo_0km | bueno | regular | malo
""")

# ======= PLACEHOLDERS VISUALES =======
st.subheader("📈 Placeholders (se activan con datos)")

df_campo = load_campo()

if df_campo.empty:
    st.info("""
    **Cuando haya datos, aquí verás:**
    
    1. **Distribución por municipio** — Barras apiladas por modelo/propulsión
    2. **Top modelos en calle** — Ranking real vs ranking online
    3. **Comparación Campo vs Online** — Qué se ve en calle vs qué se anuncia
    4. **Por tipo/uso** — Carga vs pasajeros vs mixto
    5. **Mapa de calor municipal** — Densidad por zona
    """)
    
    # Mostrar placeholders visuales vacíos
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Frecuencia por municipio (ejemplo)**")
        fig, ax = fig_ax(figsize=(6, 4))
        ax.text(0.5, 0.5, "Sin datos de campo\n\nEjecuta el inventario municipal\npara activar este gráfico", 
                ha="center", va="center", fontsize=12, color="#999")
        ax.set_xlabel(""); ax.set_ylabel(""); ax.set_xticks([]); ax.set_yticks([])
        st.pyplot(fig)
    
    with col2:
        st.markdown("**Comparación Campo vs Online (ejemplo)**")
        fig, ax = fig_ax(figsize=(6, 4))
        ax.text(0.5, 0.5, "Sin datos de campo\n\nComparará frecuencias\nreales vs anuncios", 
                ha="center", va="center", fontsize=12, color="#999")
        ax.set_xlabel(""); ax.set_ylabel(""); ax.set_xticks([]); ax.set_yticks([])
        st.pyplot(fig)

else:
    # ======= CON DATOS REALES =======
    st.success(f"✅ **{len(df_campo)} observaciones** en **{df_campo['municipio'].nunique()} municipios**")
    
    # KPIs
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Observaciones", len(df_campo))
    c2.metric("Municipios", df_campo['municipio'].nunique())
    c3.metric("Modelos únicos", df_campo['modelo_norm'].nunique())
    c4.metric("Propulsiones", df_campo['propulsion'].nunique() if 'propulsion' in df_campo.columns else 0)
    
    # Por municipio
    st.markdown("### 📍 Frecuencia por municipio")
    if 'municipio' in df_campo.columns and 'modelo_norm' in df_campo.columns:
        muni = df_campo.groupby(["municipio", "modelo_norm", "propulsion"]).size().reset_index(name="count")
        muni = muni.sort_values(["municipio", "count"], ascending=[True, False])
        st.dataframe(muni, use_container_width=True, hide_index=True)
    
    # Comparación campo vs online
    df_comp = load_comparacion()
    if not df_comp.empty:
        st.markdown("### ⚖️ Comparación Campo vs Online")
        st.dataframe(df_comp.head(20), use_container_width=True, hide_index=True)
    
    # Por tipo/uso
    if all(c in df_campo.columns for c in ['tipo', 'uso']):
        st.markdown("### 📦 Por tipo y uso")
        tipo_uso = df_campo.groupby(["tipo", "uso", "modelo_norm", "propulsion"]).size().reset_index(name="count")
        tipo_uso = tipo_uso.sort_values(["tipo", "uso", "count"], ascending=[True, True, False])
        st.dataframe(tipo_uso, use_container_width=True, hide_index=True)

st.markdown("---")

# ======= INSTRUCCIONES DE EJECUCIÓN =======
st.subheader("▶️ Cómo ejecutar el trabajo de campo")

st.code("""
# 1. Preparar hoja de captura (CSV con cabecera)
#    Ya existe: Data/registro_ubicaciones.csv (vacía, con 11 columnas)

# 2. Imprimir o usar en móvil la plantilla
#    Campos: fecha, municipio, tipo, uso, propulsion, modelo, marca, motor, estado, observador, notas

# 3. Ejecutar 3 rutas × 5 municipios (≈8h total)
#    - Ruta 1: Habana Vieja, Centro Habana, Cerro, Diez de Octubre, San Miguel del Padrón
#    - Ruta 2: Plaza, Arroyo Naranjo, Boyeros, Cotorro, La Lisa
#    - Ruta 3: Marianao, Playa, Guanabacoa, Habana del Este, Regla

# 4. Consolidar en Data/registro_ubicaciones.csv

# 5. Re-ejecutar análisis
python3 codes/analisis.py

# 6. El reporte se actualiza solo al refrescar (lee Data/clean_data/ en vivo)
""", language="bash")
