#!/usr/bin/env python3
"""
Genera `Data/modelos_canonicos.json`: la tabla de nombres de modelo CURADA.

La tabla se construye a partir de `Data/clean_data/` (los nombres que el
usuario revisó a mano el 2026-10-19) más las separaciones de variante que
decidió ese mismo día, y se versiona en el repo: es la fuente de verdad de
la identidad de cada producto.

Reglas aplicadas al construir la tabla:
  - clave = URL del producto (estable entre corridas; un producto = una URL);
  - `por_url`: {modelo, marca} canónicos;
  - `excluidos`: URL + motivo (productos que el usuario decidió dejar fuera);
  - `variantes`: separaciones explícitas de productos que comparten nombre
    pero NO son el mismo (specs distintas) -> se cuentan por separado.

Uso:
    python3 codes/crear_canonicos.py            # escribe Data/modelos_canonicos.json
    python3 codes/crear_canonicos.py --check     # solo muestra el resumen
"""

import json
import subprocess
import sys
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "Data"
CLEAN_DIR = DATA_DIR / "clean_data"
OUT_PATH = DATA_DIR / "modelos_canonicos.json"

# ---- Separaciones de variante decididas por el usuario (2026-10-19) ----
# "si no son exactamente iguales, déjalos separados y cuéntalos por separado"
VARIANTES = {
    # OIM: el "disponible" ($3.400, 1200 W) y el "de pasaje" ($3.500) son
    # productos distintos que comparten marca y nombre.
    "https://elyerromenu.com/b/cuba-sobre-ruedas/product/triciclos-oim-de-pasaje":
        ("OIM PASAJE", "OIM"),
    # RALLY de KikiHabana: uno es de pasajeros (500 kg) y otro de carga (2.000 kg).
    "https://kikihabana.com/producto/triciclos-electricos-para-cuba-2/":
        ("RALLY PASAJEROS", "RALLY"),
    "https://kikihabana.com/producto/triciclos-para-cuba/":
        ("RALLY CARGA", "RALLY"),
    # MZ Products: tres "E-CARGO" distintos solo por batería (80/60/100 Ah).
    "https://www.mzproducts.com/producto/triciclo-electrico-72v-80ah-mz-products-cargo/":
        ("E-CARGO 80AH MZ PRODUCTS", "MZ PRODUCTS"),
    "https://www.mzproducts.com/producto/triciclo-electrico-72v-60-ah-2500w-mz-products/":
        ("E-CARGO 60AH MZ PRODUCTS", "MZ PRODUCTS"),
    "https://www.mzproducts.com/producto/triciclo-electrico-100a-mz-products-cargo/":
        ("E-CARGO 100AH MZ PRODUCTS", "MZ PRODUCTS"),
    # VEDCA C800B: el "fotovoltaico" es una variante con panel (precio propio).
    "https://islagrande.com/triciclo-electrico-carga-pasajeros-c800b-fotovoltaico-lifepo4-60v-90ah-habana.html":
        ("VEDCA C800B FOTOVOLTAICO", "VEDCA"),
}

# ---- Productos que el usuario decidió dejar fuera (2026-10-19) ----
# "TRICICLOS HIBRIDOS MEJOR PRECIO": nombre 100% publicitario, sin modelo
# identificable; era una de las 3 ofertas con precio contradictorio declaradas
# como limitación. Se excluye, pero queda constancia del motivo para que una
# corrida futura no lo resucite en silencio.
EXCLUIDOS = {
    "https://elyerromenu.com/b/cuba-sobre-ruedas/product/triciclos-hibridos-el-mejor-precio-de":
        "Nombre 100% publicitario ('MEJOR PRECIO'), sin modelo identificable; "
        "excluido por decisión del usuario (2026-10-19).",
}

# ---- Ficheros que el usuario NO curó: se conservan tal cual y se avisa ----
SIN_CURAR = {"acubaenvioscargo.jsonl"}

# ---- Pares (curado -> crudo) para poder desambiguar por el nombre original ----
# El fichero crudo conserva el nombre tal como venía de la web; sirve para
# distinguir productos que comparten URL (mrcuba: una sola página de Wix).
ORIGEN_CRUDE = {
    "anuncios_triciclos.jsonl": "raw_data/anuncios_triciclos.jsonl",
    "kikihabana.jsonl": "empresas/kikihabana.jsonl",
    "mzproducts.jsonl": "empresas/mzproducts.jsonl",
    "mrcuba.jsonl": "empresas/mrcuba.jsonl",
    "acubaenvioscargo.jsonl": "empresas/acubaenvioscargo.jsonl",
}


def _nombres_crudos(rel):
    """Nombres originales de los productos de un fichero crudo.

    Se lee primero la versión del último commit (el fichero crudo se
    normaliza al migrar, así que los nombres originales ya no están en el
    archivo de trabajo) y, si no está en git, el fichero actual.
    """
    ruta = DATA_DIR / rel
    try:
        # Ruta RELATIVA a la raíz del repo (git la necesita así).
        rel_repo = ruta.relative_to(DATA_DIR.parent).as_posix()
        out = subprocess.run(["git", "show", f"HEAD:{rel_repo}"],
                             capture_output=True, text=True, check=True).stdout
        lineas = out.strip().split("\n")
    except Exception:
        if not ruta.exists():
            return {}
        lineas = [l for l in open(ruta, encoding="utf-8").read().split("\n") if l.strip()]
    res = {}
    for l in lineas:
        l = l.strip()
        if not l:
            continue
        try:
            rr = json.loads(l)
        except json.JSONDecodeError:
            continue
        nombre = (rr.get("modelo") or "").strip().upper()
        res.setdefault(rr.get("url"), []).append(nombre)
    return res


def main():
    check = "--check" in sys.argv
    por_url = {}
    pendientes = {}

    for f in sorted(CLEAN_DIR.glob("*.jsonl")):
        # Nombre original del mismo producto (fichero crudo): permite
        # desambiguar cuando una URL sirve a varios productos.
        crudo_por_url = {}
        rel = ORIGEN_CRUDE.get(f.name)
        if rel:
            crudo_por_url = _nombres_crudos(rel)

        # ¿Alguna URL de este fichero sirve a más de un producto?
        conteo = {}
        for line in open(f, encoding="utf-8"):
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            u = r.get("url")
            if u and u not in EXCLUIDOS:
                conteo[u] = conteo.get(u, 0) + 1

        vistos = {}
        for line in open(f, encoding="utf-8"):
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            url = r.get("url")
            if not url or url in EXCLUIDOS:
                continue
            if url in VARIANTES:
                modelo, marca = VARIANTES[url]
                por_url[url] = {"modelo": modelo, "marca": marca, "origen": "variante"}
                continue

            if conteo.get(url, 0) > 1:
                # Varios productos con la misma URL: se guardan como opciones y
                # se elige la que casa con el nombre original; si el nombre ya
                # está normalizado, se usa la propulsión como discriminante
                # (mrcuba: la página única de Wix sirve dos productos).
                idx = vistos.get(url, 0)
                vistos[url] = idx + 1
                crudos = crudo_por_url.get(url, [])
                match = crudos[idx] if idx < len(crudos) else (r.get("modelo") or "")
                por_url.setdefault(url, {"opciones": []})["opciones"].append({
                    "match": match,
                    "propulsion": (r.get("propulsion") or "").lower(),
                    "modelo": r.get("modelo"),
                    "marca": r.get("marca"),
                    "origen": "curado",
                })
                continue

            por_url[url] = {
                "modelo": r.get("modelo"),
                "marca": r.get("marca"),
                "origen": "curado",
            }
            if f.name in SIN_CURAR:
                pendientes[url] = f.name

    # Los productos de Facebook comparten la misma URL base con variantes
    # distintas (permisos); la clave por URL no los distingue, así que para
    # Facebook se indexa además por (marca, modelo) en la tabla de alias del
    # análisis. Aquí solo se registran las URLs canónicas de las fichas
    # scrapeadas (una URL = un producto).
    data = {
        "version": "2026-10-19",
        "nota": (
            "Tabla curada de identidad de producto (clave: URL). La usan "
            "codes/norm_modelo.py y los scrapers, de modo que raw_data nace "
            "con los nombres ya normalizados. Editar aquí, no a mano en los "
            "JSONL: la siguiente pasada del scraper sobrescribe lo editado "
            "a mano."
        ),
        "por_url": por_url,
        "excluidos": EXCLUIDOS,
        "sin_curar": pendientes,
    }

    if not check:
        with open(OUT_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print(f"-> Escrito: {OUT_PATH}")

    n_mod = sum(1 for v in por_url.values() if v.get("modelo"))
    n_sin = sum(1 for v in por_url.values() if not v.get("modelo"))
    print(f"Productos en la tabla: {len(por_url)} "
          f"(con nombre de modelo: {n_mod}, sin nombre: {n_sin})")
    print(f"Excluidos: {len(EXCLUIDOS)} | variantes separadas: {len(VARIANTES)}")
    print(f"Sin curar por el usuario: {len(pendientes)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
