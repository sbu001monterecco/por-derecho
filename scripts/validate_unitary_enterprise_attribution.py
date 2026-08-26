#!/usr/bin/env python3
"""Validate the 26-Aug attributed-enterprise / RDM-manifest control package."""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTROL_25 = "PD-UNITARY-STATE-20260825-01"
CONTROL_26 = "PD-UNITARY-STATE-20260826-01"
SOURCE_MAIN = "5b1652e00151a3ea2944cd0519cdaf2e04da4453"
PRODUCTION_STATUS_SHA256 = "1a5088a4a5ebafc8dbbb6aa30e5b8459ed4763fa98d4d6b52900b89731c28068"

MANIFEST = ROOT / "publication-manifests/unitary-enterprise-rdm-manifest-analysis-20260826.json"
ADDENDUM = ROOT / "archive/POR_DERECHO_UNITARY_CRIMINAL_ENTERPRISE_POSITION_AND_RDM_MANIFEST_ADDENDUM_26AUG2026.md"
PROMPT = ROOT / "archive/prompts/RDM_PRIVATE_MAILBOX_UNITARY_CRIMINAL_ENTERPRISE_ANALYSIS_PROMPT_26AUG2026.md"
CROSSWALK = ROOT / "archive/knowledge-project/ALLEGATIONS_CROSSWALK_AN2023_DP1901_DP1956_CONTROL24_16AUG2026.md"
RETRIEVAL = ROOT / "archive/knowledge-project/ALLEGATIONS_RETRIEVAL_GATE_16AUG2026.md"
STATE = ROOT / "ops/CURRENT_UNITARY_STATE.json"
STATE_MD = ROOT / "CURRENT_UNITARY_STATE.md"
PRODUCTION_STATUS = ROOT / "ops/PRODUCTION_STATUS.json"
CURRENT_CONTROL_DOCS = (
    "CURRENT_HANDOVER_PROSECUTION_REVERSE_ENGINEERING_21AUG2026.md",
    "CURRENT_PUBLIC_PROSECUTION_SHARPENING_21AUG2026.md",
    "archive/COMUNIDAD_UNITARY_REVERSE_ENGINEERING_PROSECUTION_CRIMINAL_LENSES_PROMPT_18AUG2026.md",
    "archive/CRIMINAL_FIRST_UNITARY_REVERSE_ENGINEERING_2011_TO_PRESENT_25AUG2026.md",
    "archive/EXPRESS_CRIMINAL_ATTRIBUTION_NON_DILUTION_SOURCE_FIDELITY_RULE_23AUG2026.md",
    "archive/POR_DERECHO_UNITARY_CASE_RECONSTRUCTION_MULTIDISCIPLINARY_CRIMINAL_FORENSIC_PROTOCOL_17AUG2026.md",
    "archive/SUN_PARK_UNITARY_REPOSITORY_WEBSITE_REDIGEST_21AUG2026.md",
)

ATTRIBUTION_EN = "one continuing economic-criminal enterprise"
ATTRIBUTION_ES = "una sola empresa continuada de criminalidad económica"


def load_object(path: Path, errors: list[str]) -> dict:
    if not path.is_file():
        errors.append(f"missing {path.relative_to(ROOT)}")
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"invalid JSON {path.relative_to(ROOT)}: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"{path.relative_to(ROOT)}: root must be an object")
        return {}
    return value


def require_markers(path: Path, markers: tuple[str, ...], errors: list[str]) -> str:
    if not path.is_file():
        errors.append(f"missing {path.relative_to(ROOT)}")
        return ""
    text = path.read_text(encoding="utf-8")
    for marker in markers:
        if marker not in text:
            errors.append(f"{path.relative_to(ROOT)}: missing {marker!r}")
    return text


def main() -> int:
    errors: list[str] = []

    manifest = load_object(MANIFEST, errors)
    expected_manifest = {
        "schema": "por-derecho.publication-manifest.v1",
        "publication_id": "unitary-enterprise-rdm-manifest-analysis-20260826",
        "control_id": CONTROL_26,
        "control_date": "2026-08-26",
        "current_state": "PREPARED_PENDING_MERGE",
        "status": "prepared_pending_merge",
        "source_main_sha": SOURCE_MAIN,
        "publication_merge_sha": None,
        "pages_run_id": None,
        "live_verification": "pending",
    }
    for key, expected in expected_manifest.items():
        if manifest.get(key) != expected:
            errors.append(f"manifest {key}: expected {expected!r}, got {manifest.get(key)!r}")

    allegation = manifest.get("controlling_allegation") or {}
    if allegation.get("id") != "ALG-ENT-018":
        errors.append("manifest does not control ALG-ENT-018")
    if ATTRIBUTION_EN not in str(allegation.get("english", "")) or ATTRIBUTION_ES not in str(allegation.get("spanish", "")):
        errors.append("manifest bilingual attributed-enterprise formulation is incomplete")
    for key in ("not_a_finding", "independent_of_rdm_manifest"):
        if allegation.get(key) is not True:
            errors.append(f"manifest allegation safeguard is not true: {key}")
    if allegation.get("rdm_manifest_evidential_support") != "NONE_UNTIL_RELEVANT_NATIVES_ARE_ACQUIRED_AUTHENTICATED_AND_TESTED":
        errors.append("manifest improperly gives the RDM index evidential support")

    statutory = manifest.get("statutory_boundaries") or {}
    if statutory.get("criminal_organisation_cp_570_bis") != "SEPARATE_ELEMENT_SPECIFIC_QUESTION":
        errors.append("CP 570 bis boundary missing")
    if statutory.get("criminal_group_cp_570_ter") != "SEPARATE_RESIDUAL_ALTERNATIVE":
        errors.append("CP 570 ter boundary missing")
    if statutory.get("retired_autonomous_theory") != "ALG-ORG-011":
        errors.append("retired ALG-ORG-011 boundary missing")

    private = manifest.get("private_source") or {}
    for key, expected in {
        "public_alias": "RDM-PRIVATE-MAILBOX-01",
        "received_package_class": "MANIFEST_WORKBOOK_ONLY",
        "phase_a": "PUBLIC_SAFE_MANIFEST_TRIAGE_COMPLETE",
        "phase_b": "NATIVE_EMAIL_ATTACHMENT_AND_DRIVE_ACQUISITION_AND_ANALYSIS_OPEN",
        "temporary_status_for_decisive_unacquired_sources": "NOT YET TESTABLE FROM MANIFEST",
    }.items():
        if private.get(key) != expected:
            errors.append(f"manifest private-source boundary mismatch: {key}")
    denominators = private.get("public_safe_approximate_denominators") or {}
    if not denominators or not all(isinstance(value, str) for value in denominators.values()):
        errors.append("public denominator values must be coarse strings, never exact numeric fields")
    if not isinstance(denominators.get("actor_or_address_rows"), str) or "hundreds" not in denominators.get("actor_or_address_rows", "").lower():
        errors.append("actor/address denominator is not coarsened to hundreds")
    if len(private.get("not_delivered", [])) < 5:
        errors.append("manifest does not preserve the native-source acquisition gap")

    addendum_text = require_markers(
        ADDENDUM,
        (
            "ALG-ENT-018",
            "one continuing economic-criminal enterprise",
            "successive adoption and divided functions",
            "PARTY ALLEGATION / PROSECUTORIAL-INVESTIGATIVE MODEL",
            "CP 570 bis",
            "CP 570 ter",
            "does not reactivate",
            "adds **no evidential support to `ALG-ENT-018`**",
            "NOT YET TESTABLE FROM MANIFEST",
            "Por Derecho bears the evidential burden",
        ),
        errors,
    )
    prompt_text = require_markers(
        PROMPT,
        (
            "PUBLIC-SAFE MASTER PROMPT / MANIFEST-ONLY PHASE A PREPARED / NATIVE PHASE B OPEN",
            "ALG-ENT-018",
            "one continuing economic-criminal enterprise",
            "successive adoption and divided functions",
            "NOT YET TESTABLE FROM MANIFEST",
            "CP 570 bis",
            "CP 570 ter",
            "Por Derecho bears",
            "lead, investigation, accusation, trial and conviction",
        ),
        errors,
    )
    crosswalk_text = require_markers(
        CROSSWALK,
        (
            "### ALG-ENT-018",
            "ACTIVE CURRENT PARTY ALLEGATION / FACTUAL AND PROSECUTORIAL CASE THEORY",
            "successive adoption and divided functions",
            "do not retroactively create authorship, participation or complicity under Articles 28–29 CP",
            "### ALG-ORG-011",
            "SUPERSEDED AS AUTONOMOUS 2026 THEORY",
            "This retirement does not dilute or contradict `ALG-ENT-018`",
        ),
        errors,
    )
    retrieval_text = require_markers(
        RETRIEVAL,
        (
            "Mandatory `ALG-ENT-018` boundary",
            "reason to fragment or dilute `ALG-ENT-018`",
            "manifest is independent discovery metadata and adds no evidential support",
        ),
        errors,
    )
    for relative in (
        "reports/UNITARY_EVIDENCE_DIGEST_24AUG2026.md",
        "reports/2018_PROTECTION_QUESTION_AND_DO_OVER_24AUG2026.md",
    ):
        require_markers(
            ROOT / relative,
            (
                "26 August 2026 supersession notice — current theory",
                "source-bounded assessment",
                "one continuing economic-criminal enterprise",
                "ALG-ENT-018",
            ),
            errors,
        )

    for relative in CURRENT_CONTROL_DOCS:
        control_text = require_markers(
            ROOT / relative,
            (
                "ALG-ENT-018",
                "one continuing economic-criminal enterprise, advanced through successive adoption and divided functions",
                "not a judicial finding",
                "Articles 570 bis/ter CP",
                "Por Derecho bears the evidential burden",
                "adds no evidential support to `ALG-ENT-018`",
                "full private Phase A",
                "native email, attachment and Drive Phase B remain open",
            ),
            errors,
        )
        lowered_control = control_text.lower()
        if "source-bounded" not in lowered_control or "opposite" not in lowered_control:
            errors.append(f"{relative}: dated-ceiling/non-proof-of-opposite boundary missing")

    state = load_object(STATE, errors)
    if state.get("control_id") != CONTROL_25 or state.get("status") != "LIVE_VERIFIED":
        errors.append("last live unitary control must remain 25-Aug LIVE_VERIFIED")
    pending = state.get("pending_material_publication") or {}
    for key, expected in {
        "control_id": CONTROL_26,
        "state": "PREPARED_PENDING_MERGE",
        "source_main_sha": SOURCE_MAIN,
        "publication_manifest": str(MANIFEST.relative_to(ROOT)),
        "repository_latest_material_date": "2026-08-26",
        "live_verification": "PENDING_MERGE_DEPLOYMENT_AND_EXACT_EDGE_READBACK",
    }.items():
        if pending.get(key) != expected:
            errors.append(f"pending unitary state mismatch: {key}")
    material = state.get("material_updates") or {}
    for key, expected in {
        "repository_latest_material_date": "2026-08-26",
        "last_live_verified_material_date": "2026-08-25",
        "public_parity": "2026-08-25_LIVE_VERIFIED_WITH_2026-08-26_PENDING",
    }.items():
        if material.get(key) != expected:
            errors.append(f"unitary material-date split mismatch: {key}")
    require_markers(
        STATE_MD,
        (
            CONTROL_25,
            "LIVE_VERIFIED",
            CONTROL_26,
            "PREPARED_PENDING_MERGE",
            "not yet live",
            "2026-08-25_LIVE_VERIFIED_WITH_2026-08-26_PENDING",
        ),
        errors,
    )

    if not PRODUCTION_STATUS.is_file():
        errors.append("ops/PRODUCTION_STATUS.json is missing")
    elif hashlib.sha256(PRODUCTION_STATUS.read_bytes()).hexdigest() != PRODUCTION_STATUS_SHA256:
        errors.append("ops/PRODUCTION_STATUS.json changed before exact post-merge live verification")

    # Public Git must not contain a private account address, locator, filename,
    # private digest or exact row-count object in this package.  The exclusions
    # may be described generically; actual values must remain outside Git.
    public_control_text = "\n".join((addendum_text, prompt_text, json.dumps(manifest, ensure_ascii=False)))
    if re.search(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b", public_control_text):
        errors.append("private-source control exposes an email address")
    if re.search(r"\b[0-9a-f]{64}\b", public_control_text, re.I):
        errors.append("private-source control exposes a 64-hex digest")
    if re.search(r"https?://(?:drive|mail)\.google\.com", public_control_text, re.I):
        errors.append("private-source control exposes a Gmail/Drive locator")
    if re.search(r'"(?:message|thread|drive_(?:item|file|document))_id"\s*:', public_control_text, re.I):
        errors.append("private-source control exposes a provider locator field")

    # The two historical formulations may appear only to identify the
    # superseded, source-bounded conclusion; current controls must reject them
    # as a present ceiling.
    for text, label in ((addendum_text, "addendum"), (prompt_text, "prompt"), (retrieval_text, "retrieval gate")):
        if "does not define" not in text.lower() and "do not use" not in text.lower() and "must not" not in text.lower():
            errors.append(f"{label}: historical-ceiling non-controlling rule missing")

    if errors:
        print("UNITARY ENTERPRISE ATTRIBUTION CONTROL: FAIL", file=sys.stderr)
        for error in errors:
            print(f" - {error}", file=sys.stderr)
        return 1

    print("UNITARY ENTERPRISE ATTRIBUTION CONTROL: PASS")
    print(" - ALG-ENT-018 active and attributed; ALG-ORG-011 remains retired")
    print(" - manifest-only Phase A separated from native Phase B")
    print(" - 25-Aug live truth preserved; 26-Aug material remains PREPARED_PENDING_MERGE")
    print(" - production observation preserved unchanged")
    print(" - no private account address, locator or digest exposed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
