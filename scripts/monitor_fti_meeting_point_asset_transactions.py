#!/usr/bin/env python3
"""Monitor public sources for FTI / Meeting Point Spanish asset-transaction changes.

The monitor deliberately emits change signals, never transaction findings. It
stores hashes and controlled-term IDs only; source bodies and snippets are not
written to artifacts or the repository.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import html
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPORT_SCHEMA = "por-derecho.fti-meeting-point-asset-transaction-monitor-report.v1"
STATE_SCHEMA = "por-derecho.fti-meeting-point-asset-transaction-monitor-state.v2"
PENDING_SCHEMA = "por-derecho.fti-meeting-point-asset-transaction-pending-queue.v1"
INCIDENT_SCHEMA = "por-derecho.fti-meeting-point-asset-transaction-monitor-incident.v1"
HISTORY_SCHEMA = "por-derecho.fti-meeting-point-asset-transaction-monitor-history-entry.v1"
REGISTER_CONTROL = "PD-FTI-MP-ASSET-TX-REGISTER-20260827-01"
USER_AGENT = "Por-Derecho-Public-Asset-Transaction-Monitor/1.0 (+https://sbu001monterecco.github.io/por-derecho/)"
FINGERPRINT_RE = re.compile(r"^[0-9a-f]{64}$")
MAX_HISTORY_ENTRIES = 1000
MAX_ACKNOWLEDGEMENT_LOG = 200
PROHIBITED_REQUEST_HEADERS = {"authorization", "cookie", "proxy-authorization"}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON root is not an object: {path}")
    return value


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def normalize_pending_entries(source_id: str, entries: Any) -> list[dict[str, Any]]:
    """Collapse legacy duplicates into one sticky, bounded review window per source."""
    valid = [dict(item) for item in entries if isinstance(item, dict)] if isinstance(entries, list) else []
    if not valid:
        return []
    first = valid[0]
    first.setdefault("source_id", source_id)
    first.setdefault("first_observed_fingerprint", first.get("observed_fingerprint"))
    chain = first.get("fingerprint_chain_sha256")
    if not isinstance(chain, str) or not FINGERPRINT_RE.fullmatch(chain):
        chain = hashlib.sha256(str(first.get("observed_fingerprint", "")).encode("utf-8")).hexdigest()
    distinct = int(first.get("distinct_fingerprint_count", 1))
    for extra in valid[1:]:
        observed = extra.get("observed_fingerprint")
        if isinstance(observed, str) and FINGERPRINT_RE.fullmatch(observed):
            chain = hashlib.sha256(f"{chain}\0{observed}".encode("utf-8")).hexdigest()
            first["observed_fingerprint"] = observed
            distinct += 1
        first["last_seen_at"] = extra.get("last_seen_at") or first.get("last_seen_at")
        first["times_seen"] = int(first.get("times_seen", 0)) + int(extra.get("times_seen", 0))
    first["fingerprint_chain_sha256"] = chain
    first["distinct_fingerprint_count"] = distinct
    first["compacted_prior_fingerprint_count"] = max(0, distinct - 1)
    first["queue_model"] = "ONE_STICKY_REVIEW_WINDOW_PER_SOURCE"
    if len(valid) > 1:
        first["legacy_entries_consolidated"] = len(valid)
        first["consolidation_boundary"] = "Legacy queue entries were folded into the rolling fingerprint chain; no event or finding was created."
    return [first]


def migrate_state(previous: dict[str, Any], checked_at: str) -> dict[str, Any]:
    """Upgrade legacy last-seen fingerprints into an explicit reviewed baseline."""
    if previous.get("schema") == STATE_SCHEMA:
        result = dict(previous)
        result.setdefault("sources", {})
        pending_changes = result.setdefault("pending_changes", {})
        if isinstance(pending_changes, dict):
            result["pending_changes"] = {
                source_id: normalized
                for source_id, entries in pending_changes.items()
                if (normalized := normalize_pending_entries(source_id, entries))
            }
        result.setdefault("acknowledgement_log", [])
        result.setdefault("state_warnings", [])
        return result
    legacy_sources = previous.get("sources", {}) if isinstance(previous.get("sources"), dict) else {}
    migrated_sources: dict[str, Any] = {}
    for source_id, item in legacy_sources.items():
        if not isinstance(item, dict):
            continue
        fingerprint = item.get("acknowledged_fingerprint") or item.get("fingerprint")
        if not isinstance(fingerprint, str) or not FINGERPRINT_RE.fullmatch(fingerprint):
            continue
        migrated_sources[source_id] = {
            "acknowledged_fingerprint": fingerprint,
            "last_observed_fingerprint": item.get("last_observed_fingerprint") or fingerprint,
            "normalization": item.get("normalization"),
            "last_success_at": item.get("last_success_at"),
            "content_type": item.get("content_type"),
            "etag": item.get("etag"),
            "last_modified": item.get("last_modified"),
            "baseline_origin": "LEGACY_LAST_SEEN_ASSUMED_ACKNOWLEDGED_DURING_V2_MIGRATION",
        }
    warnings = []
    if previous and previous.get("schema") != STATE_SCHEMA:
        warnings.append(
            {
                "code": "LEGACY_STATE_MIGRATED",
                "at": checked_at,
                "boundary": "Legacy last-seen fingerprints had no pending queue and are treated as acknowledged solely to preserve continuity; this is not proof of human review.",
            }
        )
    return {
        "schema": STATE_SCHEMA,
        "control_id": REGISTER_CONTROL,
        "updated_at": checked_at,
        "sources": migrated_sources,
        "pending_changes": {},
        "acknowledgement_log": [],
        "state_warnings": warnings,
    }


def pending_id(source_id: str, baseline: str, observed: str) -> str:
    digest = hashlib.sha256(f"{source_id}\0{baseline}\0{observed}".encode("utf-8")).hexdigest()[:20]
    return f"FTI-TX-PENDING-{digest}"


def apply_acknowledgement(
    state: dict[str, Any],
    acknowledgement: str,
    reason: str,
    checked_at: str,
) -> dict[str, Any] | None:
    if not acknowledgement:
        if reason:
            raise ValueError("acknowledgement reason supplied without SOURCE_ID=SHA256 acknowledgement")
        return None
    if "=" not in acknowledgement:
        raise ValueError("acknowledgement must be exact SOURCE_ID=SHA256")
    source_id, fingerprint = (part.strip() for part in acknowledgement.split("=", 1))
    if not re.fullmatch(r"FTI-TX-SRC-[0-9]{3}", source_id) or not FINGERPRINT_RE.fullmatch(fingerprint):
        raise ValueError("acknowledgement must contain a controlled source ID and lowercase 64-character SHA-256")
    if len(reason.strip()) < 8:
        raise ValueError("acknowledgement requires a public-safe reason of at least eight characters")
    queue = state.setdefault("pending_changes", {})
    entries = queue.get(source_id, [])
    matching = [item for item in entries if item.get("observed_fingerprint") == fingerprint]
    if len(matching) != 1:
        raise ValueError("acknowledgement fingerprint must match exactly one pending item for the source")
    acknowledged = matching[0]
    remaining = [item for item in entries if item is not acknowledged]
    if remaining:
        queue[source_id] = remaining
    else:
        queue.pop(source_id, None)
    source_state = state.setdefault("sources", {}).setdefault(source_id, {})
    source_state["acknowledged_fingerprint"] = fingerprint
    source_state["acknowledged_at"] = checked_at
    source_state["acknowledgement_boundary"] = "EXACT_PENDING_FINGERPRINT_ONLY"
    record = {
        "source_id": source_id,
        "pending_id": acknowledged.get("pending_id"),
        "fingerprint": fingerprint,
        "acknowledged_at": checked_at,
        "reason": reason.strip(),
        "github_run_id": os.environ.get("GITHUB_RUN_ID"),
        "effect": "REVIEWED_BASELINE_ONLY_NO_EVENT_CARET_FINDING_PUBLICATION_OR_EXTERNAL_ACTION",
    }
    log = state.setdefault("acknowledgement_log", [])
    log.append(record)
    state["acknowledgement_log"] = log[-MAX_ACKNOWLEDGEMENT_LOG:]
    return record


def append_history(path: Path, entry: dict[str, Any]) -> list[str]:
    warnings: list[str] = []
    existing: list[str] = []
    if path.exists():
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            try:
                value = json.loads(line)
                if not isinstance(value, dict):
                    raise ValueError("entry is not an object")
                existing.append(json.dumps(value, ensure_ascii=False, separators=(",", ":")))
            except Exception:
                warnings.append(f"ignored malformed cached history line {line_number}")
    existing.append(json.dumps(entry, ensure_ascii=False, separators=(",", ":")))
    trimmed = existing[-MAX_HISTORY_ENTRIES:]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(trimmed) + "\n", encoding="utf-8")
    return warnings


def normalize_html(raw: bytes, charset: str | None) -> str:
    encoding = charset or "utf-8"
    try:
        text = raw.decode(encoding, errors="replace")
    except LookupError:
        text = raw.decode("utf-8", errors="replace")
    text = re.sub(r"<(script|style|noscript|svg)\b[^>]*>.*?</\1\s*>", " ", text, flags=re.I | re.S)
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    return " ".join(text.split())


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1].lower()


def normalize_rss(raw: bytes) -> str:
    """Return a deterministic title/link/date set without preserving full bodies."""
    root = ET.fromstring(raw)
    records: list[str] = []
    for element in root.iter():
        if local_name(element.tag) not in {"item", "entry"}:
            continue
        values: dict[str, str] = {}
        for child in list(element):
            name = local_name(child.tag)
            if name in {"title", "link", "guid", "id", "pubdate", "published", "updated"}:
                if name == "link" and not (child.text or "").strip():
                    value = str(child.attrib.get("href", ""))
                else:
                    value = child.text or ""
                values[name] = " ".join(value.split())
        records.append(" | ".join(f"{key}={values[key]}" for key in sorted(values)))
    return "\n".join(sorted(set(records)))


def content_charset(content_type: str) -> str | None:
    match = re.search(r"charset\s*=\s*['\"]?([^;\s'\"]+)", content_type, flags=re.I)
    return match.group(1) if match else None


def fetch(source: dict[str, Any], timeout: float, max_bytes: int) -> tuple[bytes, dict[str, Any]]:
    if source.get("access_lane") != "AUTOMATED_SAFE":
        raise ValueError("source is not classified for automated public-safe access")
    headers = {"User-Agent": USER_AGENT, "Accept": "text/html,application/xhtml+xml,application/xml,application/rss+xml,application/pdf;q=0.9,*/*;q=0.5"}
    configured_headers = source.get("request_headers", {})
    if any(str(name).casefold() in PROHIBITED_REQUEST_HEADERS for name in configured_headers):
        raise ValueError("Authorization, Cookie and Proxy-Authorization headers are prohibited")
    headers.update(configured_headers)
    request = urllib.request.Request(source["url"], headers=headers)
    with urllib.request.urlopen(request, timeout=timeout) as response:
        status = int(getattr(response, "status", 200))
        raw = response.read(max_bytes + 1)
        if len(raw) > max_bytes:
            raise ValueError(f"response exceeds configured {max_bytes}-byte limit")
        metadata = {
            "http_status": status,
            "content_type": response.headers.get("Content-Type", ""),
            "etag": response.headers.get("ETag"),
            "last_modified": response.headers.get("Last-Modified"),
            "content_length": len(raw),
        }
        return raw, metadata


def normalize_source(source: dict[str, Any], raw: bytes, content_type: str) -> tuple[bytes, str]:
    source_type = source["source_type"]
    if source_type == "PDF":
        return raw, "BINARY_SHA256"
    if source_type == "RSS":
        normalized = normalize_rss(raw)
        return normalized.encode("utf-8"), "RSS_ENTRY_SET_SHA256"
    normalized = normalize_html(raw, content_charset(content_type))
    return normalized.encode("utf-8"), "HTML_VISIBLE_TEXT_SHA256"


def controlled_match(text: str, alias: str) -> bool:
    if not alias.strip():
        return False
    folded_text = text.casefold()
    folded_alias = alias.casefold().strip()
    pattern = r"(?<!\w)" + re.escape(folded_alias).replace(r"\ ", r"\s+") + r"(?!\w)"
    return re.search(pattern, folded_text) is not None


def match_ids(
    normalized: bytes,
    source: dict[str, Any],
    entities: dict[str, dict[str, Any]],
    terms: dict[str, dict[str, Any]],
    geography_terms: list[str],
) -> tuple[list[str], list[str], list[str]]:
    if source["source_type"] == "PDF":
        return [], [], []
    text = normalized.decode("utf-8", errors="replace")
    matched_entities: list[str] = []
    for entity_id in source.get("entity_ids", []):
        entity = entities.get(entity_id, {})
        aliases = [entity.get("display_name", ""), *entity.get("aliases", [])]
        if any(controlled_match(text, alias) for alias in aliases):
            matched_entities.append(entity_id)
    matched_terms: list[str] = []
    for term_id in source.get("transaction_term_ids", []):
        term = terms.get(term_id, {})
        if any(controlled_match(text, alias) for alias in term.get("aliases", [])):
            matched_terms.append(term_id)
    matched_geography = [term for term in geography_terms if controlled_match(text, term)]
    return sorted(matched_entities), sorted(matched_terms), sorted(set(matched_geography), key=str.casefold)


def classify_change(
    source: dict[str, Any],
    previous_fingerprint: str | None,
    fingerprint: str,
    matched_entities: list[str],
    matched_terms: list[str],
    matched_geography: list[str],
) -> str:
    if previous_fingerprint is None:
        return "BASELINE_ESTABLISHED"
    if previous_fingerprint == fingerprint:
        return "UNCHANGED"
    policy = source["change_review_policy"]
    if policy == "ANY_CHANGE":
        return "CONTENT_CHANGED_REVIEW_REQUIRED"
    if matched_entities and matched_terms and matched_geography:
        return "POTENTIAL_TRANSACTION_CHANGE_REVIEW_REQUIRED"
    return "CONTENT_CHANGED_NO_JOINT_SCOPE_MATCH"


def safe_error(exc: Exception) -> str:
    if isinstance(exc, urllib.error.HTTPError):
        return f"HTTP {exc.code}"
    if isinstance(exc, urllib.error.URLError):
        reason = getattr(exc, "reason", None)
        return f"network error: {type(reason).__name__ if reason is not None else 'URLError'}"
    if isinstance(exc, TimeoutError):
        return "network timeout"
    return f"{type(exc).__name__}: {str(exc)[:180]}"


def build_summary(report: dict[str, Any]) -> str:
    counts = report["counts"]
    lines = [
        "# FTI / Meeting Point public asset-transaction monitor",
        "",
        f"- Checked: `{report['checked_at']}`",
        f"- Status: **{report['status']}**",
        f"- Sources: {counts['total']} configured; {counts['fetched']} fetched; {counts['fetch_errors']} errors",
        f"- Review signals: {counts['review_required']}",
        f"- Sticky pending source-review windows: {counts['pending_changes']}",
        f"- Prior distinct fingerprints represented by rolling chains: {counts['compacted_prior_fingerprints']}",
        f"- Acknowledgements applied this run: {counts['acknowledgements_applied']}",
        f"- Prior state: {'available' if report['state_continuity']['prior_state_available'] else 'unavailable — fresh baseline only, not proof of no intervening change'}",
        "- Effect: change detection only; no transaction event, caret, allegation, website update or external notification is created automatically.",
        "- Durability: pending state and bounded history are cached and uploaded for 90 days; cache eviction/artifact expiry can cause a fresh baseline and are not an indefinite evidentiary archive.",
        "",
        "| Source | Priority | Change state | Pending | Matched entity IDs | Matched transaction-term IDs |",
        "| --- | --- | --- | ---: | --- | --- |",
    ]
    for item in report["sources"]:
        lines.append(
            "| {source} | {priority} | {state} | {pending} | {entities} | {terms} |".format(
                source=item["source_id"],
                priority=item["priority"],
                state=item["change_state"],
                pending=item.get("pending_count", 0),
                entities=", ".join(item.get("matched_entity_ids", [])) or "—",
                terms=", ".join(item.get("matched_transaction_term_ids", [])) or "—",
            )
        )
    lines.extend(
        [
            "",
            "Any review signal must be reconciled to the exact legal person, asset, capacity, date and primary source before the canonical register is changed.",
            "",
        ]
    )
    return "\n".join(lines)


def process_source(
    source: dict[str, Any],
    previous_item: dict[str, Any],
    prior_pending: list[dict[str, Any]],
    entities: dict[str, dict[str, Any]],
    terms: dict[str, dict[str, Any]],
    geography_terms: list[str],
    checked_at: str,
    timeout: float,
    max_bytes: int,
) -> tuple[dict[str, Any], dict[str, Any] | None, list[dict[str, Any]]]:
    source_id = source["source_id"]
    base_report = {
        "source_id": source_id,
        "configured_url": source["url"],
        "priority": source["priority"],
        "access_lane": source["access_lane"],
        "source_type": source["source_type"],
        "required": bool(source.get("required", False)),
        "change_review_policy": source["change_review_policy"],
        "automatic_event_created": False,
        "automatic_caret_assigned": False,
    }
    if not source.get("enabled", False):
        return (
            {
                **base_report,
                "change_state": "SOURCE_DISABLED",
                "review_required": bool(prior_pending),
                "pending_count": len(prior_pending),
                "pending_ids": [item.get("pending_id") for item in prior_pending],
            },
            None,
            prior_pending,
        )
    try:
        raw, metadata = fetch(source, timeout, max_bytes)
        normalized, normalization = normalize_source(source, raw, metadata["content_type"])
        fingerprint = hashlib.sha256(normalized).hexdigest()
        matched_entities, matched_terms, matched_geography = match_ids(normalized, source, entities, terms, geography_terms)
        acknowledged_fingerprint = previous_item.get("acknowledged_fingerprint") or previous_item.get("fingerprint")
        change_state = classify_change(
            source,
            acknowledged_fingerprint,
            fingerprint,
            matched_entities,
            matched_terms,
            matched_geography,
        )
        new_signal_requires_review = change_state in {
            "CONTENT_CHANGED_REVIEW_REQUIRED",
            "POTENTIAL_TRANSACTION_CHANGE_REVIEW_REQUIRED",
        }
        pending = normalize_pending_entries(source_id, prior_pending)
        new_pending = False
        superseding_observation = False
        if acknowledged_fingerprint is None:
            acknowledged_fingerprint = fingerprint
            baseline_origin = "FIRST_OBSERVED_BASELINE_NO_PRIOR_STATE"
        elif new_signal_requires_review:
            existing = pending[0] if pending else None
            if existing is None:
                identifier = pending_id(source_id, acknowledged_fingerprint, fingerprint)
                existing = {
                    "pending_id": identifier,
                    "source_id": source_id,
                    "baseline_fingerprint": acknowledged_fingerprint,
                    "observed_fingerprint": fingerprint,
                    "first_observed_fingerprint": fingerprint,
                    "fingerprint_chain_sha256": hashlib.sha256(fingerprint.encode("utf-8")).hexdigest(),
                    "distinct_fingerprint_count": 1,
                    "compacted_prior_fingerprint_count": 0,
                    "first_detected_at": checked_at,
                    "original_change_state": change_state,
                    "matched_entity_ids": matched_entities,
                    "matched_transaction_term_ids": matched_terms,
                    "matched_geography_terms": matched_geography,
                    "acknowledgement_required": True,
                    "effect": "UNREVIEWED_CHANGE_SIGNAL_ONLY_NOT_TRANSACTION_PROOF",
                    "queue_model": "ONE_STICKY_REVIEW_WINDOW_PER_SOURCE",
                }
                pending.append(existing)
                new_pending = True
            elif existing.get("observed_fingerprint") != fingerprint:
                previous_chain = existing.get("fingerprint_chain_sha256")
                if not isinstance(previous_chain, str) or not FINGERPRINT_RE.fullmatch(previous_chain):
                    previous_chain = hashlib.sha256(str(existing.get("observed_fingerprint", "")).encode("utf-8")).hexdigest()
                existing["fingerprint_chain_sha256"] = hashlib.sha256(
                    f"{previous_chain}\0{fingerprint}".encode("utf-8")
                ).hexdigest()
                existing["observed_fingerprint"] = fingerprint
                existing["distinct_fingerprint_count"] = int(existing.get("distinct_fingerprint_count", 1)) + 1
                existing["compacted_prior_fingerprint_count"] = existing["distinct_fingerprint_count"] - 1
                existing["last_change_state"] = change_state
                existing["matched_entity_ids"] = matched_entities
                existing["matched_transaction_term_ids"] = matched_terms
                existing["matched_geography_terms"] = matched_geography
                superseding_observation = True
            existing["last_seen_at"] = checked_at
            existing["times_seen"] = int(existing.get("times_seen", 0)) + 1
        elif change_state == "CONTENT_CHANGED_NO_JOINT_SCOPE_MATCH" and not pending:
            acknowledged_fingerprint = fingerprint
            baseline_origin = "AUTO_ADVANCED_AFTER_NO_JOINT_SCOPE_MATCH"
        if pending and not new_pending:
            change_state = "PENDING_ACKNOWLEDGEMENT"
        review_required = bool(pending)
        report_item = {
            **base_report,
            **metadata,
            "normalization": normalization,
            "fingerprint": fingerprint,
            "acknowledged_fingerprint": acknowledged_fingerprint,
            "previous_observed_fingerprint": previous_item.get("last_observed_fingerprint") or previous_item.get("fingerprint"),
            "change_state": change_state,
            "review_required": review_required,
            "new_pending_signal": new_pending,
            "superseding_pending_observation": superseding_observation,
            "pending_count": len(pending),
            "pending_ids": [item.get("pending_id") for item in pending],
            "matched_entity_ids": matched_entities,
            "matched_transaction_term_ids": matched_terms,
            "matched_geography_terms": matched_geography,
            "evidence_effect": "CHANGE_SIGNAL_ONLY_NOT_TRANSACTION_PROOF",
        }
        state_item = {
            "acknowledged_fingerprint": acknowledged_fingerprint,
            "last_observed_fingerprint": fingerprint,
            "normalization": normalization,
            "last_success_at": checked_at,
            "content_type": metadata["content_type"],
            "etag": metadata["etag"],
            "last_modified": metadata["last_modified"],
            "baseline_origin": locals().get("baseline_origin", previous_item.get("baseline_origin", "EXPLICIT_ACKNOWLEDGED_BASELINE")),
        }
        return report_item, state_item, pending
    except Exception as exc:
        return (
            {
                **base_report,
                "change_state": "FETCH_ERROR",
                "review_required": bool(prior_pending),
                "pending_count": len(prior_pending),
                "pending_ids": [item.get("pending_id") for item in prior_pending],
                "error": safe_error(exc),
                "acknowledged_fingerprint_retained": previous_item.get("acknowledged_fingerprint") or previous_item.get("fingerprint"),
                "evidence_effect": "SOURCE_AVAILABILITY_GAP_ONLY",
            },
            None,
            prior_pending,
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--register", default="assets/data/fti-meeting-point-canary-spain-asset-transaction-register-v1.json")
    parser.add_argument("--state-in", default="artifacts/fti-meeting-point-asset-transaction-monitor/state.json")
    parser.add_argument("--state-out", default="artifacts/fti-meeting-point-asset-transaction-monitor/state.json")
    parser.add_argument("--report", default="artifacts/fti-meeting-point-asset-transaction-monitor/report.json")
    parser.add_argument("--summary", default="artifacts/fti-meeting-point-asset-transaction-monitor/summary.md")
    parser.add_argument("--pending-output", default="artifacts/fti-meeting-point-asset-transaction-monitor/pending.json")
    parser.add_argument("--incident", default="artifacts/fti-meeting-point-asset-transaction-monitor/incident.json")
    parser.add_argument("--history", default="artifacts/fti-meeting-point-asset-transaction-monitor/history.jsonl")
    parser.add_argument("--acknowledgement", default=os.environ.get("FTI_TX_MONITOR_ACKNOWLEDGEMENT", ""))
    parser.add_argument("--acknowledgement-reason", default=os.environ.get("FTI_TX_MONITOR_ACKNOWLEDGEMENT_REASON", ""))
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--max-bytes", type=int, default=25_000_000)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--only-source", action="append", default=[])
    args = parser.parse_args()

    repo = Path(args.repo_root).resolve()
    register_path = repo / args.register
    checked_at = utc_now()
    try:
        register = load_json(register_path)
        if register.get("control_id") != REGISTER_CONTROL:
            raise ValueError("unexpected register control_id")
        previous_path = repo / args.state_in
        previous_raw = load_json(previous_path) if previous_path.exists() else {}
        previous = migrate_state(previous_raw, checked_at)
        if not previous_raw:
            previous.setdefault("state_warnings", []).append(
                {
                    "code": "NO_PRIOR_STATE_FRESH_BASELINE",
                    "at": checked_at,
                    "boundary": "Prior cache state was unavailable. First observations establish fresh baselines and cannot prove that no intervening source change occurred.",
                }
            )
        acknowledgement_record = apply_acknowledgement(
            previous,
            args.acknowledgement.strip(),
            args.acknowledgement_reason,
            checked_at,
        )
        previous_sources = previous.get("sources", {}) if isinstance(previous.get("sources", {}), dict) else {}
        previous_pending = previous.get("pending_changes", {}) if isinstance(previous.get("pending_changes", {}), dict) else {}
    except Exception as exc:
        print(f"CONFIG ERROR: {safe_error(exc)}", file=sys.stderr)
        return 2

    selected_ids = set(args.only_source)
    sources = [source for source in register["sources"] if not selected_ids or source["source_id"] in selected_ids]
    if selected_ids - {source["source_id"] for source in sources}:
        print(f"CONFIG ERROR: unknown --only-source IDs: {sorted(selected_ids - {source['source_id'] for source in sources})}", file=sys.stderr)
        return 2

    entities = {item["entity_id"]: item for item in register["known_entities"]}
    terms = {item["term_id"]: item for item in register["term_dictionary"]["transaction_terms"]}
    geography_terms = register["term_dictionary"]["geography_terms"]
    report_items: list[dict[str, Any]] = []
    next_sources: dict[str, Any] = dict(previous_sources)
    next_pending: dict[str, list[dict[str, Any]]] = {
        source_id: [dict(item) for item in entries if isinstance(item, dict)]
        for source_id, entries in previous_pending.items()
        if isinstance(entries, list)
    }

    workers = max(1, min(args.workers, 8, len(sources) or 1))
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        futures = []
        for source in sources:
            source_id = source["source_id"]
            previous_item = previous_sources.get(source_id, {}) if isinstance(previous_sources.get(source_id, {}), dict) else {}
            pending_items = next_pending.get(source_id, [])
            futures.append(
                executor.submit(
                    process_source,
                    source,
                    previous_item,
                    pending_items,
                    entities,
                    terms,
                    geography_terms,
                    checked_at,
                    args.timeout,
                    args.max_bytes,
                )
            )
        for source, future in zip(sources, futures):
            report_item, state_item, pending_items = future.result()
            report_items.append(report_item)
            if state_item is not None:
                next_sources[source["source_id"]] = state_item
            if pending_items:
                next_pending[source["source_id"]] = pending_items
            else:
                next_pending.pop(source["source_id"], None)

    counts = {
        "total": len(report_items),
        "fetched": sum(item["change_state"] not in {"FETCH_ERROR", "SOURCE_DISABLED"} for item in report_items),
        "fetch_errors": sum(item["change_state"] == "FETCH_ERROR" for item in report_items),
        "review_required": sum(bool(item.get("review_required")) for item in report_items),
        "baseline_established": sum(item["change_state"] == "BASELINE_ESTABLISHED" for item in report_items),
        "unchanged": sum(item["change_state"] == "UNCHANGED" for item in report_items),
        "pending_changes": sum(len(entries) for entries in next_pending.values()),
        "pending_sources": sum(bool(entries) for entries in next_pending.values()),
        "acknowledgements_applied": 1 if acknowledgement_record is not None else 0,
        "compacted_prior_fingerprints": sum(
            int(item.get("compacted_prior_fingerprint_count", 0))
            for entries in next_pending.values()
            for item in entries
        ),
    }
    pending_window_summaries = [
        {
            "source_id": source_id,
            "pending_id": item.get("pending_id"),
            "latest_observed_fingerprint": item.get("observed_fingerprint"),
            "fingerprint_chain_sha256": item.get("fingerprint_chain_sha256"),
            "distinct_fingerprint_count": item.get("distinct_fingerprint_count", 1),
            "first_detected_at": item.get("first_detected_at"),
            "last_seen_at": item.get("last_seen_at"),
        }
        for source_id in sorted(next_pending)
        for item in next_pending[source_id]
    ]
    required_errors = [item["source_id"] for item in report_items if item["change_state"] == "FETCH_ERROR" and item["required"]]
    if required_errors and counts["pending_changes"]:
        status = "FAIL_REQUIRED_SOURCE_FAILURES_WITH_PENDING_REVIEW"
    elif required_errors:
        status = "FAIL_REQUIRED_SOURCE_FAILURES"
    elif counts["pending_changes"]:
        status = "REVIEW_REQUIRED"
    elif counts["fetch_errors"]:
        status = "PASS_WITH_OPTIONAL_SOURCE_FAILURES"
    else:
        status = "PASS"

    report: dict[str, Any] = {
        "schema": REPORT_SCHEMA,
        "control_id": REGISTER_CONTROL,
        "checked_at": checked_at,
        "github_sha": os.environ.get("GITHUB_SHA"),
        "status": status,
        "counts": counts,
        "required_source_failures": required_errors,
        "pending_change_ids": [
            item.get("pending_id")
            for source_id in sorted(next_pending)
            for item in next_pending[source_id]
        ],
        "pending_windows": pending_window_summaries,
        "acknowledgements_applied": [acknowledgement_record] if acknowledgement_record is not None else [],
        "sources": report_items,
        "non_inference_guard": "A content change or controlled-term co-occurrence is a review signal only. It does not prove a transaction, identity, capacity, date, asset inclusion, knowledge, causation, wrongdoing or liability.",
        "automatic_register_mutation": False,
        "automatic_website_mutation": False,
        "automatic_external_action": False,
        "state_continuity": {
            "prior_state_available": bool(previous_raw),
            "fresh_baseline_boundary": (
                "PRIOR_STATE_AVAILABLE"
                if previous_raw
                else "NO_PRIOR_STATE_FRESH_BASELINE_NOT_PROOF_OF_NO_INTERVENING_CHANGE"
            ),
            "cache_and_artifact_boundary": "GitHub cache and uploaded artifacts can be evicted or expire after 90 days; they are not an indefinite evidentiary archive.",
        },
    }
    next_state = {
        "schema": STATE_SCHEMA,
        "control_id": REGISTER_CONTROL,
        "updated_at": checked_at,
        "sources": next_sources,
        "pending_changes": next_pending,
        "acknowledgement_log": previous.get("acknowledgement_log", [])[-MAX_ACKNOWLEDGEMENT_LOG:],
        "state_warnings": previous.get("state_warnings", []),
    }

    pending_output = {
        "schema": PENDING_SCHEMA,
        "control_id": REGISTER_CONTROL,
        "checked_at": checked_at,
        "count": counts["pending_changes"],
        "source_count": counts["pending_sources"],
        "pending_changes": next_pending,
        "queue_model": "ONE_STICKY_REVIEW_WINDOW_PER_SOURCE",
        "acknowledgement_required": bool(next_pending),
        "acknowledgement_boundary": "Each source has one bounded sticky review window. Its exact latest SOURCE_ID=SHA256 and rolling fingerprint chain require an explicit public-safe review reason. Acknowledgement updates only the reviewed baseline; it creates no event, caret, finding, publication or external action.",
        "compaction_boundary": "When a source changes again before review, the queue retains the exact first/latest fingerprints, distinct count and rolling SHA-256 chain in one sticky window; per-run public-safe history records each chain state. Intermediate source bodies are never stored.",
    }
    run_id = os.environ.get("GITHUB_RUN_ID")
    server_url = os.environ.get("GITHUB_SERVER_URL")
    repository = os.environ.get("GITHUB_REPOSITORY")
    run_url = f"{server_url}/{repository}/actions/runs/{run_id}" if server_url and repository and run_id else None
    incident = {
        "schema": INCIDENT_SCHEMA,
        "control_id": REGISTER_CONTROL,
        "incident_id": f"FTI-TX-MONITOR-{run_id or checked_at.replace(':', '').replace('+', '-')}",
        "checked_at": checked_at,
        "state": "OPEN" if required_errors or next_pending else ("NOTICE" if not previous_raw else "CLEAR"),
        "severity": "ERROR" if required_errors else ("WARNING" if next_pending or not previous_raw else "NONE"),
        "status": status,
        "required_source_failures": required_errors,
        "pending_change_ids": report["pending_change_ids"],
        "pending_windows": pending_window_summaries,
        "workflow_run_url": run_url,
        "automatic_external_notification": False,
        "visibility_boundary": "A non-green GitHub workflow and public-safe artifact are repository-maintenance signals, not notice to any authority, party, investor, creditor or other external recipient.",
        "durability_boundary": "The contents-read workflow cannot commit an incident. Cache and artifacts can be evicted and artifacts expire after 90 days; a reviewed canonical repository update is required for indefinite preservation.",
    }
    history_entry = {
        "schema": HISTORY_SCHEMA,
        "control_id": REGISTER_CONTROL,
        "checked_at": checked_at,
        "github_run_id": run_id,
        "github_sha": os.environ.get("GITHUB_SHA"),
        "status": status,
        "counts": counts,
        "required_source_failures": required_errors,
        "pending_change_ids": report["pending_change_ids"],
        "pending_windows": pending_window_summaries,
        "source_states": {item["source_id"]: item["change_state"] for item in report_items},
        "effect": "PUBLIC_SAFE_MONITOR_HISTORY_ONLY_NO_TRANSACTION_FINDING_OR_EXTERNAL_ACTION",
    }

    history_warnings = append_history(repo / args.history, history_entry)
    if history_warnings:
        report["history_warnings"] = history_warnings
        incident["history_warnings"] = history_warnings
        next_state.setdefault("state_warnings", []).extend(
            {"code": "HISTORY_RECOVERY_WARNING", "at": checked_at, "boundary": warning}
            for warning in history_warnings
        )

    write_json(repo / args.report, report)
    write_json(repo / args.state_out, next_state)
    write_json(repo / args.pending_output, pending_output)
    write_json(repo / args.incident, incident)
    summary = build_summary(report)
    summary_path = repo / args.summary
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(summary, encoding="utf-8")

    print(
        f"FTI / Meeting Point asset-transaction monitor: {status}; "
        f"sources={counts['total']} fetched={counts['fetched']} "
        f"review={counts['review_required']} errors={counts['fetch_errors']}"
    )
    for source_id in required_errors:
        print(f"ERROR: required source unavailable: {source_id}", file=sys.stderr)
    if required_errors:
        return 3
    if counts["pending_changes"]:
        print("ERROR: one or more change fingerprints require explicit review and acknowledgement", file=sys.stderr)
        return 4
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
