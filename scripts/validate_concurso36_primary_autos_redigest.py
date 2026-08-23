#!/usr/bin/env python3
"""Release gate for the 21 August 2026 Concurso 36/2012 autos redigest.

This validator keeps five publication layers aligned:

* pinned, name-sanitised public analytical derivatives;
* the bilingual machine-readable order register;
* the two dedicated public readers;
* sitemap/robots discovery; and
* downstream public routes, data and runtime scripts that can reintroduce a
  superseded date-layer, remedy, bidder or order-function claim.

It deliberately does not publish or validate native court/e-mail/Drive
binaries. Those remain in restricted custody under the archive README.
"""

from __future__ import annotations

import hashlib
import json
import pathlib
import re
import runpy
import sys
import xml.etree.ElementTree as ET
import zipfile
from collections.abc import Iterable
from collections.abc import Callable


ROOT = pathlib.Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "archive" / "concurso36-primary-autos-21aug2026"
DATA = ROOT / "assets" / "data" / "concurso36-what-court-ordered-v1.json"

ES_PAGE = ROOT / "es" / "concurso-36-2012-que-ordeno-el-juzgado" / "index.html"
EN_PAGE = ROOT / "en" / "concurso-36-2012-what-the-court-ordered" / "index.html"

BASE_URL = "https://sbu001monterecco.github.io/por-derecho"
ES_URL = f"{BASE_URL}/es/concurso-36-2012-que-ordeno-el-juzgado/"
EN_URL = f"{BASE_URL}/en/concurso-36-2012-what-the-court-ordered/"
COURT_ORDERS_SITEMAP_URL = f"{BASE_URL}/sitemap-concurso36-court-orders.xml"

EXACT_SURPLUS_CAVEAT = "No primary evidence of payment has yet been identified"

# These hashes bind the published, name-sanitised derivatives. They are not the
# hashes of the restricted originals preserved outside public Git. README.md is
# marker-validated instead: it is repository-native custody documentation and
# may acquire later, traceable editorial additions.
PUBLIC_DERIVATIVE_HASHES = {
    "FORENSIC_EVIDENCE_INDEX_CONCURSO_36_2012_21AUG2026.csv":
        "8d09e1ae079c03fbe01f73c567e8cb8e5668b51d9f34689f2e2a737fd1ceef62",
    "FORENSIC_SCAN_CRITICAL_AUTOS_CONCURSO_36_2012_21AUG2026.md":
        "ec01072a90b6f4b9f2d728ffa269f97e7864f9f9af51c5db7cf2a2e7eae324ad",
    "FORENSIC_SCAN_MANIFEST_CONCURSO_36_2012_21AUG2026.txt":
        "3e057b26f3db8c7ae857fcc1300db0db63eaa335ada1a4da51f57882e3bcdd5c",
    "GAP_CLOSURE_REGISTER_CONCURSO_36_2012_21AUG2026.csv":
        "4fbc5ae32cfbae2de6e605edefd5049595ba13760d1f5c62ce3efcaff4d9c468",
    "GAP_CLOSURE_REGISTER_CONCURSO_36_2012_21AUG2026.xlsx":
        "f69d6f3b9d89c99e475c35109f348712b426ce3f5bcccdd8d0ea8239444a5900",
    "REVERSE_ENGINEERING_FORENSIC_PROMPT_V2_CONCURSO_36_2012_21AUG2026.md":
        "7945816cd75bee612d0e27eb1c842c2bc16ae321ff3cf59fa1f79c7f662e1d3b",
    "REVERSE_ENGINEERING_REDIGEST_CONCURSO_36_2012_21AUG2026.md":
        "d4dab5840ad28334e8fb4485d03a199d71c54dab04b1ac36482c2007fdd4def8",
    "REVERSE_ENGINEERING_REDIGEST_MANIFEST_CONCURSO_36_2012_21AUG2026.txt":
        "b0167929cd92ddc1a14c9062942815039a2dedb01a26bb1250c6132dfb0b32eb",
    "artifact_closure_audit.md":
        "e904688b2711e7715cfcfa7411152dac54e375da8ef0c352af53c3fdbced8923",
    "connected_gap_scan.md":
        "17c6b9089dd31e0a1fc156928b245a77e62cc8df9e94d3c8ed67564553536249",
    "repo_site_reverse_engineering.md":
        "b34418785baba16a768b8b3c10c2316516acbb5c21d918c6bcec73f84308adbb",
}

PUBLIC_DERIVATIVE_MANIFEST = "PUBLIC_DERIVATIVE_SHA256SUMS.txt"
PUBLIC_DERIVATIVE_MANIFEST_SHA256 = (
    "b9b9ea61f6b31096ea37e6c71cc5f64d2aa85fb4c9a98acc54ff1e4cb5348d43"
)

EXPECTED_ORDER_IDS = {
    "C36-2012-06-06-DECLARATION",
    "C36-2017-12-19-LIQUIDATION",
    "C36-2018-02-15-CREDITOR",
    "C36-2018-04-16-PLAN",
    "C36-2018-06-04-CLARIFICATION",
    "C36-2018-06-26-STAY",
    "C36-2019-10-24-NONCONVALIDATION",
    "C36-2021-02-24-EXTENSION",
    "C36-2021-05-18-AUTO164",
    "C36-2021-10-15-PAIR",
    "C36-2022-01-26-CLARIFICATIONS",
    "C36-2022-02-21-PROTOCOL457",
}

EVIDENCE_LABELS = {
    "PROVEN BY PRIMARY DOCUMENT",
    "STRONGLY SUPPORTED",
    "INFERENCE",
    "UNRESOLVED",
    "CONTRADICTED",
    "DOCUMENT NOT YET LOCATED",
}

ORDER_FIELDS = {
    "id",
    "date",
    "document",
    "judge",
    "pages",
    "source",
    "source_status",
    "operative_effect_es",
    "operative_effect_en",
    "scope_es",
    "scope_en",
    "condition_es",
    "condition_en",
    "later_event_es",
    "later_event_en",
    "compliance_es",
    "compliance_en",
    "unresolved_es",
    "unresolved_en",
}

PAGE_MARKERS = {
    ES_PAGE: (
        "Texto judicial primario → condición o límite → hecho posterior → "
        "prueba de cumplimiento → cuestión no resuelta.",
        "15/02/2018",
        "20 días",
        "quedan pendientes de reinspección",
        "INVENTARIO PARCIAL",
        "concurso36-complete-record-v1.json",
        "04/06/2018",
        "copia canónica completa tiene <strong>3 páginas</strong>",
        "18/05/2021",
        "Aprobar de modo definitivo la propuesta de enajenación a favor de Construcciones Acosta Matos, S.A.",
        "postor tercero de 14,8 M€ no compareció ni consignó caución",
        "Dos <strong>aclaraciones</strong>",
        "No efectuaron nueva adjudicación",
        "Protocolo 457 —instrumento notarial, no auto—",
        "21/02/2022",
        "cinco días naturales",
        "Se excluyen de la liquidación los bienes de propiedad ajena",
        "Matkator 8584 y 8588",
        "No se ha identificado puente judicial de transferencia",
        EXACT_SURPLUS_CAVEAT,
        "Esto no prueba que naciera un sobrante jurídicamente exigible ni que no se pagara",
        "../../assets/data/concurso36-what-court-ordered-v1.json",
        "../../archive/CONCURSO36_COMPLETE_RECORD_EXECUTION_DIGEST_23AUG2026.md",
        "../../archive/JUDGE_LAJ_COMMUNICATIONS_REGISTER_CONCURSO36.md",
        EN_URL,
    ),
    EN_PAGE: (
        "Primary judicial text → condition or limit → later event → "
        "evidence of compliance → unresolved question.",
        "15 Feb 2018",
        "Twenty-day appeal",
        "await reinspection",
        "INVENTORY PARTIAL",
        "concurso36-complete-record-v1.json",
        "4 Jun 2018",
        "complete canonical copy has <strong>3 pages</strong>",
        "18 May 2021",
        "The disposal proposal in favour of Construcciones Acosta Matos, S.A. is definitively approved.",
        "EUR 14.8m third-party bidder did not appear or lodge the bond",
        "Two <strong>clarifications</strong>",
        "They made no new award",
        "Protocol 457—deed, not court order—",
        "21 Feb 2022",
        "five calendar days",
        "Third-party property is excluded from liquidation",
        "Matkator 8584 and 8588",
        "No judicial transfer bridge has been identified",
        EXACT_SURPLUS_CAVEAT,
        "This proves neither that a legally payable surplus arose nor that it went unpaid",
        "../../assets/data/concurso36-what-court-ordered-v1.json",
        "../../archive/CONCURSO36_COMPLETE_RECORD_EXECUTION_DIGEST_23AUG2026.md",
        "../../archive/JUDGE_LAJ_COMMUNICATIONS_REGISTER_CONCURSO36.md",
        ES_URL,
    ),
}

PUBLIC_SUFFIXES = {".html", ".htm", ".js", ".mjs", ".json", ".py"}
PUBLIC_TREES = (ROOT / "es", ROOT / "en", ROOT / "assets", ROOT / "scripts")
SELF_REFERENTIAL_SCRIPT_PREFIXES = ("audit_", "validate_", "rewrite_")

FORBIDDEN_PUBLIC_LOCATOR_PATTERNS = (
    re.compile(r"https://(?:drive|docs|mail)\.google\.com", re.IGNORECASE),
    re.compile(r"\bA05003250-[A-Za-z0-9-]+\b", re.IGNORECASE),
    re.compile(r"\b(?:Drive|Native Drive document)\s+[A-Za-z0-9_-]{20,}\b"),
)


def rel(path: pathlib.Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def read_text(path: pathlib.Path, failures: list[str]) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        failures.append(f"missing required file: {rel(path)}")
    except UnicodeDecodeError as exc:
        failures.append(f"UTF-8 decode failed for {rel(path)}: {exc}")
    return ""


def require_markers(
    path: pathlib.Path,
    text: str,
    markers: Iterable[str],
    failures: list[str],
) -> None:
    for marker in markers:
        if marker not in text:
            failures.append(f"{rel(path)} missing marker: {marker!r}")


def sha256(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def check_archive(failures: list[str]) -> None:
    if not ARCHIVE.is_dir():
        failures.append(f"missing public-safe archive directory: {rel(ARCHIVE)}")
        return

    manifest_path = ARCHIVE / PUBLIC_DERIVATIVE_MANIFEST
    manifest_text = read_text(manifest_path, failures)
    manifest_values: dict[str, str] = {}
    if not manifest_text and manifest_path.is_file():
        failures.append(f"public-derivative checksum manifest is empty: {rel(manifest_path)}")
    if manifest_text:
        for line_number, line in enumerate(manifest_text.splitlines(), start=1):
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            match = re.fullmatch(r"([0-9a-f]{64})  ([^/\\]+)", line)
            if match is None:
                failures.append(
                    f"invalid public-derivative checksum line {line_number}: {line!r}"
                )
                continue
            digest, name = match.groups()
            if name in manifest_values:
                failures.append(f"duplicate public-derivative checksum entry: {name}")
            manifest_values[name] = digest

        if manifest_values != PUBLIC_DERIVATIVE_HASHES:
            missing = set(PUBLIC_DERIVATIVE_HASHES) - set(manifest_values)
            unexpected = set(manifest_values) - set(PUBLIC_DERIVATIVE_HASHES)
            changed = {
                name
                for name in set(manifest_values) & set(PUBLIC_DERIVATIVE_HASHES)
                if manifest_values[name] != PUBLIC_DERIVATIVE_HASHES[name]
            }
            if missing:
                failures.append(
                    "public-derivative manifest missing entries: " + ", ".join(sorted(missing))
                )
            if unexpected:
                failures.append(
                    "public-derivative manifest has unexpected entries: "
                    + ", ".join(sorted(unexpected))
                )
            if changed:
                failures.append(
                    "public-derivative manifest hash drift: " + ", ".join(sorted(changed))
                )

        actual_manifest_hash = sha256(manifest_path)
        if actual_manifest_hash != PUBLIC_DERIVATIVE_MANIFEST_SHA256:
            failures.append(
                "public-derivative checksum manifest hash mismatch: expected "
                f"{PUBLIC_DERIVATIVE_MANIFEST_SHA256}, got {actual_manifest_hash}"
            )

    for name, expected in PUBLIC_DERIVATIVE_HASHES.items():
        path = ARCHIVE / name
        if not path.is_file():
            failures.append(f"missing hashed archive artifact: {rel(path)}")
            continue
        actual = sha256(path)
        if actual != expected:
            failures.append(
                f"archive hash mismatch: {rel(path)} expected {expected}, got {actual}"
            )

    readme = ARCHIVE / "README.md"
    text = read_text(readme, failures)
    require_markers(
        readme,
        text,
        (
            "public-safe analytical archive",
            "analysis and indexes, not the primary evidence itself",
            "raw or unredacted judicial, notarial, Registry, banking, tax, investor, email and litigation binaries",
            "b5e1b2ad71259f2be1d4d2c3e8d91b842a4152a101218e8f43cb98f0ee08be85",
            "public-safe, name-sanitised analytical reports",
            "exact hashes of the public derivatives in `PUBLIC_DERIVATIVE_SHA256SUMS.txt`",
            "Restricted-original and public-derivative integrity",
            "publication derivatives and are not represented as byte-identical "
            "replacements for the restricted originals",
            "`PUBLIC_DERIVATIVE_SHA256SUMS.txt` is the controlling checksum manifest",
            "must not be used as expected hashes for a public derivative whose protected name was sanitised",
            "Clickable mailbox/Drive URLs, Drive object IDs and court verification codes are withheld",
            EXACT_SURPLUS_CAVEAT,
            "does not prove non-existence",
            "PROVEN BY PRIMARY DOCUMENT",
            "DOCUMENT NOT YET LOCATED",
        ),
        failures,
    )

    # A public-safe analytical directory is not the place for native source
    # evidence or mailbox/container exports. The formatted XLSX register is the
    # one intentional non-text analytical artifact.
    risky_suffixes = {".pdf", ".zip", ".eml", ".msg", ".pst", ".mbox", ".doc", ".docx"}
    for path in ARCHIVE.rglob("*"):
        if path.is_file() and path.suffix.casefold() in risky_suffixes:
            failures.append(f"native/restricted evidence type in public archive: {rel(path)}")
        if ".cam_offer" in path.name.casefold():
            failures.append(f"temporary restricted source artifact in public archive: {rel(path)}")

    supersession_files = {
        "FORENSIC_SCAN_CRITICAL_AUTOS_CONCURSO_36_2012_21AUG2026.md":
            "SUPERSEDED DATE LAYER — 23 August 2026",
        "REVERSE_ENGINEERING_REDIGEST_CONCURSO_36_2012_21AUG2026.md":
            "SUPERSEDED DATE LAYER — 23 August 2026",
        "repo_site_reverse_engineering.md":
            "SUPERSEDED DATE LAYER — 23 August 2026",
        "artifact_closure_audit.md":
            "SUPERSEDED DATE LAYER — 23 August 2026",
    }
    for name, marker in supersession_files.items():
        path = ARCHIVE / name
        require_markers(path, read_text(path, failures), (marker,), failures)


def joined(record: dict[str, object], *fields: str) -> str:
    return " ".join(str(record.get(field, "")) for field in fields)


def require_terms(
    label: str,
    text: str,
    terms: Iterable[str],
    failures: list[str],
) -> None:
    folded = text.casefold()
    for term in terms:
        if term.casefold() not in folded:
            failures.append(f"{label} missing canonical term: {term!r}")


def check_json(failures: list[str]) -> None:
    raw = read_text(DATA, failures)
    if not raw:
        return
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        failures.append(f"invalid JSON in {rel(DATA)}: {exc}")
        return

    if data.get("schema_version") != "1.0":
        failures.append(f"{rel(DATA)} schema_version must be '1.0'")
    if data.get("generated_on") != "2026-08-23":
        failures.append(f"{rel(DATA)} generated_on must be 2026-08-23")

    case = data.get("case")
    if not isinstance(case, dict):
        failures.append(f"{rel(DATA)} case must be an object")
    else:
        if case.get("proceeding") != "Concurso ordinario 36/2012":
            failures.append(f"{rel(DATA)} has the wrong proceeding")
        if case.get("nig") != "3501647120120000351":
            failures.append(f"{rel(DATA)} has the wrong NIG")

    labels = data.get("evidence_labels")
    if not isinstance(labels, list) or set(labels) != EVIDENCE_LABELS:
        failures.append(f"{rel(DATA)} must preserve the six canonical evidence labels")

    orders = data.get("orders")
    if not isinstance(orders, list):
        failures.append(f"{rel(DATA)} orders must be a list")
        return

    by_id: dict[str, dict[str, object]] = {}
    for number, record in enumerate(orders, start=1):
        if not isinstance(record, dict):
            failures.append(f"{rel(DATA)} order {number} is not an object")
            continue
        missing = ORDER_FIELDS - set(record)
        if missing:
            failures.append(
                f"{rel(DATA)} order {number} missing fields: {', '.join(sorted(missing))}"
            )
        order_id = record.get("id")
        if not isinstance(order_id, str) or not order_id:
            failures.append(f"{rel(DATA)} order {number} has no valid id")
            continue
        if order_id in by_id:
            failures.append(f"{rel(DATA)} duplicate order id: {order_id}")
        by_id[order_id] = record

        source_status = record.get("source_status")
        if source_status not in EVIDENCE_LABELS:
            failures.append(f"{rel(DATA)} {order_id} has non-canonical source_status")
        for field in (
            "operative_effect_es",
            "operative_effect_en",
            "scope_es",
            "scope_en",
            "condition_es",
            "condition_en",
            "later_event_es",
            "later_event_en",
            "compliance_es",
            "compliance_en",
            "unresolved_es",
            "unresolved_en",
        ):
            if not isinstance(record.get(field), str) or not str(record.get(field)).strip():
                failures.append(f"{rel(DATA)} {order_id} has empty/non-text {field}")

    missing_ids = EXPECTED_ORDER_IDS - set(by_id)
    if missing_ids:
        failures.append(f"{rel(DATA)} missing order ids: {', '.join(sorted(missing_ids))}")

    def order(order_id: str) -> dict[str, object]:
        return by_id.get(order_id, {})

    creditor = order("C36-2018-02-15-CREDITOR")
    if creditor:
        if creditor.get("date") != "2018-02-15":
            failures.append("current creditor-substitution order control must be 2018-02-15")
        if creditor.get("pages") != 3:
            failures.append("creditor-substitution primary copy must have three pages")
        require_terms(
            "creditor-substitution current control",
            joined(creditor, "operative_effect_es", "operative_effect_en"),
            ("15 de febrero de 2018", "15 February 2018", "control primario", "primary-source control"),
            failures,
        )
        date_conflict = creditor.get("date_layer_conflict")
        if not isinstance(date_conflict, dict):
            failures.append("creditor-substitution record lacks a typed date-layer conflict")
        else:
            require_terms(
                "creditor-substitution date-layer conflict",
                joined(date_conflict, "status", "es", "en"),
                ("SUPERSEDED", "reinspecci", "re-inspect", "8/9/14"),
                failures,
            )
        require_terms(
            "creditor-substitution remedy",
            joined(creditor, "condition_es", "condition_en"),
            ("veinte días", "twenty days", "apelación", "appeal"),
            failures,
        )

    plan = order("C36-2018-04-16-PLAN")
    if plan:
        require_terms(
            "16 April 2018 plan perimeter",
            joined(plan, "operative_quote_es", "scope_es", "scope_en"),
            ("propiedad ajena", "third-party property", "exclusion"),
            failures,
        )

    june = order("C36-2018-06-04-CLARIFICATION")
    if june:
        if june.get("date") != "2018-06-04" or june.get("pages") != 3:
            failures.append("4 June 2018 canonical primary copy must be dated correctly and have three pages")
        require_terms(
            "4 June 2018 completeness",
            joined(june, "later_event_es", "later_event_en", "compliance_es", "compliance_en"),
            ("copia canónica completa", "complete canonical copy", "tres páginas", "three pages"),
            failures,
        )

    approval = order("C36-2021-05-18-AUTO164")
    if approval:
        if approval.get("date") != "2021-05-18":
            failures.append("Auto 164/2021 definitive approval date must be 2021-05-18")
        approval_effect = joined(
            approval,
            "document",
            "operative_quote_es",
            "operative_effect_es",
            "operative_effect_en",
        )
        require_terms(
            "Auto 164/2021 outcome",
            approval_effect,
            (
                "Auto 164/2021",
                "definitiv",
                "Construcciones Acosta Matos",
                "postor tercero",
                "third-party bidder",
                "no compareciera",
                "neither appeared",
                "caución",
                "bond",
            ),
            failures,
        )
        if "aweswell" in approval_effect.casefold():
            failures.append("Auto 164/2021 JSON must not associate Aweswell with the EUR 14.8m bid")
        require_terms(
            "Auto 164/2021 perimeter",
            joined(approval, "scope_es", "scope_en"),
            ("159", "31", "no propiedad de terceros", "no third-party property"),
            failures,
        )

    clarifications = order("C36-2022-01-26-CLARIFICATIONS")
    if clarifications:
        if clarifications.get("date") != "2022-01-26":
            failures.append("clarification-pair date must be 2022-01-26")
        if clarifications.get("pages") != [2, 3]:
            failures.append("26 January 2022 must preserve the two-copy page counts [2, 3]")
        require_terms(
            "26 January 2022 function",
            joined(
                clarifications,
                "document",
                "operative_effect_es",
                "operative_effect_en",
                "scope_es",
                "scope_en",
            ),
            ("dos autos de aclaración", "clarified", "no efectuaron una nueva adjudicación", "no new award"),
            failures,
        )

    protocol = order("C36-2022-02-21-PROTOCOL457")
    if protocol:
        if protocol.get("date") != "2022-02-21":
            failures.append("Protocol 457 date must be 2022-02-21")
        if protocol.get("judge") is not None:
            failures.append("Protocol 457 is a deed, not a judicial order with an issuing judge")
        require_terms(
            "Protocol 457 function",
            joined(protocol, "document", "operative_effect_es", "operative_effect_en"),
            ("Protocolo 457", "escritura", "no auto", "159"),
            failures,
        )
        require_terms(
            "Protocol 457 reporting duty",
            joined(protocol, "condition_es", "condition_en", "compliance_es", "compliance_en"),
            ("cinco días naturales", "five calendar days", "Juzgado", "court"),
            failures,
        )
        require_terms(
            "Protocol 457 third-party exclusion",
            joined(protocol, "scope_es", "scope_en"),
            ("Matkator", "8584", "8588", "31", "no incluyó", "did not include"),
            failures,
        )

    findings = data.get("cross_cutting_findings")
    if not isinstance(findings, dict):
        failures.append(f"{rel(DATA)} cross_cutting_findings must be an object")
    else:
        require_terms(
            "cross-cutting third-party finding",
            joined(findings, "third_party_es", "third_party_en"),
            ("Matkator", "8584", "8588", "puente judicial", "judicial transfer bridge"),
            failures,
        )
        require_terms(
            "cross-cutting surplus finding",
            joined(findings, "surplus_es", "surplus_en"),
            (
                EXACT_SURPLUS_CAVEAT,
                "no prueba que naciera",
                "ni que no se pagara",
                "neither that a legally payable surplus arose",
                "nor that it went unpaid",
            ),
            failures,
        )

    boundary = data.get("public_private_boundary")
    if not isinstance(boundary, dict):
        failures.append(f"{rel(DATA)} public_private_boundary must be an object")
    else:
        require_terms(
            "public/private boundary",
            joined(boundary, "es", "en"),
            ("custodia restringida", "restricted custody", "hashes", "completeness"),
            failures,
        )


def load_protected_token_check(failures: list[str]) -> Callable[[str], bool] | None:
    """Load the established hash-only bidder-name predicate."""

    anonymiser_path = ROOT / "scripts" / "validate_public_bidder_anonymisation.py"
    try:
        namespace = runpy.run_path(str(anonymiser_path), run_name="public_bidder_gate")
        contains_protected_token = namespace["contains_protected_token"]
    except Exception as exc:  # pragma: no cover - release diagnostics
        failures.append(f"could not load bidder-name digest gate: {exc}")
        return None
    return contains_protected_token


def check_archive_protected_token(
    contains_protected_token: Callable[[str], bool],
    failures: list[str],
) -> None:
    """Scan public derivatives, including the internal text of the XLSX."""

    text_suffixes = {".csv", ".json", ".md", ".rst", ".txt", ".xml"}
    for path in sorted(ARCHIVE.rglob("*")):
        if not path.is_file():
            continue
        if contains_protected_token(path.name):
            failures.append(f"protected bidder name found in public archive filename: {rel(path)}")

        if path.suffix.casefold() in text_suffixes:
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError as exc:
                failures.append(f"UTF-8 decode failed during archive privacy scan: {rel(path)}: {exc}")
                continue
            if contains_protected_token(text):
                failures.append(f"protected bidder name found in public archive derivative: {rel(path)}")
            for pattern in FORBIDDEN_PUBLIC_LOCATOR_PATTERNS:
                if pattern.search(text):
                    failures.append(
                        "restricted provider locator or court verification code found in "
                        f"public archive derivative: {rel(path)}"
                    )
                    break
            continue

        if path.suffix.casefold() != ".xlsx":
            continue
        try:
            with zipfile.ZipFile(path) as workbook:
                for member in workbook.infolist():
                    if member.is_dir() or not member.filename.casefold().endswith(
                        (".xml", ".rels", ".txt")
                    ):
                        continue
                    text = workbook.read(member).decode("utf-8", "replace")
                    if contains_protected_token(text):
                        failures.append(
                            "protected bidder name found inside public XLSX derivative: "
                            f"{rel(path)}::{member.filename}"
                        )
                        break
                    for pattern in FORBIDDEN_PUBLIC_LOCATOR_PATTERNS:
                        if pattern.search(text):
                            failures.append(
                                "restricted provider locator or court verification code found "
                                "inside public XLSX derivative: "
                                f"{rel(path)}::{member.filename}"
                            )
                            break
        except zipfile.BadZipFile as exc:
            failures.append(f"invalid XLSX during archive privacy scan: {rel(path)}: {exc}")

    workbook_path = ARCHIVE / "GAP_CLOSURE_REGISTER_CONCURSO_36_2012_21AUG2026.xlsx"
    try:
        with zipfile.ZipFile(workbook_path) as workbook:
            xml_text = " ".join(
                workbook.read(member).decode("utf-8", "replace")
                for member in workbook.namelist()
                if member.casefold().endswith((".xml", ".rels", ".txt"))
            )
    except (FileNotFoundError, zipfile.BadZipFile) as exc:
        failures.append(f"could not inspect controlled XLSX date layer: {rel(workbook_path)}: {exc}")
    else:
        if "Current repository control: 15 Feb 2018" not in xml_text:
            failures.append("public XLSX lacks the current 15-Feb-2018 date control")
        for forbidden in (
            "No public/generated occurrence uses 15 Feb as ruling date",
            "Creditor-substitution ruling was body-dated 8 February",
        ):
            if forbidden in xml_text:
                failures.append(f"public XLSX retains superseded date assertion: {forbidden!r}")


def check_pages_and_privacy(failures: list[str]) -> None:
    texts: dict[pathlib.Path, str] = {}
    for path, markers in PAGE_MARKERS.items():
        text = read_text(path, failures)
        texts[path] = text
        require_markers(path, text, markers, failures)

    # Reuse the repository's digest-only name check. This validator never needs
    # to know or reproduce the protected bidder's name.
    contains_protected_token = load_protected_token_check(failures)
    if contains_protected_token is None:
        return

    for path, text in {**texts, DATA: read_text(DATA, failures)}.items():
        if text and contains_protected_token(text):
            failures.append(f"protected bidder name found on canonical public surface: {rel(path)}")
    check_archive_protected_token(contains_protected_token, failures)


def parse_sitemap(path: pathlib.Path, failures: list[str]) -> tuple[set[str], set[str]]:
    text = read_text(path, failures)
    if not text:
        return set(), set()
    try:
        root = ET.fromstring(text)
    except ET.ParseError as exc:
        failures.append(f"invalid sitemap XML in {rel(path)}: {exc}")
        return set(), set()

    locs: set[str] = set()
    alternates: set[str] = set()
    for element in root.iter():
        local_name = element.tag.rsplit("}", 1)[-1]
        if local_name == "loc" and element.text:
            locs.add(element.text.strip())
        if local_name == "link" and element.attrib.get("rel") == "alternate":
            href = element.attrib.get("href")
            if href:
                alternates.add(href.strip())
    return locs, alternates


def check_discovery(failures: list[str]) -> None:
    main_sitemap = ROOT / "sitemap.xml"
    court_sitemap = ROOT / "sitemap-concurso36-court-orders.xml"
    main_locs, main_alternates = parse_sitemap(main_sitemap, failures)
    court_locs, court_alternates = parse_sitemap(court_sitemap, failures)

    for url in (ES_URL, EN_URL):
        if url not in main_locs:
            failures.append(f"{rel(main_sitemap)} does not discover {url}")
        if url not in main_alternates:
            failures.append(f"{rel(main_sitemap)} lacks bilingual alternate {url}")
        if url not in court_locs:
            failures.append(f"{rel(court_sitemap)} does not discover {url}")
        if url not in court_alternates:
            failures.append(f"{rel(court_sitemap)} lacks bilingual alternate {url}")

    robots = ROOT / "robots.txt"
    robots_text = read_text(robots, failures)
    if f"Sitemap: {COURT_ORDERS_SITEMAP_URL}" not in robots_text:
        failures.append(f"{rel(robots)} does not advertise the Concurso 36 court-orders sitemap")


def public_text_files() -> Iterable[pathlib.Path]:
    for tree in PUBLIC_TREES:
        if not tree.is_dir():
            continue
        for path in tree.rglob("*"):
            if not path.is_file() or path.suffix.casefold() not in PUBLIC_SUFFIXES:
                continue
            if path.resolve() == pathlib.Path(__file__).resolve():
                continue
            if tree == ROOT / "scripts" and path.name.startswith(
                SELF_REFERENTIAL_SCRIPT_PREFIXES
            ):
                # These controls necessarily encode the superseded strings they
                # are designed to find. Runtime/build scripts remain in scope.
                continue
            yield path


def compact(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def window(text: str, start: int, end: int, radius: int = 420) -> str:
    return text[max(0, start - radius): min(len(text), end + radius)]


def check_targeted_stale_claims(failures: list[str]) -> None:
    """Reject positive repetitions of the four high-risk superseded claims.

    Corrective quotations remain allowed when the local text expressly marks
    them as contradicted, false, superseded or not the operative proposition.
    """

    bidder = re.compile(
        r"aweswell.{0,180}(?:14[.,]8|postor|oferente|bidder|winning|winner|ganador)"
        r"|(?:14[.,]8|postor|oferente|bidder|winning|winner|ganador).{0,180}aweswell",
        re.IGNORECASE | re.DOTALL,
    )
    bidder_correction = re.compile(
        r"contradicted|false version|versi[oó]n err[oó]nea|correction|corrected|"
        r"correcci[oó]n|supersed|queda superad|no fue|was not|do not|no usar",
        re.IGNORECASE,
    )

    stale_creditor_date_8 = re.compile(
        r"(?:8(?:/02/2018|\s+(?:de\s+)?febrero(?:\s+de)?\s+2018|\s+february\s+2018|"
        r"\s+feb\s+2018)|2018-02-08).{0,340}"
        r"(?:CAM|PH122|sustituci[oó]n\s+de\s+acreedor|creditor[- ]substitution|article\s+1535)"
        r"|(?:CAM|PH122|sustituci[oó]n\s+de\s+acreedor|creditor[- ]substitution|article\s+1535)"
        r".{0,340}(?:8(?:/02/2018|\s+(?:de\s+)?febrero(?:\s+de)?\s+2018|"
        r"\s+february\s+2018|\s+feb\s+2018)|2018-02-08)",
        re.IGNORECASE | re.DOTALL,
    )
    stale_creditor_date_allowed = re.compile(
        r"supersed|superad|pending\s+(?:direct\s+)?re[- ]?inspection|"
        r"pendiente\s+de\s+reinspecci[oó]n|requires[-_ ]separate[-_ ]source|"
        r"no\s+se\s+publican\s+como\s+hechos|not\s+published\s+as\s+facts|"
        r"must\s+not\s+be\s+repeated|no\s+debe\s+repetirse",
        re.IGNORECASE,
    )

    five_day_remedy = re.compile(
        r"(?:auto|order).{0,260}(?:preve[ií]a|provided|carried|permit[ií]a|allowed)"
        r".{0,140}(?:reposici[oó]n\s+(?:en|de)\s+cinco\s+d[ií]as|"
        r"five[- ]day\s+(?:reconsideration|review))"
        r"|(?:reposici[oó]n\s+(?:en|de)\s+cinco\s+d[ií]as|"
        r"five[- ]day\s+(?:reconsideration|review)).{0,260}(?:auto|order)",
        re.IGNORECASE | re.DOTALL,
    )
    remedy_correction = re.compile(
        r"veinte\s+d[ií]as|20[- ]day|twenty[- ]day",
        re.IGNORECASE,
    )

    january_original = re.compile(
        r"(?:26(?:/01/2022|\s+(?:de\s+)?(?:ene(?:ro)?)(?:\s+de)?\s+2022|"
        r"\s+jan(?:uary)?\s+2022))"
        r".{0,220}(?:autoriz\w*.{0,50}adjudic|authori[sz]\w*.{0,50}(?:award|adjudic)|"
        r"adjudication\s+order|auto\s+de\s+adjudicaci[oó]n|alleged\s+adjudication)"
        r"|(?:autoriz\w*.{0,50}adjudic|authori[sz]\w*.{0,50}(?:award|adjudic)|"
        r"adjudication\s+order|auto\s+de\s+adjudicaci[oó]n|alleged\s+adjudication)"
        r".{0,220}(?:26(?:/01/2022|\s+(?:de\s+)?(?:ene(?:ro)?)(?:\s+de)?\s+2022|"
        r"\s+jan(?:uary)?\s+2022))",
        re.IGNORECASE | re.DOTALL,
    )
    january_correction = re.compile(
        r"clarification|aclaraci[oó]n|not\s+the\s+original|no\s+fueron?\s+la\s+"
        r"adjudicaci[oó]n|no\s+adjudic|made\s+no\s+new\s+award|contradicted|"
        r"correction|correcci[oó]n|do\s+not\s+use|no\s+usar",
        re.IGNORECASE,
    )

    june_incomplete = re.compile(
        r"(?:2018-06-04|04/06/2018|4\s+(?:de\s+)?junio(?:\s+de)?\s+2018|"
        r"4\s+june\s+2018).{0,520}(?:incomplet|continuation\s+missing|"
        r"two[- ]page|2\s+pages?|dos\s+p[aá]ginas?|2\s+p[aá]ginas?|ending\s+mid)"
        r"|(?:incomplet|continuation\s+missing|two[- ]page|2\s+pages?|"
        r"dos\s+p[aá]ginas?|2\s+p[aá]ginas?|ending\s+mid).{0,520}"
        r"(?:2018-06-04|04/06/2018|4\s+(?:de\s+)?junio(?:\s+de)?\s+2018|"
        r"4\s+june\s+2018)",
        re.IGNORECASE | re.DOTALL,
    )
    june_correction = re.compile(
        r"(?:complete\s+canonical|copia\s+can[oó]nica\s+completa).{0,100}"
        r"(?:three|tres|3).{0,25}(?:pages|p[aá]ginas)"
        r"|(?:three|tres|3).{0,25}(?:pages|p[aá]ginas).{0,100}"
        r"(?:complete\s+canonical|copia\s+can[oó]nica\s+completa)",
        re.IGNORECASE | re.DOTALL,
    )

    for path in public_text_files():
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        for match in bidder.finditer(text):
            context = window(text, match.start(), match.end())
            if bidder_correction.search(context):
                continue
            failures.append(
                f"stale bidder association on public surface: {rel(path)} :: "
                f"{compact(match.group(0))[:220]}"
            )
            break

        for match in stale_creditor_date_8.finditer(text):
            context = window(text, match.start(), match.end(), 180)
            if stale_creditor_date_allowed.search(context):
                continue
            failures.append(
                "8 February presented as the creditor-substitution order date without "
                f"the current 15-February/supersession control: {rel(path)}"
            )
            break

        for match in five_day_remedy.finditer(text):
            context = window(text, match.start(), match.end(), 520)
            if remedy_correction.search(context):
                continue
            failures.append(
                f"five-day remedy attributed to the creditor-substitution order: {rel(path)}"
            )
            break

        for match in january_original.finditer(text):
            context = window(text, match.start(), match.end(), 520)
            if january_correction.search(context):
                continue
            failures.append(
                f"26 January 2022 presented as original adjudication/award authority: {rel(path)}"
            )
            break

        for match in june_incomplete.finditer(text):
            context = window(text, match.start(), match.end(), 680)
            if june_correction.search(context):
                continue
            failures.append(
                f"4 June 2018 primary copy still presented as incomplete/two-page: {rel(path)}"
            )
            break


def main() -> int:
    failures: list[str] = []
    check_archive(failures)
    check_json(failures)
    check_pages_and_privacy(failures)
    check_discovery(failures)
    check_targeted_stale_claims(failures)

    if failures:
        print("Concurso 36/2012 primary-autos redigest gate FAILED", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print("Concurso 36/2012 primary-autos redigest gate passed")
    print(f"- {len(PUBLIC_DERIVATIVE_HASHES)} pinned public-derivative hashes verified")
    print(f"- {len(EXPECTED_ORDER_IDS)} canonical register entries verified")
    print("- bilingual readers and sitemap/robots discovery verified")
    print("- targeted stale-claim and bidder-name controls passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
