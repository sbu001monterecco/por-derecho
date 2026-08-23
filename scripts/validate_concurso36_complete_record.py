#!/usr/bin/env python3
"""Validate the denominator-aware Concurso 36/2012 whole-record release.

The gate is intentionally strict about the final 23 August 2026 catalogue and
intentionally modest about what that catalogue means.  It proves internal
consistency, public-source integrity and discovery wiring; it never certifies
that the court file is complete.

Only Python's standard library is used so the check can run in an isolated
GitHub Actions job without installing document or HTML packages.
"""

from __future__ import annotations

import hashlib
import json
import pathlib
import re
import subprocess
import sys
import urllib.parse
import xml.etree.ElementTree as ET
from collections import Counter
from html.parser import HTMLParser
from typing import Any, Iterable


ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE_URL = "https://sbu001monterecco.github.io/por-derecho"

CATALOGUE = ROOT / "assets/data/concurso36-complete-record-v1.json"
ROUTE_REGISTRY = ROOT / "assets/data/unitary-route-registry-v1.json"
DIGEST = ROOT / "archive/CONCURSO36_COMPLETE_RECORD_EXECUTION_DIGEST_23AUG2026.md"
COMMUNICATIONS = ROOT / "archive/JUDGE_LAJ_COMMUNICATIONS_REGISTER_CONCURSO36.md"
PROMPT = ROOT / "archive/prompts/CONCURSO36_COMPLETE_JUDICIAL_PARTY_RECORD_ACQUISITION_DIGITISATION_PUBLICATION_PROMPT_23AUG2026.md"
PUBLICATION_MANIFEST = ROOT / "publication-manifests/concurso36-complete-record-20260823.json"
PRIMARY_AUTOS_ARCHIVE = ROOT / "archive/concurso36-primary-autos-21aug2026"
IMPLEMENTATION_REGISTER = ROOT / "archive/CONCURSO36_JUDICIAL_ACTS_IMPLEMENTATION_REGISTER_21AUG2026.md"

SECURITY_DIR = ROOT / "evidence/sun-park/2018-02-27-ac-security-request"
SECURITY_MANIFEST = SECURITY_DIR / "manifest.json"
SECURITY_README = SECURITY_DIR / "README.md"
SECURITY_REDACTION_LOG = SECURITY_DIR / "redaction-log.md"
SECURITY_CONTROL = ROOT / "archive/SUN_PARK_27FEB2018_AC_SECURITY_REQUEST_PUBLICATION_CONTROL_21AUG2026.md"
SECURITY_TRANSCRIPT_ES = SECURITY_DIR / "transcript.es.md"
SECURITY_TRANSCRIPT_EN = SECURITY_DIR / "transcript.en.md"
SECURITY_PDF = SECURITY_DIR / "public/2018-02-27-ac-community-security-request-redacted-searchable.pdf"
SECURITY_SHA256SUMS = SECURITY_DIR / "SHA256SUMS.txt"

EXPECTED_SECURITY_PDF_SHA256 = (
    "129cfdd2b74fe7f5e35b0db7890878aa10c5b81e6d4d6c9d3eaf0845eb820607"
)
EXPECTED_RESTRICTED_SOURCE_SHA256 = (
    "497ecb49495badbcee155397fe70d37d090c36c4e7998308172e7a612046dbed"
)

RESULT_LABELS = {
    "inventory_status": "INVENTORY PARTIAL — CERTIFIED DOCKET OR RECORDS STILL MISSING",
    "publication_status": "PUBLICATION COMPLETE FOR THE IDENTIFIED PUBLIC-SAFE CORPUS — NOT THE WHOLE COURT FILE",
}

EXPECTED_COUNTS = {
    "canonical_records": 127,
    "historical_forensic_records": 72,
    "historical_complete_copies": 49,
    "historical_missing_complete_copies": 21,
    "historical_copy_status_uncertain": 2,
    "specialist_records": 50,
    "specialist_public_full_text_transcripts": 50,
    "specialist_public_pdfs": 10,
    "supplemental_canonical_records": 5,
    "supplemental_source_copy_entries": 8,
    "supplemental_public_pdfs": 1,
    "supplemental_page_complete_transcripts": 0,
    "public_safe_pdfs_total": 11,
    "public_page_complete_source_transcripts_total": 50,
}

EXPECTED_CLASS_COUNTS = {
    "implementation_or_notarial_record": 2,
    "judicial_act": 40,
    "judicial_or_laj_type_unresolved": 1,
    "laj_or_court_office_act": 39,
    "other_evidential_record": 2,
    "party_communication": 2,
    "party_filing": 34,
    "photographic_derivative": 1,
    "registry_record": 4,
    "report_inventory_or_certificate": 2,
}

EXPECTED_HISTORICAL_CLASS_COUNTS = {
    "implementation_or_notarial_record": 2,
    "judicial_act": 34,
    "judicial_or_laj_type_unresolved": 1,
    "laj_or_court_office_act": 20,
    "other_evidential_record": 2,
    "party_filing": 7,
    "registry_record": 4,
    "report_inventory_or_certificate": 2,
}

SPECIALIST_ROUTES = (
    "es/concurso-36-2012-autos-resoluciones/",
    "en/insolvency-36-2012-orders-decisions/",
)
CRITICAL_READER_ROUTES = (
    "es/concurso-36-2012-que-ordeno-el-juzgado/",
    "en/concurso-36-2012-what-the-court-ordered/",
)
SECURITY_ROUTES = (
    "es/solicitud-seguridad-administracion-concursal-sun-park-27-febrero-2018/",
    "en/insolvency-administrator-security-request-sun-park-27-february-2018/",
)
ADJUDICATION_ROUTES = (
    "es/adjudicacion-2022-reconstruccion-documental/",
    "en/2022-adjudication-documentary-reconstruction/",
)
REQUIRED_ROUTES = (
    *SPECIALIST_ROUTES,
    *CRITICAL_READER_ROUTES,
    *SECURITY_ROUTES,
    *ADJUDICATION_ROUTES,
)

FORBIDDEN_PUBLIC_LOCATOR_PATTERNS = (
    re.compile(r"https://(?:drive|docs|mail)\.google\.com[^\s\"'<>]+", re.IGNORECASE),
    re.compile(r"\bA05003250-[A-Za-z0-9-]+\b", re.IGNORECASE),
    re.compile(r"\b(?:Drive|Native Drive document)\s+[A-Za-z0-9_-]{20,}\b"),
    re.compile(
        r"\bCSV[ \t:#-]+(?=[A-Z0-9-]*\d)[A-Z0-9-]{8,}\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:secure[- ]verification code|c[oó]digo (?:seguro )?de verificaci[oó]n)"
        r"[ \t:#-]+(?=[A-Z0-9-]*\d)[A-Z0-9-]{8,}\b",
        re.IGNORECASE,
    ),
)

RELEASE_PRIVACY_TEXT_SUFFIXES = {
    ".csv", ".html", ".js", ".json", ".jsonl", ".md", ".mjs",
    ".py", ".rst", ".txt", ".xml", ".yml", ".yaml",
}

MANIFEST_ROUTES = {
    "es": {
        "es/concurso-36-2012-autos-resoluciones/index.html",
        "es/concurso-36-2012-que-ordeno-el-juzgado/index.html",
        "es/concurso-36-2012-columna-judicial/index.html",
        "es/solicitud-seguridad-administracion-concursal-sun-park-27-febrero-2018/index.html",
        "es/concurso-36-2012-separacion-ac-honorarios/index.html",
        "es/acreedor-de-registro/credito-litigioso-escritura/index.html",
        "es/reconstruccion-unitaria-autoridades-publicas/index.html",
        "es/ric-private-equity-sun-park/index.html",
        "es/adjudicacion-2022-reconstruccion-documental/index.html",
    },
    "en": {
        "en/insolvency-36-2012-orders-decisions/index.html",
        "en/concurso-36-2012-what-the-court-ordered/index.html",
        "en/concurso-36-2012-judicial-spine/index.html",
        "en/insolvency-administrator-security-request-sun-park-27-february-2018/index.html",
        "en/insolvency-36-2012-administrator-removal-fees/index.html",
        "en/lender-of-record/litigious-credit-hidden-deed/index.html",
        "en/public-authority-unitary-case-reconstruction/index.html",
        "en/ric-private-equity-sun-park/index.html",
        "en/2022-adjudication-documentary-reconstruction/index.html",
    },
}

ESSENTIAL_MANIFEST_SOURCES = {
    "assets/data/concurso36-complete-record-v1.json",
    "assets/data/concurso36-autos-fulltext-v1.json",
    "assets/data/concurso36-what-court-ordered-v1.json",
    "assets/data/concurso36-judicial-spine-v1.json",
    "assets/data/concurso36-judicial-acts-v1.json",
    "assets/data/unitary-route-registry-v1.json",
    "archive/CONCURSO36_COMPLETE_RECORD_EXECUTION_DIGEST_23AUG2026.md",
    "archive/JUDGE_LAJ_COMMUNICATIONS_REGISTER_CONCURSO36.md",
    "archive/SUN_PARK_27FEB2018_AC_SECURITY_REQUEST_PUBLICATION_CONTROL_21AUG2026.md",
    "archive/SUN_PARK_ACTIVE_ESTATE_2018_2021_EIGHT_SOURCE_SUPPLEMENT_23AUG2026.md",
    "archive/CONCURSO36_JUDICIAL_ACTS_IMPLEMENTATION_REGISTER_21AUG2026.md",
    "archive/prompts/CONCURSO36_COMPLETE_JUDICIAL_PARTY_RECORD_ACQUISITION_DIGITISATION_PUBLICATION_PROMPT_23AUG2026.md",
    "archive/CONCURSO_36_2012_PRIMARY_AUTOS_REDIGEST_HANDOVER_21AUG2026.md",
    "archive/concurso36-primary-autos-21aug2026/README.md",
    "archive/concurso36-primary-autos-21aug2026/PUBLIC_DERIVATIVE_SHA256SUMS.txt",
    "archive/concurso36-primary-autos-21aug2026/FORENSIC_EVIDENCE_INDEX_CONCURSO_36_2012_21AUG2026.csv",
    "archive/concurso36-primary-autos-21aug2026/FORENSIC_SCAN_CRITICAL_AUTOS_CONCURSO_36_2012_21AUG2026.md",
    "archive/concurso36-primary-autos-21aug2026/GAP_CLOSURE_REGISTER_CONCURSO_36_2012_21AUG2026.csv",
    "archive/concurso36-primary-autos-21aug2026/GAP_CLOSURE_REGISTER_CONCURSO_36_2012_21AUG2026.xlsx",
    "archive/concurso36-primary-autos-21aug2026/REVERSE_ENGINEERING_FORENSIC_PROMPT_V2_CONCURSO_36_2012_21AUG2026.md",
    "archive/concurso36-primary-autos-21aug2026/REVERSE_ENGINEERING_REDIGEST_CONCURSO_36_2012_21AUG2026.md",
    "archive/concurso36-primary-autos-21aug2026/artifact_closure_audit.md",
    "archive/concurso36-primary-autos-21aug2026/connected_gap_scan.md",
    "archive/concurso36-primary-autos-21aug2026/repo_site_reverse_engineering.md",
    "evidence/sun-park/2018-02-27-ac-security-request/README.md",
    "evidence/sun-park/2018-02-27-ac-security-request/SHA256SUMS.txt",
    "evidence/sun-park/2018-02-27-ac-security-request/manifest.json",
    "evidence/sun-park/2018-02-27-ac-security-request/transcript.es.md",
    "evidence/sun-park/2018-02-27-ac-security-request/transcript.en.md",
    "evidence/sun-park/2018-02-27-ac-security-request/public/2018-02-27-ac-community-security-request-redacted-searchable.pdf",
    "scripts/build_concurso36_complete_record.py",
    "scripts/validate_concurso36_complete_record.py",
    ".github/workflows/validate-concurso36-complete-record.yml",
    "tools/build_ac_security_request_public_pdf.py",
    "sitemap.xml",
    "sitemap-unitary-shell.xml",
    "sitemap-concurso36-court-orders.xml",
    "sitemap-adjudicacion-2022.xml",
    "robots.txt",
}

MAIN_SITEMAP = ROOT / "sitemap.xml"
UNITARY_SITEMAP = ROOT / "sitemap-unitary-shell.xml"
SPECIALIST_SITEMAP = ROOT / "sitemap-concurso36-court-orders.xml"
ADJUDICATION_SITEMAP = ROOT / "sitemap-adjudicacion-2022.xml"
ROBOTS = ROOT / "robots.txt"

EMAIL_RE = re.compile(
    r"(?i)(?<![\w.+-])[a-z0-9.!#$%&'*+/=?^_`{|}~-]+@"
    r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?"
    r"(?:\.[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?)+"
)


def relative(path: pathlib.Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def read_text(path: pathlib.Path, failures: list[str]) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        failures.append(f"missing required file: {relative(path)}")
    except UnicodeDecodeError as exc:
        failures.append(f"UTF-8 decode failed for {relative(path)}: {exc}")
    return ""


def load_json(path: pathlib.Path, failures: list[str]) -> Any:
    text = read_text(path, failures)
    if not text:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        failures.append(f"invalid JSON in {relative(path)}: {exc}")
        return None


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def require_markers(
    path: pathlib.Path,
    text: str,
    markers: Iterable[str],
    failures: list[str],
) -> None:
    for marker in markers:
        if marker not in text:
            failures.append(f"{relative(path)} missing marker: {marker!r}")


def sha256(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def recursive_strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        strings: list[str] = []
        for item in value.values():
            strings.extend(recursive_strings(item))
        return strings
    if isinstance(value, list):
        strings = []
        for item in value:
            strings.extend(recursive_strings(item))
        return strings
    return []


def check_catalogue(failures: list[str]) -> None:
    payload = load_json(CATALOGUE, failures)
    if not isinstance(payload, dict):
        return

    require(payload.get("schema") == "concurso36-complete-record-v1",
            "whole-record catalogue has unexpected schema", failures)
    case = payload.get("case")
    require(isinstance(case, dict), "catalogue case object missing", failures)
    if isinstance(case, dict):
        require(case.get("proceeding") == "Concurso ordinario 36/2012",
                "catalogue proceeding identity changed", failures)
        require(case.get("nig") == "3501647120120000351",
                "catalogue NIG changed", failures)

    result = payload.get("result")
    require(isinstance(result, dict), "catalogue result object missing", failures)
    if isinstance(result, dict):
        for key, expected in RESULT_LABELS.items():
            require(result.get(key) == expected,
                    f"catalogue result.{key} must equal {expected!r}", failures)
        require(result.get("certified_docket_obtained") is False,
                "catalogue must keep certified_docket_obtained=false", failures)
        require(result.get("official_denominator") is None,
                "catalogue must keep official_denominator=null", failures)
        require(result.get("complete_or_all_uploaded_claim_permitted") is False,
                "catalogue must prohibit complete/all-uploaded claims", failures)
        require(result.get("discovery_lower_bound_act_families_2012_2023") == 95,
                "catalogue discovery lower bound must remain 95", failures)
        require(result.get("historical_workbook_rows_reported") == "600+ including filings, copies and duplicates",
                "catalogue historical-workbook lower-bound label changed", failures)

    coverage = payload.get("current_run_source_coverage")
    require(isinstance(coverage, dict), "catalogue connector/source coverage object missing", failures)
    if isinstance(coverage, dict):
        for key in ("repository_and_history", "live_website", "local_supplied_files", "gmail", "google_drive", "library_files", "interpretation"):
            require(bool(coverage.get(key)), f"catalogue source-coverage field {key} missing", failures)
        interpretation = str(coverage.get("interpretation", "")).lower()
        require("access-coverage limitation" in interpretation and "not evidence of non-existence or deletion" in interpretation,
                "connector-null interpretation must remain an access limit, not an absence finding", failures)

    counts = payload.get("counts")
    require(isinstance(counts, dict), "catalogue counts object missing", failures)
    if isinstance(counts, dict):
        for key, expected in EXPECTED_COUNTS.items():
            require(counts.get(key) == expected,
                    f"catalogue counts.{key}: expected {expected}, got {counts.get(key)!r}", failures)
        require(counts.get("record_classes") == EXPECTED_CLASS_COUNTS,
                "catalogue record-class counts do not match the 127-record contract", failures)

    records = payload.get("records")
    require(isinstance(records, list), "catalogue records array missing", failures)
    if not isinstance(records, list):
        return
    require(len(records) == 127,
            f"catalogue must contain 127 records, found {len(records)}", failures)

    ids = [record.get("canonical_id") for record in records if isinstance(record, dict)]
    require(len(ids) == len(records), "one or more catalogue records are not objects", failures)
    require(all(isinstance(item, str) and item for item in ids),
            "every catalogue record needs a non-empty canonical_id", failures)
    require(len(ids) == len(set(ids)), "duplicate canonical IDs in whole-record catalogue", failures)

    catalogue_text = json.dumps(payload, ensure_ascii=False)
    for pattern in FORBIDDEN_PUBLIC_LOCATOR_PATTERNS:
        require(pattern.search(catalogue_text) is None,
                "whole-record catalogue exposes a restricted provider locator or court verification code",
                failures)

    expected_historical = {f"C36-E{number:03d}" for number in range(1, 73)}
    expected_specialist = {
        *(f"C36-SPECIALIST-R{number:02d}" for number in range(1, 33)),
        *(f"C36-SPECIALIST-F{number:02d}" for number in range(1, 19)),
    }
    historical = [record for record in records if record.get("canonical_id") in expected_historical]
    specialist = [record for record in records if record.get("canonical_id") in expected_specialist]
    supplemental = [record for record in records if str(record.get("canonical_id", "")).startswith("C36-SUP-")]
    require({record.get("canonical_id") for record in historical} == expected_historical,
            "historical IDs must be exactly C36-E001 through C36-E072", failures)
    require({record.get("canonical_id") for record in specialist} == expected_specialist,
            "specialist IDs must be exactly R01-R32 and F01-F18", failures)
    require(len(supplemental) == 5,
            f"expected five supplemental canonical records, found {len(supplemental)}", failures)
    require(len(historical) + len(specialist) + len(supplemental) == len(records),
            "catalogue contains records outside the historical/specialist/supplemental partitions", failures)

    historical_copy_counts = Counter(record.get("complete_copy_status") for record in historical)
    require(historical_copy_counts == Counter({"yes": 49, "no": 21, "not independently established": 2}),
            f"historical copy-status counts changed: {dict(historical_copy_counts)!r}", failures)
    historical_class_counts = Counter(record.get("record_class") for record in historical)
    require(dict(sorted(historical_class_counts.items())) == EXPECTED_HISTORICAL_CLASS_COUNTS,
            f"historical record-class counts changed: {dict(sorted(historical_class_counts.items()))!r}", failures)
    class_counts = Counter(record.get("record_class") for record in records)
    require(dict(sorted(class_counts.items())) == EXPECTED_CLASS_COUNTS,
            f"computed record-class counts changed: {dict(sorted(class_counts.items()))!r}", failures)

    specialist_transcripts = sum(
        record.get("public_derivative", {}).get("page_complete_transcript") is True
        for record in specialist
    )
    specialist_pdfs = sum(
        bool(record.get("public_derivative", {}).get("public_pdf"))
        for record in specialist
    )
    require(specialist_transcripts == 50,
            f"expected 50 specialist transcripts, found {specialist_transcripts}", failures)
    require(specialist_pdfs == 10,
            f"expected 10 specialist public PDFs, found {specialist_pdfs}", failures)

    gaps = payload.get("known_gaps")
    require(isinstance(gaps, list) and len(gaps) == 12,
            "catalogue must contain exactly 12 controlled gaps", failures)
    if isinstance(gaps, list):
        require(len({str(item).strip() for item in gaps}) == 12,
                "controlled gaps must be non-empty and unique", failures)

    crosswalk = payload.get("source_copy_crosswalk")
    require(isinstance(crosswalk, list) and len(crosswalk) == 8,
            "source-copy crosswalk must contain exactly eight entries", failures)
    if isinstance(crosswalk, list):
        source_ids = [item.get("source_id") for item in crosswalk if isinstance(item, dict)]
        require(len(source_ids) == 8 and len(set(source_ids)) == 8,
                "source-copy crosswalk source IDs must be eight unique values", failures)
        require(sum(
            isinstance(item, dict)
            and item.get("canonical_record") == "C36-SUP-ACSEC-2018-02-27"
            for item in crosswalk
        ) == 1, "security-request source must have exactly one crosswalk entry", failures)
        known_ids = set(ids)
        for item in crosswalk:
            if isinstance(item, dict):
                require(item.get("canonical_record") in known_ids,
                        f"crosswalk points to unknown canonical record: {item!r}", failures)

    by_id = {
        record.get("canonical_id"): record
        for record in records
        if isinstance(record, dict)
    }
    for judicial_id in ("C36-E003", "C36-E007", "C36-E009", "C36-E012", "C36-E043"):
        require(by_id.get(judicial_id, {}).get("record_class") == "judicial_act",
                f"{judicial_id} must remain judicial despite the LAJ also appearing on the copy", failures)
    for laj_id in ("C36-E013", "C36-E017", "C36-E020", "C36-E037", "C36-E048", "C36-E054"):
        require(by_id.get(laj_id, {}).get("record_class") == "laj_or_court_office_act",
                f"{laj_id} must remain an LAJ/court-office act", failures)
    require(by_id.get("C36-E071", {}).get("record_class") == "judicial_or_laj_type_unresolved",
            "C36-E071 must remain unresolved until the signed Auto-or-Decreto source is recovered", failures)
    creditor = by_id.get("C36-E007")
    require(isinstance(creditor, dict), "C36-E007 missing", failures)
    if isinstance(creditor, dict):
        require(creditor.get("date") == "2018-02-15",
                "C36-E007 must use the current 2018-02-15 control", failures)
        conflict = creditor.get("date_layer_conflict")
        require(isinstance(conflict, dict),
                "C36-E007 must preserve a structured superseded date-layer control", failures)
        if isinstance(conflict, dict):
            require(conflict.get("status") == "SUPERSEDED_RECONSTRUCTION_REQUIRES_PRIMARY_REINSPECTION",
                    "C36-E007 date-layer status changed", failures)
            require(conflict.get("current_control") == "2018-02-15",
                    "C36-E007 date-layer current control changed", failures)
            require(bool(conflict.get("superseded_snapshot")),
                    "C36-E007 must identify the superseded snapshot without adopting it", failures)
            rule = str(conflict.get("rule", "")).lower()
            require("do not repeat" in rule and "primary" in rule,
                    "C36-E007 date-layer rule must prohibit unsupported republication", failures)

    security = by_id.get("C36-SUP-ACSEC-2018-02-27")
    require(isinstance(security, dict),
            "C36-SUP-ACSEC-2018-02-27 missing from final catalogue", failures)
    if isinstance(security, dict):
        require(security.get("date") == "2018-02-27",
                "security-request canonical date must be 2018-02-27", failures)
        require(security.get("record_class") == "party_communication",
                "security request must remain a party communication, not a court act", failures)
        require(str(security.get("complete_copy_status", "")).startswith("yes"),
                "security request must record a complete located copy", failures)
        require(security.get("public_derivative", {}).get("page_complete_transcript") is False,
                "security request transcript must not be labelled page-complete while the corporate footer is omitted", failures)
        security_strings = recursive_strings(security)
        for required_value in (
            "2018-02-27-ac-community-security-request-redacted-searchable.pdf",
            "transcript.es.md",
            "transcript.en.md",
            EXPECTED_SECURITY_PDF_SHA256,
            EXPECTED_RESTRICTED_SOURCE_SHA256,
        ):
            require(any(required_value in item for item in security_strings),
                    f"security canonical record does not point to {required_value}", failures)
        joined = " ".join(security_strings).lower()
        require("request" in joined or "solicitud" in joined,
                "security record must describe a request, not an order", failures)
        require(any(term in joined for term in ("does not", "no establish", "no acredita", "no autoriza")),
                "security record must preserve a limiting proposition", failures)


def check_publication_manifest(failures: list[str]) -> None:
    manifest = load_json(PUBLICATION_MANIFEST, failures)
    if not isinstance(manifest, dict):
        return

    require(manifest.get("publication_id") == "CONCURSO36-COMPLETE-RECORD-20260823",
            "complete-record publication manifest ID changed", failures)
    require(manifest.get("current_state") in {
        "DRAFT", "REMOTE_SOURCE", "PR_OPEN", "CI_GREEN", "MERGED",
        "DEPLOYED", "LIVE_VERIFIED", "DELETION_SAFE",
    }, "complete-record publication manifest has an invalid lifecycle state", failures)

    labels = manifest.get("result_labels")
    require(isinstance(labels, dict), "publication manifest result_labels missing", failures)
    if isinstance(labels, dict):
        require(labels.get("inventory") == RESULT_LABELS["inventory_status"],
                "publication manifest inventory label drifted", failures)
        require(labels.get("publication") == RESULT_LABELS["publication_status"],
                "publication manifest publication label drifted", failures)
        require(labels.get("certified_docket_obtained") is False,
                "publication manifest must keep certified_docket_obtained=false", failures)
        require(labels.get("official_denominator") is None,
                "publication manifest must keep official_denominator=null", failures)
        require(labels.get("complete_court_file_claim_permitted") is False,
                "publication manifest must prohibit a complete-court-file claim", failures)

    controlled_counts = manifest.get("controlled_counts")
    expected_manifest_counts = {
        "canonical_records": 127,
        "historical_forensic_records": 72,
        "specialist_records": 50,
        "supplemental_records": 5,
        "historical_complete_copies": 49,
        "historical_missing_complete_copies": 21,
        "historical_copy_status_uncertain": 2,
        "public_safe_pdfs": 11,
        "public_page_complete_source_transcripts": 50,
        "record_classes": EXPECTED_CLASS_COUNTS,
    }
    require(controlled_counts == expected_manifest_counts,
            "publication manifest controlled counts do not match the canonical catalogue", failures)

    routes = manifest.get("expected_routes")
    require(isinstance(routes, dict), "publication manifest expected_routes missing", failures)
    if isinstance(routes, dict):
        for lang, expected in MANIFEST_ROUTES.items():
            values = routes.get(lang)
            require(isinstance(values, list),
                    f"publication manifest expected_routes.{lang} must be a list", failures)
            if isinstance(values, list):
                require(set(values) == expected and len(values) == len(expected),
                        f"publication manifest {lang} route inventory is not exact", failures)
                for route in values:
                    require((ROOT / route).is_file(),
                            f"publication manifest route missing from source: {route}", failures)

    sources = manifest.get("expected_source_files")
    require(isinstance(sources, list), "publication manifest expected_source_files missing", failures)
    if isinstance(sources, list):
        require(len(sources) == len(set(sources)),
                "publication manifest contains duplicate source paths", failures)
        require(ESSENTIAL_MANIFEST_SOURCES.issubset(set(sources)),
                "publication manifest omits one or more essential complete-record source controls", failures)
        for source in sources:
            require(isinstance(source, str) and (ROOT / source).is_file(),
                    f"publication manifest source missing from Git tree: {source!r}", failures)

    release_inventory = manifest.get("release_file_inventory")
    require(isinstance(release_inventory, dict),
            "publication manifest exact release-file inventory missing", failures)
    if isinstance(release_inventory, dict):
        release_base = str(release_inventory.get("base_sha", ""))
        release_paths = release_inventory.get("paths")
        require(release_inventory.get("base_sha") == manifest.get("base_sha_at_start"),
                "release-file inventory base SHA does not match the publication base", failures)
        require(isinstance(release_paths, list),
                "release-file inventory paths must be a list", failures)
        if isinstance(release_paths, list):
            require(release_inventory.get("count") == len(release_paths) == 114,
                    "release-file inventory must remain locked to the 114 reviewed paths", failures)
            require(len(release_paths) == len(set(release_paths)),
                    "release-file inventory contains duplicate paths", failures)
            require(release_paths == sorted(release_paths),
                    "release-file inventory paths must remain sorted", failures)
            require(str(PUBLICATION_MANIFEST.relative_to(ROOT)) in release_paths,
                    "release-file inventory must include its own publication manifest", failures)
            for release_path in release_paths:
                target = ROOT / release_path if isinstance(release_path, str) else None
                require(target is not None and target.is_file(),
                        f"release-file inventory path missing from Git tree: {release_path!r}", failures)
                if target is None or not target.is_file() or target.suffix.casefold() not in RELEASE_PRIVACY_TEXT_SUFFIXES:
                    continue
                release_text = read_text(target, failures)
                baseline = subprocess.run(
                    ["git", "show", f"{release_base}:{release_path}"],
                    cwd=ROOT,
                    check=False,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL,
                    text=True,
                )
                baseline_text = baseline.stdout if baseline.returncode == 0 else ""
                for pattern in FORBIDDEN_PUBLIC_LOCATOR_PATTERNS:
                    current_matches = Counter(match.group(0) for match in pattern.finditer(release_text))
                    baseline_matches = Counter(match.group(0) for match in pattern.finditer(baseline_text))
                    new_count = sum(
                        max(0, count - baseline_matches.get(token, 0))
                        for token, count in current_matches.items()
                    )
                    require(
                        new_count == 0,
                        "release-file inventory introduces a restricted provider locator or "
                        f"secure-verification code: {release_path}",
                        failures,
                    )

    nested = manifest.get("nested_artifact_inventories")
    require(isinstance(nested, dict), "publication manifest nested artifact inventories missing", failures)
    if isinstance(nested, dict):
        specialist = nested.get("specialist_corpus")
        require(isinstance(specialist, dict), "specialist nested inventory missing", failures)
        if isinstance(specialist, dict):
            require(specialist.get("manifest") == "assets/data/concurso36-autos-fulltext-v1.json",
                    "specialist nested manifest path changed", failures)
            require((specialist.get("records"), specialist.get("full_text_transcripts"), specialist.get("public_pdfs")) == (50, 50, 10),
                    "specialist nested inventory must remain 50 records / 50 transcripts / 10 PDFs", failures)
        security = nested.get("security_source_package")
        require(isinstance(security, dict), "security nested inventory missing", failures)
        if isinstance(security, dict):
            require(security.get("public_pdf_sha256") == EXPECTED_SECURITY_PDF_SHA256,
                    "security nested inventory PDF hash changed", failures)

    validation = manifest.get("validation")
    require(isinstance(validation, dict), "publication manifest validation object missing", failures)
    if isinstance(validation, dict) and CATALOGUE.is_file():
        require(validation.get("catalog_sha256") == sha256(CATALOGUE),
                "publication manifest catalogue hash does not match the generated JSON", failures)

    email = manifest.get("email_control")
    require(isinstance(email, dict)
            and email.get("email_authorized_by_this_publication") is False
            and email.get("email_sent") is False,
            "publication manifest must preserve the no-email boundary", failures)


def check_security_publication(failures: list[str]) -> None:
    manifest = load_json(SECURITY_MANIFEST, failures)
    if not isinstance(manifest, dict):
        return

    require(manifest.get("evidence_id") == "SP-2018-02-27-AC-SECURITY-REQUEST",
            "security manifest evidence ID changed", failures)
    require(manifest.get("event_date", "").startswith("2018-02-27T"),
            "security manifest event date changed", failures)

    source = manifest.get("source")
    require(isinstance(source, dict), "security manifest source object missing", failures)
    if isinstance(source, dict):
        require(source.get("restricted_source_sha256") == EXPECTED_RESTRICTED_SOURCE_SHA256,
                "restricted security-source hash changed", failures)
        require(source.get("public_repository_contains_unredacted_original") is False,
                "manifest must state that the unredacted original is not public", failures)
        original_name = str(source.get("original_filename", ""))
        if original_name:
            leaked_originals = [
                path for path in ROOT.rglob(original_name)
                if ".git" not in path.parts
            ]
            require(not leaked_originals,
                    "unredacted security source is present in the public worktree: "
                    + ", ".join(relative(path) for path in leaked_originals), failures)

    derivative = manifest.get("public_derivative")
    require(isinstance(derivative, dict),
            "security manifest public_derivative object missing", failures)
    if isinstance(derivative, dict):
        require(derivative.get("path") == "public/2018-02-27-ac-community-security-request-redacted-searchable.pdf",
                "security manifest public PDF path changed", failures)
        require(derivative.get("sha256") == EXPECTED_SECURITY_PDF_SHA256,
                "security manifest public PDF hash changed", failures)
        require(derivative.get("size_bytes") == 88176,
                "security public PDF size must remain 88,176 bytes", failures)
        require(derivative.get("pages") == 1,
                "security public PDF must remain one page", failures)
        require(derivative.get("searchable") is True,
                "security public PDF must remain marked searchable", failures)
        require(str(derivative.get("authoritative_transcript", "")).endswith("transcript.es.md"),
                "security manifest Spanish transcript pointer missing", failures)
        require(str(derivative.get("translation", "")).endswith("transcript.en.md"),
                "security manifest English transcript pointer missing", failures)

    redactions = manifest.get("redactions")
    require(isinstance(redactions, list) and len(redactions) == 3,
            "security manifest must retain exactly three address redactions", failures)
    if isinstance(redactions, list):
        require({item.get("marker") for item in redactions if isinstance(item, dict)} == {"R1", "R2", "R3"},
                "security manifest redaction markers must be R1/R2/R3", failures)

    processing = manifest.get("processing")
    require(isinstance(processing, dict), "security processing controls missing", failures)
    if isinstance(processing, dict):
        for key in (
            "manual_visual_review_of_source",
            "manual_transcript_review",
            "silent_correction_prohibited",
            "deterministic_pdf_generation",
            "pdf_invariant_mode",
        ):
            require(processing.get(key) is True,
                    f"security processing control {key} must remain true", failures)
        for key in (
            "search_layer_sensitive_string_check",
            "pdf_structure_check",
            "visual_render_check",
        ):
            require(processing.get(key) == "passed",
                    f"security processing control {key} must remain passed", failures)

    meaning = manifest.get("controlled_meaning")
    require(isinstance(meaning, dict), "security controlled_meaning object missing", failures)
    if isinstance(meaning, dict):
        supports = meaning.get("directly_supports")
        limits = meaning.get("does_not_establish_by_itself")
        require(isinstance(supports, list) and len(supports) >= 4,
                "security manifest needs at least four directly-supported propositions", failures)
        require(isinstance(limits, list) and len(limits) >= 6,
                "security manifest needs at least six express limitations", failures)

    for path in (
        SECURITY_PDF,
        SECURITY_TRANSCRIPT_ES,
        SECURITY_TRANSCRIPT_EN,
        SECURITY_README,
        SECURITY_REDACTION_LOG,
        SECURITY_SHA256SUMS,
    ):
        require(path.is_file() and path.stat().st_size > 0,
                f"missing or empty security publication artifact: {relative(path)}", failures)

    if SECURITY_PDF.is_file():
        actual_hash = sha256(SECURITY_PDF)
        require(actual_hash == EXPECTED_SECURITY_PDF_SHA256,
                f"security public PDF hash mismatch: {actual_hash}", failures)
        raw_pdf = SECURITY_PDF.read_bytes()
        for forbidden in (b"/JavaScript", b"/JS ", b"/OpenAction", b"/EmbeddedFile", b"/AcroForm", b"/Encrypt"):
            require(forbidden not in raw_pdf,
                    f"security public PDF contains forbidden structure marker {forbidden!r}", failures)

    checksum_text = read_text(SECURITY_SHA256SUMS, failures)
    require(
        f"{EXPECTED_SECURITY_PDF_SHA256}  public/2018-02-27-ac-community-security-request-redacted-searchable.pdf"
        in checksum_text,
        "security checksum manifest does not bind the canonical public PDF",
        failures,
    )
    require(EXPECTED_RESTRICTED_SOURCE_SHA256 not in checksum_text,
            "security checksum manifest must not list an intentionally absent restricted source as a check target", failures)
    for line_number, line in enumerate(checksum_text.splitlines(), start=1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
        require(match is not None,
                f"invalid security checksum line {line_number}: {line!r}", failures)
        if match is None:
            continue
        expected_hash, target = match.groups()
        target_path = SECURITY_DIR / target
        require(target_path.is_file(),
                f"security checksum target is not committed: {target}", failures)
        if target_path.is_file():
            require(sha256(target_path) == expected_hash,
                    f"security checksum mismatch: {target}", failures)

    es_text = read_text(SECURITY_TRANSCRIPT_ES, failures)
    en_text = read_text(SECURITY_TRANSCRIPT_EN, failures)
    require_markers(
        SECURITY_TRANSCRIPT_ES,
        es_text,
        (
            "SP-2018-02-27-AC-SECURITY-REQUEST",
            "[DIRECCIÓN ELECTRÓNICA DIRECTA SUPRIMIDA — R1]",
            "[DIRECCIÓN ELECTRÓNICA DIRECTA SUPRIMIDA — R2]",
            "[DIRECCIÓN ELECTRÓNICA DIRECTA SUPRIMIDA — R3]",
            "[sic]",
        ),
        failures,
    )
    require_markers(
        SECURITY_TRANSCRIPT_EN,
        en_text,
        (
            "SP-2018-02-27-AC-SECURITY-REQUEST",
            "[DIRECT ELECTRONIC ADDRESS REMOVED — R1]",
            "[DIRECT ELECTRONIC ADDRESS REMOVED — R2]",
            "[DIRECT ELECTRONIC ADDRESS REMOVED — R3]",
            "not adopted as an independently verified fact",
        ),
        failures,
    )
    for path, text in ((SECURITY_TRANSCRIPT_ES, es_text), (SECURITY_TRANSCRIPT_EN, en_text)):
        matches = sorted(set(EMAIL_RE.findall(text)))
        require(not matches,
                f"direct email address leaked in {relative(path)}: {matches!r}", failures)

    readme = read_text(SECURITY_README, failures)
    redaction_log = read_text(SECURITY_REDACTION_LOG, failures)
    publication_control = read_text(SECURITY_CONTROL, failures)
    require_markers(
        SECURITY_README,
        readme,
        (
            "REDACTED · SEARCHABLE · SOURCE-CONTROLLED",
            "Public/private separation",
            "unredacted scan is not stored in the public repository",
            EXPECTED_SECURITY_PDF_SHA256,
        ),
        failures,
    )
    require_markers(
        SECURITY_REDACTION_LOG,
        redaction_log,
        (
            "R1",
            "R2",
            "R3",
            "No unredacted copy is committed",
            EXPECTED_SECURITY_PDF_SHA256,
        ),
        failures,
    )
    require_markers(
        SECURITY_CONTROL,
        publication_control,
        (
            "SP-2018-02-27-AC-SECURITY-REQUEST",
            "PRIMARY SOURCE LOCATED",
            "Public/private separation",
            EXPECTED_SECURITY_PDF_SHA256,
            "not, without additional sources, evidence of",
        ),
        failures,
    )

    committed_pdfs = sorted(path.relative_to(SECURITY_DIR).as_posix() for path in SECURITY_DIR.rglob("*.pdf"))
    require(committed_pdfs == ["public/2018-02-27-ac-community-security-request-redacted-searchable.pdf"],
            f"unexpected PDF in public security evidence directory: {committed_pdfs!r}", failures)


def check_analytical_artifacts(failures: list[str]) -> None:
    digest = read_text(DIGEST, failures)
    communications = read_text(COMMUNICATIONS, failures)
    prompt = read_text(PROMPT, failures)

    common_markers = (
        "127 canonical records",
        RESULT_LABELS["inventory_status"],
        RESULT_LABELS["publication_status"],
        "C36-SUP-ACSEC-2018-02-27",
        "15 February 2018",
    )
    require_markers(DIGEST, digest, common_markers, failures)
    require_markers(
        DIGEST,
        digest,
        (
            "72",
            "50",
            "5",
            "8",
            "official denominator",
            "Twelve priority gaps",
            "Public/private boundary",
            "connector",
        ),
        failures,
    )
    digest_hash_match = re.search(
        r"\*\*Control-file SHA-256 at this run:\*\* `([0-9a-f]{64})`",
        digest,
    )
    require(digest_hash_match is not None,
            "digest must lock a 64-hex SHA-256 for the final catalogue", failures)
    if digest_hash_match is not None and CATALOGUE.is_file():
        require(digest_hash_match.group(1) == sha256(CATALOGUE),
                "digest catalogue hash does not match the final JSON bytes", failures)
    require_markers(COMMUNICATIONS, communications, common_markers, failures)
    require_markers(
        COMMUNICATIONS,
        communications,
        (
            "Source / canonical ID",
            "Status",
            "Action or communication",
            "Located court/LAJ response",
            "Next proof required",
            "Twelve controlled next-proof priorities",
            "Non-merger map",
        ),
        failures,
    )
    require_markers(
        PROMPT,
        prompt,
        (
            "127 canonical records",
            "five additional unique records",
            "CONCURSO36_COMPLETE_RECORD_EXECUTION_DIGEST_23AUG2026.md",
            "JUDGE_LAJ_COMMUNICATIONS_REGISTER_CONCURSO36.md",
            "SP-2018-02-27-AC-SECURITY-REQUEST",
            RESULT_LABELS["inventory_status"],
            RESULT_LABELS["publication_status"],
            "15 February 2018",
            "certified court index",
            "connected-source acquisition is read-only",
            "do not send, reply, forward, file, lodge or self-email",
        ),
        failures,
    )

    def count_numbered_items(text: str, heading: str, next_heading: str) -> int:
        start = text.find(heading)
        if start == -1:
            return 0
        end = text.find(next_heading, start + len(heading))
        section = text[start:end if end != -1 else None]
        return len(re.findall(r"(?m)^\d+\.\s", section))

    require(count_numbered_items(digest, "## 8. Twelve priority gaps", "## 9.") == 12,
            "digest must enumerate exactly 12 priority gaps", failures)
    require(count_numbered_items(communications, "## 9. Twelve controlled next-proof priorities", "## 10.") == 12,
            "communications register must enumerate exactly 12 next-proof priorities", failures)
    for path, text in ((DIGEST, digest), (COMMUNICATIONS, communications)):
        for pattern in (r"\b8 February 2018\b", r"\b8-Feb-2018\b", r"\b8 de febrero de 2018\b"):
            require(re.search(pattern, text, flags=re.IGNORECASE) is None,
                    f"{relative(path)} republishes the superseded creditor-date layer", failures)


class _HTMLCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[str] = []
        self.text_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = dict(attrs)
        for key in ("href", "src", "data"):
            value = attr_map.get(key)
            if value:
                self.links.append(value)

    def handle_data(self, data: str) -> None:
        self.text_parts.append(data)


def html_text(path: pathlib.Path, failures: list[str]) -> tuple[str, str, list[str]]:
    raw = read_text(path, failures)
    parser = _HTMLCollector()
    if raw:
        try:
            parser.feed(raw)
        except Exception as exc:  # HTMLParser errors are rare but should fail closed.
            failures.append(f"HTML parse failed for {relative(path)}: {exc}")
    return raw, " ".join(parser.text_parts), parser.links


def check_route_pages(failures: list[str]) -> None:
    page_text: dict[str, tuple[str, str, list[str]]] = {}
    for route in REQUIRED_ROUTES:
        path = ROOT / route / "index.html"
        require(path.is_file(), f"required bilingual route missing: {route}", failures)
        if path.is_file():
            page_text[route] = html_text(path, failures)
            raw = page_text[route][0]
            require(f'{BASE_URL}/{route}' in raw,
                    f"{route} lacks its canonical absolute URL", failures)

    marker_groups = {
        SPECIALIST_ROUTES[0]: ("50", "25", "especialista", "127", "cinco fuentes adicionales únicas", "11 PDF públicos seguros", "concurso36-complete-record-v1.json"),
        SPECIALIST_ROUTES[1]: ("50", "25", "specialist", "127", "five additional unique sources", "11 public-safe PDFs", "concurso36-complete-record-v1.json"),
        CRITICAL_READER_ROUTES[0]: ("15/02/2018", "INVENTARIO PARCIAL", "concurso36-complete-record-v1.json", "C36-SUP-ACSEC-2018-02-27", "2018-02-27-ac-community-security-request-redacted-searchable.pdf", "transcript.es.md"),
        CRITICAL_READER_ROUTES[1]: ("15 Feb 2018", "INVENTORY PARTIAL", "concurso36-complete-record-v1.json", "C36-SUP-ACSEC-2018-02-27", "2018-02-27-ac-community-security-request-redacted-searchable.pdf", "transcript.en.md"),
        SECURITY_ROUTES[0]: ("SP-2018-02-27-AC-SECURITY-REQUEST", "C36-SUP-ACSEC-2018-02-27", "27 de febrero de 2018", "redact", "2018-02-27-ac-community-security-request-redacted-searchable.pdf", "transcript.es.md"),
        SECURITY_ROUTES[1]: ("SP-2018-02-27-AC-SECURITY-REQUEST", "C36-SUP-ACSEC-2018-02-27", "27 February 2018", "redact", "2018-02-27-ac-community-security-request-redacted-searchable.pdf", "transcript.en.md"),
        ADJUDICATION_ROUTES[0]: ("18/05/2021 · E044", "15/10/2021 · E046", "15/10/2021 · E047", "26/01/2022 · E050", "26/01/2022 · E051", "no hizo nueva adjudicación", "recitación contradictoria de la escritura"),
        ADJUDICATION_ROUTES[1]: ("18 May 2021 · E044", "15 Oct 2021 · E046", "15 Oct 2021 · E047", "26 Jan 2022 · E050", "26 Jan 2022 · E051", "made no new award", "conflicting deed recital"),
    }
    for route, markers in marker_groups.items():
        raw = page_text.get(route, ("", "", []))[0]
        for marker in markers:
            require(marker.lower() in raw.lower(), f"{route} missing marker {marker!r}", failures)

    stale_count_markers = (
        "126-record",
        "126 registros",
        "four additional unique sources",
        "cuatro fuentes adicionales únicas",
        "10 public-safe PDFs",
    )
    for route in (*SPECIALIST_ROUTES, *CRITICAL_READER_ROUTES, *SECURITY_ROUTES):
        raw = page_text.get(route, ("", "", []))[0].lower()
        for marker in stale_count_markers:
            require(marker.lower() not in raw,
                    f"{route} retains superseded whole-record count marker {marker!r}", failures)

    if SPECIALIST_ROUTES[0] in page_text:
        specialist_es = page_text[SPECIALIST_ROUTES[0]][1].lower()
        require("todo el expediente" in specialist_es and ("no sustituye" in specialist_es or "no permite" in specialist_es),
                "Spanish specialist route must deny whole-file completeness", failures)
    if SPECIALIST_ROUTES[1] in page_text:
        specialist_en = page_text[SPECIALIST_ROUTES[1]][1].lower()
        require("whole file" in specialist_en and ("does not" in specialist_en or "not the whole" in specialist_en),
                "English specialist route must deny whole-file completeness", failures)
    if CRITICAL_READER_ROUTES[0] in page_text:
        critical_es = page_text[CRITICAL_READER_ROUTES[0]][1].lower()
        require("no es" in critical_es and ("expediente completo" in critical_es or "archivo completo" in critical_es),
                "Spanish critical reader must deny certified/whole-file completeness", failures)
    if CRITICAL_READER_ROUTES[1] in page_text:
        critical_en = page_text[CRITICAL_READER_ROUTES[1]][1].lower()
        require("not" in critical_en and ("complete court file" in critical_en or "whole court file" in critical_en),
                "English critical reader must deny certified/whole-file completeness", failures)

    for route in SECURITY_ROUTES:
        text = page_text.get(route, ("", "", []))[1].lower()
        require(any(term in text for term in ("does not identify", "does not prove", "no identifica", "no prueba", "no demuestra")),
                f"{route} must state what the security request does not establish", failures)
        require(any(term in text for term in ("restricted custody", "custodia restringida")),
                f"{route} must preserve the restricted-original boundary", failures)

    for route in ADJUDICATION_ROUTES:
        text = page_text.get(route, ("", "", []))[1].lower()
        require("complete signed" in text or "completo y firmado" in text,
                f"{route} must identify the located signed decision copies", failures)
        require("no distinct judicial act established" in text or "no original judicial" in text or "no un original judicial" in text,
                f"{route} must type 22 January as a deed recital, not a missing court act", failures)
        for stale in (
            "signed 18 may decision missing",
            "signed 15 october decisions missing",
            "decisiones firmadas de 18 de mayo pendientes",
            "decisiones firmadas de 15 de octubre pendientes",
        ):
            require(stale not in text,
                    f"{route} retains superseded missing-signed-decision wording: {stale!r}", failures)

    # The disputed alternate reconstruction must not escape into the analytical
    # critical readers.  Source transcriptions elsewhere may quote a party's
    # historical wording and are therefore deliberately outside this scan.
    disputed_date_patterns = (
        r"\b8 February 2018\b",
        r"\b8-Feb-2018\b",
        r"\b08/02/2018\b",
        r"\b8 de febrero de 2018\b",
    )
    for route in CRITICAL_READER_ROUTES:
        raw = page_text.get(route, ("", "", []))[0]
        for pattern in disputed_date_patterns:
            require(re.search(pattern, raw, flags=re.IGNORECASE) is None,
                    f"{route} republishes the superseded creditor-date layer: {pattern}", failures)

    for route, (_, _, links) in page_text.items():
        check_local_links(ROOT / route / "index.html", links, failures)

    check_unsupported_completeness_claims(
        [ROOT / route / "index.html" for route in REQUIRED_ROUTES] + [DIGEST, COMMUNICATIONS],
        failures,
    )


def check_implementation_register(failures: list[str]) -> None:
    text = read_text(IMPLEMENTATION_REGISTER, failures)
    require_markers(
        IMPLEMENTATION_REGISTER,
        text,
        (
            "18-May definitive approval (E046)",
            "12-May providencia (E047)",
            "clarification of J36-2021-10-15-B / E047",
            "clarification/completion of J36-2021-10-15-A / E046",
            "Notarial date recital only; no distinct judicial act established",
            "located signed **18 May 2021 E044 / Auto 164/2021**",
            "located signed **15 October 2021 E046 and E047** Autos",
            "located signed **26 January 2022 E050 and E051** clarifications",
        ),
        failures,
    )
    for stale in (
        "Recover the signed 18 May",
        "Recover the signed 15 October",
        "Recover the signed 26 January",
        "missing judicial original" + " for 22 January",
    ):
        require(stale not in text,
                f"implementation register retains superseded recovery target: {stale!r}", failures)


def resolve_local_target(source: pathlib.Path, link: str) -> pathlib.Path | None:
    link = link.strip()
    if not link or link.startswith(("#", "mailto:", "tel:", "javascript:", "data:")):
        return None
    parsed = urllib.parse.urlsplit(link)
    if parsed.scheme in {"http", "https"}:
        if f"{parsed.scheme}://{parsed.netloc}" != "https://sbu001monterecco.github.io":
            return None
        path_text = parsed.path
        prefix = "/por-derecho"
        if not path_text.startswith(prefix):
            return None
        path_text = path_text[len(prefix):]
        target = ROOT / urllib.parse.unquote(path_text.lstrip("/"))
    elif parsed.scheme or parsed.netloc:
        return None
    else:
        path_text = urllib.parse.unquote(parsed.path)
        if not path_text:
            return None
        if path_text.startswith("/por-derecho/"):
            target = ROOT / path_text[len("/por-derecho/"):]
        elif path_text.startswith("/"):
            target = ROOT / path_text.lstrip("/")
        else:
            target = source.parent / path_text
    target = target.resolve()
    try:
        target.relative_to(ROOT.resolve())
    except ValueError:
        return target
    return target


def check_local_links(source: pathlib.Path, links: Iterable[str], failures: list[str]) -> None:
    for link in sorted(set(links)):
        target = resolve_local_target(source, link)
        if target is None:
            continue
        try:
            target.relative_to(ROOT.resolve())
        except ValueError:
            failures.append(f"{relative(source)} local link escapes repository: {link!r}")
            continue
        candidate = target / "index.html" if target.is_dir() else target
        if not candidate.exists() and target.suffix == "" and link.rstrip().endswith("/"):
            candidate = target / "index.html"
        if not candidate.exists():
            failures.append(
                f"broken local link in {relative(source)}: {link!r} -> {relative(candidate)}"
            )


def check_unsupported_completeness_claims(paths: Iterable[pathlib.Path], failures: list[str]) -> None:
    patterns = (
        re.compile(r"\b(?:all|every)\b.{0,80}\b(?:decisions|orders|court records|court documents|communications)\b.{0,50}\b(?:uploaded|published)\b", re.I | re.S),
        re.compile(r"\b(?:complete|entire)\s+(?:certified\s+)?(?:court file|docket)\b", re.I),
        re.compile(r"\b(?:todos?|todas?)\b.{0,80}\b(?:autos|resoluciones|documentos judiciales|comunicaciones)\b.{0,50}\b(?:subidos?|publicados?)\b", re.I | re.S),
        re.compile(r"\bexpediente\s+(?:judicial\s+)?(?:completo|íntegro)\b", re.I),
    )
    caveats = (
        " not ", " no ", "never", "nunca", "neither", "until", "hasta que",
        "without", "sin ", "identified", "located", "public-safe", "público seguro",
        "not the whole", "no es", "no claim", "no se afirma", "no permite",
    )
    for path in paths:
        raw = read_text(path, failures)
        if not raw:
            continue
        if path.suffix.lower() in {".html", ".htm"}:
            parser = _HTMLCollector()
            parser.feed(raw)
            text = " ".join(parser.text_parts)
        else:
            text = raw
        lowered = " " + re.sub(r"\s+", " ", text).lower() + " "
        for pattern in patterns:
            for match in pattern.finditer(lowered):
                window = lowered[max(0, match.start() - 160): min(len(lowered), match.end() + 160)]
                if any(caveat in window for caveat in caveats):
                    continue
                failures.append(
                    f"unsupported completeness/all-uploaded wording in {relative(path)}: "
                    f"{match.group(0)!r}"
                )


def sitemap_urls(path: pathlib.Path, failures: list[str]) -> set[str]:
    try:
        root = ET.parse(path).getroot()
    except FileNotFoundError:
        failures.append(f"missing required sitemap: {relative(path)}")
        return set()
    except ET.ParseError as exc:
        failures.append(f"invalid XML in {relative(path)}: {exc}")
        return set()
    namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    return {
        element.text.strip()
        for element in root.findall("sm:url/sm:loc", namespace)
        if element.text and element.text.strip()
    }


def check_discovery(failures: list[str]) -> None:
    registry = load_json(ROUTE_REGISTRY, failures)
    require(isinstance(registry, list), "unitary route registry must be a JSON array", failures)
    if isinstance(registry, list):
        paths = [entry.get("path") for entry in registry if isinstance(entry, dict)]
        require(len(paths) == len(set(paths)), "duplicate paths in unitary route registry", failures)
        for route in REQUIRED_ROUTES:
            require(paths.count(route) == 1,
                    f"unitary route registry must contain exactly one {route}", failures)
        for entry in registry:
            if isinstance(entry, dict) and entry.get("path") in REQUIRED_ROUTES:
                route = str(entry.get("path"))
                expected_lang = route.split("/", 1)[0]
                require(entry.get("lang") == expected_lang,
                        f"route-registry language mismatch for {route}", failures)
                require(bool(entry.get("summary")) and bool(entry.get("title")),
                        f"route-registry title/summary missing for {route}", failures)

    main_urls = sitemap_urls(MAIN_SITEMAP, failures)
    unitary_urls = sitemap_urls(UNITARY_SITEMAP, failures)
    specialist_urls = sitemap_urls(SPECIALIST_SITEMAP, failures)
    adjudication_urls = sitemap_urls(ADJUDICATION_SITEMAP, failures)
    expected_all_urls = {f"{BASE_URL}/{route}" for route in REQUIRED_ROUTES}
    expected_specialist_urls = {
        f"{BASE_URL}/{route}"
        for route in (*SPECIALIST_ROUTES, *CRITICAL_READER_ROUTES)
    }
    expected_adjudication_urls = {f"{BASE_URL}/{route}" for route in ADJUDICATION_ROUTES}
    for url in sorted(expected_all_urls):
        require(url in main_urls, f"main sitemap missing {url}", failures)
        require(url in unitary_urls, f"unitary sitemap missing {url}", failures)
    for url in sorted(expected_specialist_urls):
        require(url in specialist_urls, f"specialist sitemap missing {url}", failures)
    for url in sorted(expected_adjudication_urls):
        require(url in adjudication_urls, f"adjudication sitemap missing {url}", failures)

    robots = read_text(ROBOTS, failures)
    for sitemap in (MAIN_SITEMAP, UNITARY_SITEMAP, SPECIALIST_SITEMAP, ADJUDICATION_SITEMAP):
        url = f"{BASE_URL}/{sitemap.name}"
        require(f"Sitemap: {url}" in robots,
                f"robots.txt does not discover {sitemap.name}", failures)


def main() -> int:
    failures: list[str] = []
    check_catalogue(failures)
    check_publication_manifest(failures)
    check_security_publication(failures)
    check_analytical_artifacts(failures)
    check_route_pages(failures)
    check_implementation_register(failures)
    check_discovery(failures)

    if failures:
        print(f"Concurso 36/2012 complete-record validation failed ({len(failures)} issue(s)):")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(
        "Concurso 36/2012 complete-record validation passed: "
        "127 canonical records (72 historical + 50 specialist + 5 supplemental), "
        "8 source-copy links, 12 controlled gaps, public-source privacy/hash controls, "
        "bilingual discovery and local-link integrity."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
