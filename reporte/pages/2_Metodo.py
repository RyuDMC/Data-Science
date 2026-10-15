"""
Página 2: Método — Pesos, normalización, reglas de decisión.
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
from reporte.theme import apply_style


st.set_page_config(page_title="Método", page_icon="🔬", layout="wide")
apply_style()

st.title("🔬 Método y Decisiones Metodológicas")

st.markdown("""
Este reporte integra **tres fuentes de evidencia** para responder a la pregunta central:
> *¿Cuál es el triciclo más común en La Habana?, ¿por qué es ese?, ¿existe una mejor opción?*

Cada fuente mide algo distinto y se trata de forma separada.
""")

# ======= FUENTES =======
st.header("1️⃣ Fuentes de datos")

fuentes = pd.DataFrame({
    "Fuente": [
        "Anuncios online (scraper)",
        "Catálogos de empresas (scraper)",
        "Trabajo de campo (inventario municipal)"
    ],
    "Qué mide": [
        "Oferta visible, precios, specs declaradas",
        "Oferta formal, disponibilidad, specs de fabricante",
        "Circulación real observada en calle"
    ],
    "Registros": [71, 21, 0],
    "Modelos únicos": [43, 21, 0],
    "Cobertura": [
        "6 fuentes: elyerromenu, islagrande, vedca_telegram, casalindashop, cubancargos, Facebook",
        "4 empresas: KikiHabana, MZ Products, A Cuba Envíos Cargo, Mr Cuba",
        "15 municipios, 3 rutas × ~2.5h (pendiente)"
    ],
    "Estado": ["✅ Activo", "✅ Activo", "⏳ Pendiente"]
})
st.dataframe(fuentes, use_container_width=True, hide_index=True)

st.markdown("---")

# ======= SCORING =======
st.header("2️⃣ Scoring de 'Mejor Opción'")

st.subheader("Pesos aprobados")
pesos = pd.DataFrame({
    "Criterio": ["Precio (USD)", "Autonomía (km)", "Carga (kg)", "Legalidad (binario)", "Repuestos (proxy)"],
    "Peso": [0.40, 0.25, 0.20, 0.10, 0.05],
    "Dirección": ["Menor = mejor", "Mayor = mejor", "Mayor = mejor", "1 = menciona legalidad", "1 = >1 fuente"],
    "Fuente": ["Anuncios/Empresas", "Anuncios/Empresas", "Anuncios/Empresas", "Anuncios/Empresas", "Anuncios"]
})
st.dataframe(pesos, use_container_width=True, hide_index=True)

st.markdown("""
**Fórmula:**
```
score = Σ (criterio_norm × peso)
```
- Cada criterio se normaliza **min-max 0-1 dentro de su grupo de propulsión** (eléctricos vs eléctricos, etc.)
- **Ausentes → 0.5 neutro** (no castiga ni beneficia) + se reporta `n_criterios` (cobertura real)
- **No se comparan scores entre propulsiones** (normalización intra-grupo)
""")

st.subheader("Reglas de decisión clave")
reglas = pd.DataFrame({
    "Tema": [
        "Rangos de autonomía",
        "Datos ausentes",
        "Variantes por química",
        "C400 vs C400A",
        "Oferta viva",
        "Gasolina: autonomía",
        "Repuestos proxy",
        "Precios EUR (islagrande)"
    ],
    "Regla": [
        "Siempre límite inferior (ej. '90-100 km' → 90 km)",
        "Imputación neutra 0.5 + columna n_criterios",
        "Sólo en eléctricos: modelo_norm incluye química (LiFePO4 ≠ GelPb)",
        "Modelos distintos (no se fusionan)",
        "Sin fecha = vigente; con fecha → ≥ 2026-01-01; 'agotado' = no viva",
        "NO se estima (prohibido inventar datos)",
        "1 si modelo aparece en >1 fuente, 0 si no",
        "Se guardan en precio_valor/moneda; NO se convierten a USD"
    ]
})
st.dataframe(reglas, use_container_width=True, hide_index=True)

st.markdown("---")

# ======= LIMPIEZA =======
st.header("3️⃣ Pipeline de limpieza (raw → clean → score)")

st.markdown("""
```
Data/raw_data/           →  Crudos inmutables (write once)
    ├── anuncios_triciclos.jsonl
    ├── anuncios_facebook.jsonl  (parseado desde data_from_FB)
    └── data_from_FB              (original, no se toca)

codes/parse_fb.py        →  Parsing tolerante a errores + normalización
codes/scrape_empresas.py →  Scraping catálogos + normalización
        ↓
Data/clean_data/         →  Limpios listos para análisis (entrada de analisis.py)
    ├── anuncios_triciclos.jsonl
    ├── anuncios_facebook.jsonl
    ├── empresas_kikihabana.jsonl
    ├── empresas_mzproducts.jsonl
    ├── empresas_acubaenvioscargo.jsonl
    ├── empresas_mrcuba.jsonl
    └── registro_ubicaciones.csv   (cuando haya campo)

codes/analisis.py        →  Carga clean_data/, aplica alias, scoring, genera CSVs
        ↓
Data/clean_data/ (outputs)
    ├── score_modelos.csv
    ├── comparacion_campo_online.csv
    ├── frecuencia_por_municipio.csv
    └── frecuencia_por_tipo_uso.csv
""")

st.markdown("**Regla de oro:** Todos los datasets se limpian/normalizan **antes** de cualquier operación. Nada de 'limpiar al vuelo en el gráfico'.")

st.markdown("---")

# ======= ALIAS =======
st.header("4️⃣ Alias de fusión (modelos entre fuentes)")

alias_data = [
    ("BRIDERK (FB)", "TRICICLOS TOPMAQ BRIDERK 2026 GELPB (scraper)"),
    ("MVP POWER (FB)", "TRICICLOS MVP POWER GELPB (scraper)"),
    ("ONEBOT (FB)", "ONEBOT CLASIC 2026 (scraper)"),
    ("KIVITOVA (FB)", "TRICICLOS KIVITOVA 2026 GELPB (scraper)"),
    ("TOPMAQ genérico (FB)", "TRICICLOS TOPMAQ BRIDERK 2026 GELPB (scraper)"),
    ("VIENTO RAPIDO (FB)", "ELECTRICO VIENTO RAPIDO (scraper)"),
    ("MAF (FB)", "TRICICLOS ELECTRICOS MAF BATERIA LIFEPO4 (scraper)"),
    ("JINPENG (FB)", "JINPENG GELPB (scraper)"),
]
alias_df = pd.DataFrame(alias_data, columns=["Nombre en Facebook", "Nombre canónico (scraper)"])
st.dataframe(alias_df, use_container_width=True, hide_index=True)

st.caption("Nota: STAR eléctrico (FB) ≠ TRICICLOS HIBRIDOS STAR (scraper) → NO se fusionan (distinta propulsión).")