#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

required = [
    ROOT / ".github/governance/UNITARY_PROCEEDINGS_INTERCONNECTIVITY_MAP_PROTOCOL_30AUG2026.md",
    ROOT / ".github/governance/A_SCAN_360_CASE_PRISM_AND_READER_LENS_PROTOCOL_30AUG2026.md",
    ROOT / "archive/PROCEEDINGS_ANTI_FRAGMENTATION_CONVERGENCE_RULE_30AUG2026.md",
    ROOT / "archive/INSTITUTIONAL_READER_UNITARY_PROCEEDINGS_RULE_30AUG2026.md",
    ROOT / "archive/CAIXABANK_VALENCIA_01859_2023_REGISTRATION_GAP_30AUG2026.md",
    ROOT / "archive/PROCEEDINGS_MASTER_REGISTER_VALENCIA_1859_2023_OVERLAY_30AUG2026.md",
    ROOT / "assets/data/proceedings-interconnectivity-schema-v1.json",
    ROOT / "assets/data/proceedings-case-prism-v1.json",
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
    csv_text = (ROOT / "archive/PROCEEDINGS_MASTER_REGISTER.csv").read_text(encoding="utf-8")
    js = (ROOT / "assets/proceedings-interconnectivity-map-20260830.js").read_text(encoding="utf-8")
    css = (ROOT / "assets/proceedings-interconnectivity-map-20260830.css").read_text(encoding="utf-8")
    gov = (ROOT / ".github/governance/UNITARY_PROCEEDINGS_INTERCONNECTIVITY_MAP_PROTOCOL_30AUG2026.md").read_text(encoding="utf-8")
    ascan = (ROOT / ".github/governance/A_SCAN_360_CASE_PRISM_AND_READER_LENS_PROTOCOL_30AUG2026.md").read_text(encoding="utf-8")
    anti = (ROOT / "archive/PROCEEDINGS_ANTI_FRAGMENTATION_CONVERGENCE_RULE_30AUG2026.md").read_text(encoding="utf-8")
    institutional = (ROOT / "archive/INSTITUTIONAL_READER_UNITARY_PROCEEDINGS_RULE_30AUG2026.md").read_text(encoding="utf-8")
    valencia_gap = (ROOT / "archive/CAIXABANK_VALENCIA_01859_2023_REGISTRATION_GAP_30AUG2026.md").read_text(encoding="utf-8")
    valencia_overlay = (ROOT / "archive/PROCEEDINGS_MASTER_REGISTER_VALENCIA_1859_2023_OVERLAY_30AUG2026.md").read_text(encoding="utf-8")
    schema = json.loads((ROOT / "assets/data/proceedings-interconnectivity-schema-v1.json").read_text(encoding="utf-8"))
    prism = json.loads((ROOT / "assets/data/proceedings-case-prism-v1.json").read_text(encoding="utf-8"))

    appellate_refs = ["RPL 2523/2025", "RPL 3304/2025", "RPL 3319/2025", "RPL 421/2026"]
    valencia_exact = ["VAL-CIV-001", "ORD 1859/2023-9", "46250-42-1-2023-0049579", "28 January 2027", "10:00"]
    valencia_exact_es = ["VAL-CIV-001", "ORD 1859/2023-9", "46250-42-1-2023-0049579", "28 de enero de 2027", "10:00"]
    prism_required_views = ["DECISION_DEPENDENCY_MATRIX", "PARALLEL_PROCEEDINGS_LANES", "ISOLATION_TEST", "AUDIENCE_LENS"]
    prism_statuses = {"DIRECT", "CONTEXT", "OPEN", "NOT_LOCATED", "OUTSIDE"}
    prism_lane_ids = {lane.get("id") for lane in prism.get("lanes", [])}
    prism_master_ids = {mid for lane in prism.get("lanes", []) for mid in lane.get("master_ids", [])}

    checks = {
        "en language alternate": "../../es/mapa-procedimientos/" in en,
        "es language alternate": "../../en/proceedings-map/" in es,
        "en master backlink": "../proceedings-map/" in en_master,
        "es master backlink": "../mapa-procedimientos/" in es_master,
        "canonical csv runtime": "archive/PROCEEDINGS_MASTER_REGISTER.csv" in js,
        "case prism runtime": "assets/data/proceedings-case-prism-v1.json" in js,
        "public treatment filter": "NOT_SITE_AGGREGATED" in js and "INTERNAL_ONLY" in js and "PRIVATE" in js,
        "parent edge": "Parent_Master_ID" in js and "PARENT_CHILD" in js,
        "linked edge": "Linked_Proceedings" in js,
        "appeal review edge": "Appeal_or_Review" in js,
        "context warning": "wrongdoing or liability" in js and "ilicitud ni responsabilidad" in js,
        "trace view": "data-trace-id" in js and "renderTrace" in js,
        "chronology view": "renderChronology" in js,
        "case prism matrix rendered": "renderPrism" in js and "pdim-prism-table" in js and "data-prism-prop" in js,
        "parallel lanes rendered": "renderParallelLanes" in js and "pdim-lane-timeline" in js,
        "isolation rendered": "renderIsolation" in js and "data-isolation-lane" in js,
        "audience lens rendered": "data-prism-audience" in js and "audience_priority" in js,
        "case prism CSS": ".pdim-prism-table" in css and ".pdim-isolation-grid" in css and ".pdim-lane-timeline" in css,
        "governance beginning end": "beginning → end" in gov and "end → beginning" in gov,
        "governance direct context split": "DIRECT PROCEDURAL EDGE" in gov and "CONTEXTUAL BRIDGE" in gov,
        "shared continuum hardwired": "Shared-continuum / anti-fragmentation convergence rule" in gov and "shared asset/control/credit/harm continuum" in gov,
        "three appeals convergence": "three Audiencia Provincial appeals" in gov and "calificación appeal" in gov and "fee challenge" in gov,
        "fragmentation audit": "Fragmentation / atomisation audit" in gov and "Who, if anyone, obtained a documented procedural or patrimonial benefit" in gov,
        "fiscal unitary audit": "Ministerio Fiscal unitary-recognition audit" in gov,
        "historical current lineage": "Historical-to-current lineage rule" in gov,
        "A-scan governance": "Architecture" in ascan and "Authority" in ascan and "Attribution" in ascan and "Audience" in ascan and "Actionability" in ascan,
        "A-scan isolation boundary": "does not prove that an organ knew" in ascan,
        "A-scan reader lens invariant": "It must never change" in ascan and "source status" in ascan,
        "anti-fragmentation core": "procedural separateness" in anti.lower() and "patrimonial" in anti.lower(),
        "institutional completeness rule": "Institutional completeness test" in institutional,
        "institutional no predetermined outcome": "predetermined" in institutional,
        "institutional formal-procedure boundary": "not a substitute for a filing" in institutional,
        "institutional three-object correction": all(ref in institutional for ref in appellate_refs),
        "institutional fees correction": "Do not describe `RPL 3319/2025` as the fees appeal" in institutional,
        "canonical Valencia row exists": "VAL-CIV-001" in csv_text and "JPI nº 27 Valencia" in csv_text and "Procedimiento 1859/2023" in csv_text,
        "Valencia correction binds existing row": "canonical identity is `VAL-CIV-001`" in valencia_gap,
        "Valencia no duplicate ID": "do not create a second master row" in valencia_gap.lower() and "Do **not** create a second Valencia row" in valencia_overlay,
        "Valencia overlay corrects existing row": "correction overlay" in valencia_overlay.lower() and "VAL-CIV-001" in valencia_overlay,
        "en appellate refs": all(ref in en for ref in appellate_refs),
        "es appellate refs": all(ref in es for ref in appellate_refs),
        "en institutional test": "Institutional completeness test" in en and "No conclusion is requested here" in en,
        "es institutional test": "Prueba de integridad institucional" in es and "No se solicita aquí una conclusión" in es,
        "en formal route warning": "not an extra-record filing" in en,
        "es formal route warning": "no es un escrito procesal" in es,
        "en not-located discipline": "NOT LOCATED is not DID NOT EXIST" in en,
        "es not-located discipline": "NO LOCALIZADO no equivale a NO EXISTIÓ" in es,
        "en exact Valencia public correction": all(token in en for token in valencia_exact),
        "es exact Valencia public correction": all(token in es for token in valencia_exact_es),
        "en Case Prism first read": "A-SCAN 360 · Case Prism" in en and "Isolation test" in en and "reader lens" in en,
        "es Case Prism first read": "A-SCAN 360 · Prisma del caso" in es and "Prueba de aislamiento" in es and "lente del lector" in es,
        "en master Valencia correction notice": "valencia-val-civ-001-correction" in en_master and "ORD 1859/2023-9" in en_master,
        "es master Valencia correction notice": "correccion-valencia-val-civ-001" in es_master and "ORD 1859/2023-9" in es_master,
        "schema canonical source": schema.get("canonical_node_source") == "archive/PROCEEDINGS_MASTER_REGISTER.csv",
        "schema Case Prism source": schema.get("case_prism_source") == "assets/data/proceedings-case-prism-v1.json",
        "schema reverse navigation": schema.get("principles", {}).get("reverse_navigation_from_explicit_forward_edges_is_permitted") is True,
        "schema shared continuum": schema.get("principles", {}).get("shared_asset_control_credit_harm_continuum_must_be_tested") is True,
        "schema fragmentation audit": "FRAGMENTATION_ATOMISATION_AUDIT" in schema.get("context_lenses", {}),
        "schema convergence view": "CONVERGENCE_CLUSTER" in schema.get("required_views", []),
        "schema new Case Prism views": all(view in schema.get("required_views", []) for view in prism_required_views),
        "schema implementation mapping": all(view in schema.get("implemented_public_views", {}) for view in prism_required_views),
        "prism canonical source": prism.get("canonical_node_source") == "archive/PROCEEDINGS_MASTER_REGISTER.csv",
        "prism status vocabulary": set(prism.get("statuses", {}).keys()) == prism_statuses,
        "prism high-priority lanes": {"concurso", "calificacion", "removal", "fees", "arrecife", "valencia", "meetingpoint", "tenerife", "fiscalia", "supervision", "historical"}.issubset(prism_lane_ids),
        "prism exact appellate IDs": {"GC-APP-004", "GC-APP-005", "GC-APP-006", "GC-APP-028"}.issubset(prism_master_ids),
        "prism Valencia ID": "VAL-CIV-001" in prism_master_ids,
        "prism Meeting Point ID": "GC-CONT-025" in prism_master_ids,
        "prism finite propositions": len(prism.get("propositions", [])) >= 8,
        "prism cell status discipline": all(cell.get("status") in prism_statuses for prop in prism.get("propositions", []) for cell in prop.get("cells", {}).values()),
        "prism no second case master": not any(mid.startswith("VAL-") and mid != "VAL-CIV-001" for mid in prism_master_ids),
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
print("- institutional-reader completeness test present in both languages")
print("- Audiencia appellate objects locked as 2523 / 3304+3319 / 421")
print("- Valencia canonical identity locked to existing VAL-CIV-001; duplicate-case creation prohibited")
print("- exact Valencia court/NIG/hearing correction visible on map and master-register reader pages")
print("- A-SCAN 360 Case Prism implements decision-dependency matrix, parallel lanes, isolation test and reader lens")
