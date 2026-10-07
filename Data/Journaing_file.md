# JOURNAL — Diario operativo

Memoria episódica del agente. Consultar antes de actuar; escribir solo después de actuar. Formato de consulta: "Consulta de diario: [criterio]. Entradas relevantes: [resumen]. Aplicaré: [acción]."

Fuente del protocolo: `Prompts/Journaling Prompt.md`.

---

### Entrada de diario

- **Fecha/contexto:** 2026-10-05 — sesión en opencode; activación del protocolo de journaling sobre el clon real (disco externo `17bd76d4`)
- **Tarea:** Activar el protocolo de journaling y crear un diario nuevo en `Data/Journaing_file.md`
- **Acción(es):** Leído `Prompts/Journaling Prompt.md`; detectado que el clon de trabajo real está en el disco externo (tiene `.git`) y no en `~/Projects`; verificado `git status` limpio; confirmado que el diario previo se borró a propósito en el commit pusheado `30a210f` ("removing Journaling"); creado este diario vacío, sin arrastrar las 14 entradas del anterior
- **Resultado:** Diario nuevo creado y protocolo activo para el resto de la sesión
- **Error/éxito:** Éxito, con un paso perdido: se clonó el repo en `~/Projects/Data-Science` asumiendo que ahí vivía el proyecto; el proyecto real estaba en el disco externo
- **Lección:** Antes de clonar o crear archivos de proyecto, localizar el clon real por `.git`. Un clon nuevo en otro sitio es una copia divergente, no la fuente de verdad
- **Próxima vez:** Ante una ruta de proyecto, verificar primero si es un repo y cuál es su remoto, antes de escribir. Considerar `AGENTS.md` en la raíz del proyecto para que el protocolo sobreviva al reinicio de sesión
- **Etiquetas:** setup, journaling, infraestructura, git, disco-externo, ubicacion

---

### Entrada de diario

- **Fecha/contexto:** 2026-10-05 — sesión en opencode; tras leer `Prompts/handoff_prompt.md`
- **Tarea:** Fijar cuándo se genera el documento de handoff y dónde se guarda
- **Acción(es):** Leído el prompt de handoff (5 secciones: Contexto, Estado actual, Pendiente, Recursos, Advertencias; máx. una página; sin inventar). Registrada la instrucción del usuario: el handoff **solo** se genera al finalizar la sesión, como archivo en `Data/`
- **Resultado:** Regla de escritura acordada: nada de handoff durante la sesión; al cerrar, un archivo nuevo en `Data/` (probablemente `Data/HANDOFF.md`, el nombre que el repo ya usó antes). Queda pendiente de ejecutar
- **Error/éxito:** Éxito
- **Lección:** El handoff y el diario resuelven problemas distintos y no se mezclan: el diario es memoria persistente entrada por entrada, el handoff es una foto de cierre para otra IA. Generar el handoff antes de terminar lo convierte en una foto con trabajo a medias
- **Próxima vez:** Al abrir sesión, leer este diario y comprobar si quedó un `HANDOFF.md` pendiente de retomar
- **Etiquetas:** handoff, journaling, protocolo, cierre-de-sesion, convenciones

---

### Entrada de diario

- **Fecha/contexto:** 2026-10-05 — sesión en opencode; limpieza tras activar el protocolo
- **Tarea:** (1) borrar el clon sobrante `~/Projects/Data-Science`; (2) decidir sobre las 14 entradas del diario anterior
- **Acción(es):** Verificado `git status --porcelain` del clon sobrante antes de borrar (única diferencia: el `Data/Journaing_file.md` que yo mismo había eliminado ahí). Ejecutado `rm -rf ~/Projects/Data-Science`. Punto 2 decidido por el usuario: **no** recuperar las entradas de `3ee4f6b`; el diario nuevo sigue empezando desde cero
- **Resultado:** `~/Projects` vuelve a estar vacío. El repo real en el disco externo queda como única copia de trabajo
- **Error/éxito:** Éxito. Sin pérdida: el clon borrado era redundante y todo su contenido es recuperable del remoto público
- **Lección:** Antes de clonar un proyecto hay que localizar su copia real (por `.git`). Clonar primero genera una copia divergente que hay que limpiar después, y el nombre del repo no dice en qué disco está
- **Próxima vez:** Ante una ruta de proyecto, `ls` + buscar `.git` antes de clonar o escribir. No proponer recuperar historia borrada salvo que el usuario lo pida (ya se decidió: el diario empieza limpio). Tampoco proponer `AGENTS.md`: el usuario lo rechazó explícitamente; el protocolo se aplica en sesión, sin archivo de arranque
- **Etiquetas:** limpieza, git, clon-divergente, ubicacion, decision

---

### Entrada de diario

- **Fecha/contexto:** 2026-10-05 — sesión en opencode; diseño e implementación del proyecto triciclos La Habana
- **Tarea:** Crear scripts de scraping y análisis para el proyecto de mercado de triciclos en La Habana
- **Acción(es):** 
  1. Definido estructura de datos: CSV para inventario municipal (15 municipios, sin hora), JSONL para anuncios online
  2. Aprobados criterios de "mejor" con pesos: precio 0.4, autonomía 0.25, carga 0.2, legalidad 0.1, repuestos 0.05
  3. Creado `scrape_triciclos.py` (416 líneas): scrapea Revolico + 3 tiendas WooCommerce (KikiHabana, CubanCargos, CompraMás), visita detalle de cada anuncio, extrae 17 campos, guarda JSONL
  4. Creado `analisis.py`: carga ambos datasets, calcula score ponderado, compara campo vs online, genera CSVs de salida
  5. Actualizado `registro_ubicaciones.csv` con nueva cabecera (inventario municipal)
- **Resultado:** Infraestructura lista. Pendiente: instalar bs4 y ejecutar scraping, luego trabajo de campo en 15 municipios
- **Error/éxito:** Éxito en creación de archivos. bs4 no instalado (entorno externally-managed), usuario lo hará
- **Lección:** Separar inventario municipal (espacial) de conteo horario fue clave para ajustar a 8h reales. JSONL es mejor que CSV para anuncios por campos variables y nulables.
- **Próxima vez:** Usuario instala bs4 (`pip install beautifulsoup4 --break-system-packages` o en venv), ejecuta `python3 scrape_triciclos.py`, luego hace trabajo de campo 3 rutas × 5 municipios, finalmente `python3 analisis.py`
- **Etiquetas:** triciclos, scraping, analisis, implementacion, jsonl, csv, pesos, habana

---

### Entrada de diario

- **Fecha/contexto:** 2026-10-05 — sesión en opencode; corrección: añadir triciclos de combustión al scraper
- **Tarea:** El usuario notó que el scraper original solo cubría eléctricos; había que incluir gasolina
- **Acción(es):**
  1. Revisado `Data/Posibles fuentes de datos.md`: KikiHabana tiene categoría "motos-de-gasolina-y-electrica", Revolico tiene subcategory distinta para gasolina
  2. Actualizado `scrape_triciclos.py` (561 líneas): 8 fuentes ahora (3 Revolico: eléctrico, gasolina, vehículos de trabajo; 2 KikiHabana: eléctrico y gasolina; CubanCargos, CompraMás, elyerromenu)
  3. Añadido campo `propulsion` (electrico/gasolina/indeterminado) y `motor_cc` para combustión
  4. Función `detect_propulsion()` combina hint de URL + palabras clave en título/descripción
  5. Actualizado `analisis.py`: agrupa score por propulsión, normaliza min-max dentro de cada grupo, estima autonomía burda para gasolina (cc/10 * 3 * 12L)
  6. Salidas CSV ahora incluyen columna `propulsion` en todas las tablas
- **Resultado:** Infraestructura lista para ambos tipos. Pendiente: instalar bs4 y ejecutar
- **Error/éxito:** Éxito en refactor. La estimación de autonomía para gasolina es muy aproximada y se documenta como tal
- **Lección:** En Cuba los triciclos de gasolina (CG200, GY6, 150-250cc) son mercado aparte del eléctrico; mezclararlos en un solo ranking distorsiona. Separar por propulsión en el scoring es correcto.
- **Próxima vez:** Usuario instala bs4, ejecuta scraper, verifica que salen ambos tipos en el resumen final ("Por propulsión: electrico: X, gasolina: Y")
- **Etiquetas:** triciclos, combustion, gasolina, scraping, refactor, propulsion

---

### Entrada de diario

- **Fecha/contexto:** 2026-10-05 — sesión en opencode; cierre de sesión tras implementar infraestructura completa del proyecto triciclos La Habana
- **Tarea:** Finalizar sesión: generar handoff, reflexión final, cerrar diario
- **Acción(es):**
  1. Protocolo de journaling activado desde el inicio (3 entradas previas + esta)
  2. Repo real identificado en disco externo `/run/media/ryudmc/17bd76d4-.../Oliver/Study/DS Proyects/Data-Science`
  3. Creados 3 archivos base en `Data/`:
     - `registro_ubicaciones.csv` — hoja de inventario municipal (11 campos, 15 municipios, sin hora)
     - `scrape_triciclos.py` (561 líneas) — scraper 8 fuentes (3 Revolico, 2 KikiHabana, CubanCargos, CompraMás, elyerromenu), detecta propulsión (electrico/gasolina), extrae 17 campos, guarda JSONL
     - `analisis.py` (245 líneas) — carga campo + online, score ponderado por propulsión (pesos: precio 0.4, autonomía 0.25, carga 0.2, legalidad 0.1, repuestos 0.05), compara frecuencias, genera 4 CSVs salida
  4. Diario actualizado con 4 entradas completas (formato verificado 8/8 campos)
  5. Usuario rechaza `AGENTS.md`; decide no recuperar diario anterior (14 entradas en commit `3ee4f6b`)
  6. Clon sobrante en `~/Projects/Data-Science` eliminado
- **Resultado:** Infraestructura lista para ejecutar. Pendiente por usuario: instalar bs4, ejecutar scraper, trabajo de campo 8h (3 rutas × 5 municipios), ejecutar análisis
- **Error/éxito:** Éxito. Sin datos ejecutados aún (solo infraestructura). bs4 no instalado (externally-managed-environment), usuario lo hará
- **Lección:** Separar inventario municipal (espacial) de conteo horario fue clave para ajustar a 8h reales. Separar scoring por propulsión (eléctrico vs gasolina) evita comparar peras con manzanas. JSONL supera a CSV para anuncios por campos variables/nulables.
- **Próxima vez:** 
  1. `pip install beautifulsoup4 --break-system-packages` (o en venv)
  2. `python3 scrape_triciclos.py` → verifica resumen "Por propulsión: electrico: X, gasolina: Y"
  3. Trabajo de campo: 3 días × ~2.5h = 15 municipios, rellenar `registro_ubicaciones.csv`
  4. `python3 analisis.py` → genera `score_modelos.csv`, `comparacion_campo_online.csv`, `frecuencia_por_municipio.csv`, `frecuencia_por_tipo_uso.csv`
  5. Redactar reporte final en `Data/reporte_triciclos_2026-10-XX.md`
- **Etiquetas:** cierre, handoff, triciclos, implementacion, completa, sesion

---

### Entrada de diario

- **Fecha/contexto:** 2026-10-07 — sesión en opencode; debugging scraping: Cloudflare en Revolico, DNS fail en KikiHabana/CompraMás
- **Tarea:** El usuario reporta que el scraping no extrajo ningún registro
- **Acción(es):**
  1. Verificado estado: bs4 instalado OK, pero fuentes tienen problemas:
     - Revolico: 403 Cloudflare ("Just a moment...")
     - KikiHabana: DNS fail (no resuelve kikihabana.com)
     - CompraMás: DNS fail (no resuelve compramasonline.com)
     - elyerromenu: responde 200 pero sin triciclos visibles
     - **CubanCargos: FUNCIONA** (200, productos en /triciclos/electricos-cuba/ y /triciclos/gasolina-cuba/)
  2. Analizada estructura CubanCargos: Tailwind CSS, productos en `<a class="group relative flex flex-col...">` con `<h3>` y href `/triciclos/.../`
  3. Detalle de producto tiene specs en texto: motor (W/cc), batería (V Ah), carga (kg), autonomía (km)
- **Resultado:** Solo CubanCargos es viable ahora. Revolico necesita bypass (Playwright/Selenium o API alternativa). KikiHabana/CompraMás dominios caídos.
- **Error/éxito:** Scraper original falla en 4/5 fuentes. CubanCargos sí entrega datos.
- **Lección:** Verificar disponibilidad de fuentes ANTES de escribir scrapers completos. Sitios cubanos cambian/dominios expiran. Revolico bloquea bots simples.
- **Próxima vez:** 
  1. Reescribir scraper enfocado en CubanCargos (fuente principal viable)
  2. Para Revolico: intentar html.duckduckgo.com/html?q=site:revolico.com+triciclos o Playwright
  3. Buscar fuentes alternativas en `Data/Posibles fuentes de datos.md`
- **Etiquetas:** debugging, scraping, cloudflare, dns-fail, cubancargos, revolico, fuentes-caidas

---### Entrada de diario

- **Fecha/contexto:** 2026-10-07 — sesión en opencode; continúa el debugging del scraping
- **Tarea:** El usuario reporta "el scraping no extrajo ningún registro"; corregir el pipeline scraper → JSONL → score
- **Acción(es):**
  1. **Causa raíz del 0:** había DOS copias del scraper. `codes/scrape_triciclos.py` (Oct 5, commiteada en `d1a7437`) apunta a Revolico (403), KikiHabana y CompraMás (DNS no resuelven) → escribió `codes/anuncios_triciclos.jsonl` vacío a las 09:10. La versión nueva estaba en `Data/` y sí daba registros. El código no estaba roto: se ejecutó el archivo equivocado.
  2. **Fuente nueva y verificada:** `habana.casalindashop.com/vehiculos/triciclos.html` (Magento, 200 OK, 5 productos: 2 combustión Magic Bike 200cc/250cc + 3 eléctricos) con precio en USD y specs en el título. CubanCargos `/triciclos/gasolina-cuba` NO tiene productos propios: solo enlaza a los 4 eléctricos y sus modelos de gasolina (150/200/250/300cc) aparecen únicamente en reseñas de clientes, sin ficha.
  3. **Bugs corregidos en el scraper:** `extract_price_usd` borraba el punto decimal (`$4751.00` → 475100) y no entendía el formato europeo (`3.100,00 USD`); regex `\b(el[eé]ctric|...)\b` nunca coincidía con "eléctrico" (termina en `o`); sin dedupe por URL la página de gasolina duplicaba los 4 eléctricos; `normalize_modelo` fusionaba M004/M005 en "MAGIC BIKE" y dos modelos distintos de Casalinda en "TRICICLO EL", y troceaba "ELÉCTRICO" en "CTRICO" por no quitar tildes.
  4. **Corrección de dato falso:** 3 de los 4 triciclos de CubanCargos se anuncian como `Tipo: Híbrido` en su tabla de especificaciones, y el código los clasificaba como `electrico`. La propulsión ahora sale del campo `Tipo` (dato autoritativo), no del texto libre de la página. Añadida la categoría `hibrido`.
  5. **Dato inventado eliminado:** `analisis.py` estimaba la autonomía de gasolina con `cc/10*3*12` y Magic BIKE salía con "810 km" sin ninguna fuente. Fórmula borrada (viola la regla de no inventar datos).
  6. **Decisiones del usuario:** (a) criterios sin dato → imputación neutra 0.5, con columna `n_criterios` que expone la cobertura de cada score; (b) de aquí en adelante los scripts van en `codes/` y los datos en `Data/` — ambos scripts resuelven `DATA_DIR = padre/padre/Data`, se ejecutan desde la raíz y `codes/` ya no contiene archivos de datos.
- **Resultado:** `python3 codes/scrape_triciclos.py` → **9 registros únicos** (4 eléctrico, 3 híbrido, 2 gasolina) en `Data/anuncios_triciclos.jsonl`; `python3 codes/analisis.py` → `Data/score_modelos.csv` con score sin NaN. Ranking: eléctrico = ELECTRICO CARGA TECHO 72V (0.725, US$2850, 850kg); gasolina = MAGIC BIKE M004 (0.625, US$3100); híbrido = PORTO BELLO (0.550, US$5320, 140km, 700kg).
- **Error/éxito:** Éxito. **Advertencia metodológica sin resolver:** cobertura de los criterios ponderados — precio 100% (peso 0.40), legalidad 44% (0.10), carga 44% (0.20), autonomía 33% (0.25), repuestos **0%** (0.05). `repuestos_proxy` da 0 en todos porque ningún modelo aparece en más de una fuente: ese criterio está inerte y el 45% del peso cae sobre datos ausentes.
- **Lección:** Con dos copias de un mismo script, verificar QUÉ archivo se ejecutó antes de depurar el código: el error estaba en la ruta, no en la lógica. Y nunca dejar que una heurística ("estimación muy burda") alimente un criterio ponderado: fabrica un dato que el informe no podrá defender.
- **Próxima vez:**
  1. Decidir el destino de `repuestos_proxy` (siempre 0): redefinir el proxy o retirarlo de los pesos con el visto del usuario
  2. Cubrir autonomía y carga de los modelos de Casalinda sin inventarlos (buscar ficha técnica en otra fuente) o aceptar `n_criterios=3` y declararlo como limitación en el reporte
  3. Revolico sigue bloqueado (403): probar Playwright o descartarlo como fuente de precios
  4. Trabajo de campo sin empezar: `Data/registro_ubicaciones.csv` sigue con solo cabecera
- **Etiquetas:** scraping, duplicados, casalindashop, cubancargos, hibrido, dato-inventado-eliminado, imputacion-neutra, codes-vs-data, cobertura-de-criterios

---### Entrada de diario

- **Fecha/contexto:** 2026-10-07 (misma sesión) — el usuario pide: "utilizando como base las páginas que ya scrapeaste, busca otras que sean validas y tambien puedas scrapear"
- **Tarea:** Sondear candidatas de `Data/Posibles fuentes de datos.md` y búsqueda web, e incorporar al scraper solo las que devuelvan 200 con triciclos realmente listados.
- **Acción(es):**
  1. **Barrido de candidatas (todas verificadas con status + contenido, no solo status):** Cloudflare activo en `revolico` (403 item y search, también vía webfetch), `compramasonline`, `islagrande`, `multiservicesxpress`, `patuisla`, `mundoenvio`, `envioscubamerica`; DNS caído en `kikihabana`; y **200 pero sin triciclos** en `cubisima`, `autocubana`, `ventacuba`, `ofertas.cu` ("no hay nada que se ajuste a tus criterios"), `cubamax` (404 en el resultado de búsqueda), `cuballama`, `dimecuba`, `atrexport`, `mcvcommercial`. Los `site:` queries devolvían el reflejo del query en el buscador, no resultados: hay que leer el cuerpo, no el contador de coincidencias.
  2. **Fuente nueva 1 — `elyerromenu.com/b/cuba-sobre-ruedas`** (clasificados comerciales, vendedor "Cuba sobre ruedas", dirección declarada **Boyeros, La Habana**). Solo había mirado la portada; la sección de clasificados tiene triciclos con precio y specs. Categoría = catálogo vivo: 20 fichas de las cuales 3 son basura (cuatriciclo, cargador, gomas) → **17 triciclos**. El sitemap es la única enumeración completa (17 sub-sitemaps, 129 MB / 122 s) pero hay 7 triciclos sin categorizar fuera del listado — no se incluyen; queda como limitación anotada.
  3. **Fuente nueva 2 — `vedca.cu`** (fabricante estatal Vehículos Eléctricos del Caribe). Catálogo con `filter-tri`: 5 triciclos, pero solo **C-800 y C-400** tienen ficha `.html` (los otros 3 tienen `href="#"`). Aporta specs de tabla (`Peso de carga`, `Autonomía`, `Potencia del motor`) y **no publica precio**.
  4. **Bugs encontrados al integrar:** (a) el filtro de descarte usaba `bater[ií]a` en el slug y cazó `triciclos-electricos-maf-bateria-lifepo4`; (b) exigir la palabra "triciclo" en el cuerpo borraba los 3 ONEBOT, que no la mencionan — la evidencia correcta es la **categoría que el vendedor declara en el pie de la ficha**; (c) `requests` asume ISO-8859-1 cuando el servidor no declara `charset` y `vedca.cu` no lo declara → "Autonomía" llegaba como "AutonomÃ­a" y la especificación no se detectaba; corregido en `fetch()` (meta charset de los bytes, si no `apparent_encoding`).
  5. **Decisiones tomadas (revisables):** `vendedor_tipo="tienda"` para elyerromenu y `"fabricante"` para VEDCA; se añade `precio_texto_usd` cuando el texto del anuncio declara un precio distinto al campo estructurado, en vez de elegir uno sin poder verificar cuál está vigente; alias en `normalize_modelo` (`VEDCA C-400` ≡ `VEDCA C400`, `PORTO BELLO` ≡ `PORTOBELLO`) para que cuente `repuestos_proxy`.
- **Resultado:** `python3 codes/scrape_triciclos.py` → **28 registros únicos** de 4 fuentes (18 eléctrico, 8 híbrido, 2 gasolina) en `Data/anuncios_triciclos.jsonl`. Cobertura de los criterios ponderados: precio 92,9% (0.40), **autonomía 64,3% (0.25) — era 33%**, carga 53,6% (0.20) — era 44%, legalidad 60,7% (0.10) — era 44%, repuestos 3,7% (0.05) — era 0%. Peso cubierto: **0.702, era ~0.61**. `n_criterios`: 7 modelos con 3, 10 con 4, 10 con 5. Nuevo ranking eléctrico: KIVITOVA 2026 (0.795), TOPMAQ BRIDERK (0.676), ELECTRICO CARGA TECHO (0.670).
- **Error/éxito:** Éxito, con **tres hallazgos que hay que declarar en el reporte**: (1) `VEDCA C400` tiene specs en conflicto entre fabricante (400 kg / 90 km / 600 W) y revendedor (500 kg / 120 km / 1200 W) y la mediana los promociona silenciosamente (450 kg / 105 km / 900 W); (2) 3 anuncios con precio contradictorio (`precio_texto_usd`: TOPMAQ 4700 vs 5000, ONEBOT TANK 6500 vs 6600, MEJOR PRECIO 3600 vs 3650); (3) `repuestos_proxy` sigue prácticamente inerte — 1 modelo de 27 (VEDCA C400).
- **Lección:** Un contador de coincidencias no es evidencia: en las dos búsquedas que devolvían "resultados" el término solo aparecía reflejado en el propio buscador. Y cuando la categoría de un catálogo es la única afirmación disponible de que un producto es un triciclo (los ONEBOT), esa categoría del vendedor ES el dato — filtrar por palabras del cuerpo estaba sustituyendo la fuente por mi propia suposición.
- **Próxima vez:**
  1. Decidir con el usuario el destino de `repuestos_proxy` (1/27 modelos): redefinirlo o retirarlo de los pesos
  2. Resolver el conflicto de specs de VEDCA C400 y los 3 precios contradictorios (preguntar al vendedor o declararlo como limitación)
  3. Decidir si se recupera alguna de las 7 fichas sin categoría de elyerromenu o se acepta el catálogo vivo
  4. Trabajo de campo sin empezar: `Data/registro_ubicaciones.csv` sigue con solo cabecera
- **Etiquetas:** scraping, fuentes-nuevas, elyerromenu, vedca, boyeros, cloudflare, charset, cobertura-de-criterios, precio-contradictorio, specs-en-conflicto

---
