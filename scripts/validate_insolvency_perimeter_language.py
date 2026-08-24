#!/usr/bin/env python3
"""Prevent insolvency-perimeter and controlled-name regressions."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_ROOTS = (ROOT / "en", ROOT / "es", ROOT / "assets")
SUFFIXES = {".html", ".js", ".svg"}

FORBIDDEN = (
    "lpb was insolvent",
    "lpb era insolvente",
    "the insolvent hotel",
    "the hotel was insolvent",
    "el hotel era insolvente",
    "sun park insolvency life",
    "vida concursal de sun park",
    "the same hotel’s insolvency and investor lives",
    "the same hotel's insolvency and investor lives",
    "la vida concursal y la vida inversora del mismo hotel",
)

CANONICAL = {
    ROOT / "en" / "lpb-insolvency" / "index.html": (
        "LPB as the only debtor",
        "not 100% of Sun Park",
        "Not: “Sun Park was insolvent”",
    ),
    ROOT / "es" / "insolvencia-lpb" / "index.html": (
        "LPB como única deudora",
        "no del 100% de Sun Park",
        "No: “Sun Park estaba en concurso”",
    ),
}

NAME_REGISTER = ROOT / "ops" / "CANONICAL_ENTITY_NAMES.json"
NAME_SCAN_ROOTS = tuple(
    ROOT / name
    for name in (
        "en",
        "es",
        "assets",
        "archive",
        "operations",
        "prompts",
        "publication-manifests",
        "docs",
        "ops",
    )
)
NAME_SCAN_EXACT = tuple(
    ROOT / name
    for name in (
        "AGENTS.md",
        "CHATGPT_START_HERE.md",
        "CURRENT_HANDOVER_UNITARY_RECOVERY_21AUG2026.md",
        "README.md",
    )
)
NAME_SCAN_SUFFIXES = {
    ".html",
    ".js",
    ".mjs",
    ".json",
    ".md",
    ".csv",
    ".txt",
    ".xml",
    ".yml",
    ".yaml",
}
NAME_SCAN_EXCLUSIONS = {
    NAME_REGISTER,
    ROOT / "archive" / "CORRECTION_REGISTER.md",
}
FORBIDDEN_GENERATED_ALIASES = (
    "Lanzarote Paradise Beach",
    "Lanzarote Paradise Beach, S.L.",
    "Lanzarote Playa Blanca",
    "Luchi Playa Blanca",
    "Luci Playa Blanca",
    "Lucy Playa Blanca",
)
EXPECTED_NAME_RECORDS = {
    "E003": {
        "canonical_name": "Luchy Playa Blanca, S.L.U.",
        "first_reference": "Luchy Playa Blanca, S.L.U. (LPB)",
        "identifier": {"type": "CIF", "value": "B35998582"},
        "registered_denominational_form": "LUCHY PLAYA BLANCA SOCIEDAD LIMITADA",
        "registered_status_descriptor": "Sociedad unipersonal",
    },
    "E005": {
        "canonical_name": "Aweswell Limited",
        "identifier": {"type": "UK company number", "value": "07716847"},
        "former_name": "Monterecco Sun Park Limited",
        "former_name_period": "2011-07-25/2014-06-03",
    },
    "P-JTPS": {
        "canonical_name": "Juan Tomás Parrilla Suárez",
        "first_reference": "Juan Tomás Parrilla Suárez",
    },
}
REQUIRED_OFFICIAL_URLS = {
    "E003": {
        "https://www.boe.es/buscar/doc.php?id=BOE-B-2012-22189",
        "https://www.boe.es/buscar/doc.php?id=BOE-B-2013-26977",
        "https://www.boe.es/diario_borme/txt.php?id=BORME-A-2012-39-35",
        "https://www.boe.es/diario_borme/txt.php?id=BORME-A-2012-198-35",
    },
    "E005": {"https://find-and-update.company-information.service.gov.uk/company/07716847"},
    "P-JTPS": {"https://www.boe.es/buscar/doc.php?id=BOE-B-2010-5683"},
}
CANONICAL_NAME_MARKERS = {
    ROOT / "AGENTS.md": (
        "ops/CANONICAL_ENTITY_NAMES.json",
        "Luchy Playa Blanca, S.L.U. (LPB)",
    ),
    ROOT / "CHATGPT_START_HERE.md": (
        "ops/CANONICAL_ENTITY_NAMES.json",
        "Juan Tomás Parrilla Suárez",
    ),
    ROOT / "archive" / "OUTBOUND_EMAIL_COMMUNICATIONS_PROTOCOL_23AUG2026.md": (
        "Luchy Playa Blanca, S.L.U. (LPB)",
        "Juan Tomás Parrilla Suárez",
    ),
    ROOT / "archive" / "knowledge-project" / "SUN_PARK_CANONICAL_ENTITY_REGISTER.md": (
        "LOCKED_CANONICAL_OFFICIAL",
        "CIF B35998582",
        "company no. 07716847",
    ),
    ROOT / "publication-manifests" / "lpb-canonical-name-lock-20260824.json": (
        "LPB-CANONICAL-NAME-LOCK-20260824",
        "Luchy Playa Blanca, S.L.U. (LPB)",
        "BOE-B-2012-22189",
    ),
    ROOT / "es" / "garrigues-la-laguna" / "index.html": (
        "Luchy Playa Blanca, S.L.U. (LPB)",
        "CIF B35998582",
    ),
    ROOT / "en" / "garrigues-la-laguna" / "index.html": (
        "Luchy Playa Blanca, S.L.U. (LPB)",
        "CIF B35998582",
    ),
}


def public_files() -> list[Path]:
    files: list[Path] = []
    for root in PUBLIC_ROOTS:
        files.extend(path for path in root.rglob("*") if path.suffix.lower() in SUFFIXES)
    return sorted(files)


def controlled_name_files() -> list[Path]:
    files = {path for path in NAME_SCAN_EXACT if path.is_file()}
    for root in NAME_SCAN_ROOTS:
        if not root.is_dir():
            continue
        files.update(
            path
            for path in root.rglob("*")
            if path.is_file()
            and path.suffix.lower() in NAME_SCAN_SUFFIXES
            and path not in NAME_SCAN_EXCLUSIONS
        )
    return sorted(files)


def validate_name_register(errors: list[str]) -> None:
    if not NAME_REGISTER.is_file():
        errors.append(f"missing canonical-name register: {NAME_REGISTER.relative_to(ROOT)}")
        return

    try:
        register = json.loads(NAME_REGISTER.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid canonical-name register: {exc}")
        return

    if register.get("schema") != "por-derecho.canonical-names.v1":
        errors.append("canonical-name register schema changed or is missing")

    records = {record.get("id"): record for record in register.get("records", [])}
    for record_id, expected in EXPECTED_NAME_RECORDS.items():
        record = records.get(record_id)
        if record is None:
            errors.append(f"canonical-name register missing {record_id}")
            continue
        for field, expected_value in expected.items():
            if record.get(field) != expected_value:
                errors.append(
                    f"canonical-name register {record_id}.{field} is {record.get(field)!r}, "
                    f"expected {expected_value!r}"
                )
        source_urls = {source.get("url") for source in record.get("official_sources", [])}
        missing_urls = REQUIRED_OFFICIAL_URLS[record_id] - source_urls
        if missing_urls:
            errors.append(f"canonical-name register {record_id} missing official URLs: {sorted(missing_urls)}")

    lpb = records.get("E003", {})
    if lpb.get("registry_coordinates", {}).get("sheet") != "IL 9469":
        errors.append("canonical-name register E003 registry sheet is not IL 9469")
    if not lpb.get("do_not_translate_legal_name"):
        errors.append("canonical-name register E003 do-not-translate lock is absent")
    registered_aliases = {alias.casefold() for alias in lpb.get("forbidden_generated_aliases", [])}
    for alias in FORBIDDEN_GENERATED_ALIASES:
        if alias.casefold() not in registered_aliases:
            errors.append(f"canonical-name register E003 missing forbidden generated alias {alias!r}")


def validate_controlled_names(errors: list[str]) -> None:
    validate_name_register(errors)

    for path in controlled_name_files():
        text = path.read_text(encoding="utf-8", errors="replace").casefold()
        for alias in FORBIDDEN_GENERATED_ALIASES:
            if alias.casefold() in text:
                errors.append(
                    f"{path.relative_to(ROOT)}: forbidden invented or misspelled LPB name {alias!r}"
                )

    for path, markers in CANONICAL_NAME_MARKERS.items():
        if not path.is_file():
            errors.append(f"missing canonical-name control file: {path.relative_to(ROOT)}")
            continue
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                errors.append(f"{path.relative_to(ROOT)}: canonical-name marker missing: {marker!r}")


def main() -> int:
    errors: list[str] = []

    for path in public_files():
        text = path.read_text(encoding="utf-8", errors="replace")
        lower = text.lower()
        for phrase in FORBIDDEN:
            if phrase in lower:
                errors.append(f"{path.relative_to(ROOT)}: forbidden unqualified wording {phrase!r}")

    for path, markers in CANONICAL.items():
        if not path.is_file():
            errors.append(f"missing canonical insolvency-perimeter page: {path.relative_to(ROOT)}")
            continue
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                errors.append(f"{path.relative_to(ROOT)}: canonical marker missing: {marker!r}")

    validate_controlled_names(errors)

    if errors:
        print("INSOLVENCY-PERIMETER LANGUAGE GATE: FAIL")
        for item in errors:
            print(f" - {item}")
        return 1

    print(
        "INSOLVENCY-PERIMETER + CANONICAL-NAME GATE: PASS "
        f"({len(public_files())} public files; {len(controlled_name_files())} name-controlled files inspected)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
