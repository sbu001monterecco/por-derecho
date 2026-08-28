#!/usr/bin/env python3
"""Validate the FTI / Meeting Point / RICPE continuity release candidate."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTROL = "PD-FTI-MP-RICPE-CONTINUITY-20260827-01"
CARET_CONTROL = "PD-FTI-MP-RICPE-CARET-20260827-01"
ACTION_CONTROL = "PD-FTI-MP-RICPE-ACTIONS-20260827-01"
PUBLIC_FINGERPRINT = "e53bda34973e530520bde39648768a1e32a358d8984294b21258789faebe6a24"
UUID_RE = re.compile(r"(?<![0-9a-f])[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}(?![0-9a-f])", re.I)

PAGES = {
    "es": ROOT / "es/fti-meeting-point-ricpe-alertador-continuidad/index.html",
    "en": ROOT / "en/fti-meeting-point-ricpe-whistleblower-continuity/index.html",
    "de": ROOT / "de/fti-meeting-point-ricpe-hinweisgeber-kontinuitaet/index.html",
}
CARET_PATH = ROOT / "assets/data/caepr-caret-fti-meeting-point-ricpe-continuity-v1.json"
GRAPH_PATH = ROOT / "assets/data/fti-meeting-point-ricpe-causal-evidence-v1.json"
ACTION_PATH = ROOT / "ops/FTI_MEETING_POINT_RICPE_CROSSBORDER_ACTION_REGISTER_27AUG2026.json"
MANIFEST_PATH = ROOT / "publication-manifests/fti-meeting-point-ricpe-continuity-20260827.json"
PROF_CARET_PATH = ROOT / "assets/data/caepr-caret-fti-meeting-point-professional-institutional-v1.json"
MONITOR_CONTROL_PATH = ROOT / "ops/FTI_MEETING_POINT_CANARY_SPAIN_ASSET_TRANSACTION_MONITOR_CONTROL_27AUG2026.json"
MONITOR_REGISTER_PATH = ROOT / "assets/data/fti-meeting-point-canary-spain-asset-transaction-register-v1.json"
MONITOR_VIEW_PATH = ROOT / "assets/data/fti-meeting-point-canary-capital-control-watch-v1.json"
LIFECYCLE = (
    "DRAFT",
    "PREPARED_PENDING_MERGE",
    "REMOTE_SOURCE",
    "PR_OPEN",
    "CI_GREEN",
    "MERGED",
    "DEPLOYED",
    "LIVE_VERIFIED",
    "DELETION_SAFE",
)
STATUS_BY_STATE = {
    "DRAFT": "not_live",
    "PREPARED_PENDING_MERGE": "release_candidate_not_yet_verified_live",
    "REMOTE_SOURCE": "remote_source_not_merged",
    "PR_OPEN": "pull_request_open_not_merged",
    "CI_GREEN": "pull_request_checks_green_not_merged",
    "MERGED": "merged_awaiting_pages_deployment",
    "DEPLOYED": "deployed_awaiting_exact_live_closeout",
    "LIVE_VERIFIED": "live_verified",
    "DELETION_SAFE": "deletion_safe_live_verified",
}

errors: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def is_full_sha(value: object) -> bool:
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{40}", value) is not None


def load_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"cannot load {path.relative_to(ROOT)}: {exc}")
        return {}
    check(isinstance(value, dict), f"{path.relative_to(ROOT)} root is not an object")
    return value if isinstance(value, dict) else {}


def registry_records() -> dict[str, dict]:
    master = load_json(ROOT / "assets/data/matter-identity-registry-v1.json")
    result: dict[str, dict] = {}
    for part in master.get("parts", []):
        path = ROOT / "assets/data" / str(part.get("path", ""))
        data = load_json(path)
        for record in data.get("records", []):
            rid = record.get("id")
            if isinstance(rid, str):
                check(rid not in result, f"duplicate registry id {rid}")
                result[rid] = record
    return result


def current_files() -> list[Path]:
    try:
        output = subprocess.check_output(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
            cwd=ROOT,
            text=True,
        )
    except Exception as exc:
        errors.append(f"cannot enumerate current files: {exc}")
        return []
    return [ROOT / line for line in output.splitlines() if line]


def run_dedicated_validator(relative_path: str, label: str) -> None:
    result = subprocess.run(
        [sys.executable, relative_path],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        detail = (result.stdout + "\n" + result.stderr).strip()
        errors.append(f"{label} failed: {detail}")


def validate_privacy() -> None:
    run_dedicated_validator("scripts/validate_ricpe_channel_identifier_privacy.py", "binary-aware RICPE privacy validator")
    fingerprint_files = {
        ROOT / "evidence/ricpe-cnmv/2026-08-27/resolution.txt",
        ROOT / "CURRENT_HANDOVER_RICPE_HNT_GC836_TREASURY_21AUG2026.md",
        ROOT / "archive/THREAD_DELETION_AUDIT_CRITICAL_STATUS_UPDATE_21AUG2026.md",
    }
    for path in fingerprint_files:
        text = path.read_text(encoding="utf-8")
        check(PUBLIC_FINGERPRINT in text, f"approved public fingerprint absent from {path.relative_to(ROOT)}")
    for path in current_files():
        try:
            if path.stat().st_size > 8_000_000:
                continue
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for match in UUID_RE.findall(text):
            if hashlib.sha256(match.encode("utf-8")).hexdigest() == PUBLIC_FINGERPRINT:
                errors.append(f"private RICPE communication code exposed in {path.relative_to(ROOT)}")
    resolution = (ROOT / "evidence/ricpe-cnmv/2026-08-27/resolution.txt").read_text(encoding="utf-8")
    check("Correlación pública (SHA-256 del código privado)" in resolution, "resolution lacks privacy-safe correlation label")
    check("Código de comunicación:" not in resolution, "resolution uses prohibited exact-code label")


def validate_caret() -> None:
    data = load_json(CARET_PATH)
    check(data.get("control_id") == CARET_CONTROL, "caret control id mismatch")
    records = data.get("records", [])
    check(isinstance(records, list), "caret records are not a list")
    if not isinstance(records, list):
        return
    check(len(records) == 65, f"caret denominator is {len(records)}, expected 65")
    check([r.get("ordinal") for r in records] == list(range(1, 66)), "caret ordinals are not exactly 1..65")
    check(len({r.get("object_key") for r in records}) == 65, "caret object keys are not unique")
    states = Counter(r.get("state") for r in records)
    check(states == Counter({"CARET_CONFIRMED": 39, "CARET_PENDING": 26}), f"caret state split wrong: {states}")
    types = Counter((r.get("type"), r.get("state")) for r in records)
    expected = Counter({
        ("PERSON", "CARET_CONFIRMED"): 10,
        ("PERSON", "CARET_PENDING"): 2,
        ("ORGANISATION_OR_STRUCTURE", "CARET_CONFIRMED"): 22,
        ("ORGANISATION_OR_STRUCTURE", "CARET_PENDING"): 11,
        ("INSTITUTION_OR_SUBORGAN", "CARET_CONFIRMED"): 5,
        ("INSTITUTION_OR_SUBORGAN", "CARET_PENDING"): 6,
        ("PROCEEDING_OR_FILE", "CARET_CONFIRMED"): 2,
        ("PROCEEDING_OR_FILE", "CARET_PENDING"): 7,
    })
    check(types == expected, f"caret type/state split wrong: {types}")
    registry = registry_records()
    allowed_type = {
        "PERSON": {"PERSON"},
        "ORGANISATION_OR_STRUCTURE": {"ORGANISATION", "STRUCTURE"},
        "INSTITUTION_OR_SUBORGAN": {"INSTITUTION"},
        "PROCEEDING_OR_FILE": {"PROCEEDING"},
    }
    for record in records:
        if record.get("state") == "CARET_CONFIRMED":
            rid = record.get("caepr_id")
            check(isinstance(rid, str) and rid in registry, f"confirmed {record.get('object_key')} lacks valid CAEPR id")
            if isinstance(rid, str) and rid in registry:
                check(registry[rid].get("type") in allowed_type.get(record.get("type"), set()), f"type mismatch for {rid}")
            check("boundary" in record, f"confirmed {record.get('object_key')} lacks identity boundary")
        else:
            check("caepr_id" not in record, f"pending {record.get('object_key')} must not have caepr_id")
            check(bool(record.get("next_source_needed")), f"pending {record.get('object_key')} lacks next_source_needed")
    check(data.get("counts", {}).get("confirmed") == 39, "declared confirmed count mismatch")
    check(data.get("counts", {}).get("pending") == 26, "declared pending count mismatch")
    check("PARTIAL — NOT ALL IS^" in data.get("verdict", ""), "caret verdict missing")


def validate_professional_institutional_caret() -> None:
    run_dedicated_validator(
        "scripts/validate_fti_meeting_point_professional_institutional_caret.py",
        "professional/institutional caret validator",
    )
    data = load_json(PROF_CARET_PATH)
    check(data.get("control_id") == "PD-FTI-MP-PROF-INST-CARET-20260827-01", "professional caret control id mismatch")
    counts = data.get("counts", {})
    check(
        (counts.get("eligible"), counts.get("confirmed"), counts.get("pending"), counts.get("suspended"))
        == (101, 43, 58, 0),
        "professional caret count split is not 101/43/58/0",
    )
    check("PARTIAL — NOT ALL IS^" in str(data.get("verdict", "")), "professional caret verdict missing")


def validate_asset_transaction_monitor() -> None:
    run_dedicated_validator(
        "scripts/validate_fti_meeting_point_asset_transaction_monitor.py",
        "asset-transaction monitor validator",
    )
    control = load_json(MONITOR_CONTROL_PATH)
    register = load_json(MONITOR_REGISTER_PATH)
    view = load_json(MONITOR_VIEW_PATH)
    check(control.get("control_id") == "PD-FTI-MP-ASSET-TX-MONITOR-20260827-01", "monitor control id mismatch")
    check(register.get("control_id") == "PD-FTI-MP-ASSET-TX-REGISTER-20260827-01", "monitor register id mismatch")
    check(control.get("external_action_authorized") is False, "monitor external action must remain false")
    check(len(register.get("heritage_scopes", [])) == 3, "monitor must retain three bounded heritage scopes")
    check(len(register.get("known_entities", [])) == 11, "monitor must retain eleven controlled entity objects")
    check(len(register.get("sources", [])) == 12, "monitor must retain twelve configured public sources")
    check(len(register.get("events", [])) == 2, "monitor must retain two bounded baseline events")
    check(len(register.get("coverage_gaps", [])) == 8, "monitor must retain eight open coverage gaps")
    check(view.get("canonical_register", {}).get("control_id") == register.get("control_id"), "public monitor view is detached from canonical register")


def validate_graph() -> None:
    data = load_json(GRAPH_PATH)
    check(data.get("control_id") == CONTROL, "graph control id mismatch")
    nodes = data.get("nodes", [])
    edges = data.get("edges", [])
    check(len(nodes) == 10, f"graph has {len(nodes)} nodes, expected 10")
    check(len(edges) == 12, f"graph has {len(edges)} edges, expected 12")
    node_ids = {node.get("id") for node in nodes}
    check(node_ids == {f"FMR-N{i:02d}" for i in range(1, 11)}, "graph node IDs incomplete")
    required = {"support", "forward_inference", "reverse_test", "counterevidence", "production"}
    for edge in edges:
        check(edge.get("from") in node_ids and edge.get("to") in node_ids, f"bad endpoints for {edge.get('id')}")
        check(required <= set(edge), f"edge {edge.get('id')} lacks required evidence fields")
    thesis = data.get("thesis", {})
    check("attributed_allegation" in thesis and "proved_limit" in thesis, "graph lacks allegation/proved-limit adjacency")
    check(any("COVID" in value for edge in edges for value in edge.values() if isinstance(value, str)), "graph omits COVID counterevidence")


def validate_actions() -> None:
    data = load_json(ACTION_PATH)
    check(data.get("control_id") == ACTION_CONTROL, "action control id mismatch")
    check(data.get("external_action_authorized") is False, "external action must remain false")
    actions = data.get("actions", [])
    check(len(actions) == 31, f"action count is {len(actions)}, expected 31")
    check([a.get("id") for a in actions] == [f"MPA-{i:03d}" for i in range(1, 32)], "action IDs not exactly MPA-001..031")
    allowed = set(data.get("status_vocabulary", []))
    jurisdictions = Counter(a.get("jurisdiction") for a in actions)
    check({"GERMANY", "SPAIN", "EUROPEAN_UNION", "CROSS_BORDER"} <= set(jurisdictions), "action jurisdictions incomplete")
    for action in actions:
        check(action.get("status") in allowed, f"bad status for {action.get('id')}")
        check(action.get("external_authority") is False, f"external authority not false for {action.get('id')}")
        check(bool(action.get("target")), f"missing target for {action.get('id')}")
    check(len(data.get("package_definitions", {})) == 12, "expected twelve package definitions")
    check("immutable" in data.get("authorization_rule", ""), "action register lacks immutable preview rule")
    by_id = {action.get("id"): action for action in actions}
    check(by_id.get("MPA-027", {}).get("status") == "COMPLETED_VERIFIED", "privacy hotfix action is not completed")
    check(by_id.get("MPA-028", {}).get("package") == "ASSET-TRANSACTION-MONITORING", "monitor action/package missing")
    proceeding_map = data.get("proceeding_file_mapping", [])
    check(len(proceeding_map) == 18, "expected an eighteen-object proceeding/file action map")
    mapped_keys = {item.get("object_key") for item in proceeding_map}
    professional = load_json(PROF_CARET_PATH)
    expected_keys = {
        record.get("object_key")
        for record in professional.get("records", [])
        if record.get("type") == "PROCEEDING_OR_FILE"
    }
    check(mapped_keys == expected_keys, "action register does not map the full professional proceeding/file census")
    for item in proceeding_map:
        check(bool(item.get("boundary")), f"proceeding mapping lacks boundary: {item.get('object_key')}")
        for action_id in item.get("action_ids", []):
            check(action_id in by_id, f"proceeding mapping references unknown action: {action_id}")


def validate_pages() -> None:
    page_texts: dict[str, str] = {}
    for language, path in PAGES.items():
        text = path.read_text(encoding="utf-8")
        page_texts[language] = text
        check(f'data-fmr-control="{CONTROL}"' in text, f"{language} page lacks control marker")
        check(f'data-fmr-language="{language}"' in text, f"{language} page lacks language marker")
        check(len(re.findall(r'data-causal-node="FMR-N\d{2}"', text)) == 10, f"{language} page lacks ten causal nodes")
        check("39/65" in text or "39 of 65" in text or "39 von 65" in text, f"{language} page lacks 39/65 caret result")
        check("43/101" in text or "43 of 101" in text or "43 von 101" in text or "43 de 101" in text, f"{language} page lacks 43/101 professional caret result")
        check("31" in text and ("ACCIONES CONTROLADAS" in text or "CONTROLLED ACTIONS" in text or "KONTROLLIERTE MASSNAHMEN" in text), f"{language} page lacks 31-action marker")
        check("56/130" in text and "25/32" in text and "19/24" in text, f"{language} page merges or omits separate caret scopes")
        check("HOLD" in text, f"{language} page lacks external-action hold")
        check("fti-meeting-point-ricpe-causal-evidence-v1.json" in text, f"{language} page lacks graph link")
        check("caepr-caret-fti-meeting-point-ricpe-continuity-v1.json" in text, f"{language} page lacks caret link")
        check("FTI_MEETING_POINT_RICPE_CROSSBORDER_ACTION_REGISTER_27AUG2026.json" in text, f"{language} page lacks action link")
        check("caepr-caret-fti-meeting-point-professional-institutional-v1.json" in text, f"{language} page lacks professional caret link")
        check("fti-meeting-point-canary-capital-control-watch-v1.json" in text, f"{language} page lacks derived monitor view")
    es = page_texts.get("es", "")
    en = page_texts.get("en", "")
    de = page_texts.get("de", "")
    historic_title = "Alberto López Villarrubia"
    check(historic_title in es and "entonces Juzgado de lo Mercantil n.º 1" in es, "Spanish judicial title is incomplete")
    check(historic_title in en and "entonces Juzgado de lo Mercantil n.º 1" in en, "English page omits controlled historic title")
    check(historic_title in de and "damaligen Juzgado de lo Mercantil n.º 1" in de, "German judicial title is incomplete")
    check("deliberate concealment" not in en.lower(), "English page states deliberate concealment as fact")


def validate_integration() -> None:
    loader = (ROOT / "assets/site-pre-intervencion-highlight-20260820.js").read_text(encoding="utf-8")
    module = (ROOT / "assets/fti-meeting-point-ricpe-continuity-20260827.js").read_text(encoding="utf-8")
    check("fti-meeting-point-ricpe-continuity-20260827.js" in loader, "global loader lacks continuity module")
    check(module.count("/es/") >= 8 and module.count("/en/") >= 8, "inbound module target set is incomplete")
    for route in [
        "es/fti-meeting-point-ricpe-alertador-continuidad/",
        "en/fti-meeting-point-ricpe-whistleblower-continuity/",
        "de/fti-meeting-point-ricpe-hinweisgeber-kontinuitaet/",
        "evidence/ricpe-cnmv/2026-08-27/",
    ]:
        check(route in (ROOT / "sitemap.xml").read_text(encoding="utf-8"), f"main sitemap lacks {route}")
        check(route in (ROOT / "sitemap-meeting-point.xml").read_text(encoding="utf-8"), f"Meeting Point sitemap lacks {route}")
    correction = (ROOT / "archive/CORRECTION_REGISTER.md").read_text(encoding="utf-8")
    missing = (ROOT / "archive/MISSING_EVIDENCE_REGISTER.md").read_text(encoding="utf-8")
    check("CR-112" in correction and "CR-113" in correction, "correction register lacks CR-112/113")
    check("ME-095" in missing, "missing-evidence register lacks ME-095")
    club_es = (ROOT / "es/lava-verde-club-sei-meeting-point/index.html").read_text(encoding="utf-8")
    club_en = (ROOT / "en/lava-verde-club-sei-meeting-point/index.html").read_text(encoding="utf-8")
    for reg in ["REGAGE26e00003492334", "REGAGE26e00003609135", "REGAGE26e00003629560"]:
        check(reg in club_es and reg in club_en, f"Club Sei pages lack {reg}")
    manifest = load_json(MANIFEST_PATH)
    state = manifest.get("current_state")
    check(state in LIFECYCLE and state != "DRAFT", "publication manifest lifecycle state is invalid for the authorised release")
    check(manifest.get("status") == STATUS_BY_STATE.get(state), "publication manifest status does not match lifecycle state")
    check(manifest.get("publication_authorized") is True, "publication manifest lacks repository/website authority")
    authorization = manifest.get("publication_authorization", {})
    check(authorization.get("scope_control_id") == CONTROL, "publication authorization is not bound to this control")
    check(authorization.get("repository_and_website_only") is True, "publication authorization is not repository/website-only")
    check(authorization.get("email_authorized") is False, "publication authorization improperly opens email")
    check(authorization.get("filing_authorized") is False, "publication authorization improperly opens filing")
    check(manifest.get("communication_authorized") is False, "communication authority must remain false")
    check(manifest.get("email_or_filing_action") == "HOLD_NOT_AUTHORISED", "email/filing hold drift")
    check(manifest.get("action_register", {}).get("actions") == 31, "manifest action count drift")
    check(manifest.get("action_register", {}).get("package_definitions") == 12, "manifest package count drift")
    check(manifest.get("professional_institutional_caret_scope", {}).get("denominator") == 101, "manifest professional caret scope missing")
    check(manifest.get("asset_transaction_monitor", {}).get("public_sources") == 12, "manifest monitor scope missing")
    check(is_full_sha(manifest.get("validated_content_commit_sha")), "manifest lacks a real validated content commit SHA")
    if state in LIFECYCLE:
        rank = LIFECYCLE.index(state)
        if rank >= LIFECYCLE.index("MERGED"):
            check(is_full_sha(manifest.get("merge_sha")), f"{state} manifest lacks a full merge SHA")
        if rank >= LIFECYCLE.index("DEPLOYED"):
            deployment = manifest.get("deployment_evidence", {})
            check(deployment.get("workflow") == "pages build and deployment", f"{state} deployment workflow mismatch")
            check(deployment.get("conclusion") == "success", f"{state} Pages deployment was not successful")
            check(isinstance(deployment.get("run_id"), int) and deployment.get("run_id", 0) > 0, f"{state} deployment run id missing")
            check(deployment.get("head_sha") == manifest.get("merge_sha"), f"{state} deployment SHA differs from merge SHA")
        if rank >= LIFECYCLE.index("LIVE_VERIFIED"):
            expected_urls = [
                "https://sbu001monterecco.github.io/por-derecho" + route
                for route in manifest.get("hub_routes", {}).values()
            ]
            check(manifest.get("live_urls") == expected_urls, f"{state} live hub URL set mismatch")
            readback = manifest.get("live_readback", {})
            check(readback.get("result") == "PASS_EXACT_BYTES", f"{state} live readback is not an exact-byte pass")
            check(readback.get("head_sha") == manifest.get("merge_sha"), f"{state} live readback SHA differs from merge SHA")
            hashes = readback.get("sha256_by_route", {})
            check(isinstance(hashes, dict) and len(hashes) >= 15, f"{state} live readback hash map is incomplete")
            for route, digest in hashes.items():
                check(isinstance(route, str) and route.startswith("/"), f"{state} live readback contains an unsafe route")
                check(isinstance(digest, str) and re.fullmatch(r"[0-9a-f]{64}", digest) is not None, f"{state} live route hash invalid")
            closeout = manifest.get("closeout_control", {})
            check(closeout.get("kind") == "SEPARATE_WORKFLOW_ARTIFACT", f"{state} closeout is not separate")
            check(closeout.get("result") == "LIVE_VERIFIED", f"{state} closeout result missing")
            check(closeout.get("head_sha") == manifest.get("merge_sha"), f"{state} closeout SHA differs from merge SHA")
            check(closeout.get("communication_authorized") is False, f"{state} closeout opens communication")
            check(closeout.get("filing_authorized") is False, f"{state} closeout opens filing")
        if state == "DELETION_SAFE":
            check(bool(manifest.get("deletion_record")), "DELETION_SAFE manifest lacks deletion record")


validate_privacy()
validate_caret()
validate_professional_institutional_caret()
validate_graph()
validate_asset_transaction_monitor()
validate_actions()
validate_pages()
validate_integration()

if errors:
    print("FTI / Meeting Point / RICPE continuity validation: FAIL", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print("FTI / Meeting Point / RICPE continuity validation: PASS")
print("- privacy-safe RICPE correlation and zero exact-code exposure")
print("- 10-node / 12-edge multidirectional criminal-first graph")
print("- full finite caret census: 39/65 confirmed; 26 pending; partial")
print("- professional/institutional caret census: 43/101 confirmed; 58 pending; partial")
print("- public-source asset transaction monitor: 3 scopes; 12 sources; no automatic promotion")
print("- 31 cross-border actions and full 18-file/proceeding mapping; all external authority false")
print("- ES/EN/DE hubs, reciprocal loader, sitemaps and canonical registers")
