"""
Página 10: Limitaciones — Qué no sabemos y por qué.
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
from reporte.data import load_scores, load_anuncios, load_empresas, load_campo
from reporte.theme import apply_style, fig_ax, color_for_prop, label_for_prop


st.set_page_config(page_title="Limitaciones", page_icon="⚠️", layout="wide")
apply_style()

st.title("⚠️ Limitaciones y Pendientes")

st.markdown("""
Este reporte se basa en **datos observacionales de oferta**, no en un censo de circulación.
Todas las conclusiones deben leerse con estas limitaciones en mente.
""")

# ======= LIMITACIONES ESTRUCTURALES =======
st.header("1️⃣ Limitaciones estructurales")

limitaciones = pd.DataFrame({
    "Área": [
        "Oferta ≠ Circulación",
        "Tamaño de muestra (n)",
        "Sesgo de fuentes online",
        "Trabajo de campo ausente",
        "vedca.cu caído",
        "Normalización min-max intra-grupo",
        "Imputación neutra (0.5)",
        "Repuestos proxy débil",
    ],
    "Qué significa": [
        "Anuncios y catálogos miden **oferta declarada**, no triciclos rodando. Un modelo muy anunciado puede no ser el más común en calle.",
        "42 modelos en el ranking (41 nombres distintos: el STAR aparece en dos propulsiones) de 70 anuncios online + 22 fichas empresas. Muchos modelos con n=1. Scores con n_criterios < 5 son poco fiables.",
        "Fuentes: clasificados (Revolico), tiendas WooCommerce, Telegram, Facebook. No cubren mercado informal completo ni todas las MIPYMEs.",
        "El único dato de **circulación real** (inventario 15 municipios) está **pendiente** (0 observaciones). Sin él, no podemos validar 'el más común'.",
        "Catálogo oficial VEDCA no disponible desde 2024. Cobertura vía Telegram/islagrande es parcial y con precios EUR históricos.",
        "Un modelo extremo (muy barato/muy caro) mueve la escala de **todo el grupo**. Al añadir Facebook, el ranking eléctrico cambió.",
        "Ausentes → 0.5 neutro + n_criterios. No castiga, pero oculta que el score se basa en menos evidencia. Ver columna n_criterios.",
        "9/42 modelos tienen repuestos_proxy=1 (los que se anuncian en más de una fuente). Es un proxy, no disponibilidad real de repuestos: mide presencia en el mercado, no stock de piezas."
    ],
    "Impacto": ["ALTO", "ALTO", "MEDIO", "CRÍTICO", "MEDIO", "MEDIO", "BAJO", "BAJO"]
})

st.dataframe(limitaciones, use_container_width=True, hide_index=True,
             column_config={
                 "Impacto": st.column_config.TextColumn("Impacto", width="small"),
             })

st.markdown("---")

# ======= PENDIENTES TÉCNICOS =======
st.header("2️⃣ Pendientes técnicos (datos)")

pendientes = pd.DataFrame({
    "Item": [
        "data_from_FB integrado (parcial)",
        "repuestos_proxy: proxy de '>1 fuente' (9/42 modelos)",
        "precio_texto_usd: 3 anuncios contradictorios",
        "VEDCA C400: 3 frentes de conflicto",
        "MAGIKBIKE: rescatar o descartar",
        "Mr Cuba (Wix): frágil, solo 2 fichas",
        "Batería Wh: elyerromenu no lee '72v/58ah' (barra)",
        "Nombres de modelo: curar acubaenvioscargo (3 fichas)",
        "Marca 'MAGIC BIKE' en un triciclo eléctrico: sin respaldo en la ficha",
        "Nombres repetidos en catálogos de empresas (misma identidad, distintas configuraciones)",
    ],
    "Estado": [
        "✅ Integrado como 6ª fuente (parse_fb.py) — ranking recalculado",
        "✅ Calculado sobre el dataset completo (antes se hacía por archivo y salía 1/35)",
        "⏳ 3 anuncios con precio en texto ≠ precio campo. ¿Cuál prevalece?",
        "⏳ Specs/precio/antigüedad: C400 LIFEPO4 (elyerromenu) vs C400 GELPB (islagrande) vs C400A (telegram)",
        "⏳ KikiHabana lo excluyó como 'carrito 4 ruedas'. ¿Es triciclo? ¿Rescatar?",
        "⏳ Wix bloquea scraping. Solo modelo+precio. ¿Mantener o descartar?",
        "⏳ Kivitova queda sin V/Ah. Mejora menor detectada en diario.",
        "✅ Curado por el usuario: FLY RACING / RACING. Se recuperó además el 4º producto del catálogo (Fly Racing 2027, 'Próximamente')",
        "⏳ Declarada en la ficha, pero la ficha solo menciona 1800 W y 72 V. ¿Confirmar?",
        "⏳ 3 'E-CARGO MZ PRODUCTS' (60/80/100 Ah) y 2 'FLY RACING' (1500/2000 W) comparten nombre. En las tablas son fichas separadas; si el dataset de empresas entrara al scoring se agregarían",
    ],
    "Prioridad": ["ALTA", "BAJA", "MEDIA", "ALTA", "BAJA", "BAJA", "BAJA", "BAJA", "MEDIA", "MEDIA"]
})

st.dataframe(pendientes, use_container_width=True, hide_index=True)

st.markdown("---")

# ======= DATA QUALITY =======
st.header("3️⃣ Calidad de datos conocida")

df_online = load_anuncios()
df_empresas = load_empresas()
df_scores = load_scores()

if not df_online.empty:
    st.subheader("Completitud de campos (anuncios online)")
    
    fields = ["modelo", "marca", "modelo_norm", "propulsion", "precio_usd", "autonomia_km", "carga_kg",
              "motor_w", "motor_cc", "bateria_v", "bateria_ah", "bateria_quimica",
              "legalizacion", "condicion", "municipio_anuncio"]
    
    completitud = []
    for f in fields:
        if f in df_online.columns:
            pct = df_online[f].notna().mean() * 100
            completitud.append({"Campo": f, "Completitud": f"{pct:.0f}%", "Nulos": df_online[f].isna().sum()})
    
    comp_df = pd.DataFrame(completitud)
    st.dataframe(comp_df, use_container_width=True, hide_index=True)

st.markdown("---")

# ======= QUÉ CAMBIARÍA CON MÁS DATOS =======
st.header("4️⃣ Qué cambiaría con más datos")

st.markdown("""
| Si tuviéramos... | Cambiaría... |
|------------------|--------------|
| **Trabajo de campo (15 municipios)** | Respuesta real a "¿cuál es el más común?". Validación campo vs online. |
| **Más anuncios por modelo** (n ≥ 5) | Scores más estables, n_criterios → 5 para más modelos. |
| **Precios reales de transacción** (no solo listados) | Precio mediano más representativo, menos sesgo vendedor. |
| **Datos de repuestos reales** (talleres, importadores) | Criterio repuestos significativo (hoy solo 9/42 modelos tienen >1 fuente). |
| **VEDCA.cu operativo** | Catálogo oficial completo, specs de fabricante, precios vigentes CUP/USD. |
| **Todas las MIPYMEs** (MVP, Kvitova, etc.) | Cobertura real de oferta formal en Cuba. |
| **Histórico de precios 12+ meses** | Tendencias, estacionalidad, inflación real USD/CUP. |
""")

st.markdown("---")

# ======= REPRODUCIBILIDAD =======
st.header("5️⃣ Reproducibilidad")

st.code("""
# Entorno
python3 -m venv reporte/.venv
source reporte/.venv/bin/activate
pip install -r reporte/requirements.txt

# Pipeline completo (raw → clean → score)
python3 codes/scrape_triciclos.py    # ~4 min, 5 fuentes online
python3 codes/parse_fb.py            # Facebook → clean_data/
python3 codes/scrape_empresas.py     # 4 catálogos empresas
python3 codes/analisis.py            # scoring + CSVs en clean_data/

# Reporte interactivo
streamlit run reporte/app.py

# Versiones clave
python3 --version      # 3.14 (o 3.12 en venv si streamlit falla)
pandas --version       # 2.3+
streamlit --version    # 1.38+
matplotlib --version   # 3.8+
""", language="bash")

st.markdown("---")

# ======= VERSIONADO =======
st.header("6️⃣ Versionado de datos")

st.markdown("""
| Archivo | Fuente | Última actualización | Registros | Notas |
|---------|--------|---------------------|-----------|-------|
| `anuncios_triciclos.jsonl` | 5 scrapers | 2026-10-19 | 41 | vedca.cu caído; 1 excluido por el usuario |
| `anuncios_facebook.jsonl` | parse_fb.py | 2026-10-19 | 29 | 1 excluido (Artemisa) |
| `empresas_*.jsonl` (4) | scrape_empresas.py | 2026-10-19 | 22 | MZ 200cc = híbrido; +1 producto acuba |
| `modelos_canonicos.json` | **curado a mano** | 2026-10-19 | 90 productos | Fuente de verdad de la identidad |
| `score_modelos.csv` | analisis.py | 2026-10-19 | 42 filas (41 nombres) | Recalculado tras la limpieza de nombres |
| `registro_ubicaciones.csv` | **CAMPO** | **PENDIENTE** | 0 | 15 municipios, 8h |

**Corte propuesto para reporte final:** 30 noviembre 2026
""")

st.markdown("---")

st.caption("""
**Principio rector:** *No inventar datos.* Rangos → límite inferior. Ausentes → 0.5 neutro + n_criterios.
Si un dato no se puede verificar, no se usa. La transparencia sobre lo que **no sabemos** 
es tan importante como lo que mostramos.
""")
