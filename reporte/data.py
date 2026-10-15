"""
Capa de datos para el reporte Streamlit.
Carga y normaliza datasets desde Data/clean_data/ con st.cache_data.
"""

import pandas as pd
from pathlib import Path
import streamlit as st


CLEAN_DIR = Path(__file__).resolve().parent.parent / "Data" / "clean_data"


@st.cache_data(show_spinner="Cargando anuncios online…")
def load_anuncios() -> pd.DataFrame:
    """Carga y unifica anuncios_triciclos.jsonl + anuncios_facebook.jsonl."""
    files = [
        CLEAN_DIR / "anuncios_triciclos.jsonl",
        CLEAN_DIR / "anuncios_facebook.jsonl",
    ]
    dfs = []
    for f in files:
        if f.exists():
            df = pd.read_json(f, lines=True)
            dfs.append(df)
    if not dfs:
        return pd.DataFrame()
    df = pd.concat(dfs, ignore_index=True)

    # Normalizaciones comunes
    if "propulsion" in df.columns:
        df["propulsion"] = df["propulsion"].fillna("indeterminado").str.lower()
    if "modelo_norm" not in df.columns and "modelo" in df.columns:
        df["modelo_norm"] = df["modelo"].astype(str).str.upper().str.strip()
    if "precio_usd" in df.columns:
        df["precio_usd"] = pd.to_numeric(df["precio_usd"], errors="coerce")
    if "autonomia_km" in df.columns:
        df["autonomia_km"] = pd.to_numeric(df["autonomia_km"], errors="coerce")
    if "carga_kg" in df.columns:
        df["carga_kg"] = pd.to_numeric(df["carga_kg"], errors="coerce")
    if "motor_w" in df.columns:
        df["motor_w"] = pd.to_numeric(df["motor_w"], errors="coerce")
    if "motor_cc" in df.columns:
        df["motor_cc"] = pd.to_numeric(df["motor_cc"], errors="coerce")

    return df


@st.cache_data(show_spinner="Cargando catálogos de empresas…")
def load_empresas() -> pd.DataFrame:
    """Carga y unifica los 4 JSONL de empresas."""
    files = [
        CLEAN_DIR / "kikihabana.jsonl",
        CLEAN_DIR / "mzproducts.jsonl",
        CLEAN_DIR / "acubaenvioscargo.jsonl",
        CLEAN_DIR / "mrcuba.jsonl",
    ]
    dfs = []
    for f in files:
        if f.exists():
            df = pd.read_json(f, lines=True)
            df["fuente_empresa"] = f.stem
            dfs.append(df)
    if not dfs:
        return pd.DataFrame()
    df = pd.concat(dfs, ignore_index=True)

    # Normalizaciones
    if "propulsion" in df.columns:
        df["propulsion"] = df["propulsion"].fillna("indeterminado").str.lower()
    if "modelo_norm" not in df.columns and "modelo" in df.columns:
        df["modelo_norm"] = df["modelo"].astype(str).str.upper().str.strip()
    for col in ["precio_usd", "autonomia_km", "carga_kg", "motor_w", "motor_cc"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


@st.cache_data(show_spinner="Cargando trabajo de campo…")
def load_campo() -> pd.DataFrame:
    """Carga registro_ubicaciones.csv (inventario municipal)."""
    path = CLEAN_DIR.parent / "registro_ubicaciones.csv"
    if not path.exists():
        return pd.DataFrame(columns=["fecha", "municipio", "tipo", "uso", "propulsion",
                                      "modelo", "marca", "motor", "estado", "observador", "notas"])
    df = pd.read_csv(path)
    if "modelo_norm" not in df.columns and "modelo" in df.columns:
        df["modelo_norm"] = df["modelo"].astype(str).str.upper().str.strip()
    if "propulsion" in df.columns:
        df["propulsion"] = df["propulsion"].fillna("indeterminado").str.lower()
    return df


@st.cache_data(show_spinner="Cargando scores…")
def load_scores() -> pd.DataFrame:
    """Carga score_modelos.csv."""
    path = CLEAN_DIR / "score_modelos.csv"
    if not path.exists():
        return pd.DataFrame()
    df = pd.read_csv(path)
    if "propulsion" in df.columns:
        df["propulsion"] = df["propulsion"].fillna("indeterminado").str.lower()
    return df


@st.cache_data(show_spinner="Cargando comparación campo vs online…")
def load_comparacion() -> pd.DataFrame:
    """Carga comparacion_campo_online.csv."""
    path = CLEAN_DIR / "comparacion_campo_online.csv"
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


@st.cache_data(show_spinner="Cargando frecuencia por municipio…")
def load_frecuencia_municipio() -> pd.DataFrame:
    """Carga frecuencia_por_municipio.csv."""
    path = CLEAN_DIR / "frecuencia_por_municipio.csv"
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def get_kpis(df_online: pd.DataFrame) -> dict:
    """Calcula KPIs principales del dataset online."""
    if df_online.empty:
        return {}
    kpis = {
        "total_anuncios": len(df_online),
        "total_modelos": df_online["modelo_norm"].nunique(),
        "propulsion_dist": df_online["propulsion"].value_counts().to_dict(),
        "fuente_dist": df_online["fuente"].value_counts().to_dict() if "fuente" in df_online.columns else {},
        "precio_median": df_online["precio_usd"].median() if "precio_usd" in df_online.columns else None,
        "autonomia_median": df_online["autonomia_km"].median() if "autonomia_km" in df_online.columns else None,
        "carga_median": df_online["carga_kg"].median() if "carga_kg" in df_online.columns else None,
    }
    return kpis


def filter_by_propulsion(df: pd.DataFrame, prop: str) -> pd.DataFrame:
    """Filtra por propulsión (case-insensitive)."""
    if df.empty or "propulsion" not in df.columns:
        return df
    return df[df["propulsion"].str.lower() == prop.lower()]


def get_top_models(df_scores: pd.DataFrame, prop: str, n: int = 10) -> pd.DataFrame:
    """Top N modelos por score para una propulsión."""
    if df_scores.empty:
        return df_scores
    sub = df_scores[df_scores["propulsion"] == prop].head(n)
    return sub