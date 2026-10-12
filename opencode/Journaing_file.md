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

### Entrada de diario
- **Fecha/contexto:** 2026-10-07, sesión reabierta tras el cierre. El usuario repite la petición: "utilizando como base las páginas que ya scrapeaste, busca otras que sean validas y tambien puedas scrapear". Aplicada la consulta de diario previa (descubrimiento agotado en la lista de candidatas → ángulo nuevo: minar enlaces de las 4 fuentes activas).
- **Tarea:** hallar fuentes nuevas partiendo de las páginas ya scrapeadas, verificadas y scrapeables.
- **Acción(es):**
  1. **Mina de enlaces** de las 4 fuentes (internos + externos). Externos relevantes: subdominios casalindashop de otras provincias (fuera de alcance), `elyerroapp.com`, `supermarket23.com`, `katapulk.com`, canal WhatsApp de Cuban Cargo, Facebook, YouTube y **`t.me/MotosBateriasElectricasCuba` (enlazado desde vedca.cu)**.
  2. **Categorías internas y búsquedas**: `catalogsearch` de casalinda con q=triciclo/triciclos/carga → los mismos 5 productos (q=carga solo añade una lavadora); `/vehiculos.html` → mismos 5 triciclos + 1 cuatriciclo; cubancargos `/tienda` → solo la categoría Triciclos; elyerromenu `/?s=` (JS, 'tricic'=0) y `/search` (solo enlace de categoría); categoría `motos-y-bicimotos` → 5 fichas "Agotado" cuyo contenido real es bicimotos/motos de 2 ruedas (el slug `moto-rali-de-tres-ruedas` está reciclado: el contenido es "Bicimotos VEDCA 2026").
  3. **Descartados con evidencia**: elyerroapp (empresa de software, 'tricic'=0), supermarket23 (búsqueda JS, 'tricic'=0 en HTML crudo), katapulk ('tricic'=0), canal WhatsApp de Cuban Cargo (shell sin posts sin la app), Facebook (redirect a /login, 400), YouTube (sin texto SSR), vedca fb618/lt4202/lt4206/lt4209 (200 pero no son triciclos), sh001/L01/4211 (404: no tienen ficha).
  4. **Fuente nueva: canal público de Telegram de VEDCA** (`t.me/s/MotosBateriasElectricasCuba`, enlace en vedca.cu). Servido sin login; enumerable con paginación `?before=` → **130 mensajes desde el canal (14 páginas), 27 con 'tricic', 7 con specs registrables**. Integrada como 5ª fuente: `parse_tg_list` en `codes/scrape_triciclos.py` (pagina internamente, sin fase de detalle; rangos con límite inferior, convención de elyerromenu; `fecha_anuncio`; `municipio_anuncio="Boyeros"` solo si el mensaje declara la dirección del almacén).
  5. **2 bugs corregidos en caliente**: (a) `dict()` sobre tuplas de 3 de `_tg_mensajes` → comprensión `pid -> (fecha, texto)`; (b) el grupo de captura del token de modelo no incluía la "C" → guardaba "VEDCA 400" y NO se unificaba con "VEDCA C400" de las otras fuentes → `f"VEDCA C{...}"`. Añadido además `[A-Z]?` al alias de `normalize_modelo` para que "C400A" no colapse en "C400".
- **Resultado:** `python3 codes/scrape_triciclos.py` → **35 registros únicos de 5 fuentes** (25 eléctrico, 8 híbrido, 2 gasolina); 29 modelos. **2 modelos nuevos**: VEDCA C600 (auto 50, carga 600, 1200W, 60V/90Ah) y VEDCA C400A (auto 80, carga 400, 1500W, 60V/80Ah) — inexistentes en vedca.cu. VEDCA C400 unificado en 6 anuncios (1 elyerromenu, 1 vedca.cu, 4 telegram): precio mediana 4550→**3860** (el telegram incrusta precio de islagrande US$3.170 del 2024-12), autonomía 105→**80**, carga 450→**400**, motor 1200W (600 fabricante / 1200 revendedor / 1500 islagrande). Descubiertos **C800A y LT4211** solo como enlaces (sin ficha publicada: vedca.cu no tiene página para ellos). Ranking sin cambios de podio: KIVITOVA 2026 (0.801), TOPMAQ BRIDERK (0.676), ELECTRICO CARGA TECHO (0.675); C600 y C400A cierran la tabla (0.267 y 0.307, sin precio). Bonus para campo: el canal declara **Almacén VEDCA, Av. Independencia s/n entre Crucero de Armada y calle 100, Boyeros** (recogida lunes a viernes) y "Sólo queda 3" de stock en 2024-11; noticia institucional (2025-06-07): ventas de VEDCA 220 M de pesos en 2024, +30% vs 2023.
- **Error/éxito:** Éxito tras 2 bugs corregidos en la misma ejecución. La fuente nueva no alteró los podios; sí agrava el conflicto pendiente de VEDCA C400 (ahora 3 frentes: specs, precio y antigüedad del anuncio).
- **Lección:** Un enlace saliente de una fuente ya validada (vedca.cu → t.me) rinde más que cualquier `site:` query: el canal público de Telegram es enumerable con `?before=`, sin login ni Playwright. Y los slugs de elyerromenu se reciclan: el contenido del cuerpo manda sobre el URL.
- **Próxima vez:**
  1. Preguntar al usuario: los 3 frentes del conflicto C400 (¿precio de 2024 cuenta igual que el de 2026? ¿la mediana de 6 anuncios es la especificación "oficial"?)
  2. C400A y C400 comparten carga (400) pero no motor: no fusionarlos jamás en alias
  3. Guardar la dirección del almacén VEDCA (Boyeros) en `registro_ubicaciones.csv` como punto del inventario
  4. Trabajo de campo sigue sin empezar (15 municipios, 8h)
- **Etiquetas:** fuentes-nuevas, telegram, vedca, mina-de-enlaces, c400-conflicto, c600, c400a, catalogsearch, slugs-reciclados

---

### Entrada de diario

- **Fecha/contexto:** 2026-10-11 — sesión en opencode; reapertura tras el cierre del 2026-10-07. El usuario pide "sigue el protocolo" y luego elige "arreglar rutas y correr pipeline"
- **Tarea:** Arrancar según protocolo (leer diario) y desbloquear el pipeline, roto por la reorganización de carpetas hecha entre sesiones
- **Acción(es):**
  1. Leído el HANDOFF (desde GitHub) y las 10 entradas del diario; verificado el repo real en el disco externo `17bd76d4` (limpio salvo `data_from_FB`)
  2. **Detectada la rotura:** los datos se movieron a `Data/raw_data/` y el diario/handoff a `opencode/`, pero `scrape_triciclos.py` y `analisis.py` seguían apuntando a `Data/anuncios_triciclos.jsonl` (inexistente). `analisis.py` habría fallado y el scraper habría creado un archivo divergente en `Data/`
  3. **Fix de rutas:** `DATA_DIR` sigue siendo `Data/`; se añadió `RAW_DIR = DATA_DIR / "raw_data"`. El scraper escribe en `RAW_DIR` (con `mkdir` previo) y el análisis lee el JSONL de `RAW_DIR`; los CSV procesados y `registro_ubicaciones.csv` siguen en `Data/`. Docstrings actualizados
  4. Backup del JSONL crudo antes de sobrescribir: `/tmp/opencode/anuncios_triciclos.prebackup.20261011-221602.jsonl`
  5. Ejecutado `python3 codes/scrape_triciclos.py` (5 fuentes) y `python3 codes/analisis.py`
- **Resultado:** Pipeline funcionando. Scraper → **33 registros / 28 modelos** (23 eléctrico, 8 híbrido, 2 gasolina) de casalindashop(5), cubancargos(4), elyerromenu(17), vedca_telegram(7). `diff` contra el backup: **idéntico salvo `fecha_captura`** → el scraper es determinista y no se perdió nada. Score regenerado: podio sin cambios (KIVITOVA 2026 0.801; híbrido JINPEN 0.678; gasolina MAGIC BIKE M004 0.625). Git: 5 archivos `M` (2 scripts + 3 datos), sin commitear
- **Error/éxito:** Éxito. **Falló la fuente `vedca`** (`ConnectionError: Connection reset by peer`); verificado con curl: `vedca.cu` con y sin `www` da reset, sin `www` ni resuelve DNS. Es caída externa (el 7-oct respondía), no un bug. Por eso el total es 33 y no los 35 del handoff: faltan los 2 registros de `vedca.cu` (C-800, C-400 fabricante). El JSONL commiteado por el usuario ya venía sin ellos
- **Lección:** Cuando el usuario reorganiza carpetas entre sesiones, los scripts con rutas hardcodeadas quedan rotos en silencio: hay que verificar las rutas REALES en disco antes de correr, no fiarse del diario/handoff (repite la lección del 2026-10-07: el error estaba en la ruta). Y antes de que un scraper sobrescriba datos, `diff` contra un backup para confirmar que reproduce y no destruye
- **Próxima vez:**
  1. Reintentar `vedca.cu` (fuente del fabricante) cuando vuelva: sin ella no hay C-800 ni specs autoritativas de C-400
  2. Decidir e integrar `Data/raw_data/data_from_FB` (~14 registros manuales de Facebook): hoy no lo lee ningún script y no es JSON válido
  3. Pendientes vivos del handoff: conflicto VEDCA C400 (specs/precio/antigüedad), destino de `repuestos_proxy` y `precio_texto_usd`, trabajo de campo (15 municipios, 8h)
  4. Considerar `.gitignore` para `__pycache__/` (se generó al verificar con `py_compile`)
- **Etiquetas:** pipeline, rutas, raw_data, reorganizacion, vedca-caido, backup, diff, journaling, sesion-reabierta, determinismo

---

### Entrada de diario

- **Fecha/contexto:** 2026-10-11 (misma sesión) — el usuario pide resolver el conflicto VEDCA C400; elige la regla **B: "oferta viva manda"**
- **Tarea:** Resolver los 3 frentes del conflicto C400: (a) specs contradictorias, (b) precio 3170 vs 4550, (c) si el anuncio de 2024 pesa igual que el de 2026
- **Acción(es):**
  1. Recuperado de la historia de git (commit `4b08583`) el registro del **fabricante**: `vedca.cu/c400.html` → 600 W, 400 kg, 90 km, 60 V **50 Ah**, sin precio (el sitio está caído hoy)
  2. Releído el **texto crudo** de los mensajes de Telegram (ids 1640/1643/1647/1722) y de la ficha elyerromenu. Hallazgo: `islagrande.com` es un marketplace donde el vendedor es **VEDCA** (SKU `VDC042-C400-60V80AH-Habana`); su C400: 1500 W, 400 kg, 80–90 km, **GelPb 60 V 80 Ah**, **$3.170**
  3. Verificado en vivo: `islagrande.com` responde **200** (ya no hay Cloudflare), pero la ficha del C400 da **404 (deslistado)** y el C600 está "Out of stock" (en EUR). La **única oferta viva** del C400 es elyerromenu ($4.550)
  4. **Diagnóstico:** fabricante y tienda de VEDCA coinciden en carga (400) y autonomía (~80–90); el revendedor **infla** (500 kg, 120 km). Motor y batería difieren incluso entre canales de VEDCA (600 W/50 Ah vs 1500 W/80 Ah) → configuraciones/SKU distintos, **no promediable**. La mediana (3860 / 450 kg / 1350 W) **no corresponde a ninguna oferta real**
  5. **Implementada la regla B en `analisis.py`:** `VENTANA_VIGENCIA="2026-01-01"`; columna `es_viva` (sin fecha de publicación = catálogo vigente; con fecha, solo si cae dentro de la ventana). En `score_modelos()` se descartan las publicaciones históricas **cuando el modelo tiene oferta viva**. Añadidas columnas `oferta_viva`, `n_anuncios` (usadas) y `n_anuncios_total`
  6. Corregido el comentario del scraper que daba `islagrande` por bloqueada
- **Resultado:** `VEDCA C400` ahora = oferta viva de elyerromenu: **1200 W · 500 kg · 120 km · 60 V 90 Ah · $4.550**, `oferta_viva=True`, `n_anuncios=1`, `n_anuncios_total=5`. Score **0.563 → 0.647** (sube al puesto 5 en eléctricos). `C600` y `C400A` quedan `oferta_viva=False` (solo canal). Ningún otro modelo cambió
- **Error/éxito:** Éxito. Corrección de paso: `n_anuncios` contaba solo los anuncios **con precio** (C400 salía "2" cuando son 5); ahora `n_anuncios` = ofertas usadas y `n_anuncios_total` = todas
- **Lección:** Un promedio entre **procedencias y años** distintos no representa a nadie: la mediana del C400 fabricaba una oferta inexistente. Separar por **vigencia** y por **jerarquía de fuente** elimina el artefacto. Y verificar los sitios en vivo: islagrande pasó de "bloqueado por Cloudflare" a accesible con el producto deslistado
- **Próxima vez:**
  1. Evaluar `islagrande.com` como **fuente nueva** (ya responde 200): su categoría lista triciclos VEDCA vivos
  2. Reintentar `vedca.cu` (fabricante) cuando vuelva
  3. Llevar la vigencia por fecha también al scraper (hoy `fecha_anuncio` solo viene del canal de Telegram)
  4. Pendientes vivos: integrar `data_from_FB`, destino de `repuestos_proxy`/`precio_texto_usd`, trabajo de campo
- **Etiquetas:** c400-conflicto, oferta-viva-manda, vigencia, islagrande, vedca, mediana-artefacto, analisis, decision-usuario

---

### Entrada de diario

- **Fecha/contexto:** 2026-10-11 (misma sesión), tras resolver el C400. El usuario pide "integrar islagrande"
- **Tarea:** Evaluar `islagrande.com` (candidata del handoff) y decidir cómo integrarla como fuente
- **Acción(es):**
  1. **Reconocimiento:** la categoría `/vehiculos-electricos/triciclos.html` lista **11 fichas** (9 en La Habana; 2 de Holguín/Santiago). Todas salen del **Almacén VEDCA, Av. Independencia, Boyeros**
  2. **Moneda:** el selector Magento (EUR/USD) hace POST a `/directory/currency/switch/` y **exige `form_key`**; incluso extrayéndolo de la página, responde "Invalid Form Key" y los precios siguen en **EUR**. No se convierte (regla del proyecto: no inventar tasa)
  3. **Specs por variante** (bloque `Details`). **Hallazgo 1 — el "conflicto C400" se disuelve en gran parte: eran SKUs distintos.** Existen C400A (GelPb 80 Ah), C400 (LiFePO4 90 Ah) y C400 (LiFePO4Mn 90 Ah). La oferta viva de elyerromenu (LiFePO4 90 Ah) es **el mismo SKU** que el C400 LiFePO4 de islagrande, que declara **90–100 km** — no los 120 de elyerromenu → confirma que el revendedor infla la autonomía
  4. **Hallazgo 2:** los 11 triciclos figuran **"Out of stock"** (verificado: sin formulario de compra) → con la regla B, ninguno es oferta viva
  5. **Preguntas al usuario (2):** precio EUR → *"registrar EUR tal cual"* (recomendado); variantes del mismo modelo → *"separar por variante"* (no promediar químicas distintas)
- **Resultado:** Plan aprobado: islagrande entra como **catálogo del fabricante** (sustituye a vedca.cu, caído): precio en `precio_valor` + `moneda="EUR"` (nunca en `precio_usd`), `condicion="agotado"`, y **variantes por química de batería**
- **Error/éxito:** Éxito en la evaluación. El switch de moneda de Magento quedó **descartado** (form_key no persiste); se documenta en la cabecera del scraper
- **Lección:** Un mismo nombre comercial ("C400") esconde 3 SKUs con química y motor distintos; la química de la batería es el discriminante fiable. Y verificar el **cuerpo** de cada ficha, no el título: la URL del C400 GelPb (que enlazaba el canal) está **deslistada (404)** pero su equivalente C400A sigue en catálogo
- **Próxima vez:**
  1. No fusionar C400/C400A/C400 LiFePO4Mn en ninguna tabla: son variantes separadas por decisión del usuario
  2. Si se necesita el precio en USD de islagrande, pedir al usuario una tasa documentada (no inferirla del selector Magento)
  3. El C800A (LiFePO4Mn) aparece solo en "Up-Sell Products" de otras fichas y como enlace en el canal: no tiene ficha propia
- **Etiquetas:** islagrande, fuente-nueva, vedca, moneda-eur, magento-form-key, variantes-bateria, sku, c400-desambiguado, agotado

---

### Entrada de diario

- **Fecha/contexto:** 2026-10-11 (misma sesión) — implementación de la integración de `islagrande` aprobada
- **Tarea:** Integrar islagrande en scraper y análisis, con precio en EUR y variantes por química, sin romper lo anterior
- **Acción(es):**
  1. **Helper `extract_bateria_quimica(text)`**: prioridad LiFePO4Mn → LiFePO4 → GelPb → Plomo → Litio; normaliza subíndices (LiFePO₄→LiFePO4); comprueba **LiFePO4 antes que "gel"** para no confundir la frase "Digital Li/gel with NFC" de las fichas de litio
  2. **Química en las fuentes existentes**: elyerromenu (cuerpo), vedca (tabla), telegram (texto). Verificado con los textos reales: Kivitova "6 Baterías de GEL", MVP "72V 58Ah GEL", C400A telegram "Gel Plomo", C600 "LiFePO4"
  3. **`parse_islagrande_list` / `parse_islagrande_detail`**: filtro `"triciclo"` en la URL (excluye el accesorio batería/cargador `bateria-cargador-lifep4-64v-90ah.html`), exclusión de `-holguin`/`-santiago`/`-santaclara`; specs **solo** desde `.product.attribute.description`; autonomía = **límite inferior** (c400_lfp "between 90 and 100 km"→90; c300 "Up to 60… ~40 cargado"→40); carga por etiqueta (net load/load capacity/cargo weight/max payload); `precio_valor` desde `data-price-amount`; `condicion="agotado"`
  4. **Bug corregido en caliente:** la primera versión acotaba el texto desde la palabra "Details" con una ventana fija → se colaba en la sección **"Up-Sell Products"** y metía "C800A LiFePO4Mn" en la química del **C400A y del SH001** (daban LiFePO4Mn). El contenedor correcto es `.product.attribute.description`
  5. **`analisis.py`**: campos `bateria_quimica`/`precio_valor`/`moneda`; `modelo_norm` incluye la química **solo en eléctricos** (en híbridos la batería es el extensor, no define variante); `es_viva` excluye `condicion="agotado"`; columnas nuevas `precio_valor` y `monedas`
  6. **Cabecera del scraper** actualizada: islagrande pasa a fuente activa; vedca.cu marcado caído; nota del selector de moneda
- **Resultado:** Scraper **33 → 42 registros** (+9 islagrande) / **28 → 35 modelos**. `VEDCA C400 LIFEPO4` mantiene sus números intactos (**1200 W · 500 kg · 120 km · $4.550**, `oferta_viva=True`, `n_anuncios=1/2`; solo cambia el nombre al separarse de GelPb). Nuevos modelos islagrande (todos `oferta_viva=False`, precio en **EUR**): C400 GELPB, C400A GELPB, C400 LIFEPO4MN, C600 LIFEPO4, C600 GELPB, C800B, C800B FOTOVOLTAICO, C300, SH001. Se renombran por química 9 eléctricos de elyerromenu (p. ej. KIVITOVA→…GELPB). **Efecto colateral:** 3 modelos eléctricos no-VEDCA cambian de score (ELECTRICO CARGA TECHO 0.675→0.683; NIPPON SE 0.532→0.591; VIENTO RAPIDO 0.477→0.545) porque el **min/max del grupo eléctrico** se amplía con las specs de islagrande (la normalización es intra-grupo)
- **Error/éxito:** Éxito tras corregir el bug de contaminación por "Up-Sell". Backup del JSONL en `/tmp/opencode/anuncios_triciclos.prebackup.20261011-231056.jsonl` y del score en `/tmp/opencode/score_modelos.prebackup.*.csv`. Compilan ambos scripts. Git: 6 archivos `M` + `__pycache__/` sin ignorar
- **Lección:** Acotar la extracción por **contenedor del DOM**, no por ventana de texto: los carruseles de "productos recomendados" contaminan química y specs (mismo patrón que el pie "Categorías" de elyerromenu). Y al añadir una fuente, los scores **relativos** de todo el grupo pueden moverse aunque esa fuente no tenga precio: la normalización min-max es sensible a los extremos nuevos
- **Próxima vez:**
  1. Decidir el destino de `Data/raw_data/data_from_FB` (sigue sin integrar)
  2. Pendientes vivos: `repuestos_proxy` (1 modelo de 35), `precio_texto_usd` (3 anuncios contradictorios), trabajo de campo (15 municipios, 8h)
  3. Considerar `.gitignore` para `__pycache__/`
  4. Mejora menor detectada: `extract_battery` de elyerromenu no lee "72v/58ah" (barra) — Kivitova queda sin V/Ah (preexistente)
- **Etiquetas:** islagrande, integracion, variantes-bateria, quimica-bateria, bug-upsell, precio-eur, es-viva, agotado, analisis, min-max-grupo

---
