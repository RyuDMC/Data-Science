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

## Reflexión final de sesión

### Sesión 2026-09-17 → 2026-09-18

- **¿Qué patrón veo?** El mercado automotor cubano es consistente: mercado informal (clasificados, precios en USD) que responde a cada reforma legal (292/2011, 320/2013, 2025, 163/2026). La fuente del repo (2014) y los trabajos de 2026 repiten la misma estructura analítica. La tarea de "encontrar similares" es un ciclo que ya se automatizó: leer fuente → identificar género → buscar sucesores → cruzar 2-3 fuentes → clasificados para precios.
- **¿Qué haría diferente?** Verificar vigencia normativa antes de citar el 2025 (decreto 163/2026 la superó). Anticipar 403 en medios cubanos (elTOQUE) usando snippets del search como plan B desde el inicio. Guardar los enlaces completos (no truncados) apenas se obtienen.
- **¿Qué debo recordar sí o sí?** El diario vive en JOURNAL.md (leerlo al iniciar, escribir al actuar). El género del mercado autos cubano = regulación + precios informales + crítica. Para precios 2026: Revolico. Marco vigente: Decreto 163/2026.
