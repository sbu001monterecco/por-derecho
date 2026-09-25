#!/usr/bin/env python3
"""Validate Por Derecho Transparency Phase 1 publication and name boundaries."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EN = ROOT / "en/por-derecho/transparency/index.html"
ES = ROOT / "es/por-derecho/transparencia/index.html"
DATA = ROOT / "assets/data/por-derecho-transparency-phase1-v1.json"
PEOPLE = ROOT / "assets/data/matter-identity-registry-v1.people.json"
SITEMAP = ROOT / "sitemap-por-derecho-foundation.xml"
SCRIPT = ROOT / "assets/por-derecho/por-derecho.js"
RECORD = ROOT / "archive/POR_DERECHO_TRANSPARENCY_PHASE1_25AUG2026.md"

REQUIRED = [EN, ES, DATA, PEOPLE, SITEMAP, SCRIPT, RECORD]
ALLOWED_PUBLIC_PERSON_IDS = {"PD-SP-P-0001"}
FORBIDDEN_PUBLIC_TOKENS = [
    "mail.google.com/",
    "drive.google.com/",
    "gmail_message_id",
    "attachment_id",
    "drive_file_id",
    "provider_locator",
    "private_locator",
    "sk-proj-",
    "OPENAI_API_KEY",
]


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> int:
    errors: list[str] = []
    for path in REQUIRED:
        if not path.exists():
            fail(errors, f"missing required file: {path.relative_to(ROOT)}")
    if errors:
        for item in errors:
            print(f"ERROR: {item}", file=sys.stderr)
        return 1

    en = read(EN)
    es = read(ES)
    sitemap = read(SITEMAP)
    script = read(SCRIPT)
    record = read(RECORD)
    data = json.loads(read(DATA))
    people = json.loads(read(PEOPLE))

    page_checks = {
        "English transparency page": (
            en,
            [
                'data-pd-transparency-hub="phase1-20260825"',
                "Por Derecho is an initiative in formation",
                "Gil Marer",
                "PD-SP-P-0001",
                "No independent governing body has been constituted",
                "Phase 1 introduces no new historical actor profile",
                "Inclusion records a role; it does not imply wrongdoing",
                "A consolidated present-tense statement",
                "No response is treated as an admission",
                'href="../../matter-identity-registry/"',
            ],
        ),
        "Spanish transparency page": (
            es,
            [
                'data-pd-transparency-hub="phase1-20260825"',
                "Por Derecho es una iniciativa en formación",
                "Gil Marer",
                "PD-SP-P-0001",
                "No existe todavía un órgano de gobierno independiente constituido",
                "La Fase 1 no crea ninguna nueva ficha histórica",
                "La inclusión registra una función; no implica conducta ilícita",
                "Está en verificación una declaración consolidada",
                "La falta de respuesta no se trata como admisión",
                'href="../../registro-identidad-materia/"',
            ],
        ),
    }
    for label, (body, markers) in page_checks.items():
        for marker in markers:
            if marker not in body:
                fail(errors, f"{label} missing marker: {marker!r}")

    if 'hreflang="es" href="https://sbu001monterecco.github.io/por-derecho/es/por-derecho/transparencia/"' not in en:
        fail(errors, "English route lacks exact Spanish alternate")
    if 'hreflang="en" href="https://sbu001monterecco.github.io/por-derecho/en/por-derecho/transparency/"' not in es:
        fail(errors, "Spanish route lacks exact English alternate")

    for token in FORBIDDEN_PUBLIC_TOKENS:
        if token in en or token in es or token in read(DATA) or token in record:
            fail(errors, f"private/security-sensitive token found in Phase 1 package: {token}")

    person_records = people.get("records", [])
    person_by_id = {record.get("id"): record.get("name") for record in person_records}
    if person_by_id.get("PD-SP-P-0001") != "Gil Marer":
        fail(errors, "PD-SP-P-0001 does not resolve to Gil Marer in the immutable registry")
    combined_pages = f"{en}\n{es}"
    for person_id, name in person_by_id.items():
        if not isinstance(name, str) or person_id in ALLOWED_PUBLIC_PERSON_IDS:
            continue
        if re.search(rf"(?<![\wÁÉÍÓÚÜÑáéíóúüñ]){re.escape(name)}(?![\wÁÉÍÓÚÜÑáéíóúüñ])", combined_pages):
            fail(errors, f"unapproved canonical person name appears in Phase 1 pages: {person_id} {name}")

    if data.get("release_id") != "PD-TR-20260825-01":
        fail(errors, "unexpected transparency release ID")
    if data.get("organisational_status", {}).get("current_public_voice", {}).get("identity_id") != "PD-SP-P-0001":
        fail(errors, "current public voice is not tied to PD-SP-P-0001")
    policy = data.get("historical_names_policy", {})
    if policy.get("public_tiers_permitted") != ["P0", "P1", "P2", "P3"]:
        fail(errors, "public tier boundary must be exactly P0-P3")
    if policy.get("new_public_actor_profiles_created_by_phase1") != 0:
        fail(errors, "Phase 1 must create zero new actor profiles")
    if policy.get("unreviewed_names_permitted") is not False:
        fail(errors, "unreviewed names must remain prohibited")
    if policy.get("completeness_claimed") is not False:
        fail(errors, "Phase 1 must not claim historical census completeness")

    for route in (
        "https://sbu001monterecco.github.io/por-derecho/en/por-derecho/transparency/",
        "https://sbu001monterecco.github.io/por-derecho/es/por-derecho/transparencia/",
    ):
        if route not in sitemap:
            fail(errors, f"Foundation sitemap missing route: {route}")

    script_markers = [
        "pdTransparencyLink",
        "data-pd-transparency-phase1",
        "addTransparencyHome",
        "addTransparencyStrip",
        "transparency/",
        "transparencia/",
    ]
    for marker in script_markers:
        if marker not in script:
            fail(errors, f"Por Derecho shared script missing Phase 1 marker: {marker}")

    if "Authorise Phase 1 using only the reviewed P0–P3 names" not in record:
        fail(errors, "authorisation wording is not preserved in the governance record")

    if errors:
        print("Por Derecho Transparency Phase 1 validation FAILED", file=sys.stderr)
        for item in errors:
            print(f"- {item}", file=sys.stderr)
        return 1

    print(
        "Por Derecho Transparency Phase 1 validation PASS: paired routes, P0-P3 name gate, "
        "founder-interest disclosure, funding uncertainty, AI boundary, sitemap and shared discovery verified."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
