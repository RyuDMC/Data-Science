#!/usr/bin/env python3
"""
Análisis combinado: datos de campo + datos online.
Calcula score de "mejor opción" con pesos predefinidos.

Uso:
    python3 analisis.py
"""

import json
import pandas as pd
from pathlib import Path


# ==================== PESOS APROBADOS ====================
PESOS = {
    "precio_usd": 0.40,        # menor es mejor (invertir)
    "autonomia_km": 0.25,      # mayor es mejor
    "carga_kg": 0.20,          # mayor es mejor
    "legalidad": 0.10,         # binario: 1 si menciona legalización, 0 si no
    "repuestos": 0.05,         # proxy: 1 si modelo aparece en >1 fuente, 0 si no
}

# Columnas esperadas en el JSONL online
ONLINE_FIELDS = [
    "modelo", "marca", "motor_w", "bateria_v", "bateria_ah",
    "autonomia_km", "carga_kg", "precio_usd", "precio_desde",
    "ano", "condicion", "legalizacion", "vendedor_tipo",
    "municipio_anuncio", "url", "fecha_captura", "fuente",
]


def load_online(jsonl_path: str) -> pd.DataFrame:
    """Carga JSONL y normaliza."""
    records = []
    with open(jsonl_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    if not records:
        return pd.DataFrame(columns=ONLINE_FIELDS)

    df = pd.DataFrame(records)

    # Asegurar columnas
    for col in ONLINE_FIELDS:
        if col not in df.columns:
            df[col] = None

    # Normalizar modelo
    df["modelo_norm"] = df["modelo"].str.upper().str.strip()

    # Calcular Wh de batería si hay voltaje y amperaje
    df["bateria_wh"] = df["bateria_v"] * df["bateria_ah"]

    # Legalidad binaria
    df["legalidad_bin"] = df["legalizacion"].notna().astype(int)

    # Repuestos proxy: modelos que aparecen en múltiples fuentes
    fuente_por_modelo = df.groupby("modelo_norm")["fuente"].nunique()
    df["repuestos_proxy"] = df["modelo_norm"].map(fuente_por_modelo > 1).astype(int)

    return df


def load_campo(csv_path: str) -> pd.DataFrame:
    """Carga CSV de inventario municipal."""
    if not Path(csv_path).exists():
        return pd.DataFrame(columns=["fecha", "municipio", "tipo", "uso", "propulsion",
                                      "modelo", "marca", "motor", "estado", "observador", "notas"])
    df = pd.read_csv(csv_path)
    df["modelo_norm"] = df["modelo"].str.upper().str.strip()
    return df


def score_modelos(df_online: pd.DataFrame) -> pd.DataFrame:
    """Calcula score ponderado por modelo (agregado)."""
    if df_online.empty:
        return pd.DataFrame()

    # Agregar por modelo: mediana para numéricos, any para binarios
    agg = df_online.groupby("modelo_norm").agg(
        precio_usd=("precio_usd", "median"),
        autonomia_km=("autonomia_km", "median"),
        carga_kg=("carga_kg", "median"),
        legalidad_bin=("legalidad_bin", "max"),
        repuestos_proxy=("repuestos_proxy", "max"),
        n_anuncios=("precio_usd", "count"),
        marcas=("marca", lambda x: list(x.dropna().unique())),
        fuentes=("fuente", lambda x: list(x.dropna().unique())),
    ).reset_index()

    # Normalizar cada criterio a 0-1 (min-max)
    # Para precio: invertir (menor = mejor)
    for col in ["precio_usd", "autonomia_km", "carga_kg"]:
        if agg[col].notna().any():
            mn, mx = agg[col].min(), agg[col].max()
            if mx > mn:
                if col == "precio_usd":
                    agg[f"{col}_norm"] = 1 - (agg[col] - mn) / (mx - mn)
                else:
                    agg[f"{col}_norm"] = (agg[col] - mn) / (mx - mn)
            else:
                agg[f"{col}_norm"] = 0.5
        else:
            agg[f"{col}_norm"] = 0.5

    # Legalidad y repuestos ya son 0/1
    agg["legalidad_norm"] = agg["legalidad_bin"]
    agg["repuestos_norm"] = agg["repuestos_proxy"]

    # Score ponderado
    agg["score"] = (
        PESOS["precio_usd"] * agg["precio_usd_norm"] +
        PESOS["autonomia_km"] * agg["autonomia_km_norm"] +
        PESOS["carga_kg"] * agg["carga_kg_norm"] +
        PESOS["legalidad"] * agg["legalidad_norm"] +
        PESOS["repuestos"] * agg["repuestos_norm"]
    )

    return agg.sort_values("score", ascending=False).reset_index(drop=True)


def comparar_campo_online(df_campo: pd.DataFrame, df_online: pd.DataFrame) -> pd.DataFrame:
    """Compara frecuencias: qué se ve en la calle vs qué se anuncia."""
    if df_campo.empty or df_online.empty:
        return pd.DataFrame()

    campo_freq = df_campo["modelo_norm"].value_counts().reset_index()
    campo_freq.columns = ["modelo_norm", "freq_campo"]

    online_freq = df_online["modelo_norm"].value_counts().reset_index()
    online_freq.columns = ["modelo_norm", "freq_online"]

    comp = pd.merge(campo_freq, online_freq, on="modelo_norm", how="outer").fillna(0)
    comp["freq_campo"] = comp["freq_campo"].astype(int)
    comp["freq_online"] = comp["freq_online"].astype(int)
    comp["total"] = comp["freq_campo"] + comp["freq_online"]
    comp = comp.sort_values("total", ascending=False).reset_index(drop=True)

    return comp


def main():
    # Rutas
    online_path = "anuncios_triciclos.jsonl"
    campo_path = "registro_ubicaciones.csv"

    print("=== CARGANDO DATOS ===")
    df_online = load_online(online_path)
    df_campo = load_campo(campo_path)

    print(f"Online: {len(df_online)} anuncios, {df_online['modelo_norm'].nunique()} modelos únicos")
    print(f"Campo:  {len(df_campo)} observaciones, {df_campo['modelo_norm'].nunique()} modelos únicos")

    # 1. Score de mejor opción
    print("\n=== SCORE MEJOR OPCIÓN ===")
    df_score = score_modelos(df_online)
    if not df_score.empty:
        print(df_score[["modelo_norm", "score", "precio_usd", "autonomia_km", "carga_kg",
                         "legalidad_bin", "repuestos_proxy", "n_anuncios"]].to_string(index=False))

        # Guardar
        df_score.to_csv("score_modelos.csv", index=False)
        print("\n-> Guardado: score_modelos.csv")

    # 2. Comparación campo vs online
    print("\n=== COMPARACIÓN CAMPO vs ONLINE ===")
    df_comp = comparar_campo_online(df_campo, df_online)
    if not df_comp.empty:
        print(df_comp.head(15).to_string(index=False))
        df_comp.to_csv("comparacion_campo_online.csv", index=False)
        print("\n-> Guardado: comparacion_campo_online.csv")

    # 3. Resumen por municipio (campo)
    if not df_campo.empty:
        print("\n=== POR MUNICIPIO (CAMPO) ===")
        muni = df_campo.groupby(["municipio", "modelo_norm"]).size().reset_index(name="count")
        muni = muni.sort_values(["municipio", "count"], ascending=[True, False])
        print(muni.to_string(index=False))
        muni.to_csv("frecuencia_por_municipio.csv", index=False)
        print("\n-> Guardado: frecuencia_por_municipio.csv")

    # 4. Resumen por tipo/uso
    if not df_campo.empty:
        print("\n=== POR TIPO Y USO (CAMPO) ===")
        tipo_uso = df_campo.groupby(["tipo", "uso", "modelo_norm"]).size().reset_index(name="count")
        tipo_uso = tipo_uso.sort_values(["tipo", "uso", "count"], ascending=[True, True, False])
        print(tipo_uso.to_string(index=False))
        tipo_uso.to_csv("frecuencia_por_tipo_uso.csv", index=False)
        print("\n-> Guardado: frecuencia_por_tipo_uso.csv")


if __name__ == "__main__":
    main()
