from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
EN = ROOT / "en/capital-relationships/index.html"
ES = ROOT / "es/relaciones-de-capital/index.html"
DATA = ROOT / "assets/data/sun-rock-capital-relationships-v1.json"
ROUTE = ROOT / "assets/capital-relationships-route-20260916.js"
SITE = ROOT / "assets/site.js"
HOME = ROOT / "assets/home-future-institutional-20260916.js"
SITEMAP = ROOT / "sitemap-sun-rock-institutional-20260916.xml"

errors = []

def need(path, needle, label=None, case_sensitive=True):
    text = path.read_text(encoding="utf-8")
    haystack = text if case_sensitive else text.lower()
    target = needle if case_sensitive else needle.lower()
    if target not in haystack:
        errors.append(f"{path.relative_to(ROOT)} missing {label or needle!r}")

required = [EN, ES, DATA, ROUTE, SITE, HOME, SITEMAP]
for p in required:
    if not p.exists():
        errors.append(f"missing required file: {p.relative_to(ROOT)}")

if not errors:
    need(EN, "Aweswell Limited")
    need(ES, "Aweswell Limited")
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

    data = json.loads(DATA.read_text(encoding="utf-8"))
    if data.get("status") != "PUBLIC_SAFE_GATEWAY_NOT_OFFER_NOT_COMMITMENT":
        errors.append("capital relationship data status is not fail-closed")
    if data.get("sponsor") != "Aweswell Limited":
        errors.append("Sponsor identity lock failed")

    combined = EN.read_text(encoding="utf-8").lower() + "\n" + ES.read_text(encoding="utf-8").lower()
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
