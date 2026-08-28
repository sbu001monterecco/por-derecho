#!/usr/bin/env python3
"""Validate the deletion-continuity package for the controlled media desk."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
START = ROOT / "CHATGPT_START_HERE.md"
CONTROL = ROOT / "CHATBOT_MEDIA_INQUIRY_DESK_CONTROL_28AUG2026.md"
AUDIT = ROOT / "docs/deletion-audits/2026-08-28-chatbot-media-inquiry-desk-thread-closeout.md"
MANIFEST = ROOT / "publication-manifests/chatbot-media-inquiry-desk-continuity-20260828.json"
VALIDATOR = ROOT / "scripts/validate_chatbot_media_inquiry_desk_continuity.py"

EXPECTED_FILES = {
    str(START.relative_to(ROOT)),
    str(CONTROL.relative_to(ROOT)),
    str(AUDIT.relative_to(ROOT)),
    str(MANIFEST.relative_to(ROOT)),
    str(VALIDATOR.relative_to(ROOT)),
}

REQUIRED_CONTROL_MARKERS = [
    "PD-CHATBOT-MEDIA-DESK-20260828-01",
    "Ask the Record / Pregunta al expediente",
    "controlled digital press desk",
    "Source → Authority → Perimeter → Contradiction → Consequence → Reversibility",
    "Recovery objective and legal-outcome control",
    "must never predict",
    "Judicial-independence qualification",
    "Three independent authorisations",
    "Text and voice flow",
    "Privacy and legal deployment gate",
    "Initial canonical questions",
    "Reconstruction sequence",
    "exact prior prototype: not recovered",
]

REQUIRED_AUDIT_MARKERS = [
    "DELETION-SAFE WITH OPEN IMPLEMENTATION",
    "not represented as recovered",
    "No credential, token or environment value is preserved",
    "does not deploy a chatbot",
    "Open items do not depend on the originating conversation",
]

SECRET_PATTERNS = [
    re.compile(r"sk-(?:proj-)?[A-Za-z0-9_-]{20,}"),
    re.compile(r"OPENAI_API_KEY\s*=\s*\S+"),
]


def main() -> int:
    errors: list[str] = []

    for path in (START, CONTROL, AUDIT, MANIFEST, VALIDATOR):
        if not path.is_file():
            errors.append(f"missing required file: {path.relative_to(ROOT)}")

    if errors:
        return report(errors)

    control = CONTROL.read_text(encoding="utf-8")
    audit = AUDIT.read_text(encoding="utf-8")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    for marker in REQUIRED_CONTROL_MARKERS:
        if marker.casefold() not in control.casefold():
            errors.append(f"control missing marker: {marker}")
    for marker in REQUIRED_AUDIT_MARKERS:
        if marker.casefold() not in audit.casefold():
            errors.append(f"audit missing marker: {marker}")

    if manifest.get("publication_id") != "PD-CHATBOT-MEDIA-DESK-20260828-01":
        errors.append("manifest publication_id mismatch")
    if manifest.get("current_state") not in {"REMOTE_SOURCE", "DELETION_SAFE"}:
        errors.append("manifest current_state must be REMOTE_SOURCE or DELETION_SAFE")
    if set(manifest.get("expected_source_files", [])) != EXPECTED_FILES:
        errors.append("manifest expected_source_files does not match the continuity package")
    if manifest.get("reader_facing_product_release") is not False:
        errors.append("manifest must not claim a reader-facing product release")
    if manifest.get("external_communications_authorized") is not False:
        errors.append("manifest must keep external communications unauthorised")
    if manifest.get("implementation_state", {}).get("exact_prior_prototype") != "NOT_RECOVERED":
        errors.append("manifest must preserve the lost-prototype boundary")
    if manifest.get("implementation_state", {}).get("credential_in_repository") is not False:
        errors.append("manifest must state that no credential is in the repository")

    combined = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (START, CONTROL, AUDIT, MANIFEST, VALIDATOR)
    )
    for pattern in SECRET_PATTERNS:
        if pattern.search(combined):
            errors.append(f"possible credential material matched: {pattern.pattern}")

    if manifest.get("current_state") == "DELETION_SAFE":
        for field in (
            "merge_sha",
            "deployment_evidence",
            "live_urls",
            "live_verification_evidence",
            "deletion_record",
        ):
            if not manifest.get(field):
                errors.append(f"DELETION_SAFE manifest missing {field}")

    return report(errors)


def report(errors: list[str]) -> int:
    if errors:
        print("CHATBOT MEDIA DESK CONTINUITY: FAIL")
        for error in errors:
            print(f" - {error}")
        return 1
    print("CHATBOT MEDIA DESK CONTINUITY: PASS (5 files; no executable release claimed)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
