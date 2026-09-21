#!/usr/bin/env python3
from __future__ import annotations
import json, pathlib, re, sys

ROOT=pathlib.Path(__file__).resolve().parents[1]
BASE=ROOT/"evidence/judicial/june-2026-three-track"
fail=[]

required=[
 BASE/"README.md",BASE/"FROZEN_INDEX.md",BASE/"source-manifest.json",
 BASE/"dynamic/ref21-living-dossier.md",BASE/"dynamic/ref22-living-dossier.md",BASE/"dynamic/ref24-living-dossier.md",
 BASE/"frozen/ref21-25jun2026-pages-001-030.md",BASE/"frozen/ref21-25jun2026-pages-031-060.md",BASE/"frozen/ref21-25jun2026-pages-061-086.md",
 BASE/"frozen/ref21-26jun2026-working-pages-001-026.md",BASE/"frozen/ref21-09jul2026-ampliacion-pages-001-019.md",
 BASE/"frozen/ref22-18jun2026-pages-001-030.md",BASE/"frozen/ref22-18jun2026-pages-031-055.md",
 BASE/"frozen-linked/di169-ref24-traceability-aportacion-25jun2026.md",
 ROOT/"evidence/judicial-governance/decanato-reference-24/full-text/denuncia-magistrado-18jun2026-public-transcription.md",
 ROOT/"evidence/judicial-governance/decanato-reference-24/full-text/ampliacion-denuncia-magistrado-25jun2026-public-transcription.md",
]
for p in required:
 if not p.is_file(): fail.append(f"missing:{p.relative_to(ROOT)}")

if not fail:
 data=json.loads((BASE/"source-manifest.json").read_text(encoding="utf-8"))
 if data.get("schema")!="por-derecho.june-three-track-dual-version.v1": fail.append("schema")
 if data["tracks"]["REF21"]["frozen"].get("working_status")!="SOURCE_PRESERVED_FILING_NOT_PROVED": fail.append("ref21_26jun_status")
 if data["tracks"]["REF21"]["frozen"].get("ampliacion_pages")!=19: fail.append("ref21_09jul_pages")
 if data["tracks"]["REF22"]["frozen"].get("pages")!=55: fail.append("ref22_pages")
 if data["tracks"]["REF24"]["frozen"].get("supplement_pages")!=13: fail.append("ref24_supplement_pages")
 if data["tracks"]["REF24"].get("linked_institutional_traceability",{}).get("pages")!=9: fail.append("ref24_cgpj_trace_pages")
 if data["tracks"]["REF24"].get("linked_institutional_traceability",{}).get("relationship")!="SEPARATE_INSTITUTIONAL_ROUTE_NOT_SECOND_REF24_JUDICIAL_PLEADING": fail.append("ref24_cgpj_route_separation")

 pii_patterns=[r"Y2231410X",r"sbu001@",r"Pozo Cabildo",r"\+34\s*648",r"\+44\s*7748"]
 for p in (BASE/"frozen").glob("*.md"):
  t=p.read_text(encoding="utf-8",errors="ignore")
  for pat in pii_patterns:
   if re.search(pat,t,re.I): fail.append(f"pii:{p.name}:{pat}")

 if "FROZEN" not in (BASE/"README.md").read_text(encoding="utf-8") or "DYNAMIC" not in (BASE/"README.md").read_text(encoding="utf-8"):
  fail.append("dual_layer_rule_missing")

print("PASS" if not fail else "FAIL")
for x in fail: print(x)
sys.exit(1 if fail else 0)
