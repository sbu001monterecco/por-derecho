#!/usr/bin/env python3
"""Validate the finite first-hop caret census and rendered provenance.

The 27-28 August control remains an immutable historical census of eighteen
rendered ``<main>`` surfaces and 130 deduplicated identity-eligible objects. A
later public-surface control may declare a narrowly scoped, blob-pinned successor
for a route whose editorial occurrence layer intentionally changed.

For an authorised successor surface this validator requires:

* exact predecessor snapshot linkage;
* an exact Git blob SHA-1 for the successor page;
* only the declared, already-confirmed CAEPR IDs;
* a confirmed state on every machine-readable identity occurrence;
* visible caret presentation; and
* continued presence of every predecessor proof literal assigned to that route.

The other first-hop surfaces retain the original normalized length/hash, exact
proof-count and no-inline-caret rules. Identity reconciliation never establishes
conduct, knowledge, intent, wrongdoing, liability or outcome.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
import unicodedata
from collections import Counter
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "assets/data/caepr-caret-alberto-meeting-point-first-hop-v1.json"
SUCCESSOR_DATA = ROOT / "assets/data/caret-public-surface-coverage-v1.json"
CONTROL_ID = "PD-ALV-MP357-FIRST-HOP-CARET-20260827-01"
SUCCESSOR_CONTROL_ID = "PD-SP-CARET-SURFACE-20260902-01"
NODE_IDS = {f"AM357-N{number:02d}" for number in range(1, 10)}
EXPECTED_TYPE_COUNTS = {
    "PERSON": {"eligible": 27, "confirmed": 12, "pending": 15, "suspended": 0},
    "ORGANISATION_OR_PERIMETER": {"eligible": 64, "confirmed": 30, "pending": 34, "suspended": 0},
    "INSTITUTION_OR_SUBORGAN": {"eligible": 25, "confirmed": 13, "pending": 12, "suspended": 0},
    "PROCEEDING": {"eligible": 14, "confirmed": 6, "pending": 8, "suspended": 0},
}
EXPECTED_GUARDS = {
    "Carlos": ("CARLOS_PWC", "CARET_PENDING"),
    "José D.": ("JOSE_DANIEL_ACOSTA_MATOS", "CARET_CONFIRMED"),
    "Irigoyen": ("DANIEL_IRIGOYEN", "CARET_CONFIRMED"),
    "Laura Acosta Matos": ("LAURA_PATRICIA_ACOSTA_MATOS", "CARET_CONFIRMED"),
    "Community / Comunidad": ("BARE_COMMUNITY", "CARET_PENDING"),
}


class MainSurface(HTMLParser):
    """Extract rendered ``main`` text and classify identity/caret markup."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.main_depth = 0
        self.skip_depth = 0
        self.sup_depth = 0
        self.parts: list[str] = []
        self.caepr_occurrences: list[tuple[str, str]] = []
        self.prohibited_identity_markup: list[str] = []
        self.visible_caret_sup_count = 0

    def handle_starttag(self, tag: str, attrs_list: list[tuple[str, str | None]]) -> None:
        attrs = {key: value or "" for key, value in attrs_list}
        if tag == "main":
            self.main_depth += 1
        if self.main_depth:
            classes = set(attrs.get("class", "").split())
            if "data-caepr-id" in attrs:
                self.caepr_occurrences.append(
                    (attrs["data-caepr-id"], attrs.get("data-caret-state", ""))
                )
            if "data-caret-id" in attrs or "caret" in classes:
                self.prohibited_identity_markup.append(tag)
            if tag == "sup":
                self.sup_depth += 1
            if (
                self.skip_depth
                or tag in {"script", "style", "template", "noscript"}
                or "hidden" in attrs
                or attrs.get("aria-hidden") == "true"
            ):
                self.skip_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if self.main_depth and self.skip_depth:
            self.skip_depth -= 1
        if self.main_depth and tag == "sup" and self.sup_depth:
            self.sup_depth -= 1
        if tag == "main":
            self.main_depth -= 1

    def handle_data(self, data: str) -> None:
        if self.main_depth and not self.skip_depth:
            self.parts.append(data)
            if self.sup_depth and "^" in data:
                self.visible_caret_sup_count += data.count("^")


def normalize(value: str) -> str:
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", unescape(value))).strip()


def route_path(route: str) -> Path:
    if not isinstance(route, str) or not route.startswith("/") or not route.endswith("/"):
        raise ValueError(f"unsafe or non-canonical route: {route!r}")
    candidate = (ROOT / route.strip("/") / "index.html").resolve()
    candidate.relative_to(ROOT.resolve())
    return candidate


def safe_path(relative: str) -> Path:
    candidate = Path(relative)
    if candidate.is_absolute() or ".." in candidate.parts:
        raise ValueError(f"unsafe repository path: {relative!r}")
    resolved = (ROOT / candidate).resolve()
    resolved.relative_to(ROOT.resolve())
    return resolved


def git_blob_sha1(payload: bytes) -> str:
    return hashlib.sha1(f"blob {len(payload)}\0".encode("ascii") + payload).hexdigest()


errors: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def load_object(path: Path, label: str) -> dict[str, Any]:
    check(path.is_file(), f"{label} is missing")
    if not path.is_file():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"cannot parse {label}: {exc}")
        return {}
    if not isinstance(payload, dict):
        errors.append(f"{label} root is not an object")
        return {}
    return payload


payload = load_object(DATA, "first-hop caret control")
successor_payload = load_object(SUCCESSOR_DATA, "caret public-surface successor control")
if not payload or not successor_payload:
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    raise SystemExit(1)

records = payload.get("records") or []
counts = payload.get("counts") or {}
check(payload.get("control_id") == CONTROL_ID, "first-hop control ID drift")
check(payload.get("status") == "PARTIAL_NOT_ALL_IS", "first-hop status is not partial")
check(
    (counts.get("eligible"), counts.get("confirmed"), counts.get("pending"), counts.get("suspended"))
    == (130, 61, 69, 0),
    "first-hop count is not 130/61/69/0",
)
check(counts.get("by_type") == EXPECTED_TYPE_COUNTS, "first-hop type counts drift")
check(isinstance(records, list) and len(records) == 130, "first-hop records are not exactly 130")
check(
    [item.get("ordinal") for item in records] == list(range(1, 131)),
    "record ordinals are not 1..130",
)

record_by_key = {item.get("object_key"): item for item in records if isinstance(item, dict)}
check(len(record_by_key) == 130 and None not in record_by_key, "record keys are not 130 unique values")
state_counts = Counter(item.get("state") for item in records if isinstance(item, dict))
check(
    state_counts == Counter({"CARET_PENDING": 69, "CARET_CONFIRMED": 61}),
    "record state split drift",
)
for item in records:
    if not isinstance(item, dict):
        continue
    if item.get("state") == "CARET_CONFIRMED":
        check(bool(item.get("caepr_id")), f"confirmed {item.get('object_key')} lacks a CAEPR ID")
    elif item.get("state") == "CARET_PENDING":
        check("caepr_id" not in item, f"pending {item.get('object_key')} carries an admitted CAEPR ID")
        check(bool(item.get("next_source_needed")), f"pending {item.get('object_key')} lacks its next source")

route_scope = payload.get("route_scope") or []
check(len(route_scope) == 9, "route scope is not nine semantic node pairs")
check(
    {item.get("node_id") for item in route_scope if isinstance(item, dict)} == NODE_IDS,
    "route nodes drift",
)
expected_routes: dict[tuple[str, str], str] = {}
for item in route_scope:
    if not isinstance(item, dict):
        continue
    for language in ("es", "en"):
        route = item.get(language)
        expected_routes[(item.get("node_id"), language)] = route
        try:
            check(route_path(route).is_file(), f"missing controlled route {route}")
        except (TypeError, ValueError):
            errors.append(f"invalid controlled route {route!r}")

control = payload.get("rendered_occurrence_control") or {}
check(
    control.get("schema") == "por-derecho.rendered-route-occurrence-provenance.v1",
    "provenance schema drift",
)
check(
    control.get("mapping_granularity")
    == "DEDUPLICATED_OBJECT_WITH_FROZEN_ROUTE_SURFACES_AND_ONE_EXACT_BODY_ANCHOR",
    "provenance mapping granularity drift",
)
check(
    "does not pretend" in str(control.get("machine_attestation_limit", "")),
    "machine limit is not candid",
)
check(
    str(control.get("inline_rendering_policy", "")).startswith(
        "NO_INLINE_CARETS_ON_FIRST_HOP_SOURCE_ROUTES"
    ),
    "historical no-inline-caret policy missing",
)
check(len(control.get("explicit_occurrence_exclusions") or []) == 4, "occurrence exclusions drift")

snapshots = control.get("route_snapshots") or []
snapshot_by_surface = {
    (item.get("node_id"), item.get("language")): item
    for item in snapshots
    if isinstance(item, dict)
}
check(len(snapshots) == len(snapshot_by_surface) == 18, "surface snapshot set is not 18 unique routes")
check(set(snapshot_by_surface) == set(expected_routes), "surface snapshot keys do not match route scope")

check(
    successor_payload.get("schema") == "por-derecho.caret-public-surface-coverage.v1",
    "successor control schema drift",
)
check(successor_payload.get("control_id") == SUCCESSOR_CONTROL_ID, "successor control ID drift")
successor = successor_payload.get("first_hop_successor") or {}
check(successor.get("predecessor_control_id") == CONTROL_ID, "successor predecessor ID drift")
check(
    successor.get("predecessor_control_path")
    == "assets/data/caepr-caret-alberto-meeting-point-first-hop-v1.json",
    "successor predecessor path drift",
)
check(successor.get("successor_control_id") == SUCCESSOR_CONTROL_ID, "successor self-ID drift")
check(
    successor.get("policy")
    == "HISTORICAL_SNAPSHOT_IMMUTABLE_SUCCESSOR_BLOB_PINNED_DECLARED_CONFIRMED_IDENTITIES_ONLY",
    "successor exception policy drift",
)

successor_rows = successor.get("surfaces") or []
successor_by_surface = {
    (item.get("node_id"), item.get("language")): item
    for item in successor_rows
    if isinstance(item, dict)
}
check(len(successor_rows) == len(successor_by_surface) == 2, "successor surface set is not two unique routes")
check(set(successor_by_surface) == {("AM357-N07", "es"), ("AM357-N07", "en")}, "successor scope escaped AM357-N07")

strict_surface_ids: dict[tuple[str, str], set[str]] = {}
for item in successor_payload.get("strict_surfaces") or []:
    if not isinstance(item, dict):
        continue
    surface = (item.get("first_hop_node_id"), item.get("language"))
    strict_surface_ids[surface] = {
        row.get("id")
        for row in item.get("records") or []
        if isinstance(row, dict) and isinstance(row.get("id"), str)
    }

surface_text: dict[tuple[str, str], str] = {}
for surface, route in expected_routes.items():
    try:
        path = route_path(route)
    except (TypeError, ValueError):
        continue
    raw = path.read_bytes()
    parser = MainSurface()
    parser.feed(raw.decode("utf-8"))
    text = normalize(" ".join(parser.parts))
    surface_text[surface] = text
    predecessor = snapshot_by_surface.get(surface) or {}
    check(predecessor.get("route") == route, f"snapshot route drift for {surface}")

    successor_row = successor_by_surface.get(surface)
    if successor_row:
        check(successor_row.get("route") == route, f"successor route drift for {surface}")
        try:
            successor_path = safe_path(str(successor_row.get("path")))
            check(successor_path == path, f"successor path/route mismatch for {surface}")
        except (TypeError, ValueError):
            errors.append(f"unsafe successor path for {surface}")
        check(
            successor_row.get("predecessor_normalized_characters")
            == predecessor.get("normalized_characters"),
            f"successor predecessor length drift for {surface}",
        )
        check(
            successor_row.get("predecessor_normalized_main_sha256")
            == predecessor.get("normalized_main_sha256"),
            f"successor predecessor hash drift for {surface}",
        )
        expected_blob = successor_row.get("expected_git_blob_sha1")
        check(
            isinstance(expected_blob, str) and re.fullmatch(r"[0-9a-f]{40}", expected_blob) is not None,
            f"successor blob SHA is invalid for {surface}",
        )
        check(git_blob_sha1(raw) == expected_blob, f"successor blob drift for {surface}")

        permitted = set(successor_row.get("permitted_identity_ids") or [])
        required = set(successor_row.get("required_identity_ids") or [])
        observed = [identity_id for identity_id, _ in parser.caepr_occurrences]
        observed_set = set(observed)
        check(permitted == strict_surface_ids.get(surface), f"successor/strict ID mismatch for {surface}")
        check(required <= permitted, f"successor required IDs escape permitted set for {surface}")
        check(observed_set <= permitted, f"undeclared CAEPR ID on successor surface {surface}")
        check(required <= observed_set, f"required CAEPR ID absent from successor surface {surface}")
        for identity_id, state in parser.caepr_occurrences:
            check(identity_id in permitted, f"unpermitted CAEPR ID {identity_id} on {route}")
            check(state == "CARET_CONFIRMED", f"non-confirmed occurrence state for {identity_id} on {route}")
        minimum_carets = successor_row.get("minimum_visible_caret_occurrences")
        check(
            isinstance(minimum_carets, int) and minimum_carets >= 1,
            f"invalid minimum visible caret count for {surface}",
        )
        if isinstance(minimum_carets, int):
            check(
                parser.visible_caret_sup_count >= minimum_carets,
                f"visible caret minimum not met for {surface}",
            )
        check(not parser.prohibited_identity_markup, f"legacy/uncontrolled caret markup on {route}")
        if not successor_row.get("plain_caret_labels_permitted"):
            check(
                text.count("^") == parser.visible_caret_sup_count,
                f"plain caret labels are not permitted on {route}",
            )
    else:
        check(
            predecessor.get("normalized_characters") == len(text),
            f"snapshot length drift for {surface}",
        )
        check(
            predecessor.get("normalized_main_sha256")
            == hashlib.sha256(text.encode("utf-8")).hexdigest(),
            f"snapshot hash drift for {surface}",
        )
        check(not parser.caepr_occurrences, f"uncontrolled inline CAEPR markup on {route}")
        check(not parser.prohibited_identity_markup, f"uncontrolled inline caret markup on {route}")
        check("^" not in text, f"uncontrolled inline caret character on {route}")

provenance = control.get("record_provenance") or []
check(len(provenance) == 130, "record provenance is not exactly 130 entries")
check(
    [item.get("ordinal") for item in provenance if isinstance(item, dict)] == list(range(1, 131)),
    "provenance ordinals drift",
)
provenance_keys = [item.get("object_key") for item in provenance if isinstance(item, dict)]
check(len(provenance_keys) == len(set(provenance_keys)) == 130, "provenance keys are not unique")
check(set(provenance_keys) == set(record_by_key), "provenance is not a bijection over the 130 records")

for item in provenance:
    if not isinstance(item, dict):
        continue
    key = item.get("object_key")
    record = record_by_key.get(key) or {}
    check(item.get("ordinal") == record.get("ordinal"), f"provenance ordinal drift for {key}")
    check(item.get("state") == record.get("state"), f"provenance state drift for {key}")
    proof = item.get("proof_occurrence") or {}
    surface = (proof.get("node_id"), proof.get("language"))
    check(surface in expected_routes, f"unknown proof surface for {key}: {surface}")
    check(proof.get("route") == expected_routes.get(surface), f"proof route drift for {key}")
    literal = proof.get("normalized_literal")
    check(isinstance(literal, str) and bool(literal.strip()), f"empty proof literal for {key}")
    if isinstance(literal, str) and surface in surface_text:
        actual_count = surface_text[surface].casefold().count(normalize(literal).casefold())
        check(actual_count > 0, f"proof literal is absent from rendered body for {key}")
        if surface not in successor_by_surface:
            check(
                actual_count == proof.get("normalized_occurrence_count"),
                f"proof occurrence count drift for {key}",
            )

guards = payload.get("occurrence_guards") or []
guard_by_display = {item.get("display"): item for item in guards if isinstance(item, dict)}
check(set(guard_by_display) == set(EXPECTED_GUARDS), "occurrence guard display set drift")
for display, (key, state) in EXPECTED_GUARDS.items():
    guard = guard_by_display.get(display) or {}
    check(guard.get("object_key") == key, f"guard object mapping drift for {display}")
    check(guard.get("required_state") == state, f"guard state drift for {display}")
    check((record_by_key.get(key) or {}).get("state") == state, f"guard/record state mismatch for {display}")
    check(
        guard.get("rendering_policy") == "NO_INLINE_CARET_UNTIL_OCCURRENCE_RECONCILED",
        f"guard does not block inline caret for {display}",
    )

if errors:
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    raise SystemExit(1)

print("PASS: historical first-hop census remains 130 objects; 61 confirmed / 69 pending")
print("PASS: 16 predecessor surfaces retain exact normalized snapshots and proof counts")
print("PASS: 2 AM357-N07 successor surfaces are exact-blob pinned and ID restricted")
print("PASS: predecessor proof literals remain present; no pending identity was promoted")
