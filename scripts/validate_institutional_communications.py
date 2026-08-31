#!/usr/bin/env python3
"""Validate the public-safe institutional communications continuity layer."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from reconcile_institutional_communications import (
    BASELINE_COHORT,
    BASELINE_EXPECTED,
    BASELINE_SOURCE_SHA256,
    DEFAULT_CHECKPOINT,
    DEFAULT_MAILBOX_INDEX,
    DEFAULT_REGISTER,
    DEFAULT_SOURCE,
    KEY_EVENTS,
    MAILBOX_COHORT,
    MAILBOX_EXPECTED,
    PRIVATE_MANIFEST_ROWS,
    PRIVATE_MANIFEST_SHA256,
    RECEIPT_BOUNDARY,
    RECIPIENTS,
    REPO_ROOT,
    load_source_rows,
    sha256_file,
    subject_category,
    subject_digest,
)
from build_public_mailbox_event_index import (
    ALLOWED_DIRECTIONS as MAILBOX_ALLOWED_DIRECTIONS,
    ALLOWED_OFFICE_ROUTES as MAILBOX_ALLOWED_OFFICE_ROUTES,
    PUBLIC_MATCH_KEY_RE,
    TRANSPORT_STATE as MAILBOX_TRANSPORT_STATE,
)


DEFAULT_SCHEMA = REPO_ROOT / ".github/evidence-intelligence/schemas/institutional-communications.schema.json"
DEFAULT_ID_POLICY = REPO_ROOT / ".github/evidence-intelligence/id-extension-policy.json"
DEFAULT_PEOPLE = REPO_ROOT / "assets/data/matter-identity-registry-v1.people.json"
EVENT_ID_RE = re.compile(r"^PD-SP-EVT-[0-9]{4}$")
EMAIL_RE = re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b")
PRIVATE_URL_RE = re.compile(r"(?i)https?://[^\s\"]*(?:mail\.google|gmail|drive\.google|docs\.google)[^\s\"]*")
BARE_PROVIDER_ID_RE = re.compile(r"^[0-9a-f]{16,40}$")
FORBIDDEN_KEYS = {
    "gmail_message_id",
    "gmail_thread_id",
    "message_id",
    "thread_id",
    "drive_file_id",
    "provider_id",
    "provider_locator",
    "private_message_locator",
    "vault_locator",
    "email_body",
    "email_address",
    "direct_phone",
    "access_token",
    "refresh_token",
    "exact_private_subject",
    "provider_message_id",
    "provider_thread_id",
    "sender_exact",
    "to_exact",
    "cc_exact",
    "bcc_exact",
    "exact_subject",
    "attachment_names",
    "inline_image_names",
    "provider_labels",
}
ALLOWED_HASH_KEYS = {
    "sha256",
    "detailed_index_sha256",
    "controlling_154_page_pdf_sha256",
    "public_safe_transcript_sha256",
    "controlling_source_pdf_sha256",
    "register_sha256",
    "source_sha256",
    "mailbox_index_sha256",
    "private_custody_manifest_sha256",
    "manifest_sha256",
}


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def _scan_public_safety(value: Any, path: str, errors: list[str], parent_key: str = "") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}" if path else key
            if key.casefold() in FORBIDDEN_KEYS:
                errors.append(f"private/provider field prohibited: {child_path}")
            _scan_public_safety(child, child_path, errors, key)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _scan_public_safety(child, f"{path}[{index}]", errors, parent_key)
    elif isinstance(value, str):
        if EMAIL_RE.search(value):
            errors.append(f"email address prohibited at {path}")
        if PRIVATE_URL_RE.search(value):
            errors.append(f"private mail/drive URL prohibited at {path}")
        if parent_key not in ALLOWED_HASH_KEYS and BARE_PROVIDER_ID_RE.fullmatch(value):
            errors.append(f"bare provider-like identifier prohibited at {path}")


def _validate_schema_if_available(instance: dict[str, Any], schema_path: Path, errors: list[str]) -> None:
    try:
        schema = load_json(schema_path)
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"schema cannot be loaded: {exc}")
        return
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        errors.append("schema must declare JSON Schema draft 2020-12")
    try:
        import jsonschema  # type: ignore
    except ImportError:
        return
    validator = jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())
    for violation in sorted(validator.iter_errors(instance), key=lambda item: list(item.absolute_path)):
        location = ".".join(str(part) for part in violation.absolute_path) or "<root>"
        errors.append(f"schema violation at {location}: {violation.message}")


def validate_register(
    register: dict[str, Any],
    checkpoint: dict[str, Any],
    *,
    repo_root: Path = REPO_ROOT,
    source_path: Path = DEFAULT_SOURCE,
    mailbox_index_path: Path = DEFAULT_MAILBOX_INDEX,
    register_path: Path = DEFAULT_REGISTER,
    schema_path: Path = DEFAULT_SCHEMA,
) -> list[str]:
    errors: list[str] = []
    _validate_schema_if_available(register, schema_path, errors)
    _scan_public_safety(register, "register", errors)
    _scan_public_safety(checkpoint, "checkpoint", errors)
    try:
        mailbox_index = load_json(mailbox_index_path)
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"public mailbox index cannot be loaded: {exc}")
        mailbox_index = {}
    _scan_public_safety(mailbox_index, "mailbox_index", errors)

    if register.get("schema") != "por-derecho.institutional-communications-register.v1":
        errors.append("unexpected register schema")
    denominator = register.get("denominator_control", {})
    expected_denominator = {
        "wider_regage_records_reported": 97,
        "reported_received": 90,
        "reported_rejected": 7,
        "detailed_baseline_receipt_rows_expected": 75,
        "detailed_baseline_receipt_rows_registered": 75,
        "metadata_only_records_reported": 22,
        "metadata_only_representation": "ONE_UNRESOLVED_BATCH_NOT_22_SYNTHETIC_EVENTS",
        "private_manifest_rows": 231,
        "private_manifest_baseline_receipt_rows": 75,
        "private_manifest_mailbox_event_rows": 156,
        "mailbox_outbound_email_rows": 42,
        "mailbox_inbound_email_rows": 101,
        "mailbox_self_archive_rows": 10,
        "mailbox_draft_rows": 3,
        "mailbox_route_not_publicly_attested_rows": 81,
        "mailbox_transport_events": 156,
    }
    for key, expected in expected_denominator.items():
        if denominator.get(key) != expected:
            errors.append(f"denominator {key}: expected {expected!r}, found {denominator.get(key)!r}")
    if 75 + 22 != denominator.get("wider_regage_records_reported"):
        errors.append("75 detailed + 22 metadata-only denominator does not reconcile to 97")
    if denominator.get("reported_received", 0) + denominator.get("reported_rejected", 0) != 97:
        errors.append("90 received + 7 rejected denominator does not reconcile to 97")

    events = register.get("events")
    if not isinstance(events, list):
        return errors + ["events must be an array"]
    ids = [event.get("event_id") for event in events if isinstance(event, dict)]
    if len(ids) != len(set(ids)):
        errors.append("duplicate event_id")
    for event_id in ids:
        if not isinstance(event_id, str) or not EVENT_ID_RE.fullmatch(event_id):
            errors.append(f"invalid event_id: {event_id!r}")
    source_keys = [event.get("source_key") for event in events if isinstance(event, dict)]
    if len(source_keys) != len(set(source_keys)):
        errors.append("duplicate source_key")

    if mailbox_index.get("schema") != "por-derecho.institutional-communications-mailbox-index.v1":
        errors.append("unexpected public mailbox-index schema")
    mailbox_custody = mailbox_index.get("source_custody", {})
    expected_mailbox_custody = {
        "custody_reference": "PD-SP-CUST-0001",
        "manifest_sha256": PRIVATE_MANIFEST_SHA256,
        "manifest_rows": PRIVATE_MANIFEST_ROWS,
        "mailbox_event_rows": MAILBOX_EXPECTED,
        "baseline_receipt_rows": BASELINE_EXPECTED,
        "persistence_status": "PERSISTED_PRIVATE_CUSTODY",
        "provider_or_storage_identifier_published": False,
    }
    if mailbox_custody != expected_mailbox_custody:
        errors.append("public mailbox-index custody controls are inconsistent")
    mailbox_index_events = mailbox_index.get("events", [])
    if not isinstance(mailbox_index_events, list) or len(mailbox_index_events) != MAILBOX_EXPECTED:
        errors.append(f"expected {MAILBOX_EXPECTED} public mailbox-index events")
        mailbox_index_events = []
    mailbox_index_ids = [event.get("event_id") for event in mailbox_index_events if isinstance(event, dict)]
    mailbox_match_keys = [event.get("public_event_match_key") for event in mailbox_index_events if isinstance(event, dict)]
    if len(mailbox_index_ids) != len(set(mailbox_index_ids)):
        errors.append("duplicate event_id in public mailbox index")
    if len(mailbox_match_keys) != len(set(mailbox_match_keys)):
        errors.append("duplicate public_event_match_key in public mailbox index")
    for event in mailbox_index_events:
        event_id = event.get("event_id")
        key = event.get("public_event_match_key")
        direction = event.get("direction")
        route = event.get("office_route")
        if not isinstance(event_id, str) or not EVENT_ID_RE.fullmatch(event_id):
            errors.append(f"invalid mailbox-index event ID: {event_id!r}")
        if not isinstance(key, str) or not PUBLIC_MATCH_KEY_RE.fullmatch(key):
            errors.append(f"invalid public mailbox match key at {event_id}: {key!r}")
        if direction not in MAILBOX_ALLOWED_DIRECTIONS:
            errors.append(f"invalid mailbox direction at {event_id}: {direction!r}")
        elif event.get("transport_state") != MAILBOX_TRANSPORT_STATE[direction]:
            errors.append(f"mailbox transport-state mismatch at {event_id}")
        if route not in MAILBOX_ALLOWED_OFFICE_ROUTES:
            errors.append(f"invalid mailbox route at {event_id}: {route!r}")
        digest = event.get("subject_digest_sha256")
        if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
            errors.append(f"invalid subject digest at {event_id}")
        if event.get("subject_text_published") is not False:
            errors.append(f"mailbox subject-publication boundary changed at {event_id}")
        if not isinstance(event.get("attachment_count"), int) or event.get("attachment_count", -1) < 0:
            errors.append(f"invalid attachment count at {event_id}")
    mailbox_denominator = mailbox_index.get("denominator_control", {})
    expected_direction_counts = {"DRAFT": 3, "INBOUND_EMAIL": 101, "OUTBOUND_EMAIL": 42, "SELF_ARCHIVE": 10}
    if mailbox_denominator.get("mailbox_event_rows") != 156:
        errors.append("mailbox-index row denominator is not 156")
    if mailbox_denominator.get("direction_counts") != expected_direction_counts:
        errors.append("mailbox-index direction denominator drift")
    if mailbox_denominator.get("route_not_publicly_attested_rows") != 81:
        errors.append("mailbox-index unresolved-route denominator drift")

    register_mailbox = [event for event in events if event.get("cohort") == MAILBOX_COHORT]
    register_mailbox_ids = {event.get("event_id") for event in register_mailbox}
    if register_mailbox_ids != set(mailbox_index_ids):
        errors.append("register mailbox cohort does not exactly match public mailbox index IDs")
    non_mailbox_ids = {event.get("event_id") for event in events if event.get("cohort") != MAILBOX_COHORT}
    if register_mailbox_ids & non_mailbox_ids:
        errors.append("mailbox event namespace collides with a non-mailbox register event")
    register_match_keys = {event.get("public_match_key") for event in register_mailbox}
    if register_match_keys != set(mailbox_match_keys):
        errors.append("register mailbox cohort does not exactly match public mailbox match keys")

    baseline = [event for event in events if event.get("cohort") == BASELINE_COHORT]
    if len(baseline) != BASELINE_EXPECTED:
        errors.append(f"expected exactly 75 baseline receipt events; found {len(baseline)}")
    if any(event.get("record_type") != "REGISTRATION_RECEIPT" for event in baseline):
        errors.append("every baseline event must be REGISTRATION_RECEIPT")

    try:
        source_rows = load_source_rows(source_path, BASELINE_EXPECTED)
    except (OSError, ValueError) as exc:
        errors.append(f"source index invalid: {exc}")
        source_rows = []
    source_by_ref = {row["official_reference"]: row for row in source_rows}
    baseline_by_ref = {event.get("official_reference"): event for event in baseline}
    if len(baseline_by_ref) != len(baseline):
        errors.append("duplicate baseline official_reference")
    if set(baseline_by_ref) != set(source_by_ref):
        missing = sorted(set(source_by_ref) - set(baseline_by_ref))
        extra = sorted(set(baseline_by_ref) - set(source_by_ref))
        errors.append(f"baseline/source reference mismatch; missing={missing}, extra={extra}")

    annex_total = 0
    recipient_counts: Counter[str] = Counter()
    for reference, source in source_by_ref.items():
        event = baseline_by_ref.get(reference)
        if event is None:
            continue
        expected_fields = {
            "event_date": source["presented"].date().isoformat(),
            "presented_local": source["presented"].isoformat(timespec="seconds"),
            "source_timezone": "NOT_STATED_IN_RECEIPT_INDEX",
            "office": source["office"],
            "subject_category": subject_category(str(source["source_subject"])),
            "subject_digest_sha256": subject_digest(str(source["source_subject"])),
            "subject_label_status": "FORMAL_REGISTRATION_LABEL_IN_CANONICAL_SOURCE_NOT_REPEATED_HERE",
            "source_pages": source["source_pages"],
            "annex_count": source["annex_count"],
            "recipient_dir3": RECIPIENTS[source["office"]][0],
            "institution_id": RECIPIENTS[source["office"]][1],
        }
        for key, expected in expected_fields.items():
            if event.get(key) != expected:
                errors.append(f"{event.get('event_id')} {key}: expected {expected!r}, found {event.get(key)!r}")
        annex_total += int(event.get("annex_count", 0))
        recipient_counts[str(event.get("office"))] += 1
        if event.get("evidence_state") != RECEIPT_BOUNDARY:
            errors.append(f"{event.get('event_id')} receipt evidence-state boundary changed")
    if annex_total != 126:
        errors.append(f"expected 126 baseline annex listings; found {annex_total}")
    expected_recipients = Counter({
        "Fiscalia Provincial de Las Palmas": 45,
        "Fiscalia de la Comunidad Autonoma de Canarias": 8,
        "Fiscalia de Area de Arrecife de Lanzarote-Puerto del Rosario": 5,
        "Fiscalia Provincial de Santa Cruz de Tenerife": 5,
        "Fiscalia Especial contra la Corrupcion y Criminalidad Organizada": 4,
        "Fiscalía Europea": 2,
        "Fiscalía General del Estado": 2,
        "Fiscalia Provincial de Valencia": 1,
        "Fiscalía de la Sala de lo Penal del Tribunal Supremo": 1,
        "Fiscalia de la Audiencia Nacional": 1,
        "Unidad de Apoyo a la Fiscalía Europea": 1,
    })
    if recipient_counts != expected_recipients:
        errors.append(f"recipient distribution mismatch: {dict(recipient_counts)}")

    for event in events:
        if event.get("record_type") == "REGISTRATION_RECEIPT" and event.get("evidence_state") != RECEIPT_BOUNDARY:
            errors.append(f"{event.get('event_id')} receipt status improperly exceeds the receipt boundary")
        source_integrity = event.get("source_integrity", {})
        anchor = source_integrity.get("repository_anchor")
        if not isinstance(anchor, str) or not anchor:
            errors.append(f"{event.get('event_id')} missing repository source anchor")
        elif not (repo_root / anchor).is_file():
            errors.append(f"{event.get('event_id')} source anchor does not exist: {anchor}")

    curated_expected = {event["event_id"] for event in KEY_EVENTS}
    curated_found = {event.get("event_id") for event in events if event.get("cohort") == "CURATED_SOURCE_PROVED_EVENT"}
    if curated_found != curated_expected:
        errors.append(f"curated-event set drift: expected {sorted(curated_expected)}, found {sorted(curated_found)}")
    for event in events:
        for linked_id in event.get("linked_transport_event_ids", []):
            if linked_id not in register_mailbox_ids:
                errors.append(f"{event.get('event_id')} linked transport is absent or not a mailbox transport row: {linked_id}")

    di22_acts = [
        event for event in events
        if "DI 22/2026" in event.get("matter_references", [])
        and event.get("cohort") == "CURATED_SOURCE_PROVED_EVENT"
        and event.get("record_type") in {"OFFICIAL_DECISION", "OFFICIAL_ROUTING_ACT"}
    ]
    if len(di22_acts) != 11:
        errors.append(f"DI 22 must have 11 distinct official act rows; found {len(di22_acts)}")
    di22_dates = Counter(event.get("event_date") for event in di22_acts)
    if di22_dates.get("2026-02-11") != 2 or di22_dates.get("2026-02-13") != 2:
        errors.append(f"DI 22 11/13-Feb multiplicity is wrong: {dict(di22_dates)}")
    august_receipt_refs = {
        str(event.get("official_reference", "")).split(" / ")[0]
        for event in events
        if event.get("record_type") == "REGISTRATION_RECEIPT"
        and event.get("event_date") == "2026-08-02"
        and "REGAGE26e000702" in str(event.get("official_reference", ""))
    }
    expected_august_receipts = {
        "REGAGE26e00070235399", "REGAGE26e00070235775", "REGAGE26e00070236067",
        "REGAGE26e00070236245", "REGAGE26e00070236543", "REGAGE26e00070236749",
        "REGAGE26e00070237051",
    }
    if august_receipt_refs != expected_august_receipts:
        errors.append(f"seven-destination August receipt family mismatch: {sorted(august_receipt_refs)}")
    st104_ack = [
        event for event in events
        if "ST 104/2025" in event.get("matter_references", [])
        and event.get("record_type") == "INSTITUTIONAL_ACKNOWLEDGEMENT"
        and event.get("event_id") in {"PD-SP-EVT-0130", "PD-SP-EVT-0131", "PD-SP-EVT-0132", "PD-SP-EVT-0133", "PD-SP-EVT-0134"}
    ]
    if len(st104_ack) != 5:
        errors.append(f"ST 104/2025 must retain five separate acknowledgement rows; found {len(st104_ack)}")

    namespace = register.get("id_namespace_authority", {})
    try:
        id_policy = load_json(DEFAULT_ID_POLICY)
        policy_pattern = id_policy.get("extensions", {}).get("EVENT")
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"ID extension policy cannot be loaded: {exc}")
        policy_pattern = None
    if policy_pattern != r"^PD-SP-EVT-[0-9]{4}$":
        errors.append(f"EVENT namespace is not declared as expected in ID policy: {policy_pattern!r}")
    if namespace != {
        "policy_path": ".github/evidence-intelligence/id-extension-policy.json",
        "extension": "EVENT",
        "declared_pattern": "^PD-SP-EVT-[0-9]{4}$",
        "status": "DECLARED_IN_EXISTING_POLICY_AND_VALIDATED",
    }:
        errors.append("register ID namespace authority is missing or inconsistent")

    try:
        people = load_json(DEFAULT_PEOPLE).get("records", [])
        people_by_id = {person.get("id"): person for person in people}
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"people identity registry cannot be loaded: {exc}")
        people_by_id = {}
    for event in events:
        attribution = event.get("attribution_state")
        person_id = event.get("signatory_person_id")
        person_label = event.get("signatory_person_label")
        if attribution == "SOURCE_PROVED_SIGNATORY":
            if person_id not in people_by_id:
                errors.append(f"{event.get('event_id')} source-proved signatory lacks a registered person ID")
            elif people_by_id[person_id].get("name") != person_label:
                errors.append(f"{event.get('event_id')} signatory label does not match identity registry")
        elif person_id is not None or person_label is not None:
            errors.append(f"{event.get('event_id')} has a person signatory without source-proved attribution")
        if attribution == "INSTITUTION_ONLY_SIGNATURE_PENDING" and (person_id is not None or person_label is not None):
            errors.append(f"{event.get('event_id')} office-only act must not invent a signatory")

    batches = register.get("unresolved_batches", [])
    if len(batches) != 1:
        errors.append(f"expected one unresolved aggregate batch; found {len(batches)}")
    elif (
        batches[0].get("record_count") != 22
        or batches[0].get("aggregate_received_count") != 15
        or batches[0].get("aggregate_rejected_count") != 7
        or batches[0].get("synthetic_event_rows_created") != 0
    ):
        errors.append("22-record aggregate batch controls are incorrect")
    if any(event.get("cohort") == "METADATA_ONLY_22" for event in events):
        errors.append("aggregate-only records must not be expanded into event rows")

    source_controls = register.get("source_controls", {})
    actual_source_hash = sha256_file(source_path) if source_path.is_file() else "MISSING"
    if actual_source_hash != BASELINE_SOURCE_SHA256:
        errors.append(f"canonical source index hash mismatch: {actual_source_hash}")
    if source_controls.get("detailed_index_sha256") != actual_source_hash:
        errors.append("register detailed_index_sha256 does not match source")
    actual_mailbox_hash = sha256_file(mailbox_index_path) if mailbox_index_path.is_file() else "MISSING"
    if source_controls.get("mailbox_index_sha256") != actual_mailbox_hash:
        errors.append("register mailbox_index_sha256 does not match public mailbox index")
    if source_controls.get("private_custody_manifest_sha256") != PRIVATE_MANIFEST_SHA256:
        errors.append("register private custody manifest hash mismatch")
    if source_controls.get("private_custody_manifest_row_count") != PRIVATE_MANIFEST_ROWS:
        errors.append("register private custody manifest row denominator mismatch")

    if checkpoint.get("schema") != "por-derecho.institutional-communications-scan-checkpoint.v1":
        errors.append("unexpected checkpoint schema")
    baseline_checkpoint = checkpoint.get("baseline_import", {})
    for key, expected in {
        "expected_rows": 75,
        "imported_rows": 75,
        "unique_regage_references": 75,
        "annex_listings": 126,
        "source_exhausted": True,
    }.items():
        if baseline_checkpoint.get(key) != expected:
            errors.append(f"checkpoint baseline_import.{key}: expected {expected!r}")
    aggregate_checkpoint = checkpoint.get("aggregate_only_control", {})
    if aggregate_checkpoint.get("reported_rows") != 22 or aggregate_checkpoint.get("synthetic_event_rows") != 0:
        errors.append("checkpoint aggregate-only control is incorrect")
    mail_control = checkpoint.get("last_month_mail_control", {})
    if mail_control.get("pagination_complete") is not True:
        errors.append("last-month mail control is not marked pagination-complete")
    if mail_control.get("provider_locators_published") is not False:
        errors.append("checkpoint must state that provider locators are not published")
    custody = register.get("private_locator_boundary", {}).get("custody_manifest", {})
    if custody != {
        "custody_reference": "PD-SP-CUST-0001",
        "status": "PERSISTED_PRIVATE_CUSTODY",
        "manifest_sha256": PRIVATE_MANIFEST_SHA256,
        "manifest_row_count": PRIVATE_MANIFEST_ROWS,
        "provider_or_storage_identifier_published": False,
    }:
        errors.append("opaque private-custody reference/status boundary is inconsistent")

    if register_path.is_file():
        register_hash = sha256_file(register_path)
        if checkpoint.get("register_sha256") != register_hash:
            errors.append("checkpoint register_sha256 does not match register bytes")
    if baseline_checkpoint.get("source_sha256") != actual_source_hash:
        errors.append("checkpoint source_sha256 does not match source index")
    checkpoint_custody = checkpoint.get("private_custody", {})
    if checkpoint_custody != {
        "custody_reference": "PD-SP-CUST-0001",
        "status": "PERSISTED_PRIVATE_CUSTODY",
        "manifest_sha256": PRIVATE_MANIFEST_SHA256,
        "manifest_rows": PRIVATE_MANIFEST_ROWS,
        "provider_or_storage_identifier_published": False,
    }:
        errors.append("checkpoint private-custody control mismatch")
    checkpoint_mailbox = checkpoint.get("mailbox_index", {})
    for key, expected in {
        "source_sha256": actual_mailbox_hash,
        "event_rows": 156,
        "outbound_email_rows": 42,
        "inbound_email_rows": 101,
        "self_archive_rows": 10,
        "draft_rows": 3,
        "route_not_publicly_attested_rows": 81,
        "source_exhausted": True,
    }.items():
        if checkpoint_mailbox.get(key) != expected:
            errors.append(f"checkpoint mailbox_index.{key}: expected {expected!r}")
    return errors


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--register", type=Path, default=DEFAULT_REGISTER)
    parser.add_argument("--checkpoint", type=Path, default=DEFAULT_CHECKPOINT)
    parser.add_argument("--source-index", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--mailbox-index", type=Path, default=DEFAULT_MAILBOX_INDEX)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        register = load_json(args.register)
        checkpoint = load_json(args.checkpoint)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    errors = validate_register(
        register,
        checkpoint,
        repo_root=REPO_ROOT,
        source_path=args.source_index.resolve(),
        mailbox_index_path=args.mailbox_index.resolve(),
        register_path=args.register.resolve(),
        schema_path=args.schema.resolve(),
    )
    if errors:
        print("institutional communications validation failed:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1
    print(
        "OK: 75 detailed receipts + 156 mailbox transports reconciled; "
        "22 aggregate-only records remain one batch; "
        f"{len(KEY_EVENTS)} curated events source-anchored; public/private boundary enforced"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
