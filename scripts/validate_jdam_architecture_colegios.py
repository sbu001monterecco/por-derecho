from pathlib import Path
import json
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]

checks = {
    "es/arquitectura-nodo-documental-jdam/index.html": [
        "26/008230", "26/008474", "26/008476", "22/000036/7800",
        "e4bd916e483d4a9a8ef742fda7c039de", "DP 1901/2026",
        "artículo 262 LECrim", "mHn9IJU0qI4"
    ],
    "en/architecture-documentary-node-jdam/index.html": [
        "26/008230", "22/000036/7800", "DP 1901/2026",
        "Article 262 LECrim", "mHn9IJU0qI4"
    ],
    "assets/jdam-architecture-colegios-20260820.js": [
        "jdam-architecture-gateway", "20 August 2026", "20 agosto 2026"
    ],
    "assets/site.js": [
        "jdam-architecture-colegios-20260820.js", "palacete-visuals-20260820.js"
    ],
    "robots.txt": ["sitemap-jdam-architecture.xml"],
    "README.md": ["arquitectura-nodo-documental-jdam", "architecture-documentary-node-jdam"],
    "INSTITUTIONAL_ACTIONS_ARCHITECTS_COALZ_COAGC_20AUG2026.md": [
        "26/008476", "Article 262 LECrim"
    ],
}

for rel, needles in checks.items():
    text = (ROOT / rel).read_text(encoding="utf-8")
    for needle in needles:
        assert needle in text, f"{needle!r} missing from {rel}"

with (ROOT / "assets/data/jdam-architecture-documentary-node-v1.json").open(encoding="utf-8") as handle:
    json.load(handle)

for rel in ["sitemap-jdam-architecture.xml", "es/actualizaciones/feed.xml", "en/updates/feed.xml"]:
    ET.parse(ROOT / rel)

for rel in ["assets/jdam-pwc-conocimiento-2016-ES.svg", "assets/jdam-san-telmo-ricpe-sun-park-ES.svg"]:
    text = (ROOT / rel).read_text(encoding="utf-8")
    assert "<svg" in text and "No " in text

print("JDAM architecture / Colleges validation passed")
