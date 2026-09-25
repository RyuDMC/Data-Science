# JOURNAL — Diario operativo

Memoria episódica del agente. Consultar antes de actuar; escribir solo después de actuar. Formato de consulta: "Consulta de diario: [criterio]. Entradas relevantes: [resumen]. Aplicaré: [acción]."

---

### Entrada de diario

- **Fecha/contexto:** 2026-09-17 — sesión en opencode, proyecto "Default Project"
- **Tarea:** Adoptar comportamiento de journaling y crear JOURNAL.md como diario persistente
- **Acción(es):** Leído el prompt fuente (github.com/RyuDMC/Data-Science → Journaling Prompt.md); creado este archivo en el proyecto
- **Resultado:** JOURNAL.md creado; diario activo en archivo
- **Error/éxito:** Éxito a la primera
- **Lección:** La conversación no persiste entre sesiones; el diario debe vivir en archivo del proyecto
- **Próxima vez:** Al iniciar sesión, leer JOURNAL.md antes de actuar; al cerrar, entregarlo al usuario para guardarlo
- **Etiquetas:** setup, journaling, infraestructura

---

### Entrada de diario

- **Fecha/contexto:** 2026-09-18 — investigación mercado automotriz cubano
- **Tarea:** Obtener información sobre compra de autos en Cuba 2025
- **Acción(es):** Fetched directoriocubano.info (precios, modelos, requisitos de importación 2025)
- **Resultado:** Marco normativo (CIMEX/TRANSIMPORT/DIVEP/DUNA), aranceles ($100-$300+$8), margen comercial hasta 20%, IEPS hasta 35%, 4% traspaso patrimonial; catálogo de modelos con precios USD
- **Error/éxito:** Éxito
- **Lección:** Preferir fuentes cubanas actualizadas; distinguir normas 2025 vs. 2026
- **Próxima vez:** Verificar vigencia normativa (Decreto 163/2026 la superó)
- **Etiquetas:** investigación, autos, cuba, importación

---

### Entrada de diario

- **Fecha/contexto:** 2026-09-18 — trabajo similar al artículo de OnCuba 2014
- **Tarea:** Usar la parte del mercado automovilístico de "Links de Referencias.md" para encontrar trabajos similares en Cuba
- **Acción(es):** Fetched cubainformacion.tv (2014, fuente del repo); websearch sobre mercado automotriz cubano; revisados resultados de elTOQUE, CiberCuba, Revolico, AutoCubana
- **Resultado:** Sucesores naturales identificados: elTOQUE y CiberCuba (ago 2026) sobre nuevas reglas de compra/venta/importación; elTOQUE sobre comercio EE.UU.→Cuba; clasificados Revolico como vitrina de precios informales (mismo método de 2014)
- **Error/éxito:** Éxito a la primera
- **Lección:** El género es estable: análisis de regulación + precios de mercado informal; el 2026 lo encabezan los eléctricos y el Decreto 163/2026
- **Próxima vez:** Cruzar datos de al menos 2 fuentes (elTOQUE + CiberCuba) antes de concluir
- **Etiquetas:** investigación, autos, cuba, comparativa, fuente-externa

---

### Entrada de diario

- **Fecha/contexto:** 2026-09-18 — uso de "Links de Referencias.md" (parte Mercado Automovilístico) para encontrar artículos similares en Cuba
- **Tarea:** Partiendo del artículo de 2014 (cubainformacion.tv: "El mercado automovilístico en Cuba: surrealismo antillano"), hallar artículos equivalentes 2025-2026
- **Acción(es):** Fetched el archivo fuente y el artículo original (2014); 2 websearches (mercado automotriz + Decreto 163/2026); cruce de fuentes
- **Resultado:** El género del 2014 = regulación jurídica + precios de mercado informal (clasificados) + crítica. Sucesores 2026: CiberCuba ×5 (reglas compra/venta/importación, impuestos, vigencia, eliminación del límite de 6 autos, importación directa eléctricos), elTOQUE Jurídico (importación eléctricos, motos >1000W), AP/Chicago Tribune (cerco energético + flexibilización), cubainformacion.tv (Transporte: movilidad eléctrica), directoriocubano.info, cubanoticias360, americateve. Marco actual: Decreto 163/2026 + R.172/2026 + Comité Evaluador de Medios Automotores; tasas 35/25/20/15/5/3%; eléctricos exentos con estación renovable. El 2014 usó Porlalivre (3 705 anuncios); hoy la misma vitrina informal es Revolico
- **Error/éxito:** Éxito parcial; elTOQUE devolvió 403 al fetch directo (cubierto vía extractos del search)
- **Lección:** El cruce elTOQUE + CiberCuba + una fuente internacional (AP) basta para un panorama robusto; los clasificados (Revolico) siguen siendo la vía para replicar el análisis de precios del 2014
- **Próxima vez:** Prever bloqueos (403) en medios cubanos: usar search snippets como respaldo antes de iterar
- **Etiquetas:** investigación, autos, cuba, comparativa, fuente-externa, mercado-informal

---

### Entrada de diario

- **Fecha/contexto:** 2026-09-22 — sesión opencode, proyecto "Default Project"
- **Tarea:** Continuar el trabajo del diario: completar la pieza pendiente del 18-sep — precios del mercado informal cubano 2026 vía clasificados (Revolico)
- **Acción(es):** Consulta de diario ("¿Qué experiencias se parecen?") → aplicación de lecciones previas (cruce de fuentes, verificar vigencia Decreto 163/2026). Fetch a Revolico: portada → extracción de hrefs reales de categorías del HTML → fetch de categoría Carros (1.ª página, ~90 anuncios)
- **Resultado:** Vitrina de precios 2026 (USD, mercado informal):
  - Clásicos/nacionales: VW Escarabajo 86: 5 000; Dodge/Plymouth 1954: 6 000-6 500; Moskovich: 5 000-6 500; Fiat 125: 5 500; VW Jetta 91: 13 000; Bel Air 1957: 29 000
  - Segmento medio coreano/chino: MG3 2019: 15 000; Grand i10 2021: 16 000; Picanto 2017-2020: 17 000-18 500; Kia Morning 2020: 18 500; Elantra 2019: 20 000-20 500; Sonata 2017: 20 000; Tucson 2017-2021: 20 000-24 000; Chery Tiggo 4 2020: 20 500; Corolla 2023: 34 000
  - SUV/sedán modernos: Santa Fe 2017-2024: 22 000-56 000; Sportage 2024: 42 000; X-Trail 2024: 32 000; VW ID4 2021: 38 000; Honda Accord 2022-2025: 30 000-35 000
  - Eléctricos (tope del mercado): Nissan Leaf 2019: 30 000-32 000; Bestune 2026 (0 km): 33 000-34 000; Dongfeng Vigo Pro/Bestune T55: 30 000-36 000; IONIQ 5 2024-25: 36 000-47 000; IONIQ 6 2024-25: 40 000-53 000; Voyah Free 318 2026 (híbrido): 82 000; Mercedes C300e 2022 híbrido: 80 000; Nissan Titan 2016: 51 000
- **Error/éxito:** Éxito parcial. Fallos: websearch cancelado/indisponible toda la sesión; /category/carros (transport) y /search/carros y /vehiculos/carros (404) no funcionan. Resuelto: portada + grep de hrefs → ruta correcta `search?category=vehiculos&subcategory=vehiculos-carros`
- **Lección:** El patrón de URL de Revolico cambió: las categorías viven en `/search?...&subcategory=...` (el viejo `/category/` ya no responde); ante un sitio JS/SPA, fetchear la portada y grepear hrefs del HTML es el atajo fiable. Confirma la tesis del diario: en 2026 el tope del mercado informal lo ocupan los eléctricos (Bestune, IONIQ 5/6, VW ID4, Leaf) y el medio lo dominan coreanos/chinos; clásicos y nacionales quedan en la franja baja (5 000-30 000 USD)
- **Próxima vez:** Ir directo a la ruta correcta sin iterar; muestrear 2-3 páginas (hay 6) para una muestra comparable a Porlalivre 2014 antes de concluir promedios
- **Etiquetas:** investigación, autos, cuba, precios, mercado-informal, revolico, 2026

---

### Entrada de diario

- **Fecha/contexto:** 2026-09-22 — ejecución del prompt "Prompt_for_search_data_sources.md" (buscar fuentes de datos para un mercado; pedir mercado antes de buscar)
- **Tarea:** Hallar fuentes de datos (sitios/apps, publicaciones de ventas, grupos/canales, sitios de anuncios) para el mercado de **triciclos** en Cuba
- **Acción(es):** Preguntado tipo de mercado (respuesta: triciclos). Websearch integrado seguía caído → usado DuckDuckGo HTML vía webfetch como motor (nuevo método que funcionó). Feches verificatorios a Revolico (search q=triciclo, ~100 anuncios) y a catálogos (cubancargos, vedca.cu, kikihabana, compramasonline, elyerromenu/Cuba Sobre Ruedas, islagrande), Telegram (t.me/MotosBateriasElectricasCuba, @cubaventas) y artículos regulatorios (CiberCuba, Cubadebate, Prensa Latina, periodicocubano, directoriocubano)
- **Resultado:** Entrega con ~30 fuentes verificadas agrupadas en 4 categorías: productores (VEDCA), tiendas de envíos (kikihabana, compramasonline, cubancargos, Islagrande, Full-Envío), vendedores con catálogo (Cuba Sobre Ruedas/El Yerro), clasificados (Revolico, Anuncios_cu), grupos FB/Telegram, y marco regulatorio (Decreto 163/2026, Instrucción 1/2026, importación 1 triciclo/residente, ~70% de ventas son ciclomotores/motos/triciclos). Precios clave Revolico: 1 800–7 100 USD; El Yerro: triciclos 3 550–6 600 USD
- **Error/éxito:** Éxito. Fallos menores: full-envio.com y vedca.cu (https) dieron error de transporte (vedca resuelto con http); Facebook no admite fetch directo (verificado vía snippets)
- **Lección:** El método DDG-HTML vía webfetch reemplaza al websearch cuando está caído. Facebook = verificación por fragmentos del buscador, nunca por fetch. Para mercados con "triangular" estatal + informal, combinar productor oficial + tiendas de envío + clasificados + prensa regulatoria da un mapa completo
- **Próxima vez:** Reutilizar perfil de búsqueda: 2-3 búsquedas DDG por tipo de fuente + verificación directa de lo esencial + marcar verificados (✅) vs indexados (🔎)
- **Etiquetas:** búsqueda-fuentes, datos, triciclos, cuba, automotriz, verificación, 2026

---

### Entrada de diario

- **Fecha/contexto:** 2026-09-22 — segunda ejecución del prompt "Prompt_for_search_data_sources.md" (nuevo mercado)
- **Tarea:** Hallar fuentes de datos para el mercado de **paneles solares** en Cuba
- **Acción(es):** Preguntado mercado (respuesta: paneles solares). Método DDG-HTML + Revolico (search q=panel solar, ~130 anuncios) + verificación directa (electro-habana, tiendasolar, cubasolar, t.me/s/avatarenergia) + DDG para grupos FB/Telegram, instaladores y marco regulatorio
- **Resultado:** Entrega con ~25 fuentes verificadas: tiendas/instaladores (Electro Habana, Tienda Solar, Sunwell Caribe, Espoleta Solar, QvaSolar, SunCar, SalvaPC, Onfase, Kitsolares), clasificados (Revolico: paneles 120–300 USD; JINKO 620W bifacial 150; kits EcoFlow/Bluetti; servicios de instalación), grupos FB (Cuba Solar Baterías y Paneles; Todo de Paneles Solares Cuba; Instaladores y Proveedores) y Telegram (@HabaNetVenta, @cubaventas), y marco regulatorio fuerte (Res. 114/2026: 90 CUP/kWh excedentes; Res. 76/2025 y esquema estatal en USD: 1 kW/20 años pasó de 1 500 MLC a 600 USD; Res. 41/2026 beneficios fiscales; Decreto-Ley 345/2017)
- **Error/éxito:** Éxito. kitsolares.online e infinitysolarcuba.com no verificables por fetch (404/placeholder); cubasolar.cu verificado pero con contenido hasta 2024 (⚠️ vigencia)
- **Lección:** El mercado solar cubano es "doble": esquema ESTATAL (potencia contratada en USD, tarifas de excedentes) + mercado PRIVADO (paneles $120-300 USD en Revolico, tiendas con catálogo). Los materiales regulatorios de 2026 (Res. 114/2026, 76/2025, 41/2026) son la mina de oro para análisis de precios/incidencia
- **Próxima vez:** Para mercados de energía incluir siempre instancias oficiales (MFP/MINEM/Gaceta) además de compraventa informal; verificar fecha de vigencia de cada resolución citada
- **Etiquetas:** búsqueda-fuentes, datos, paneles-solares, cuba, energía, regulación, verificación, 2026

---

### Entrada de diario

- **Fecha/contexto:** 2026-09-22 (noche) — ejecución del prompt "Prompt_data_structure.md" (crear estructura de datos JSON para un mercado) sobre el **Mercado Inmobiliario** cubano, con los enlaces de `Data/Posibles fuentes de datos.md`
- **Tarea:** Diseñar una estructura limpia, eficiente y simple para almacenar anuncios inmobiliarios de los 10 portales dados, definiendo campos comunes reales (sin inventar datos) y campos de interés, en JSON con explicación de cada campo
- **Acción(es):** Fetched de los 10 sitios de la sección Inmobiliaria (Revolico: portada + `/search?category=inmobiliaria` + anuncio individual; GAOS: portada + ficha detallada; Casas Oasis; HogarEnCuba; CubanOSS; ElCaimán; Cubisima; AlojamientosEnCuba; Porlalivre; CasasCubaOficial vía curl → SPA base44). Ampliado con búsqueda de grupos de Facebook inmobiliarios verificada por snippets DDG-HTML (el prompt original no los incluía; el usuario pidió considerarlos). Guardado el entregable en `Data_Structure_for_Inmbuebles.md`
- **Resultado:** Schema `mercado_inmobiliario_cuba_v1` (JSON) con bloques: identificación/fuente, precio (monto+moneda+periodicidad+% rebaja), tipo de inmueble (11 valores), ubicación jerárquica (provincia→municipio→zona→dirección→coordenadas), dimensiones (hab/baños/niveles/superficie), estado y construcción (vocabulario de Casas Oasis), ~35 características booleanas (incl. respaldo energético, 2026), anunciante (particular/agente/agencia + verificado), contacto, fotos/visitas/destacado, permuta (1x1/1x2/múltiple) y metadatos de captura. 12 grupos FB verificados en 4 categorías (venta, permuta, renta, oficial Revolico) marcados 🔎 no scrapeables. Viabilidad: ✅ HTML (Revolico, Cubisima, HogarEnCuba, AlojamientosEnCuba), ⚠️ SPA/XHR (GAOS Supabase, Oasis, CubanOSS, ElCaimán, CasasCubaOficial base44), ❌ Porlalivre en renovación (figura como viable en el repo pero hoy no expone anuncios), 🔎 FB solo snippets/Graph API
- **Error/éxito:** Éxito. Fallos: Porlalivre en renovación (solo landing "Próximamente"); CasasCubaOficial devuelve HTML vacío (#root SPA) → resuelto con curl al HTML del shell y meta; websearch integrado aún caído → respaldo DDG-HTML; dos búsquedas exactas de FB sin resultados → reformuladas sin comillas
- **Lección:** La estructura del mercado inmobiliario cubano es convergente entre portales: acción + precio/moneda + tipo + jerarquía geográfica + hab/baños + características booleanas; los campos ricos (estado, construcción) solo Casas Oasis los estructura, el resto los lleva en la descripción. Porlalivre, pese a estar listado como viable, está fuera de servicio hoy → toda fuente "viable" del repo requiere re-verificación antes de automatizar
- **Próxima vez:** Para SPA (GAOS/Oasis/CasasCubaOficial) priorizar búsqueda de endpoints XHR/JSON (DevTools) antes que Playwright; marcar Porlalivre como pendiente de reverificación en el repo; cuando el usuario pide "tener en cuenta" algo no listado (FB), verificar por snippets y añadirlo como bloque 🔎 sin mezclarlo con el dataset estructurado
- **Etiquetas:** estructura-datos, inmobiliario, cuba, json, scraping, facebook, verificación, 2026

---

### Entrada de diario

- **Fecha/contexto:** 2026-09-23 — ejecución del prompt "Prompt_data_structure.md" sobre el **Mercado Automovilístico** cubano, con los enlaces de `Data/Posibles fuentes de datos.md` (sección `# Mercado Automovilistico`)
- **Tarea:** Diseñar una estructura JSON limpia, eficiente y simple para almacenar anuncios del mercado automotriz de las fuentes dadas, definiendo campos comunes reales (sin inventar datos) y explicando cada campo
- **Acción(es):** Fetch de las fuentes del listado: atrexport (catálogo gasolina, precios "Desde X €"), mcvcommercial (solo shell SPA), autocubana (listado de 664 vehículos + ficha detallada BYD S6 con campos estructurados), ventacuba (osclass, categorías y precios CUC/USD/EUR), cubisima/carros (directorio de marcas + listado + ficha Honda Accord con detalle completo), ofertas.cu (2 reintentos fail), apululu (filtros y precios), revolico vehiculos-carros (confirmado). Grupos FB intentados por DDG (no indexados → se marcan 🔎 sin nombre). Guardado el entregable en `Data_Structure_for_Autos.md`
- **Resultado:** Schema `mercado_automovilistico_cuba_v1` (JSON) con bloques: identificación/fuente (patrones de id por portal), fechas (publicación/creación/captura), precio (monto+moneda de 5 monedas coexistentes USD/CUC/CUP/EUR/MLC + "es_precio_desde" para catálogos ATR + estado_precio: disponible/negociable/llamar_para_precio/sin_precio/no_disponible), vehículo (tipo, marca, modelo, año, época de fabricación, carrocería, combustible, transmisión, km, condición, colores, tracción, dirección, equipamiento booleano), ubicación provincia→municipio, canal_comercial (venta_local/importación/coche_en_plaza/renta_leasing/compra_publicada), anunciante (particular/agencia_importadora/comercio), estado_comercial (en_venta/vendido), métricas y metadatos de captura. Corrección al handoff: Autocubana y Apululu sirven HTML completo (no necesitan Playwright). Viabilidad: ✅ HTML (Revolico, Cubisima, VentaCuba, Autocubana, Apululu, ATR), ⚠️ SPA (MCV), ❌ Ofertas.cu no responde hoy (HTTP 000), 🔎 no scrapeables (2 grupos FB + elBacheBot)
- **Error/éxito:** Éxito (con correcciones al handoff y 1 pendiente). Fallos: ofertas.cu inaccesible (http y https, curl y webfetch) → pendiente de reverificación; búsquedas DDG con `site:facebook.com/groups/ <id>` sin resultados (IDs no indexados) → no se inventaron nombres de grupo
- **Lección:** El mercado automovilístico cubano es convergente en el esqueleto (título, precio+moneda, marca/modelo/año, ubicación, anunciante) pero su rasgo distintivo es la **bicoexistencia local/importación** (mercado en plaza vs catálogos "Desde €" de ATR/MCV) y la **multiplicidad de monedas** que obliga a guardar moneda explícita. Autocubana (no el esperado) es la fuente más estructurada; VentaCuba es la más ruidosa (spam)→ filtrar por estado_precio + umbral de monto. La "época de fabricación" (filtro Cubisima) es un campo analítico valioso para el parque cubano
- **Próxima vez:** Revisar la clasificación del handoff para autos (Autocubana/Apululu ✅ HTML; ofertas.cu a reverificar); para detalle de anuncios usar Cubisima (ficha con CIF Maríel) y Autocubana (ficha completa); filtrar spam de VentaCuba con marca/descripción
- **Etiquetas:** estructura-datos, automovilístico, cuba, json, scraping, importación, verificación, 2026

---

### Entrada de diario

- **Fecha/contexto:** 2026-09-23/24 — ejecución del prompt "Prompt_data_structure.md" sobre el **Mercado de Motorinas, Bicicletas Eléctricas y Patinetes Eléctricas** cubano, con los enlaces de `Data/Posibles fuentes de datos.md` (sección `# Mercado de Motorinas, Bicicletas Eléctricas y Patinetes Eléctricas`)
- **Tarea:** Diseñar una estructura JSON limpia, eficiente y simple para almacenar datos del mercado usando solo la información de los 6 enlaces dados (2 tiendas + 4 grupos FB), explicando cada campo
- **Acción(es):** Fetch de islagrande.com/vehiculos-electricos.html (Magento: 29 productos en 3 páginas, precios EUR, "Out of stock", descuentos Special/was, ficha técnica completa de la moto LT-4206 con SKU `VDC4206-72V45AH-HAV`, "Supplied By VEDCA" con rating 5.0, retiro en almacén VEDCA La Habana), multiservicesxpress (WooCommerce: 5 bicicletas + 4 motos eléctricas, precios USD, "Select options" variantes, SKU `BICI BUCATTI-1`, tabla peso/dimensiones/colores, REST wp-json y feed RSS detectados); los 4 grupos FB verificados por búsqueda exacta DDG (no indexados → 🔎). Guardado el entregable en `Data_Structure_for_Movilidad_Electrica.md`
- **Resultado:** Schema `mercado_movilidad_electrica_cuba_v1` (JSON) con bloques: identificación/fuente (SKU o slug como id_externo), fechas (publicación null — los catálogos no la exponen; captura siempre), precio (monto+moneda EUR/USD + es_oferta + monto_anterior + descuento_porciento), **stock** (disponible/agotado/con_variantes — el estado determinante de este mercado), vehículo/producto (tipo con 10 valores incl. patinete reservado; marca/modelo; especificaciones con batería tipo/voltaje/Ah, motor W, velocidad, autonomía, peso, dimensiones, colores, garantía, frenos, llanta; extras booleanos), canal_comercial (tienda_envios/proveedor_en_tienda/grupo_facebook; envio_a_cuba; retiro_almacén; pagos TropiPay/Visa/MC/cripto), ubicación_entrega (La Habana/Boyeros/almacén VEDCA + origen vendedor Miami), anunciante (tienda + proveedor tercero + teléfonos +53/+1), métricas (rating vendedor, reviews, nº productos) y metadatos de captura. Hallazgo de cobertura: **ninguna tienda lista patinetes**; los catálogos cubren motos/scooters/bicis/bici-motos/triciclos/baterías. Corrección al handoff: MultiServicesXpress ✅ HTML server-rendered + wp-json (no "parcial/XHR")
- **Error/éxito:** Éxito. Fallos menores: 4 búsquedas DDG exactas de IDs de grupo sin resultados (no indexados) → sin inventar nombres; ficha de variantes (delta de precio por color) no verificada → quedó fuera
- **Lección:** Este es el mercado de importación pura por tiendas de envío: monedas EUR/USD (cero CUP/CUC), fechas de publicación ausentes, y el **stock** ("Out of stock") como estado comercial dominante en contraste con los clasificados de autos/inmuebles (donde manda el precio). La ficha técnica (batería/motor/autonomía) es el bloque más valioso y se repite entre importadores → el par marca+modelo+batería permite cruzar ofertas de tiendas distintas. WooCommerce/Magento sirven HTML completo: el patrón "tiendas de envío" es scrapeable sin Playwright
- **Próxima vez:** Para datificar patinetes habrá que acudir a los grupos FB (Graph API/manual) o buscar otras tiendas; al automatizar MultiServicesXpress usar `/wp-json` y el feed `/feed/` antes que parsear HTML; registrar precios EUR de Islagrande con su fecha porque hay selector USD que puede cambiar la moneda mostrada
- **Etiquetas:** estructura-datos, movilidad-eléctrica, motorinas, bicicletas, patinetes, cuba, json, scraping, verificación, 2026

---

### Entrada de diario

- **Fecha/contexto:** 2026-09-24 — ejecución del prompt "Prompt_data_structure.md" sobre el **Mercado de Triciclos** cubano, con los enlaces de `Data/Posibles fuentes de datos.md` (sección `# Mercado de Triciclos`). Desde esta sesión, JOURNAL y handoff viven en `Data/` del repo local (`/media/.../Data-Science/Data`)
- **Tarea:** Diseñar una estructura JSON limpia, eficiente y simple para almacenar datos del mercado usando solo los 12 enlaces dados (4 tiendas de envío + Revolico + 4 grupos FB + 3 Telegram), explicando cada campo
- **Acción(es):** Verificadas kikihabana (WooCommerce ✅: categoría "Carritos y Triciclos", 12 productos USD $2 800–$4 300, ficha IZUKI Titan p-3000 con specs completas y oferta 3 500→3 200 $), compramasonline (WooCommerce ✅: categoría triciclos/ 11 productos, extensores de rango $600–$700, combo RALLY+extensor), cubancargos (Next.js **SSR** ✅: PORTO BELLO/JINPEING/Furikazan híbridos 1100W + Nippon SE eléctrico, "Agotado", reseñas, 10% descuento, entrega 25–35 días a La Habana/Artemisa/Pinar del Río), revolico (bloqueado hoy directo: 403/transport → subcategoría oficial `vehiculos-motos-electricas-y-triciclos` verificada por snippets: precios 1 350–5 000 USD, specs en título, legalización "factura mipyme/chapa"), elyerromenu (SPA Nuxt bazar, **0 triciclos** en HTML), FB `todotricicloselectricos` ✅ verificado (grupo de la tienda Miami todotricicloselectricos.com, extensores 3000–5000W) + 3 IDs 🔎, Telegram 🔎. Guardado el entregable en `Estructuras/Data_Structure_for_Triciclos.md`
- **Resultado:** Schema `mercado_triciclos_cuba_v1` (JSON) con bloques: identificación/fuente (slug WooCommerce o `/item/<slug>-<id>` de Revolico), fechas (tiendas sin fecha de publicación; Revolico sí), precio (USD, monto+moneda+es_oferta+monto_anterior), estado (stock + condición nuevo_0km/usado/preventa), **triciclo** (uso carga/pasajeros/mixto/ocio, propulsión eléctrico/híbrido/gasolina, marca/modelo/año, **extensor de rango**, especificaciones: motor W, batería tipo/V/Ah, autonomía, velocidad, tiempo de carga, carga máx kg, capacidad personas, controlador Votol/24 tubos, cama, techo, colores), **legalizacion** (factura mipyme a nombre del cliente / chapa y permiso / arancel aduanal incluido — campo distintivo), canal_comercial (tienda_envios/clasificado; mensajería incluida a La Habana; 25–35 días; origen Miami o Cuba), ubicación del anuncio (municipios de La Habana), anunciante (tienda/mipyme/particular), métricas (reseñas) y metadatos de captura. Hallazgo de mercado: **2 capas** (tiendas de envío con triciclos nuevos y ficha técnica vs clasificados locales con usados/0km y papeles) y el **híbrido/extensor de rango** (3000–5000W) como rasgo del nicho. Corrección al handoff: CubanCargos SSR sirve el catálogo en HTML; El Yerro sin evidencia de triciclos
- **Error/éxito:** Éxito. Fallos: Revolico inaccesible directo desde este entorno (403 curl / transport webfetch) → snippets; kikihabana lento (webfetch timeout → curl 25s OK); 3 IDs FB sin indexar (sin inventar nombres)
- **Lección:** El mercado triciclos tiene 2 capas con campos distintos: tiendas (USD, catálogo, ficha técnica, entrega) y clasificados (condición, papeles/legalización, mensajería). El rasgo único del nicho es la **legalización** ("factura de mipyme a nombre del cliente", "directo a chapa", chapa y permiso) + el **triciclo híbrido con extensor de rango**, vendido como combo, accesorio o atributo. Los modelos se comparten entre canales (IZUKI, HUAIHAI, RALLY, Mighong) → marca+modelo+motor/batería cruza ofertas. WooCommerce/Next-SSR vuelven a confirmar que las "tiendas de envío" se scrapean sin Playwright
- **Próxima vez:** Para Revolico-triciclos muestrear la subcategoría completa cuando el entorno permita fetch (aún bloqueado); tratar el **extensor de rango** como entidad propia (producto y atributo); normalizar specs del título de Revolico contra la ficha de KikiHabana
- **Etiquetas:** estructura-datos, triciclos, cuba, json, scraping, legalización, híbrido, verificación, 2026

---

## Reflexión final de sesión

### Sesión 2026-09-17 → 2026-09-18

- **¿Qué patrón veo?** El mercado automotor cubano es consistente: mercado informal (clasificados, precios en USD) que responde a cada reforma legal (292/2011, 320/2013, 2025, 163/2026). La fuente del repo (2014) y los trabajos de 2026 repiten la misma estructura analítica. La tarea de "encontrar similares" es un ciclo que ya se automatizó: leer fuente → identificar género → buscar sucesores → cruzar 2-3 fuentes → clasificados para precios.
- **¿Qué haría diferente?** Verificar vigencia normativa antes de citar el 2025 (decreto 163/2026 la superó). Anticipar 403 en medios cubanos (elTOQUE) usando snippets del search como plan B desde el inicio. Guardar los enlaces completos (no truncados) apenas se obtienen.
- **¿Qué debo recordar sí o sí?** El diario vive en JOURNAL.md (leerlo al iniciar, escribir al actuar). El género del mercado autos cubano = regulación + precios informales + crítica. Para precios 2026: Revolico. Marco vigente: Decreto 163/2026.

### Sesión 2026-09-22

- **¿Qué patrón veo?** El ciclo del diario se completó: la pieza "precios informales 2026" que quedó pendiente el 18-sep se resolvió exactamente por la vía predicha (Revolico). Los fallos de la sesión (websearch caído, URLs viejas de Revolico) se superaron con el método aprendido: fetch + grep de hrefs.
- **¿Qué debo recordar sí o sí?** Ruta correcta de Revolico: `https://www.revolico.com/search?category=vehiculos&subcategory=vehiculos-carros`. Los eléctricos (Bestune, IONIQ 5/6, ID4) son el tope de precios 2026 (30 000-82 000 USD); el medio lo dominan coreanos/chinos (15 000-25 000 USD); clásicos y nacionales abajo (5 000-30 000 USD).

### Sesión 2026-09-22 (tarde) — búsqueda de fuentes (triciclos + paneles solares)

- **¿Qué patrón veo?** Dos mercados distintos, mismo esqueleto de fuentes: productor oficial (VEDCA / esquema estatal solar) + tiendas de envío directo a Cuba (kikihabana, cubancargos, compramasonline) + catálogos de vendedores (Cuba Sobre Ruedas / Electro Habana) + clasificados (Revolico) + grupos FB/Telegram. En ambos, el cruce prensa-regulación 2026 (Decreto 163/2026 para autos; Res. 114/2026, 76/2025 y 41/2026 para solar) es lo que da valor analítico. El mercado solar live en la paradoja "estatal en USD vs. privado en USD".
- **¿Qué debo recordar sí o sí?** Cuando el websearch integrado falle, `https://html.duckduckgo.com/html/?q=...` vía webfetch es el motor de respaldo. Facebook solo se verifica por snippets del buscador. Marcar fuentes ✅ (fetch directo) vs 🔎 (indexadas). Para energía, siempre incluir MFP/MINEM/Gaceta y verificar vigencia de cada resolución (hay contenido 2024 aún en circulación).

### Sesión 2026-09-22 (noche) — estructura de datos inmobiliario

- **¿Qué patrón veo?** El ciclo del prompt `Prompt_data_structure.md` cierra el flujo de fuentes: primero se buscan fuentes (triciclos/paneles), luego se clasifican por scraping y ahora se les da estructura de datos. El mercado inmobiliario repite el esqueleto de los otros mercados: portales oficiales/clasificados + vendedores directos + grupos FB/Telegram (no scrapeables) — y la estructura JSON resultante es reutilizable para cualquier mercado.
- **¿Qué debo recordar sí o sí?** La clave de deduplicación es url + id_externo (HEC####, UUIDs GAOS, slugs Revolico). Porlalivre está en renovación: reverificar antes de automatizar. Los grupos FB inmobiliarios solo se verifican por snippets (Graph API/página o manual). Schema guardado en `Data_Structure_for_Inmbuebles.md`.

### Sesión 2026-09-23 — estructura de datos automovilístico

- **¿Qué patrón veo?** El ciclo `Prompt_data_structure.md` se repite mercado a mercado con el mismo esqueleto (identificación, precio+moneda, tipo, geografía, físico, anunciante, métricas, captura). La novedad del automovilístico es la **bicoexistencia local/importación** (clasificados en plaza vs catálogos de importadoras con "Desde €") y el **ruido** (spam en VentaCuba, piezas a 1 USD en Cubisima/Revolico) que obliga a un `estado_precio` explícito. Autocubana desmiente el handoff: es HTML completo y la fuente con ficha más rica.
- **¿Qué debo recordar sí o sí?** Guardar siempre `moneda` + `fecha_captura` (5 monedas coexistentes, CUC legacy con conversión 1:1). Campo `es_precio_desde` para catálogos de importación. Ofertas.cu no responde hoy (HTTP 000): reverificar. Schema guardado en `Data_Structure_for_Autos.md`.

### Sesión 2026-09-23/24 — estructura de datos movilidad eléctrica

- **¿Qué patrón veo?** El ciclo `Prompt_data_structure.md` ya es un molde estable que se llena mercado a mercado; la variante aquí es el **mercado de importación pura**: tiendas de envío (Islagrande/MultiServicesXpress) con precios EUR/USD, sin fechas de publicación y con el **stock** como señal dominante ("Out of stock" en casi todo el catálogo de Islagrande) — opuesto a los clasificados locales donde manda el precio. WooCommerce y Magento sirven HTML completo: los "dinámicos" del handoff vuelven a desmentirse (como Autocubana/Apululu). La ficha técnica (batería, motor, autonomía) es el activo único de este mercado y permite cruzar el mismo producto entre importadores por marca+modelo+batería.
- **¿Qué debo recordar sí o sí?** En este mercado no hay CUP/CUC ni fecha de publicación: `moneda` (EUR/USD) + `captura` + `stock` son el trío crítico. MultiServicesXpress expone REST `wp-json` y feed RSS por categoría (usar antes que HTML). Ninguna tienda lista patinetes: ese segmento solo vive en FB (🔎). Schema guardado en `Data_Structure_for_Movilidad_Electrica.md`.

### Sesión 2026-09-24 — estructura de datos triciclos

- **¿Qué patrón veo?** El molde `Prompt_data_structure.md` ya está consolidado (identificación, precio+moneda, físico/técnico, geografía, canal, anunciante, métricas, captura) y el triciclos lo llena con 2 rasgos únicos: la **legalización** como campo de precio implícito ("factura de mipyme a nombre del cliente", "directo a chapa") — señal de mercado maduro con subcategoría propia en Revolico — y la **propulsión híbrida / extensor de rango** (3000–5000W) vendido como combo, accesorio ($600–$700) o atributo. Se confirma además el patrón de infraestructura: las tiendas (WooCommerce, Next-SSR) se scrapean en HTML puro, y Revolico sigue siendo el clasificado de referencia (hoy bloqueado desde este entorno → snippets).
- **¿Qué debo recordar sí o sí?** Todo el mercado opera en USD. Revolico-triciclos = `search?category=vehiculos&subcategory=vehiculos-motos-electricas-y-triciclos`. Los modelos se repiten entre canales (IZUKI, HUAIHAI, RALLY, Mighong): la clave de cruce es marca+modelo+motor/batería. El "extensor de rango" debe modelarse como entidad propia. Schema en `Estructuras/Data_Structure_for_Triciclos.md` (repo local Data).