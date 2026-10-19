# HANDOFF — Proyecto Triciclos La Habana (cierre 2026-10-19, sesión 7)

## 1. Contexto
- Investigación del mercado de triciclos en La Habana (15 municipios). Pregunta central: *"¿Cuál es el triciclo más común en La Habana?, ¿por qué es ese?, ¿existe una mejor opción?"*
- Entregable = **reporte interactivo** (Streamlit). Fuentes: anuncios online, catálogos de empresas, trabajo de campo (pendiente).
- Esta sesión (2 tandas): el usuario **curó a mano** los `Data/clean_data/*.jsonl` (9 commits) y pidió revisar sus cambios, compararlos con los míos y analizar qué se había hecho mal al limpiar la data. Decisiones: la identidad del producto es *modelo → (si no hay) marca*; la propulsión forma parte de la clave; el registro `TRICICLOS HIBRIDOS MEJOR PRECIO` queda fuera; los 3 "E-CARGO" de MZ Products llevan **el mismo nombre** (la capacidad va en su propio campo) y **la limpieza se aplica en el scraper** (no a mano en el JSONL).

## 2. Estado actual
- **Identidad del producto, en el origen** (decisión del usuario, 2026-10-19):
  - `codes/norm_modelo.py` (nuevo): la regla como código — quita genéricos de categoría, marketing y specs; extrae `marca X` del texto; `modelo` null → la identidad es la **marca**; `identidad()` (vectorizada) compartida por `analisis.py` y `reporte/data.py`.
  - `Data/modelos_canonicos.json` (nuevo, 91 productos, clave = URL): **fuente de verdad** de la identidad, generada con `python3 codes/crear_canonicos.py`; incluye los productos excluidos (con motivo), las separaciones de variante y los nombres fijados a mano (`OVERRIDES`), que se aplican aunque el producto aún no esté en `clean_data`.
  - `scrape_triciclos.py`, `scrape_empresas.py` y `parse_fb.py` normalizan **antes de escribir** → `raw_data/` y `Data/empresas/` nacen limpios. Migrados en el sitio (sin red).
- **Bugs corregidos**: (a) `modelo` null se convertía en `"NONE"` → 7 registros de 5 productos distintos en 3 grupos fantasma, y `NONE GELPB` encabezaba el ranking eléctrico (0.826); (b) `n_anuncios` contaba 0 en registros sin nombre; (c) **`repuestos_proxy` se calculaba por archivo** → el criterio (peso 0.05) pasa de 1/35 a **9/42 modelos**; (d) `n_anuncios_total`/`oferta_viva`/`repuestos_proxy`/`comparar_campo_online` no incluían la propulsión → el STAR eléctrico y el híbrido podían fusionarse.
- **Datos**: 70 anuncios online (41 electrico, 7 hibrido, 2 gasolina) → **41 nombres / 42 filas de ranking** (el STAR aparece en dos propulsiones). + **22 fichas de empresas** (acuba pasó de 3 a 4: se recuperó el "Fly Racing 2027", que el scraper perdía). `clean_data/` reproduce la curaduría del usuario salvo las **4 separaciones de variante** que él aprobó (OIM / OIM PASAJE, RALLY PASAJEROS / RALLY CARGA, VEDCA C800B / VEDCA C800B FOTOVOLTAICO). Score: `score_modelos.csv` regenerado (TOPMAQ BRIDERK 2026 GELPB 0.786 > ONEBOT CLASIC 2026 0.775 > KIVITOVA GELPB 0.723).
- **Scraper de empresas corregido**: (a) un producto "Próximamente" no tiene botón de compra → no hay id de carrito → ahora se identifica por su **permalink** (antes se perdía: la categoría de acuba tiene 4 productos y se capturaban 3); (b) "Próximamente" se comprueba antes que "En stock" (el bloque lleva las dos etiquetas y el producto aún no es comprable); (c) si el título no dice el tipo, la **categoría** ("Triciclos Eléctricos") da la propulsión → `electrico` en vez de `indeterminado`.
- **Reporte**: `2_Metodo.py` (nueva sección "Identidad del producto", alias y cifras al día), `10_Limitaciones.py` (cifras, pendientes, versionado), `3_Mercado.py` / `9_Empresas.py` (columna `nombre_producto`), `app.py` (70/42 y 22 fichas de empresas).
- **Verificado**: `analisis.py` OK (0 identificadores vacíos, 0 "NONE", 0 `n_anuncios=0`); `AppTest` 11/11 sin excepciones; **servidor real** (WS protobuf de Streamlit 1.66) 11/11 OK; migración **idempotente** (`python3 codes/norm_modelo.py --check` → 0 cambios).
- **Git**: `HEAD = afd83b0` (commits del usuario). **Sin commitear**: `Data/clean_data/acubaenvioscargo.jsonl` (+1 producto), `Data/empresas/acubaenvioscargo.jsonl`, `Data/empresas/mzproducts.jsonl`, `Data/modelos_canonicos.json`, `codes/crear_canonicos.py`, `codes/scrape_empresas.py`, `reporte/app.py`, `reporte/pages/{2_Metodo,9_Empresas,10_Limitaciones}.py`, diario/handoff. Revisa y commitea el usuario.
- **Entorno**: disco externo `17bd76d4` montado y operativo.

## 3. Pendiente
1. **Revisar y commitear** lo de esta sesión (el usuario suele revisar antes de commitear).
2. **Revisar el producto recuperado** "FLY RACING 2027" (marca RACING, eléctrico, $4.580, "Próximamente", sin specs: la web no las publica) y decidir si `Data/empresas/` entra o no en el scoring (hoy queda fuera).
3. **Confirmar la marca "MAGIC BIKE"** del triciclo eléctrico de cabina de Casalinda: la ficha solo dice 1800 W y 72 V (sin marca) y declara **"Carga Maxima: 650 KG"**, que está en `null` en la data. La marca "CHILWEE" del triciclo de carga sí está verificada ("batería de plomo-ácido marca CHILWEE").
4. **Trabajo de campo** (única fuente de circulación real): 3 rutas × 5 municipios, ~8h; `Data/registro_ubicaciones.csv` sigue con solo cabecera.
5. **Ofertado y no ejecutado**: (a) añadir la justificación documental (`Data/fuentes_justificacion.md`) a `reporte/pages/2_Metodo.py`; (b) análisis de sensibilidad de pesos ±25% en `analisis.py` (estándar MCDM, como Niu et al. 2024).
6. **Nombres repetidos en empresas**: 3 fichas "E-CARGO MZ PRODUCTS" (60/80/100 Ah) y 2 "FLY RACING" (1500/2000 W) comparten identidad por decisión del usuario. En las tablas son fichas separadas, pero **si el dataset de empresas entra al scoring se agregarían** (mediana de 3 configuraciones).
7. Heredados: `precio_texto_usd` (3 contradictorios), conflicto VEDCA C400 (specs/precio/antigüedad), `use_container_width` → `width="stretch"` (Streamlit 1.66), `vedca.cu` caído, MAGIKBIKE, Mr Cuba (Wix), deploy futuro.

## 4. Recursos
- **Repo:** `/run/media/ryudmc/17bd76d4-00a3-4be2-a374-79313809c703/Oliver/Study/DS Proyects/Data-Science` — remoto `https://github.com/RyuDMC/Data-Science/`
- **Identidad del producto:** `Data/modelos_canonicos.json` (curada) · `codes/norm_modelo.py` (regla) · `codes/crear_canonicos.py` (genera la tabla)
- **Otros enlaces:** `Data/fuentes_justificacion.md`, `Data/Links de Referencias.md`, `Data/Posibles fuentes de datos.md`
- **Pipeline:** `codes/scrape_triciclos.py`, `codes/parse_fb.py`, `codes/scrape_empresas.py`, `codes/analisis.py`
- **Datos limpios:** `Data/clean_data/` (JSONL + `score_modelos.csv`) · **Reporte:** `reporte/app.py`, `reporte/data.py`, `reporte/theme.py`, `reporte/pages/*`
- **Protocolos:** `Prompts/Journaling Prompt.md`, `Prompts/handoff_prompt.md` · **Diario:** `opencode/Journaing_file.md` (22 entradas)
- **Pesos:** precio 0.40, autonomía 0.25, carga 0.20, legalidad 0.10, repuestos 0.05; min-max intra-propulsión; ausentes → 0.5 + `n_criterios`. **No comparar scores entre propulsiones.**
```bash
cd "/run/media/ryudmc/17bd76d4-00a3-4be2-a374-79313809c703/Oliver/Study/DS Proyects/Data-Science"
reporte/.venv/bin/streamlit run reporte/app.py   # reporte en http://localhost:8501
python3 codes/scrape_triciclos.py                # ~4 min, 5 fuentes (vedca puede fallar)
python3 codes/parse_fb.py                        # Facebook → clean_data/
python3 codes/scrape_empresas.py                 # 4 catálogos de empresas
python3 codes/analisis.py                        # recalcula clean_data/score_modelos.csv
python3 codes/norm_modelo.py --check             # ¿queda algo sin normalizar?
python3 codes/crear_canonicos.py                 # regenera la tabla canónica
```

## 5. Advertencias
- **Prohibido inventar datos.** Rangos → límite inferior. Ausentes → 0.5 + `n_criterios`. Los pesos **no** se cambian sin decisión del usuario; si se citan en el reporte, declararlos como juicio experto calibrado con literatura (ver `fuentes_justificacion.md`).
- **La identidad se cambia en `Data/modelos_canonicos.json` (o en `codes/crear_canonicos.py`), NUNCA editando el JSONL a mano**: el scraper sobrescribe lo editado a mano. Tras editar la tabla: `python3 codes/norm_modelo.py --migrar` y luego `python3 codes/analisis.py`.
- **Comparar SIEMPRE la curaduría manual con la tabla canónica antes de migrar**: la tabla manda y se genera desde `clean_data`; si no se refleja, la siguiente pasada revierte el trabajo.
- **Regla de identidad**: `modelo` = nombre propio; si no hay, la **marca**; la **propulsión** forma parte de la clave (mismo nombre + distinta propulsión = productos distintos). No fusionar: STAR eléctrico/híbrido, OIM/OIM PASAJE, JINPENG/JINPEN/TY150UK, DDS-OD.
- **Disco externo:** verificar montado antes de escribir en el repo; si no lo está, **preguntar al usuario** (nunca crear copias divergentes en otro sitio).
- **Antes de redactar el handoff:** `git log -3` + `git status --porcelain` (el usuario commitea a menudo antes del cierre).
- **Streamlit multipagina:** mantener el bootstrap de `sys.path` al inicio de cada página; verificar con el **servidor real** (en 1.66 el protocolo WS es protobuf binario, no JSON), no con `python -c`.
- **Arch externally-managed (PEP 668):** `pip` solo dentro de `reporte/.venv`; no usar `--break-system-packages`.
- **`vedca.cu` caído**; Cloudflare/anti-bot bloquean IEEE, AP News y algunas fuentes (los enlaces abren en navegador); Playwright solo si el usuario lo pide.
- **No hay `AGENTS.md`** y no se quiere. El usuario decide cuestiones metodológicas; preguntar antes de cambiar criterios. Handoff **solo** al cerrar sesión (este archivo).
