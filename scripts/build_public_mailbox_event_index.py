#!/usr/bin/env python3
"""Create a public-safe mailbox event index from a private custody manifest.

The input contains native provider locators and exact mailbox metadata and must
remain outside Git.  The output deliberately retains only event time, a
controlled transport state and office route, narrowly extracted official
references, a one-way subject digest/category, attachment counts, and a stable
public match key.  No provider identifier, address, subject text, message body
or native attachment name is copied to the output.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
import unicodedata
from datetime import datetime
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = REPO_ROOT / "assets/data/institutional-communications-mailbox-index-v1.json"
CONTROL_DATE = "2026-08-31"
CUSTODY_REFERENCE = "PD-SP-CUST-0001"
PRIVATE_MANIFEST_SHA256 = "bdd12a8fa62b5058525e1c37053fb7899ac24a60d12ff48ab8b74bda617cd6f6"
PRIVATE_MANIFEST_ROWS = 231
EXPECTED_MAILBOX_ROWS = 156
EXPECTED_BASELINE_ROWS = 75
MAILBOX_EVENT_START = 1001
EVENT_ID_RE = re.compile(r"^PD-SP-EVT-(\d{4})$")
PUBLIC_MATCH_KEY_RE = re.compile(r"^MF-MAIL-[A-Z0-9-]{1,80}$")

PRIVATE_COLUMNS = {
    "record_class",
    "event_date",
    "event_timestamp",
    "direction",
    "office_route",
    "provider_message_id",
    "provider_thread_id",
    "sender_exact",
    "to_exact",
    "cc_exact",
    "bcc_exact",
    "exact_subject",
    "attachment_names",
    "inline_image_names",
    "official_reference",
    "public_event_match_key",
    "baseline_regage",
    "baseline_source_pages",
    "baseline_recipient",
    "baseline_annex_count",
    "provider_labels",
    "limitations",
}

ALLOWED_DIRECTIONS = {"OUTBOUND_EMAIL", "INBOUND_EMAIL", "SELF_ARCHIVE", "DRAFT"}
ALLOWED_OFFICE_ROUTES = {
    "FISCALIA_ANTICORRUPCION",
    "FISCALIA_CAC",
    "FGE_ATENCION_CIUDADANO",
    "FISCALIA_PROVINCIAL_TENERIFE",
    "FGE_SECRETARIA_TECNICA",
    "FISCALIA_PROVINCIAL_LAS_PALMAS",
    "FGE_SECRETARIA_TECNICA | FGE_ATENCION_CIUDADANO",
    "FISCALIA_AUDIENCIA_NACIONAL",
    "FISCALIA_AREA_ARRECIFE_PUERTO_ROSARIO",
    "FISCALIA_GUBERNATIVO_LAS_PALMAS",
    "FISCALIA_PROVINCIAL_LAS_PALMAS | FISCALIA_GUBERNATIVO_LAS_PALMAS",
    "FISCALIA_CAC_TENERIFE",
    "INSPECCION_FISCAL_OFFICIAL_SENDER",
    "ROUTE_NOT_PUBLICLY_ATTESTED",
}

TRANSPORT_STATE = {
    "OUTBOUND_EMAIL": "SENT_EMAIL_LOCATED",
    "INBOUND_EMAIL": "RECEIVED_EMAIL_LOCATED",
    "SELF_ARCHIVE": "SELF_ARCHIVE_CONTROL_NOT_AN_INSTITUTIONAL_SEND",
    "DRAFT": "DRAFT_NOT_SENT",
}

PROOF_CEILING = {
    "OUTBOUND_EMAIL": "Proves an email transmission event from the controlled mailbox. It does not prove formal filing, destination receipt, reading, allocation, association, examination or merits treatment.",
    "INBOUND_EMAIL": "Proves an incoming email event and only the content/status established by a separately controlled public-safe source. It does not by itself prove formal filing, internal allocation, complete-file review or merits correctness.",
    "SELF_ARCHIVE": "Proves a self-archive/control event only. It is not an institutional send, filing, recipient receipt or merits event.",
    "DRAFT": "Proves a saved draft only. It was not sent and is not a filing, receipt or merits event.",
}

REFERENCE_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("REGAGE", re.compile(r"\bREGAGE\d{2}[eE]\d{11}\b", re.I)),
    ("DIP", re.compile(r"\bD\.?\s*I\.?\s*P\.?\s*\d{1,6}\s*[/\-]\s*20\d{2}\b", re.I)),
    ("DI", re.compile(r"\bD\.?\s*I\.?\s*(?:PREPROCESAL\s*)?\d{1,6}\s*[/\-]\s*20\d{2}\b", re.I)),
    ("EG", re.compile(r"\bE\.?\s*G\.?\s*\d{1,6}\s*[/\-]\s*20\d{2}\b", re.I)),
    ("ST", re.compile(r"\bS\.?\s*T\.?\s*\d{1,6}\s*[/\-]\s*20\d{2}\b", re.I)),
    ("DP", re.compile(r"\bD\.?\s*P\.?\s*\d{1,6}\s*[/\-]\s*20\d{2}\b", re.I)),
    ("CC_CA", re.compile(r"\bCC\s*/\s*CA\s*\d{1,6}\s*[/\-]\s*20\d{2}\b", re.I)),
    ("NIG", re.compile(r"\b\d{19}\b")),
)

FORBIDDEN_OUTPUT_KEYS = {
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
    "limitations",
}


def canonical_json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def normalized_text(value: str) -> str:
    return "".join(
        character
        for character in unicodedata.normalize("NFKD", value.casefold())
        if not unicodedata.combining(character)
    )


def subject_digest(value: str) -> str:
    normalized = unicodedata.normalize("NFC", value.strip())
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def subject_category(value: str) -> str:
    label = normalized_text(value)
    rules = (
        (("informacion", "copia", "acceso"), "INFORMATION_OR_COPY_REQUEST"),
        (("trazabilidad", "certificacion", "saip"), "TRACEABILITY_OR_CERTIFICATION_REQUEST"),
        (("preservacion", "custodia"), "PRESERVATION_OR_CUSTODY_REQUEST"),
        (("denuncia", "ampliacion"), "CRIMINAL_NOTICE_OR_AMPLIFICATION"),
        (("aportacion", "documentacion", "anexo"), "EVIDENCE_OR_DOCUMENT_CONTRIBUTION"),
        (("revision", "reposicion", "recurso", "impulso"), "REVIEW_OR_INVESTIGATIVE_IMPULSE"),
        (("remision", "traslado", "inhibicion", "competencia"), "ROUTING_OR_REMITTAL"),
        (("acuse", "recibido", "recepcion", "acknowledg"), "INSTITUTIONAL_ACKNOWLEDGEMENT"),
        (("decreto", "resolucion", "notificacion", "expediente"), "OFFICIAL_ACT_OR_NOTICE"),
        (("registro", "regage", "justificante"), "FORMAL_REGISTRATION_OR_RECEIPT"),
    )
    for needles, category in rules:
        if any(needle in label for needle in needles):
            return category
    return "OTHER_INSTITUTIONAL_COMMUNICATION"


def canonical_reference(kind: str, value: str) -> str:
    compact = re.sub(r"\s+", " ", value.strip().upper()).replace("-", "/")
    if kind == "REGAGE":
        return "REGAGE" + compact[6:8] + "e" + compact[-11:]
    if kind == "NIG":
        return f"NIG {compact}"
    if kind == "CC_CA":
        numbers = re.findall(r"\d+", compact)
        return f"CC/CA {numbers[0]}/{numbers[1]}"
    numbers = re.findall(r"\d+", compact)
    if len(numbers) < 2:
        raise ValueError(f"could not canonicalize {kind} reference")
    prefix = {"DI": "DI", "DIP": "DIP", "EG": "EG", "ST": "ST", "DP": "DP"}[kind]
    return f"{prefix} {int(numbers[0])}/{numbers[1]}"


def extract_public_references(value: str) -> list[str]:
    found: list[tuple[int, str]] = []
    for kind, pattern in REFERENCE_PATTERNS:
        for match in pattern.finditer(value):
            found.append((match.start(), canonical_reference(kind, match.group(0))))
    ordered: list[str] = []
    for _, reference in sorted(found):
        if reference not in ordered:
            ordered.append(reference)
    return ordered


def attachment_count(value: str) -> int:
    return len([part for part in value.split("|") if part.strip()])


def load_private_rows(path: Path) -> list[dict[str, str]]:
    if sha256_file(path) != PRIVATE_MANIFEST_SHA256:
        raise ValueError("private manifest hash does not match the controlled 31-August snapshot")
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if set(reader.fieldnames or []) != PRIVATE_COLUMNS:
            raise ValueError("private manifest columns do not match the controlled schema")
        rows = list(reader)
    if len(rows) != PRIVATE_MANIFEST_ROWS:
        raise ValueError(f"expected {PRIVATE_MANIFEST_ROWS} private manifest rows; found {len(rows)}")
    classes = {name: sum(row["record_class"] == name for row in rows) for name in {row["record_class"] for row in rows}}
    expected = {"GMAIL_EVENT": EXPECTED_MAILBOX_ROWS, "BASELINE_REGAGE_RECEIPT": EXPECTED_BASELINE_ROWS}
    if classes != expected:
        raise ValueError(f"unexpected record-class denominator: {classes}")
    return [row for row in rows if row["record_class"] == "GMAIL_EVENT"]


def existing_ids(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    return {
        event["public_event_match_key"]: event["event_id"]
        for event in value.get("events", [])
        if isinstance(event, dict)
        and isinstance(event.get("public_event_match_key"), str)
        and isinstance(event.get("event_id"), str)
    }


def allocate_ids(rows: list[dict[str, str]], prior: dict[str, str]) -> dict[str, str]:
    assigned: dict[str, str] = {}
    used: set[int] = set()
    for key, event_id in prior.items():
        match = EVENT_ID_RE.fullmatch(event_id)
        if key and match and int(match.group(1)) >= MAILBOX_EVENT_START:
            assigned[key] = event_id
            used.add(int(match.group(1)))
    next_number = MAILBOX_EVENT_START
    for row in sorted(rows, key=lambda item: item["public_event_match_key"]):
        key = row["public_event_match_key"]
        if key in assigned:
            continue
        while next_number in used:
            next_number += 1
        if next_number > 9999:
            raise ValueError("PD-SP-EVT namespace exhausted")
        assigned[key] = f"PD-SP-EVT-{next_number:04d}"
        used.add(next_number)
        next_number += 1
    return assigned


def public_event(row: dict[str, str], event_id: str) -> dict[str, Any]:
    direction = row["direction"].strip()
    if direction not in ALLOWED_DIRECTIONS:
        raise ValueError(f"unsupported mailbox direction: {direction!r}")
    event_date = row["event_date"].strip()
    datetime.strptime(event_date, "%Y-%m-%d")
    timestamp = row["event_timestamp"].strip()
    parsed_timestamp = datetime.fromisoformat(timestamp)
    if parsed_timestamp.date().isoformat() != event_date:
        raise ValueError("mailbox event date/timestamp mismatch")
    public_match_key = row["public_event_match_key"].strip()
    if not PUBLIC_MATCH_KEY_RE.fullmatch(public_match_key):
        raise ValueError("public event match key violates the controlled safe pattern")
    route = row["office_route"].strip() or "ROUTE_NOT_PUBLICLY_ATTESTED"
    if route not in ALLOWED_OFFICE_ROUTES:
        raise ValueError(f"unsupported office route token: {route!r}")
    references = extract_public_references(row["official_reference"])
    return {
        "attachment_count": attachment_count(row["attachment_names"]),
        "attachment_count_basis": "NON_INLINE_NATIVE_ATTACHMENTS_COUNTED_PRIVATELY; NAMES_NOT_PUBLISHED",
        "direction": direction,
        "event_date": event_date,
        "event_id": event_id,
        "event_timestamp": timestamp,
        "office_route": route,
        "official_references": references,
        "proof_ceiling": PROOF_CEILING[direction],
        "public_event_match_key": public_match_key,
        "route_proof_state": (
            "ROUTE_NOT_PUBLICLY_ATTESTED"
            if route == "ROUTE_NOT_PUBLICLY_ATTESTED"
            else "CONTROLLED_PUBLIC_SAFE_OFFICE_CLASS"
        ),
        "source_custody_reference": CUSTODY_REFERENCE,
        "subject_category": subject_category(row["exact_subject"]),
        "subject_digest_sha256": subject_digest(row["exact_subject"]),
        "subject_text_published": False,
        "transport_state": TRANSPORT_STATE[direction],
    }


def build_index(rows: list[dict[str, str]], prior: dict[str, str]) -> dict[str, Any]:
    if len({row["public_event_match_key"] for row in rows}) != len(rows):
        raise ValueError("duplicate public event match key in private manifest")
    ids = allocate_ids(rows, prior)
    events = [public_event(row, ids[row["public_event_match_key"]]) for row in rows]
    events.sort(key=lambda event: (event["event_timestamp"], event["public_event_match_key"]))
    directions = {direction: sum(event["direction"] == direction for event in events) for direction in sorted(ALLOWED_DIRECTIONS)}
    routes_unresolved = sum(event["office_route"] == "ROUTE_NOT_PUBLICLY_ATTESTED" for event in events)
    return {
        "schema": "por-derecho.institutional-communications-mailbox-index.v1",
        "index_id": "PD-SP-INSTITUTIONAL-MAILBOX-INDEX-001",
        "control_date": CONTROL_DATE,
        "source_custody": {
            "custody_reference": CUSTODY_REFERENCE,
            "manifest_sha256": PRIVATE_MANIFEST_SHA256,
            "manifest_rows": PRIVATE_MANIFEST_ROWS,
            "mailbox_event_rows": EXPECTED_MAILBOX_ROWS,
            "baseline_receipt_rows": EXPECTED_BASELINE_ROWS,
            "persistence_status": "PERSISTED_PRIVATE_CUSTODY",
            "provider_or_storage_identifier_published": False,
        },
        "privacy_boundary": {
            "contains": [
                "event date/timestamp",
                "controlled direction/state and office-route class",
                "narrowly extracted official reference where publication-safe",
                "subject SHA-256/category without subject text",
                "non-inline attachment count without names",
                "stable public match key",
                "proof ceiling",
            ],
            "excludes": [
                "provider message/thread identifiers",
                "email addresses and display names",
                "exact subjects or bodies",
                "native attachment or inline-image names",
                "mailbox labels and storage locators",
            ],
        },
        "denominator_control": {
            "mailbox_event_rows": len(events),
            "direction_counts": directions,
            "route_not_publicly_attested_rows": routes_unresolved,
            "unique_public_match_keys": len({event["public_event_match_key"] for event in events}),
            "unique_event_ids": len({event["event_id"] for event in events}),
        },
        "events": events,
    }


def scan_forbidden_keys(value: Any, path: str = "$", errors: list[str] | None = None) -> list[str]:
    errors = [] if errors is None else errors
    if isinstance(value, dict):
        for key, child in value.items():
            if key.casefold() in FORBIDDEN_OUTPUT_KEYS:
                errors.append(f"forbidden key at {path}.{key}")
            scan_forbidden_keys(child, f"{path}.{key}", errors)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            scan_forbidden_keys(child, f"{path}[{index}]", errors)
    elif isinstance(value, str):
        if "@" in value or re.search(r"https?://(?:mail|drive)\.google\.", value, re.I):
            errors.append(f"address/provider URL-like value at {path}")
    return errors


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--private-input", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true")
    return parser.parse_args(argv)


def run(args: argparse.Namespace) -> int:
    rows = load_private_rows(args.private_input.resolve())
    value = build_index(rows, existing_ids(args.output.resolve()))
    errors = scan_forbidden_keys(value)
    if errors:
        raise ValueError("public-output safety failure: " + "; ".join(errors))
    content = canonical_json_bytes(value)
    if args.check:
        if not args.output.exists() or args.output.read_bytes() != content:
            print("public mailbox index drift", file=sys.stderr)
            return 1
        print(f"OK: {len(value['events'])} public-safe mailbox events")
        return 0
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(content)
    print(f"wrote {args.output}")
    print(f"mailbox event rows {len(value['events'])}")
    return 0


def main(argv: list[str] | None = None) -> int:
    try:
        return run(parse_args(argv))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
