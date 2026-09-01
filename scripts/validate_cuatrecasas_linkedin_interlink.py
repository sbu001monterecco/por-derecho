#!/usr/bin/env python3
"""Validate the Cuatrecasas LinkedIn evidence, images and reciprocal interlinks."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "evidence/cuatrecasas/2026-03-06-inigo-de-luisa-linkedin-message.json"
PANEL = ROOT / "assets/cuatrecasas-inigo-linkedin-record-20260831.js"
SITE_LOADER = ROOT / "assets/site.js"
IMAGE_MANIFEST = ROOT / "publication-manifests/cuatrecasas-linkedin-image-publication-20260901.json"
IMAGE_CONTROL = ROOT / "archive/CUATRECASAS_LINKEDIN_IMAGE_PUBLICATION_CONTROL_01SEP2026.md"
PUBLIC_CAPTURES = {
    "CUATRECASAS-LINKEDIN-20260306-INIGO-DE-LUISA.CAPTURE-01": {
        "path": ROOT / "assets/evidence/cuatrecasas/inigo-de-luisa-linkedin-message-20260306-capture-01.jpg",
        "public_asset": "/assets/evidence/cuatrecasas/inigo-de-luisa-linkedin-message-20260306-capture-01.jpg",
        "sha256": "ddf86dfe42a0cfa8d4481a6e504c4dc94a63e48c2ce7cb98ec764fa20cb25102",
        "byte_size": 151680,
        "dimensions": (921, 2048),
    },
    "CUATRECASAS-LINKEDIN-20260306-INIGO-DE-LUISA.CAPTURE-02": {
        "path": ROOT / "assets/evidence/cuatrecasas/inigo-de-luisa-linkedin-message-20260306-capture-02.jpg",
        "public_asset": "/assets/evidence/cuatrecasas/inigo-de-luisa-linkedin-message-20260306-capture-02.jpg",
        "sha256": "baefb00dc12914aef4c32f0b69bd63842b15f4d83860a254294900a3822d2aab",
        "byte_size": 138006,
        "dimensions": (921, 2048),
    },
}
CUATRE_PAGES = {
    "en": ROOT / "en/cuatrecasas-sun-park/index.html",
    "es": ROOT / "es/cuatrecasas-sun-park/index.html",
}
ICAM_PAGES = {
    "en": ROOT / "en/cuatrecasas-icam-ccacm-2026/index.html",
    "es": ROOT / "es/cuatrecasas-icam-ccacm-2026/index.html",
}


def jpeg_dimensions(data: bytes) -> tuple[int, int] | None:
    """Return JPEG width and height from a start-of-frame segment."""
    if not data.startswith(b"\xff\xd8"):
        return None
    offset = 2
    start_of_frame = {
        0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
        0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF,
    }
    while offset + 4 <= len(data):
        if data[offset] != 0xFF:
            offset += 1
            continue
        while offset < len(data) and data[offset] == 0xFF:
            offset += 1
        if offset >= len(data):
            return None
        marker = data[offset]
        offset += 1
        if marker in {0x01, *range(0xD0, 0xD9)}:
            continue
        if offset + 2 > len(data):
            return None
        length = int.from_bytes(data[offset:offset + 2], "big")
        if length < 2 or offset + length > len(data):
            return None
        if marker in start_of_frame and length >= 7:
            height = int.from_bytes(data[offset + 3:offset + 5], "big")
            width = int.from_bytes(data[offset + 5:offset + 7], "big")
            return width, height
        offset += length
    return None


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
    if record.get("governance_revision") != "2026-09-01a":
        errors.append("evidence record is not on governance revision 2026-09-01a")
    if record.get("image_publication_authorized") != "2026-09-01":
        errors.append("image publication authority date is missing")

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
        errors.append("exactly two controlled public capture records are required")
    else:
        actual_ids = {item.get("evidence_id") for item in captures if isinstance(item, dict)}
        if actual_ids != expected_capture_ids:
            errors.append("capture evidence IDs do not match the controlled pair")
        for item in captures:
            evidence_id = item.get("evidence_id")
            expected = PUBLIC_CAPTURES.get(evidence_id)
            if expected is None:
                continue
            if item.get("custody_status") != "HASH_VERIFIED_PUBLIC_COPY":
                errors.append(f"{evidence_id}: custody status is not a hash-verified public copy")
            if item.get("public_binary") is not True:
                errors.append(f"{evidence_id}: authorized public binary flag must be true")
            if item.get("public_asset") != expected["public_asset"]:
                errors.append(f"{evidence_id}: controlled public asset path mismatch")
            if item.get("sha256") != expected["sha256"]:
                errors.append(f"{evidence_id}: record SHA-256 mismatch")
            if item.get("byte_size") != expected["byte_size"]:
                errors.append(f"{evidence_id}: record byte size mismatch")
            dimensions = item.get("pixel_dimensions") or {}
            if (dimensions.get("width"), dimensions.get("height")) != expected["dimensions"]:
                errors.append(f"{evidence_id}: record dimensions mismatch")
            if item.get("publication_authority") != "CURRENT_USER_AUTHORISED_2026-09-01":
                errors.append(f"{evidence_id}: publication authority marker missing")

    for evidence_id, expected in PUBLIC_CAPTURES.items():
        path = expected["path"]
        if not path.is_file():
            errors.append(f"{evidence_id}: public JPEG is missing")
            continue
        data = path.read_bytes()
        if len(data) != expected["byte_size"]:
            errors.append(f"{evidence_id}: public JPEG byte size changed")
        if hashlib.sha256(data).hexdigest() != expected["sha256"]:
            errors.append(f"{evidence_id}: public JPEG SHA-256 changed")
        if jpeg_dimensions(data) != expected["dimensions"]:
            errors.append(f"{evidence_id}: public JPEG dimensions changed")

    forbidden_public_tokens = (
        "IMG-20260306-WA0002",
        "IMG-20260306-WA0003",
        "ANNEX-01_20260306",
        "ANNEX-02_20260306",
        "same_day_preservation_email_subject",
        "later_archive_email_subject",
        "libfile_",
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
        "cuatrecasas-linkedin-images-20260901",
        "data-public-capture-count=\"2\"",
        "inigo-de-luisa-linkedin-message-20260306-capture-01.jpg",
        "inigo-de-luisa-linkedin-message-20260306-capture-02.jpg",
        "../../evidence/cuatrecasas/2026-03-06-inigo-de-luisa-linkedin-message.json",
        "../cuatrecasas-icam-ccacm-2026/",
        "window.location.hash === '#inigo-linkedin-20260306'",
        "section.scrollIntoView",
        "data-governance-revision', '20260901a'",
        "The captures, not only the transcript",
        "Las capturas, no sólo la transcripción",
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
    if panel.count("<img ") != 2:
        errors.append("panel must render exactly two controlled screenshot images")
    if any(token in panel for token in forbidden_public_tokens[:4]):
        errors.append("panel exposes a received private filename or locator")

    loader = SITE_LOADER.read_text(encoding="utf-8")
    if "cuatrecasas-inigo-linkedin-record-20260831.js?v=20260901a" not in loader:
        errors.append("site loader does not request the cache-busted panel revision")
    if "data-cuatrecasas-inigo-linkedin-loader', '20260901a'" not in loader:
        errors.append("site loader revision marker is missing")

    for lang, path in CUATRE_PAGES.items():
        body = path.read_text(encoding="utf-8")
        if "../../assets/site.js?v=20260901a" not in body:
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

    try:
        image_manifest = json.loads(IMAGE_MANIFEST.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"invalid image-publication manifest: {exc}")
    else:
        if image_manifest.get("publication_id") != "cuatrecasas-linkedin-image-publication-20260901":
            errors.append("unexpected image-publication manifest ID")
        custody = image_manifest.get("evidence_custody") or {}
        if custody.get("public_capture_count") != 2 or custody.get("raw_screenshots_public") is not True:
            errors.append("image-publication manifest must declare two authorized public captures")
        if image_manifest.get("authority", {}).get("raw_screenshot_publication") != "AUTHORISED_2026-09-01_EXACT_TWO_CAPTURES_ONLY":
            errors.append("image-publication manifest authority is missing or overbroad")

    control_text = IMAGE_CONTROL.read_text(encoding="utf-8") if IMAGE_CONTROL.is_file() else ""
    for marker in (
        "exact two supplied screenshot copies",
        "does not prove deletion, blocking, deactivation or moderation",
        "do not prove the Madrid Bar outcome",
        "No email, message, filing or third-party contact is authorised",
    ):
        if marker not in control_text:
            errors.append(f"image-publication control marker missing: {marker}")

    if errors:
        print("CUATRECASAS LINKEDIN INTERLINK VALIDATION FAILED")
        for error in errors:
            print(f" - {error}")
        return 1

    print(
        "CUATRECASAS LINKEDIN INTERLINK VALIDATION PASSED — "
        "2 hash-verified public captures, 2 bilingual public panels, 10 controlled proposition groups, "
        "9 minimized email chronology groups, 3 procedural records and exact image-publication authority"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
