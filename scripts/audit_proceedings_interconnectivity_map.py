#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

required = [
    ROOT / ".github/governance/UNITARY_PROCEEDINGS_INTERCONNECTIVITY_MAP_PROTOCOL_30AUG2026.md",
    ROOT / "assets/data/proceedings-interconnectivity-schema-v1.json",
    ROOT / "assets/proceedings-interconnectivity-map-20260830.js",
    ROOT / "assets/proceedings-interconnectivity-map-20260830.css",
    ROOT / "en/proceedings-map/index.html",
    ROOT / "es/mapa-procedimientos/index.html",
    ROOT / "en/master-proceedings-register/index.html",
    ROOT / "es/registro-maestro-procedimientos/index.html",
    ROOT / "archive/PROCEEDINGS_MASTER_REGISTER.csv",
]

errors = []
for path in required:
    if not path.is_file():
        errors.append(f"missing required file: {path.relative_to(ROOT)}")

if not errors:
    en = (ROOT / "en/proceedings-map/index.html").read_text(encoding="utf-8")
    es = (ROOT / "es/mapa-procedimientos/index.html").read_text(encoding="utf-8")
    en_master = (ROOT / "en/master-proceedings-register/index.html").read_text(encoding="utf-8")
    es_master = (ROOT / "es/registro-maestro-procedimientos/index.html").read_text(encoding="utf-8")
    js = (ROOT / "assets/proceedings-interconnectivity-map-20260830.js").read_text(encoding="utf-8")
    gov = (ROOT / ".github/governance/UNITARY_PROCEEDINGS_INTERCONNECTIVITY_MAP_PROTOCOL_30AUG2026.md").read_text(encoding="utf-8")
    schema = json.loads((ROOT / "assets/data/proceedings-interconnectivity-schema-v1.json").read_text(encoding="utf-8"))

    checks = {
        "en language alternate": "../../es/mapa-procedimientos/" in en,
        "es language alternate": "../../en/proceedings-map/" in es,
        "en master backlink": "../proceedings-map/" in en_master,
        "es master backlink": "../mapa-procedimientos/" in es_master,
        "canonical csv runtime": "archive/PROCEEDINGS_MASTER_REGISTER.csv" in js,
        "public treatment filter": "NOT_SITE_AGGREGATED" in js and "INTERNAL_ONLY" in js and "PRIVATE" in js,
        "parent edge": "Parent_Master_ID" in js and "PARENT_CHILD" in js,
        "linked edge": "Linked_Proceedings" in js,
        "appeal review edge": "Appeal_or_Review" in js,
        "context warning": "wrongdoing or liability" in js and "ilicitud ni responsabilidad" in js,
        "trace view": "data-trace-id" in js and "renderTrace" in js,
        "chronology view": "renderChronology" in js,
        "governance beginning end": "beginning → end" in gov and "end → beginning" in gov,
        "governance direct context split": "DIRECT PROCEDURAL EDGE" in gov and "CONTEXTUAL BRIDGE" in gov,
        "shared continuum hardwired": "Shared-continuum / anti-fragmentation convergence rule" in gov and "shared asset/control/credit/harm continuum" in gov,
        "three appeals convergence": "three Audiencia Provincial appeals" in gov and "calificación appeal" in gov and "fee challenge" in gov,
        "fragmentation audit": "Fragmentation / atomisation audit" in gov and "Who, if anyone, obtained a documented procedural or patrimonial benefit" in gov,
        "fiscal unitary audit": "Ministerio Fiscal unitary-recognition audit" in gov,
        "historical current lineage": "Historical-to-current lineage rule" in gov,
        "schema canonical source": schema.get("canonical_node_source") == "archive/PROCEEDINGS_MASTER_REGISTER.csv",
        "schema reverse navigation": schema.get("principles", {}).get("reverse_navigation_from_explicit_forward_edges_is_permitted") is True,
        "schema shared continuum": schema.get("principles", {}).get("shared_asset_control_credit_harm_continuum_must_be_tested") is True,
        "schema fragmentation audit": "FRAGMENTATION_ATOMISATION_AUDIT" in schema.get("context_lenses", {}),
        "schema convergence view": "CONVERGENCE_CLUSTER" in schema.get("required_views", []),
    }
    for label, ok in checks.items():
        if not ok:
            errors.append(f"failed invariant: {label}")

if errors:
    print("PROCEEDINGS INTERCONNECTIVITY MAP AUDIT: FAIL")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print("PROCEEDINGS INTERCONNECTIVITY MAP AUDIT: PASS")
print("- canonical node source preserved")
print("- EN/ES routes and master-register backlinks present")
print("- explicit procedural edges separated from contextual lenses")
print("- reverse trace, chronology and public-treatment safeguards present")
print("- shared asset/control/credit/harm convergence and fragmentation audit are hardwired")
