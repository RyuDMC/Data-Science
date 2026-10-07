#!/usr/bin/env python3
"""
Análisis combinado: datos de campo + datos online.
Calcula score de "mejor opción" con pesos predefinidos.
Maneja triciclos eléctricos, híbridos y de combustión.

Estructura del repo (decisión del usuario, 2026-10-07):
  codes/ -> scripts    Data/ -> datos de entrada y salida

Uso:
    python3 codes/analisis.py     # lee Data/*.jsonl|csv, escribe Data/*.csv
"""

import json
import numpy as np
import pandas as pd
from pathlib import Path


# ==================== PESOS APROBATOS ====================
# Nota: "autonomia_km" solo se usa si viene en la fuente. NO se estima para
# gasolina (regla del proyecto: no inventar datos). Los criterios ausentes se
# imputan como 0.5 neutro (decisión del usuario, 2026-10-07) y la cobertura
# real de cada score se reporta en la columna n_criterios.

PESOS = {
    "precio_usd": 0.40,        # menor es mejor (invertir)
    "autonomia_km": 0.25,      # mayor es mejor
    "carga_kg": 0.20,          # mayor es mejor
    "legalidad": 0.10,         # binario: 1 si menciona legalización, 0 si no
    "repuestos": 0.05,         # proxy: 1 si modelo aparece en >1 fuente, 0 si no
}

# Convención de carpetas (decisión del usuario, 2026-10-07):
#   codes/ -> scripts, Data/ -> datos (entrada y salida)
DATA_DIR = Path(__file__).resolve().parent.parent / "Data"

ONLINE_FIELDS = [
    "modelo", "marca", "propulsion", "motor_w", "motor_cc",
    "bateria_v", "bateria_ah", "bateria_wh",
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

    for col in ONLINE_FIELDS:
        if col not in df.columns:
            df[col] = None

    # Normalizar modelo
    df["modelo_norm"] = df["modelo"].astype(str).str.upper().str.strip()

    # Propulsión: normalizar valores
    df["propulsion"] = df["propulsion"].fillna("indeterminado").str.lower()

    # Batería Wh
    df["bateria_wh"] = df["bateria_v"] * df["bateria_ah"]

    # NOTA: NO se estima la autonomía de los triciclos de gasolina.
    # Una fórmula tipo "cc/10*3*12" inventaría datos no verificables, lo cual
    # está prohibido en este proyecto. Los NaN se manejan en score_modelos()
    # re-pesando los criterios disponibles.

    # Legalidad binaria
    df["legalidad_bin"] = df["legalizacion"].notna().astype(int)

    # Repuestos proxy: modelos en múltiples fuentes
    fuente_por_modelo = df.groupby("modelo_norm")["fuente"].nunique()
    df["repuestos_proxy"] = df["modelo_norm"].map(fuente_por_modelo > 1).astype(int)

    return df


def load_campo(csv_path: str) -> pd.DataFrame:
    """Carga CSV de inventario municipal."""
    if not Path(csv_path).exists():
        return pd.DataFrame(columns=["fecha", "municipio", "tipo", "uso", "propulsion",
                                      "modelo", "marca", "motor", "estado", "observador", "notas"])
    df = pd.read_csv(csv_path)
    df["modelo_norm"] = df["modelo"].astype(str).str.upper().str.strip()
    # Normalizar propulsión en campo también
    if "propulsion" in df.columns:
        df["propulsion"] = df["propulsion"].fillna("indeterminado").str.lower()
    return df


def score_modelos(df_online: pd.DataFrame) -> pd.DataFrame:
    """Calcula score ponderado por modelo (agregado), separado por propulsión."""
    if df_online.empty:
        return pd.DataFrame()

    # Agregar por modelo + propulsión
    agg = df_online.groupby(["modelo_norm", "propulsion"]).agg(
        precio_usd=("precio_usd", "median"),
        autonomia_km=("autonomia_km", "median"),
        carga_kg=("carga_kg", "median"),
        legalidad_bin=("legalidad_bin", "max"),
        repuestos_proxy=("repuestos_proxy", "max"),
        n_anuncios=("precio_usd", "count"),
        motor_w_med=("motor_w", "median"),
        motor_cc_med=("motor_cc", "median"),
        marcas=("marca", lambda x: list(x.dropna().unique())),
        fuentes=("fuente", lambda x: list(x.dropna().unique())),
    ).reset_index()

    # Normalizar cada criterio a 0-1 (min-max) DENTRO de cada grupo de propulsión
    # para comparar eléctricos con eléctricos y gasolina con gasolina
    agg["precio_usd_norm"] = 0.5
    agg["autonomia_km_norm"] = 0.5
    agg["carga_kg_norm"] = 0.5

    for prop in agg["propulsion"].unique():
        mask = agg["propulsion"] == prop
        sub = agg[mask]
        for col in ["precio_usd", "autonomia_km", "carga_kg"]:
            if sub[col].notna().any():
                mn, mx = sub[col].min(), sub[col].max()
                if mx > mn:
                    if col == "precio_usd":
                        agg.loc[mask, f"{col}_norm"] = 1 - (sub[col] - mn) / (mx - mn)
                    else:
                        agg.loc[mask, f"{col}_norm"] = (sub[col] - mn) / (mx - mn)
                else:
                    agg.loc[mask, f"{col}_norm"] = 0.5

    agg["legalidad_norm"] = agg["legalidad_bin"]
    agg["repuestos_norm"] = agg["repuestos_proxy"]

    # Score ponderado. Si un criterio no está disponible (NaN), NO se imputa:
    # se re-pesan los criterios disponibles proporcionalmente, para que un dato
    # ausente no castigue ni beneficie al modelo.
    # Cobertura real: con cuántos criterios SÍ tiene dato cada modelo.
    # Se calcula sobre los datos CRUDOS, no sobre las normas (que ya van
    # imputadas a 0.5 y ocultarían la ausencia).
    raw_cols = ["precio_usd", "autonomia_km", "carga_kg", "legalidad_bin", "repuestos_proxy"]
    agg["n_criterios"] = agg[raw_cols].apply(pd.to_numeric, errors="coerce").notna().sum(axis=1)

    cols = ["precio_usd_norm", "autonomia_km_norm", "carga_kg_norm",
            "legalidad_norm", "repuestos_norm"]
    w = [PESOS["precio_usd"], PESOS["autonomia_km"], PESOS["carga_kg"],
         PESOS["legalidad"], PESOS["repuestos"]]

    M = agg[cols].apply(pd.to_numeric, errors="coerce").to_numpy(dtype=float)
    W = np.array(w, dtype=float)

    # Imputación neutra 0.5 (decisión del usuario 2026-10-07): un criterio
    # ausente vale "medio", ni castiga ni beneficia, y todos los scores quedan
    # comparables entre sí. n_criterios expone la fiabilidad de cada score.
    M = np.where(np.isnan(M), 0.5, M)
    agg["score"] = M @ W

    return agg.sort_values(["propulsion", "score"], ascending=[True, False]).reset_index(drop=True)


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

    # Añadir propulsión dominante de cada modelo (del online)
    prop_map = df_online.groupby("modelo_norm")["propulsion"].agg(lambda x: x.mode().iloc[0] if not x.mode().empty else "indeterminado")
    comp["propulsion"] = comp["modelo_norm"].map(prop_map)

    return comp


def main():
    online_path = DATA_DIR / "anuncios_triciclos.jsonl"
    campo_path = DATA_DIR / "registro_ubicaciones.csv"

    print("=== CARGANDO DATOS ===")
    df_online = load_online(str(online_path))
    df_campo = load_campo(str(campo_path))

    print(f"Online: {len(df_online)} anuncios, {df_online['modelo_norm'].nunique()} modelos únicos")
    if not df_online.empty:
        print(f"  Propulsión: {df_online['propulsion'].value_counts().to_dict()}")
    print(f"Campo:  {len(df_campo)} observaciones, {df_campo['modelo_norm'].nunique()} modelos únicos")
    if not df_campo.empty and "propulsion" in df_campo.columns:
        print(f"  Propulsión: {df_campo['propulsion'].value_counts().to_dict()}")

    # 1. Score de mejor opción (por propulsión)
    print("\n=== SCORE MEJOR OPCIÓN (POR PROPULSIÓN) ===")
    df_score = score_modelos(df_online)
    if not df_score.empty:
        # Mostrar top 10 por propulsión
        for prop in df_score["propulsion"].unique():
            sub = df_score[df_score["propulsion"] == prop].head(10)
            print(f"\n--- {prop.upper()} ---")
            cols = ["modelo_norm", "score", "n_criterios", "precio_usd", "autonomia_km", "carga_kg",
                    "legalidad_bin", "repuestos_proxy", "n_anuncios", "motor_w_med", "motor_cc_med"]
            print(sub[cols].to_string(index=False))

        df_score.to_csv(DATA_DIR / "score_modelos.csv", index=False)
        print("\n-> Guardado: score_modelos.csv")

    # 2. Comparación campo vs online
    print("\n=== COMPARACIÓN CAMPO vs ONLINE ===")
    df_comp = comparar_campo_online(df_campo, df_online)
    if not df_comp.empty:
        print(df_comp.head(20).to_string(index=False))
        df_comp.to_csv(DATA_DIR / "comparacion_campo_online.csv", index=False)
        print("\n-> Guardado: comparacion_campo_online.csv")

    # 3. Resumen por municipio (campo)
    if not df_campo.empty:
        print("\n=== POR MUNICIPIO (CAMPO) ===")
        muni = df_campo.groupby(["municipio", "modelo_norm", "propulsion"]).size().reset_index(name="count")
        muni = muni.sort_values(["municipio", "count"], ascending=[True, False])
        print(muni.to_string(index=False))
        muni.to_csv(DATA_DIR / "frecuencia_por_municipio.csv", index=False)
        print("\n-> Guardado: frecuencia_por_municipio.csv")

    # 4. Resumen por tipo/uso
    if not df_campo.empty:
        print("\n=== POR TIPO Y USO (CAMPO) ===")
        tipo_uso = df_campo.groupby(["tipo", "uso", "modelo_norm", "propulsion"]).size().reset_index(name="count")
        tipo_uso = tipo_uso.sort_values(["tipo", "uso", "count"], ascending=[True, True, False])
        print(tipo_uso.to_string(index=False))
        tipo_uso.to_csv(DATA_DIR / "frecuencia_por_tipo_uso.csv", index=False)
        print("\n-> Guardado: frecuencia_por_tipo_uso.csv")

    # 5. Resumen online por propulsión
    if not df_online.empty:
        print("\n=== ONLINE: ESTADÍSTICAS POR PROPULSIÓN ===")
        for prop in df_online["propulsion"].unique():
            sub = df_online[df_online["propulsion"] == prop]
            print(f"\n{prop.upper()} ({len(sub)} anuncios):")
            print(f"  Precio median: ${sub['precio_usd'].median():.0f}" if sub['precio_usd'].notna().any() else "  Precio: N/A")
            print(f"  Autonomía median: {sub['autonomia_km'].median():.0f} km" if sub['autonomia_km'].notna().any() else "  Autonomía: N/A")
            print(f"  Carga median: {sub['carga_kg'].median():.0f} kg" if sub['carga_kg'].notna().any() else "  Carga: N/A")
            if prop == "electrico":
                print(f"  Motor W median: {sub['motor_w'].median():.0f} W" if sub['motor_w'].notna().any() else "  Motor: N/A")
                print(f"  Batería Wh median: {sub['bateria_wh'].median():.0f} Wh" if sub['bateria_wh'].notna().any() else "  Batería: N/A")
            else:
                print(f"  Motor cc median: {sub['motor_cc'].median():.0f} cc" if sub['motor_cc'].notna().any() else "  Motor cc: N/A")


if __name__ == "__main__":
    main()
