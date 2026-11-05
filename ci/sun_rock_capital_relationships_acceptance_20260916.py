from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
EN = ROOT / "en/capital-relationships/index.html"
ES = ROOT / "es/relaciones-de-capital/index.html"
IC_EN = ROOT / "en/institutional-capital/index.html"
IC_ES = ROOT / "es/capital-institucional/index.html"
PROCESS = ROOT / "assets/data/sun-rock-capital-process-v1.json"
DATA = ROOT / "assets/data/sun-rock-capital-relationships-v1.json"
ROUTE = ROOT / "assets/capital-relationships-route-20260916.js"
SITE = ROOT / "assets/site.js"
HOME = ROOT / "assets/home-future-institutional-20260916.js"
SITEMAP = ROOT / "sitemap-sun-rock-institutional-20260916.xml"
HOME_EN = ROOT / "en/index.html"
HOME_ES = ROOT / "es/index.html"
FUTURE_EN = ROOT / "en/future/index.html"
FUTURE_ES = ROOT / "es/futuro/index.html"

errors = []

def need(path, needle, label=None, case_sensitive=True):
    text = path.read_text(encoding="utf-8")
    haystack = text if case_sensitive else text.lower()
    target = needle if case_sensitive else needle.lower()
    if target not in haystack:
        errors.append(f"{path.relative_to(ROOT)} missing {label or needle!r}")

required = [EN, ES, IC_EN, IC_ES, PROCESS, DATA, ROUTE, SITE, HOME, SITEMAP, HOME_EN, HOME_ES, FUTURE_EN, FUTURE_ES]
for p in required:
    if not p.exists():
        errors.append(f"missing required file: {p.relative_to(ROOT)}")

if not errors:
    need(EN, "AWESWELL LIMITED")
    need(ES, "AWESWELL LIMITED")
    need(EN, "A private capital conversation begins with fit, not terms.")
    need(ES, "Una conversación privada de capital empieza por el encaje, no por las condiciones.")
    need(EN, "No public route")
    need(ES, "Sin vía pública")
    need(EN, "No public coupon")
    need(ES, "Sin cupón")
    need(EN, "Seven gates before investment-specific material.", "private-process gate heading")
    need(EN, "Principal or intermediary", case_sensitive=False)
    need(ES, "principal o intermediario", case_sensitive=False)
    need(EN, "mailto:sbu001@monterecco.com?subject=PSR%20%E2%80%94%20Private%20capital%20relationship")
    need(ES, "mailto:sbu001@monterecco.com?subject=PSR%20%E2%80%94%20Relaci%C3%B3n%20privada%20de%20capital")
    need(ROUTE, "capital-relationships/")
    need(ROUTE, "relaciones-de-capital/")
    need(SITE, "loadCapitalRelationships")
    need(SITE, "capital-relationships-route-20260916.js")
    need(SITE, "/por-derecho/en/strategic-financial-relationship/")
    need(SITE, "/por-derecho/es/relacion-financiera-estrategica/")
    need(SITE, "/por-derecho/en/montana-roja/")
    need(SITE, "/por-derecho/es/montana-roja/")
    need(HOME, "CAPITAL RELATIONSHIPS")
    need(HOME, "RELACIONES DE CAPITAL")
    need(SITEMAP, "/en/capital-relationships/")
    need(SITEMAP, "/es/relaciones-de-capital/")
    need(SITEMAP, "/en/institutional-capital/")
    need(SITEMAP, "/es/capital-institucional/")
    need(EN, "../institutional-capital/")
    need(ES, "../capital-institucional/")
    need(IC_EN, "Capital built for progression, not publicity.")
    need(IC_ES, "Capital diseñado para avanzar, no para publicitar.")
    need(IC_EN, "From an email to an investable decision.")
    need(IC_ES, "De un email a una decisión invertible.")
    need(IC_EN, "Committed financing / definitive offer")
    need(IC_ES, "Financiación comprometida / oferta definitiva")


    # Investor landing-cluster visibility lock:
    # investor/capital pages stay public and search-engine discoverable, but ordinary
    # site navigation must not provide an inbound route. Entry is by exact URL,
    # search-engine result, or another page already inside the landing cluster.
    home_en = HOME_EN.read_text(encoding="utf-8")
    home_es = HOME_ES.read_text(encoding="utf-8")
    if 'href="future/"' not in home_en:
        errors.append("en/index.html missing standalone Future route")
    if 'href="futuro/"' not in home_es:
        errors.append("es/index.html missing standalone Futuro route")

    ordinary_pages = [
        ROOT / "en/index.html",
        ROOT / "en/future/index.html",
        ROOT / "en/about/index.html",
        ROOT / "en/open-letter-lanzarote/index.html",
        ROOT / "en/collaborate/index.html",
        ROOT / "es/index.html",
        ROOT / "es/futuro/index.html",
        ROOT / "es/sobre-nosotros/index.html",
        ROOT / "es/carta-abierta-lanzarote/index.html",
        ROOT / "es/colaborar/index.html",
    ]
    landing_href_fragments = [
        "institutional-capital/",
        "capital-relationships/",
        "platform-scale/",
        "montana-roja/",
        "private-note-programme-administration/",
        "capital-institucional/",
        "relaciones-de-capital/",
        "escala-plataforma/",
        "administracion-programa-notas-privadas/",
    ]
    for page in ordinary_pages:
        if not page.exists():
            errors.append(f"missing ordinary-page isolation target: {page.relative_to(ROOT)}")
            continue
        body = page.read_text(encoding="utf-8")
        for frag in landing_href_fragments:
            if f'href="../{frag}' in body or f'href="{frag}' in body or f'href="../../{frag}' in body:
                errors.append(f"{page.relative_to(ROOT)} links into investor landing cluster: {frag!r}")

    future_en = FUTURE_EN.read_text(encoding="utf-8")
    future_es = FUTURE_ES.read_text(encoding="utf-8")
    need(FUTURE_EN, "separate public landing pages for direct sharing and search-engine discovery", "landing-page boundary")
    need(FUTURE_ES, "landing pages públicas separadas para compartir por enlace directo y para descubrimiento mediante buscadores", "landing-page boundary")

    route_text = ROUTE.read_text(encoding="utf-8")
    for forbidden_runtime_route in (
        "/por-derecho/en/open-letter-lanzarote/",
        "/por-derecho/en/collaborate/",
        "/por-derecho/es/carta-abierta-lanzarote/",
        "/por-derecho/es/colaborar/",
    ):
        if forbidden_runtime_route in route_text.split("if (!supported.has(path)")[0]:
            errors.append(f"capital runtime injector exposes ordinary route: {forbidden_runtime_route}")

    process = json.loads(PROCESS.read_text(encoding="utf-8"))
    if process.get("public_status") != "INSTITUTIONAL_CONVERSATIONS_ACTIVE_NO_COMMITTED_FINANCING":
        errors.append("institutional capital process status is not fail-closed")
    if process.get("capital_lanes", {}).get("project_montana_roja", {}).get("committed_financing") is not False:
        errors.append("Montaña Roja committed-financing boundary failed")
    if process.get("capital_lanes", {}).get("project_montana_roja", {}).get("definitive_offer") is not False:
        errors.append("Montaña Roja definitive-offer boundary failed")

    data = json.loads(DATA.read_text(encoding="utf-8"))
    if data.get("status") != "PUBLIC_SAFE_GATEWAY_NOT_OFFER_NOT_COMMITMENT":
        errors.append("capital relationship data status is not fail-closed")
    if data.get("sponsor") != "Aweswell Limited":
        errors.append("Sponsor identity lock failed")

    combined = "\n".join([EN.read_text(encoding="utf-8").lower(), ES.read_text(encoding="utf-8").lower(), IC_EN.read_text(encoding="utf-8").lower(), IC_ES.read_text(encoding="utf-8").lower()])
    prohibited_cta_fragments = [
        ">invest now<",
        ">subscribe now<",
        ">reserve notes<",
        ">invertir ahora<",
        ">suscribirse ahora<",
        "minimum investment:",
        "inversión mínima:",
        "guaranteed return",
        "guaranteed yield",
        "rentabilidad garantizada",
    ]
    for term in prohibited_cta_fragments:
        if term in combined:
            errors.append(f"prohibited public-investment CTA/claim present: {term!r}")

if errors:
    print("CAPITAL RELATIONSHIPS ACCEPTANCE: FAIL")
    for err in errors:
        print("-", err)
    sys.exit(1)

print("CAPITAL RELATIONSHIPS ACCEPTANCE: PASS")
