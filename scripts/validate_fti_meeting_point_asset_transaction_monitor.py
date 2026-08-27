#!/usr/bin/env python3
"""Validate the FTI / Meeting Point Spanish asset-transaction monitor."""

from __future__ import annotations

import importlib.util
import json
import py_compile
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
CONTROL_PATH = ROOT / "ops/FTI_MEETING_POINT_CANARY_SPAIN_ASSET_TRANSACTION_MONITOR_CONTROL_27AUG2026.json"
REGISTER_PATH = ROOT / "assets/data/fti-meeting-point-canary-spain-asset-transaction-register-v1.json"
SCHEMA_PATH = ROOT / "assets/data/fti-meeting-point-canary-spain-asset-transaction-monitor-schema-v1.json"
MONITOR_PATH = ROOT / "scripts/monitor_fti_meeting_point_asset_transactions.py"
WORKFLOW_PATH = ROOT / ".github/workflows/monitor-fti-meeting-point-asset-transactions.yml"
CARET_CENSUS_PATH = ROOT / "assets/data/caepr-caret-fti-meeting-point-professional-institutional-v1.json"

CONTROL_ID = "PD-FTI-MP-ASSET-TX-MONITOR-20260827-01"
REGISTER_ID = "PD-FTI-MP-ASSET-TX-REGISTER-20260827-01"
PIN_RE = re.compile(r"uses:\s+[^\s@]+@[a-f0-9]{40}(?:\s|$)")
EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)
UUID_RE = re.compile(r"(?<![0-9a-f])[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}(?![0-9a-f])", re.I)
FINGERPRINT_RE = re.compile(r"^[0-9a-f]{64}$")

errors: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"cannot parse {path.relative_to(ROOT)}: {exc}")
        return {}
    check(isinstance(value, dict), f"{path.relative_to(ROOT)} root is not an object")
    return value if isinstance(value, dict) else {}


def load_registry_records() -> dict[str, dict[str, Any]]:
    master = load_json(ROOT / "assets/data/matter-identity-registry-v1.json")
    records: dict[str, dict[str, Any]] = {}
    for part in master.get("parts", []):
        path = ROOT / "assets/data" / str(part.get("path", ""))
        data = load_json(path)
        for record in data.get("records", []):
            record_id = record.get("id")
            if isinstance(record_id, str):
                check(record_id not in records, f"duplicate CAEPR ID {record_id}")
                records[record_id] = record
    return records


def load_caret_confirmed_records() -> dict[str, dict[str, Any]]:
    census = load_json(CARET_CENSUS_PATH)
    confirmed: dict[str, dict[str, Any]] = {}
    for record in census.get("records", []):
        if record.get("state") == "CARET_CONFIRMED" and isinstance(record.get("caepr_id"), str):
            confirmed[record["caepr_id"]] = record
    return confirmed


def schema_type_matches(value: Any, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "null":
        return value is None
    return False


def resolve_local_ref(root_schema: dict[str, Any], ref: str) -> dict[str, Any] | None:
    if not ref.startswith("#/"):
        errors.append(f"JSON Schema contains unsupported non-local reference: {ref}")
        return None
    value: Any = root_schema
    for raw_part in ref[2:].split("/"):
        part = raw_part.replace("~1", "/").replace("~0", "~")
        if not isinstance(value, dict) or part not in value:
            errors.append(f"JSON Schema reference cannot be resolved: {ref}")
            return None
        value = value[part]
    if not isinstance(value, dict):
        errors.append(f"JSON Schema reference is not an object: {ref}")
        return None
    return value


def validate_json_schema_instance(
    value: Any,
    schema: dict[str, Any],
    root_schema: dict[str, Any],
    path: str = "$",
) -> list[str]:
    """Dependency-free validation for every keyword used by the monitor schema."""
    found: list[str] = []
    if "$ref" in schema:
        resolved = resolve_local_ref(root_schema, str(schema["$ref"]))
        if resolved is None:
            return found
        found.extend(validate_json_schema_instance(value, resolved, root_schema, path))

    expected_type = schema.get("type")
    if expected_type is not None:
        allowed = expected_type if isinstance(expected_type, list) else [expected_type]
        if not any(schema_type_matches(value, str(item)) for item in allowed):
            found.append(f"{path}: expected type {allowed}, found {type(value).__name__}")
            return found
    if "const" in schema and value != schema["const"]:
        found.append(f"{path}: value does not equal schema const {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        found.append(f"{path}: value is outside schema enum")

    if isinstance(value, dict):
        required = schema.get("required", [])
        for key in required:
            if key not in value:
                found.append(f"{path}: missing required property {key}")
        if "maxProperties" in schema and len(value) > int(schema["maxProperties"]):
            found.append(f"{path}: has more than {schema['maxProperties']} properties")
        properties = schema.get("properties", {})
        for key, item in value.items():
            child_path = f"{path}.{key}"
            if key in properties:
                found.extend(validate_json_schema_instance(item, properties[key], root_schema, child_path))
            elif schema.get("additionalProperties") is False:
                found.append(f"{child_path}: additional property is prohibited")
            elif isinstance(schema.get("additionalProperties"), dict):
                found.extend(validate_json_schema_instance(item, schema["additionalProperties"], root_schema, child_path))

    if isinstance(value, list):
        if "minItems" in schema and len(value) < int(schema["minItems"]):
            found.append(f"{path}: has fewer than {schema['minItems']} items")
        if "maxItems" in schema and len(value) > int(schema["maxItems"]):
            found.append(f"{path}: has more than {schema['maxItems']} items")
        if schema.get("uniqueItems"):
            rendered = [json.dumps(item, sort_keys=True, ensure_ascii=False) for item in value]
            if len(rendered) != len(set(rendered)):
                found.append(f"{path}: items are not unique")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(value):
                found.extend(validate_json_schema_instance(item, item_schema, root_schema, f"{path}[{index}]"))

    if isinstance(value, str):
        if "minLength" in schema and len(value) < int(schema["minLength"]):
            found.append(f"{path}: string is shorter than {schema['minLength']}")
        if "pattern" in schema:
            try:
                if re.search(str(schema["pattern"]), value) is None:
                    found.append(f"{path}: string does not match {schema['pattern']}")
            except re.error as exc:
                found.append(f"{path}: invalid schema regular expression: {exc}")
        if schema.get("format") == "date":
            try:
                date.fromisoformat(value)
            except ValueError:
                found.append(f"{path}: string is not an ISO date")
    return found


def validate_control(control: dict[str, Any]) -> None:
    check(control.get("control_id") == CONTROL_ID, "monitor control_id mismatch")
    check(control.get("external_action_authorized") is False, "monitor must not authorize external action")
    scope = control.get("scope", {})
    check(scope.get("prospective_transaction_development_excluded") is True, "prospective transaction development is not excluded")
    check(scope.get("private_source_ingestion_excluded") is True, "private source ingestion is not excluded")
    check(scope.get("website_auto_publication_excluded") is True, "website auto-publication is not excluded")
    check({"CANARY_ISLANDS", "SPAIN"} == set(scope.get("geographies", [])), "geography scope is not exactly Canary Islands and Spain")
    check(len(control.get("source_priority", [])) == 4, "source-priority ladder must have four tiers")
    priorities = [item.get("code") for item in control.get("source_priority", [])]
    check(priorities == ["P1_OFFICIAL", "P2_PARTY_OR_FIDUCIARY", "P3_INDEPENDENT_TRADE", "P4_DISCOVERY"], "source-priority order drift")
    access_lanes = control.get("source_access_lanes", [])
    check(
        [item.get("code") for item in access_lanes] == ["AUTOMATED_SAFE", "MANUAL_PUBLIC", "PAID_OR_RESTRICTED"],
        "source-access lane vocabulary/order drift",
    )
    check(access_lanes and access_lanes[0].get("automated_fetch_permitted") is True, "AUTOMATED_SAFE lane is not fetch-enabled")
    check(all(item.get("automated_fetch_permitted") is False for item in access_lanes[1:]), "manual/restricted access lane enables automated fetch")
    access = control.get("access_safeguards", {})
    check(access.get("automated_lane_only") == "AUTOMATED_SAFE", "automated access is not limited to AUTOMATED_SAFE")
    check(
        {str(item).casefold() for item in access.get("prohibited_request_headers", [])}
        == {"authorization", "cookie", "proxy-authorization"},
        "prohibited request-header set drift",
    )
    check(access.get("credentials_and_authentication_prohibited") is True, "credentialed access is not prohibited")
    check(access.get("captcha_or_session_circumvention_prohibited") is True, "CAPTCHA/session circumvention is not prohibited")
    check(access.get("restricted_or_legitimate_interest_source_auto_fetch_prohibited") is True, "restricted-source automated fetch is not prohibited")
    coverage = control.get("coverage_boundary", {})
    check(coverage.get("status") == "BOUNDED_MONITOR_NOT_COMPREHENSIVE", "control coverage status is not bounded")
    check(coverage.get("configured_heritage_scopes") == 3, "control heritage-scope denominator drift")
    check(coverage.get("configured_public_sources") == 12, "control source denominator drift")
    check(coverage.get("configured_official_source_lanes") == 11, "control official-source-lane denominator drift")
    check(coverage.get("configured_open_gaps") == 8, "control open-gap denominator drift")
    check(coverage.get("unknown_counterparty_extraction") is False, "control implies unknown-counterparty extraction")
    pending_control = control.get("pending_review_and_acknowledgement", {})
    check(pending_control.get("bounded_queue_model") == "ONE_STICKY_REVIEW_WINDOW_PER_SOURCE", "sticky queue is not bounded to one review window per source")
    check(pending_control.get("automatic_acknowledgement") is False, "sticky queue permits automatic acknowledgement")
    check(len(control.get("non_inference_guards", [])) >= 10, "fewer than ten non-inference guards")
    promotion = control.get("promotion_rules", {})
    for field in ["automatic_register_event_creation", "automatic_caret_assignment", "automatic_website_update", "automatic_external_notification"]:
        check(promotion.get(field) is False, f"automatic promotion must remain false: {field}")
    for required in ["asset", "entities_and_capacities", "transaction_date", "source_refs", "evidence_state", "change_detection"]:
        check(required in control.get("event_required_fields", []), f"control event contract lacks {required}")


def validate_register(
    control: dict[str, Any],
    register: dict[str, Any],
    caepr: dict[str, dict[str, Any]],
    caret_confirmed_records: dict[str, dict[str, Any]],
) -> None:
    check(register.get("control_id") == REGISTER_ID, "transaction register control_id mismatch")
    check(register.get("public_safe") is True, "transaction register must be public-safe")
    field_contract = register.get("field_contract", {})
    exact_fields = {"entity", "asset", "capacity", "date", "source", "evidence_state", "change_detection"}
    check(set(field_contract) == exact_fields, "field contract does not contain the exact seven required field definitions")

    entities = register.get("known_entities", [])
    entity_ids = [item.get("entity_id") for item in entities]
    check(len(entities) == 11, f"expected 11 controlled entity objects, found {len(entities)}")
    check(len(entity_ids) == len(set(entity_ids)), "duplicate transaction-monitor entity IDs")
    for entity in entities:
        state = entity.get("caepr_state")
        caepr_id = entity.get("caepr_id")
        check(state in {"CARET_CONFIRMED", "CARET_PENDING", "PERIMETER_RECORD_NOT_EXACT_LEGAL_PERSON"}, f"bad CAEPR state for {entity.get('entity_id')}")
        if state == "CARET_CONFIRMED":
            check(isinstance(caepr_id, str) and caepr_id in caepr, f"confirmed entity lacks valid CAEPR ID: {entity.get('entity_id')}")
            if isinstance(caepr_id, str) and caepr_id in caepr:
                check(
                    caepr[caepr_id].get("identity_resolution") == "CARET_CONFIRMED" or caepr_id in caret_confirmed_records,
                    f"CAEPR record is not confirmed by either exact registry state or the declared caret census: {caepr_id}",
                )
        else:
            check(bool(entity.get("next_identity_source_needed")), f"unresolved entity lacks next identity source: {entity.get('entity_id')}")
        check("^" not in str(entity.get("display_name", "")), f"machine identity name contains presentation caret: {entity.get('entity_id')}")

    labranda = next((item for item in entities if item.get("entity_id") == "FTI-TX-ENT-010"), {})
    check(labranda.get("caepr_state") == "CARET_CONFIRMED" and labranda.get("caepr_id") == "PD-SP-O-0041", "Labranda brand identity does not match canonical caret census")
    labranda_census = caret_confirmed_records.get("PD-SP-O-0041", {})
    check(labranda_census.get("label") == "Labranda" and labranda_census.get("role_class") == "BRAND_OBJECT", "Labranda caret census confirmation is not compatible with the controlled brand-object type")
    check("brand" in str(labranda_census.get("boundary", "")).casefold(), "Labranda caret census lacks a brand-only boundary")
    labranda_boundary = str(labranda.get("identity_boundary", "")).casefold()
    check("brand" in labranda_boundary and "does not" in labranda_boundary and "owner" in labranda_boundary and "operator" in labranda_boundary, "Labranda brand-only/non-capacity boundary is incomplete")
    bluesea = next((item for item in entities if item.get("entity_id") == "FTI-TX-ENT-011"), {})
    check(bluesea.get("display_name") == "BLUESEA commercial perimeter", "BLUESEA pending perimeter label drift")
    check(bluesea.get("caepr_state") == "CARET_PENDING" and not bluesea.get("caepr_id"), "BLUESEA commercial perimeter must remain caret-pending")
    blue_boundary = str(bluesea.get("identity_boundary", "")).casefold()
    check("distinct from gestora blue sea partner" in blue_boundary and "not an exact owner" in blue_boundary, "BLUESEA/Gestora/non-capacity boundary is incomplete")

    scopes = register.get("heritage_scopes", [])
    scope_ids = [item.get("heritage_scope_id") for item in scopes]
    check(len(scopes) == 3, f"expected three heritage scopes, found {len(scopes)}")
    check(len(scope_ids) == len(set(scope_ids)), "duplicate heritage-scope IDs")
    for scope in scopes:
        check(scope.get("geography") in {"CANARY_ISLANDS", "SPAIN"}, f"out-of-scope geography: {scope.get('heritage_scope_id')}")
        for object_id in scope.get("included_object_ids", []):
            check(object_id in entity_ids, f"heritage scope references unknown entity {object_id}")
        check(bool(scope.get("does_not_establish")), f"scope lacks proof boundary: {scope.get('heritage_scope_id')}")

    transaction_terms = register.get("term_dictionary", {}).get("transaction_terms", [])
    term_ids = [item.get("term_id") for item in transaction_terms]
    check(len(transaction_terms) == 10, f"expected ten transaction term groups, found {len(transaction_terms)}")
    check(len(term_ids) == len(set(term_ids)), "duplicate transaction-term IDs")

    priorities = {item.get("code") for item in control.get("source_priority", [])}
    sources = register.get("sources", [])
    source_ids = [item.get("source_id") for item in sources]
    check(len(sources) == 12, f"expected twelve monitored public sources, found {len(sources)}")
    check(len(source_ids) == len(set(source_ids)), "duplicate monitor source IDs")
    priority_counts = Counter(item.get("priority") for item in sources)
    check(priority_counts["P1_OFFICIAL"] >= 4, "fewer than four official sources")
    check(priority_counts["P2_PARTY_OR_FIDUCIARY"] >= 4, "fewer than four party/fiduciary sources")
    check(priority_counts["P3_INDEPENDENT_TRADE"] >= 1, "independent trade source absent")
    check(priority_counts["P4_DISCOVERY"] >= 1, "discovery source absent")
    for source in sources:
        source_id = source.get("source_id")
        check(str(source.get("url", "")).startswith("https://"), f"non-HTTPS source: {source_id}")
        check(source.get("priority") in priorities, f"bad priority for {source_id}")
        check(source.get("access_lane") == "AUTOMATED_SAFE", f"configured source is not AUTOMATED_SAFE: {source_id}")
        check(source.get("source_type") in {"HTML", "PDF", "RSS"}, f"bad type for {source_id}")
        check(source.get("change_review_policy") in {"ANY_CHANGE", "ENTITY_AND_TRANSACTION_TERM", "DISCOVERY_ONLY"}, f"bad change policy for {source_id}")
        for scope_id in source.get("heritage_scope_ids", []):
            check(scope_id in scope_ids, f"source {source_id} references unknown scope {scope_id}")
        for entity_id in source.get("entity_ids", []):
            check(entity_id in entity_ids, f"source {source_id} references unknown entity {entity_id}")
        for term_id in source.get("transaction_term_ids", []):
            check(term_id in term_ids, f"source {source_id} references unknown term {term_id}")
        check(bool(source.get("source_boundary")), f"source lacks boundary: {source_id}")
        headers = source.get("request_headers", {})
        check(not ({str(name).casefold() for name in headers} & {"authorization", "cookie", "proxy-authorization"}), f"source uses a prohibited authentication header: {source_id}")

    gap_ids = {item.get("gap_id") for item in register.get("coverage_gaps", [])}
    for scope in scopes:
        source_refs = scope.get("source_refs", [])
        gap_refs = scope.get("source_gap_refs", [])
        for source_id in source_refs:
            check(source_id in source_ids, f"heritage scope references unknown source {source_id}")
        for gap_id in gap_refs:
            check(gap_id in gap_ids, f"heritage scope references unknown gap {gap_id}")
        if scope.get("heritage_source_state") == "CONFIGURED_PUBLIC_SOURCE_REFS":
            check(bool(source_refs), f"configured heritage scope has no source refs: {scope.get('heritage_scope_id')}")
        elif scope.get("heritage_source_state") == "OPEN_PRIMARY_SOURCE_NOT_CONFIGURED":
            check(not source_refs and bool(gap_refs), f"open heritage scope is not explicitly linked to an open gap: {scope.get('heritage_scope_id')}")
        else:
            check(False, f"bad heritage-source state: {scope.get('heritage_scope_id')}")

    official_lanes = register.get("official_source_lanes", [])
    lane_ids = [item.get("lane_id") for item in official_lanes]
    check(len(official_lanes) == 11, f"expected eleven explicit official-source lanes, found {len(official_lanes)}")
    check(len(lane_ids) == len(set(lane_ids)), "duplicate official-source lane IDs")
    required_lane_terms = {
        "BOE", "BORME", "Registro Público Concursal", "Insolvenzbekanntmachungen",
        "Unternehmensregister", "Handelsregister", "CNMC", "CNMV", "tourism",
        "BDNS", "SNPSAP", "TED", "property title", "Catastro",
    }
    lane_text = " ".join(str(item.get("label", "")) + " " + str(item.get("boundary", "")) for item in official_lanes)
    for term in required_lane_terms:
        check(term.casefold() in lane_text.casefold(), f"official-source lane inventory omits {term}")
    for lane in official_lanes:
        lane_id = lane.get("lane_id")
        check(lane.get("access_lane") in {"AUTOMATED_SAFE", "MANUAL_PUBLIC", "PAID_OR_RESTRICTED"}, f"bad access lane for {lane_id}")
        check(lane.get("coverage_state") in {"CONFIGURED_SAFE_DISCOVERY", "OPEN_GAP_NOT_AUTOMATED"}, f"bad coverage state for {lane_id}")
        for source_id in lane.get("configured_source_refs", []):
            check(source_id in source_ids, f"official lane {lane_id} references unknown source {source_id}")
        for gap_id in lane.get("gap_refs", []):
            check(gap_id in gap_ids, f"official lane {lane_id} references unknown gap {gap_id}")
        if lane.get("coverage_state") == "OPEN_GAP_NOT_AUTOMATED":
            check(bool(lane.get("gap_refs")), f"open official lane lacks finite gap reference: {lane_id}")
            check(lane.get("access_lane") != "AUTOMATED_SAFE", f"open official lane is mislabeled automated: {lane_id}")

    source_008 = next((item for item in sources if item.get("source_id") == "FTI-TX-SRC-008"), {})
    check("year=" not in str(source_008.get("url", "")).casefold(), "MHBK discovery source contains a hard-coded year filter")
    source_012 = next((item for item in sources if item.get("source_id") == "FTI-TX-SRC-012"), {})
    discovery_query = unquote(str(source_012.get("url", ""))).casefold()
    for term in ["canarias", "canary islands", "kanaren", "españa", "spain", "spanien", "adquisición", "übernahme", "financiación", "finanzierung", "restrukturierung"]:
        check(term in discovery_query, f"multilingual discovery source omits {term}")

    capacities = set(control.get("capacity_vocabulary", []))
    transaction_types = set(control.get("transaction_type_vocabulary", []))
    transaction_states = set(control.get("transaction_state_vocabulary", []))
    evidence_states = set(control.get("evidence_state_vocabulary", []))
    events = register.get("events", [])
    event_ids = [item.get("event_id") for item in events]
    check(len(events) == 2, f"expected two public baseline events, found {len(events)}")
    check(len(event_ids) == len(set(event_ids)), "duplicate event IDs")
    required_fields = set(control.get("event_required_fields", []))
    for event in events:
        event_id = event.get("event_id")
        check(required_fields <= set(event), f"event {event_id} lacks required exact fields")
        check(event.get("heritage_scope_id") in scope_ids, f"event {event_id} references unknown scope")
        check(event.get("transaction_type") in transaction_types, f"event {event_id} has bad transaction type")
        check(event.get("transaction_state") in transaction_states, f"event {event_id} has bad transaction state")
        check(event.get("evidence_state") in evidence_states, f"event {event_id} has bad evidence state")
        check(event.get("asset", {}).get("geography") in {"CANARY_ISLANDS", "SPAIN"}, f"event {event_id} asset geography out of scope")
        for participant in event.get("entities_and_capacities", []):
            check(participant.get("entity_id") in entity_ids, f"event {event_id} references unknown entity")
            check(participant.get("capacity") in capacities, f"event {event_id} uses uncontrolled capacity")
            for source_id in participant.get("capacity_source_refs", []):
                check(source_id in source_ids, f"event {event_id} capacity references unknown source")
        for source_id in event.get("source_refs", []):
            check(source_id in source_ids, f"event {event_id} references unknown source {source_id}")
        change = event.get("change_detection", {})
        check(change.get("automatic_promotion") is False, f"event {event_id} enables automatic promotion")
        for source_id in change.get("monitored_source_ids", []):
            check(source_id in source_ids, f"event {event_id} monitor references unknown source")
        public = event.get("public_safety", {})
        check(public.get("classification") == "TX-0_PUBLIC", f"event {event_id} has unsafe classification")
        check(public.get("contains_private_source") is False, f"event {event_id} contains private source")
        check(public.get("contains_unannounced_transaction") is False, f"event {event_id} contains unannounced transaction")
        check(public.get("website_publication_authorized") is False, f"event {event_id} auto-authorizes website publication")
        check(bool(event.get("proves")) and bool(event.get("does_not_prove")) and bool(event.get("contrary_or_limiting_evidence")), f"event {event_id} lacks adjacent boundaries")

    gaps = register.get("coverage_gaps", [])
    check(len(gaps) == 8, f"expected eight open coverage gaps, found {len(gaps)}")
    check(all(item.get("status") == "OPEN" for item in gaps), "coverage gap is not OPEN")

    public_text = REGISTER_PATH.read_text(encoding="utf-8") + "\n" + CONTROL_PATH.read_text(encoding="utf-8")
    check(EMAIL_RE.search(public_text) is None, "public monitor contains an email address")
    check(UUID_RE.search(public_text) is None, "public monitor contains a UUID-like private locator")
    for prohibited in ["message_id", "thread_id", "gmail", "private subject", "native email body", "website_publication_authorized\": true"]:
        check(prohibited.casefold() not in public_text.casefold(), f"public monitor contains prohibited pattern: {prohibited}")


def validate_workflow() -> None:
    text = WORKFLOW_PATH.read_text(encoding="utf-8")
    check("cron: '17 */6 * * *'" in text, "workflow does not run four times daily")
    check("workflow_dispatch:" in text, "workflow lacks manual dispatch")
    check("permissions:\n  contents: read" in text, "workflow permissions are not contents-read only")
    check("timeout-minutes: 15" in text, "workflow lacks bounded timeout")
    check("validate_fti_meeting_point_asset_transaction_monitor.py" in text, "workflow omits validator")
    check("monitor_fti_meeting_point_asset_transactions.py" in text, "workflow omits monitor")
    check("retention-days: 90" in text, "workflow artifact retention is not 90 days")
    check("actions/cache/restore@" in text and "actions/cache/save@" in text, "workflow lacks state continuity cache")
    check("acknowledgement:" in text and "acknowledgement_reason:" in text, "workflow lacks explicit acknowledgement inputs")
    check("FTI_TX_MONITOR_ACKNOWLEDGEMENT:" in text and "FTI_TX_MONITOR_ACKNOWLEDGEMENT_REASON:" in text, "workflow does not pass acknowledgement through environment variables")
    check("id: monitor_sources" in text and "continue-on-error: true" in text, "monitor step cannot preserve outputs before its final non-green result")
    for output in ["pending.json", "incident.json", "history.jsonl", "report.json", "summary.md", "state.json"]:
        check(output in text, f"workflow does not preserve {output}")
    check("fti-meeting-point-asset-transaction-state-v2-" in text, "workflow cache key was not versioned for sticky state v2")
    check(text.count("history.jsonl") >= 3, "workflow does not restore, save and generate bounded history")
    check("# v7.0.0" in text and "# v6.1.0" not in text, "setup-python pin comment does not match v7.0.0 hash")
    check("Enforce required-source and sticky-review result after preservation" in text, "workflow lacks final non-green enforcement gate")
    upload_index = text.find("Upload public-safe monitor evidence")
    enforce_index = text.find("Enforce required-source and sticky-review result after preservation")
    check(upload_index >= 0 and enforce_index > upload_index, "workflow enforces failure before artifact preservation")
    check('report.get("required_source_failures"' in text and 'get("pending_changes"' in text, "final workflow gate does not enforce required-source and sticky pending results")
    for line in [line.strip() for line in text.splitlines() if "uses:" in line]:
        check(PIN_RE.search(line) is not None, f"workflow Action is not immutable-pinned: {line}")
    for prohibited in ["contents: write", "issues: write", "pull-requests: write", "git push", "git commit", "gh issue", "github.rest.issues", "curl -X POST"]:
        check(prohibited not in text, f"workflow contains prohibited mutation: {prohibited}")


def validate_scripts() -> None:
    try:
        py_compile.compile(str(MONITOR_PATH), doraise=True)
        py_compile.compile(str(Path(__file__)), doraise=True)
    except Exception as exc:
        errors.append(f"Python compilation failed: {exc}")
    text = MONITOR_PATH.read_text(encoding="utf-8")
    for marker in [
        "CHANGE_SIGNAL_ONLY_NOT_TRANSACTION_PROOF",
        "automatic_register_mutation",
        "automatic_website_mutation",
        "automatic_external_action",
        "BASELINE_ESTABLISHED",
        "POTENTIAL_TRANSACTION_CHANGE_REVIEW_REQUIRED",
        "PENDING_ACKNOWLEDGEMENT",
        "pending_changes",
        "--acknowledgement",
        "append_history",
        "INCIDENT_SCHEMA",
        "return 3",
        "return 4",
        "AUTOMATED_SAFE",
        "PROHIBITED_REQUEST_HEADERS",
        "ONE_STICKY_REVIEW_WINDOW_PER_SOURCE",
    ]:
        check(marker in text, f"monitor script lacks safeguard marker {marker}")
    for prohibited in ["subprocess", "git push", "git commit", "smtplib", "requests.post", "urllib.request.urlopen(request, data="]:
        check(prohibited not in text, f"monitor script contains prohibited mutation path: {prohibited}")


def validate_sticky_queue_runtime() -> None:
    """Regression-test bounded compaction and exact acknowledgement without network access."""
    try:
        spec = importlib.util.spec_from_file_location("fti_asset_monitor_runtime_check", MONITOR_PATH)
        if spec is None or spec.loader is None:
            raise RuntimeError("cannot load monitor module")
        monitor = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(monitor)

        payload = {"body": b"<html>Meeting Point Canarias acquisition 0</html>"}

        def fake_fetch(source: dict[str, Any], timeout: float, max_bytes: int) -> tuple[bytes, dict[str, Any]]:
            body = payload["body"]
            return body, {
                "http_status": 200,
                "content_type": "text/html; charset=utf-8",
                "etag": None,
                "last_modified": None,
                "content_length": len(body),
            }

        monitor.fetch = fake_fetch
        source = {
            "source_id": "FTI-TX-SRC-001",
            "url": "https://example.invalid/",
            "priority": "P1_OFFICIAL",
            "access_lane": "AUTOMATED_SAFE",
            "source_type": "HTML",
            "enabled": True,
            "required": True,
            "change_review_policy": "ANY_CHANGE",
            "entity_ids": ["FTI-TX-ENT-001"],
            "transaction_term_ids": ["FTI-TX-TERM-001"],
        }
        entities = {"FTI-TX-ENT-001": {"display_name": "Meeting Point", "aliases": []}}
        terms = {"FTI-TX-TERM-001": {"aliases": ["acquisition"]}}
        state_item: dict[str, Any] = {"acknowledged_fingerprint": "a" * 64}
        pending: list[dict[str, Any]] = []
        report_item: dict[str, Any] = {}
        for index in range(40):
            payload["body"] = f"<html>Meeting Point Canarias acquisition {index}</html>".encode()
            report_item, next_state, pending = monitor.process_source(
                source,
                state_item,
                pending,
                entities,
                terms,
                ["Canarias"],
                f"2026-08-27T00:{index:02d}:00+00:00",
                1.0,
                100_000,
            )
            if next_state is None:
                raise AssertionError("synthetic source unexpectedly failed")
            state_item = next_state
            if len(pending) != 1:
                raise AssertionError("pending queue is not bounded to one source review window")
        window = pending[0]
        check(window.get("distinct_fingerprint_count") == 40, "rolling pending window lost its distinct-fingerprint count")
        check(window.get("compacted_prior_fingerprint_count") == 39, "rolling pending window does not disclose compaction count")
        check(window.get("observed_fingerprint") == report_item.get("fingerprint"), "rolling pending window does not retain the exact latest fingerprint")
        check(FINGERPRINT_RE.fullmatch(str(window.get("fingerprint_chain_sha256", ""))) is not None, "rolling pending window lacks a valid SHA-256 chain")

        legacy_duplicate = dict(window)
        legacy_duplicate["pending_id"] = "FTI-TX-PENDING-legacyduplicate"
        legacy_duplicate["observed_fingerprint"] = "b" * 64
        legacy_state = {
            "schema": monitor.STATE_SCHEMA,
            "control_id": REGISTER_ID,
            "sources": {"FTI-TX-SRC-001": state_item},
            "pending_changes": {"FTI-TX-SRC-001": [window, legacy_duplicate]},
            "acknowledgement_log": [],
            "state_warnings": [],
        }
        migrated = monitor.migrate_state(legacy_state, "2026-08-27T01:00:00+00:00")
        consolidated = migrated["pending_changes"]["FTI-TX-SRC-001"]
        check(len(consolidated) == 1, "legacy multi-entry pending queue was not consolidated")
        latest = consolidated[0]["observed_fingerprint"]
        acknowledgement = monitor.apply_acknowledgement(
            migrated,
            f"FTI-TX-SRC-001={latest}",
            "Reviewed exact compacted window",
            "2026-08-27T01:01:00+00:00",
        )
        check(acknowledgement is not None, "exact acknowledgement did not produce a record")
        check("FTI-TX-SRC-001" not in migrated["pending_changes"], "exact acknowledgement did not clear the consolidated source window")
    except Exception as exc:
        errors.append(f"sticky queue runtime regression failed: {exc}")


def main() -> int:
    for path in [CONTROL_PATH, REGISTER_PATH, SCHEMA_PATH, MONITOR_PATH, WORKFLOW_PATH, CARET_CENSUS_PATH]:
        check(path.is_file(), f"missing required file: {path.relative_to(ROOT)}")
    if errors:
        return finish()
    control = load_json(CONTROL_PATH)
    register = load_json(REGISTER_PATH)
    schema = load_json(SCHEMA_PATH)
    check(schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema", "JSON Schema draft marker mismatch")
    check(schema.get("properties", {}).get("control_id", {}).get("const") == REGISTER_ID, "JSON Schema register control mismatch")
    for schema_error in validate_json_schema_instance(register, schema, schema):
        errors.append(f"register JSON Schema violation: {schema_error}")
    caepr = load_registry_records()
    caret_confirmed_records = load_caret_confirmed_records()
    validate_control(control)
    validate_register(control, register, caepr, caret_confirmed_records)
    validate_workflow()
    validate_scripts()
    validate_sticky_queue_runtime()
    return finish()


def finish() -> int:
    if errors:
        print("FTI / Meeting Point asset-transaction monitor validation: FAIL", file=sys.stderr)
        for error in errors:
            print(f" - {error}", file=sys.stderr)
        return 1
    print("FTI / Meeting Point asset-transaction monitor validation: PASS")
    print(" - 3 heritage scopes; 11 entity objects; 12 automated-safe public sources; 11 explicit official-source lanes; 8 open gaps; 2 bounded baseline events")
    print(" - register validated against the complete local JSON Schema with dependency-free Draft 2020-12 keyword coverage used by this schema")
    print(" - exact entity/asset/capacity/date/source/evidence/change fields enforced")
    print(" - sticky acknowledgement queue and non-green required-source/review signal workflow enforced")
    print(" - no automatic event, caret, website, email, filing or external notification; no authenticated or restricted-source fetching")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
