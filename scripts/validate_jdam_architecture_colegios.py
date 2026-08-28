from pathlib import Path
import json
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]

checks = {
    "es/arquitectura-nodo-documental-jdam/index.html": [
        "26/008230", "26/008474", "26/008476", "22/000036/7800",
        "e4bd916e483d4a9a8ef742fda7c039de", "DP 1901/2026",
        "artículo 262 LECrim", "mHn9IJU0qI4", "No se declara delito"
    ],
    "en/architecture-documentary-node-jdam/index.html": [
        "26/008230", "26/008474", "26/008476", "22/000036/7800",
        "e4bd916e483d4a9a8ef742fda7c039de", "DP 1901/2026",
        "Article 262 LECrim", "mHn9IJU0qI4", "No crime"
    ],
    "assets/jdam-architecture-colegios-20260820.js": [
        "jdam-architecture-gateway", "20 August 2026", "20 agosto 2026",
        "criminal-engineering", "public-authority", "ricpe-idoneidad",
        "jdamInstitutionalParity", "26/008474", "26/008476",
        "datos aportados «no son coincidentes»", "four-channel redistribution",
        "Junta del COALZ", "Article 262 LECrim only if the threshold is met",
        "Registration, receipt, internal transfer or dispatch does not prove"
    ],
    "assets/site.js": [
        "site-pre-treasury-154-hq-20260828.js?v=20260828a",
        "data-pre-treasury-154-site-loader",
    ],
    "assets/site-pre-intervencion-highlight-before-eg95-20260823.js": [
        "jdam-architecture-colegios-20260820.js",
        "playa-blanca-concept-home-20260820.js",
        "palacete-san-bernardo-historica-marco.webp"
    ],
    "robots.txt": ["sitemap-jdam-architecture.xml"],
    "INSTITUTIONAL_ACTIONS_ARCHITECTS_COALZ_COAGC_20AUG2026.md": [
        "26/008476", "Article 262 LECrim", "four functional COAGC channels"
    ],
    "JDAM_ARCHITECTURE_DOCUMENTARY_NODE_MASTER_RECORD_20AUG2026.md": [
        "documentary conversion node", "Silence is not an admission"
    ],
    "es/actualizaciones/feed.xml": [
        "arquitectura-nodo-documental-jdam", "COALZ–COAGC"
    ],
    "en/updates/feed.xml": [
        "architecture-documentary-node-jdam", "COALZ–COAGC"
    ],
}

for rel, needles in checks.items():
    text = (ROOT / rel).read_text(encoding="utf-8")
    for needle in needles:
        assert needle in text, f"{needle!r} missing from {rel}"

with (ROOT / "assets/data/jdam-architecture-documentary-node-v1.json").open(encoding="utf-8") as handle:
    ledger = json.load(handle)
assert ledger["visado"]["reference"] == "22/000036/7800"
assert ledger["public_boundary"]["not_a_finding"] is True
assert ledger["right_of_reply"] is True

for rel in ["sitemap-jdam-architecture.xml", "es/actualizaciones/feed.xml", "en/updates/feed.xml"]:
    ET.parse(ROOT / rel)

for rel in ["assets/jdam-pwc-conocimiento-2016-ES.svg", "assets/jdam-san-telmo-ricpe-sun-park-ES.svg"]:
    text = (ROOT / rel).read_text(encoding="utf-8")
    assert "<svg" in text and "No " in text

for rel in [
    "es/arquitectura-nodo-documental-jdam/index.html",
    "en/architecture-documentary-node-jdam/index.html",
]:
    text = (ROOT / rel).read_text(encoding="utf-8")
    assert "criminal liability is established" not in text.lower()

print("JDAM architecture / Colleges validation passed")
