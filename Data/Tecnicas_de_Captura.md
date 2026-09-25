# Técnicas de Captura del Dato — Mercados cubanos estudiados

Playbook técnico para capturar, parsear, normalizar y almacenar datos de los mercados ya modelados
(inmobiliario, automovilístico, movilidad eléctrica, triciclos), a partir de lo **observado y verificado**
en las fuentes (2026-09-17 → 2026-09-24). Cada técnica indica el estado real del acceso (✅ directo,
⚠️ requiere JS, 🔎 no scrapeable) y los endpoints usados.

```text
Pipeline general
┌─────────────┐ ┌────────────┐ ┌────────────┐ ┌───────────────┐ ┌──────────────┐
│ 1. Mapeo    │→│ 2. Descarga│→│ 3. Parseo  │→│ 4. Normaliza  │→│ 5. Almacena  │
│    fuente → │ │    HTTP    │ │    HTML/   │ │    al esquema │ │    JSONL +   │
│    plantilla│ │    + caché │ │    JSON    │ │    + dedup    │ │    validación│
└─────────────┘ └────────────┘ └────────────┘ └───────────────┘ └──────────────┘
```

---

## 0. Cómo funciona por dentro — visión conceptual

**¿Qué es "capturar un dato"?** Pedirle a un servidor una URL (una pregunta) y leer la respuesta.
La respuesta viene en un **formato** y ese formato define la técnica:

- **HTML** — página pensada para humanos (navegadores la "dibujan"). Para extraer hay que *parsear*
  (buscar elementos por selectores con BeautifulSoup).
- **JSON/XML** — datos pensados para máquinas (APIs y feeds). Llegan ya estructurados: solo hay que
  leerlos y normalizarlos. **Siempre preferible al HTML.**

Los 3 ejes que deciden la técnica (árbol de decisión):

```text
1) ¿Dónde se construye la página?
     · En el servidor (SSR: WooCommerce, Magento, Next.js SSR)  →  el HTML ya trae todo → requests + BS4
     · En el navegador (SPA: Nuxt/Vue/React)                    →  el HTML es un cascarón; la data llega
                                                                   por llamadas JSON internas (XHR)
       → opción A: reproducir esas llamadas con requests (reverse-XHR, ligero)
       → opción B: navegador automatizado con Playwright (fiable pero pesado)
2) ¿El sitio ofrece una API pública?  (wp-json, wc/store, /feed/) → requests + JSON (más limpio que HTML)
3) ¿Hay barreras?  (403 Cloudflare, 429 rate-limit, timeouts)    → cortesía (ritmo, backoff, caché, UA);
   si todo falla → snippets del buscador (verificación muestral, no corpus completo)
```

**Las 4 fases de todo pipeline** — cada una con su ejemplo real del piloto triciclos:

```text
DESCARGA        →  requests.get(url)  →  obtienes bytes/texto (HTML o JSON)
                   Ej: GET /wp-json/wc/store/v1/products?per_page=100 (JSON) o el grid de KikiHabana (HTML)
PARSEO          →  extraer lo que te interesa del formato crudo
                   Ej: selector ul.products li.product → título, href, precio; o precios['price'] del JSON
NORMALIZACIÓN   →  transformar lo crudo a los campos del esquema (la "cocina")
                   Ej: "330000" (centavos) → 3300.00 USD · "El precio original era: 3,500.00$…" → es_oferta
ALMACENAMIENTO  →  guardar con procedencia (metodo + fechas.captura) y clave de dedup schema|url|captura
                   Ej: JSONL con una línea por registro
```

**La regla de oro**: prefiere JSON estructurado → usa HTML solo si no hay API → Playwright solo si el
HTML es cascarón → snippets solo como rescate muestral. Y **nunca inventes un dato**: si no se vio, `null`.

---

## 1. Matriz técnica por fuente (lo verificado)

| Fuente | Plataforma | Técnica recomendada | Estado | Endpoints / detalles |
|---|---|---|---|---|
| **Revolico** (todos los mercados) | HTML clasificados | requests + BS4; paginación por subcategoría | ✅ (bloqueado desde este entorno: 403/transport → fallback **snippets DDG**) | `https://www.revolico.com/search?category=<c>&subcategory=<sc>&page=N` · detalle `/item/<slug>-<id>` · verificado: `vehiculos` / `vehiculos-motos-electricas-y-triciclos` (triciclos). Otras subcategorías confirmar desde el menú de la portada |
| **Islagrande** | Magento | HTML catálogo paginado | ✅ | `https://islagrande.com/vehiculos-electricos.html` + `?p=2`/`?p=3` (29 productos); specs en pestaña "Details" o título; "Out of stock"; SKU `VDC4206-72V45AH-HAV`; precios EUR; pagos TropiPay/Visa/MC/crypto |
| **MultiServicesXpress** | WooCommerce | HTML + **REST wp-json + RSS** | ✅ | `/producto/<slug>/` · `/wp-json/wp/v2/product?per_page=100&page=N` · `/feed/` o `/category/.../feed/` · USD con descuentos −19%…−7% · variantes "Select options" · SKU `BICI BUCATTI-1` · tabla peso/dimensiones/colores |
| **KikiHabana** | WooCommerce | HTML + wp-json | ✅ (lento: dar timeouts de 60–75 s) | `/categoria-producto/.../carritos-y-triciclos/` · `/producto/<slug>/` · ficha técnica en la descripción · oferta "El precio original era: X. El precio actual es: Y" · atributo color (variantes) |
| **CompraMásOnline** | WooCommerce | HTML + wp-json | ✅ | `/categoria-producto/triciclos/` (11 productos + extensores) |
| **Apululu / Autocubana** | WooCommerce | HTML + wp-json | ✅ | Mismo molde WooCommerce (corrección handoff: no requieren Playwright) |
| **CubanCargos** | **Next.js (SSR)** | HTML directo (catálogo en el HTML) + `__NEXT_DATA__` | ✅ catálogo / ⚠️ compra | `/triciclos` · el listado viene renderizado (PORTO BELLO, JINPEING, Furikazan, Nippon SE; estado AGOTADO; reseñas; 10% descuento) |
| **El Yerro** (elyerromenu.com) | Nuxt SPA | Playwright o reverse de XHR… **o descartar** | ⚠️ sin evidencia | 0 menciones de "triciclo" en el HTML servido → no viable observado para este mercado |
| **GAOS / CasasOasis / HogarEnCuba** (inmobiliario) | SPA | Playwright/JS (o reverse de API interna) | ⚠️ | SPAs; listados requieren esperar render |
| **Facebook (4+ grupos)** | Red social | **No scrapear**: Graph API (token + membresía) o captura manual con procedencia | 🔎 | `todotricicloselectricos` verificado por nombre; 3 IDs sin indexar |
| **Telegram (anuncios_cu, MotosBateriasElectricasCuba, cubaventas)** | Bot API / MTProto | Bot API oficial (solo con admin) o **Telethon** con sesión autorizada; si no, captura manual | 🔎 | No scrapear sin autorización |

**Regla de oro**: cada registro debe nacer con `metadatos_captura.metodo` y su `fechas.captura` — un dato
no observado hoy no debe "inventarse" mañana. Los métodos ✅ son BS4 puro; los 🔎 quedan fuera del pipeline
automático.

---

## 2. Descarga HTTP con cortesía (plantilla base)

```python
# captura_http.py
import hashlib, json, time, os
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
CACHE = "/tmp/opencode/cache_html"          # caché en disco (evita re-descargas)

def sesion():
    s = requests.Session()
    s.headers.update({"User-Agent": UA, "Accept-Language": "es,en;q=0.8"})
    retry = Retry(total=3, backoff_factor=2.0, status_forcelist=[429, 500, 502, 503, 504],
                  allowed_methods=["GET"])
    s.mount("https://", HTTPAdapter(max_retries=retry))
    return s

def descargar(url, usar_cache=True, espera=0.7, s=None):
    """Descarga URL con ritmo (1–2 req/s), caché y backoff ante 429/403."""
    key = hashlib.sha1(url.encode()).hexdigest()[:16]
    path = f"{CACHE}/{key}.html"
    if usar_cache and os.path.exists(path):
        return open(path, encoding="utf-8", errors="ignore").read()
    s = s or sesion()
    r = s.get(url, timeout=45)
    r.raise_for_status()
    time.sleep(espera)                       # cortesía: ritmo mínimo
    os.makedirs(CACHE, exist_ok=True)
    open(path, "w", encoding="utf-8").write(r.text)
    return r.text
```

---

## 3. WooCommerce (MultiServices, KikiHabana, CompraMásOnline, Apululu, Autocubana)

Tres vías complementarias; usar la **REST primero** (más limpia) y HTML como respaldo.

### 3.1 REST wp-json (estructurado, paginado)

```python
import requests, json, time

BASE = "https://multiservicesxpress.com"     # mismo patrón para kikihabana.com, compramasonline.com...

def productos_wc(s):
    """Itera todas las páginas de /product con sus atributos."""
    url = f"{BASE}/wp-json/wp/v2/product"
    page = 1
    while True:
        r = s.get(url, params={"per_page": 100, "page": page}, timeout=45)
        r.raise_for_status()
        items = r.json()
        if not items:
            break
        for it in items:
            meta = it.get("meta") or {}       # _regular_price / _sale_price / _sku ...
            yield {
                "id": it["id"], "slug": it["slug"],
                "titulo": it["name"], "descripcion": (it.get("description") or "")[:500],
                "precio_regular": meta.get("_regular_price"), "precio_oferta": meta.get("_sale_price"),
                "sku": meta.get("_sku"), "stock": meta.get("_stock_status"),  # instock/outofstock
                "url": it.get("link"),
            }
        total = r.headers.get("X-WP-TotalPages", "1")
        if page >= int(total):
            break
        page += 1
        time.sleep(0.7)
```

> Atributos extra (peso, dimensiones, colores) viven en `it["product_attributes"]` o en el endpoint
> `/wp-json/wp/v2/products/<id>` según el tema. Verificar el namespace real (`product` vs `products`).

### 3.2 HTML + BS4 (respaldo y atributos de la ficha)

```python
from bs4 import BeautifulSoup

def parsear_loop_woo(html):
    """Tarjetas de la tienda: título, precio (regular vs oferta), URL."""
    soup = BeautifulSoup(html, "html.parser")
    out = []
    for card in soup.select("ul.products li.product"):
        a = card.select_one("h2.woocommerce-loop-product__title a, a.woocommerce-LoopProduct-link")
        precios = card.select("span.woocommerce-Price-amount")
        p = [x.get_text(strip=True) for x in precios]          # ["3,500.00$", "3,200.00$"] si hay oferta
        out.append({
            "url": a["href"] if a else None,
            "titulo": a.get_text(strip=True) if a else None,
            "precios": p,                                      # 1 = normal, 2 = [regular, oferta]
        })
    return out

def parsear_ficha_woo(html):
    """Ficha: precio, obtención de SKU, tabla 'Información adicional' y descripción."""
    soup = BeautifulSoup(html, "html.parser")
    datos = {}
    m = soup.select_one("form.variations_form")                # selector de variantes (color, etc.)
    datos["con_variantes"] = bool(m)
    precio = None
    orig = soup.find(string=lambda t: t and "El precio original era" in t)
    actual = soup.find(string=lambda t: t and "El precio actual es" in t)
    if orig and actual:
        datos["es_oferta"] = True
        datos["monto_anterior"] = orig.parent.get_text(strip=True)
    for tr in soup.select("table.shop_attributes tr"):         # "Información adicional"
        th, td = tr.select("th"), tr.select("td")
        if th and td:
            datos[th[0].get_text(strip=True)] = td[0].get_text(strip=True)
    sku = soup.select_one(".sku")
    datos["sku"] = sku.get_text(strip=True) if sku else None   # suele ser "N/D"
    return datos
```

### 3.3 RSS por categoría (respaldo estructurado)

```python
import re, html as H

def parsear_rss_feed(xml):
    items = re.findall(r"<item>(.*?)</item>", xml, re.S)
    out = []
    for it in items:
        t = re.search(r"<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>", it, re.S)
        l = re.search(r"<link>(.*?)</link>", it, re.S)
        out.append({"titulo": H.unescape(t.group(1)) if t else None, "url": l.group(1).strip() if l else None})
    return out
```

---

## 4. Magento — Islagrande (EUR, SKU y "Out of stock")

```python
def parsear_magento(html):
    soup = BeautifulSoup(html, "html.parser")
    out = []
    for card in soup.select("li.item.product, .product-item"):
        t = card.select_one(".product-item-link, a.product")        # título+URL
        p = card.select_one(".price")                               # "€535.38"
        sku = card.select_one(".sku, [data-sku]")
        stock = card.select_one(".stock")                           # "Out of stock" o "In stock"
        out.append({
            "titulo": t.get_text(strip=True) if t else None,
            "url": t["href"] if t else None,
            "precio": p.get_text(strip=True) if p else None,
            "sku": sku.get("data-sku") if sku else (sku.get_text(strip=True) if sku else None),
            "stock": stock.get_text(strip=True) if stock else None,
        })
    return out
# Paginación: añadir ?p=2, ?p=3 al mismo category URL
```

---

## 5. Next.js SSR — CubanCargos (catálogo ya viene en el HTML)

```python
def extraer_next_json(html):
    """Si el HTML incluye <script id='__NEXT_DATA__'>, extrae el JSON con todo el estado."""
    m = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html, re.S)
    return json.loads(m.group(1)) if m else None
# Entonces: recorrer data.props.pageProps.productos... (estructura a confirmar en cada build)
# Respaldo: parsear con BS4 el HTML ya renderizado (títulos, precios, estado AGOTADO, reseñas)
```

El catálogo **no requiere Playwright**: el SSR entrega el listado en el HTML. La interacción de compra sí
es JS (queda fuera del alcance de captura de datos).

---

## 6. SPA (Nuxt/Vue — El Yerro, GAOS, CasasOasis, HogarEnCuba)

Solo cuando la ruta realmente contenga datos (El Yerro: **no** se observaron triciclos → descartar hasta
evidencia):

```python
from playwright.sync_api import sync_playwright

def capturar_spa(url, selector_espera, espera_ms=3500):
    """Abre la página, espera al selector de productos y devuelve el HTML final."""
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        pg = b.new_page(user_agent="Mozilla/5.0 ... Chrome/124")
        pg.goto(url, wait_until="networkidle", timeout=60000)
        pg.wait_for_selector(selector_espera, timeout=60000)       # ej: "ul.products li.product"
        pg.wait_for_timeout(espera_ms)                             # lazy-load
        html = pg.content()
        b.close()
    return html
```

Alternativa más ligera: **reverse de XHR** (DevTools → Network): replicar las llamadas JSON internas
con `requests` (más rápido y sin navegador). Solo si las respuestas no requieren tokens efímeros.

---

## 7. Revolico — clasificados (HTML) + fallback por snippets

### 7.1 Captura normal (entorno sin bloqueo)

```python
def listar_revolico(s, categorias, max_paginas=5):
    """categorias: [("vehiculos","vehiculos-motos-electricas-y-triciclos"), ...]"""
    for cat, sub in categorias:
        for page in range(1, max_paginas + 1):
            html = descargar(f"https://www.revolico.com/search?category={cat}&subcategory={sub}&page={page}", s=s)
            soup = BeautifulSoup(html, "html.parser")
            for art in soup.select("article, .listing, div[class*='listing']"):
                a = art.select_one("a[href*='/item/']")
                if not a:
                    continue
                yield {
                    "url": a["href"], "id": re.search(r"-(\d+)$", a["href"]).group(1),
                    "titulo": a.get_text(" ", strip=True),
                    "precio": extraer_precio(art),                  # ver sección 9
                    "ubicacion": extraer_ubicacion(art),
                    "fecha": extraer_fecha(art),
                }
            time.sleep(1.0)
```

### 7.2 Fallback: snippets del buscador (cuando hay 403/transport)

```python
def snippets_ddg(query, n=8):
    """https://html.duckduckgo.com/html/?q=... → títulos, URLs y texto de cada resultado."""
    r = requests.get("https://html.duckduckgo.com/html/",
                     params={"q": query}, headers={"User-Agent": UA}, timeout=30)
    soup = BeautifulSoup(r.text, "html.parser")
    out = []
    for res in soup.select(".result")[:n]:
        a = res.select_one(".result__a")
        t = res.select_one(".result__snippet")
        out.append({"titulo": a.get_text(strip=True) if a else None,
                    "url": a["href"] if a else None,
                    "snippet": t.get_text(" ", strip=True) if t else None})
    return out
# Ejemplo: snippets_ddg('site:revolico.com triciclo') → precios/specs del título (estado ✅/⚠️ por snippet)
```

Los snippets **no sustituyen el corpus completo**: solo sirven de verificación muestral y de redescubrimiento
de URLs `/item/<slug>-<id>` para luego capturarlas directo cuando el acceso lo permita.

---

## 8. Canal 🔎 (Facebook / Telegram): fuera del pipeline automático

- **Facebook**: sin scrapeo de páginas (viola ToS y requiere login). Solo (a) **Graph API** con token de
  la cuenta y membresía en el grupo (`/v21.0/<group_id>/feed`), obtenido con flujo OAuth del usuario, o
  (b) **captura manual documentada** (copiar anuncio, fecha, procedencia) — mantener el campo `fuente`
  y `metadatos_captura.metodo: "manual"`.
- **Telegram**: con autorización del canal, `pip install telethon` y sesión del usuario:

```python
from telethon import TelegramClient, events
client = TelegramClient("sesion", api_id, api_hash)   # credenciales del usuario
async def dump(canal, limite=200):
    await client.start()
    async for msg in client.iter_messages(canal, limit=limite):
        print(msg.date, msg.message[:200])            # texto plano; fotos → msg.media
# Sin autorización: captura manual. Nunca intentar bypass.
```

---

## 9. Normalización hacia los esquemas (ej: mercado_triciclos_cuba_v1)

```python
import re

def extraer_precio(nodo):
    t = nodo.get_text(" ", strip=True)
    m = re.search(r"([\d][\d.,]*)\s*\$", t)           # "3,200.00$" / "$3,200"
    return float(m.group(1).replace(",", "")) if m else None

def parsear_oferta(texto):
    """KikiHabana: 'El precio original era: 3,500.00$. El precio actual es: 3,200.00$.'"""
    m = re.search(r"original era:\s*([\d.,]+).*?actual es:\s*([\d.,]+)", texto)
    if not m:
        return None
    anterior, actual = (float(x.replace(",", "")) for x in m.groups())
    return {"monto": actual, "monto_anterior": anterior,
            "es_oferta": True, "descuento_porciento": round((1 - actual / anterior) * 100)}

def specs_desde_titulo(t):
    """Revolico: 'Motor de 2000w ☑️ 6 Bateria de gel ☑️ 72v por 58ah ☑️ Caja Votol EM-100 ☑️ Autonomía de 100 a 120km'"""
    def g(pat): 
        m = re.search(pat, t, re.I); return float(m.group(1)) if m else None
    return {
        "motor_potencia_w": g(r"motor de (\d+)\s*w"),
        "bateria_voltaje_v": g(r"(\d+)\s*v\s*por\s*(\d+)\s*ah") and
                             (lambda m: m)(re.search(r"(\d+)\s*v\s*por", t, re.I)).group(1) if re.search(r"(\d+)\s*v\s*por", t, re.I) else None,
        "bateria_capacidad_ah": g(r"(\d+)\s*ah"),
        "autonomia_km": g(r"autonom[ií]a[^\d]*(\d+)"),
        "velocidad_max_kmh": g(r"velocidad m[aá]x[^\d]*(\d+)"),
        "carga_max_kg": g(r"carga m[aá]x[^\d]*(\d+)"),
    }

def construir_registro(raw, esquema="mercado_triciclos_cuba_v1"):
    """Une fuente + url + campos parseados + metadatos en un dict alineado al JSON del esquema."""
    return {
        "schema": esquema,
        "fuente": raw["fuente"], "url_anuncio": raw["url"], "id_externo": raw["id"],
        "titulo": raw["titulo"], "descripcion": raw.get("desc"),
        "fechas": {"publicacion": raw.get("fecha"), "captura": raw["captura"]},
        "precio": parsear_oferta(raw.get("texto")) or {"monto": extraer_precio(raw), "moneda": "USD",
                                                       "es_oferta": False, "monto_anterior": None,
                                                       "descuento_porciento": None},
        "triciclo": {"uso": raw.get("uso"), "propulsion": raw.get("propulsion"),
                     "marca": raw.get("marca"), "modelo": raw.get("modelo"), "anio": raw.get("anio"),
                     "especificaciones": specs_desde_titulo(raw.get("titulo", ""))},
        "legalizacion": {"papeles": raw.get("papeles"), "nota": raw.get("nota_papeles")},
        "canal_comercial": {"tipo": raw["tipo_canal"], "envio_incluido": raw.get("envio"),
                            "origen_vendedor": raw.get("origen")},
        "ubicacion_anuncio": {"provincia": raw.get("provincia"), "municipio": raw.get("municipio")},
        "anunciante": {"tipo": raw.get("tipo_anunciante"), "nombre": raw.get("vendedor")},
        "metadatos_captura": {"metodo": raw["metodo"],
                              "observaciones": raw.get("notas_captura")},
    }
```

### Almacenamiento JSONL (+ dedup)

```python
def guardar_registro(reg, archivo="capturas.jsonl"):
    """Línea por registro; la deduplicación usa schema+url_anuncio+captura."""
    clave = f"{reg['schema']}|{reg['url_anuncio']}|{reg['fechas']['captura']}"
    with open(archivo, "a", encoding="utf-8") as f:
        f.write(json.dumps({"_clave": clave, **reg}, ensure_ascii=False) + "\n")
```

---

## 10. Buenas prácticas y advertencias (mantener)

1. **Cortesía**: 1–2 peticiones/segundo por dominio, backoff exponencial ante 429/403/5xx, caché en disco.
2. **Base legal**: respetar `robots.txt` y ToS; **Facebook y Telegram no se scrapean** (API o manual).
3. **Procedencia siempre**: `metodo` (requests_bs4 / wp_json_api / snippets_buscador / xhr_js / manual),
   `captura` ISO y, si hubo bloqueo, anotarlo en `observaciones`.
4. **No inventar**: todo campo nulo si no se observó; fechas de publicación solo si la fuente las expone.
5. **Paginación**: respetar `X-WP-TotalPages` (Woo), `?p=N` (Magento), `page=N` (Revolico), `limit` (API).
6. **Monedas por mercado**: inmobiliario/autos multi-moneda (campo `moneda` obligatorio); movilidad/triciclos
   todo USD (salvo Islagrande EUR — verificar campo `moneda` igualmente).
7. **Claves de cruce**: inmuebles `municipio+protocolo+titulo`; autos/movilidad/triciclos
   `marca+modelo(+motor/batería)` — permiten unir la misma oferta entre tienda y Revolico.
8. **Recordar el bloqueo vigente de Revolico desde este entorno**: usar fallback de snippets (sección 7.2)
   y retomar el fetch completo desde un entorno sin bloqueo.

---

## 11. Orden de implementación sugerido

1. **Piloto de 1 fuente**: KikiHabana o CompraMásOnline (WooCommerce, ✅, ficha rica) → 12–11 registros
   completos con `construir_registro()`.
2. **Ampliar a catálogos**: MultiServicesXpress (wp-json), Islagrande (Magento), CubanCargos (SSR).
3. **Revolico** cuando el entorno permita: 2–3 páginas de `vehiculos-motos-electricas-y-triciclos`.
4. **Normalización cruzada y análisis**: precios por marca/modelo, ofertas, extensores, legalización.
5. **Capa 🔎 manual** (FB/Telegram) aparte, con procedencia documentada.