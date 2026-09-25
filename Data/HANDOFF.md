# HANDOFF — Traspaso de sesión unificado (v2026-09-24)

Fecha: 2026-09-24 · Proyecto: Default Project / repo RyuDMC/Data-Science · Sede: opencode
Desde esta sesión, el diario (JOURNAL) y el handoff viven en: `/media/ryudmc/17bd76d4-00a3-4be2-a374-79313809c703/Oliver/Study/DS Proyects/Data-Science/Data`

## 1. Contexto

- Sesión de formación en captura de datos/scraping con un científico de datos cubano. Flujo: **Journaling Prompt** + **Prompt_for_search_data_sources** + **Prompt_data_structure.md**.
- **Enfoque exclusivo desde 2026-09-24**: el trabajo gira solo alrededor del **mercado de triciclos** (captura, análisis y pipeline). Los otros mercados quedan documentados pero fuera de alcance activo.
- El usuario ejecuta el prompt `Prompt_data_structure.md` (estructura JSON + explicación de cada campo, sin inventar datos, solo info de los sitios dados) mercado por mercado, sobre las secciones de `Data/Posibles fuentes de datos.md`.
- Mercados con **estructura de datos entregada** (2026-09-22 → 24):
  1. **Inmobiliario** → `mercado_inmobiliario_cuba_v1` (Data_Structure_for_Inmbuebles.md)
  2. **Automovilístico** → `mercado_automovilistico_cuba_v1` (Data_Structure_for_Autos.md)
  3. **Motorinas/Bicicletas/Patinetes** → `mercado_movilidad_electrica_cuba_v1` (Data_Structure_for_Movilidad_Electrica.md)
  4. **Triciclos** → `mercado_triciclos_cuba_v1` (Data_Structure_for_Triciclos.md, en `Data/Estructuras/`)

## 2. Estado actual

### Diario
- `Data/Journaing_file.md` = diario activo (sincronizado con el espejo `Default Project/JOURNAL.md` local). Entradas 2026-09-17 → 2026-09-24 + reflexiones finales por sub-sesión.

### Estructuras entregadas (4)
| Schema | Archivo | Nota clave |
|---|---|---|
| mercado_inmobiliario_cuba_v1 | Data_Structure_for_Inmbuebles.md | Porlalivre en renovación (reverificar) |
| mercado_automovilistico_cuba_v1 | Data_Structure_for_Autos.md | 5 monedas; es_precio_desde para catálogos; Ofertas.cu caído (reverificar) |
| mercado_movilidad_electrica_cuba_v1 | Data_Structure_for_Movilidad_Electrica.md | Stock como señal dominante; sin patinetes en catálogos |
| mercado_triciclos_cuba_v1 | Data_Structure_for_Triciclos.md | Legalización + híbrido/extensor de rango como rasgos únicos |

### Correcciones al handoff anterior (aplicar en el repo)
- **Autocubana y Apululu**: ✅ HTML directo (no Playwright).
- **MultiServicesXpress**: ✅ HTML (WooCommerce server-rendered) + REST `wp-json` + feed RSS (no "parcial/XHR").
- **CubanCargos**: Next.js **SSR** → el catálogo viene en el HTML (no requiere XHR para el listado).
- **El Yerro (elyerromenu.com)**: SPA Nuxt bazar genérico, **sin evidencia de triciclos** en la ruta dada → candidato a descartar o inspección JS.
- **Ofertas.cu** (autos): no respondía el 23-sep (HTTP 000) → reverificar.
- **Revolico**: bloqueado desde este entorno (403/transport) los días 23-24-sep → verificación por snippets DDG-HTML; rutas oficiales por subcategoría (`search?category=vehiculos&subcategory=vehiculos-motos-electricas-y-triciclos`, `.../vehiculos-carros`).

## 3. Pendiente

- Actualizar `Data/Posibles fuentes de datos.md` del repo con las clasificaciones corregidas (✅/⚠️/🔎/❌) de los 4 mercados. El agente no puede hacer push a GitHub; generar texto listo para pegar si se pide.
- Reverificar **Ofertas.cu** (autos) y descartar/confirmar **El Yerro** (triciclos) con inspección JS (DevTools/XHR).
- Datificar **patinetes** (no aparecen en las tiendas de movilidad): solo vía grupos FB (Graph API/manual) o nuevas tiendas.
- (Opcional) mostrar Revolico-triciclos completo cuando el entorno permita fetch; muestrear 2-3 páginas de `vehiculos-motos-electricas-y-triciclos` para promedios de precios.
- **✅ Piloto de captura triciclos ejecutado (2026-09-24)**: 27 registros JSONL en `Data/Capturas/triciclos_2026-09-24.jsonl` (KikiHabana 12 vía BS4 grid, CompraMásOnline 11 vía Store API, CubanCargos 4 vía SSR; 9 ofertas; $600–$4 300 USD; ficha completa del IZUKI). Pendiente: fichas de los 11 triciclos restantes de KikiHabana, Revolico (bloqueado), cruce de precios por marca+modelo+motor/batería.
- Actualizar `Data/Journaing_file.md` en GitHub (push manual del usuario; el archivo ya está local).

## 4. Recursos

- `Data/Journaing_file.md` — diario activo (fuente de verdad). · `Data/handoff.md` — handoff v2026-09-22 (histórico).
- `Data/Tecnicas_de_Captura.md` — playbook de captura (pipeline, parsers por plataforma, normalización, snippets fallback, JSONL).
- `Data/Capturas/triciclos_2026-09-24.jsonl` — dataset piloto del mercado triciclos (27 registros).
- `Data/Estructuras/Data_Structure_for_Triciclos.md` + `Data_Structure_for_Autos.md`/`Movilidad_Electrica.md`/`Inmbuebles.md` en Default Project local.
- Repo GitHub `RyuDMC/Data-Science`: `Prompts/Prompt_data_structure.md` · `Data/Posibles fuentes de datos.md` (secciones: Inmobiliario, Automovilístico, Motorinas/Bicicletas/Patinetes, Triciclos, Paneles Solares).
- Fuentes verificadas por mercado (detalle en cada entregable): Revolico, Cubisima, VentaCuba, Autocubana, ATR, MCV, Apululu, Islagrande, MultiServicesXpress, KikiHabana, CompraMásOnline, CubanCargos, El Yerro, GAOS/CasasOasis/HogarEnCuba (SPA), VEDCA, todotricicloselectricos.com (FB verificado), Telegram (anuncios_cu, MotosBateriasElectricasCuba, cubaventas).

## 5. Advertencias

- **No scrapear Facebook**: solo Graph API o snippets del buscador (nunca inventar nombres de grupo si el ID no está indexado).
- **No scrapear Telegram**: solo Bot API/MTProto.
- **Websearch integrado caído** → respaldo `https://html.duckduckgo.com/html/?q=...` vía webfetch.
- **Revolico**: URLs antiguas `/category/...` → 404; usar `/search?category=...&subcategory=...`; si hay bloqueo (403/transport), verificar por snippets DDG.
- Respetar `robots.txt`, ToS y ritmos de 1–2 peticiones/segundo con backoff ante 403/429.
- No inventar datos: clasificaciones "parcial/a verificar" requieren inspección real; marcar ✅ (fetch directo) vs 🔎 (solo indexada).
- Normativa vigente 2026 relevante: Decreto 163/2026 (medios automotores), Res. 114/2026 (90 CUP/kWh), Res. 76/2025 y 41/2026 (solar); verificar fechas antes de citar contenido 2024.