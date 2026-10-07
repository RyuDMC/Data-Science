# HANDOFF — Proyecto Triciclos La Habana (cierre 2026-10-07)

## 1. Contexto
Investigación del mercado de triciclos en La Habana (15 municipios). Pregunta central: *"¿Cuál es el triciclo más común en La Habana?, ¿por qué es ese?, ¿existe una mejor opción?"*

"Más común" = opción B, **en circulación** (proxy de "más vendido" = velocidad de rotación). Orden del trabajo: análisis general del mercado → más vendido por usos → encontrar uno mejor → demostrar por qué es mejor → analizar si debería ser el más vendido.

Dos estudios separados (carga y motorizados), todas las propulsiones incluyendo `hibrido` como categoría propia. Entregable = **reporte**, no pipeline.

## 2. Estado actual
- **Convención fija:** `codes/` = scripts, `Data/` = datos. Ambos scripts resuelven `DATA_DIR = padre/padre/Data` y se ejecutan desde la raíz.
- **Scraper funcionando** — `python3 codes/scrape_triciclos.py` → **28 registros únicos** en `Data/anuncios_triciclos.jsonl` (18 eléctrico, 8 híbrido, 2 gasolina), de **4 fuentes verificadas**:
  - `casalindashop` (5) — Magento, 2 combustión + 3 eléctricos, con precio
  - `cubancargos` (4) — specs de la tabla `Tipo` (dato autoritativo de propulsión)
  - `elyerromenu` (17) — clasificados "Cuba sobre ruedas", vendedor en **Boyeros**
  - `vedca` (2) — fabricante estatal; specs de tabla, **sin precio**
- **Scoring funcionando** — `python3 codes/analisis.py` → `Data/score_modelos.csv` sin NaN. Ranking: eléctrico = KIVITOVA 2026 (0.795), TOPMAQ BRIDERK (0.676), ELECTRICO CARGA TECHO (0.670); híbrido = JINPEN HIBRIDO (0.678); gasolina = MAGIC BIKE M004 (0.625).
- **Cobertura de criterios** (peso cubierto 0.61 → **0.70**): precio 92.9% (0.40), autonomía 64.3% (0.25), carga 53.6% (0.20), legalidad 60.7% (0.10), repuestos 3.7% (0.05).
- **Diario al día:** `Data/Journaing_file.md`, 9 entradas, protocolo activo.
- **`bs4` instalado y funcional**; pandas 2.3.3; Python 3.14.6.
- **Nada commiteado ni pusheado.** `git status`: `M codes/{analisis,scrape_triciclos}.py` + 6 archivos sin trackear en `Data/`.

## 3. Pendiente
1. **Decidir destino de `repuestos_proxy`** (1 modelo de 27): redefinir el proxy o retirarlo de los pesos.
2. **Resolver 3 conflictos de datos** (ver Advertencias).
3. Decidir si se recupera alguna de las 7 fichas de triciclos sin categoría en elyerromenu o se acepta el catálogo vivo.
4. **Trabajo de campo sin empezar**: `Data/registro_ubicaciones.csv` solo tiene la cabecera (3 días × ~2.5h = 15 municipios).
5. Redactar `Data/reporte_triciclos_2026-10-XX.md`. Fecha de corte propuesta: 30 nov 2026, informe en diciembre.

## 4. Recursos
- **Repo (clon real con `.git`)**: `/run/media/ryudmc/17bd76d4-00a3-4be2-a374-79313809c703/Oliver/Study/DS Proyects/Data-Science` — remoto `https://github.com/RyuDMC/Data-Science/`
- **Scripts**: `codes/scrape_triciclos.py`, `codes/analisis.py`
- **Datos**: `Data/anuncios_triciclos.jsonl`, `Data/score_modelos.csv`, `Data/registro_ubicaciones.csv`
- **Protocolos**: `Prompts/Journaling Prompt.md`, `Prompts/handoff_prompt.md`, `Prompts/Prompt_data_structure.md`
- **Fuentes descartadas y por qué**: en la cabecera de `codes/scrape_triciclos.py` y en el diario
- **Pesos aprobados**: precio 0.40, autonomía 0.25, carga 0.20, legalidad 0.10, repuestos 0.05. Normalización min-max separada por propulsión. Datos ausentes → imputación neutra 0.5 + columna `n_criterios`.

## 5. Advertencias
- **Hay 3 conflictos de datos sin resolver:**
  - `VEDCA C400`: fabricante dice 400 kg / 90 km / 600 W, revendedor dice 500 kg / 120 km / 1200 W. La mediana los promociona a 450/105/900 sin avisar.
  - 3 anuncios con precio contradicho entre campo estructurado y texto (`precio_texto_usd`): TOPMAQ 4700 vs 5000, ONEBOT TANK 6500 vs 6600, MEJOR PRECIO 3600 vs 3650.
  - `repuestos_proxy` casi inerte (1/27).
- **Prohibido inventar datos.** La fórmula de autonomía de gasolina (`cc/10*3*12`) se borró por eso; no reintroducirla. Casalinda no tiene autonomía → aceptar `n_criterios=3` y declararlo.
- **Cloudflare bloquea** revolico, compramasonline, islagrande, multiservicesxpress, patuisla, mundoenvio, envioscubamerica. Probar Playwright solo si el usuario lo pide.
- **`vedca.cu` no declara `charset`**: sin el fix de `fetch()` "Autonomía" se lee como "AutonomÃ­a". No tocarlo.
- **Filtrar por la categoría del vendedor, no por palabras del cuerpo**: los 3 ONEBOT no dicen "triciclo" y un filtro por texto los borraba.
- **Campo = inventario municipal, NO conteo por hora**: una fila por triciclo visto, sin `hora_inicio`/`hora_fin`.
- **No comparar scores entre propulsiones**: cada grupo se normaliza por separado.
- **No hay `AGENTS.md`** y no se quiere. Primer paso de toda sesión: leer `Data/Journaing_file.md` y anotar la consulta antes de actuar; escribir la entrada al terminar.
- **Handoff se genera SOLO al cerrar sesión**, como este archivo en `Data/`.

## Próximos comandos sugeridos
```bash
cd "/run/media/ryudmc/17bd76d4-00a3-4be2-a374-79313809c703/Oliver/Study/DS Proyects/Data-Science"
python3 codes/scrape_triciclos.py     # ~3 min, 4 fuentes
python3 codes/analisis.py
```
