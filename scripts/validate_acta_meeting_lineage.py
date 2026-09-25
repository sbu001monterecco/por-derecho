#!/usr/bin/env python3
"""Validate ACTA event lineage, continuity data, accessibility and interlinks.

All cardinalities are derived from the controlled indexes. A newly located
event or source family therefore expands the test surface instead of requiring
another hard-coded 20/17 edit.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from html import escape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

from acta_capacity_sequence_annotations import (
    ADVERSE_SEQUENCE_MODEL,
    EVENT_ANNOTATIONS,
    EVENT_IDS,
)
from acta_document_localization import (
    LOCALIZED_FIELDS,
    STABLE_NAMES_OR_TERMS,
    localize_document_value,
    localization_status,
    validate_scalar_coverage,
)
from acta_event_actor_routes import (
    ACTOR_ROUTE_CATALOG,
    ROUTE_INFERENCE_BOUNDARY,
    actor_route_gaps_for_event,
    actor_routes_for_event,
)
from acta_owner_role_matrix import OWNER_ROLE_MATRIX, PRE_2008_CONTROL, PRINCIPAL_LINEAGES


REPO = Path(__file__).resolve().parents[1]
INDEX = REPO / "evidence/community/actas/meeting-lineage-index-v1.json"
CONTINUITY = REPO / "evidence/community/actas/event-family-continuity-v1.json"
PUBLIC_INDEX = REPO / "evidence/community/actas/public-index.json"
RECONCILIATION = REPO / "evidence/community/actas/source-family-reconciliation-v2.json"
PUBLIC_REGISTER = REPO / "evidence/community/COMMUNITY_AUTHORITY_EVENTS_EMAILS_MEETINGS_ACTAS_PUBLIC_REGISTER.md"
CSS = REPO / "assets/acta-document-room-20260822.css"
JS = REPO / "assets/acta-document-room-20260822.js"
SITEMAP = REPO / "sitemap.xml"
BASE_URL = "https://sbu001monterecco.github.io/por-derecho"
ROOMS = {
    "es": REPO / "es/comunidad-instrumentalizacion/sala-documental-actas/index.html",
    "en": REPO / "en/community-instrumentalisation/acta-document-room/index.html",
}
CHRONOLOGIES = {
    "es": REPO / "es/comunidad-instrumentalizacion/actas-2011-2022/index.html",
    "en": REPO / "en/community-instrumentalisation/minutes-2011-2022/index.html",
}

EXPECTED_PERIMETERS = {
    "pre_sale_montelanza": ("A", "A"),
    "project_lpb_aweswell_gil": ("B", "B"),
    "adverse_montelanza_molina": ("C1", "C"),
    "adverse_acosta_matos": ("C2", "C"),
    "mixed_or_contested": ("D-MIXED", "D"),
    "unresolved": ("D-OPEN", "D"),
}
PERIMETER_LABELS = {
    "pre_sale_montelanza": {"es": "Montelanza · pre-venta", "en": "Montelanza · pre-sale"},
    "project_lpb_aweswell_gil": {
        "es": "Proyecto · Multimatrix/LPB → Aweswell/LPB–Gil",
        "en": "Project · Multimatrix/LPB → Aweswell/LPB–Gil",
    },
    "adverse_montelanza_molina": {
        "es": "Adverso alegado · AAS → FMMM/Cogolludo/Pamanil",
        "en": "Alleged adverse · AAS → FMMM/Cogolludo/Pamanil",
    },
    "adverse_acosta_matos": {
        "es": "Adverso alegado · Acosta Matos/CAM",
        "en": "Alleged adverse · Acosta Matos/CAM",
    },
    "mixed_or_contested": {"es": "Mixto o controvertido", "en": "Mixed or contested"},
    "unresolved": {"es": "No resuelto", "en": "Unresolved"},
}
EVENT_FIELDS = (
    "stable_id",
    "documented_date_or_range",
    "document_type",
    "issuer_sender",
    "stated_capacity",
    "recipients",
    "meeting_body_if_any",
    "documented_convener",
    "perimeter",
    "perimeter_code",
    "source_provenance_status",
    "public_private_status",
    "relationship_to_other_documents_or_events",
    "unresolved_evidential_issues",
    "bilingual_event_routes",
    "document_record_ids",
    "continuity_audit",
    "patricia_dominguez_capacity",
    "adverse_sequence_stage",
)
DOCUMENT_FIELDS = (
    "stable_id",
    "event_family_ids",
    "documented_date_or_range",
    "document_type",
    "relationship_stage",
    "issuer_sender",
    "stated_capacity",
    "recipients",
    "meeting_body_if_any",
    "documented_convener",
    "perimeter",
    "perimeter_code",
    "source_provenance_status",
    "public_private_status",
    "relationship_to_other_documents_or_event",
    "unresolved_evidential_issues",
    "bilingual_event_routes",
)
AUDIT_FIELDS = (
    "before",
    "knowledge",
    "notice_service",
    "omitted_excluded_allegation",
    "convener",
    "body",
    "attendance_representation",
    "resolutions_proposed_voted",
    "objections",
    "minutes_versions",
    "circulation_receipt_withholding",
    "implementation",
    "later_reliance",
    "contradictions",
    "unproved",
)


def present(value: object) -> bool:
    """Treat explicit zero/false as data while rejecting empty placeholders."""
    return value is not None and value != "" and value != [] and value != {}


def nested_source_document_ids(value: object) -> set[str]:
    """Collect source_document_id values without assuming one index shape."""
    found: set[str] = set()
    if isinstance(value, dict):
        source_id = value.get("source_document_id")
        if isinstance(source_id, str) and source_id:
            found.add(source_id)
        for child in value.values():
            found.update(nested_source_document_ids(child))
    elif isinstance(value, list):
        for child in value:
            found.update(nested_source_document_ids(child))
    return found


def validate_package_source_controls(
    reconciliation: dict,
    continuity_documents: dict[str, dict],
    public_index: dict,
    errors: list[str],
) -> None:
    """Require one canonical continuity record for every package-side binary.

    A shared byte count is not identity.  Each reconciliation row therefore has
    one stable source ID and must match the continuity record on bytes, pages
    and SHA-256.  The same control is also required in its per-package manifest
    and public-index record.
    """

    rows_by_id: dict[str, list[tuple[str, str, dict]]] = defaultdict(list)
    controls_by_slug: dict[str, dict] = {}
    variants_by_slug: dict[str, list[dict]] = {}
    for family in reconciliation.get("families", []):
        slug = family.get("slug", "<missing-slug>")
        control = family.get("controlling_copy")
        if not isinstance(control, dict):
            errors.append(f"source reconciliation {slug}: missing controlling_copy")
            continue
        controls_by_slug[slug] = control
        variants = family.get("additional_variants", [])
        if not isinstance(variants, list):
            errors.append(f"source reconciliation {slug}: additional_variants is not a list")
            variants = []
        variants_by_slug[slug] = [row for row in variants if isinstance(row, dict)]
        for role, row in [("control", control), *[("variant", item) for item in variants_by_slug[slug]]]:
            source_id = row.get("source_document_id")
            if not isinstance(source_id, str) or not source_id:
                errors.append(f"source reconciliation {slug}/{role}: missing source_document_id")
                continue
            rows_by_id[source_id].append((slug, role, row))

    duplicate_package_ids = sorted(
        source_id for source_id, rows in rows_by_id.items() if len(rows) != 1
    )
    if duplicate_package_ids:
        errors.append(
            "package-side source IDs do not resolve one-to-one: "
            + ", ".join(duplicate_package_ids)
        )

    aliases: dict[str, str] = {}
    for source_id, document in continuity_documents.items():
        for alias in document.get("legacy_id_aliases", []):
            if alias in continuity_documents:
                errors.append(
                    f"continuity source alias {alias} collides with a canonical stable ID"
                )
            prior = aliases.get(alias)
            if prior and prior != source_id:
                errors.append(
                    f"continuity source alias {alias} resolves to both {prior} and {source_id}"
                )
            aliases[alias] = source_id

    def integrity_tuple(value: dict) -> tuple[object, object, object]:
        return value.get("bytes"), value.get("pages"), value.get("sha256")

    for source_id, rows in rows_by_id.items():
        if len(rows) != 1:
            continue
        slug, role, row = rows[0]
        document = continuity_documents.get(source_id)
        if document is None:
            errors.append(
                f"source reconciliation {slug}/{role}: {source_id} has no canonical continuity record"
            )
            continue
        continuity_integrity = document.get("integrity", {})
        expected = integrity_tuple(row)
        actual = (
            continuity_integrity.get("size_bytes"),
            continuity_integrity.get("page_count"),
            continuity_integrity.get("sha256"),
        )
        if expected != actual:
            errors.append(
                f"source reconciliation {slug}/{source_id}: bytes/pages/SHA-256 "
                f"{expected!r} != continuity {actual!r}"
            )
        row_aliases = set(row.get("legacy_id_aliases", []))
        continuity_aliases = set(document.get("legacy_id_aliases", []))
        if not row_aliases.issubset(continuity_aliases):
            errors.append(
                f"source reconciliation {slug}/{source_id}: legacy aliases are not preserved in continuity"
            )

    manifest_root = REPO / "evidence/community/actas"
    for slug, control in controls_by_slug.items():
        manifest_path = manifest_root / slug / "manifest.json"
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"source reconciliation {slug}: manifest unavailable: {exc}")
            continue
        source = manifest.get("source", {})
        expected_control = (
            control.get("source_document_id"),
            control.get("bytes"),
            control.get("pages"),
            control.get("sha256"),
        )
        actual_control = (
            source.get("source_document_id"),
            source.get("bytes"),
            source.get("pages"),
            source.get("sha256"),
        )
        if expected_control != actual_control:
            errors.append(
                f"source reconciliation {slug}: manifest control {actual_control!r} "
                f"!= reconciliation {expected_control!r}"
            )
        expected_variants = {
            row.get("source_document_id"): row
            for row in variants_by_slug.get(slug, [])
        }
        manifest_variants = {
            row.get("source_document_id"): row
            for row in source.get("additional_source_documents", [])
            if isinstance(row, dict) and isinstance(row.get("source_document_id"), str)
        }
        if set(expected_variants) != set(manifest_variants):
            errors.append(
                f"source reconciliation {slug}: manifest variant IDs differ from reconciliation"
            )
        for source_id in set(expected_variants) & set(manifest_variants):
            expected_variant = expected_variants[source_id]
            manifest_variant = manifest_variants[source_id]
            if integrity_tuple(expected_variant) != integrity_tuple(manifest_variant):
                errors.append(
                    f"source reconciliation {slug}/{source_id}: manifest variant "
                    "bytes/pages/SHA-256 differ"
                )
            if set(expected_variant.get("legacy_id_aliases", [])) != set(
                manifest_variant.get("legacy_id_aliases", [])
            ):
                errors.append(
                    f"source reconciliation {slug}/{source_id}: manifest legacy aliases differ"
                )

    public_records: dict[str, list[dict]] = defaultdict(list)
    for collection in ("events", "items"):
        for record in public_index.get(collection, []):
            if isinstance(record, dict) and isinstance(record.get("slug"), str):
                public_records[record["slug"]].append(record)
    for slug, control in controls_by_slug.items():
        records = public_records.get(slug, [])
        if not records:
            errors.append(f"source reconciliation {slug}: no public-index record")
            continue
        expected = (
            control.get("source_document_id"),
            control.get("pages"),
            control.get("sha256"),
        )
        for record in records:
            actual = (
                record.get("source_document_id"),
                record.get("source_pages"),
                record.get("source_hash_sha256"),
            )
            # The public index intentionally carries page/hash controls but not
            # native byte count; compare the values it does expose explicitly.
            if actual != expected:
                errors.append(
                    f"source reconciliation {slug}: public-index source control differs from reconciliation"
                )
            if set(record.get("source_document_id_legacy_aliases", [])) != set(
                control.get("legacy_id_aliases", [])
            ):
                errors.append(
                    f"source reconciliation {slug}: public-index control aliases differ"
                )
            indexed_variants = {
                row.get("source_document_id"): row
                for row in record.get("additional_source_documents", [])
                if isinstance(row, dict)
                and isinstance(row.get("source_document_id"), str)
            }
            expected_variants = {
                row.get("source_document_id"): row
                for row in variants_by_slug.get(slug, [])
            }
            if set(indexed_variants) != set(expected_variants):
                errors.append(
                    f"source reconciliation {slug}: public-index variant IDs differ"
                )
            for source_id in set(indexed_variants) & set(expected_variants):
                if integrity_tuple(indexed_variants[source_id]) != integrity_tuple(
                    expected_variants[source_id]
                ):
                    errors.append(
                        f"source reconciliation {slug}/{source_id}: public-index variant "
                        "bytes/pages/SHA-256 differ"
                    )


def validate_known_unlocated_sources(
    reconciliation: dict,
    continuity_documents: dict[str, dict],
    errors: list[str],
) -> None:
    """Keep the current open-source list deterministic and evidence-linked.

    The located 2012 president's statement must never re-enter this list merely
    because an older reconciliation contained it.  Each genuinely unlocated
    source instead points to the continuity record that documents the gap or
    the later recital on which the open-source entry rests.
    """

    expected = {
        "2012-08-10-written-objection": {
            "date": "2012-08-10",
            "continuity_evidence_record_id": "SP-SRC-OBJECTION-2012-08-10",
            "document_type": "referenced-written-objection-unlocated",
            "record_class": "explicit-missing-source-continuity-record",
        },
        "2018-11-20-standalone-acta": {
            "date": "2018-11-20",
            "continuity_evidence_record_id": "SP-SRC-RECITAL-2018-11-20",
            "document_type": "later-recital-of-unlocated-event",
            "record_class": "concrete-source-copy-or-source-record",
        },
        "2021-12-29-ricpe-primary-meeting-records": {
            "date": "2021-12-29",
            "continuity_evidence_record_id": "SP-SRC-RICPE-2021-12-29-PRIMARY-UNLOCATED",
            "document_type": {
                "es": "registro de carencia de convocatoria/ACTA/acuerdo societario primario",
                "en": "gap record for primary corporate notice/minutes/resolution",
            },
            "record_class": "explicit-missing-source-continuity-record",
        },
    }
    entries = reconciliation.get("known_unlocated_sources")
    if not isinstance(entries, list):
        errors.append("source reconciliation: known_unlocated_sources is not a list")
        return

    by_key: dict[str, dict] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            errors.append("source reconciliation: non-object known-unlocated entry")
            continue
        key = entry.get("unlocated_source_key")
        if not isinstance(key, str) or not key:
            errors.append("source reconciliation: known-unlocated entry lacks stable key")
            continue
        if key in by_key:
            errors.append(f"source reconciliation: duplicate known-unlocated key {key}")
        by_key[key] = entry

    if set(by_key) != set(expected):
        errors.append(
            "source reconciliation: known-unlocated source keys differ from "
            "the current three-source open-evidence control"
        )

    for key, control in expected.items():
        entry = by_key.get(key)
        if entry is None:
            continue
        for field in ("date", "continuity_evidence_record_id"):
            if entry.get(field) != control[field]:
                errors.append(
                    f"source reconciliation {key}: {field} differs from open-evidence control"
                )
        for locale in ("es", "en"):
            if not present(entry.get(f"description_{locale}")):
                errors.append(
                    f"source reconciliation {key}: missing {locale} open-evidence description"
                )

        evidence_id = control["continuity_evidence_record_id"]
        document = continuity_documents.get(evidence_id)
        if document is None:
            errors.append(
                f"source reconciliation {key}: continuity evidence record {evidence_id} missing"
            )
            continue
        if document.get("document_type") != control["document_type"]:
            errors.append(
                f"source reconciliation {key}: continuity evidence document type differs"
            )
        if document.get("record_class") != control["record_class"]:
            errors.append(
                f"source reconciliation {key}: continuity evidence record class differs"
            )
        controlled_date = document.get("reference_date") or document.get(
            "documented_date_or_range"
        )
        if controlled_date != control["date"]:
            errors.append(
                f"source reconciliation {key}: continuity evidence date differs"
            )
        integrity = document.get("integrity", {})
        if any(
            integrity.get(field) is not None
            for field in ("size_bytes", "page_count", "sha256")
        ):
            errors.append(
                f"source reconciliation {key}: unlocated source has assigned integrity values"
            )
        provenance_text = json.dumps(
            document.get("source_provenance_status", ""),
            ensure_ascii=False,
        ).lower()
        if not any(
            token in provenance_text
            for token in ("unlocated", "not located", "no localizad", "missing")
        ):
            errors.append(
                f"source reconciliation {key}: continuity evidence does not state the source gap"
            )

    statement = continuity_documents.get("SP-SRC-STATEMENT-2012-08-10-5P")
    if statement is None:
        errors.append("continuity: located 2012 president's statement record is missing")
    else:
        statement_integrity = statement.get("integrity", {})
        if not all(
            present(statement_integrity.get(field))
            for field in ("size_bytes", "page_count", "sha256")
        ):
            errors.append(
                "continuity: located 2012 president's statement lacks complete integrity control"
            )
        if any(
            entry.get("continuity_evidence_record_id") == statement["stable_id"]
            for entry in entries
            if isinstance(entry, dict)
        ):
            errors.append(
                "source reconciliation: located 2012 president's statement is still classified unlocated"
            )


class PageParser(HTMLParser):
    """Collect the small structural surface needed for deterministic checks."""

    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []
        self.links: list[tuple[str, str]] = []
        self.elements: list[tuple[str, dict[str, str]]] = []
        self.link_elements: list[dict[str, str]] = []
        self.html_attrs: dict[str, str] = {}
        self.body_attrs: dict[str, str] = {}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key: value or "" for key, value in attrs}
        self.elements.append((tag, values))
        if values.get("id"):
            self.ids.append(values["id"])
        if tag == "html":
            self.html_attrs = values
        elif tag == "body":
            self.body_attrs = values
        if tag == "link":
            self.link_elements.append(values)
        key = "href" if tag in {"a", "link"} else "src" if tag in {"img", "script"} else None
        if key and values.get(key):
            self.links.append((tag, values[key]))

    def by_class(self, class_name: str, tag: str | None = None) -> list[dict[str, str]]:
        return [
            attrs
            for found_tag, attrs in self.elements
            if (tag is None or found_tag == tag)
            and class_name in attrs.get("class", "").split()
        ]


_PAGE_CACHE: dict[Path, PageParser] = {}


def parse_page(path: Path) -> PageParser:
    path = path.resolve()
    if path not in _PAGE_CACHE:
        parser = PageParser()
        parser.feed(path.read_text(encoding="utf-8"))
        _PAGE_CACHE[path] = parser
    return _PAGE_CACHE[path]


def local_target(page: Path, value: str) -> tuple[Path, str] | None:
    parsed = urlsplit(value)
    if parsed.scheme or parsed.netloc or value.startswith(("mailto:", "tel:", "javascript:")):
        return None
    relative = unquote(parsed.path)
    if relative.startswith("/por-derecho/"):
        target = REPO / relative.removeprefix("/por-derecho/")
    elif relative.startswith("/"):
        target = REPO / relative.lstrip("/")
    elif relative:
        target = page.parent / relative
    else:
        target = page
    target = target.resolve()
    if relative.endswith("/") or target.is_dir():
        target /= "index.html"
    return target, unquote(parsed.fragment)


def event_url(route: str) -> str:
    return f"{BASE_URL}/{route.removesuffix('index.html')}"


def page_metadata_errors(
    path: Path,
    locale: str,
    canonical: str,
    alternates: dict[str, str],
) -> list[str]:
    errors: list[str] = []
    label = path.relative_to(REPO).as_posix()
    parser = parse_page(path)
    if parser.html_attrs.get("lang") != locale:
        errors.append(f"{label}: html lang is not {locale}")
    canonicals = [
        item.get("href", "")
        for item in parser.link_elements
        if "canonical" in item.get("rel", "").split()
    ]
    if canonicals != [canonical]:
        errors.append(f"{label}: canonical mismatch {canonicals!r} != {[canonical]!r}")
    found_alternates: dict[str, list[str]] = defaultdict(list)
    for item in parser.link_elements:
        if "alternate" in item.get("rel", "").split() and item.get("hreflang"):
            found_alternates[item["hreflang"]].append(item.get("href", ""))
    for hreflang, expected in alternates.items():
        if found_alternates.get(hreflang) != [expected]:
            errors.append(
                f"{label}: {hreflang} alternate mismatch "
                f"{found_alternates.get(hreflang, [])!r} != {[expected]!r}"
            )
    return errors


def validate_actor_route_catalog(errors: list[str]) -> None:
    """Require every controlled actor route to be a live bilingual pair."""

    for actor_key, actor in ACTOR_ROUTE_CATALOG.items():
        routes = actor.get("routes", {})
        labels = actor.get("label", {})
        if set(routes) != {"es", "en"} or set(labels) != {"es", "en"}:
            errors.append(f"actor route {actor_key}: bilingual routes/labels are incomplete")
            continue
        if routes["es"] == routes["en"]:
            errors.append(f"actor route {actor_key}: ES and EN routes are not distinct")
        alternates = {
            locale: f"{BASE_URL}/{routes[locale].lstrip('/')}"
            for locale in ("es", "en")
        }
        for locale in ("es", "en"):
            route = routes[locale]
            page = REPO / route
            if page.is_dir() or route.endswith("/"):
                page /= "index.html"
            if not page.is_file():
                errors.append(f"actor route {actor_key}/{locale}: missing {route}")
                continue
            errors.extend(
                page_metadata_errors(
                    page,
                    locale,
                    alternates[locale],
                    alternates,
                )
            )


def link_errors(page: Path) -> list[str]:
    errors: list[str] = []
    label = page.relative_to(REPO).as_posix()
    parser = parse_page(page)
    duplicate_ids = sorted(item for item, count in Counter(parser.ids).items() if count > 1)
    if duplicate_ids:
        errors.append(f"{label}: duplicate fragment IDs {duplicate_ids}")
    for tag, value in parser.links:
        resolved = local_target(page, value)
        if resolved is None:
            continue
        target, fragment = resolved
        try:
            target.relative_to(REPO.resolve())
        except ValueError:
            errors.append(f"{label}: link escapes repository: {value}")
            continue
        if not target.exists():
            errors.append(f"{label}: broken {tag} link {value}")
            continue
        if fragment and target.suffix.lower() in {".html", ".htm"}:
            target_parser = parse_page(target)
            if fragment not in set(target_parser.ids):
                errors.append(f"{label}: broken fragment {value}")
    return errors


def linear_channel(value: int) -> float:
    channel = value / 255
    return channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4


def luminance(hex_colour: str) -> float:
    colour = hex_colour.lstrip("#")
    channels = [linear_channel(int(colour[index:index + 2], 16)) for index in (0, 2, 4)]
    return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]


def contrast(first: str, second: str) -> float:
    one, two = sorted((luminance(first), luminance(second)), reverse=True)
    return (one + 0.05) / (two + 0.05)


def validate_continuity(data: dict, errors: list[str]) -> tuple[dict[str, dict], dict[str, dict]]:
    families = data.get("event_families", [])
    documents = data.get("documents", [])
    family_ids = [item.get("stable_id") for item in families]
    document_ids = [item.get("stable_id") for item in documents]
    if len(family_ids) != len(set(family_ids)):
        errors.append("continuity: duplicate event-family stable IDs")
    if len(document_ids) != len(set(document_ids)):
        errors.append("continuity: duplicate document stable IDs")
    if data.get("controlled_event_family_count") != len(families):
        errors.append("continuity: controlled_event_family_count does not match event_families")
    if data.get("document_record_count") != len(documents):
        errors.append("continuity: document_record_count does not match documents")
    if set(family_ids) != set(EVENT_IDS):
        errors.append("continuity: event-family IDs differ from capacity/sequence control universe")
    if data.get("adverse_sequence_model") != ADVERSE_SEQUENCE_MODEL:
        errors.append("continuity: adverse_sequence_model differs from deterministic control")
    errors.extend(
        f"continuity localization: {error}"
        for error in validate_scalar_coverage(documents)
    )

    family_by_id = {item.get("stable_id"): item for item in families}
    document_by_id = {item.get("stable_id"): item for item in documents}
    assigned_documents: dict[str, set[str]] = defaultdict(set)
    route_pairs = {
        (
            family.get("bilingual_event_routes", {}).get("es"),
            family.get("bilingual_event_routes", {}).get("en"),
        )
        for family in families
    }

    for family in families:
        stable_id = family.get("stable_id", "<missing-event-family-id>")
        for field in EVENT_FIELDS:
            if not present(family.get(field)):
                errors.append(f"continuity {stable_id}: missing/empty {field}")
        perimeter = family.get("perimeter")
        expected = EXPECTED_PERIMETERS.get(perimeter)
        if expected is None:
            errors.append(f"continuity {stable_id}: invalid perimeter {perimeter}")
        elif family.get("perimeter_code") != expected[0]:
            errors.append(f"continuity {stable_id}: perimeter code is not {expected[0]}")
        routes = family.get("bilingual_event_routes", {})
        if set(routes) != {"es", "en"} or not all(present(routes.get(lang)) for lang in ("es", "en")):
            errors.append(f"continuity {stable_id}: incomplete bilingual routes")
        audit = family.get("continuity_audit", {})
        for field in AUDIT_FIELDS:
            if not present(audit.get(field)):
                errors.append(f"continuity {stable_id}: missing audit field {field}")
        for document_id in family.get("document_record_ids", []):
            if document_id not in document_by_id:
                errors.append(f"continuity {stable_id}: unknown document_record_id {document_id}")
        expected_annotation = EVENT_ANNOTATIONS.get(stable_id)
        if expected_annotation is None:
            errors.append(f"continuity {stable_id}: no deterministic capacity/sequence annotation")
        else:
            for field, expected_value in expected_annotation.items():
                if family.get(field) != expected_value:
                    errors.append(f"continuity {stable_id}: {field} differs from deterministic control")

    register_source_ids: set[str] = set()
    for document in documents:
        stable_id = document.get("stable_id", "<missing-document-id>")
        for field in DOCUMENT_FIELDS:
            if not present(document.get(field)):
                errors.append(f"continuity {stable_id}: missing/empty {field}")
        perimeter = document.get("perimeter")
        expected = EXPECTED_PERIMETERS.get(perimeter)
        if expected is None:
            errors.append(f"continuity {stable_id}: invalid perimeter {perimeter}")
        elif document.get("perimeter_code") != expected[0]:
            errors.append(f"continuity {stable_id}: perimeter code is not {expected[0]}")
        event_family_ids = document.get("event_family_ids", [])
        for family_id in event_family_ids:
            if family_id not in family_by_id:
                errors.append(f"continuity {stable_id}: unknown event family {family_id}")
            else:
                assigned_documents[family_id].add(stable_id)
        routes = document.get("bilingual_event_routes", {})
        route_pair = (routes.get("es"), routes.get("en"))
        page_reason = document.get("no_page_reason") or document.get("no_standalone_page_reason")
        if route_pair not in route_pairs and not present(page_reason):
            errors.append(f"continuity {stable_id}: no stable bilingual page or no_page_reason")
        relationships = document.get("relationship_to_other_documents_or_event", {})
        if isinstance(relationships, dict):
            for related_id in relationships.get("related_document_ids", []):
                if related_id not in document_by_id and related_id not in family_by_id:
                    errors.append(f"continuity {stable_id}: unknown related document {related_id}")
            for family_id in relationships.get("event_family_ids", []):
                if family_id not in family_by_id:
                    errors.append(f"continuity {stable_id}: unknown related event family {family_id}")
        for source_id in document.get("register_source_ids", []):
            # This counter covers the 46 SP-EVT + 9 SP-REL rows in the
            # public communications register. SP-SRC rows are separately
            # identified native/source-family records and are not folded
            # into that declared 55-row denominator.
            if present(source_id) and str(source_id).startswith(("SP-EVT-", "SP-REL-")):
                register_source_ids.add(str(source_id))

    for family_id, family in family_by_id.items():
        declared = set(family.get("document_record_ids", []))
        if declared != assigned_documents.get(family_id, set()):
            errors.append(
                f"continuity {family_id}: document_record_ids differ from reverse assignments "
                f"({len(declared)} declared/{len(assigned_documents.get(family_id, set()))} assigned)"
            )

    declared_coverage = data.get("source_register_coverage_count")
    if declared_coverage is not None and declared_coverage != len(register_source_ids):
        errors.append(
            "continuity: source_register_coverage_count does not match unique register_source_ids "
            f"({declared_coverage}/{len(register_source_ids)})"
        )
    source_total = data.get("source_register_record_count")
    if source_total is not None and declared_coverage is not None and declared_coverage > source_total:
        errors.append("continuity: source-register coverage exceeds declared source-register total")

    source_documents = [
        document
        for document in documents
        if str(document.get("stable_id", "")).startswith("SP-SRC-")
    ]
    missing_source_documents = [
        document
        for document in source_documents
        if document.get("record_class") == "explicit-missing-source-continuity-record"
    ]
    concrete_source_documents = [
        document
        for document in source_documents
        if document.get("record_class") != "explicit-missing-source-continuity-record"
    ]
    for document in missing_source_documents:
        integrity = document.get("integrity", {})
        if any(
            integrity.get(field) is not None
            for field in ("size_bytes", "page_count", "sha256")
        ):
            errors.append(
                f"continuity {document.get('stable_id')}: explicit missing-source record "
                "must not carry binary integrity values"
            )
    metric_controls = (
        (
            "concrete_source_record_count",
            "concrete_source_record_coverage_count",
            "concrete_source_copy_or_source_records",
            len(concrete_source_documents),
        ),
        (
            "missing_source_continuity_record_count",
            "missing_source_continuity_record_coverage_count",
            "explicit_missing_source_continuity_records",
            len(missing_source_documents),
        ),
    )
    coverage = data.get("coverage", {})
    for count_field, covered_field, coverage_field, actual_count in metric_controls:
        if data.get(count_field) != actual_count:
            errors.append(
                f"continuity: {count_field} does not match derived source records "
                f"({data.get(count_field)}/{actual_count})"
            )
        if data.get(covered_field) != actual_count:
            errors.append(
                f"continuity: {covered_field} does not match derived source records "
                f"({data.get(covered_field)}/{actual_count})"
            )
        expected_coverage = {"denominator": actual_count, "covered": actual_count}
        if coverage.get(coverage_field) != expected_coverage:
            errors.append(
                f"continuity: coverage.{coverage_field} differs from derived source records"
            )
    return family_by_id, document_by_id


def validate_public_register_source_rows(
    continuity: dict,
    continuity_documents: dict[str, dict],
    errors: list[str],
) -> None:
    """Derive the live section-4 SP-SRC denominator from the canonical table."""

    try:
        register = PUBLIC_REGISTER.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"public register unavailable for source-row count: {exc}")
        return
    match = re.search(
        r"^## 4\. Canonical source families\s*$\n(?P<section>.*?)^## 5\.",
        register,
        re.MULTILINE | re.DOTALL,
    )
    if match is None:
        errors.append("public register: canonical source-family table section not found")
        return
    source_ids = re.findall(
        r"^\| `(SP-SRC-[A-Z0-9-]+)` \|",
        match.group("section"),
        re.MULTILINE,
    )
    duplicates = sorted(
        source_id
        for source_id, count in Counter(source_ids).items()
        if count > 1
    )
    if duplicates:
        errors.append(
            "public register: duplicate canonical source-table rows: "
            + ", ".join(duplicates)
        )
    denominator = len(source_ids)
    covered = sum(source_id in continuity_documents for source_id in source_ids)
    if continuity.get("source_register_source_row_count") != denominator:
        errors.append(
            "continuity: source_register_source_row_count does not match the "
            f"canonical section-4 table ({continuity.get('source_register_source_row_count')}/{denominator})"
        )
    if continuity.get("source_register_source_row_coverage_count") != covered:
        errors.append(
            "continuity: source_register_source_row_coverage_count does not match "
            f"continuity-linked section-4 rows ({continuity.get('source_register_source_row_coverage_count')}/{covered})"
        )
    expected_coverage = {"denominator": denominator, "covered": covered}
    if continuity.get("coverage", {}).get("canonical_source_table_rows") != expected_coverage:
        errors.append(
            "continuity: coverage.canonical_source_table_rows differs from the "
            "derived section-4 table control"
        )
    unknown = sorted(set(source_ids) - set(continuity_documents))
    if unknown:
        errors.append(
            "public register: canonical source-table IDs absent from continuity: "
            + ", ".join(unknown)
        )


def expected_document_appearance_control(
    document: dict,
    continuity_families: dict[str, dict],
) -> tuple[dict[str, str], list[dict]] | None:
    """Derive the one canonical anchor and every secondary appearance."""
    stable_id = document.get("stable_id", "<missing-document-id>")
    routes = document.get("bilingual_event_routes", {})
    if set(routes) != {"es", "en"}:
        return None
    stable_pages = {locale: f"{routes[locale]}#{stable_id}" for locale in ("es", "en")}
    appearances: list[dict] = []
    canonical_count = 0
    for event_family_id in document.get("event_family_ids", []):
        family = continuity_families.get(event_family_id)
        if family is None:
            return None
        event_routes = family.get("bilingual_event_routes", {})
        canonical = all(event_routes.get(locale) == routes[locale] for locale in ("es", "en"))
        canonical_count += int(canonical)
        fragment = stable_id if canonical else f"appearance-{stable_id}"
        appearances.append({
            "event_family_id": event_family_id,
            "page_disposition": (
                "canonical-event-family-stable-anchor"
                if canonical
                else "secondary-event-family-linked-appearance"
            ),
            "fragment": fragment,
            "es": f'{event_routes.get("es", "")}#{fragment}',
            "en": f'{event_routes.get("en", "")}#{fragment}',
        })
    if canonical_count != 1:
        return None
    return stable_pages, appearances


def validate_index(
    index: dict,
    continuity_families: dict[str, dict],
    continuity_documents: dict[str, dict],
    errors: list[str],
) -> tuple[list[dict], int]:
    events = index.get("events", [])
    ids = [event.get("id") for event in events]
    if len(ids) != len(set(ids)):
        errors.append("lineage index: duplicate event IDs")
    if index.get("controlled_event_family_count") != len(events):
        errors.append("lineage index: controlled_event_family_count does not match events")
    if set(ids) != set(continuity_families):
        errors.append("lineage index: event IDs do not match continuity event-family IDs")
    if index.get("source_communication_document_count") != len(continuity_documents):
        errors.append("lineage index: source_communication_document_count does not match continuity documents")
    if index.get("adverse_sequence_model") != ADVERSE_SEQUENCE_MODEL:
        errors.append("lineage index: adverse_sequence_model differs from deterministic control")
    if index.get("principal_owner_acta_lineages") != PRINCIPAL_LINEAGES:
        errors.append("lineage index: principal Owners' ACTA lineages differ from deterministic control")
    if index.get("pre_2008_owner_acta_control") != PRE_2008_CONTROL:
        errors.append("lineage index: pre-2008 Owners' ACTA control differs from deterministic control")
    if index.get("owner_acta_role_matrix_event_count") != len(OWNER_ROLE_MATRIX):
        errors.append("lineage index: Owners' ACTA role-matrix count mismatch")
    c1 = index.get("perimeters", {}).get("adverse_montelanza_molina", {})
    for field in ("label_es", "label_en", "definition_es", "definition_en"):
        value = c1.get(field, "")
        if not all(token in value for token in ("AAS", "FMMM", "Cogolludo", "Pamanil")):
            errors.append(f"lineage index: C1 {field} must name AAS/FMMM/Cogolludo/Pamanil")

    actual_lanes = Counter(event.get("primary_lane") for event in events)
    expected_lane_counts = index.get("primary_lane_counts", {})
    for lane in ("A", "B", "C", "D"):
        if expected_lane_counts.get(lane) != actual_lanes.get(lane, 0):
            errors.append(f"lineage index: primary lane {lane} count mismatch")

    routes: set[str] = set()
    located = 0
    appearance_controls: dict[str, tuple[dict[str, str], list[dict]]] = {}
    embedded_occurrences: Counter[str] = Counter()
    for stable_id, source_document in continuity_documents.items():
        control = expected_document_appearance_control(source_document, continuity_families)
        if control is None:
            errors.append(
                f"{stable_id}: continuity routes do not resolve to exactly one canonical event anchor"
            )
        else:
            appearance_controls[stable_id] = control
    for event in events:
        event_id = event.get("id", "<missing-event-id>")
        family = continuity_families.get(event_id, {})
        if event.get("stable_id") != event_id:
            errors.append(f"{event_id}: stable_id mismatch")
        perimeter = event.get("perimeter")
        expected = EXPECTED_PERIMETERS.get(perimeter)
        if expected is None:
            errors.append(f"{event_id}: invalid perimeter {perimeter}")
        else:
            if event.get("perimeter_code") != expected[0]:
                errors.append(f"{event_id}: perimeter code is not {expected[0]}")
            if event.get("primary_lane") != expected[1]:
                errors.append(f"{event_id}: primary lane is not {expected[1]}")
        for field in (
            "documented_date_or_range",
            "document_type",
            "issuer_sender",
            "stated_capacity",
            "recipients",
            "meeting_body_if_any",
            "documented_convener",
            "source_provenance_status",
            "public_private_status",
            "relationship_to_other_documents_or_events",
            "unresolved_evidential_issues",
            "continuity_audit",
            "documents",
            "convener_es",
            "convener_en",
            "basis_es",
            "basis_en",
            "attribution_status",
            "confidence",
            "patricia_dominguez_capacity",
            "adverse_sequence_stage",
            "actor_entity_routes",
            "actor_entity_route_gaps",
        ):
            if not present(event.get(field)):
                # An explicit empty list is valid when no event-specific actor
                # route is supported without inference.
                if field not in {"actor_entity_routes", "actor_entity_route_gaps"}:
                    errors.append(f"{event_id}: missing/empty machine field {field}")
        expected_annotation = EVENT_ANNOTATIONS.get(event_id)
        if expected_annotation is None:
            errors.append(f"{event_id}: no deterministic capacity/sequence annotation")
        else:
            for field, expected_value in expected_annotation.items():
                if event.get(field) != expected_value:
                    errors.append(f"{event_id}: {field} differs from deterministic control")
        expected_owner_roles = OWNER_ROLE_MATRIX.get(event_id)
        if expected_owner_roles is None:
            if "owner_acta_role_attribution" in event:
                errors.append(f"{event_id}: unexpected Owners' ACTA role attribution")
        elif event.get("owner_acta_role_attribution") != expected_owner_roles:
            errors.append(f"{event_id}: Owners' ACTA role attribution differs from deterministic control")
        try:
            expected_actor_routes = actor_routes_for_event(event_id)
        except KeyError as exc:
            errors.append(f"{event_id}: {exc}")
        else:
            if event.get("actor_entity_routes") != expected_actor_routes:
                errors.append(f"{event_id}: actor/entity routes differ from deterministic control")
            if event.get("actor_entity_route_gaps") != actor_route_gaps_for_event(event_id):
                errors.append(f"{event_id}: actor/entity route gaps differ from deterministic control")
        expected_documents = set(family.get("document_record_ids", []))
        indexed_documents = {item.get("stable_id") for item in event.get("documents", [])}
        if indexed_documents != expected_documents:
            errors.append(f"{event_id}: embedded documents do not match continuity family")
        for document in event.get("documents", []):
            stable_id = document.get("stable_id", "<missing-document-id>")
            embedded_occurrences[stable_id] += 1
            source_stage = continuity_documents.get(stable_id, {}).get("relationship_stage")
            expected_stage = "pre_meeting" if source_stage == "pre_meeting_notice" else source_stage
            if document.get("relationship_stage") != expected_stage:
                errors.append(f"{event_id}/{stable_id}: normalized relationship stage mismatch")
            if source_stage == "pre_meeting_notice":
                if document.get("relationship_stage_source") != "pre_meeting_notice":
                    errors.append(f"{event_id}/{stable_id}: source relationship-stage alias missing")
            elif "relationship_stage_source" in document:
                errors.append(f"{event_id}/{stable_id}: unexpected relationship-stage alias")
            control = appearance_controls.get(stable_id)
            if control is None:
                continue
            expected_pages, expected_appearances = control
            expected_current = next(
                (
                    appearance
                    for appearance in expected_appearances
                    if appearance["event_family_id"] == event_id
                ),
                None,
            )
            if expected_current is None:
                errors.append(f"{event_id}/{stable_id}: unexpected document appearance")
                continue
            if document.get("stable_bilingual_page") != expected_pages:
                errors.append(f"{event_id}/{stable_id}: canonical bilingual anchor mismatch")
            if document.get("appears_on_event_routes") != expected_appearances:
                errors.append(f"{event_id}/{stable_id}: secondary-appearance route map mismatch")
            if document.get("page_disposition") != expected_current["page_disposition"]:
                errors.append(f"{event_id}/{stable_id}: page disposition mismatch")
            expected_current_page = {
                locale: expected_current[locale] for locale in ("es", "en")
            }
            if document.get("current_appearance_page") != expected_current_page:
                errors.append(f"{event_id}/{stable_id}: current appearance page mismatch")
            if document.get("current_appearance_fragment") != expected_current["fragment"]:
                errors.append(f"{event_id}/{stable_id}: current appearance fragment mismatch")
            if not present(document.get("no_standalone_page_reason")):
                errors.append(f"{event_id}/{stable_id}: no standalone-page reason")
        for route_field, locale in (("detail_page_es", "es"), ("detail_page_en", "en")):
            route = event.get(route_field, "")
            if not route or route in routes:
                errors.append(f"{event_id}: missing/duplicate {route_field}")
                continue
            routes.add(route)
            expected_route = family.get("bilingual_event_routes", {}).get(locale)
            if route != expected_route:
                errors.append(f"{event_id}: {route_field} differs from continuity route")
        transcript = event.get("transcript_path") or event.get("transcript_source")
        if transcript:
            located += 1
            if not (REPO / transcript).is_file():
                errors.append(f"{event_id}: transcript path does not exist: {transcript}")
            marker_only = event.get("public_text_mode") == "full-page-redaction-markers"
            if marker_only and event.get("public_ocr_available") is not False:
                errors.append(f"{event_id}: marker-only public text must set public_ocr_available=false")
    for stable_id, source_document in continuity_documents.items():
        expected_count = len(source_document.get("event_family_ids", []))
        if embedded_occurrences.get(stable_id, 0) != expected_count:
            errors.append(
                f"{stable_id}: embedded appearance count "
                f"{embedded_occurrences.get(stable_id, 0)}/{expected_count}"
            )
    return events, located


def expected_local_anchor_map(events: list[dict], locale: str) -> dict[str, dict[str, str]]:
    """Build the expected localized canonical target map used by event pages."""
    es = locale == "es"
    anchors: dict[str, dict[str, str]] = {}
    for event in events:
        event_id = event["id"]
        event_route = event["detail_page_es" if es else "detail_page_en"]
        event_perimeter = event["perimeter"]
        event_code, event_lane = EXPECTED_PERIMETERS[event_perimeter]
        event_perimeter_record = PERIMETER_LABELS[event_perimeter]
        anchors[event_id] = {
            "href": f"../../../../{event_route}#ficha",
            "label": f'{"Evento relacionado" if es else "Related event"} {event_id} · {event.get(f"title_{locale}", event_id)}',
            "target_kind": "event-family",
            "target_perimeter": event_perimeter,
            "target_primary_lane": event_lane,
            "target_perimeter_code": event_code,
            "target_perimeter_label": event_perimeter_record[locale],
        }
        for document in event.get("documents", []):
            stable_id = document["stable_id"]
            route = document.get("bilingual_event_routes", {}).get(locale)
            if not route:
                continue
            date_value = document.get("documented_date_or_range")
            if isinstance(date_value, dict):
                date_value = date_value.get(locale) or date_value.get("es") or date_value.get("en")
            document_perimeter = document.get("perimeter", "unresolved")
            document_code, document_lane = EXPECTED_PERIMETERS[document_perimeter]
            candidate = {
                "href": f"../../../../{route}#{stable_id}",
                "label": (
                    f'{"Documento relacionado" if es else "Related document"} '
                    f'{stable_id} · {date_value}'
                ),
                "target_kind": "document-record",
                "target_perimeter": document_perimeter,
                "target_primary_lane": document_lane,
                "target_perimeter_code": document_code,
                "target_perimeter_label": PERIMETER_LABELS[document_perimeter][locale],
            }
            existing = anchors.get(stable_id)
            if existing is not None and existing != candidate:
                raise ValueError(f"Conflicting canonical anchor for {stable_id}")
            anchors[stable_id] = candidate
    return anchors


def validate_event_pages(events: list[dict], errors: list[str]) -> None:
    by_id = {event["id"]: event for event in events}
    anchor_maps = {
        locale: expected_local_anchor_map(events, locale) for locale in ("es", "en")
    }
    for event in events:
        event_id = event["id"]
        es_url = event_url(event["detail_page_es"])
        en_url = event_url(event["detail_page_en"])
        expected_alternates = {"es": es_url, "en": en_url, "x-default": es_url}
        expected_document_ids = {item["stable_id"] for item in event.get("documents", [])}
        for locale, route in (("es", event["detail_page_es"]), ("en", event["detail_page_en"])):
            page = REPO / route
            if not page.is_file():
                errors.append(f"{event_id}: missing page {route}")
                continue
            parser = parse_page(page)
            source = page.read_text(encoding="utf-8")
            errors.extend(
                page_metadata_errors(
                    page,
                    locale,
                    es_url if locale == "es" else en_url,
                    expected_alternates,
                )
            )
            if parser.body_attrs.get("data-perimeter") != event["perimeter"]:
                errors.append(f"{route}: body perimeter machine value mismatch")
            if parser.body_attrs.get("data-primary-lane") != event["primary_lane"]:
                errors.append(f"{route}: body primary-lane machine value mismatch")
            owner_roles = event.get("owner_acta_role_attribution")
            expected_principal = owner_roles["principal_lineage"] if owner_roles else event["primary_lane"]
            expected_phase = owner_roles["phase_code"] if owner_roles else event["perimeter_code"]
            if parser.body_attrs.get("data-principal-lineage") != expected_principal:
                errors.append(f"{route}: body principal-lineage machine value mismatch")
            if parser.body_attrs.get("data-lineage-phase") != expected_phase:
                errors.append(f"{route}: body lineage-phase machine value mismatch")
            capacity = event["patricia_dominguez_capacity"]
            sequence = event["adverse_sequence_stage"]
            if parser.body_attrs.get("data-patricia-capacity") != capacity["status_code"]:
                errors.append(f"{route}: body Patricia-capacity machine value mismatch")
            if parser.body_attrs.get("data-adverse-sequence-stage") != sequence["stage_code"]:
                errors.append(f"{route}: body adverse-sequence machine value mismatch")
            for marker in (
                event_id,
                "Regla de atribución" if locale == "es" else "Attribution rule",
                "acta-lineage-facts",
                "acta-continuity-table",
                "event-family-continuity-v1.json",
                "COMMUNITY_AUTHORITY_EVENTS_EMAILS_MEETINGS_ACTAS_PUBLIC_REGISTER.md",
            ):
                if marker not in source:
                    errors.append(f"{route}: missing marker {marker}")
            if not re.search(
                rf'class="acta-perimeter-code"[^>]*>{re.escape(event["perimeter_code"])}</span>',
                source,
            ):
                errors.append(f"{route}: missing written perimeter code {event['perimeter_code']}")

            controls = parser.by_class("acta-capacity-sequence", "div")
            if len(controls) != 1:
                errors.append(f"{route}: mandate/sequence control block missing or duplicated")
            else:
                control = controls[0]
                if control.get("data-patricia-capacity") != capacity["status_code"]:
                    errors.append(f"{route}: capacity control lacks machine status")
                if control.get("data-adverse-sequence-stage") != sequence["stage_code"]:
                    errors.append(f"{route}: sequence control lacks machine stage")
                if control.get("data-adverse-sequence-applicability") != sequence["applicability_code"]:
                    errors.append(f"{route}: sequence control lacks applicability status")
            locale_summary = capacity.get("summary", {}).get(locale, "")
            sequence_summary = sequence.get("summary", {}).get(locale, "")
            for label, value in (
                ("Patricia capacity summary", locale_summary),
                ("adverse sequence summary", sequence_summary),
            ):
                if not value or escape(value, quote=True) not in source:
                    errors.append(f"{route}: missing bilingual {label}")
            identity_name = capacity.get("identity_control", {}).get(
                "distinct_from_canonical_name"
            )
            if not identity_name or escape(identity_name, quote=True) not in source:
                errors.append(f"{route}: missing Patricia/Laura identity distinction")
            role_blocks = parser.by_class("acta-owner-role-control", "section")
            if owner_roles:
                if len(role_blocks) != 1:
                    errors.append(f"{route}: Owners' ACTA role block missing or duplicated")
                else:
                    block = role_blocks[0]
                    if block.get("data-principal-lineage") != owner_roles["principal_lineage"]:
                        errors.append(f"{route}: role block principal-lineage mismatch")
                    if block.get("data-lineage-phase") != owner_roles["phase_code"]:
                        errors.append(f"{route}: role block phase mismatch")
                for role_key in ("caller", "meeting_management", "acta_authorship", "custody_circulation"):
                    value = owner_roles[role_key][locale]
                    if escape(value, quote=True) not in source:
                        errors.append(f"{route}: missing localized owner role {role_key}")
            elif role_blocks:
                errors.append(f"{route}: non-owner event renders an Owners' ACTA role block")

            expected_actor_routes = event.get("actor_entity_routes", [])
            actor_links = parser.by_class("acta-actor-entity-link", "a")
            if len(actor_links) != len(expected_actor_routes):
                errors.append(
                    f"{route}: actor/entity link count "
                    f"{len(actor_links)}/{len(expected_actor_routes)}"
                )
            actor_links_by_key = {
                link.get("data-actor-key", ""): link for link in actor_links
            }
            if len(actor_links_by_key) != len(actor_links):
                errors.append(f"{route}: actor/entity keys are duplicated")
            for actor in expected_actor_routes:
                actor_key = actor["actor_key"]
                link = actor_links_by_key.get(actor_key)
                if link is None:
                    errors.append(f"{route}: actor/entity link missing {actor_key}")
                    continue
                expected_label = actor["label"][locale]
                expected_href = f'../../../../{actor["routes"][locale]}'
                if link.get("href") != expected_href:
                    errors.append(f"{route}: actor/entity href mismatch for {actor_key}")
                if link.get("aria-label") != expected_label:
                    errors.append(f"{route}: actor/entity localized label mismatch for {actor_key}")
                if link.get("data-actor-link-locale") != locale:
                    errors.append(f"{route}: actor/entity locale mismatch for {actor_key}")
                if link.get("data-relationship-status") != actor["relationship_status_code"]:
                    errors.append(f"{route}: actor/entity relationship status mismatch for {actor_key}")
            expected_route_gaps = event.get("actor_entity_route_gaps", [])
            route_gaps = parser.by_class("acta-actor-route-gap", "li")
            if len(route_gaps) != len(expected_route_gaps):
                errors.append(
                    f"{route}: actor/entity route-gap count "
                    f"{len(route_gaps)}/{len(expected_route_gaps)}"
                )
            route_gap_codes = {
                gap.get("data-actor-route-gap", "") for gap in route_gaps
            }
            if route_gap_codes != {
                gap["subject_code"] for gap in expected_route_gaps
            }:
                errors.append(f"{route}: actor/entity route-gap machine values differ")
            for gap in expected_route_gaps:
                if escape(gap["reason"][locale], quote=True) not in source:
                    errors.append(
                        f'{route}: localized actor/entity route-gap reason missing '
                        f'{gap["subject_code"]}'
                    )
            boundaries = parser.by_class("acta-route-inference-boundary", "p")
            if len(boundaries) != 1 or escape(
                ROUTE_INFERENCE_BOUNDARY[locale], quote=True
            ) not in source:
                errors.append(f"{route}: localized actor-route inference boundary missing")

            toggles = parser.by_class("nav-toggle", "button")
            if len(toggles) != 1 or toggles[0].get("aria-controls") != "main-nav" or toggles[0].get("aria-expanded") != "false":
                errors.append(f"{route}: accessible mobile navigation toggle missing or malformed")
            main_nav = [attrs for tag, attrs in parser.elements if tag == "nav" and attrs.get("id") == "main-nav"]
            if len(main_nav) != 1:
                errors.append(f"{route}: main-nav target missing or duplicated")

            cards = parser.by_class("acta-document-card", "article")
            card_ids = {card.get("data-document-id") for card in cards}
            if card_ids != expected_document_ids:
                errors.append(
                    f"{route}: document-card identities differ "
                    f"({len(card_ids)}/{len(expected_document_ids)})"
                )
            for card in cards:
                card_id = card.get("data-document-id")
                document = next((item for item in event.get("documents", []) if item["stable_id"] == card_id), None)
                if not document:
                    continue
                expected = EXPECTED_PERIMETERS[document["perimeter"]]
                if card.get("data-perimeter") != document["perimeter"] or card.get("data-primary-lane") != expected[1]:
                    errors.append(f"{route}: document card {card_id} lacks machine perimeter/lane")
                if card.get("data-relationship-stage") != document.get("relationship_stage"):
                    errors.append(f"{route}: document card {card_id} relationship-stage mismatch")
                disposition = document.get("page_disposition")
                if card.get("data-page-disposition") != disposition:
                    errors.append(f"{route}: document card {card_id} page disposition mismatch")
                if card.get("id") != document.get("current_appearance_fragment"):
                    errors.append(f"{route}: document card {card_id} appearance fragment mismatch")
                stable_page = document.get("stable_bilingual_page", {}).get(locale)
                if card.get("data-stable-bilingual-page") != stable_page:
                    errors.append(f"{route}: document card {card_id} canonical-page value mismatch")
                if card.get("data-localization-locale") != locale:
                    errors.append(f"{route}: document card {card_id} lacks localization locale")

                card_field_elements = [
                    attrs
                    for _tag, attrs in parser.elements
                    if attrs.get("data-source-document-id") == card_id
                    and attrs.get("data-card-field") in LOCALIZED_FIELDS
                ]
                by_field: dict[str, list[dict[str, str]]] = defaultdict(list)
                for attrs in card_field_elements:
                    by_field[attrs["data-card-field"]].append(attrs)
                for field in LOCALIZED_FIELDS:
                    matches = by_field.get(field, [])
                    if len(matches) != 1:
                        errors.append(
                            f"{route}: document card {card_id} localization field {field} "
                            f"count {len(matches)}/1"
                        )
                        continue
                    if field == "no_page_reason":
                        raw_value = (
                            document.get("no_page_reason")
                            or document.get("no_standalone_page_reason")
                        )
                    else:
                        raw_value = document.get(field)
                    try:
                        localized = localize_document_value(raw_value, locale, field)
                    except (KeyError, ValueError) as exc:
                        errors.append(f"{route}: document card {card_id}/{field}: {exc}")
                        continue
                    if isinstance(localized, list):
                        localized_display = "; ".join(str(item) for item in localized) or "—"
                    else:
                        localized_display = "—" if localized in (None, "") else str(localized)
                    match = matches[0]
                    if match.get("data-localization-status") != localization_status(raw_value, field):
                        errors.append(f"{route}: document card {card_id}/{field} localization status mismatch")
                    if match.get("data-localized-value") != localized_display:
                        errors.append(f"{route}: document card {card_id}/{field} localized value mismatch")
                    if (
                        locale == "es"
                        and isinstance(raw_value, str)
                        and raw_value not in STABLE_NAMES_OR_TERMS
                        and match.get("data-localized-value") == raw_value
                    ):
                        errors.append(f"{route}: document card {card_id}/{field} silently falls back to English")

                canonical_links = [
                    attrs
                    for tag, attrs in parser.elements
                    if tag == "a" and attrs.get("data-canonical-document-id") == card_id
                ]
                if disposition == "secondary-event-family-linked-appearance":
                    if len(canonical_links) != 1:
                        errors.append(f"{route}: secondary card {card_id} lacks one canonical link")
                    else:
                        canonical_link = canonical_links[0]
                        expected_href = f"../../../../{stable_page}"
                        if canonical_link.get("href") != expected_href:
                            errors.append(f"{route}: secondary card {card_id} canonical href mismatch")
                        if canonical_link.get("data-canonical-label-locale") != locale:
                            errors.append(f"{route}: secondary card {card_id} canonical link locale mismatch")
                elif canonical_links:
                    errors.append(f"{route}: canonical card {card_id} has a secondary-appearance link")

            expected_relations: Counter[tuple[str, str]] = Counter()
            for document in event.get("documents", []):
                relationships = document.get("relationship_to_other_documents_or_event", {})
                related_ids = (
                    relationships.get("related_document_ids", [])
                    if isinstance(relationships, dict)
                    else []
                )
                for related_id in related_ids:
                    expected_relations[(document["stable_id"], related_id)] += 1
            relation_links = parser.by_class("acta-document-relation", "a")
            actual_relations = Counter(
                (
                    link.get("data-source-document-id", ""),
                    link.get("data-related-document-id", ""),
                )
                for link in relation_links
            )
            if actual_relations != expected_relations:
                errors.append(f"{route}: rendered related-document link set mismatch")
            for link in relation_links:
                related_id = link.get("data-related-document-id", "")
                target = anchor_maps[locale].get(related_id)
                if target is None:
                    errors.append(f"{route}: relation link targets unmapped ID {related_id}")
                    continue
                if link.get("href") != target["href"]:
                    errors.append(f"{route}: relation link {related_id} canonical href mismatch")
                if link.get("data-related-target-kind") != target["target_kind"]:
                    errors.append(f"{route}: relation link {related_id} target kind mismatch")
                if link.get("data-related-label-locale") != locale:
                    errors.append(f"{route}: relation link {related_id} locale mismatch")
                if link.get("aria-label") != target["label"]:
                    errors.append(f"{route}: relation link {related_id} localized label mismatch")
                for attribute, target_field in (
                    ("data-perimeter", "target_perimeter"),
                    ("data-primary-lane", "target_primary_lane"),
                    ("data-perimeter-code", "target_perimeter_code"),
                    ("data-perimeter-label", "target_perimeter_label"),
                ):
                    if link.get(attribute) != target[target_field]:
                        errors.append(
                            f"{route}: relation link {related_id} {attribute} mismatch"
                        )

            relation_markers = parser.by_class(
                "acta-document-relation-marker", "li"
            )
            marker_relations = Counter(
                (
                    marker.get("data-source-document-id", ""),
                    marker.get("data-related-document-id", ""),
                )
                for marker in relation_markers
            )
            if marker_relations != expected_relations:
                errors.append(f"{route}: related-document perimeter-marker set mismatch")
            relation_badges = parser.by_class(
                "acta-document-relation-badge", "span"
            )
            badge_relations = Counter(
                (
                    badge.get("data-source-document-id", ""),
                    badge.get("data-related-document-id", ""),
                )
                for badge in relation_badges
            )
            if badge_relations != expected_relations:
                errors.append(f"{route}: related-document written-badge set mismatch")
            for marker_type, markers in (
                ("marker", relation_markers),
                ("badge", relation_badges),
            ):
                for marker in markers:
                    related_id = marker.get("data-related-document-id", "")
                    target = anchor_maps[locale].get(related_id)
                    if target is None:
                        continue
                    for attribute, target_field in (
                        ("data-perimeter", "target_perimeter"),
                        ("data-primary-lane", "target_primary_lane"),
                        ("data-perimeter-code", "target_perimeter_code"),
                    ):
                        if marker.get(attribute) != target[target_field]:
                            errors.append(
                                f"{route}: relation {marker_type} {related_id} "
                                f"{attribute} mismatch"
                            )
                    if marker_type == "badge":
                        badge_label = (
                            f'{target["target_perimeter_code"]} '
                            f'{target["target_perimeter_label"]}'
                        )
                        if marker.get("aria-label") != badge_label:
                            errors.append(
                                f"{route}: relation badge {related_id} lacks written localized code/label"
                            )

            related_ids = [item for item in event.get("related", []) if item in by_id]
            relationship_markers = [
                marker
                for marker in parser.by_class("acta-related-marker", "li")
                if "acta-document-relation-marker"
                not in marker.get("class", "").split()
            ]
            if len(relationship_markers) != len(related_ids):
                errors.append(f"{route}: relationship-marker count {len(relationship_markers)}/{len(related_ids)}")
            for marker in relationship_markers:
                perimeter = marker.get("data-perimeter")
                expected = EXPECTED_PERIMETERS.get(perimeter)
                if expected is None or marker.get("data-primary-lane") != expected[1]:
                    errors.append(f"{route}: relationship marker lacks valid perimeter/lane")

            transcript = event.get("transcript_path") or event.get("transcript_source")
            if transcript:
                if "acta-full-ocr" not in source:
                    errors.append(f"{route}: missing embedded public text record")
                if event.get("public_text_mode") == "full-page-redaction-markers":
                    expected_marker = (
                        "no es OCR público" if locale == "es" else "not public OCR"
                    )
                    if "acta-redaction-record" not in source or expected_marker not in source:
                        errors.append(f"{route}: marker-only public text is mislabeled as OCR")
                expected_pages = len(event.get("source_preview_pages", []))
                actual_pages = len(parser.by_class("acta-source-page", "a"))
                if expected_pages != actual_pages:
                    errors.append(f"{route}: source gallery {actual_pages}/{expected_pages}")
            elif "acta-source-gap" not in source:
                errors.append(f"{route}: missing explicit source-gap block")
            errors.extend(link_errors(page))


def validate_rooms_and_chronologies(events: list[dict], errors: list[str]) -> None:
    event_count = len(events)
    room_urls = {
        "es": f"{BASE_URL}/es/comunidad-instrumentalizacion/sala-documental-actas/",
        "en": f"{BASE_URL}/en/community-instrumentalisation/acta-document-room/",
    }
    for locale, room in ROOMS.items():
        if not room.is_file():
            errors.append(f"missing ACTA document room {room.relative_to(REPO)}")
            continue
        source = room.read_text(encoding="utf-8")
        errors.extend(
            page_metadata_errors(
                room,
                locale,
                room_urls[locale],
                {"es": room_urls["es"], "en": room_urls["en"], "x-default": room_urls["es"]},
            )
        )
        if "meeting-lineage-index-v1.json" not in source:
            errors.append(f"{room.relative_to(REPO)}: lineage index not wired")
        for perimeter in EXPECTED_PERIMETERS:
            if perimeter not in source:
                errors.append(f"{room.relative_to(REPO)}: legend/filter missing {perimeter}")
        expected_c1_label = (
            "Adverso atribuido · AAS → FMMM/Cogolludo/Pamanil"
            if locale == "es"
            else "Attributed adverse · AAS → FMMM/Cogolludo/Pamanil"
        )
        if source.count(expected_c1_label) < 2:
            errors.append(f"{room.relative_to(REPO)}: C1 legend/filter label is stale")
        stale_c1_label = (
            "Adverso alegado · Montelanza/Molina"
            if locale == "es"
            else "Alleged adverse · Montelanza/Molina"
        )
        if stale_c1_label in source:
            errors.append(f"{room.relative_to(REPO)}: old Montelanza/Molina C1 label remains")
        if source.count("ACTA-OWNER-ROLE-MATRIX:START") != 1 or source.count("ACTA-OWNER-ROLE-MATRIX:END") != 1:
            errors.append(f"{room.relative_to(REPO)}: Owners' ACTA role-matrix block count invalid")
        if source.count('class="acta-phase-code"') != len(OWNER_ROLE_MATRIX):
            errors.append(
                f"{room.relative_to(REPO)}: Owners' ACTA role rows "
                f"{source.count('class=\"acta-phase-code\"')}/{len(OWNER_ROLE_MATRIX)}"
            )
        for code, lineage in PRINCIPAL_LINEAGES.items():
            if lineage["label_es" if locale == "es" else "label_en"] not in source:
                errors.append(f"{room.relative_to(REPO)}: missing principal lineage {code}")
        if escape(PRE_2008_CONTROL[locale], quote=True) not in source:
            errors.append(f"{room.relative_to(REPO)}: missing pre-2008 ACTA finding")
        errors.extend(link_errors(room))

    for locale, chronology in CHRONOLOGIES.items():
        if not chronology.is_file():
            errors.append(f"missing chronology {chronology.relative_to(REPO)}")
            continue
        source = chronology.read_text(encoding="utf-8")
        if source.count("ACTA-LINEAGE-LINKS:START") != 1 or source.count("ACTA-LINEAGE-LINKS:END") != 1:
            errors.append(f"{chronology.relative_to(REPO)}: lineage block count invalid")
        phrase = "abrir ficha completa" if locale == "es" else "open complete record"
        if source.count(phrase) != event_count:
            errors.append(f"{chronology.relative_to(REPO)}: event-page links {source.count(phrase)}/{event_count}")
        errors.extend(link_errors(chronology))


def validate_sitemap(events: list[dict], errors: list[str]) -> None:
    try:
        root = ET.parse(SITEMAP).getroot()
    except (ET.ParseError, OSError) as exc:
        errors.append(f"sitemap parse failed: {exc}")
        return
    sitemap_ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    xhtml_ns = "{http://www.w3.org/1999/xhtml}"
    entries: dict[str, dict[str, str]] = {}
    for node in root.findall(f"{sitemap_ns}url"):
        loc_node = node.find(f"{sitemap_ns}loc")
        if loc_node is None or not loc_node.text:
            continue
        entries[loc_node.text] = {
            item.get("hreflang", ""): item.get("href", "")
            for item in node.findall(f"{xhtml_ns}link")
            if item.get("rel") == "alternate"
        }
    for event in events:
        es_url = event_url(event["detail_page_es"])
        en_url = event_url(event["detail_page_en"])
        expected = {"es": es_url, "en": en_url, "x-default": es_url}
        for url in (es_url, en_url):
            if url not in entries:
                errors.append(f"sitemap missing {url}")
            elif entries[url] != expected:
                errors.append(f"sitemap alternate set mismatch for {url}")


def validate_assets(errors: list[str]) -> None:
    css = CSS.read_text(encoding="utf-8")
    js = JS.read_text(encoding="utf-8")
    for perimeter, (code, lane) in EXPECTED_PERIMETERS.items():
        selector = f'[data-perimeter="{perimeter}"]'
        match = re.search(
            rf'{re.escape(selector)}\s*\{{\s*--perimeter-colour:\s*(#[0-9a-fA-F]{{6}});\s*--perimeter-bg:\s*(#[0-9a-fA-F]{{6}});',
            css,
        )
        if not match:
            errors.append(f"ACTA CSS missing colour tokens for {perimeter}")
        else:
            foreground, background = match.groups()
            if contrast(foreground, "#ffffff") < 4.5:
                errors.append(f"ACTA CSS code contrast fails WCAG AA for {perimeter}")
            if contrast("#173840", background) < 4.5:
                errors.append(f"ACTA CSS label contrast fails WCAG AA for {perimeter}")
        if perimeter not in js or f"code: '{code}'" not in js or f"primaryLane: '{lane}'" not in js:
            errors.append(f"document-room JS missing machine perimeter metadata for {perimeter}")
    for selector in (
        ".acta-perimeter-code",
        ".acta-lane-badge",
        ".acta-lineage-facts",
        ".acta-principal-legend",
        ".acta-principal-lineage",
        ".acta-owner-role-control",
        ".acta-owner-role-grid",
        ".acta-role-table",
        ".acta-document-card",
        ".acta-related-marker",
        ".acta-continuity-table",
        '[data-perimeter="mixed_or_contested"].acta-document-card',
        '[data-perimeter="unresolved"].acta-document-card',
    ):
        if selector not in css:
            errors.append(f"ACTA CSS missing accessible lineage selector {selector}")
    for stale_fallback_token in (
        "fallbackEvents",
        "fallbackPerimeters",
        "data.items",
        "suppliedById",
        "manifestState = 'fallback'",
    ):
        if stale_fallback_token in js:
            errors.append(
                f"document-room JS retains stale fallback token {stale_fallback_token!r}"
            )
    for required_fail_closed_token in (
        "let events = [];",
        "events = supplied.map(incoming => normaliseIndexEvent(incoming));",
        ".catch(renderIndexUnavailable)",
        "else renderIndexUnavailable();",
        "room.dataset.manifestState = 'unavailable';",
        "The public ACTA index could not be loaded. No evidential records are displayed.",
        "No se pudo cargar el índice público de ACTA. No se muestra ningún registro probatorio.",
        "Attributed adverse · AAS → FMMM / Cogolludo / Pamanil",
        "Adverso atribuido · AAS → FMMM / Cogolludo / Pamanil",
    ):
        if required_fail_closed_token not in js:
            errors.append(
                f"document-room JS missing fail-closed control {required_fail_closed_token!r}"
            )


def validate_public_locators(errors: list[str]) -> None:
    checker = REPO / "scripts/remediate_acta_public_locators.py"
    if not checker.is_file():
        errors.append("public-locator remediator/checker is missing")
        return
    result = subprocess.run(
        [sys.executable, str(checker), "--check"],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode:
        detail = (result.stdout + result.stderr).strip().replace("\n", " | ")
        errors.append(f"public-locator remediator check failed: {detail}")


def main() -> int:
    errors: list[str] = []
    try:
        continuity = json.loads(CONTINUITY.read_text(encoding="utf-8"))
        index = json.loads(INDEX.read_text(encoding="utf-8"))
        public_index = json.loads(PUBLIC_INDEX.read_text(encoding="utf-8"))
        reconciliation = json.loads(RECONCILIATION.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ACTA meeting-lineage validation: FAIL\n- unable to load indexes: {exc}")
        return 1

    continuity_families, continuity_documents = validate_continuity(continuity, errors)
    validate_public_register_source_rows(
        continuity, continuity_documents, errors
    )
    validate_package_source_controls(
        reconciliation, continuity_documents, public_index, errors
    )
    validate_known_unlocated_sources(
        reconciliation, continuity_documents, errors
    )
    canonical_source_ids = set(continuity_documents)
    indexed_source_ids = nested_source_document_ids(public_index) | nested_source_document_ids(reconciliation)
    unknown_indexed_source_ids = indexed_source_ids - canonical_source_ids
    if unknown_indexed_source_ids:
        errors.append(
            "source-document IDs diverge from continuity index: "
            + ", ".join(sorted(unknown_indexed_source_ids))
        )
    register_source_ids = set(
        re.findall(
            r"`(SP-SRC-[A-Z0-9-]+)`",
            PUBLIC_REGISTER.read_text(encoding="utf-8"),
        )
    )
    unknown_register_source_ids = register_source_ids - canonical_source_ids
    if unknown_register_source_ids:
        errors.append(
            "public-register source IDs diverge from continuity index: "
            + ", ".join(sorted(unknown_register_source_ids))
        )
    events, located = validate_index(index, continuity_families, continuity_documents, errors)
    validate_actor_route_catalog(errors)
    validate_event_pages(events, errors)
    validate_rooms_and_chronologies(events, errors)
    validate_sitemap(events, errors)
    validate_assets(errors)
    validate_public_locators(errors)

    if errors:
        print("ACTA meeting-lineage validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    gaps = len(events) - located
    marker_only = sum(
        bool(event.get("transcript_path") or event.get("transcript_source"))
        and event.get("public_text_mode") == "full-page-redaction-markers"
        for event in events
    )
    public_ocr = located - marker_only
    print("ACTA meeting-lineage validation: PASS")
    print(f"- {len(events)} controlled events / {len(events) * 2} bilingual pages")
    print(f"- {located} located source-gallery families: {public_ocr} public redacted-OCR editions + {marker_only} marker-only public redaction records; {gaps} explicit gap/non-ACTA entries")
    print(f"- {len(continuity_documents)} separately identified continuity documents")
    print("- perimeter labels/codes, contrast, mobile navigation and machine values checked")
    print("- canonical/hreflang/x-default, sitemap, local files and fragments reconciled")
    print("- public source locators pass the opaque-token privacy check")
    return 0


if __name__ == "__main__":
    sys.exit(main())
