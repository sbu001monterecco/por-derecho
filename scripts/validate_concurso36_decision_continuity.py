#!/usr/bin/env python3
"""Validate the bounded Concurso 36/2012 decision-continuity release.

The release is a continuity audit, not a certificate that the complete court
file has been obtained.  This gate reconciles its 51 public rows to the
canonical judicial-act sources, preserves same-date instruments and separate
proceedings, checks the bilingual web/XLSX derivatives, and prevents private
mail/Drive provenance from leaking into the public package.

Only Python's standard library is used so the check can run in GitHub Actions.
"""

from __future__ import annotations

import datetime as dt
import html
import json
import pathlib
import posixpath
import re
import sys
import urllib.parse
import xml.etree.ElementTree as ET
import zipfile
from collections import Counter, defaultdict
from html.parser import HTMLParser
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE_URL = "https://sbu001monterecco.github.io/por-derecho"

DATA = ROOT / "assets/data/concurso36-decision-continuity-2014-2026-v1.json"
XLSX = ROOT / "assets/data/concurso36-decision-continuity-2014-2026-v1.xlsx"
DOCX = ROOT / "assets/data/concurso36-decision-continuity-assessment-2014-2026.docx"
PDF = ROOT / "assets/data/concurso36-decision-continuity-assessment-2014-2026.pdf"
CATALOGUE = ROOT / "assets/data/concurso36-complete-record-v1.json"
COURT_FILE = ROOT / "assets/data/concurso36-court-file-v1.json"
AUTOS = ROOT / "assets/data/concurso36-autos-fulltext-v1.json"
CARET_DIGEST = ROOT / "assets/data/caepr-caret-unitary-digest-v1.json"

ES_PAGE = ROOT / "es/concurso-36-2012-autos-resoluciones/index.html"
EN_PAGE = ROOT / "en/insolvency-36-2012-orders-decisions/index.html"
ES_ROUTE = "/es/concurso-36-2012-autos-resoluciones/"
EN_ROUTE = "/en/insolvency-36-2012-orders-decisions/"
ES_URL = BASE_URL + ES_ROUTE
EN_URL = BASE_URL + EN_ROUTE

AUDIT = ROOT / "archive/CONCURSO36_DECISION_CONTINUITY_AUDIT_2014_2026_28AUG2026.md"
ADDENDA = (
    ROOT / "archive/MISSING_EVIDENCE_REGISTER_CONCURSO36_DECISION_CONTINUITY_ADDENDUM_28AUG2026.md",
    ROOT / "archive/CORRECTION_REGISTER_CONCURSO36_DECISION_CONTINUITY_ADDENDUM_28AUG2026.md",
    ROOT / "archive/CONTINUOUS_MAINTENANCE_MATRIX_CONCURSO36_DECISION_CONTINUITY_ADDENDUM_28AUG2026.md",
)
MANIFEST = ROOT / "publication-manifests/concurso36-court-decision-continuity-20260828.json"
CLOSEOUT = ROOT / "docs/deletion-audits/2026-08-28-concurso36-decision-continuity.md"
MAIN_SITEMAP = ROOT / "sitemap.xml"
COURT_SITEMAP = ROOT / "sitemap-concurso36-court-orders.xml"

EXPECTED_RESULT = {
    "audited_rows": 51,
    "core_primary_decisions_controlled": 28,
    "earlier_in_case_anchor_decisions_controlled": 4,
    "connected_or_contextual_primary_decisions_controlled": 2,
    "controlled_court_office_acts": 2,
    "unresolved_or_partial_family_rows": 15,
}
EXPECTED_RESULT_STATUS = (
    "PARTIAL — CERTIFIED DENOMINATOR AND DECISION FAMILIES STILL OPEN"
)
EXPECTED_CLASSIFICATIONS = {
    "core_primary_decision_controlled": 28,
    "earlier_in_case_anchor_decision_controlled": 4,
    "connected_or_contextual_primary_decision_controlled": 2,
    "controlled_court_office_act": 2,
    "unresolved_or_partial_family": 15,
}
CLASSIFICATION_LABELS = {
    "core_primary_decision_controlled": (
        "Decisión central primaria controlada", "Core primary decision controlled"
    ),
    "earlier_in_case_anchor_decision_controlled": (
        "Ancla interna anterior controlada", "Earlier in-case anchor controlled"
    ),
    "connected_or_contextual_primary_decision_controlled": (
        "Decisión conexa o contextual controlada",
        "Connected or contextual decision controlled",
    ),
    "controlled_court_office_act": (
        "Acto de oficina judicial controlado", "Court-office act controlled"
    ),
    "unresolved_or_partial_family": (
        "Familia abierta o parcial", "Open or partial family"
    ),
}
EXPECTED_STATE_COUNTS = {
    "PRIMARY_COPY_CONTROLLED": 32,
    "CONTEXTUAL_PRIMARY_COPY_CONTROLLED": 2,
    "COURT_OFFICE_COPY_CONTROLLED_FAMILY_INCOMPLETE": 2,
    "REFERENCED_PRIMARY_FAMILY_INCOMPLETE": 10,
    "UNCONFIRMED_SECONDARY_REFERENCE": 2,
    "IDENTITY_AND_OUTCOME_UNRESOLVED": 1,
    "PARTIAL_SOURCE_CHAIN": 1,
    "OPEN_FINAL_CHAIN": 1,
}
EXPECTED_SAME_DATE = {
    "2018-04-16": (
        "C36-DC-2018-04-16-PLAN", "C36-DC-2018-04-16-INTEREST"
    ),
    "2019-10-24": (
        "C36-DC-2019-10-24-NONCONVALIDATION", "C36-DC-2019-10-24-STANDING"
    ),
    "2020-05-12": ("C36-DC-2020-05-12-LPB", "C36-DC-2020-05-12-AUTO83"),
    "2021-02-24": (
        "C36-DC-2021-02-24-EXTENSION", "C36-DC-2021-02-24-WORKS"
    ),
    "2021-05-06": (
        "C36-DC-2021-05-06-RECONSIDERATION", "C36-DC-2021-05-06-AUTO356"
    ),
    "2021-10-15": ("C36-DC-2021-10-15-AUTO-A", "C36-DC-2021-10-15-AUTO-B"),
    "2022-01-26": ("C36-DC-2022-01-26-A", "C36-DC-2022-01-26-B"),
    "2025-09-12": ("C36-DC-2025-09-12-R05", "C36-DC-2025-09-12-R06"),
}
ALLOWED_DATE_STATUS = {
    "exact", "reported_date", "aggregate_earliest_date",
    "year_only_sort_key", "undated_future_endpoint",
}
FLAG_TO_CLASSIFICATION = {
    "core_controlled_decision": "core_primary_decision_controlled",
    "earlier_in_case_anchor": "earlier_in_case_anchor_decision_controlled",
    "contextual_control": "connected_or_contextual_primary_decision_controlled",
    "controlled_court_office_act": "controlled_court_office_act",
}

EXPECTED_XLSX_HEADERS = [
    "Sort date (ISO)", "Same-date seq", "Period / periodo", "Stable ID",
    "Family (ES)", "Family (EN)", "Proceeding / lane (ES)",
    "Proceeding / lane (EN)", "Coverage state", "Status (ES)",
    "Status (EN)", "Classification code", "Classification (ES)",
    "Classification (EN)", "Row type", "Date status",
    "Canonical record IDs", "Priority", "Copy control", "Public access",
    "Remaining gap (ES)", "Remaining gap (EN)", "Public ES", "Public EN",
]

REQUIRED_MANIFEST_SOURCES = {
    "publication-manifests/concurso36-court-decision-continuity-20260828.json",
    "assets/data/concurso36-decision-continuity-2014-2026-v1.json",
    "assets/data/concurso36-decision-continuity-2014-2026-v1.xlsx",
    "assets/data/concurso36-decision-continuity-assessment-2014-2026.docx",
    "assets/data/concurso36-decision-continuity-assessment-2014-2026.pdf",
    "assets/data/concurso36-complete-record-v1.json",
    "assets/data/concurso36-court-file-v1.json",
    "assets/data/concurso36-autos-fulltext-v1.json",
    "assets/data/caepr-caret-unitary-digest-v1.json",
    "archive/CONCURSO36_DECISION_CONTINUITY_AUDIT_2014_2026_28AUG2026.md",
    "archive/MISSING_EVIDENCE_REGISTER_CONCURSO36_DECISION_CONTINUITY_ADDENDUM_28AUG2026.md",
    "archive/CORRECTION_REGISTER_CONCURSO36_DECISION_CONTINUITY_ADDENDUM_28AUG2026.md",
    "archive/CONTINUOUS_MAINTENANCE_MATRIX_CONCURSO36_DECISION_CONTINUITY_ADDENDUM_28AUG2026.md",
    "archive/CONCURSO36_COMPLETE_RECORD_EXECUTION_DIGEST_23AUG2026.md",
    "archive/CONCURSO36_AUTOS_FULLTEXT_UNITARY_RECORD_23AUG2026.md",
    "archive/CONCURSO_36_2012_UNITARY_COURT_FILE_RECONSTRUCTION_24AUG2026.md",
    "scripts/build_concurso_autos_pages.py",
    "scripts/build_concurso36_complete_record.py",
    "scripts/build_concurso_autos_fulltext.py",
    "scripts/validate_concurso36_decision_continuity.py",
    "scripts/validate_concurso36_complete_record.py",
    "scripts/validate_concurso_autos_publication.py",
    "scripts/validate_concurso36_primary_autos_redigest.py",
    ".github/workflows/validate-concurso36-decision-continuity.yml",
    "docs/deletion-audits/2026-08-28-concurso36-decision-continuity.md",
    "docs/deletion-audits/README.md",
    "sitemap.xml",
    "sitemap-concurso36-court-orders.xml",
    "es/concurso-36-2012-autos-resoluciones/index.html",
    "en/insolvency-36-2012-orders-decisions/index.html",
}

LIFECYCLE = (
    "DRAFT", "PREPARED_PENDING_MERGE", "REMOTE_SOURCE", "PR_OPEN",
    "CI_GREEN", "MERGED", "DEPLOYED", "LIVE_VERIFIED", "DELETION_SAFE",
    "BLOCKED_RECOVERY",
)

EMAIL_RE = re.compile(
    r"(?i)(?<![\w.+-])[a-z0-9.!#$%&'*+/=?^_`{|}~-]+@"
    r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?"
    r"(?:\.[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?)+"
)
PRIVACY_PATTERNS = {
    "email address": EMAIL_RE,
    "Google mail/Drive URL": re.compile(
        r"https?://(?:mail|drive|docs)\.google\.com[^\s\"'<>]*", re.I
    ),
    "provider message or Drive identifier": re.compile(
        r"\b(?:gmail|message(?:[_ -]?id)?|drive(?:[_ -]?(?:id|object))?|attachment)"
        r"\s*[:=#]\s*[a-z0-9_-]{16,}\b", re.I
    ),
    "mailbox file": re.compile(r"(?i)\b[^\s/\\]+\.(?:eml|mbox|msg)\b"),
    "auth-bearing URL query": re.compile(
        r"(?i)https?://[^\s\"'<>]+[?&](?:authuser|token|access_token|code|usp|id)="
    ),
    "court verification code": re.compile(
        r"(?i)\bA05003250-[A-Za-z0-9-]+\b|"
        r"\b(?:CSV|c[oó]digo\s+seguro\s+de\s+verificaci[oó]n)\s*[:#-]\s*"
        r"(?=[A-Z0-9-]*\d)[A-Z0-9-]{8,}\b"
    ),
    "court personal locator": re.compile(
        r"(?i)\b(?:NIG|IUP)\s*[:#-]?\s*[A-Z0-9/-]{8,}\b"
    ),
    "private filesystem path": re.compile(
        r"(?i)(?:/Users/|/home/|/workspace/|[A-Z]:\\Users\\)[^\s\"'<>]+"
    ),
}


def relative(path: pathlib.Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def read_text(path: pathlib.Path, failures: list[str]) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        failures.append(f"missing required file: {relative(path)}")
    except UnicodeDecodeError as exc:
        failures.append(f"UTF-8 decode failed for {relative(path)}: {exc}")
    return ""


def load_json(path: pathlib.Path, failures: list[str]) -> dict[str, Any]:
    text = read_text(path, failures)
    if not text:
        return {}
    try:
        value = json.loads(text)
    except json.JSONDecodeError as exc:
        failures.append(f"invalid JSON in {relative(path)}: {exc}")
        return {}
    if not isinstance(value, dict):
        failures.append(f"top-level JSON is not an object: {relative(path)}")
        return {}
    return value


def iso_date(value: Any) -> dt.date | None:
    if not isinstance(value, str):
        return None
    try:
        return dt.date.fromisoformat(value)
    except ValueError:
        return None


def check_privacy(label: str, text: str, failures: list[str]) -> None:
    for description, pattern in PRIVACY_PATTERNS.items():
        match = pattern.search(text)
        if match:
            failures.append(
                f"privacy leak ({description}) in {label}: {match.group(0)[:100]!r}"
            )


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.hrefs: list[str] = []
        self.canonicals: list[str] = []
        self.alternates: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.append(str(values["id"]))
        if tag == "a" and values.get("href"):
            self.hrefs.append(str(values["href"]))
        if tag == "link" and values.get("href"):
            rel_value = str(values.get("rel", ""))
            if rel_value == "canonical":
                self.canonicals.append(str(values["href"]))
            if rel_value == "alternate" and values.get("hreflang"):
                self.alternates.append((str(values["hreflang"]), str(values["href"])))


def extract_continuity_section(text: str, anchor: str) -> str:
    marker = f'id="{anchor}"'
    position = text.find(marker)
    if position < 0:
        return ""
    start = text.rfind("<section", 0, position)
    end = text.find("<section", position + len(marker))
    return text[start:end if end >= 0 else len(text)]


def public_url(row: dict[str, Any], language: str) -> str:
    href = row.get(f"public_href_{language}")
    route = ES_URL if language == "es" else EN_URL
    section = "continuidad-2014-2026" if language == "es" else "continuity-2014-2026"
    if isinstance(href, str) and href:
        return urllib.parse.urljoin(route, href)
    anchor = row.get("public_anchor")
    if isinstance(anchor, str) and anchor:
        return f"{route}#{anchor}"
    return f"{route}#{section}"


def local_target(page: pathlib.Path, href: str) -> tuple[pathlib.Path | None, str]:
    parsed = urllib.parse.urlsplit(href)
    fragment = parsed.fragment
    if parsed.scheme:
        if not href.startswith(BASE_URL + "/"):
            return None, fragment
        raw_path = parsed.path.removeprefix("/por-derecho/")
        target = ROOT / urllib.parse.unquote(raw_path)
    else:
        target = page.parent / urllib.parse.unquote(parsed.path)
    target = target.resolve()
    try:
        target.relative_to(ROOT.resolve())
    except ValueError:
        return None, fragment
    if not parsed.path:
        target = page
    elif target.is_dir() or parsed.path.endswith("/"):
        target = target / "index.html"
    return target, fragment


def check_rows(
    data: dict[str, Any], catalogue: dict[str, Any], court_file: dict[str, Any],
    autos: dict[str, Any], caret_digest: dict[str, Any], failures: list[str],
) -> list[dict[str, Any]]:
    scope = data.get("scope")
    result = data.get("result")
    labels = data.get("status_labels")
    rows = data.get("rows")
    require(isinstance(scope, dict), "continuity JSON scope must be an object", failures)
    require(isinstance(result, dict), "continuity JSON result must be an object", failures)
    require(isinstance(labels, dict), "continuity JSON status_labels must be an object", failures)
    require(isinstance(rows, list), "continuity JSON rows must be an array", failures)
    if not all(isinstance(item, dict) for item in rows or []):
        failures.append("every continuity row must be an object")
        return []
    rows = list(rows or [])

    if isinstance(scope, dict):
        require(scope.get("start") == "2014-01-01", "scope start must be 2014-01-01", failures)
        require(scope.get("cutoff") == "2026-08-28", "scope cutoff must be 2026-08-28", failures)
        require(scope.get("proceeding") == "Concurso ordinario 36/2012^",
                "scope proceeding must preserve the CAEPR caret suffix", failures)
        require(scope.get("caepr_id") == "PD-SP-R-0001", "scope CAEPR ID drift", failures)
        require(scope.get("caepr_resolution_status") == "CARET_CONFIRMED",
                "scope CAEPR state must be CARET_CONFIRMED", failures)
        caret_es = scope.get("caret_definition_es", "")
        caret_en = scope.get("caret_definition_en", "")
        require("^" in caret_es and "no es una nota" in caret_es and "altera" in caret_es,
                "Spanish caret definition is incomplete", failures)
        require("^" in caret_en and "not a footnote" in caret_en and "does not alter" in caret_en,
                "English caret definition is incomplete", failures)
        for key in ("included_es", "included_en", "excluded_es", "excluded_en",
                    "aggregate_exception_es", "aggregate_exception_en"):
            require(isinstance(scope.get(key), str) and bool(scope.get(key).strip()),
                    f"scope missing bilingual boundary field {key}", failures)
        require("no es un censo completo" in str(scope.get("excluded_es", "")).lower(),
                "Spanish scope must disclaim a complete census", failures)
        require("not a full" in str(scope.get("excluded_en", "")).lower(),
                "English scope must disclaim a complete census", failures)

    if isinstance(result, dict):
        require(result.get("status") == EXPECTED_RESULT_STATUS, "result status drift", failures)
        for key, expected in EXPECTED_RESULT.items():
            require(result.get(key) == expected,
                    f"result {key} must be {expected}, got {result.get(key)!r}", failures)
        require(result.get("certified_docket_obtained") is False,
                "certified_docket_obtained must remain false", failures)
        require(result.get("official_denominator") is None,
                "official_denominator must remain null", failures)
        require(result.get("complete_procedural_family_count") is None,
                "complete_procedural_family_count must remain null", failures)
        for key in ("counting_rule_es", "counting_rule_en"):
            require(isinstance(result.get(key), str) and bool(result.get(key).strip()),
                    f"result missing {key}", failures)

    state_counts = Counter(row.get("coverage_state") for row in rows)
    require(state_counts == Counter(EXPECTED_STATE_COUNTS),
            f"coverage-state partition drift: {dict(state_counts)}", failures)
    class_counts = Counter(row.get("classification") for row in rows)
    require(class_counts == Counter(EXPECTED_CLASSIFICATIONS),
            f"classification partition drift: {dict(class_counts)}", failures)
    require(len(rows) == 51, f"expected 51 rows, found {len(rows)}", failures)

    if isinstance(labels, dict):
        used_states = set(state_counts)
        require(used_states <= set(labels),
                f"status label map omits used states: {sorted(used_states - set(labels))}", failures)
        for state, pair in labels.items():
            require(isinstance(pair, dict) and isinstance(pair.get("es"), str)
                    and isinstance(pair.get("en"), str) and pair.get("es") and pair.get("en"),
                    f"status {state} lacks non-empty ES/EN labels", failures)

    seen_ids: set[str] = set()
    ordered: list[tuple[str, int]] = []
    date_groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for index, row in enumerate(rows, start=1):
        prefix = f"row {index} ({row.get('id', '<missing>')})"
        row_id = row.get("id")
        require(isinstance(row_id, str) and bool(re.fullmatch(r"C36-DC-[A-Z0-9-]+", row_id or "")),
                f"{prefix}: invalid stable ID", failures)
        if isinstance(row_id, str):
            require(row_id not in seen_ids, f"duplicate row ID: {row_id}", failures)
            seen_ids.add(row_id)
        for key in ("period", "sort_date", "family_es", "family_en", "coverage_state",
                    "gap_es", "gap_en", "priority", "date_status", "row_type",
                    "classification", "public_access_status"):
            require(isinstance(row.get(key), str) and bool(row.get(key).strip()),
                    f"{prefix}: missing non-empty {key}", failures)
        proceeding_es = row.get("proceeding_es", row.get("proceeding"))
        proceeding_en = row.get("proceeding_en", row.get("proceeding"))
        require(isinstance(proceeding_es, str) and bool(proceeding_es.strip()),
                f"{prefix}: missing proceeding_es", failures)
        require(isinstance(proceeding_en, str) and bool(proceeding_en.strip()),
                f"{prefix}: missing proceeding_en", failures)
        require(isinstance(row.get("canonical_record_ids"), list)
                and all(isinstance(value, str) and value for value in row.get("canonical_record_ids", [])),
                f"{prefix}: canonical_record_ids must be a string array", failures)
        sequence = row.get("same_date_sequence")
        require(isinstance(sequence, int) and not isinstance(sequence, bool) and sequence > 0,
                f"{prefix}: invalid same_date_sequence", failures)
        sort_date = row.get("sort_date")
        parsed_date = iso_date(sort_date)
        require(parsed_date is not None, f"{prefix}: invalid ISO sort_date", failures)
        if parsed_date and isinstance(sequence, int):
            ordered.append((sort_date, sequence))
            date_groups[sort_date].append(row)
        date_status = row.get("date_status")
        require(date_status in ALLOWED_DATE_STATUS,
                f"{prefix}: unsupported date_status {date_status!r}", failures)
        if parsed_date and date_status in {"exact", "reported_date"}:
            expected_period = parsed_date.strftime("%d/%m/%Y")
            require(str(row.get("period", "")).startswith(expected_period),
                    f"{prefix}: period must expose the ISO date", failures)
        if date_status == "year_only_sort_key":
            require(str(row.get("period")) == str(sort_date)[:4]
                    and str(sort_date)[5:] in {"01-01", "12-31"},
                    f"{prefix}: invalid declared year-only key", failures)
        if date_status == "undated_future_endpoint":
            require(sort_date == "9999-12-31" and row.get("row_type") == "future_endpoint",
                    f"{prefix}: invalid future endpoint", failures)
        flags = []
        for flag in FLAG_TO_CLASSIFICATION:
            require(type(row.get(flag)) is bool, f"{prefix}: {flag} must be boolean", failures)
            if row.get(flag) is True:
                flags.append(flag)
        classification = row.get("classification")
        if flags:
            require(len(flags) == 1, f"{prefix}: controlled category flags overlap", failures)
            require(classification == FLAG_TO_CLASSIFICATION[flags[0]],
                    f"{prefix}: flag/classification mismatch", failures)
        else:
            require(classification == "unresolved_or_partial_family",
                    f"{prefix}: unflagged row must remain unresolved/partial", failures)
        state = row.get("coverage_state")
        if classification in {
            "core_primary_decision_controlled",
            "earlier_in_case_anchor_decision_controlled",
        }:
            require(state == "PRIMARY_COPY_CONTROLLED",
                    f"{prefix}: in-case controlled decision has wrong state", failures)
        elif classification == "connected_or_contextual_primary_decision_controlled":
            require(state == "CONTEXTUAL_PRIMARY_COPY_CONTROLLED",
                    f"{prefix}: contextual decision has wrong state", failures)
        elif classification == "controlled_court_office_act":
            require(state == "COURT_OFFICE_COPY_CONTROLLED_FAMILY_INCOMPLETE",
                    f"{prefix}: controlled court-office act has wrong state", failures)
        else:
            require(state not in {
                "PRIMARY_COPY_CONTROLLED", "CONTEXTUAL_PRIMARY_COPY_CONTROLLED",
                "COURT_OFFICE_COPY_CONTROLLED_FAMILY_INCOMPLETE",
            }, f"{prefix}: unresolved row uses a controlled state", failures)

    require(ordered == sorted(ordered), "rows are not sorted by ISO date and sequence", failures)
    actual_pairs = {date: tuple(item.get("id") for item in group)
                    for date, group in date_groups.items() if len(group) > 1}
    require(actual_pairs == EXPECTED_SAME_DATE,
            f"same-date instrument partition drift: {actual_pairs}", failures)
    for date, group in date_groups.items():
        sequences = [item.get("same_date_sequence") for item in group]
        require(sequences == list(range(1, len(group) + 1)),
                f"{date}: same-date sequence must be contiguous from 1", failures)
        if len(group) == 2:
            require(str(group[0].get("period", "")).endswith("· A")
                    and str(group[1].get("period", "")).endswith("· B"),
                    f"{date}: paired instruments must be displayed as A/B", failures)

    catalogue_rows = catalogue.get("records", [])
    require(isinstance(catalogue_rows, list), "canonical catalogue records missing", failures)
    catalogue_by_id = {item.get("canonical_id"): item for item in catalogue_rows
                       if isinstance(item, dict) and isinstance(item.get("canonical_id"), str)}
    complete_judicial = {
        key: item for key, item in catalogue_by_id.items()
        if item.get("record_class") == "judicial_act"
        and "2014-01-01" <= str(item.get("date", "")) <= "2026-08-28"
        and str(item.get("complete_copy_status", "")).lower().startswith("yes")
    }
    require(len(complete_judicial) == 31,
            f"canonical complete judicial-act denominator must be 31, found {len(complete_judicial)}",
            failures)
    controlled_classes = set(EXPECTED_CLASSIFICATIONS) - {
        "controlled_court_office_act", "unresolved_or_partial_family"
    }
    controlled = [row for row in rows if row.get("classification") in controlled_classes]
    canonical_usage: Counter[str] = Counter()
    special_ids = {
        "PD-SP-R-0007", "C36-JUD-2017-03-22-OPEN-CONVENIO",
        "C36-JUD-2017-05-05-AC-REMUNERATION",
    }
    for row in controlled:
        ids = row.get("canonical_record_ids", [])
        require(len(ids) == 1,
                f"{row.get('id')}: every controlled decision must have one canonical ID", failures)
        if len(ids) != 1:
            continue
        canonical_id = ids[0]
        if canonical_id not in special_ids:
            canonical_usage[canonical_id] += 1
            source = complete_judicial.get(canonical_id)
            require(source is not None,
                    f"{row.get('id')}: controlled ID {canonical_id} is not a complete judicial act",
                    failures)
            if source:
                require(source.get("date") == row.get("sort_date"),
                        f"{row.get('id')}: canonical date mismatch for {canonical_id}", failures)
                label = str(source.get("evidence_label", "")).upper()
                require("PRIMARY DOCUMENT" in label or "SOURCE COPY LOCATED" in label,
                        f"{canonical_id}: canonical evidence label does not support copy control",
                        failures)
    require(set(canonical_usage) == set(complete_judicial),
            "controlled chronology does not cover every complete canonical judicial act exactly once; "
            f"missing={sorted(set(complete_judicial)-set(canonical_usage))}, "
            f"extra={sorted(set(canonical_usage)-set(complete_judicial))}", failures)
    for canonical_id, count in canonical_usage.items():
        require(count == 1, f"canonical judicial act {canonical_id} used {count} times", failures)

    court_rows = court_file.get("records", [])
    court_by_id = {item.get("id"): item for item in court_rows if isinstance(item, dict)}
    for canonical_id, expected_date in {
        "C36-JUD-2017-03-22-OPEN-CONVENIO": "2017-03-22",
        "C36-JUD-2017-05-05-AC-REMUNERATION": "2017-05-05",
    }.items():
        source = court_by_id.get(canonical_id, {})
        require(source.get("date") == expected_date and source.get("kind") == "judicial_order"
                and source.get("status") == "primary_text",
                f"court-file source control failed for {canonical_id}", failures)
    ap89 = next((row for row in rows if row.get("id") == "C36-DC-2014-AP89-CONTEXT"), {})
    require(ap89.get("canonical_record_ids") == ["PD-SP-R-0007"]
            and ap89.get("classification") == "connected_or_contextual_primary_decision_controlled"
            and "separad" in str(ap89.get("proceeding_es", ap89.get("proceeding", ""))).lower(),
            "Judgment 89/2014 must remain a separately controlled contextual lane", failures)

    office_rows = [row for row in rows if row.get("controlled_court_office_act") is True]
    require({row.get("id") for row in office_rows} == {
        "C36-DC-2021-10-25-DIOR", "C36-DC-2021-10-27-DILIGENCIA"
    }, "selected controlled court-office acts drift", failures)
    office_27 = next((row for row in office_rows if row.get("sort_date") == "2021-10-27"), {})
    source_48 = catalogue_by_id.get("C36-E048", {})
    require(office_27.get("canonical_record_ids") == ["C36-E048"]
            and source_48.get("record_class") == "laj_or_court_office_act"
            and source_48.get("date") == "2021-10-27"
            and str(source_48.get("complete_copy_status", "")).lower().startswith("yes"),
            "27 October court-office act is not reconciled to C36-E048", failures)
    office_25 = next((row for row in office_rows if row.get("sort_date") == "2021-10-25"), {})
    require(office_25.get("canonical_record_ids") == []
            and office_25.get("copy_control_status") == "VERIFIED_PARTIAL"
            and "testimonios" in str(office_25.get("gap_es", "")).lower()
            and "service" in str(office_25.get("gap_en", "")).lower(),
            "25 October court-office act must remain a partial family without invented canonical ID",
            failures)

    source_pair_dates = Counter(item.get("date") for item in complete_judicial.values())
    require({date for date, count in source_pair_dates.items() if count > 1} == set(EXPECTED_SAME_DATE),
            "canonical same-date judicial pairs no longer match the public partition", failures)

    autos_rows = autos.get("documents", [])
    autos_by_id = {item.get("id"): item for item in autos_rows if isinstance(item, dict)}
    for anchor in ("R05", "R06", "R09", "F13", "R26", "R30"):
        row = next((item for item in rows if item.get("public_anchor") == anchor), {})
        source = autos_by_id.get(anchor, {})
        require(row and row.get("canonical_record_ids") == [f"C36-SPECIALIST-{anchor}"],
                f"specialist anchor {anchor} lacks canonical continuity row", failures)
        require(source.get("record_class") == "court" and source.get("date") == row.get("sort_date")
                and "localizada" in str(source.get("copy_status", "")).lower(),
                f"specialist source mismatch for {anchor}", failures)

    by_id = {row.get("id"): row for row in rows}
    creditor = by_id.get("C36-DC-2018-02-15-CREDITOR", {})
    conflict = creditor.get("date_layer_conflict", {})
    require(isinstance(conflict, dict)
            and conflict.get("repository_control_date") == "2018-02-15"
            and conflict.get("primary_body_or_recital_date") == "2018-02-08"
            and conflict.get("signature_layer_dates") == ["2018-02-09", "2018-02-14"]
            and conflict.get("distinct_act_inferred") is False
            and conflict.get("status") == "DIRECT_PRIMARY_REINSPECTION_OPEN",
            "15 February 2018 date-layer control is incomplete", failures)
    require("C36-DC-2018-02-08" not in seen_ids,
            "8 February date layer must not be promoted to a distinct act", failures)
    tc = by_id.get("C36-DC-2023-10-23-TC2811", {})
    require(tc.get("coverage_state") == "UNCONFIRMED_SECONDARY_REFERENCE"
            and tc.get("date_status") == "reported_date"
            and tc.get("canonical_record_ids") == []
            and "no afirmar" in str(tc.get("gap_es", "")).lower()
            and "do not state" in str(tc.get("gap_en", "")).lower(),
            "TC 2811/2023 must remain a reported, unconfirmed reference", failures)
    auto164 = by_id.get("C36-DC-2021-05-18-AUTO164", {})
    require("firmeza" in str(auto164.get("gap_es", "")).lower()
            and "finality" in str(auto164.get("gap_en", "")).lower(),
            "18 May 2021 controlled copy must leave finality open", failures)
    j163 = by_id.get("C36-DC-2023-09-28-J163", {})
    require(("apel" in str(j163.get("gap_es", "")).lower()
             or "recurr" in str(j163.get("gap_es", "")).lower())
            and "appeal" in str(j163.get("gap_en", "")).lower(),
            "Judgment 163/2023 must preserve its open appeal", failures)
    for row_id in ("C36-DC-2025-09-12-R05", "C36-DC-2026-01-21-F13"):
        row = by_id.get(row_id, {})
        require("fondo" in str(row.get("gap_es", "")).lower()
                and "merits" in str(row.get("gap_en", "")).lower(),
                f"{row_id}: merits must remain open", failures)
    r30 = by_id.get("C36-DC-2026-07-15-R30", {})
    require("acumul" in (str(r30.get("family_es", "")) + str(r30.get("gap_es", ""))).lower()
            and "no resuelve el fondo" in str(r30.get("gap_es", "")).lower()
            and "does not decide the merits" in str(r30.get("gap_en", "")).lower(),
            "R30 accumulation order must not be upgraded to a merits decision", failures)

    refined = data.get("audit_prompt", {})
    require(isinstance(refined, dict), "refined_prompt must be bilingual", failures)
    for language in ("es", "en"):
        text = str(refined.get(language, ""))
        require("36/2012^" in text, f"refined prompt {language} lost the caret suffix", failures)
        require(("Google Drive" in text or "correo" in text or "email" in text)
                and ("PDF" in text) and ("XLSX" in text),
                f"refined prompt {language} omits requested source/deliverable classes", failures)
    require("No envíe correo" in str(refined.get("es", ""))
            and "Do not send email" in str(refined.get("en", "")),
            "refined prompt must preserve the no-send/no-file authority boundary", failures)

    confirmed = caret_digest.get("confirmed_objects", [])
    matches = [item for item in confirmed if isinstance(item, dict)
               and item.get("id") == "PD-SP-R-0001"]
    require(len(matches) == 1 and matches[0].get("state") == "CARET_CONFIRMED"
            and matches[0].get("type") == "PROCEEDING",
            "CAEPR digest does not confirm PD-SP-R-0001 exactly once", failures)
    return rows


def check_pages(rows: list[dict[str, Any]], data: dict[str, Any], failures: list[str]) -> None:
    page_data: dict[str, tuple[pathlib.Path, str, str, str, str, str]] = {
        "es": (ES_PAGE, ES_URL, "continuidad-2014-2026", "51 filas de control", "Fecha exacta",
               "PARCIAL — SIGUEN ABIERTOS EL DENOMINADOR CERTIFICADO Y FAMILIAS DE RESOLUCIONES"),
        "en": (EN_PAGE, EN_URL, "continuity-2014-2026", "51 control rows", "Exact date",
               EXPECTED_RESULT_STATUS),
    }
    labels = data.get("status_labels", {})
    for language, (path, url, section_id, caption_marker, exact_marker, status_marker) in page_data.items():
        text = read_text(path, failures)
        parser = PageParser()
        parser.feed(text)
        section = extract_continuity_section(text, section_id)
        require(section, f"{relative(path)} missing #{section_id} section", failures)
        require(text.count(f'id="{section_id}"') == 1,
                f"{relative(path)} must contain #{section_id} exactly once", failures)
        require(parser.canonicals == [url], f"{relative(path)} canonical URL drift", failures)
        expected_alternates = {("es", ES_URL), ("en", EN_URL)}
        require(expected_alternates <= set(parser.alternates),
                f"{relative(path)} lacks reciprocal ES/EN alternates", failures)
        require(caption_marker in section and section.count('class="audit-date-status"') == 51,
                f"{relative(path)} does not render the 51-row chronology", failures)
        require("<span>28</span>" in section and status_marker in section,
                f"{relative(path)} summary counts/status drift", failures)
        require(exact_marker in section, f"{relative(path)} lacks date-status labelling", failures)
        for row in rows:
            row_id = str(row.get("id"))
            require(section.count(row_id) == 1,
                    f"{relative(path)} must render {row_id} exactly once", failures)
            values = (
                row.get(f"family_{language}"),
                row.get(f"proceeding_{language}", row.get("proceeding")),
                row.get(f"gap_{language}"),
                labels.get(row.get("coverage_state"), {}).get(language),
            )
            for value in values:
                escaped = html.escape(str(value), quote=True)
                require(escaped in section,
                        f"{relative(path)} missing public-safe {language} value for {row_id}: {value!r}",
                        failures)
            href = row.get(f"public_href_{language}")
            if isinstance(href, str) and href:
                require(f'href="{html.escape(href, quote=True)}"' in section,
                        f"{relative(path)} missing local public link for {row_id}", failures)
                target, fragment = local_target(path, href)
                require(target is not None and target.is_file(),
                        f"{row_id}: public {language} link does not resolve locally: {href}", failures)
                if target and target.is_file() and fragment and target.suffix.lower() in {".html", ".htm"}:
                    target_parser = PageParser()
                    target_parser.feed(read_text(target, failures))
                    require(fragment in target_parser.ids,
                            f"{row_id}: link fragment #{fragment} missing from {relative(target)}", failures)
            anchor = row.get("public_anchor")
            if isinstance(anchor, str) and anchor:
                require(anchor in parser.ids,
                        f"{relative(path)} missing source anchor #{anchor} for {row_id}", failures)
        for artifact in (
            "../../assets/data/concurso36-decision-continuity-2014-2026-v1.json",
            "../../assets/data/concurso36-decision-continuity-2014-2026-v1.xlsx",
            "../../assets/data/concurso36-decision-continuity-assessment-2014-2026.docx",
            "../../assets/data/concurso36-decision-continuity-assessment-2014-2026.pdf",
            "../../archive/CONCURSO36_DECISION_CONTINUITY_AUDIT_2014_2026_28AUG2026.md",
        ):
            require(f'href="{artifact}"' in section,
                    f"{relative(path)} missing release link {artifact}", failures)
            target, _ = local_target(path, artifact)
            require(target is not None and target.is_file(),
                    f"release link does not resolve locally: {artifact}", failures)
        check_privacy(f"{relative(path)}#{section_id}", html.unescape(section), failures)


def relationship_part(part: str) -> str:
    directory, name = posixpath.split(part)
    return posixpath.join(directory, "_rels", name + ".rels")


def xlsx_cells(root: ET.Element, shared: list[str]) -> tuple[dict[str, str], dict[str, str]]:
    ns = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
    values: dict[str, str] = {}
    formulas: dict[str, str] = {}
    for cell in root.findall(".//" + ns + "c"):
        ref = cell.get("r")
        if not ref:
            continue
        formula = cell.find(ns + "f")
        if formula is not None:
            formulas[ref] = formula.text or ""
        value = cell.find(ns + "v")
        cell_type = cell.get("t")
        if cell_type == "inlineStr":
            values[ref] = "".join(node.text or "" for node in cell.iter(ns + "t"))
        elif value is None:
            values[ref] = ""
        elif cell_type == "s":
            try:
                values[ref] = shared[int(value.text or "0")]
            except (ValueError, IndexError):
                values[ref] = ""
        else:
            values[ref] = value.text or ""
    return values, formulas


def check_xlsx(rows: list[dict[str, Any]], data: dict[str, Any], failures: list[str]) -> None:
    if not XLSX.is_file():
        failures.append(f"missing required file: {relative(XLSX)}")
        return
    ns = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
    rel_ns = "{http://schemas.openxmlformats.org/package/2006/relationships}"
    office_rel = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
    try:
        with zipfile.ZipFile(XLSX) as package:
            names = package.namelist()
            require(package.testzip() is None, "XLSX ZIP CRC check failed", failures)
            require(len(names) == len(set(names)), "XLSX contains duplicate ZIP members", failures)
            for name in names:
                pure = pathlib.PurePosixPath(name)
                require(not name.startswith("/") and ".." not in pure.parts,
                        f"XLSX contains unsafe ZIP member: {name}", failures)
            forbidden = (
                "vbaproject", "macrosheet", "xl/externallinks", "xl/connections",
                "customxml", "comments", "threadedcomments", "persons", "embeddings",
                "activex", "ctrlprops",
            )
            for name in names:
                lower = name.lower()
                require(not any(marker in lower for marker in forbidden),
                        f"XLSX contains forbidden active/private part: {name}", failures)
            for name in names:
                if name.endswith(".rels"):
                    rel_root = ET.fromstring(package.read(name))
                    for relationship in rel_root.findall(rel_ns + "Relationship"):
                        require(relationship.get("TargetMode") != "External",
                                f"XLSX external relationship forbidden in {name}", failures)

            shared: list[str] = []
            if "xl/sharedStrings.xml" in names:
                shared_root = ET.fromstring(package.read("xl/sharedStrings.xml"))
                for item in shared_root.findall(ns + "si"):
                    shared.append("".join(node.text or "" for node in item.iter(ns + "t")))
            workbook = ET.fromstring(package.read("xl/workbook.xml"))
            workbook_rels = ET.fromstring(package.read("xl/_rels/workbook.xml.rels"))
            targets = {item.get("Id"): item.get("Target") for item in workbook_rels}
            sheets: dict[str, tuple[str, ET.Element, dict[str, str], dict[str, str]]] = {}
            sheet_nodes = workbook.find(ns + "sheets")
            require(sheet_nodes is not None, "XLSX workbook lacks sheets", failures)
            for node in list(sheet_nodes) if sheet_nodes is not None else []:
                sheet_name = node.get("name", "")
                require(node.get("state", "visible") == "visible",
                        f"XLSX sheet must not be hidden: {sheet_name}", failures)
                target = str(targets.get(node.get(office_rel), "")).lstrip("/")
                if not target.startswith("xl/"):
                    target = posixpath.normpath(posixpath.join("xl", target))
                require(target in names, f"XLSX missing sheet part for {sheet_name}", failures)
                if target in names:
                    root = ET.fromstring(package.read(target))
                    values, formulas = xlsx_cells(root, shared)
                    sheets[sheet_name] = (target, root, values, formulas)
            require(set(sheets) == {"Summary", "Decision families", "Status legend"},
                    f"XLSX sheet topology drift: {sorted(sheets)}", failures)
            if "Decision families" not in sheets:
                return
            _, _, detail_values, detail_formulas = sheets["Decision families"]
            headers = [detail_values.get(f"{chr(65 + index)}3", "") for index in range(24)]
            require(headers == EXPECTED_XLSX_HEADERS,
                    f"XLSX decision-family headers drift: {headers}", failures)
            labels = data.get("status_labels", {})
            for offset, row in enumerate(rows, start=4):
                row_id = row.get("id")
                expected = [
                    row.get("sort_date"), str(row.get("same_date_sequence")), row.get("period"),
                    row_id, row.get("family_es"), row.get("family_en"),
                    row.get("proceeding_es", row.get("proceeding")),
                    row.get("proceeding_en", row.get("proceeding")), row.get("coverage_state"),
                    labels.get(row.get("coverage_state"), {}).get("es", ""),
                    labels.get(row.get("coverage_state"), {}).get("en", ""),
                    row.get("classification"),
                    CLASSIFICATION_LABELS.get(row.get("classification"), ("", ""))[0],
                    CLASSIFICATION_LABELS.get(row.get("classification"), ("", ""))[1],
                    row.get("row_type"), row.get("date_status"),
                    "; ".join(row.get("canonical_record_ids", [])), row.get("priority"),
                    row.get("copy_control_status", ""), row.get("public_access_status"),
                    row.get("gap_es"), row.get("gap_en"),
                ]
                for column_index, value in enumerate(expected, start=1):
                    column = "" if column_index < 1 else chr(64 + column_index)
                    require(detail_values.get(f"{column}{offset}", "") == str(value or ""),
                            f"XLSX/JSON parity failure {row_id} column {column}", failures)
                for column in "ABCDEFGHIJKLMNOPQRSTUV":
                    require(f"{column}{offset}" not in detail_formulas,
                            f"XLSX decision data must not be formula-derived: {column}{offset}", failures)
                for column, language in (("W", "es"), ("X", "en")):
                    formula = detail_formulas.get(f"{column}{offset}", "")
                    expected_url = public_url(row, language)
                    value = detail_values.get(f"{column}{offset}", "")
                    require((formula.startswith("HYPERLINK(") and expected_url in formula)
                            or (not formula and value == expected_url),
                            f"XLSX public {language} link mismatch for {row_id}", failures)
            require(not any(re.match(r"[A-X](?:5[5-9]|[6-9]\d|\d{3,})$", ref)
                            and value for ref, value in detail_values.items()),
                    "XLSX decision sheet contains data below row 54", failures)

            if "Summary" in sheets:
                _, _, summary_values, summary_formulas = sheets["Summary"]
                summary_expected = [51, 28, 4, 2, 2, 15, 51]
                for row_number, expected in zip(range(5, 12), summary_expected):
                    require(summary_values.get(f"B{row_number}") == str(expected)
                            and summary_values.get(f"C{row_number}") == str(expected)
                            and summary_values.get(f"D{row_number}") == "0",
                            f"XLSX summary count/variance mismatch at row {row_number}", failures)
                require("'Decision families'!$L$4:$L$54" in summary_formulas.get("B6", "")
                        and "'Decision families'!$L$4:$L$54" in summary_formulas.get("B10", "")
                        and summary_formulas.get("B11") == "SUM(B6:B10)",
                        "XLSX summary formulas do not cover the exact classification partition", failures)
                require(summary_values.get("F5") == EXPECTED_RESULT_STATUS,
                        "XLSX controlling conclusion drift", failures)
            if "Status legend" in sheets:
                _, _, legend_values, legend_formulas = sheets["Status legend"]
                status_order = list(data.get("status_labels", {}))
                for row_number, state in enumerate(status_order, start=4):
                    pair = data.get("status_labels", {}).get(state, {})
                    require(legend_values.get(f"A{row_number}") == state
                            and legend_values.get(f"B{row_number}") == pair.get("es")
                            and legend_values.get(f"C{row_number}") == pair.get("en")
                            and legend_values.get(f"D{row_number}") == str(EXPECTED_STATE_COUNTS.get(state, 0)),
                            f"XLSX status legend mismatch for {state}", failures)
                    require("'Decision families'!$I$4:$I$54" in legend_formulas.get(f"D{row_number}", ""),
                            f"XLSX status count formula mismatch for {state}", failures)
                for row_number, (classification, expected_count) in enumerate(
                    EXPECTED_CLASSIFICATIONS.items(), start=17
                ):
                    labels_pair = CLASSIFICATION_LABELS[classification]
                    require(legend_values.get(f"A{row_number}") == classification
                            and legend_values.get(f"B{row_number}") == labels_pair[0]
                            and legend_values.get(f"C{row_number}") == labels_pair[1]
                            and legend_values.get(f"D{row_number}") == str(expected_count)
                            and legend_values.get(f"E{row_number}") == str(expected_count),
                            f"XLSX classification legend mismatch for {classification}", failures)

            table_expectations = {
                "DecisionContinuitySummaryTable": "A4:D11",
                "DecisionContinuityTable": "A3:X54",
                "DecisionStatusLegendTable": "A3:G12",
                "DecisionClassificationLegendTable": "A16:E21",
            }
            actual_tables: dict[str, str] = {}
            for name in names:
                if name.startswith("xl/tables/") and name.endswith(".xml"):
                    table = ET.fromstring(package.read(name))
                    actual_tables[str(table.get("displayName"))] = str(table.get("ref"))
            require(actual_tables == table_expectations,
                    f"XLSX table topology/ranges drift: {actual_tables}", failures)

            visible_text = "\n".join(shared)
            for sheet_name, (_, _, values, formulas) in sheets.items():
                visible_text += "\n" + "\n".join(values.values()) + "\n" + "\n".join(formulas.values())
                check_privacy(f"{relative(XLSX)}:{sheet_name}", visible_text, failures)
            xml_text = "\n".join(
                package.read(name).decode("utf-8", "ignore")
                for name in names if name.endswith((".xml", ".rels"))
            )
            check_privacy(f"{relative(XLSX)} OOXML", xml_text, failures)
    except (zipfile.BadZipFile, ET.ParseError, KeyError) as exc:
        failures.append(f"XLSX structural validation failed: {exc}")


def check_document_artifacts(failures: list[str]) -> None:
    if not DOCX.is_file():
        failures.append(f"missing required file: {relative(DOCX)}")
    else:
        try:
            with zipfile.ZipFile(DOCX) as package:
                require(package.testzip() is None, "DOCX ZIP CRC check failed", failures)
                names = package.namelist()
                require("word/document.xml" in names, "DOCX lacks word/document.xml", failures)
                for name in names:
                    lower = name.lower()
                    require(not any(marker in lower for marker in (
                        "vbaproject", "embeddings", "activex", "comments", "people.xml"
                    )), f"DOCX contains forbidden active/private part: {name}", failures)
                    if name.endswith(".rels"):
                        root = ET.fromstring(package.read(name))
                        rel_ns = "{http://schemas.openxmlformats.org/package/2006/relationships}"
                        for relationship in root.findall(rel_ns + "Relationship"):
                            if relationship.get("TargetMode") == "External":
                                target = relationship.get("Target", "")
                                require(str(target).startswith(BASE_URL),
                                        f"DOCX contains non-public external relationship: {target}", failures)
                text = "\n".join(package.read(name).decode("utf-8", "ignore")
                                 for name in names if name.endswith((".xml", ".rels")))
                check_privacy(relative(DOCX), text, failures)
                require("51" in text and "28" in text,
                        "DOCX does not preserve release counts", failures)
        except (zipfile.BadZipFile, ET.ParseError) as exc:
            failures.append(f"DOCX structural validation failed: {exc}")
    if not PDF.is_file():
        failures.append(f"missing required file: {relative(PDF)}")
    else:
        raw = PDF.read_bytes()
        require(raw.startswith(b"%PDF-") and raw.rstrip().endswith(b"%%EOF"),
                "PDF signature or EOF marker is invalid", failures)
        require(len(re.findall(rb"/Type\s*/Page\b", raw)) >= 1,
                "PDF contains no page objects", failures)
        check_privacy(relative(PDF), raw.decode("latin-1", "ignore"), failures)


def check_manifest_and_closeout(data: dict[str, Any], failures: list[str]) -> None:
    manifest = load_json(MANIFEST, failures)
    state = manifest.get("current_state")
    require(manifest.get("schema") == "por-derecho.publication-manifest.v1",
            "publication manifest schema drift", failures)
    require(manifest.get("publication_id") == "concurso36-court-decision-continuity-20260828",
            "publication manifest ID drift", failures)
    require(state in LIFECYCLE, f"unsupported publication lifecycle state: {state!r}", failures)
    require(manifest.get("expected_routes") == {
        "es": ["es/concurso-36-2012-autos-resoluciones/index.html"],
        "en": ["en/insolvency-36-2012-orders-decisions/index.html"],
    }, "manifest route set drift", failures)
    require(manifest.get("expected_anchors") == {
        "es": "continuidad-2014-2026", "en": "continuity-2014-2026"
    }, "manifest anchor set drift", failures)
    source_files = manifest.get("expected_source_files", [])
    require(isinstance(source_files, list) and len(source_files) == len(set(source_files)),
            "manifest expected_source_files must be a unique array", failures)
    if isinstance(source_files, list):
        missing = REQUIRED_MANIFEST_SOURCES - set(source_files)
        require(not missing, f"manifest omits release/source files: {sorted(missing)}", failures)
        for item in source_files:
            require(isinstance(item, str) and (ROOT / item).exists(),
                    f"manifest expected source is missing: {item!r}", failures)
    controlled = manifest.get("controlled_result", {})
    require(isinstance(controlled, dict), "manifest controlled_result must be an object", failures)
    if isinstance(controlled, dict):
        require(controlled.get("status") == EXPECTED_RESULT_STATUS,
                "manifest controlled result status drift", failures)
        for key, expected in EXPECTED_RESULT.items():
            require(controlled.get(key) == expected,
                    f"manifest controlled_result {key} must be {expected}, got {controlled.get(key)!r}",
                    failures)
        require(controlled.get("certified_docket_obtained") is False
                and controlled.get("official_denominator") is None,
                "manifest must preserve the uncertified/null denominator", failures)
        require("official_notification_families_located" not in controlled,
                "manifest retains superseded notification-family partition field", failures)
    privacy = manifest.get("privacy_controls", {})
    for key in (
        "private_email_or_drive_locators_published", "exact_private_filenames_published",
        "unredacted_source_copies_published", "verification_codes_or_personal_contact_data_published",
    ):
        require(isinstance(privacy, dict) and privacy.get(key) is False,
                f"manifest privacy control must remain false: {key}", failures)
    require(isinstance(privacy, dict) and privacy.get("public_safe_stable_ids_only") is True,
            "manifest must assert public-safe stable IDs only", failures)
    boundaries = "\n".join(str(value) for value in manifest.get("evidential_boundaries", []))
    for marker in (
        "closes only the decision-copy node", "Same-date decisions remain distinct",
        "separate civil lane", "unconfirmed", "do not determine", "does not mean nonexistent",
    ):
        require(marker.lower() in boundaries.lower(),
                f"manifest evidential boundaries omit: {marker}", failures)
    authority = manifest.get("authority", {})
    require(isinstance(authority, dict), "manifest authority must be an object", failures)
    if isinstance(authority, dict):
        require(authority.get("email") is False and authority.get("filing") is False
                and authority.get("authority_contact") is False,
                "manifest must not authorise email, filing or third-party contact", failures)
    validation = manifest.get("validation", {})
    require(isinstance(validation, dict), "manifest validation must be an object", failures)
    evidence = validation.get("evidence", []) if isinstance(validation, dict) else []

    prepared_states = {"PREPARED_PENDING_MERGE", "REMOTE_SOURCE", "PR_OPEN", "CI_GREEN",
                       "MERGED", "DEPLOYED", "LIVE_VERIFIED", "DELETION_SAFE"}
    if state in prepared_states:
        require(bool(re.fullmatch(r"[0-9a-f]{40}", str(manifest.get("base_sha_at_start", "")))),
                f"{state} requires a 40-character base SHA", failures)
        require(isinstance(manifest.get("branch"), str) and manifest.get("branch") not in {"", "main"},
                f"{state} requires a non-main candidate branch", failures)
        require(isinstance(validation, dict)
                and validation.get("status") in {"PASSED_LOCAL_VALIDATION", "CI_GREEN"}
                and isinstance(evidence, list) and len(evidence) >= 3,
                f"{state} requires recorded local validation evidence", failures)
        evidence_text = json.dumps(evidence)
        for script in (
            "validate_concurso36_decision_continuity.py",
            "validate_concurso36_primary_autos_redigest.py",
            "validate_concurso36_complete_record.py",
        ):
            require(script in evidence_text, f"manifest validation evidence omits {script}", failures)
    if state in {"DRAFT", "PREPARED_PENDING_MERGE"}:
        require(manifest.get("merge_sha") is None and manifest.get("deployment_evidence") is None
                and manifest.get("live_verification_evidence") is None
                and manifest.get("live_urls") == [],
                f"{state} must not claim merge, deployment or live evidence", failures)
        if isinstance(authority, dict):
            for key in ("push", "pull_request", "merge", "deploy"):
                require(authority.get(key) is False,
                        f"{state} authority must leave {key} false", failures)
    if state in {"REMOTE_SOURCE", "PR_OPEN", "CI_GREEN", "MERGED", "DEPLOYED",
                 "LIVE_VERIFIED", "DELETION_SAFE"}:
        require(bool(re.fullmatch(r"[0-9a-f]{40}", str(manifest.get("remote_source_sha", "")))),
                f"{state} requires remote_source_sha", failures)
    if state in {"PR_OPEN", "CI_GREEN", "MERGED", "DEPLOYED", "LIVE_VERIFIED", "DELETION_SAFE"}:
        require(bool(manifest.get("pull_request")), f"{state} requires pull-request evidence", failures)
    if state in {"CI_GREEN", "MERGED", "DEPLOYED", "LIVE_VERIFIED", "DELETION_SAFE"}:
        require(bool(manifest.get("ci_evidence")), f"{state} requires successful CI evidence", failures)
    if state in {"MERGED", "DEPLOYED", "LIVE_VERIFIED", "DELETION_SAFE"}:
        require(bool(re.fullmatch(r"[0-9a-f]{40}", str(manifest.get("merge_sha", "")))),
                f"{state} requires merge_sha", failures)
    if state in {"DEPLOYED", "LIVE_VERIFIED", "DELETION_SAFE"}:
        require(bool(manifest.get("deployment_evidence")),
                f"{state} requires deployment evidence", failures)
    if state in {"LIVE_VERIFIED", "DELETION_SAFE"}:
        require(set(manifest.get("live_urls", [])) == {ES_URL, EN_URL}
                and bool(manifest.get("live_verification_evidence")),
                f"{state} requires bilingual live readback evidence", failures)
    if state == "DELETION_SAFE":
        require(bool(manifest.get("deletion_record")),
                "DELETION_SAFE requires an explicit deletion record", failures)
    if state == "BLOCKED_RECOVERY":
        require(bool(manifest.get("recovery_blocker")) and bool(manifest.get("recovery_evidence")),
                "BLOCKED_RECOVERY requires blocker and recovery evidence", failures)

    closeout = read_text(CLOSEOUT, failures)
    for marker in ("51-row chronology", "28 core primary decisions", "four earlier in-case anchors",
                   "two connected/contextual", "two selected court-office", "Fifteen rows remain"):
        require(marker.lower() in closeout.lower(), f"closeout omits release result: {marker}", failures)
    require("No push, pull request, merge, Pages deployment or live readback is claimed" in closeout,
            "prepared closeout must disclaim remote publication actions", failures)
    require("Email, filing, portal submission and authority contact are not authorised" in closeout,
            "closeout must preserve the no-email/no-filing boundary", failures)
    if state != "DELETION_SAFE":
        require("NOT SAFE TO DELETE" in closeout,
                "closeout must not claim deletion safety before live verification", failures)
    else:
        require("SAFE TO DELETE" in closeout and "NOT SAFE TO DELETE" not in closeout,
                "DELETION_SAFE closeout verdict mismatch", failures)
    check_privacy(relative(MANIFEST), read_text(MANIFEST, failures), failures)
    check_privacy(relative(CLOSEOUT), closeout, failures)


def check_reports_and_sitemaps(data: dict[str, Any], failures: list[str]) -> None:
    audit_text = read_text(AUDIT, failures)
    for marker in (
        "51", "28", "four", "two", "15", "36/2012^",
        "No envíe correo", "Do not send email", "No certified chronological docket",
    ):
        require(marker.lower() in audit_text.lower(), f"audit report missing marker: {marker}", failures)
    for path in ADDENDA:
        text = read_text(path, failures)
        require(bool(text.strip()), f"empty continuity addendum: {relative(path)}", failures)
        check_privacy(relative(path), text, failures)
    check_privacy(relative(AUDIT), audit_text, failures)

    refined = data.get("audit_prompt", {})
    if isinstance(refined, dict):
        def prompt_normal_form(value: str) -> str:
            without_quotes = re.sub(r"[\"'“”‘’]", "", value)
            return re.sub(r"\s+", " ", without_quotes).strip()

        normal_audit = prompt_normal_form(audit_text)
        require(prompt_normal_form(str(refined.get("es", ""))) in normal_audit
                and prompt_normal_form(str(refined.get("en", ""))) in normal_audit,
                "audit report and machine-readable refined prompt diverge", failures)

    ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    for path in (MAIN_SITEMAP, COURT_SITEMAP):
        try:
            root = ET.fromstring(read_text(path, failures))
        except ET.ParseError as exc:
            failures.append(f"invalid sitemap XML in {relative(path)}: {exc}")
            continue
        entries: dict[str, str] = {}
        for url in root.findall(ns + "url"):
            loc = url.findtext(ns + "loc", default="")
            lastmod = url.findtext(ns + "lastmod", default="")
            entries[loc] = lastmod
        for url in (ES_URL, EN_URL):
            require(entries.get(url) == "2026-08-28",
                    f"{relative(path)} missing {url} with 2026-08-28 lastmod", failures)


def main() -> int:
    failures: list[str] = []
    data = load_json(DATA, failures)
    catalogue = load_json(CATALOGUE, failures)
    court_file = load_json(COURT_FILE, failures)
    autos = load_json(AUTOS, failures)
    caret_digest = load_json(CARET_DIGEST, failures)
    rows = check_rows(data, catalogue, court_file, autos, caret_digest, failures)
    if rows:
        check_pages(rows, data, failures)
        check_xlsx(rows, data, failures)
    check_document_artifacts(failures)
    check_manifest_and_closeout(data, failures)
    check_reports_and_sitemaps(data, failures)

    for label, path in (
        (relative(DATA), DATA), (relative(AUDIT), AUDIT),
        *( (relative(item), item) for item in ADDENDA ),
    ):
        if path.is_file():
            check_privacy(label, path.read_text(encoding="utf-8"), failures)

    unique_failures = list(dict.fromkeys(failures))
    if unique_failures:
        print("Concurso 36/2012 decision-continuity validation FAILED:", file=sys.stderr)
        for failure in unique_failures:
            print(f" - {failure}", file=sys.stderr)
        return 1
    print(
        "Concurso 36/2012 decision continuity validated: "
        "51 = 28 core + 4 earlier + 2 contextual + 2 court-office + 15 open; "
        "canonical dates/copies, same-date pairs, bilingual pages, XLSX, privacy and lifecycle OK."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
