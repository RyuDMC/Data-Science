# HANDOFF — Proyecto Triciclos La Habana (cierre 2026-10-15, sesión 5)

## 1. Contexto
- Investigación del mercado de triciclos en La Habana (15 municipios). Pregunta central: *"¿Cuál es el triciclo más común en La Habana?, ¿por qué es ese?, ¿existe una mejor opción?"*
- Entregable = **reporte interactivo** (Streamlit), no pipeline. Tres fuentes: anuncios online, catálogos de empresas, trabajo de campo (pendiente).
- Esta sesión: (a) Facebook integrado como 6ª fuente + capa `clean_data/`; (b) construcción del reporte en `reporte/`; (c) corrección del bug de **páginas en blanco**.

## 2. Estado actual
- **Facebook (6ª fuente):** `codes/parse_fb.py` → `Data/clean_data/anuncios_facebook.jsonl` (29; 1 excluido: Artemisa). `analisis.py` lee de `clean_data/` y aplica `MODELO_ALIAS`. Totales: **71 anuncios → 43 modelos** (33 eléctricos, 8 híbridos, 2 gasolina). Top eléctrico: **TOPMAQ BRIDERK 2026 GELPB 0.736**, **ONEBOT CLASIC 2026 0.725**.
- **Capa limpia `Data/clean_data/`:** `anuncios_triciclos.jsonl` (42), `anuncios_facebook.jsonl` (29), 4 JSONL de empresas (kikihabana 9, mzproducts 7, acubaenvioscargo 3, mrcuba 2), `score_modelos.csv` (43).
- **Reporte `reporte/`** (Streamlit 1.66 + Matplotlib): `app.py`, `data.py`, `theme.py`, `.streamlit/config.toml`, `requirements.txt` y 10 páginas (`pages/1_Resumen.py` … `10_Limitaciones.py`). Lee **en vivo** de `clean_data/`.
- **Bug "páginas vacías" corregido:** bootstrap de `sys.path` (raíz del repo) al inicio de cada página + `fig_ax(**kwargs)` + imports faltantes + renombre `5_P_A_C.py`→`5_Precio_Carga.py`.
- **Verificado:** `AppTest` (11 vistas, 0 errores) y **servidor real por WebSocket** (navegación con 11 entradas; 10 páginas sin excepción).
- **Entorno:** `reporte/.venv` (Python 3.14; streamlit 1.66.0, matplotlib 3.11.2, pandas, numpy). Pipeline usa el `python3` del sistema (tiene pandas/bs4/requests). Arch/Archcraft es *externally-managed* (PEP 668): el reporte corre con el venv.
- **Git:** `HEAD = a9fd9ee "created reporte"` (2026-10-15). Único sin commitear: `.gitignore` (`??`).
- **Servidor:** detenido al cerrar.

## 3. Pendiente
1. **Trabajo de campo** (única fuente de circulación real): 3 rutas × 5 municipios, ~8h; registro `Data/registro_ubicaciones.csv` (11 campos, vacío). Página 8 en "pendiente".
2. **Commitear `.gitignore`** (untracked).
3. Deprecación Streamlit 1.66: reemplazar `use_container_width=True` por `width="stretch"` (se elimina tras 2025-12-31; hoy solo avisa).
4. Decidir si `Data/empresas/` se integra al pipeline o queda aparte (hoy solo copiado a `clean_data/`).
5. Heredados: `repuestos_proxy` (1 de ~35), `precio_texto_usd` (3 anuncios contradictorios), VEDCA C400 (3 frentes), `vedca.cu` caído, MAGIKBIKE, Mr Cuba (Wix), Kivitova sin V/Ah.
6. Deploy del reporte (Streamlit Community Cloud) — futuro.

## 4. Recursos
- **Repo:** `/run/media/ryudmc/17bd76d4-00a3-4be2-a374-79313809c703/Oliver/Study/DS Proyects/Data-Science` — remoto `https://github.com/RyuDMC/Data-Science/`
- **Pipeline:** `codes/scrape_triciclos.py`, `codes/parse_fb.py`, `codes/scrape_empresas.py`, `codes/analisis.py`
- **Datos limpios:** `Data/clean_data/` (JSONL + `score_modelos.csv`)
- **Reporte:** `reporte/app.py`, `reporte/data.py`, `reporte/theme.py`, `reporte/pages/*`
- **Protocolos:** `Prompts/Journaling Prompt.md`, `Prompts/handoff_prompt.md` · **Diario:** `opencode/Journaing_file.md`
- **Pesos:** precio 0.40, autonomía 0.25, carga 0.20, legalidad 0.10, repuestos 0.05; min-max intra-propulsión; ausentes → 0.5 + `n_criterios`. **No comparar scores entre propulsiones.**

## 5. Advertencias
- **Prohibido inventar datos.** Rangos → límite inferior. Ausentes → 0.5 + `n_criterios`.
- **Streamlit multipágina en subcarpeta:** mantener el bootstrap de `sys.path` al inicio de cada página; `from reporte.x import` **falla** sin él. Verificar con el **servidor real**, no con `python -c` (ese sí añade el CWD y enmascara el fallo).
- **No fusionar** `TRICICLOS HIBRIDOS STAR` (híbrido) con STAR eléctrico (FB). `C400 ≠ C400A`. Los alias se aplican por `modelo_norm`.
- **Arch externally-managed (PEP 668):** `pip` solo dentro de `reporte/.venv`; no usar `--break-system-packages`.
- **`vedca.cu` caído**; Cloudflare bloquea fuentes; Playwright solo si el usuario lo pide.
- **No hay `AGENTS.md`** y no se quiere. El usuario decide cuestiones metodológicas; preguntar antes de cambiar criterios. Handoff **solo** al cerrar sesión (este archivo).

## Próximos comandos
```bash
cd "/run/media/ryudmc/17bd76d4-00a3-4be2-a374-79313809c703/Oliver/Study/DS Proyects/Data-Science"
reporte/.venv/bin/streamlit run reporte/app.py   # reporte en http://localhost:8501
python3 codes/scrape_triciclos.py                # ~4 min, 5 fuentes (vedca puede fallar)
python3 codes/parse_fb.py                        # Facebook → clean_data/
python3 codes/scrape_empresas.py                 # 4 catálogos de empresas
python3 codes/analisis.py                        # recalcula clean_data/score_modelos.csv
```
