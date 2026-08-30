#!/usr/bin/env python3
"""Fail closed on the Arrecife 1103→1132→1010→804 caret/interlink repair."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
errors: list[str] = []


def require(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


with (ROOT / "archive/PROCEEDINGS_MASTER_REGISTER.csv").open(encoding="utf-8", newline="") as handle:
    rows = {row["Master_ID"]: row for row in csv.DictReader(handle)}

jud = rows.get("LZ-JUD-003", {})
app = rows.get("LZ-APP-004", {})
require(jud.get("Reference") == "DP 1132/2018", "LZ-JUD-003 DP reference drift")
require("1103/2018-00" in jud.get("Secondary_Reference", ""), "1103 origin missing from LZ-JUD-003")
require(jud.get("NIG") == "3500443220180003508", "LZ-JUD-003 NIG drift")
require(jud.get("Linked_Proceedings") == "LZ-APP-004", "DP→appeal link missing")
require("Rollo 1010/2018" in jud.get("Appeal_or_Review", ""), "DP appeal roll missing")
require(app.get("Reference") == "Rollo 1010/2018", "LZ-APP-004 roll drift")
require(app.get("Secondary_Reference") == "Auto 804/2018", "LZ-APP-004 order drift")
require(app.get("Parent_Master_ID") == "LZ-JUD-003", "appeal→DP parent link missing")
require(app.get("Linked_Proceedings") == "LZ-JUD-003", "appeal backlink missing")
require(app.get("NIG") == jud.get("NIG"), "shared NIG mismatch")
require("13 Nov 2018" in app.get("Latest_Known_Event", ""), "appellate date missing")
require("final/no further appeal" in app.get("Status", ""), "appellate finality boundary missing")

identity = json.loads((ROOT / "assets/data/matter-identity-registry-v1.proceedings.json").read_text(encoding="utf-8"))
family = next((item for item in identity["records"] if item.get("id") == "PD-SP-R-0023"), {})
aliases = set(family.get("aliases", []))
require(family.get("identity_resolution") == "CARET_CONFIRMED", "CAEPR family not caret-confirmed")
require(set(family.get("master_register_ids", [])) == {"LZ-JUD-003", "LZ-APP-004"}, "CAEPR master-ID family mismatch")
require(family.get("routes") == {"es": "/es/arrecife-1103-2018-cadena-procesal/", "en": "/en/arrecife-1103-2018-procedural-lineage/"}, "CAEPR dedicated caret routes drift")
for alias in ("Diligencias Indeterminadas 1103/2018-00", "DP 1132/2018", "Rollo 1010/2018", "Auto 804/2018"):
    require(alias in aliases, f"CAEPR alias missing: {alias}")
require("does not prove" in family.get("identity_boundary", ""), "CAEPR merits boundary missing")
identity_index = json.loads((ROOT / "assets/data/matter-identity-registry-v1.json").read_text(encoding="utf-8"))
require(identity_index.get("counts", {}).get("PROCEEDING") == 23, "CAEPR proceeding denominator not advanced to 23")
require(identity_index.get("counts", {}).get("total") == 231, "CAEPR total denominator not advanced to 231")
ops = json.loads((ROOT / "assets/data/matter-identity-operational-control-v1.json").read_text(encoding="utf-8"))
require(any(item.get("id") == "PD-SP-R-0023" for item in ops.get("proceeding_identity_corrections", [])), "CAEPR operational correction missing")

caret_pages = {
    "en": (ROOT / "en/arrecife-1103-2018-procedural-lineage/index.html").read_text(encoding="utf-8"),
    "es": (ROOT / "es/arrecife-1103-2018-cadena-procesal/index.html").read_text(encoding="utf-8"),
}
dossier_pages = {
    "en": (ROOT / "en/sun-park-takeover-7-june-2018/index.html").read_text(encoding="utf-8"),
    "es": (ROOT / "es/toma-control-sun-park-7-junio-2018/index.html").read_text(encoding="utf-8"),
}
required_page_tokens = (
    "1103/2018-00", "1132/2018", "1010/2018", "804/2018", "3500443220180003508",
    "PD-SP-R-0023", "LZ-JUD-003", "LZ-APP-004",
)
for lang, page in caret_pages.items():
    for token in required_page_tokens:
        require(token in page, f"{lang} public chain missing {token}")
    require(page.count('<sup class="caret">^</sup>') == 4, f"{lang} four-reference caret display missing")
    require("Matkator" in page and ("ONA" in page), f"{lang} relevance/context links missing")
require("master-proceedings" in caret_pages["en"] and "proceedings-map" in caret_pages["en"], "EN register/map links missing")
require("registro-maestro-procedimientos" in caret_pages["es"] and "mapa-procedimientos" in caret_pages["es"], "ES register/map links missing")
for lang, page in dossier_pages.items():
    for token in required_page_tokens:
        require(token in page, f"{lang} dossier explanation missing {token}")
    require("CAEPR-confirmed" in page or "confirmado por CAEPR" in page, f"{lang} dossier identity wording missing")

runtime = (ROOT / "assets/master-proceedings-publication-20260830.js").read_text(encoding="utf-8")
for token in ("detailRoutes", "LZ-JUD-003", "LZ-APP-004", "linkMasterReferences", "case-${esc(r.Master_ID)}"):
    require(token in runtime, f"Master Register backlink runtime missing {token}")

control = (ROOT / "archive/ARRECIFE_1103_1132_1010_804_CARET_INTERLINK_CONTROL_30AUG2026.md").read_text(encoding="utf-8")
for token in ("PRIMARY COPY REVIEWED", "CEXP", "Matkator", "Laura Patricia Acosta Matos", "PARTIAL"):
    require(token in control, f"continuity control missing {token}")
require("court-certified" in control.lower(), "continuity control missing court-certified gap")
require("CR-150" in (ROOT / "archive/CORRECTION_REGISTER.md").read_text(encoding="utf-8"), "canonical correction CR-150 missing")
require("ME-115" in (ROOT / "archive/MISSING_EVIDENCE_REGISTER.md").read_text(encoding="utf-8"), "canonical evidence gap ME-115 missing")

manifest = json.loads((ROOT / "publication-manifests/arrecife-1103-2018-caret-interlink-20260830.json").read_text(encoding="utf-8"))
require(manifest.get("publication_id") == "PD-SP-ARRECIFE-1103-2018-CARET-20260830-01", "publication manifest identity drift")

if errors:
    print("ARRECIFE 1103 CARET / INTERLINK AUDIT: FAIL")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print("ARRECIFE 1103 CARET / INTERLINK AUDIT: PASS")
print("- 4 procedural references / 1 CAEPR family / 2 Master IDs")
print("- DP↔appeal relationship and dossier↔register backlinks verified")
print("- bilingual identity, adverse-outcome and merits-boundary text verified")
print("- certified-file and representation gaps remain explicit")
