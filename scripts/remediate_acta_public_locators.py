#!/usr/bin/env python3
"""Replace provider-native ACTA locators with stable public-safe tokens.

The public token is deliberately non-reversible: it is a truncated SHA-256
digest over a versioned domain separator, locator kind and private locator.
When requested, the script writes the reverse lookup to a private JSON file
outside the repository.  It never prints private locator values.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTER = (
    REPO_ROOT
    / "evidence/community/COMMUNITY_AUTHORITY_EVENTS_EMAILS_MEETINGS_ACTAS_PUBLIC_REGISTER.md"
)

TEXT_SUFFIXES = {".csv", ".html", ".js", ".json", ".md", ".txt", ".yaml", ".yml"}

ADDITIONAL_PUBLIC_PRIVACY_TARGETS = {
    "CHATGPT_START_HERE.md",
    "INSTITUTIONAL_ACTIONS.md",
    "archive/BORJA_PWC_SUN_PARK_JUNTA_21APR2016_PRIMARY_EMAIL_RECORD_22AUG2026.md",
    "archive/CORRECTION_REGISTER_JONATHAN_SIMO_PWC_2016_APPEND_17AUG2026.md",
    "archive/CORRECTION_REGISTER.md",
    "archive/JONATHAN_SIMO_NATIVE_REPORTS_AND_MEETING_DATE_CORRECTION_17AUG2026.md",
    "archive/JONATHAN_SIMO_PWC_2016_PREMEETING_PRIMARY_EMAIL_ADDENDUM_17AUG2026.md",
    "archive/JONATHAN_SIMO_PWC_2016_RECORDING_RETRIEVAL_GATE_17AUG2026.md",
    "archive/PWC_2016_TRANSCRIPT_MANDATE_PERIMETER_AND_PAGES_DEPLOY_AUDIT_17AUG2026.md",
    "archive/SUN_PARK_COMMUNITY_PAMANIL_COMMUNICATIONS_DIGITISATION_REGISTER_22AUG2026.md",
    "archive/THREAD_DELETION_CONTINUITY_AUDIT_CEXP_MONTERECCO_PINK_AUTO804_FORENSIC_20AUG2026.md",
    "archive/THREAD_DELETION_CONTINUITY_AUDIT_GIL_PAMANIL_PINK_AEAT_22AUG2026.md",
    "archive/THREAD_DELETION_CONTINUITY_AUDIT_GIL_PINK_NULLITY_AEAT_COMMUNITY_22AUG2026.md",
    "archive/ESPEJO_SIMO_ACCOUNTING_CALIFICACION_EVIDENCE_DOSSIER_17AUG2026.md",
    "archive/THREAD_DELETION_CONTINUITY_AUDIT_ESPEJO_SIMO_ACCOUNTING_DOSSIER_17AUG2026.md",
    "archive/SUN_PARK_JUNTA_PWC_15_26APR2016_UNITARY_EVIDENCE_AND_CRIMINAL_LAW_TEST_22AUG2026.md",
    "archive/knowledge-project/PWC_CNMV_GAME_THEORY_THREAD_DELETION_ADDENDUM_19AUG2026.md",
    "archive/knowledge-project/PWC_CNMV_SOURCE_CORRECTION_DELETION_AUDIT_19AUG2026.md",
    "archive/knowledge-project/PWC_FINAL_ONE_SEND_RECIPIENT_CONTROL_19AUG2026.md",
    "archive/knowledge-project/PWC_INSTITUTIONAL_ESCALATION_SENT_RECORD_19AUG2026.md",
    "archive/knowledge-project/PWC_INVOICE_APPENDIX_89_7_HOURS_SOURCE_CONTROL_19AUG2026.md",
    "archive/knowledge-project/THREAD_DELETION_AUDIT_2026-08-19_PWC_MADRID_LONDON_SEND.md",
    "archive/knowledge-project/THREAD_DELETION_AUDIT_PWC_SAN_TELMO_RSM_GT_23AUG2026.md",
    "assets/data/alberto-meeting-point-357-multidirectional-evidence-v1.json",
    "docs/deletion-audits/2026-08-22-pwc-ac-refusal-alertador-sitewide-thread.md",
    "publication-manifests/pwc-ac-refusal-alertador-sitewide-20260822.json",
    "en/ric-private-equity-sun-park/index.html",
    "es/ric-private-equity-sun-park/index.html",
}

SCOPED_LINE_MARKERS: dict[str, tuple[str, ...]] = {}

# This source register uses a compact list in which several Gmail message IDs
# precede their descriptive prose and therefore have no same-line provider
# label.  The bounded path rule avoids treating unrelated 16-hex values in the
# wider repository as message locators.
BARE_GMAIL_ID_TARGETS = {
    "archive/CORRECTION_REGISTER.md",
    "archive/ESPEJO_SIMO_ACCOUNTING_CALIFICACION_EVIDENCE_DOSSIER_17AUG2026.md",
    "archive/JONATHAN_SIMO_PWC_2016_PREMEETING_PRIMARY_EMAIL_ADDENDUM_17AUG2026.md",
    "archive/SUN_PARK_JUNTA_PWC_15_26APR2016_UNITARY_EVIDENCE_AND_CRIMINAL_LAW_TEST_22AUG2026.md",
    "archive/THREAD_DELETION_CONTINUITY_AUDIT_ESPEJO_SIMO_ACCOUNTING_DOSSIER_17AUG2026.md",
    "archive/knowledge-project/PWC_CNMV_GAME_THEORY_THREAD_DELETION_ADDENDUM_19AUG2026.md",
    "archive/knowledge-project/PWC_CNMV_SOURCE_CORRECTION_DELETION_AUDIT_19AUG2026.md",
    "archive/knowledge-project/PWC_FINAL_ONE_SEND_RECIPIENT_CONTROL_19AUG2026.md",
    "archive/knowledge-project/PWC_INSTITUTIONAL_ESCALATION_SENT_RECORD_19AUG2026.md",
    "archive/knowledge-project/PWC_INVOICE_APPENDIX_89_7_HOURS_SOURCE_CONTROL_19AUG2026.md",
    "archive/knowledge-project/THREAD_DELETION_AUDIT_2026-08-19_PWC_MADRID_LONDON_SEND.md",
    "archive/knowledge-project/THREAD_DELETION_AUDIT_PWC_SAN_TELMO_RSM_GT_23AUG2026.md",
    "assets/data/alberto-meeting-point-357-multidirectional-evidence-v1.json",
    "docs/deletion-audits/2026-08-22-pwc-ac-refusal-alertador-sitewide-thread.md",
    "publication-manifests/pwc-ac-refusal-alertador-sitewide-20260822.json",
}

PRIVATE_EMAIL_TARGETS = {
    "archive/CORRECTION_REGISTER.md",
    "archive/ESPEJO_SIMO_ACCOUNTING_CALIFICACION_EVIDENCE_DOSSIER_17AUG2026.md",
    "archive/JONATHAN_SIMO_NATIVE_REPORTS_AND_MEETING_DATE_CORRECTION_17AUG2026.md",
    "archive/JONATHAN_SIMO_PWC_2016_PREMEETING_PRIMARY_EMAIL_ADDENDUM_17AUG2026.md",
    "archive/JONATHAN_SIMO_PWC_2016_RECORDING_RETRIEVAL_GATE_17AUG2026.md",
    "archive/SUN_PARK_JUNTA_PWC_15_26APR2016_UNITARY_EVIDENCE_AND_CRIMINAL_LAW_TEST_22AUG2026.md",
    "archive/knowledge-project/PWC_FINAL_ONE_SEND_RECIPIENT_CONTROL_19AUG2026.md",
    "archive/knowledge-project/PWC_INSTITUTIONAL_ESCALATION_SENT_RECORD_19AUG2026.md",
    "archive/knowledge-project/PWC_INVOICE_APPENDIX_89_7_HOURS_SOURCE_CONTROL_19AUG2026.md",
    "archive/knowledge-project/THREAD_DELETION_AUDIT_2026-08-19_PWC_MADRID_LONDON_SEND.md",
}

TOKEN_PREFIX = "SP-PRV-LCTR"
TOKEN_DOMAIN = "por-derecho/acta-public-locator/v1"
TOKEN_DIGEST_CHARS = 20

# Gmail message IDs are the provider's 16-hex identifiers. Requiring non-hex
# neighbours prevents matching a 16-character window inside a SHA-256 value.
# A second, contextual gate below requires a Gmail/message/thread label on the
# same source line; a bare 16-hex value is never treated as a locator.
GMAIL_MESSAGE_ID_RE = re.compile(r"(?<![0-9A-Fa-f])[0-9a-f]{16}(?![0-9A-Fa-f])")
GMAIL_CONTEXT_RE = re.compile(
    r"(?i)\b(?:gmail|message(?:s)?|thread|forward(?:ed)?(?:\s+copy)?|"
    r"mensaje(?:s)?|hilo|correo(?:s)?)\b"
)

# Google Drive/Docs IDs are base64url-like and, in the controlled material,
# begin with "1". The upper bound and right boundary avoid SHA-256 values.
# As with Gmail IDs, candidates are accepted only after an explicit Drive
# label or when embedded in a provider URL.
DRIVE_FILE_ID_RE = re.compile(
    r"(?<![A-Za-z0-9_-])1[A-Za-z0-9_-]{24,62}(?![A-Za-z0-9_-])"
)

# Two legacy discovery rows exposed truncated Drive locator fragments.  They
# are sensitive locators too, even though they are not retrieval-complete.
DRIVE_FRAGMENT_RE = re.compile(
    r"(?<![A-Za-z0-9_-])1[A-Za-z0-9_-]{2,23}(?:…|\.{3})(?![A-Za-z0-9_-])"
)

EMAIL_ADDRESS_RE = re.compile(
    r"(?i)(?<![A-Z0-9._%+-])[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}(?![A-Z0-9.-])"
)

DRIVE_CONTEXT_RE = re.compile(
    r"(?i)\b(?:(?:google\s+)?drive|google[\s-]+doc(?:ument)?s?|folder)\b"
)
HASH_CONTEXT_RE = re.compile(r"(?i)\b(?:sha(?:-?256)?|hash|digest|checksum)\b")
DRIVE_URL_RE = re.compile(
    r"https?://(?:drive|docs)\.google\.com/[A-Za-z0-9_?&=/#.%:+-]*",
    re.IGNORECASE,
)

PUBLIC_TOKEN_RE = re.compile(
    rf"{TOKEN_PREFIX}-(?:GM|GD|EM)-[0-9A-F]{{{TOKEN_DIGEST_CHARS}}}"
)

PUBLIC_LINK_REPLACEMENTS: dict[str, tuple[tuple[str, str | None], ...]] = {
    "en/community-instrumentalisation/index.html": (
        (
            "view the 29 April 2008 minutes",
            "/en/community-instrumentalisation/acta-document-room/2008-04-29/",
        ),
        ("Order 804/2018", None),
    ),
    "es/comunidad-instrumentalizacion/index.html": (
        (
            "ver el acta de 29 de abril de 2008",
            "/es/comunidad-instrumentalizacion/sala-documental-actas/2008-04-29/",
        ),
        ("Auto 804/2018", None),
    ),
    "en/ric-private-equity-sun-park/index.html": (
        (
            "collective resolution of 29 April 2008",
            "/en/community-instrumentalisation/acta-document-room/2008-04-29/",
        ),
        ("Order 804/2018", None),
        ("12 May 2017 email", None),
        (
            "4 June 2014 · GE-014212/2014",
            "/en/cabildo-lanzarote-tourism-traceability/",
        ),
    ),
    "es/ric-private-equity-sun-park/index.html": (
        (
            "acuerdo colectivo de 29 de abril de 2008",
            "/es/comunidad-instrumentalizacion/sala-documental-actas/2008-04-29/",
        ),
        ("Auto 804/2018", None),
        ("correo de 12 de mayo de 2017", None),
        (
            "4 junio 2014 · GE-014212/2014",
            "/es/cabildo-lanzarote-turismo-trazabilidad/",
        ),
    ),
}

PUBLIC_MARKDOWN_LINK_REPLACEMENTS: dict[
    str, tuple[tuple[str, str | None], ...]
] = {
    "INSTITUTIONAL_ACTIONS.md": (
        (
            "29 April 2008 owners’ resolution",
            "en/community-instrumentalisation/acta-document-room/2008-04-29/",
        ),
        (
            "4 June 2014 filing GE-014212/2014",
            "en/cabildo-lanzarote-tourism-traceability/",
        ),
        (
            "Cabildo Resolution 2026-2735 / file 614/2026",
            "en/cabildo-lanzarote-tourism-traceability/",
        ),
        (
            "Order 804/2018",
            "en/ric-private-equity-sun-park/#order-804-2018-pink-cessation",
        ),
    ),
}


@dataclass(frozen=True)
class LocatorOccurrence:
    """One raw public occurrence and its normalized private locator."""

    locator_kind: str
    private_locator: str
    matched_text: str
    public_token: str


def controlled_text_targets() -> list[Path]:
    """Return tracked ACTA/public-room text surfaces in deterministic order."""

    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=REPO_ROOT,
        check=True,
        stdout=subprocess.PIPE,
    )
    targets: list[Path] = []
    for raw in result.stdout.split(b"\0"):
        if not raw:
            continue
        relative = Path(os.fsdecode(raw))
        if relative.suffix.lower() not in TEXT_SUFFIXES:
            continue
        posix = relative.as_posix()
        lower = posix.lower()
        if lower.startswith("scripts/") or lower.startswith(".github/"):
            continue
        if (
            "acta" in lower
            or lower.startswith("en/community-instrumentalisation/")
            or lower.startswith("es/comunidad-instrumentalizacion/")
            or posix in ADDITIONAL_PUBLIC_PRIVACY_TARGETS
        ):
            targets.append(REPO_ROOT / relative)
    return sorted(targets)


def _line_context(text: str, start: int, end: int) -> tuple[str, str]:
    line_start = text.rfind("\n", 0, start) + 1
    line_end = text.find("\n", end)
    if line_end < 0:
        line_end = len(text)
    return text[line_start:start], text[end:line_end]


def _drive_label_precedes(prefix: str) -> bool:
    """Accept a Drive-labelled value, but reject SHA/hash abbreviations."""

    matches = list(DRIVE_CONTEXT_RE.finditer(prefix))
    if not matches:
        return False
    after_label = prefix[matches[-1].end() :]
    if len(after_label) > 240:
        return False
    return HASH_CONTEXT_RE.search(after_label) is None


def _gmail_label_precedes(prefix: str) -> bool:
    """Accept a message/thread-labelled value, not a labelled checksum."""

    matches = list(GMAIL_CONTEXT_RE.finditer(prefix))
    if not matches:
        return False
    after_label = prefix[matches[-1].end() :]
    if len(after_label) > 160:
        return False
    return HASH_CONTEXT_RE.search(after_label) is None


def _gmail_label_nearby(prefix: str, suffix: str) -> bool:
    """Accept a Gmail/message label immediately before or after a row value."""

    if _gmail_label_precedes(prefix):
        return True
    match = GMAIL_CONTEXT_RE.search(suffix)
    if match is None or match.start() > 160:
        return False
    return HASH_CONTEXT_RE.search(suffix[: match.end()]) is None


def replace_known_public_links(path: Path, text: str) -> str:
    """Route live pages to public derivatives or render private links as text."""

    try:
        relative = path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return text
    remediated = text
    for anchor_text, public_href in PUBLIC_LINK_REPLACEMENTS.get(relative, ()):
        pattern = re.compile(
            r'<a\b[^>]*href="https?://(?:drive|docs)\.google\.com/[^"]+"[^>]*>'
            + re.escape(anchor_text)
            + r"</a>",
            re.IGNORECASE,
        )
        replacement = (
            anchor_text
            if public_href is None
            else f'<a href="{public_href}">{anchor_text}</a>'
        )
        remediated, replacement_count = pattern.subn(replacement, remediated)
        if replacement_count > 1:
            raise RuntimeError(
                f"unexpected duplicate private provider link for {relative}"
            )
    for anchor_text, public_href in PUBLIC_MARKDOWN_LINK_REPLACEMENTS.get(
        relative, ()
    ):
        pattern = re.compile(
            r"\["
            + re.escape(anchor_text)
            + r"\]\(https?://(?:drive|docs)\.google\.com/[^)]+\)",
            re.IGNORECASE,
        )
        replacement = (
            anchor_text
            if public_href is None
            else f"[{anchor_text}]({public_href})"
        )
        remediated, replacement_count = pattern.subn(replacement, remediated)
        if replacement_count > 1:
            raise RuntimeError(
                f"unexpected duplicate private provider link for {relative}"
            )
    return remediated


def _scoped_line_markers(path: Path) -> tuple[str, ...]:
    try:
        relative = path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return ()
    return SCOPED_LINE_MARKERS.get(relative, ())


def discover_for_path(path: Path, text: str) -> list[LocatorOccurrence]:
    """Discover locators within the whole target or its enumerated rows."""

    markers = _scoped_line_markers(path)
    if not markers:
        found = discover(text)
        try:
            relative = path.relative_to(REPO_ROOT).as_posix()
        except ValueError:
            relative = ""
        if relative in BARE_GMAIL_ID_TARGETS:
            known_spans = {
                (occurrence.locator_kind, occurrence.private_locator)
                for occurrence in found
            }
            for match in GMAIL_MESSAGE_ID_RE.finditer(text):
                value = match.group(0)
                if ("gmail_message_id", value) in known_spans:
                    continue
                prefix, suffix = _line_context(text, match.start(), match.end())
                if HASH_CONTEXT_RE.search(prefix + suffix):
                    continue
                found.append(
                    LocatorOccurrence(
                        "gmail_message_id",
                        value,
                        value,
                        token_for("gmail_message_id", value),
                    )
                )
        if relative in PRIVATE_EMAIL_TARGETS:
            known_emails = {
                occurrence.private_locator
                for occurrence in found
                if occurrence.locator_kind == "email_address"
            }
            for match in EMAIL_ADDRESS_RE.finditer(text):
                value = match.group(0)
                if value in known_emails:
                    continue
                found.append(
                    LocatorOccurrence(
                        "email_address",
                        value,
                        value,
                        token_for("email_address", value),
                    )
                )
        return found
    found: list[LocatorOccurrence] = []
    for line in text.splitlines(keepends=True):
        if any(marker in line for marker in markers):
            found.extend(discover(line))
    return found


def replace_locators_for_path(
    path: Path, text: str
) -> tuple[str, list[LocatorOccurrence]]:
    """Replace only the controlled rows when a target has a bounded scope."""

    markers = _scoped_line_markers(path)
    if not markers:
        return replace_discovered_locators(text, discover_for_path(path, text))
    occurrences: list[LocatorOccurrence] = []
    remediated_lines: list[str] = []
    for line in text.splitlines(keepends=True):
        if any(marker in line for marker in markers):
            line, line_occurrences = replace_locators(line)
            occurrences.extend(line_occurrences)
        remediated_lines.append(line)
    return "".join(remediated_lines), occurrences


def token_for(locator_kind: str, private_locator: str) -> str:
    """Return the stable, one-way public token for a private locator."""

    kind_code = {
        "gmail_message_id": "GM",
        "google_drive_file_id": "GD",
        "email_address": "EM",
    }[locator_kind]
    material = (
        TOKEN_DOMAIN.encode("utf-8")
        + b"\x00"
        + locator_kind.encode("ascii")
        + b"\x00"
        + private_locator.encode("utf-8")
    )
    digest = hashlib.sha256(material).hexdigest().upper()[:TOKEN_DIGEST_CHARS]
    return f"{TOKEN_PREFIX}-{kind_code}-{digest}"


def discover(text: str) -> list[LocatorOccurrence]:
    """Return context-verified raw provider locator occurrences."""

    found: list[LocatorOccurrence] = []
    provider_url_spans: list[tuple[int, int]] = []

    for match in DRIVE_URL_RE.finditer(text):
        provider_url = match.group(0)
        id_matches = list(DRIVE_FILE_ID_RE.finditer(provider_url))
        if len(id_matches) != 1:
            # A raw provider URL is unsafe even if an unfamiliar URL shape
            # prevents automatic replacement. Keep an explicit sentinel that
            # makes --check fail without exposing the URL in output.
            found.append(
                LocatorOccurrence(
                    "unresolved_provider_url",
                    provider_url,
                    provider_url,
                    "",
                )
            )
            provider_url_spans.append(match.span())
            continue
        private_locator = id_matches[0].group(0)
        found.append(
            LocatorOccurrence(
                "google_drive_file_id",
                private_locator,
                provider_url,
                token_for("google_drive_file_id", private_locator),
            )
        )
        provider_url_spans.append(match.span())

    def inside_provider_url(start: int, end: int) -> bool:
        return any(start >= left and end <= right for left, right in provider_url_spans)

    for match in GMAIL_MESSAGE_ID_RE.finditer(text):
        value = match.group(0)
        prefix, suffix = _line_context(text, match.start(), match.end())
        if not _gmail_label_nearby(prefix, suffix):
            continue
        found.append(
            LocatorOccurrence(
                "gmail_message_id",
                value,
                value,
                token_for("gmail_message_id", value),
            )
        )

    for pattern in (DRIVE_FILE_ID_RE, DRIVE_FRAGMENT_RE):
        for match in pattern.finditer(text):
            if inside_provider_url(match.start(), match.end()):
                continue
            value = match.group(0)
            if PUBLIC_TOKEN_RE.fullmatch(value):
                continue
            prefix, _suffix = _line_context(text, match.start(), match.end())
            if pattern is DRIVE_FILE_ID_RE:
                # Some archival controls put the explicit "Drive source:"
                # label on the preceding line and the locator alone on the
                # next non-empty line. A bounded backwards window covers that
                # format without treating distant prose as locator context.
                prefix = text[max(0, match.start() - 240) : match.start()]
            if not _drive_label_precedes(prefix):
                continue
            found.append(
                LocatorOccurrence(
                    "google_drive_file_id",
                    value,
                    value,
                    token_for("google_drive_file_id", value),
                )
            )
    return found


def replace_discovered_locators(
    text: str, occurrences: list[LocatorOccurrence]
) -> tuple[str, list[LocatorOccurrence]]:
    """Replace a previously bounded locator set and return its metadata."""

    token_owner: dict[str, tuple[str, str]] = {}
    for occurrence in occurrences:
        if occurrence.locator_kind == "unresolved_provider_url":
            raise RuntimeError(
                "raw provider URL has no single recognizable Drive ID; manual remediation required"
            )
        owner = token_owner.setdefault(
            occurrence.public_token,
            (occurrence.locator_kind, occurrence.private_locator),
        )
        if owner != (occurrence.locator_kind, occurrence.private_locator):
            raise RuntimeError("public-token collision; increase TOKEN_DIGEST_CHARS")

    remediated = text
    # Longer matched values first ensures a whole provider URL is replaced
    # before a standalone copy of its normalized file ID.
    unique = sorted(
        {
            (
                occurrence.matched_text,
                occurrence.public_token,
                occurrence.locator_kind,
                occurrence.private_locator,
            )
            for occurrence in occurrences
        },
        key=lambda item: (-len(item[0]), item[2], item[3]),
    )
    for matched_text, public_token, _kind, _private_locator in unique:
        remediated = remediated.replace(matched_text, public_token)
    return remediated, occurrences


def replace_locators(text: str) -> tuple[str, list[LocatorOccurrence]]:
    """Replace every controlled raw locator and return occurrence metadata."""

    return replace_discovered_locators(text, discover(text))


def is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def mapping_payload(
    occurrences: list[LocatorOccurrence],
    source_paths: list[Path],
) -> dict[str, Any]:
    counts = Counter(
        (
            occurrence.locator_kind,
            occurrence.private_locator,
            occurrence.public_token,
        )
        for occurrence in occurrences
    )
    entries = []
    for (kind, private_locator, public_token), occurrence_count in sorted(
        counts.items(), key=lambda item: item[0][2]
    ):
        entries.append(
            {
                "public_token": public_token,
                "locator_kind": kind,
                "locator_completeness": (
                    "partial" if private_locator.endswith("…") else "complete"
                ),
                "private_locator": private_locator,
                "occurrence_count": occurrence_count,
            }
        )
    return {
        "schema_version": "1.0",
        "classification": "PRIVATE_CUSTODY_DO_NOT_COMMIT",
        "source_register": str(REGISTER.relative_to(REPO_ROOT)),
        "source_scope": [
            str(path.relative_to(REPO_ROOT)) for path in sorted(set(source_paths))
        ],
        "public_token_scheme": {
            "name": "SP-PRV-LCTR-v1",
            "algorithm": "SHA-256",
            "domain_separator": TOKEN_DOMAIN,
            "digest_hex_characters": TOKEN_DIGEST_CHARS,
            "format": f"{TOKEN_PREFIX}-<GM|GD>-<digest>",
        },
        "entries": entries,
    }


def load_existing_mapping(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError("existing private mapping is unreadable or invalid") from exc
    if payload.get("classification") != "PRIVATE_CUSTODY_DO_NOT_COMMIT":
        raise RuntimeError("existing private mapping has an unexpected classification")
    if not isinstance(payload.get("entries"), list):
        raise RuntimeError("existing private mapping has no valid entries array")
    return payload


def merge_mapping(existing: dict[str, Any] | None, new: dict[str, Any]) -> dict[str, Any]:
    if existing is None:
        return new

    merged_by_token: dict[str, dict[str, Any]] = {}
    for entry in existing["entries"] + new["entries"]:
        token = entry.get("public_token")
        if not isinstance(token, str) or not PUBLIC_TOKEN_RE.fullmatch(token):
            raise RuntimeError("private mapping contains an invalid public token")
        prior = merged_by_token.get(token)
        if prior is not None:
            identity_fields = ("locator_kind", "private_locator", "locator_completeness")
            if any(prior.get(field) != entry.get(field) for field in identity_fields):
                raise RuntimeError("private mapping contains a public-token collision")
            prior["occurrence_count"] = max(
                int(prior.get("occurrence_count", 0)),
                int(entry.get("occurrence_count", 0)),
            )
        else:
            merged_by_token[token] = dict(entry)

    merged = dict(new)
    merged["entries"] = [merged_by_token[token] for token in sorted(merged_by_token)]
    return merged


def write_private_mapping(path: Path, payload: dict[str, Any]) -> bool:
    resolved = path.expanduser().resolve()
    if is_within(resolved, REPO_ROOT.resolve()):
        raise RuntimeError("private mapping path must be outside the Git repository")

    existing = load_existing_mapping(resolved)
    merged = merge_mapping(existing, payload)
    rendered = json.dumps(merged, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if existing is not None and resolved.read_text(encoding="utf-8") == rendered:
        os.chmod(resolved, 0o600)
        return False

    resolved.parent.mkdir(parents=True, exist_ok=True)
    temporary = resolved.with_name(f".{resolved.name}.tmp-{os.getpid()}")
    descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(rendered)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, resolved)
        os.chmod(resolved, 0o600)
    finally:
        if temporary.exists():
            temporary.unlink()
    return True


def summary(occurrences: list[LocatorOccurrence]) -> str:
    occurrence_counts = Counter(item.locator_kind for item in occurrences)
    unique_counts = Counter(
        (item.locator_kind, item.public_token) for item in occurrences
    )
    unique_by_kind = Counter(kind for kind, _token in unique_counts)
    return (
        f"occurrences={len(occurrences)}; unique_tokens={len(unique_counts)}; "
        f"gmail_occurrences={occurrence_counts['gmail_message_id']}; "
        f"gmail_tokens={unique_by_kind['gmail_message_id']}; "
        f"drive_occurrences={occurrence_counts['google_drive_file_id']}; "
        f"drive_tokens={unique_by_kind['google_drive_file_id']}; "
        f"email_occurrences={occurrence_counts['email_address']}; "
        f"email_tokens={unique_by_kind['email_address']}"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="make no changes; fail if any raw provider locator remains",
    )
    parser.add_argument(
        "--mapping-out",
        type=Path,
        help="write/merge a reversible private mapping JSON outside Git",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.check and args.mapping_out is not None:
        print("ERROR: --check and --mapping-out cannot be combined", file=sys.stderr)
        return 2

    targets = controlled_text_targets()
    occurrences: list[LocatorOccurrence] = []
    per_file: list[tuple[Path, str, str, list[LocatorOccurrence]]] = []
    for path in targets:
        original = path.read_text(encoding="utf-8")
        if args.check:
            file_occurrences = discover_for_path(path, original)
            remediated = original
        else:
            link_safe = replace_known_public_links(path, original)
            remediated, file_occurrences = replace_locators_for_path(
                path, link_safe
            )
        occurrences.extend(file_occurrences)
        per_file.append((path, original, remediated, file_occurrences))

    if args.check:
        if occurrences:
            affected = sum(bool(items) for _path, _old, _new, items in per_file)
            print(
                "FAIL: raw ACTA provider locators remain; "
                f"files={affected}; {summary(occurrences)}"
            )
            return 1
        print(
            "PASS: no context-verified raw Gmail IDs, Google Drive IDs or "
            f"provider URLs detected across {len(targets)} controlled ACTA text files"
        )
        return 0

    if occurrences and args.mapping_out is None:
        print(
            "ERROR: remediation requires --mapping-out outside Git so the private "
            "reverse correlation is preserved",
            file=sys.stderr,
        )
        return 2

    affected_paths = [
        path for path, original, remediated, _items in per_file if remediated != original
    ]
    if args.mapping_out is not None and occurrences:
        changed = write_private_mapping(
            args.mapping_out,
            mapping_payload(occurrences, affected_paths),
        )
        state = "updated" if changed else "unchanged"
        print(
            f"Private mapping {state}; "
            f"entries={len(set(item.public_token for item in occurrences))}"
        )
    elif args.mapping_out is not None:
        print("Private mapping unchanged; no raw locators were available to map")

    if not affected_paths:
        print("Controlled ACTA text unchanged; no raw provider locators detected")
        return 0

    for path, original, remediated, _items in per_file:
        if remediated != original:
            path.write_text(remediated, encoding="utf-8")

    residual: list[LocatorOccurrence] = []
    for path in targets:
        residual.extend(
            discover_for_path(path, path.read_text(encoding="utf-8"))
        )
    if residual:
        print(
            "ERROR: post-write ACTA provider-locator check failed; "
            f"{summary(residual)}",
            file=sys.stderr,
        )
        return 1

    print(
        f"Controlled ACTA text remediated; files={len(affected_paths)}; "
        f"{summary(occurrences)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
