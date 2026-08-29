#!/usr/bin/env python3
"""Validate the complete Concurso 36/2012 linked-continuity control.

This validator keeps publication/release truth separate from evidential closure. It
uses only repository source and fails closed when a required route, source object,
state field or evidential boundary disappears.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
CONTROL = "PD-C36-LINKED-CONTINUITY-20260829-01"
RELEASE_SHA = "0b0423820942cb95f7a98e8d6fc519f6a9482a04"
RELEASE_PR = 1190
RELEASE_PAGES_RUN = 33233442563
PUBLIC_ORIGIN = "https://sbu001monterecco.github.io/por-derecho/"

MANIFEST_PATH = Path("publication-manifests/concurso36-linked-continuity-20260829.json")
REGISTER_PATH = Path("assets/data/concurso36-linked-continuity-20260829-v1.json")
CONTINUE_PATH = Path("CONCURSO36_CONTINUE_HERE.md")
DELETION_PATH = Path("docs/deletion-audits/2026-08-29-concurso36-linked-continuity.md")
SMOKE_PATH = Path("scripts/production_smoke_check.py")

EXPECTED_ROUTES = {
    "en": ["en/insolvency-36-2012-continuity-control/index.html"],
    "es": ["es/concurso-36-2012-control-continuidad/index.html"],
}
EXPECTED_PROCEDURAL_FAMILY = [
    "filing",
    "receipt",
    "opposition",
    "decision",
    "service",
    "clarification_or_reconsideration",
    "appeal",
    "appellate_decision",
    "finality",
    "implementation_or_accounting",
]
EXPECTED_STATE_FIELDS = {
    "CURRENT_MAIN",
    "RELEASE_SHA",
    "SCOPED_VALIDATION",
    "GLOBAL_INTEGRITY",
    "PAGES_DEPLOYMENT",
    "EXACT_ROUTE_READBACK",
    "EVIDENCE_CLOSURE",
    "DELETION_SAFE",
}
CANONICAL_HASHES = {
    "archive/MISSING_EVIDENCE_REGISTER_CONCURSO36_DECISION_CONTINUITY_ADDENDUM_28AUG2026.md":
        "6e4351dec0516c4908d57f22fbd0ccade66ba80d2b17080a6ea6807fb536ff2c",
    "archive/CONCURSO_36_2012_DOCKET_WIDE_DISCOVERY_PROMOTION_REGISTER_17AUG2026.md":
        "d804bd43373fb24004ac41fe6271e4ed626e0e454f999fded4bf48db1d03552b",
}

errors: list[str] = []
checks = 0


def fail(message: str) -> None:
    errors.append(message)


def check(condition: bool, message: str) -> None:
    global checks
    checks += 1
    if not condition:
        fail(message)


def load_json(rel: Path) -> dict[str, Any]:
    path = ROOT / rel
    if not path.is_file():
        fail(f"missing JSON control: {rel}")
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # pragma: no cover - diagnostic path
        fail(f"invalid JSON in {rel}: {exc}")
        return {}
    if not isinstance(value, dict):
        fail(f"JSON control is not an object: {rel}")
        return {}
    return value


def text(rel: Path) -> str:
    path = ROOT / rel
    if not path.is_file():
        fail(f"missing text control: {rel}")
        return ""
    return path.read_text(encoding="utf-8")


def require_markers(rel: Path, markers: list[str]) -> str:
    value = text(rel)
    for marker in markers:
        check(marker in value, f"{rel}: missing marker {marker!r}")
    check("mailto:" not in value.lower(), f"{rel}: mailto link is not permitted")
    check("tel:" not in value.lower(), f"{rel}: telephone link is not permitted")
    return value


manifest = load_json(MANIFEST_PATH)
register = load_json(REGISTER_PATH)

# Manifest identity, generic publication-integrity fields and release lineage.
check(manifest.get("schema") == "por-derecho.publication-manifest.v1", "manifest schema mismatch")
check(manifest.get("publication_id") == "concurso36-linked-continuity-20260829", "publication_id mismatch")
check(manifest.get("control_id") == CONTROL, "manifest control_id mismatch")
check(manifest.get("owner") == "Por Derecho / Project Sun Rock", "manifest owner mismatch")
check(manifest.get("current_state") in {"DEPLOYED", "LIVE_VERIFIED", "DELETION_SAFE"}, "manifest release state is not a truthful post-merge state")
check(manifest.get("publication_origin") == PUBLIC_ORIGIN, "publication origin mismatch")
check(manifest.get("expected_routes") == EXPECTED_ROUTES, "manifest bilingual route declaration changed")
check(manifest.get("merge_sha") == RELEASE_SHA, "immutable release SHA mismatch")

release = manifest.get("release_lineage") or {}
check(release.get("pull_request_number") == RELEASE_PR, "release PR number mismatch")
check(release.get("release_sha") == RELEASE_SHA, "release lineage SHA mismatch")
check(release.get("pages_run_id") == RELEASE_PAGES_RUN, "release Pages run mismatch")
check(release.get("pages_conclusion") == "success", "release Pages conclusion is not success")

deployment = manifest.get("deployment_evidence") or {}
check(deployment.get("provider") == "GitHub Pages", "deployment provider mismatch")
check(deployment.get("run_id") == RELEASE_PAGES_RUN, "deployment evidence run mismatch")
check(deployment.get("sha") == RELEASE_SHA, "deployment evidence SHA mismatch")
check(deployment.get("conclusion") == "success", "deployment evidence is not successful")

state_control = manifest.get("state_control") or {}
check(set(state_control) == EXPECTED_STATE_FIELDS, "manifest must expose exactly the eight independent state fields")
check(state_control.get("CURRENT_MAIN") == "RESOLVE_AT_RUNTIME", "CURRENT_MAIN must be resolved at runtime")
check(state_control.get("RELEASE_SHA") == RELEASE_SHA, "state-control release SHA mismatch")
check(str(state_control.get("EVIDENCE_CLOSURE", "")).startswith("OPEN_"), "evidential closure must remain open")
if manifest.get("current_state") != "DELETION_SAFE":
    check(state_control.get("DELETION_SAFE") == "NO", "deletion safety must remain withheld before closeout")

controlled = manifest.get("controlled_result") or {}
check(controlled.get("new_evidence_promoted") is False, "manifest must state no new evidence promoted")
check(controlled.get("p0_evidence_gates_open") == 9, "manifest P0 count changed")
check(controlled.get("p1_evidence_gates_open") == 2, "manifest P1 count changed")
check(controlled.get("certified_docket_obtained") is False, "manifest overclaims certified docket")
check(controlled.get("complete_ac_report_series_obtained") is False, "manifest overclaims AC report series")

boundaries = manifest.get("evidential_boundaries") or []
check(any("Not located in the controlled corpus does not mean nonexistent" in item for item in boundaries), "nonexistence disclaimer removed")
check(any("Same-date instruments remain distinct" in item for item in boundaries), "same-date non-collapse rule removed")
check(any("Favourable and neutral acts" in item for item in boundaries), "favourable/neutral visibility rule removed")

authority = manifest.get("authority") or {}
for key in ("email", "filing", "authority_contact"):
    check(authority.get(key) is False, f"manifest {key} authority must remain false")
validation = manifest.get("validation") or {}
check(bool(validation.get("commands")), "manifest validation command missing")
check(bool(validation.get("evidence")), "manifest release validation evidence missing")

# Every declared route and source object must exist in Git source.
for language, routes in EXPECTED_ROUTES.items():
    for rel in routes:
        check((ROOT / rel).is_file(), f"missing {language} public route source: {rel}")
for rel in manifest.get("expected_source_files") or []:
    check(isinstance(rel, str) and (ROOT / rel).is_file(), f"missing manifest-declared source file: {rel!r}")

# Immutable canonical source equivalence is recomputed rather than trusted.
manifest_sources = {
    item.get("path"): item
    for item in (manifest.get("source_equivalence") or {}).get("files", [])
    if isinstance(item, dict)
}
for rel, expected_hash in CANONICAL_HASHES.items():
    path = ROOT / rel
    check(path.is_file(), f"canonical source missing: {rel}")
    if path.is_file():
        actual_hash = hashlib.sha256(path.read_bytes()).hexdigest()
        check(actual_hash == expected_hash, f"canonical source hash changed: {rel}: {actual_hash}")
        declared = manifest_sources.get(rel) or {}
        check(declared.get("sha256") == expected_hash, f"manifest source hash mismatch: {rel}")
        check(declared.get("equivalence") == "BYTE_IDENTICAL_TO_MAIN", f"source equivalence weakened: {rel}")

# Machine register denominator, family structure and governance boundaries.
check(register.get("schema") == "por-derecho.linked-continuity-register.v1", "machine register schema mismatch")
check(register.get("control_id") == CONTROL, "machine register control_id mismatch")
check(register.get("release_type") == "continuity_reconciliation_no_new_evidence_promotion", "machine register release type changed")
check(register.get("source_equivalence", {}).get("result") == "EXACT_MATCH__CANONICAL_MAIN_COPIES_CONTROL", "machine source-equivalence control missing")
check(register.get("procedural_family") == EXPECTED_PROCEDURAL_FAMILY, "procedural family changed or fragmented")

open_gates = register.get("open_evidence_gates") or {}
p0 = open_gates.get("P0") or []
p1 = open_gates.get("P1") or []
check(len(p0) == 9, "expected exactly nine P0 evidence gates")
check(len(p1) == 2, "expected exactly two P1 evidence gates")
for priority, gates in (("P0", p0), ("P1", p1)):
    ids = [gate.get("id") for gate in gates if isinstance(gate, dict)]
    check(len(ids) == len(gates), f"{priority} contains a non-object gate")
    check(len(set(ids)) == len(ids), f"{priority} gate IDs are not unique")
    for gate in gates:
        if not isinstance(gate, dict):
            continue
        check(all(str(gate.get(key, "")).strip() for key in ("id", "family", "missing", "closure")), f"{priority} gate is incomplete: {gate.get('id')!r}")

check(len(register.get("same_date_controls") or []) >= 5, "same-date controls were reduced")
workstreams = register.get("workstreams") or []
check(len(workstreams) >= 10, "linked workstream queue was unexpectedly reduced")
check(all(isinstance(item, dict) and item.get("id") and item.get("next_action") for item in workstreams), "workstream queue contains an incomplete item")
check(register.get("legacy_pr_default") == "COMPARE_CURRENT_MAIN__TRANSPLANT_ONLY__NO_WHOLESALE_MERGE", "legacy-PR transplant gate weakened")
check(register.get("private_counsel_material") == "EXCLUDE_FROM_PUBLIC_RELEASE", "private-counsel exclusion weakened")
check(register.get("unrelated_matters") == "EXCLUDE", "unrelated-matter exclusion weakened")
check(register.get("external_action_authorized") is False, "machine register must not authorise external action")

# Bilingual public copy must distinguish operational control from evidence and cross-link the dossier.
en_page = require_markers(
    Path(EXPECTED_ROUTES["en"][0]),
    [
        "Continuation control reconciled; evidential closure remains open.",
        'data-c36-continuity-truth="20260829"',
        "Operational control and evidential record are distinct",
        "../insolvency-36-2012-orders-decisions/",
        "Not located in the controlled corpus does not mean that the document does not exist.",
        "filing → receipt → opposition → decision",
        "No new evidence promoted",
    ],
)
es_page = require_markers(
    Path(EXPECTED_ROUTES["es"][0]),
    [
        "Control de continuidad conciliado; el cierre probatorio sigue abierto.",
        'data-c36-continuity-truth="20260829"',
        "El control operativo y el expediente probatorio son distintos",
        "../concurso-36-2012-autos-resoluciones/",
        "No localizado en el corpus controlado no significa que el documento no exista.",
        "escrito → recepción → oposición → resolución",
        "Sin nueva prueba promovida",
    ],
)
check("../../es/concurso-36-2012-control-continuidad/" in en_page, "English route lacks reciprocal Spanish link")
check("../../en/insolvency-36-2012-continuity-control/" in es_page, "Spanish route lacks reciprocal English link")
for field in EXPECTED_STATE_FIELDS:
    check(field in en_page, f"English route missing state field {field}")
    check(field in es_page, f"Spanish route missing state field {field}")

# Restart and deletion controls must carry the same eight-state model.
continue_text = text(CONTINUE_PATH)
for field in EXPECTED_STATE_FIELDS:
    check(field in continue_text, f"restart pointer missing state field {field}")
for marker in (CONTROL, RELEASE_SHA, str(RELEASE_PAGES_RUN), PUBLIC_ORIGIN, "Resolve `refs/heads/main` afresh"):
    check(marker in continue_text, f"restart pointer missing lineage marker {marker!r}")

audit_text = text(DELETION_PATH)
for marker in (CONTROL, RELEASE_SHA, str(RELEASE_PAGES_RUN), "nine P0", "two P1", "no unique source or operative instruction survives only in this chat"):
    check(marker in audit_text, f"deletion audit missing marker {marker!r}")
if manifest.get("current_state") != "DELETION_SAFE":
    check("NOT DELETION-SAFE" in audit_text, "deletion audit must remain explicitly not deletion-safe")

# Smoke test must follow the current delegated loader rather than obsolete scripts.
smoke_text = text(SMOKE_PATH)
for marker in (
    "site-pre-treasury-154-hq-20260828.js?v=20260828a",
    "treasury-154-hq-visual-20260828.js?v=20260828c",
    "data-pre-treasury-154-site-loader",
):
    check(marker in smoke_text, f"production smoke missing current loader marker {marker!r}")
check("site-pre-intervencion-highlight-20260820.js?v=20260824e" not in smoke_text, "production smoke still requires superseded loader marker")
check("intervencion-protected-assets-highlight-20260820.js?v=20260820a" not in smoke_text, "production smoke still requires superseded protected-assets marker")

# Sitemap and master prompt remain part of the controlled publication architecture.
sitemap = ROOT / "sitemap-concurso36-court-orders.xml"
check(sitemap.is_file(), "court-orders sitemap missing")
if sitemap.is_file():
    try:
        tree = ET.parse(sitemap)
        locs = {
            node.text
            for node in tree.findall(
                "{http://www.sitemaps.org/schemas/sitemap/0.9}url/"
                "{http://www.sitemaps.org/schemas/sitemap/0.9}loc"
            )
        }
        required_locs = {
            PUBLIC_ORIGIN + "en/insolvency-36-2012-continuity-control/",
            PUBLIC_ORIGIN + "es/concurso-36-2012-control-continuidad/",
        }
        check(required_locs.issubset(locs), "continuity routes missing from court-orders sitemap")
    except ET.ParseError as exc:
        fail(f"invalid sitemap XML: {exc}")

prompt = text(Path("archive/MASTER_CONTINUATION_PROMPT_CONCURSO36_AND_LINKED_THREADS_29AUG2026.md"))
for marker in (
    "WORKBOOK OR REFERENCE → LOCATE SOURCE",
    "Never merge an old branch wholesale",
    "Not authorised:",
    "private counsel identities, advice or drafts",
    "Never substitute rhetorical completion for evidential completion.",
):
    check(marker in prompt, f"master continuation prompt missing control {marker!r}")

if errors:
    print(f"FAIL — Concurso 36/2012 linked continuity ({len(errors)} errors; {checks} checks)")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)

print(f"PASS — Concurso 36/2012 linked continuity ({checks} checks)")
print(" - immutable PR #1190 release and Pages lineage recorded")
print(" - mutable current main is independently resolved at runtime")
print(" - exact canonical source hashes preserved")
print(" - nine P0 and two P1 evidence gates remain explicit")
print(" - bilingual control routes cross-link the substantive dossier")
print(" - current delegated loader contract replaces obsolete smoke markers")
print(" - no new evidence promotion and no external action authority")
