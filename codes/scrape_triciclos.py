#!/usr/bin/env python3
"""
Scraper de triciclos para fuentes cubanas.
Guarda resultados en JSON Lines (.jsonl) con un objeto por anuncio.

Fuentes objetivo:
- Revolico (clasificados)
- KikiHabana, CubanCargos, CompraMás (tiendas WooCommerce)

Uso:
    python3 scrape_triciclos.py
"""

import json
import re
import time
from datetime import datetime
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


# ==================== CONFIG ====================
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "es-ES,es;q=0.9",
}

SOURCES = {
    "revolico": {
        "url": "https://www.revolico.com/search?category=vehiculos&subcategory=vehiculos-motos-electricas-y-triciclos",
        "parser": "parse_revolico",
        "list_selector": "div.listing-item, div.ad-item, article.ad",
        "detail_link_selector": "a[href*='/item/']",
    },
    "kikihabana": {
        "url": "https://kikihabana.com/categoria-producto/triciclos/",
        "parser": "parse_woocommerce",
        "list_selector": "li.product",
        "detail_link_selector": "a.woocommerce-LoopProduct-link",
    },
    "cubancargos": {
        "url": "https://cubancargos.com/categoria-producto/triciclos/",
        "parser": "parse_woocommerce",
        "list_selector": "li.product",
        "detail_link_selector": "a.woocommerce-LoopProduct-link",
    },
    "compramas": {
        "url": "https://compramasonline.com/categoria-producto/triciclos/",
        "parser": "parse_woocommerce",
        "list_selector": "li.product",
        "detail_link_selector": "a.woocommerce-LoopProduct-link",
    },
}

OUTPUT_FILE = "anuncios_triciclos.jsonl"
REQUEST_DELAY = 2  # segundos entre requests
TIMEOUT = 30


# ==================== UTILIDADES ====================
def clean_text(text: str) -> str:
    """Limpia texto: quita espacios extra, saltos de línea."""
    if not text:
        return ""
    return re.sub(r"\s+", " ", text.strip())


def extract_price_usd(text: str):
    """Extrae precio en USD del texto. Devuelve (precio_int, es_desde_bool)."""
    if not text:
        return None, False
    text = text.lower()
    desde = "desde" in text
    # Busca $1,234 o $1234 o 1,234 USD o 1234 USD
    m = re.search(r"[\$\s]([\d,.]+)\s*(?:usd|usd?)?", text)
    if m:
        val = m.group(1).replace(",", "").replace(".", "")
        try:
            return int(val), desde
        except ValueError:
            pass
    return None, desde


def extract_motor_w(text: str):
    """Extrae potencia del motor en watts."""
    if not text:
        return None
    m = re.search(r"(\d{3,5})\s*[wW]", text)
    if m:
        return int(m.group(1))
    # Busca "3000W", "3kw", "5kw"
    m = re.search(r"(\d+(?:\.\d+)?)\s*[kK][wW]", text)
    if m:
        return int(float(m.group(1)) * 1000)
    return None


def extract_battery(text: str):
    """Extrae voltaje y amperaje de batería. Devuelve (V, Ah) o (None, None)."""
    if not text:
        return None, None
    # 60V 20Ah, 60v20ah, 72V 30AH
    m = re.search(r"(\d{2,3})\s*[vV]\s*(\d{1,3})\s*[aA][hH]?", text)
    if m:
        return int(m.group(1)), int(m.group(2))
    return None, None


def normalize_modelo(text: str) -> str:
    """Normaliza nombres de modelos conocidos."""
    if not text:
        return "indeterminado"
    text = text.upper()
    known = ["IZUKI", "HUAIHAI", "RALLY", "MIGHONG", "ZONGSHEN", "LONCIN", "YAMAHA", "HONDA"]
    for k in known:
        if k in text:
            return k
    # Si no coincide, devuelve primeras 2 palabras
    words = text.split()
    return " ".join(words[:2]) if words else "indeterminado"


# ==================== PARSERS ====================
def parse_revolico(soup: BeautifulSoup, base_url: str):
    """Parsea listado de Revolico."""
    items = []
    # Revolico usa varios selectores, probamos los más comunes
    for sel in ["div.listing-item", "div.ad-item", "article.ad", "div.item"]:
        items = soup.select(sel)
        if items:
            break

    for item in items:
        # Enlace al detalle
        link = item.select_one("a[href*='/item/']")
        if not link:
            continue
        detail_url = urljoin(base_url, link.get("href", ""))

        # Título
        title_elem = item.select_one("h2, h3, .title, .ad-title")
        titulo = clean_text(title_elem.get_text()) if title_elem else ""

        # Precio
        price_elem = item.select_one(".price, .ad-price, [class*='price']")
        precio_txt = clean_text(price_elem.get_text()) if price_elem else ""
        precio, desde = extract_price_usd(precio_txt)

        # Construir registro base
        record = {
            "modelo": normalize_modelo(titulo),
            "marca": None,  # se llena en detalle
            "motor_w": extract_motor_w(titulo),
            "bateria_v": None,
            "bateria_ah": None,
            "autonomia_km": None,
            "carga_kg": None,
            "precio_usd": precio,
            "precio_desde": desde,
            "ano": None,
            "condicion": "usado" if "usado" in titulo.lower() else "nuevo",
            "legalizacion": None,
            "vendedor_tipo": "particular",
            "municipio_anuncio": None,
            "url": detail_url,
            "fecha_captura": datetime.now().isoformat(),
            "fuente": "revolico",
            "_titulo_raw": titulo,
        }

        # Intentar extraer municipio del snippet
        location_elem = item.select_one(".location, .ad-location, [class*='location']")
        if location_elem:
            record["municipio_anuncio"] = clean_text(location_elem.get_text())

        # Extraer marca del título si aparece
        for marca in ["IZUKI", "HUAIHAI", "RALLY", "MIGHONG", "ZONGSHEN", "LONCIN"]:
            if marca in titulo:
                record["marca"] = marca
                break

        yield record


def parse_woocommerce(soup: BeautifulSoup, base_url: str):
    """Parsea listado WooCommerce genérico (KikiHabana, CubanCargos, CompraMás)."""
    items = soup.select("li.product")
    for item in items:
        link = item.select_one("a.woocommerce-LoopProduct-link")
        if not link:
            continue
        detail_url = urljoin(base_url, link.get("href", ""))

        # Título
        title_elem = item.select_one("h2.woocommerce-loop-product__title, h3, .product-title")
        titulo = clean_text(title_elem.get_text()) if title_elem else ""

        # Precio
        price_elem = item.select_one(".price, .woocommerce-Price-amount")
        precio_txt = clean_text(price_elem.get_text()) if price_elem else ""
        precio, desde = extract_price_usd(precio_txt)

        record = {
            "modelo": normalize_modelo(titulo),
            "marca": None,
            "motor_w": extract_motor_w(titulo),
            "bateria_v": None,
            "bateria_ah": None,
            "autonomia_km": None,
            "carga_kg": None,
            "precio_usd": precio,
            "precio_desde": desde,
            "ano": None,
            "condicion": "nuevo",
            "legalizacion": None,
            "vendedor_tipo": "tienda",
            "municipio_anuncio": None,
            "url": detail_url,
            "fecha_captura": datetime.now().isoformat(),
            "fuente": urlparse(base_url).netloc.replace("www.", ""),
            "_titulo_raw": titulo,
        }

        for marca in ["IZUKI", "HUAIHAI", "RALLY", "MIGHONG", "ZONGSHEN", "LONCIN"]:
            if marca in titulo:
                record["marca"] = marca
                break

        yield record


def parse_detail_revolico(soup: BeautifulSoup, record: dict):
    """Enriquece registro con página de detalle de Revolico."""
    # Descripción completa
    desc_elem = soup.select_one(".description, .ad-description, .content, div[itemprop='description']")
    if desc_elem:
        full_text = clean_text(desc_elem.get_text())
        record["_descripcion_raw"] = full_text[:2000]

        # Buscar más datos en descripción
        if not record["motor_w"]:
            record["motor_w"] = extract_motor_w(full_text)
        vb, ah = extract_battery(full_text)
        if not record["bateria_v"]:
            record["bateria_v"], record["bateria_ah"] = vb, ah

        # Buscar autonomía
        m = re.search(r"(\d{2,3})\s*km", full_text, re.I)
        if m and not record["autonomia_km"]:
            record["autonomia_km"] = int(m.group(1))

        # Buscar carga
        m = re.search(r"(\d{2,4})\s*kg", full_text, re.I)
        if m and not record["carga_kg"]:
            record["carga_kg"] = int(m.group(1))

        # Legalización
        if "factura" in full_text.lower() or "legaliz" in full_text.lower():
            record["legalizacion"] = "mencionada en descripcion"

    # Municipio en detalle
    loc_elem = soup.select_one(".location, .ad-location, [itemprop='address']")
    if loc_elem and not record["municipio_anuncio"]:
        record["municipio_anuncio"] = clean_text(loc_elem.get_text())

    # Vendedor: si tiene teléfono o whatsapp visible, es particular/tienda
    if soup.select_one("[href*='whatsapp'], [href*='tel:']"):
        record["vendedor_tipo"] = "particular"


def parse_detail_woocommerce(soup: BeautifulSoup, record: dict):
    """Enriquece registro con página de producto WooCommerce."""
    # Descripción corta
    short_desc = soup.select_one(".woocommerce-product-details__short-description, .product-short-description")
    if short_desc:
        text = clean_text(short_desc.get_text())
        if not record["motor_w"]:
            record["motor_w"] = extract_motor_w(text)
        vb, ah = extract_battery(text)
        if not record["bateria_v"]:
            record["bateria_v"], record["bateria_ah"] = vb, ah

    # Descripción completa (tabs)
    full_desc = soup.select_one("#tab-description, .woocommerce-Tabs-panel--description, .product-description")
    if full_desc:
        text = clean_text(full_desc.get_text())
        if not record["motor_w"]:
            record["motor_w"] = extract_motor_w(text)
        vb, ah = extract_battery(text)
        if not record["bateria_v"]:
            record["bateria_v"], record["bateria_ah"] = vb, ah

        m = re.search(r"(\d{2,3})\s*km", text, re.I)
        if m and not record["autonomia_km"]:
            record["autonomia_km"] = int(m.group(1))
        m = re.search(r"(\d{2,4})\s*kg", text, re.I)
        if m and not record["carga_kg"]:
            record["carga_kg"] = int(m.group(1))

    # Atributos (tabla de specs)
    for row in soup.select(".woocommerce-product-attributes tr, .product_attributes tr"):
        th = row.select_one("th")
        td = row.select_one("td")
        if th and td:
            label = clean_text(th.get_text()).lower()
            val = clean_text(td.get_text())
            if "motor" in label and not record["motor_w"]:
                record["motor_w"] = extract_motor_w(val)
            if "bater" in label:
                vb, ah = extract_battery(val)
                if vb and not record["bateria_v"]:
                    record["bateria_v"], record["bateria_ah"] = vb, ah
            if "autonom" in label and not record["autonomia_km"]:
                m = re.search(r"(\d{2,3})", val)
                if m:
                    record["autonomia_km"] = int(m.group(1))
            if "carga" in label and not record["carga_kg"]:
                m = re.search(r"(\d{2,4})", val)
                if m:
                    record["carga_kg"] = int(m.group(1))

    # Precio real (puede variar del listado)
    price_elem = soup.select_one(".price .woocommerce-Price-amount, .product_price .amount")
    if price_elem:
        precio_txt = clean_text(price_elem.get_text())
        precio, desde = extract_price_usd(precio_txt)
        if precio:
            record["precio_usd"] = precio
            record["precio_desde"] = desde


# ==================== CORE ====================
def fetch(url: str) -> str:
    """GET con reintentos básicos."""
    for attempt in range(3):
        try:
            r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
            r.raise_for_status()
            return r.text
        except Exception as e:
            if attempt == 2:
                raise
            time.sleep(2 ** attempt)
    return ""


def scrape_source(key: str, config: dict):
    """Scrapea una fuente completa: listado + detalle de cada item."""
    print(f"\n=== {key.upper()} ===")
    print(f"Fetching listado: {config['url']}")

    try:
        html = fetch(config["url"])
    except Exception as e:
        print(f"  ERROR fetch listado: {e}")
        return []

    soup = BeautifulSoup(html, "html.parser")
    parser_func = globals()[config["parser"]]
    records = list(parser_func(soup, config["url"]))
    print(f"  Items en listado: {len(records)}")

    # Visitar detalle de cada uno (con delay)
    enriched = []
    for i, rec in enumerate(records):
        detail_url = rec["url"]
        print(f"  [{i+1}/{len(records)}] Detalle: {detail_url}")
        try:
            detail_html = fetch(detail_url)
            detail_soup = BeautifulSoup(detail_html, "html.parser")
            if key == "revolico":
                parse_detail_revolico(detail_soup, rec)
            else:
                parse_detail_woocommerce(detail_soup, rec)
        except Exception as e:
            print(f"    WARNING detalle falló: {e}")
        enriched.append(rec)
        time.sleep(REQUEST_DELAY)

    return enriched


def main():
    all_records = []

    for key, config in SOURCES.items():
        try:
            records = scrape_source(key, config)
            all_records.extend(records)
            print(f"  -> {len(records)} registros OK")
        except Exception as e:
            print(f"  ERROR fuente {key}: {e}")

    # Guardar JSONL
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for rec in all_records:
            # Quitar campos internos que empiezan con _
            out = {k: v for k, v in rec.items() if not k.startswith("_")}
            f.write(json.dumps(out, ensure_ascii=False) + "\n")

    print(f"\n=== TOTAL: {len(all_records)} anuncios guardados en {OUTPUT_FILE} ===")

    # Resumen rápido
    by_fuente = {}
    for r in all_records:
        by_fuente[r["fuente"]] = by_fuente.get(r["fuente"], 0) + 1
    for src, cnt in by_fuente.items():
        print(f"  {src}: {cnt}")


if __name__ == "__main__":
    main()
