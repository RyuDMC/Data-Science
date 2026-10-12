# HANDOFF — Proyecto Triciclos La Habana (cierre 2026-10-12, sesión 4)

## 1. Contexto
Investigación del mercado de triciclos en La Habana (15 municipios). Pregunta central: *"¿Cuál es el triciclo más común en La Habana?, ¿por qué es ese?, ¿existe una mejor opción?"*

"Común" = en circulación; entregable = **reporte**, no pipeline. Dos estudios separados: (a) triciclos en anuncios (scraper + scoring), (b) **fichas de catálogos de empresas** (nuevo en esta sesión).

## 2. Estado actual
- **Estudio nuevo de empresas (2026-10-12):** extractor `codes/scrape_empresas.py` (independiente del pipeline) → **21 fichas** en `Data/empresas/*.jsonl`:
  - `kikihabana.jsonl` (9) · `mzproducts.jsonl` (7) · `acubaenvioscargo.jsonl` (3) · `mrcuba.jsonl` (2).
  - Decisiones aplicadas: MZ 200cc → `hibrido`; `marca="MZ PRODUCTS"` en MZ; Mr Cuba se mantiene (Wix, solo modelo+precio); KikiHabana excluye carritos 4 ruedas (JY-MX8 EEC, MAGIKBIKE); ONEBOY T414 conservado.
  - Fixes verificados: cirílico 120 АН→AH; miles "3 000W"→3000; autonomía solo por etiqueta (excluye km/h); cargo vs peso neto HUAIHAI 260→780; MZ specs solo de `div.wd-single-content`.
- **Pipeline triciclos intacto**: `scrape_triciclos.py` (5 fuentes) → 33 registros actuales dado `vedca.cu` caído; `analisis.py` → `Data/score_modelos.csv`. Sin tocar en esta sesión.
- **Diario al día**: `opencode/Journaing_file.md`, entradas de empresas agregadas.
- **Sin commitear** (el usuario revisa antes): `codes/scrape_empresas.py`, `Data/empresas/`, `opencode/Journaing_file.md`, `codes/__pycache__/`.

## 3. Pendiente
1. **Revisión del usuario** del working tree (¿commit? ¿`.gitignore`?).
2. Decidir si los datasets de empresas **se integran al pipeline** o quedan aparte.
3. MAGIKBIKE: rescatar o descartar (excluido por "carrito").
4. Heredados: integrar `Data/raw_data/data_from_FB`; `repuestos_proxy` (1 de 35); `precio_texto_usd` (3 anuncios contradictorios); VEDCA C400 (3 frentes); trabajo de campo (15 municipios, sin empezar).
5. Reporte final `Data/reporte_triciclos_2026-10-XX.md`. Corte propuesto: 30 nov 2026.

## 4. Recursos
- **Repo**: `/run/media/ryudmc/17bd76d4-00a3-4be2-a374-79313809c703/Oliver/Study/DS Proyects/Data-Science` — remoto `https://github.com/RyuDMC/Data-Science/`
- **Scripts**: `codes/scrape_empresas.py` (nuevo), `codes/scrape_triciclos.py`, `codes/analisis.py`
- **Datos**: `Data/empresas/` (nuevo), `Data/raw_data/anuncios_triciclos.jsonl`, `Data/score_modelos.csv`, `Data/raw_data/data_from_FB` (sin integrar)
- **Protocolos**: `Prompts/Journaling Prompt.md`, `Prompts/handoff_prompt.md`, `Prompts/Prompt_data_structure.md`
- **Pesos**: precio 0.40, autonomía 0.25, carga 0.20, legalidad 0.10, repuestos 0.05; min-max por propulsión; ausentes → 0.5 + `n_criterios`.

## 5. Advertencias
- **Prohibido inventar datos.** Rangos → límite inferior. Fórmula de autonomía de gasolina: no reintroducir.
- **`C400A` ≠ `C400`**; modelos se fusionan solo por `modelo_norm`. No comparar scores entre propulsiones.
- **`vedca.cu` caído** (reset externo, verificado con curl 2026-10-12); catálogo cubierto vía Telegram/islagrande.
- Cloudflare bloquea varias fuentes; Playwright solo si el usuario lo pide.
- **No hay `AGENTS.md`** y no se quiere. Primer paso de sesión: leer diario; entrada al terminar; **handoff solo al cerrar sesión** (este archivo).
- El usuario decide cuestiones metodológicas; preguntar antes de cambiar criterios.

## Próximos comandos sugeridos
```bash
cd "/run/media/ryudmc/17bd76d4-00a3-4be2-a374-79313809c703/Oliver/Study/DS Proyects/Data-Science"
python3 codes/scrape_triciclos.py     # ~4 min, 5 fuentes (vedca puede fallar)
python3 codes/analisis.py
```