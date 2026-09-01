#!/usr/bin/env python3
"""Validate the finite PwC / Carlos Saavedra profile, ^ census and interlinks."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "assets/data/caepr-caret-pwc-carlos-saavedra-first-hop-v1.json"
PAGES = {
    "es": ROOT / "es/pwc-canarias-carlos-saavedra-sun-park/index.html",
    "en": ROOT / "en/pwc-canarias-carlos-saavedra-sun-park/index.html",
}
EXPECTED = {
    "identity_eligible": 35,
    "identity_confirmed": 32,
    "identity_pending": 3,
    "identity_suspended": 0,
    "events_registered": 20,
    "evidence_records_registered": 19,
    "visual_assets_registered": 1,
}
VERDICT = (
    "FINITE PWC / CARLOS SAAVEDRA FIRST-HOP CENSUS COMPLETE; "
    "32/35 CARET_CONFIRMED; 3 CARET_PENDING; 0 CARET_SUSPENDED; "
    "20 EVENTS, 19 EVIDENCE RECORDS AND 1 CANONICAL VISUAL ASSET REGISTERED; "
    "PARTIAL — NOT ALL IS^"
)

errors: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def load(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"cannot load {path.relative_to(ROOT)}: {exc}")
        return {}


def canonical_registry() -> dict[str, dict]:
    master = load(ROOT / "assets/data/matter-identity-registry-v1.json")
    records: dict[str, dict] = {}
    for part in master.get("parts", []):
        path = ROOT / "assets/data" / str(part.get("path", ""))
        for record in load(path).get("records", []):
            rid = record.get("id")
            if isinstance(rid, str):
                check(rid not in records, f"duplicate canonical identity id: {rid}")
                records[rid] = record
    return records


def route_exists(route: str) -> bool:
    if not route.startswith("/") or route.startswith("//"):
        return False
    candidate = ROOT / route.lstrip("/")
    return candidate.is_file() or (candidate / "index.html").is_file()


def validate() -> None:
    data = load(LEDGER)
    check(data.get("control_id") == "PD-PWC-CS-FIRST-HOP-CARET-20260901-01", "control id mismatch")
    check(data.get("status") == "PARTIAL_NOT_ALL_IS", "status must remain PARTIAL_NOT_ALL_IS")
    check(data.get("verdict") == VERDICT, "verdict mismatch")
    counts = data.get("counts", {})
    for key, expected in EXPECTED.items():
        check(counts.get(key) == expected, f"count mismatch for {key}")

    identities = data.get("identity_records", [])
    events = data.get("events", [])
    evidence = data.get("evidence_records", [])
    visual_assets = data.get("visual_assets", [])
    check(len(identities) == 35, "identity record length mismatch")
    check(len(events) == 20, "event record length mismatch")
    check(len(evidence) == 19, "evidence record length mismatch")
    check(len(visual_assets) == 1, "visual asset length mismatch")
    check(sum(r.get("state") == "CARET_CONFIRMED" for r in identities) == 32, "confirmed identity count mismatch")
    check(sum(r.get("state") == "CARET_PENDING" for r in identities) == 3, "pending identity count mismatch")

    registry = canonical_registry()
    carlos = registry.get("PD-SP-P-0036", {})
    check(carlos.get("identity_resolution") == "CARET_CONFIRMED", "Carlos CAEPR identity is not caret-confirmed")
    check(carlos.get("visual_asset_id") == "person.carlos-saavedra-rodriguez-del-palacio.primary", "Carlos CAEPR visual asset link mismatch")
    check(carlos.get("public_profiles", {}).get("linkedin") == "https://es.linkedin.com/in/carlos-saavedra-b71418a8", "Carlos LinkedIn profile mismatch")
    check(carlos.get("routes", {}).get("es") == "/es/pwc-canarias-carlos-saavedra-sun-park/", "Carlos ES route mismatch")
    check(carlos.get("routes", {}).get("en") == "/en/pwc-canarias-carlos-saavedra-sun-park/", "Carlos EN route mismatch")
    newly_resolved = {
        "PD-SP-P-0039": "Alejandro Perera González",
        "PD-SP-P-0040": "Jonathan Simó Morales",
        "PD-SP-P-0146": "Simon Peter Thompson",
        "PD-SP-O-0003": "Matkator, S.L.U.",
        "PD-SP-O-0080": "Landwell-PricewaterhouseCoopers Tax & Legal Services, S.L.",
        "PD-SP-O-0081": "PricewaterhouseCoopers Auditores, S.L.",
        "PD-SP-O-0082": "Grupo Acosta Matos, S.L.",
        "PD-SP-O-0083": "Socios Inversores Canarios, S.L.",
        "PD-SP-I-0042": "Comisión Nacional del Mercado de Valores",
    }
    for rid, name in newly_resolved.items():
        record = registry.get(rid, {})
        check(record.get("name") == name, f"newly resolved identity name mismatch: {rid}")
        check(record.get("identity_resolution") == "CARET_CONFIRMED", f"newly resolved identity is not caret-confirmed: {rid}")
        check(bool(record.get("identity_sources")), f"newly resolved identity lacks sources: {rid}")
    check(registry.get("PD-SP-O-0003", {}).get("registry_sheet") == "TF 52875", "Matkator registry sheet mismatch")
    check(registry.get("PD-SP-O-0080", {}).get("tax_identifier") == "B80909278", "PwC Tax & Legal NIF mismatch")
    check(registry.get("PD-SP-O-0081", {}).get("roac_number") == "S0242", "PwC Auditores ROAC mismatch")
    check(registry.get("PD-SP-O-0082", {}).get("registry_sheet") == "GC 62169", "Grupo Acosta Matos registry sheet mismatch")
    check(registry.get("PD-SP-O-0083", {}).get("registry_sheet") == "GC 65871", "Socios Inversores Canarios registry sheet mismatch")
    identity_keys: set[str] = set()
    for expected_ordinal, record in enumerate(identities, 1):
        check(record.get("ordinal") == expected_ordinal, f"bad identity ordinal {expected_ordinal}")
        key = str(record.get("object_key", ""))
        check(bool(key) and key not in identity_keys, f"bad or duplicate identity key: {key}")
        identity_keys.add(key)
        state = record.get("state")
        if state == "CARET_CONFIRMED":
            rid = record.get("caepr_id")
            check(rid in registry, f"confirmed identity missing from CAEPR: {rid}")
            if rid in registry:
                check(record.get("label") == registry[rid].get("name"), f"label mismatch for {rid}")
            check("next_source_needed" not in record, f"confirmed identity has pending-source field: {key}")
        elif state == "CARET_PENDING":
            check("caepr_id" not in record, f"pending identity improperly has caepr_id: {key}")
            check(bool(record.get("next_source_needed")), f"pending identity lacks next source: {key}")
        else:
            check(False, f"unsupported identity state: {state}")

    event_ids: set[str] = set()
    evidence_ids = {str(record.get("id", "")) for record in evidence}
    check("" not in evidence_ids and len(evidence_ids) == len(evidence), "bad or duplicate evidence id")
    for event in events:
        event_id = str(event.get("id", ""))
        check(bool(event_id) and event_id not in event_ids, f"bad or duplicate event id: {event_id}")
        event_ids.add(event_id)
        check(event.get("state") == "REGISTERED", f"event not registered: {event_id}")
        for ref in event.get("evidence_refs", []):
            check(ref in evidence_ids, f"missing evidence ref {ref} on {event_id}")
        for route in event.get("routes", {}).values():
            check(route_exists(str(route)), f"missing event route: {route}")
    for record in evidence:
        for route in record.get("routes", {}).values():
            check(route_exists(str(route)), f"missing evidence route: {route}")

    visual = visual_assets[0] if len(visual_assets) == 1 else {}
    visual_path = ROOT / str(visual.get("repository_path", ""))
    check(visual.get("id") == "person.carlos-saavedra-rodriguez-del-palacio.primary", "Carlos visual asset id mismatch")
    check(visual.get("linked_identity") == "PD-SP-P-0036", "Carlos visual identity link mismatch")
    check(visual_path.is_file(), "Carlos visual asset file missing")
    if visual_path.is_file():
        check(hashlib.sha256(visual_path.read_bytes()).hexdigest() == visual.get("sha256"), "Carlos visual asset SHA-256 mismatch")

    required_markers = {
        "es": (
            'id="registro-caret"',
            "PARCIAL — NO TODO ES^",
            "32/35",
            "Impugnaciones y poderes para pleitos de LPB y Simon Thompson",
            "Jonathan Simó remite el informe; PwC revisa/aprueba la versión",
            "Dos grabaciones AMR localizadas miden ≈126m36s",
            "La ruta heredada «11-Jun» se mantiene solo como alias de historial de versión.",
            "caepr-caret-pwc-carlos-saavedra-first-hop-v1.json",
            "carlos-saavedra--linkedin-profile--20260901.jpg",
            "https://es.linkedin.com/in/carlos-saavedra-b71418a8",
            "PD-SP-P-0036 · CARET_CONFIRMED · ACTIVO VISUAL CANÓNICO",
        ),
        "en": (
            'id="caret-register"',
            "PARTIAL — NOT ALL IS^",
            "32/35",
            "LPB and Simon Thompson Community challenges and litigation powers",
            "Jonathan Simó transmits the report; PwC reviews/approves the version",
            "Two located AMR recordings measure ≈126m36s",
            "The inherited “11-Jun” route is retained only as a version-history alias.",
            "caepr-caret-pwc-carlos-saavedra-first-hop-v1.json",
            "carlos-saavedra--linkedin-profile--20260901.jpg",
            "https://es.linkedin.com/in/carlos-saavedra-b71418a8",
            "PD-SP-P-0036 · CARET_CONFIRMED · CANONICAL VISUAL ASSET",
        ),
    }
    forbidden = (
        '<span class="metric">11 jun</span>',
        '<span class="metric">11 Jun</span>',
        "Reunión de 144 minutos",
        "144-minute meeting addresses",
        "11–16 jun 2016",
        "11–16 Jun 2016",
    )
    for locale, path in PAGES.items():
        html = path.read_text(encoding="utf-8")
        for marker in required_markers[locale]:
            check(marker in html, f"{locale} page missing marker: {marker}")
        for marker in forbidden:
            check(marker not in html, f"{locale} page retains stale assertion: {marker}")
        check(html.count('src="../../assets/actors/carlos-saavedra--linkedin-profile--20260901.jpg"') == 1, f"{locale} page must display one Carlos portrait")
        check(html.count('href="../../assets/actors/carlos-saavedra--linkedin-profile--20260901.jpg"') == 1, f"{locale} page must provide one full-resolution Carlos portrait link")
        for record in identities:
            if record.get("state") == "CARET_CONFIRMED":
                rid = str(record.get("caepr_id"))
                check(f"#{rid}" in html, f"{locale} page missing confirmed identity link: {rid}")
        check(html.count("<sup>^</sup>") == 33, f"{locale} page must display 33 caret occurrences for 32 unique identities")

    backlinks = {
        ROOT / "es/actores-partes-abogados-representantes/index.html": "../pwc-canarias-carlos-saavedra-sun-park/#registro-caret",
        ROOT / "en/actors-parties-lawyers-representatives/index.html": "../pwc-canarias-carlos-saavedra-sun-park/#caret-register",
    }
    for path, marker in backlinks.items():
        check(path.read_text(encoding="utf-8").count(marker) >= 3, f"missing actor-register backlinks in {path.relative_to(ROOT)}")


if __name__ == "__main__":
    validate()
    if errors:
        print("PwC / Carlos Saavedra ^ validation: FAIL")
        for error in errors:
            print(f"- {error}")
        sys.exit(1)
    print("PwC / Carlos Saavedra ^ validation: PASS")
    print(VERDICT)
