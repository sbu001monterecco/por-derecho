#!/usr/bin/env python3
"""Deterministic continuity checks for AEAT state-transparency file 00001-00113069."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
FILES = {
    "es": ROOT / "es/transparencia-aeat-00001-00113069/index.html",
    "en": ROOT / "en/aeat-transparency-00001-00113069/index.html",
    "es_pink": ROOT / "es/pink-canary-aeat-audiencia-nacional/index.html",
    "en_pink": ROOT / "en/pink-canary-aeat-national-court/index.html",
    "es_ricpe": ROOT / "es/ricpe-idoneidad-series-f-g/index.html",
    "en_ricpe": ROOT / "en/ricpe-idoneidad-series-f-g/index.html",
    "es_updates": ROOT / "es/actualizaciones/index.html",
    "en_updates": ROOT / "en/updates/index.html",
    "actions": ROOT / "INSTITUTIONAL_ACTIONS.md",
    "handover": ROOT / "CURRENT_HANDOVER_OBLIGATION_AUDIT_21AUG2026.md",
    "audit": ROOT / "archive/intelligence/AEAT_00001_00113069_THREAD_HANDOVER_AND_DELETION_AUDIT_20260821.md",
    "sitemap": ROOT / "sitemap.xml",
}
required_everywhere = ("00001-00113069",)
timeline_common = ("RGE449073832025", "REGAGE25e00108884880")
timeline_by_language = {"es": ("20 ago", "21 ago"), "en": ("20 Aug", "21 Aug")}
separate = ("00001-00111718", "REGAGE26e00062869818", "REGAGE26e00062944142", "REGAGE26e00062943259", "REGAGE26e00072326601", "2220/2026")

errors = []
texts = {}
for name, path in FILES.items():
    if not path.is_file():
        errors.append(f"missing {path.relative_to(ROOT)}")
        continue
    texts[name] = path.read_text(encoding="utf-8")
    for marker in required_everywhere:
        if marker not in texts[name]:
            errors.append(f"{name}: missing {marker}")

for name in ("es", "en", "actions", "audit"):
    for marker in timeline_common:
        if marker not in texts.get(name, ""):
            errors.append(f"{name}: missing timeline marker {marker}")
for name, markers in timeline_by_language.items():
    for marker in markers:
        if marker not in texts.get(name, ""):
            errors.append(f"{name}: missing date marker {marker}")

for name in ("es", "en", "audit"):
    for marker in separate:
        if marker not in texts.get(name, ""):
            errors.append(f"{name}: missing separation marker {marker}")

for name, forbidden in {
    "es": ("traslado acredita recepción", "vinculación confirmada con rge"),
    "en": ("transfer proves competent receipt", "confirmed linkage to rge"),
}.items():
    for phrase in forbidden:
        if phrase in texts.get(name, "").lower():
            errors.append(f"{name}: forbidden overstatement {phrase!r}")

if errors:
    print("FAIL")
    print("\n".join(f"- {e}" for e in errors))
    sys.exit(1)
print("PASS: AEAT 00001-00113069 continuity, separation and linking checks")
