# HANDOFF — Proyecto Triciclos La Habana (cierre 2026-10-15, sesión 6)

## 1. Contexto
- Investigación del mercado de triciclos en La Habana (15 municipios). Pregunta central: *"¿Cuál es el triciclo más común en La Habana?, ¿por qué es ese?, ¿existe una mejor opción?"*
- Entregable = **reporte interactivo** (Streamlit), no pipeline. Fuentes: anuncios online, catálogos de empresas, Facebook, trabajo de campo (pendiente).
- Esta sesión fue de **revisión y justificación**: (a) lectura de protocolo de apertura (handoff + diario); (b) explicación de los pesos del scoring; (c) búsqueda de **documentación real** que justifique esos pesos → nuevo `Data/fuentes_justificacion.md`.

## 2. Estado actual
- **Justificación de pesos creada:** `Data/fuentes_justificacion.md` — por criterio, con enlaces verificados por HTTP el 2026-10-15 (11×200; IEEE/AP News/cubanet solo navegador) y nota de honestidad: *los pesos exactos son juicio experto del proyecto, calibrado con la literatura*.
  - Precio 0.40 → Niu et al. 2024 (IEEE Access 12:27931–27946, peso precio **0.417**, sensibilidad ±25%) + ISAHP 2022 (0.40).
  - Autonomía 0.25 → Hidrue et al. 2011 (Resource and Energy Economics 33:686–705) + Hong et al. 2024 (WTP/km).
  - Carga 0.20 → Trung & Ersoy 2025 (J. Appl. Eng. Sci. 23(2):345–358, tabla de 20 estudios MCDM) + uso comercial en Cuba (AP News).
  - Legalidad 0.10 → Resolución 47/2026 MINTRAN + licencias temporales sin matrícula (3 fuentes cubanas).
  - Repuestos 0.05 → apoyo indirecto ISAHP 2022 (*frequent repairs* 0.05); limitación ya declarada.
- **Sin cambios técnicos:** pipeline, `clean_data/` y `reporte/` intactos (71 anuncios → 43 modelos; top eléctrico TOPMAQ BRIDERK 0.736). Servidor Streamlit no se arrancó esta sesión.
- **Git:** `HEAD = c2fa8a5 "created fuentes_justificacion.md"` (commiteado por el usuario). Antes: `4a9aeab "added gitignore"` (pendiente 2 de la sesión 5, **resuelto**). Al cierre, solo `M` de handoff + diario (sin commitear; el usuario revisa).
- **Entorno:** disco externo `17bd76d4` estaba **no montado** durante parte de la sesión (reinicio del servidor); volvió a estar disponible y el archivo se escribió en el repo real.

## 3. Pendiente
1. **Commitear el cierre** (`opencode/HANDOFF.md` + `opencode/Journaing_file.md`, ambos `M`) — como siempre, lo revisa el usuario.
2. **Trabajo de campo** (única fuente de circulación real): 3 rutas × 5 municipios, ~8h; `Data/registro_ubicaciones.csv` sigue con solo cabecera.
3. **Nuevo (ofertado):** añadir la justificación a `reporte/pages/2_Metodo.py`.
4. **Nuevo (ofertado):** análisis de sensibilidad de pesos ±25% en `analisis.py` para demostrar estabilidad de los podios (estándar MCDM; lo hace Niu et al. 2024).
5. Deprecación Streamlit 1.66: `use_container_width=True` → `width="stretch"`.
6. Decidir si `Data/empresas/` se integra al pipeline o queda aparte.
7. Heredados: `repuestos_proxy` (1 de ~35), `precio_texto_usd` (3 contradictorios), VEDCA C400 (3 frentes), `vedca.cu` caído, MAGIKBIKE, Mr Cuba (Wix), Kivitova sin V/Ah, deploy futuro.

## 4. Recursos
- **Repo:** `/run/media/ryudmc/17bd76d4-00a3-4be2-a374-79313809c703/Oliver/Study/DS Proyects/Data-Science` — remoto `https://github.com/RyuDMC/Data-Science/`
- **Justificación de pesos:** `Data/fuentes_justificacion.md` · **Otros enlaces:** `Data/Links de Referencias.md`, `Data/Posibles fuentes de datos.md`
- **Pipeline:** `codes/scrape_triciclos.py`, `codes/parse_fb.py`, `codes/scrape_empresas.py`, `codes/analisis.py`
- **Datos limpios:** `Data/clean_data/` (JSONL + `score_modelos.csv`) · **Reporte:** `reporte/app.py`, `reporte/data.py`, `reporte/theme.py`, `reporte/pages/*`
- **Protocolos:** `Prompts/Journaling Prompt.md`, `Prompts/handoff_prompt.md` · **Diario:** `opencode/Journaing_file.md` (21 entradas)
- **Pesos:** precio 0.40, autonomía 0.25, carga 0.20, legalidad 0.10, repuestos 0.05; min-max intra-propulsión; ausentes → 0.5 + `n_criterios`. **No comparar scores entre propulsiones.**
```bash
cd "/run/media/ryudmc/17bd76d4-00a3-4be2-a374-79313809c703/Oliver/Study/DS Proyects/Data-Science"
reporte/.venv/bin/streamlit run reporte/app.py   # reporte en http://localhost:8501
python3 codes/scrape_triciclos.py                # ~4 min, 5 fuentes (vedca puede fallar)
python3 codes/parse_fb.py                        # Facebook → clean_data/
python3 codes/scrape_empresas.py                 # 4 catálogos de empresas
python3 codes/analisis.py                        # recalcula clean_data/score_modelos.csv
```

## 5. Advertencias
- **Prohibido inventar datos.** Rangos → límite inferior. Ausentes → 0.5 + `n_criterios`. Los pesos **no** se cambian sin decisión del usuario; si se citan en el reporte, declararlos como juicio experto calibrado con literatura (ver `fuentes_justificacion.md`).
- **Disco externo:** verificar montado antes de escribir en el repo; si no lo está, **preguntar al usuario** (nunca crear copias divergentes en otro sitio).
- **Antes de redactar el handoff:** `git log -3` + `git status --porcelain` (el usuario commitea a menudo antes del cierre).
- **Streamlit multipagina:** mantener el bootstrap de `sys.path` al inicio de cada página; verificar con el **servidor real**, no con `python -c`.
- **No fusionar** `TRICICLOS HIBRIDOS STAR` (híbrido) con STAR eléctrico (FB). `C400 ≠ C400A` (ni por química de batería). Alias solo por `modelo_norm`.
- **Arch externally-managed (PEP 668):** `pip` solo dentro de `reporte/.venv`; no usar `--break-system-packages`.
- **`vedca.cu` caído**; Cloudflare/anti-bot bloquean IEEE, AP News y algunas fuentes (los enlaces abren en navegador); Playwright solo si el usuario lo pide.
- **No hay `AGENTS.md`** y no se quiere. El usuario decide cuestiones metodológicas; preguntar antes de cambiar criterios. Handoff **solo** al cerrar sesión (este archivo).
