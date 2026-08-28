#!/usr/bin/env python3
"""Validate the 26-Aug attributed-enterprise / RDM-manifest control package."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTROL_26 = "PD-UNITARY-STATE-20260826-01"
SOURCE_MAIN = "5b1652e00151a3ea2944cd0519cdaf2e04da4453"
MERGE_SHA = "77e2ba300af45a953947160af63283a64512e876"
TREE_SHA = "4f0ac26c5548ae44c68933306c68165cbb6c973e"
PAGES_RUN_ID = 32942972472
PAGES_RUN_NUMBER = 1128
PAGES_COMPLETED_AT = "2026-08-26T07:29:45Z"
VERIFIER_RUN_ID = 32942975508
VERIFIER_RUN_NUMBER = 4
VERIFIER_JOB_ID = 98097657687
VERIFIER_COMPLETED_AT = "2026-08-26T07:29:55Z"

MANIFEST = ROOT / "publication-manifests/unitary-enterprise-rdm-manifest-analysis-20260826.json"
ADDENDUM = ROOT / "archive/POR_DERECHO_UNITARY_CRIMINAL_ENTERPRISE_POSITION_AND_RDM_MANIFEST_ADDENDUM_26AUG2026.md"
PROMPT = ROOT / "archive/prompts/RDM_PRIVATE_MAILBOX_UNITARY_CRIMINAL_ENTERPRISE_ANALYSIS_PROMPT_26AUG2026.md"
CROSSWALK = ROOT / "archive/knowledge-project/ALLEGATIONS_CROSSWALK_AN2023_DP1901_DP1956_CONTROL24_16AUG2026.md"
RETRIEVAL = ROOT / "archive/knowledge-project/ALLEGATIONS_RETRIEVAL_GATE_16AUG2026.md"
STATE = ROOT / "ops/CURRENT_UNITARY_STATE.json"
STATE_MD = ROOT / "CURRENT_UNITARY_STATE.md"
MATERIAL_UPDATES = ROOT / "assets/data/material-updates-v1.json"
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
        "current_state": "LIVE_VERIFIED",
        "status": "live_verified",
        "source_main_sha": SOURCE_MAIN,
        "merge_sha": MERGE_SHA,
        "publication_merge_sha": MERGE_SHA,
        "publication_tree_sha": TREE_SHA,
        "pages_run_id": PAGES_RUN_ID,
        "live_verification": "passed_exact_no_cache",
    }
    for key, expected in expected_manifest.items():
        if manifest.get(key) != expected:
            errors.append(f"manifest {key}: expected {expected!r}, got {manifest.get(key)!r}")

    deployment_evidence = manifest.get("deployment_evidence") or {}
    for key, expected in {
        "pages_run_id": PAGES_RUN_ID,
        "pages_run_number": PAGES_RUN_NUMBER,
        "head_sha": MERGE_SHA,
        "tree_sha": TREE_SHA,
        "status": "completed",
        "conclusion": "success",
        "completed_at": PAGES_COMPLETED_AT,
    }.items():
        if deployment_evidence.get(key) != expected:
            errors.append(f"manifest deployment evidence mismatch: {key}")
    verifier_evidence = manifest.get("live_verification_evidence") or {}
    for key, expected in {
        "workflow_run_id": VERIFIER_RUN_ID,
        "workflow_run_number": VERIFIER_RUN_NUMBER,
        "job_id": VERIFIER_JOB_ID,
        "head_sha": MERGE_SHA,
        "tree_sha": TREE_SHA,
        "source_publication_sha": MERGE_SHA,
        "status": "completed",
        "conclusion": "success",
        "completed_at": VERIFIER_COMPLETED_AT,
        "verified_url_count": 21,
    }.items():
        if verifier_evidence.get(key) != expected:
            errors.append(f"manifest verifier evidence mismatch: {key}")
    if len(manifest.get("live_urls") or []) != 21:
        errors.append("manifest must preserve the exact 21-URL verification scope")

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
    if state.get("control_id") != CONTROL_26 or state.get("status") != "LIVE_VERIFIED":
        errors.append("current unitary control must be 26-Aug LIVE_VERIFIED")
    repository = state.get("repository") or {}
    for key, expected in {
        "current_main_sha_at_preparation": MERGE_SHA,
        "source_publication_merge_sha": MERGE_SHA,
        "verified_tree_sha": TREE_SHA,
    }.items():
        if repository.get(key) != expected:
            errors.append(f"unitary repository evidence mismatch: {key}")
    promoted = state.get("promoted_material_publication") or {}
    for key, expected in {
        "control_id": CONTROL_26,
        "state": "LIVE_VERIFIED",
        "source_main_sha": SOURCE_MAIN,
        "publication_merge_sha": MERGE_SHA,
        "publication_tree_sha": TREE_SHA,
        "publication_manifest": str(MANIFEST.relative_to(ROOT)),
        "repository_latest_material_date": "2026-08-26",
        "pages_run_id": PAGES_RUN_ID,
        "live_verification_run_id": VERIFIER_RUN_ID,
        "live_verification_job_id": VERIFIER_JOB_ID,
        "live_verification": "EXACT_SHA_DEPLOYMENT_AND_21_URL_NO_CACHE_READBACK_VERIFIED",
    }.items():
        if promoted.get(key) != expected:
            errors.append(f"promoted unitary state mismatch: {key}")
    material_updates = load_object(MATERIAL_UPDATES, errors)
    material = state.get("material_updates") or {}
    repository_latest = material.get("repository_latest_material_date")
    last_live = material.get("last_live_verified_material_date")
    if repository_latest != material_updates.get("latest_material_date"):
        errors.append("unitary material-date parity mismatch: repository_latest_material_date")
    if material.get("latest_material_date") != repository_latest:
        errors.append("unitary material-date parity mismatch: latest_material_date")
    if not isinstance(last_live, str) or not isinstance(repository_latest, str) or last_live > repository_latest:
        errors.append("unitary material-date parity mismatch: last_live_verified_material_date")
    else:
        expected_parity = (
            f"{repository_latest}_LIVE_VERIFIED"
            if last_live == repository_latest
            else f"REPOSITORY_{repository_latest}_PENDING_PUBLICATION_LAST_LIVE_VERIFIED_{last_live}"
        )
        if material.get("public_parity") != expected_parity:
            errors.append("unitary material-date parity mismatch: public_parity")
    publication = state.get("publication") or {}
    pages = publication.get("last_pages_deployment") or {}
    for key, expected in {
        "sha": MERGE_SHA,
        "tree_sha": TREE_SHA,
        "run_id": PAGES_RUN_ID,
        "run_number": PAGES_RUN_NUMBER,
        "status": "completed",
        "conclusion": "success",
        "completed_at": PAGES_COMPLETED_AT,
    }.items():
        if pages.get(key) != expected:
            errors.append(f"unitary Pages evidence mismatch: {key}")
    readback = publication.get("current_sha_edge_readback") or {}
    for key, expected in {
        "state": "LIVE_VERIFIED",
        "workflow_run_id": VERIFIER_RUN_ID,
        "workflow_run_number": VERIFIER_RUN_NUMBER,
        "job_id": VERIFIER_JOB_ID,
        "head_sha": MERGE_SHA,
        "tree_sha": TREE_SHA,
        "source_publication_sha": MERGE_SHA,
        "completed_at": VERIFIER_COMPLETED_AT,
        "verified_url_count": 21,
        "conclusion": "success",
    }.items():
        if readback.get(key) != expected:
            errors.append(f"unitary readback evidence mismatch: {key}")
    if len(publication.get("live_urls") or []) != 21:
        errors.append("unitary state must preserve the exact 21-URL verification scope")
    state_md_text = require_markers(
        STATE_MD,
        (
            CONTROL_26,
            "LIVE_VERIFIED",
            MERGE_SHA,
            TREE_SHA,
            str(PAGES_RUN_ID),
            str(VERIFIER_RUN_ID),
            str(VERIFIER_JOB_ID),
            "2026-08-26_LIVE_VERIFIED",
        ),
        errors,
    )
    # A later, expressly separate specialist module may legitimately be at a
    # pre-merge lifecycle state.  The regression guard applies to the
    # controlling 26-August unitary-enterprise release above that additive
    # section, not to every independently lifecycle-controlled module recorded
    # in the same restart file.
    controlling_state_text = state_md_text
    if "## 26 August material — live verified" in controlling_state_text:
        controlling_state_text = controlling_state_text.split(
            "## 26 August material — live verified", 1
        )[1]
    controlling_state_text = controlling_state_text.split("\n### ", 1)[0]
    if (
        "PREPARED_PENDING_MERGE" in controlling_state_text
        or "not yet live" in controlling_state_text.lower()
    ):
        errors.append("CURRENT_UNITARY_STATE.md retains a stale pending-publication statement for the controlling unitary-enterprise release")

    production = load_object(PRODUCTION_STATUS, errors)
    if production.get("served_sha") != MERGE_SHA or production.get("source_tree_sha") != TREE_SHA:
        errors.append("production status does not identify the exact promoted merge/tree")
    production_deployment = production.get("deployment") or {}
    if production_deployment.get("workflow_run_id") != PAGES_RUN_ID:
        errors.append("production status Pages run does not match promoted evidence")
    production_verification = production.get("verification") or {}
    if production_verification.get("state") != "LIVE_VERIFIED":
        errors.append("production verification state is not LIVE_VERIFIED")
    if production_verification.get("current_exact_route_content_verification") != "LIVE_VERIFIED_FOR_SERVED_SHA":
        errors.append("production exact-route content verification is not LIVE_VERIFIED")
    specialist = production_verification.get("latest_live_verified_specialist_release") or {}
    for key, expected in {
        "control_id": CONTROL_26,
        "source_publication_sha": MERGE_SHA,
        "source_tree_sha": TREE_SHA,
        "verification_head_sha": MERGE_SHA,
        "pages_run_id": PAGES_RUN_ID,
        "workflow_run_id": VERIFIER_RUN_ID,
        "job_id": VERIFIER_JOB_ID,
        "verified_at": VERIFIER_COMPLETED_AT,
    }.items():
        if specialist.get(key) != expected:
            errors.append(f"production specialist evidence mismatch: {key}")

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
    print(" - 26-Aug merge, Pages deployment and 21-URL exact readback are LIVE_VERIFIED")
    print(f" - repository latest material date: {repository_latest}")
    print(f" - last live-verified material date: {last_live}")
    print(f" - repository/public material parity: {material.get('public_parity')}")
    print(" - no private account address, locator or digest exposed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
