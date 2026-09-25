from pathlib import Path
import json
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]

checks = {
    "es/fiscalia-tenerife-eg95-2026/index.html": [
        "Expediente Gubernativo 95/2026",
        "archivo procedimental",
        "no prueba mala fe ni invalidez jurídica",
        "No acredita incorporación judicial",
        "DIP 20/2026",
        "hreflang=\"en\"",
    ],
    "en/fiscalia-tenerife-eg95-2026/index.html": [
        "Administrative File 95/2026",
        "procedural closure",
        "does not by itself prove bad faith or legal invalidity",
        "No proof of judicial incorporation",
        "DIP 20/2026",
        "hreflang=\"es\"",
    ],
    "assets/fiscalia-eg95-propagation-20260823.js": [
        "data-eg95-dp748-update",
        "data-eg95-institutional-record",
        "data-eg95-update",
        "fiscalia-tenerife-eg95-2026",
        "does not expressly reject",
        "no rechaza expresamente",
    ],
    "assets/site.js": [
        "site-pre-treasury-154-hq-20260828.js?v=20260828a",
        "data-pre-treasury-154-site-loader",
    ],
    "assets/site-pre-treasury-154-hq-20260828.js": [
        "site-pre-intervencion-highlight-20260820.js",
        "jdam-architecture-colegios-20260820.js",
        "playa-blanca-concept-home-20260820.js",
    ],
    "assets/site-pre-intervencion-highlight-20260820.js": [
        "site-pre-intervencion-highlight-before-eg95-20260823.js",
        "fiscalia-eg95-propagation-20260823.js",
    ],
    "archive/FISCALIA_TENERIFE_EG95_RETRIEVAL_GATE_23AUG2026.md": [
        "EG 95/2026 is not DP 748/2026",
        "did not expressly reject",
        "Judicial incorporation",
    ],
    "archive/CORRECTION_REGISTER_FISCALIA_TENERIFE_EG95_APPEND_23AUG2026.md": [
        "CR-EG95-01",
        "Superseded",
        "Not established",
    ],
    "archive/MISSING_EVIDENCE_REGISTER_FISCALIA_TENERIFE_EG95_APPEND_23AUG2026.md": [
        "ME-EG95-01",
        "ME-EG95-07",
        "Absence from the current source set",
    ],
    "archive/public_office_communications/fiscalia_tenerife/2026-08-21_EG95/2026-08-21__FISCALIA_TENERIFE__OUTGOING_EMAIL__CONTROLLED_TEXT.md": [
        "preservados",
        "asociados",
        "ETJ 163/2020",
        "Cambiario 1048/2019",
        "D. Carlos Saavedra",
    ],
    "archive/public_office_communications/fiscalia_tenerife/2026-08-21_EG95/2026-08-21__FISCALIA_TENERIFE__EG_95_2026__CONTROLLED_TRANSCRIPTION_AND_FULL_ENGLISH_TRANSLATION.md": [
        "EXPEDIENTE GUBERNATIVO",
        "ADMINISTRATIVE/GOVERNANCE FILE",
        "opened under numbers 7, 12 and 20/2026",
    ],
    "robots.txt": ["sitemap-fiscalia-tenerife.xml"],
}

for rel, needles in checks.items():
    path = ROOT / rel
    assert path.is_file(), f"missing {rel}"
    text = path.read_text(encoding="utf-8")
    for needle in needles:
        assert needle in text, f"{needle!r} missing from {rel}"

with (ROOT / "assets/data/fiscalia-tenerife-eg95-20260823.json").open(encoding="utf-8") as handle:
    state = json.load(handle)
assert state["status"] == "procedural-archive-no-express-merits-determination"
assert state["routes"]["es"].endswith("/fiscalia-tenerife-eg95-2026/")
assert state["routes"]["en"].endswith("/fiscalia-tenerife-eg95-2026/")
assert any("incorporated" in item for item in state["not_proved"])

ET.parse(ROOT / "sitemap-fiscalia-tenerife.xml")

sitemap = (ROOT / "sitemap-fiscalia-tenerife.xml").read_text(encoding="utf-8")
for route in [
    "/es/fiscalia-tenerife-eg95-2026/",
    "/en/fiscalia-tenerife-eg95-2026/",
    "/es/fiscalia-tenerife-dp748/",
]:
    assert route in sitemap

print("Fiscalía Tenerife EG 95/2026 validation passed")
