#!/usr/bin/env python3
"""Repository-wide publication/deletion-safety guard for Por Derecho.

The invariant is simple: chat narration is never proof of publication. Source must be
recoverable in Git, validation must be reproducible, merge must be observable, and
LIVE VERIFIED / DELETION SAFE are states earned by evidence rather than prose.
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import os
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_DIR = ROOT / "publication-manifests"
ORDER = [
    "DRAFT",
    "PREPARED_PENDING_MERGE",
    "REMOTE_SOURCE",
    "PR_OPEN",
    "CI_GREEN",
    "MERGED",
    "DEPLOYED",
    "LIVE_VERIFIED",
    "DELETION_SAFE",
]
VALID_STATES = set(ORDER) | {"BLOCKED_RECOVERY"}
FORBIDDEN_TEMP_NAMES = {"NOOP.tmp", "SHOULD_NOT_EXIST.tmp"}
ENCODED_SUFFIXES = {".b64", ".tar", ".gz", ".tgz", ".zip"}


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def changed_files() -> list[str]:
    base = os.getenv("GITHUB_BASE_SHA", "").strip()
    head = os.getenv("GITHUB_HEAD_SHA", "HEAD").strip() or "HEAD"
    if not base or set(base) == {"0"}:
        return []
    try:
        out = subprocess.check_output(
            ["git", "diff", "--name-only", f"{base}...{head}"],
            cwd=ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        )
        return [line.strip() for line in out.splitlines() if line.strip()]
    except Exception:
        return []


def load_manifests(errors: list[str]) -> list[tuple[Path, dict]]:
    manifests: list[tuple[Path, dict]] = []
    if not MANIFEST_DIR.exists():
        return manifests
    for path in sorted(MANIFEST_DIR.glob("*.json")):
        try:
            manifests.append((path, json.loads(path.read_text(encoding="utf-8"))))
        except Exception as exc:
            fail(f"{path.relative_to(ROOT)}: invalid JSON: {exc}", errors)
    return manifests


def load_json_control(manifest_path: Path, declared_path: object, label: str, errors: list[str]) -> dict | None:
    rel = manifest_path.relative_to(ROOT)
    if not isinstance(declared_path, str) or not declared_path.strip():
        fail(f"{rel}: domain reconciliation control {label!r} must be a repository-relative path", errors)
        return None
    candidate = Path(declared_path)
    if candidate.is_absolute() or ".." in candidate.parts:
        fail(f"{rel}: unsafe domain reconciliation control path for {label}: {declared_path!r}", errors)
        return None
    path = ROOT / candidate
    if not path.is_file():
        fail(f"{rel}: domain reconciliation control missing: {declared_path}", errors)
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"{rel}: invalid domain reconciliation control {declared_path}: {exc}", errors)
        return None
    if not isinstance(value, dict):
        fail(f"{rel}: domain reconciliation control must contain a JSON object: {declared_path}", errors)
        return None
    return value


def source_document_ids(value: object) -> list[str]:
    """Return concrete source IDs without treating legacy-alias arrays as new sources."""
    found: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            if key == "source_document_id" and isinstance(child, str) and child.strip():
                found.append(child)
            else:
                found.extend(source_document_ids(child))
    elif isinstance(value, list):
        for child in value:
            found.extend(source_document_ids(child))
    return found


def validate_acta_domain_reconciliation(path: Path, data: dict, errors: list[str]) -> None:
    reconciliation = data.get("domain_reconciliation")
    if reconciliation is None:
        return
    rel = path.relative_to(ROOT)
    if not isinstance(reconciliation, dict):
        fail(f"{rel}: domain_reconciliation must be an object", errors)
        return
    profile = reconciliation.get("profile")
    if profile != "community-acta-document-room-v1":
        fail(f"{rel}: unsupported domain_reconciliation profile {profile!r}", errors)
        return

    controls = reconciliation.get("controls")
    expected = reconciliation.get("expected")
    if not isinstance(controls, dict) or not isinstance(expected, dict):
        fail(f"{rel}: domain_reconciliation requires object-valued controls and expected fields", errors)
        return

    public_index = load_json_control(path, controls.get("public_index"), "public_index", errors)
    lineage = load_json_control(path, controls.get("meeting_lineage"), "meeting_lineage", errors)
    source_reconciliation = load_json_control(
        path, controls.get("source_family_reconciliation"), "source_family_reconciliation", errors
    )
    private_ocr = load_json_control(path, controls.get("private_ocr_custody"), "private_ocr_custody", errors)
    if None in (public_index, lineage, source_reconciliation, private_ocr):
        return

    public_events = public_index.get("events")
    lineage_events = lineage.get("events")
    source_families = source_reconciliation.get("families")
    private_packages = private_ocr.get("packages")
    if not all(isinstance(value, list) for value in (public_events, lineage_events, source_families, private_packages)):
        fail(f"{rel}: ACTA reconciliation controls must expose events/families/packages arrays", errors)
        return

    route_es = [event.get("detail_page_es") for event in lineage_events if isinstance(event, dict)]
    route_en = [event.get("detail_page_en") for event in lineage_events if isinstance(event, dict)]
    for language, routes in (("ES", route_es), ("EN", route_en)):
        if len(routes) != len(lineage_events) or any(not isinstance(route, str) or not route for route in routes):
            fail(f"{rel}: {language} event-route coverage is incomplete", errors)
            continue
        if len(set(routes)) != len(routes):
            fail(f"{rel}: duplicate {language} event routes in meeting-lineage control", errors)
        missing = [route for route in routes if not (ROOT / route).is_file()]
        if missing:
            fail(f"{rel}: {language} event routes missing from repository: {', '.join(missing)}", errors)

    source_ids = source_document_ids(source_families)
    source_page_count = sum(int(event.get("source_preview_count", 0) or 0) for event in public_events)
    preview_count = sum(int(event.get("preview_count", 0) or 0) for event in public_events)
    pdf_page_count = sum(int(event.get("public_pdf_page_count", 0) or 0) for event in public_events)
    source_facsimile_paths = {
        event.get("redacted_source_facsimile")
        for event in public_events
        if isinstance(event, dict) and event.get("redacted_source_facsimile")
    }
    text_pdf_paths = {
        event.get("public_pdf") for event in public_events if isinstance(event, dict) and event.get("public_pdf")
    }
    private_source_pages = sum(
        int(package.get("source", {}).get("pages", 0) or 0) for package in private_packages if isinstance(package, dict)
    )
    private_rendered_pages = sum(
        int(package.get("ocr", {}).get("rendered_image_count", 0) or 0)
        for package in private_packages
        if isinstance(package, dict)
    )
    private_text_pages = sum(
        int(package.get("ocr", {}).get("ocr_text_count", 0) or 0)
        for package in private_packages
        if isinstance(package, dict)
    )
    perimeter_event_distribution: dict[str, int] = {}
    for event in lineage_events:
        code = event.get("perimeter_code")
        if isinstance(code, str) and code:
            perimeter_event_distribution[code] = perimeter_event_distribution.get(code, 0) + 1

    actual = {
        "controlled_events": len(lineage_events),
        "bilingual_event_pages": len(route_es) + len(route_en),
        "located_acta_or_minutes_families": source_reconciliation.get("located_acta_or_minutes_families"),
        "located_non_acta_source_packages": source_reconciliation.get("located_non_acta_source_packages"),
        "controlled_source_packages": source_reconciliation.get("controlled_source_packages"),
        "source_pages": source_page_count,
        "text_edition_pages": pdf_page_count,
        "source_facsimiles": len(source_facsimile_paths),
        "text_edition_pdfs": len(text_pdf_paths),
        "source_page_images": len(list(ROOT.glob("assets/evidence/community-actas-source/*/*.jpg"))),
        "text_preview_images": len(list(ROOT.glob("assets/evidence/community-actas/*/*.jpg"))),
        "current_jpeg_derivatives": len(list(ROOT.glob("assets/evidence/community-actas-source/*/*.jpg")))
        + len(list(ROOT.glob("assets/evidence/community-actas/*/*.jpg"))),
        "legacy_webp_derivatives": len(list(ROOT.glob("assets/evidence/community-actas/*/*.webp"))),
        "public_redacted_ocr_packages": public_index.get("public_redacted_ocr_packages"),
        "marker_only_packages": public_index.get("marker_only_public_redaction_packages"),
        "unique_source_document_ids": len(set(source_ids)),
        "private_ocr_packages": len(private_packages),
        "private_ocr_source_pages": private_source_pages,
        "perimeter_event_distribution": perimeter_event_distribution,
    }
    required_keys = set(actual)
    if set(expected) != required_keys:
        missing = sorted(required_keys - set(expected))
        extra = sorted(set(expected) - required_keys)
        fail(f"{rel}: domain expected-key mismatch (missing={missing}, extra={extra})", errors)
    for key, value in actual.items():
        if expected.get(key) != value:
            fail(f"{rel}: domain count {key} expected {expected.get(key)!r}, control/filesystem has {value!r}", errors)

    # Independent within-control parity catches a coherent-looking manifest backed by
    # contradictory indexes or incomplete rendering output.
    parity_checks = [
        ("public-index configured source packages", public_index.get("configured_source_packages"), len(public_events)),
        ("public-index controlled source packages", public_index.get("controlled_source_packages"), len(public_events)),
        ("source-family rows", len(source_families), source_reconciliation.get("controlled_source_packages")),
        ("text preview/PDF page totals", preview_count, pdf_page_count),
        ("private OCR rendered/source pages", private_rendered_pages, private_source_pages),
        ("private OCR text/source pages", private_text_pages, private_source_pages),
        ("source IDs/unique source IDs", len(source_ids), len(set(source_ids))),
    ]
    for label, left, right in parity_checks:
        if left != right:
            fail(f"{rel}: {label} mismatch ({left!r} vs {right!r})", errors)

    package_state = data.get("package_state") or {}
    package_state_map = {
        "located_acta_or_minutes_families": "located_acta_or_minutes_families",
        "located_non_acta_source_packages": "located_non_acta_source_packages",
        "controlled_source_packages": "controlled_source_packages",
        "unique_source_document_ids": "unique_source_document_ids",
        "digitised_and_prepared_packages": "controlled_source_packages",
        "source_pages_represented": "source_pages",
        "redacted_source_facsimiles": "source_facsimiles",
        "redacted_source_page_images": "source_page_images",
        "ocr_text_packages": "public_redacted_ocr_packages",
        "marker_only_public_redaction_packages": "marker_only_packages",
        "rendered_text_edition_pdfs": "text_edition_pdfs",
        "rendered_text_edition_pages": "text_edition_pages",
        "rendered_text_edition_page_images": "text_preview_images",
        "current_jpeg_derivatives": "current_jpeg_derivatives",
        "legacy_webp_derivatives": "legacy_webp_derivatives",
        "controlled_meeting_acta_events": "controlled_events",
        "bilingual_individual_event_pages": "bilingual_event_pages",
        "embedded_public_redacted_ocr_packages": "public_redacted_ocr_packages",
        "private_automated_ocr_packages": "private_ocr_packages",
        "private_automated_ocr_source_pages": "private_ocr_source_pages",
        "perimeter_event_distribution": "perimeter_event_distribution",
    }
    for state_key, expected_key in package_state_map.items():
        if package_state.get(state_key) != expected.get(expected_key):
            fail(
                f"{rel}: package_state.{state_key}={package_state.get(state_key)!r} "
                f"does not match domain expected {expected_key}={expected.get(expected_key)!r}",
                errors,
            )

    expected_routes = data.get("expected_routes") or {}
    if expected_routes.get("individual_event_pages_es") != len(route_es):
        fail(f"{rel}: expected_routes.individual_event_pages_es does not match meeting-lineage control", errors)
    if expected_routes.get("individual_event_pages_en") != len(route_en):
        fail(f"{rel}: expected_routes.individual_event_pages_en does not match meeting-lineage control", errors)

    if data.get("current_state") == "PREPARED_PENDING_MERGE":
        closeout = data.get("publication_closeout") or {}
        if closeout.get("pull_request") is not None or closeout.get("merge_sha") is not None:
            fail(f"{rel}: prepared-pending-merge state must not declare a PR or merge SHA", errors)
        if data.get("merge_sha") is not None:
            fail(f"{rel}: prepared-pending-merge state must keep top-level merge_sha null", errors)


def validate_manifest(path: Path, data: dict, errors: list[str]) -> None:
    rel = path.relative_to(ROOT)
    required = ["publication_id", "current_state", "expected_routes", "owner"]
    for key in required:
        if key not in data:
            fail(f"{rel}: missing required field {key!r}", errors)

    state = data.get("current_state")
    if state not in VALID_STATES:
        fail(f"{rel}: unknown current_state {state!r}", errors)
        return

    routes = data.get("expected_routes") or {}
    es = routes.get("es") or []
    en = routes.get("en") or []
    if not isinstance(es, list) or not isinstance(en, list):
        fail(f"{rel}: expected_routes.es/en must be arrays", errors)
        return
    if es or en:
        if len(es) != len(en):
            fail(f"{rel}: bilingual route parity failed ({len(es)} ES vs {len(en)} EN)", errors)
        if len(set(es + en)) != len(es + en):
            fail(f"{rel}: duplicate route paths declared", errors)

    if state == "BLOCKED_RECOVERY":
        if not data.get("blocking_reason"):
            fail(f"{rel}: BLOCKED_RECOVERY requires blocking_reason", errors)
        if not data.get("recovery_requirements"):
            fail(f"{rel}: BLOCKED_RECOVERY requires recovery_requirements", errors)
        return

    rank = ORDER.index(state)
    if rank >= ORDER.index("REMOTE_SOURCE"):
        for route in es + en:
            if not (ROOT / route).is_file():
                fail(f"{rel}: declared route missing from Git source: {route}", errors)
        for source in data.get("expected_source_files", []):
            if not (ROOT / source).is_file():
                fail(f"{rel}: declared source file missing from Git: {source}", errors)

    if rank >= ORDER.index("CI_GREEN"):
        validation = data.get("validation") or {}
        if not validation.get("evidence"):
            fail(f"{rel}: CI_GREEN or later requires validation.evidence", errors)
    if rank >= ORDER.index("MERGED") and not data.get("merge_sha"):
        fail(f"{rel}: MERGED or later requires merge_sha", errors)
    if rank >= ORDER.index("DEPLOYED") and not data.get("deployment_evidence"):
        fail(f"{rel}: DEPLOYED or later requires deployment_evidence", errors)
    if rank >= ORDER.index("LIVE_VERIFIED"):
        if not data.get("live_urls"):
            fail(f"{rel}: LIVE_VERIFIED or later requires live_urls", errors)
        if not data.get("live_verification_evidence"):
            fail(f"{rel}: LIVE_VERIFIED or later requires live_verification_evidence", errors)
    if rank >= ORDER.index("DELETION_SAFE") and not data.get("deletion_record"):
        fail(f"{rel}: DELETION_SAFE requires deletion_record", errors)

    validate_acta_domain_reconciliation(path, data, errors)


def validate_changed_files(files: list[str], manifests: list[tuple[Path, dict]], errors: list[str]) -> None:
    bootstrap_rules = []
    for _, data in manifests:
        rule = data.get("encoded_bootstrap")
        if rule:
            bootstrap_rules.append(rule)

    for rel in files:
        p = Path(rel)
        if p.name in FORBIDDEN_TEMP_NAMES or p.suffix == ".tmp":
            fail(f"forbidden temporary/placeholder artefact changed: {rel}", errors)

        if p.suffix.lower() in ENCODED_SUFFIXES and ("payload" in rel.lower() or "bootstrap" in rel.lower()):
            allowed = False
            for rule in bootstrap_rules:
                pattern = rule.get("pattern", "")
                if pattern and fnmatch.fnmatch(rel, pattern):
                    complete = bool(rule.get("complete"))
                    declared = int(rule.get("declared_parts", 0) or 0)
                    actual = len(list(ROOT.glob(pattern)))
                    if complete and declared > 0 and actual == declared:
                        allowed = True
                    else:
                        fail(
                            f"encoded bootstrap is incomplete: {rel} (declared={declared}, actual={actual}, complete={complete})",
                            errors,
                        )
                    break
            if not allowed and not any(fnmatch.fnmatch(rel, r.get("pattern", "")) for r in bootstrap_rules):
                fail(f"encoded bootstrap/payload is not an accepted publication source: {rel}", errors)


def live_check(manifests: list[tuple[Path, dict]], errors: list[str]) -> None:
    for path, data in manifests:
        state = data.get("current_state")
        if state not in {"DEPLOYED", "LIVE_VERIFIED", "DELETION_SAFE"}:
            continue
        markers = data.get("live_markers") or {}
        for url in data.get("live_urls") or []:
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "por-derecho-publication-integrity/1"})
                with urllib.request.urlopen(req, timeout=20) as response:
                    body = response.read().decode("utf-8", errors="replace")
                    if response.status != 200:
                        fail(f"{path.name}: live URL returned {response.status}: {url}", errors)
                    for marker in markers.get(url, []):
                        if marker not in body:
                            fail(f"{path.name}: live marker missing at {url}: {marker!r}", errors)
            except Exception as exc:
                fail(f"{path.name}: live verification failed for {url}: {exc}", errors)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--live", action="store_true", help="also verify manifests at DEPLOYED or later against public URLs")
    args = parser.parse_args()

    errors: list[str] = []
    manifests = load_manifests(errors)
    files = changed_files()
    validate_changed_files(files, manifests, errors)
    for path, data in manifests:
        validate_manifest(path, data, errors)
    if args.live:
        live_check(manifests, errors)

    if errors:
        print("PUBLICATION INTEGRITY GATE: FAIL")
        for error in errors:
            print(f" - {error}")
        return 1
    print(f"PUBLICATION INTEGRITY GATE: PASS ({len(manifests)} manifests; {len(files)} changed files inspected)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
