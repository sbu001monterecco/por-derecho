#!/usr/bin/env python3
"""Validate the 22-Sep-2026 public-safe institutional recipient projection."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "assets/data/institutional-recipient-forensic-spine-20260922.json"
MANIFEST = ROOT / "publication-manifests/institutional-recipient-forensic-spine-20260922.json"

PAIRS = {
    "google": (
        "en/google-sun-park-evidence-cooperation/index.html",
        "es/google-sun-park-cooperacion-evidencia/index.html",
    ),
    "hub": (
        "en/sun-park-digital-identity-google-mynd/index.html",
        "es/identidad-digital-sun-park-google-mynd/index.html",
    ),
    "lourdes": (
        "en/lourdes-google-mynd-incident/index.html",
        "es/incidente-lourdes-google-mynd/index.html",
    ),
    "pwc": (
        "en/pwc-canarias-carlos-saavedra-sun-park/index.html",
        "es/pwc-canarias-carlos-saavedra-sun-park/index.html",
    ),
    "rsm": (
        "en/rsm/nnr4-1025c2f66/index.html",
        "es/rsm/nnr4-1025c2f66/index.html",
    ),
    "gt": (
        "en/grant-thornton/2024-04/index.html",
        "es/grant-thornton/2024-04/index.html",
    ),
    "aggregate": (
        "en/prosecutorial-professional-evidence-pwc-grant-thornton-rsm/index.html",
        "es/fiscalia-evidencia-profesional-pwc-grant-thornton-rsm/index.html",
    ),
}


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def load_json(path: Path, errors: list[str]) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"cannot parse {path.relative_to(ROOT)}: {exc}", errors)
        return {}
    if not isinstance(value, dict):
        fail(f"{path.relative_to(ROOT)} root is not an object", errors)
        return {}
    return value


def main() -> int:
    errors: list[str] = []
    data = load_json(DATA, errors)
    manifest = load_json(MANIFEST, errors)
    if data.get("control_id") != "PD-IRF-SPINE-20260922-01":
        fail("unexpected forensic-spine control_id", errors)
    if data.get("control_date") != "2026-09-22":
        fail("unexpected forensic-spine control_date", errors)
    entity = data.get("canonical_entity") or {}
    expected_entity = {
        "display_name": "Aweswell Limited",
        "legal_register_literal": "AWESWELL LIMITED",
        "company_number": "07716847",
    }
    for key, value in expected_entity.items():
        if entity.get(key) != value:
            fail(f"canonical entity mismatch: {key}", errors)
    if set(data.get("relation_labels") or {}) != {"DOC", "HIP", "OPEN", "NOTICE", "CONTRARY", "ADVERSE", "GAP"}:
        fail("relation vocabulary drift", errors)
    if len(data.get("spine") or []) != 5:
        fail("forensic spine must contain five controlled nodes", errors)
    if len(data.get("recipients") or []) != 4:
        fail("recipient projection must contain four recipients", errors)
    if manifest.get("publication_id") != "PD-INSTITUTIONAL-RECIPIENT-FORENSIC-SPINE-20260922":
        fail("publication manifest identity drift", errors)
    if manifest.get("current_state") != "PREPARED_PENDING_MERGE":
        fail("prepared manifest must not self-certify deployment", errors)

    expected_pages = {item for pair in PAIRS.values() for item in pair}
    manifest_pages = {
        item
        for language in (manifest.get("expected_routes") or {}).values()
        for item in language
    }
    if expected_pages != manifest_pages:
        fail("manifest page inventory differs from validator inventory", errors)

    texts: dict[str, str] = {}
    for label, pair in PAIRS.items():
        for rel in pair:
            path = ROOT / rel
            if not path.is_file():
                fail(f"missing route: {rel}", errors)
                continue
            text = path.read_text(encoding="utf-8")
            texts[rel] = text
            if 'data-recipient-focus="true"' not in text:
                fail(f"recipient-focus marker missing: {rel}", errors)
            if "recipient-forensic-20260922.css" not in text:
                fail(f"recipient CSS missing: {rel}", errors)
            if re.search(r"\bOswell Limited\b", text, flags=re.IGNORECASE):
                fail(f"uncorrected entity name in {rel}", errors)
        if label in {"google", "hub", "lourdes"} and all(rel in texts for rel in pair):
            en, es = (texts[rel] for rel in pair)
            if 'hreflang="es"' not in en or 'hreflang="en"' not in en:
                fail(f"English hreflang incomplete: {label}", errors)
            if 'hreflang="es"' not in es or 'hreflang="en"' not in es:
                fail(f"Spanish hreflang incomplete: {label}", errors)

    for rel in PAIRS["google"]:
        text = texts.get(rel, "")
        for marker in ("19740425", "24008448", "26176867", "5-5076000032482", "R33"):
            if marker not in text:
                fail(f"Google route missing marker {marker}: {rel}", errors)
        if "Business Profile" not in text and "Perfil de Empresa" not in text:
            fail(f"Google Business lane missing: {rel}", errors)
        if "Google Account" not in text and "Cuenta de Google" not in text:
            fail(f"Google Account lane missing: {rel}", errors)

    broken_asset = "sunpark-digital-identity-evidence-sequence-redacted.jpg"
    for rel in PAIRS["lourdes"]:
        text = texts.get(rel, "")
        if broken_asset in text:
            fail(f"corrupt public derivative remains embedded: {rel}", errors)
        if "PUBLIC_DERIVATIVE_INTEGRITY_FAILED" not in text:
            fail(f"integrity notice missing: {rel}", errors)

    for key in ("pwc", "rsm", "gt", "aggregate"):
        for rel in PAIRS[key]:
            text = texts.get(rel, "")
            for marker in ("22 September 2026", "22 SEPTEMBER 2026", "22 septiembre 2026", "22 SEPTIEMBRE 2026"):
                if marker in text:
                    break
            else:
                fail(f"22-Sep status missing: {rel}", errors)
            if "Aweswell Limited" not in text or "AWESWELL LIMITED" not in text or "07716847" not in text:
                fail(f"canonical entity triad missing: {rel}", errors)
            if "Silence is not admission" not in text and "silence is not admission" not in text and "silencio no es admisión" not in text and "El silencio no es admisión" not in text:
                fail(f"silence boundary missing: {rel}", errors)

    js_files = [
        "assets/ac-loyalty-breakpoint-20260819.js",
        "assets/ac-de-facto-knowing-facilitation-visibility-20260820.js",
        "assets/control-22-24-interlink-20260904.js",
        "assets/hotel-finca-title-system-interlink-20260903.js",
        "assets/matkator-8584-hotel-title-multitrack-20260903.js",
        "assets/dp1901-platform-recovery-nexus-20260920.js",
        "assets/jdam-architecture-colegios-20260820.js",
    ]
    for rel in js_files:
        text = (ROOT / rel).read_text(encoding="utf-8")
        if "recipientFocus" not in text:
            fail(f"recipient-focus injector guard missing: {rel}", errors)

    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    for route in ("/en/google-sun-park-evidence-cooperation/", "/es/google-sun-park-cooperacion-evidencia/"):
        if route not in sitemap:
            fail(f"sitemap route missing: {route}", errors)

    if errors:
        print("INSTITUTIONAL RECIPIENT FORENSIC SPINE: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("INSTITUTIONAL RECIPIENT FORENSIC SPINE: PASS")
    print(f"- bilingual route pairs: {len(PAIRS)}")
    print("- canonical recipient projection: PASS")
    print("- proof-ceiling and public/private boundaries: PASS")
    print("- corrupt derivative withdrawn without deletion/reconstruction: PASS")
    print("- recipient-focus injector guards: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
