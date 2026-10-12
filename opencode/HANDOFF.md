# HANDOFF — Proyecto Triciclos La Habana (cierre 2026-10-07, sesión 2)

## 1. Contexto
Investigación del mercado de triciclos en La Habana (15 municipios). Pregunta central: *"¿Cuál es el triciclo más común en La Habana?, ¿por qué es ese?, ¿existe una mejor opción?"*

"Más común" = opción B, **en circulación** (proxy de "más vendido" = velocidad de rotación). Orden: análisis general → más vendido por usos → encontrar uno mejor → demostrar por qué → analizar si debería ser el más vendido.

Dos estudios separados (carga y motorizados), todas las propulsiones incluyendo `hibrido`. Entregable = **reporte**, no pipeline.

## 2. Estado actual
- **Convención fija:** `codes/` = scripts, `Data/` = datos. Ambos scripts resuelven `DATA_DIR` y se ejecutan desde la raíz.
- **Scraper con 5 fuentes** — `python3 codes/scrape_triciclos.py` → **35 registros** en `Data/anuncios_triciclos.jsonl` (25 eléctrico, 8 híbrido, 2 gasolina), **29 modelos**:
  - `casalindashop` (5, verificado completo vía catalogsearch) · `cubancargos` (4) · `elyerromenu` (17) · `vedca` (2, catálogo con 3 triciclos sin ficha .html)
  - **`vedca_telegram` (7) — nueva esta sesión**: canal público `t.me/s/MotosBateriasElectricasCuba` (enlazado desde vedca.cu), enumerable con `?before=` (130 mensajes, 14 páginas, sin login). Aportó **C600** y **C400A** (nuevos) y precio de C400 (US$3.170, 2024-12).
- **Scoring** — `python3 codes/analisis.py` → `Data/score_modelos.csv`. Tops: eléctrico **KIVITOVA 2026 (0.801)**, TOPMAQ BRIDERK (0.676), ELECTRICO CARGA TECHO (0.675); híbrido JINPEN HIBRIDO (0.678); gasolina MAGIC BIKE M004 (0.625). C600 y C400A cierran la tabla (sin precio).
- **Cobertura** (peso cubierto **0.653**, era 0.702 antes del Telegram — diluye): precio 77.1% (0.40), autonomía 71.4% (0.25), carga 54.3% (0.20), legalidad 48.6% (0.10), repuestos 1 modelo (0.05).
- **Diario al día**: `Data/Journaing_file.md`, **10 entradas**, protocolo activo.
- **Nada commiteado por mí.** `git status`: `M` en `Journaing_file.md`, `anuncios_triciclos.jsonl`, `data_from_FB`, `score_modelos.csv`, `scrape_triciclos.py` (el usuario trackeó archivos entre sesiones).

## 3. Pendiente
1. **Decisión del usuario sobre VEDCA C400 — ahora 3 frentes**: (a) specs: motor 600 W fabricante / 1200 W revendedor / 1500 W islagrande→Telegram, batería LiFePO4 50Ah vs GelPb 80Ah, autonomía 80/90/120 → mediana 80; (b) precio 3170 (2024-12) vs 4550 (elerromenu) → mediana 3860; (c) ¿el anuncio de 2024 pesa igual que el de 2026?
2. **Destino de `repuestos_proxy`** (1 modelo de 29) y de **`precio_texto_usd`** (3 anuncios contradictorios).
3. **C800A y LT4211** existen solo como enlaces (sin ficha publicada en vedca.cu): ¿se declara o se ignora?
4. **Trabajo de campo sin empezar**: `Data/registro_ubicaciones.csv` solo cabecera (3 días × ~2.5h = 15 municipios). Punto útil: **Almacén VEDCA, Av. Independencia s/n Boyeros** (lun-vie).
5. Reporte final `Data/reporte_triciclos_2026-10-XX.md`. Corte propuesto: 30 nov 2026, informe en diciembre.

## 4. Recursos
- **Repo**: `/run/media/ryudmc/17bd76d4-00a3-4be2-a374-79313809c703/Oliver/Study/DS Proyects/Data-Science` — remoto `https://github.com/RyuDMC/Data-Science/`
- **Scripts**: `codes/scrape_triciclos.py` (5 fuentes, cabecera documenta descartadas y por qué), `codes/analisis.py`
- **Datos**: `Data/anuncios_triciclos.jsonl`, `Data/score_modelos.csv`, `Data/registro_ubicaciones.csv`
- **Protocolos**: `Prompts/Journaling Prompt.md`, `Prompts/handoff_prompt.md`, `Prompts/Prompt_data_structure.md`
- **Pesos**: precio 0.40, autonomía 0.25, carga 0.20, legalidad 0.10, repuestos 0.05; min-max separado por propulsión; ausentes → 0.5 + `n_criterios`.

## 5. Advertencias
- **Prohibido inventar datos.** Fórmula de autonomía de gasolina borrada: no reintroducir. Rangos → límite inferior (`80-90Km`→80), convención ya acordada.
- **`C400A` ≠ `C400`**: el alias de `normalize_modelo` incluye `[A-Z]?` final; no quitarlo. Modelos se fusionan solo por `modelo_norm`.
- **Telegram**: `parse_tg_list` pagina internamente con `?before=`; el texto del mensaje completo ya viene en la página (sin detalle). Enlaces secos a islagrande → descartados con recuento, visibles en la salida.
- **Cloudflare bloquea** revolico, compramasonline, islagrande, multiservicesxpress, patuisla, mundoenvio, envioscubamerica; Facebook login; WhatsApp/YouTube sin SSR. Playwright solo si lo pide el usuario.
- **`vedca.cu` sin `charset`**: fix en `fetch()` — no tocar. Slugs de elyerromenu se reciclan: manda el cuerpo, no el URL.
- **Campo = inventario municipal, NO conteo por hora.** No comparar scores entre propulsiones.
- **No hay `AGENTS.md`** y no se quiere. Primer paso de sesión: leer `Data/Journaing_file.md`; escribir entrada al terminar. **Handoff solo al cerrar sesión** (este archivo).

## Próximos comandos sugeridos
```bash
cd "/run/media/ryudmc/17bd76d4-00a3-4be2-a374-79313809c703/Oliver/Study/DS Proyects/Data-Science"
python3 codes/scrape_triciclos.py     # ~4 min, 5 fuentes
python3 codes/analisis.py
```
