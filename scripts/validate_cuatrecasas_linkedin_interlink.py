#!/usr/bin/env python3
"""Validate the minimized Cuatrecasas LinkedIn evidence interlink package."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "evidence/cuatrecasas/2026-03-06-inigo-de-luisa-linkedin-message.json"
PANEL = ROOT / "assets/cuatrecasas-inigo-linkedin-record-20260831.js"
SITE_LOADER = ROOT / "assets/site.js"
CUATRE_PAGES = {
    "en": ROOT / "en/cuatrecasas-sun-park/index.html",
    "es": ROOT / "es/cuatrecasas-sun-park/index.html",
}
ICAM_PAGES = {
    "en": ROOT / "en/cuatrecasas-icam-ccacm-2026/index.html",
    "es": ROOT / "es/cuatrecasas-icam-ccacm-2026/index.html",
}


def main() -> int:
    errors: list[str] = []

    try:
        record_text = RECORD.read_text(encoding="utf-8")
        record = json.loads(record_text)
    except Exception as exc:
        print(f"CUATRECASAS LINKEDIN INTERLINK VALIDATION FAILED\n - invalid evidence record: {exc}")
        return 1

    if record.get("record_id") != "CUATRECASAS-LINKEDIN-20260306-INIGO-DE-LUISA":
        errors.append("unexpected evidence record_id")
    if record.get("canonical_person", {}).get("caepr_id") != "PD-SP-P-0049":
        errors.append("canonical person must resolve to PD-SP-P-0049")
    if record.get("date_basis", {}).get("capture_display") != "TODAY":
        errors.append("screenshot-only date limitation is missing")
    if record.get("governance_revision") != "2026-08-31c":
        errors.append("evidence record is not on governance revision 2026-08-31c")

    official_context = record.get("official_context")
    if not isinstance(official_context, list) or len(official_context) != 3:
        errors.append("official context must contain the three controlled procedural records")
    clause_audit = record.get("clause_audit")
    if not isinstance(clause_audit, list) or len(clause_audit) != 10:
        errors.append("machine-readable clause audit must contain ten controlled proposition groups")
    email_findings = record.get("targeted_email_context", {}).get("public_safe_findings")
    if not isinstance(email_findings, list) or len(email_findings) != 9:
        errors.append("targeted email context must contain nine minimized chronology groups")

    captures = record.get("preservation", {}).get("capture_records")
    expected_capture_ids = {
        "CUATRECASAS-LINKEDIN-20260306-INIGO-DE-LUISA.CAPTURE-01",
        "CUATRECASAS-LINKEDIN-20260306-INIGO-DE-LUISA.CAPTURE-02",
    }
    if not isinstance(captures, list) or len(captures) != 2:
        errors.append("exactly two private custody capture records are required")
    else:
        actual_ids = {item.get("evidence_id") for item in captures if isinstance(item, dict)}
        if actual_ids != expected_capture_ids:
            errors.append("capture evidence IDs do not match the controlled pair")
        for item in captures:
            if item.get("custody_status") != "HASH_VERIFIED_PRIVATE_COPY":
                errors.append(f"{item.get('evidence_id')}: custody status is not hash verified")
            if item.get("public_binary") is not False:
                errors.append(f"{item.get('evidence_id')}: raw public binary must remain false")

    forbidden_public_tokens = (
        "IMG-20260306-WA0002",
        "IMG-20260306-WA0003",
        "ANNEX-01_20260306",
        "ANNEX-02_20260306",
        "same_day_preservation_email_subject",
        "later_archive_email_subject",
        "libfile_",
        ".jpg",
    )
    for token in forbidden_public_tokens:
        if token in record_text:
            errors.append(f"public evidence record exposes forbidden private locator token: {token}")

    if record.get("communication_governance", {}).get("direct_contact") != "HOLD_NOT_AUTHORISED":
        errors.append("direct no-contact governance is missing")
    targets = set(record.get("public_page_targets") or [])
    for target in {
        "/en/cuatrecasas-sun-park/#inigo-linkedin-20260306",
        "/es/cuatrecasas-sun-park/#inigo-linkedin-20260306",
        "/en/cuatrecasas-icam-ccacm-2026/",
        "/es/cuatrecasas-icam-ccacm-2026/",
    }:
        if target not in targets:
            errors.append(f"public target missing: {target}")

    panel = PANEL.read_text(encoding="utf-8")
    for marker in (
        "section.id = 'inigo-linkedin-20260306'",
        "cuatrecasas-linkedin-interlink-20260831",
        "../../evidence/cuatrecasas/2026-03-06-inigo-de-luisa-linkedin-message.json",
        "../cuatrecasas-icam-ccacm-2026/",
        "window.location.hash === '#inigo-linkedin-20260306'",
        "section.scrollIntoView",
        "data-governance-revision', '20260831c'",
        "A procedural archive does not answer the professional record",
        "Un archivo procesal no responde al expediente profesional",
        "Every statement, in context",
        "Cada afirmación, en su contexto",
        "No actual third-party dissemination or campaign has been proved.",
        "No se ha probado difusión efectiva a terceros ni una campaña.",
        "This prevents an obstruction-of-venia claim.",
        "Impide afirmar obstrucción de la venia.",
        "delivery bounced or expired",
        "hubo rebotes y expiración",
    ):
        if marker not in panel:
            errors.append(f"panel marker missing: {marker}")
    if "<img" in panel or any(token in panel for token in forbidden_public_tokens[:4]):
        errors.append("panel must not publish or reference the raw screenshots")

    loader = SITE_LOADER.read_text(encoding="utf-8")
    if "cuatrecasas-inigo-linkedin-record-20260831.js?v=20260831c" not in loader:
        errors.append("site loader does not request the cache-busted panel revision")
    if "data-cuatrecasas-inigo-linkedin-loader', '20260831c'" not in loader:
        errors.append("site loader revision marker is missing")

    for lang, path in CUATRE_PAGES.items():
        body = path.read_text(encoding="utf-8")
        if "../../assets/site.js?v=20260831c" not in body:
            errors.append(f"{lang} Cuatrecasas page does not cache-bust the shared loader")
        if "17 Sep / 18 Oct 2024" not in body and "17 sep / 18 oct 2024" not in body:
            errors.append(f"{lang} Cuatrecasas page lacks the source-qualified 2024 ETJ dates")
        if f'../cuatrecasas-icam-ccacm-2026/' not in body:
            errors.append(f"{lang} Cuatrecasas page lacks the general ICAM/CCACM route")

    for lang, path in ICAM_PAGES.items():
        body = path.read_text(encoding="utf-8")
        direct = '../cuatrecasas-sun-park/#inigo-linkedin-20260306'
        if body.count(direct) != 1:
            errors.append(f"{lang} ICAM/CCACM page must contain exactly one proposition-specific link")
        required_boundary = "does not prove the Madrid Bar outcome" if lang == "en" else "no prueba la decisión del Colegio de Madrid"
        if required_boundary not in body:
            errors.append(f"{lang} ICAM/CCACM page lacks the outcome boundary")

    if errors:
        print("CUATRECASAS LINKEDIN INTERLINK VALIDATION FAILED")
        for error in errors:
            print(f" - {error}")
        return 1

    print(
        "CUATRECASAS LINKEDIN INTERLINK VALIDATION PASSED — "
        "2 private capture IDs, 2 bilingual public panels, 10 controlled proposition groups, "
        "9 minimized email chronology groups, 3 procedural records, raw screenshots excluded"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
