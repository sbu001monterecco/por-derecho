#!/usr/bin/env python3
"""Advisory, changed-lines-only guard for private sources, voice statements and OSINT."""

from __future__ import annotations

import argparse
import csv
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VOICE_PROTOCOL = "archive/declarations/VOICE_TO_TEXT_STATEMENT_OF_FACT_AND_TRUTH_PROTOCOL_25AUG2026.md"
MAIL_PROTOCOL = "archive/RESERVED_DECLARANT_PRIVATE_MAILBOX_ACQUISITION_AND_CUSTODY_PROTOCOL_25AUG2026.md"
OSINT_PROTOCOL = "archive/OPEN_SOURCE_INTELLIGENCE_NAMED_PERSON_ENTITY_PROTOCOL_25AUG2026.md"
OSINT_SCAN = "archive/CAMPANARIO_PRIETO_NORIEGA_COMMUNITY_CORPORATE_UNITARY_SCAN_25AUG2026.md"
RDC_REGISTER = "archive/GIL_RESERVED_DECLARANT_CONTRADICTION_CLARIFICATION_REGISTER_22AUG2026.md"


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def read(relative: str) -> str:
    path = ROOT / relative
    if not path.is_file():
        fail(f"missing required control: {relative}")
    return path.read_text(encoding="utf-8")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def git(*args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and result.returncode:
        fail(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout


def changed_paths(base: str) -> tuple[dict[str, str], dict[str, list[tuple[int, str, int]]]]:
    statuses: dict[str, str] = {}
    for raw in git("diff", "--name-status", "--find-renames", base, "--").splitlines():
        parts = raw.split("\t")
        if len(parts) < 2:
            continue
        status = parts[0]
        path = parts[-1]
        statuses[path] = status

    untracked = git("ls-files", "--others", "--exclude-standard").splitlines()
    for path in untracked:
        statuses[path] = "A"

    added: dict[str, list[tuple[int, str, int]]] = {path: [] for path in statuses}
    current: str | None = None
    target_line = 0
    hunk_id = 0
    in_hunk = False
    diff = git("diff", "--unified=0", "--no-color", base, "--")
    for line in diff.splitlines():
        if line.startswith("diff --git "):
            current = None
            in_hunk = False
        elif not in_hunk and line.startswith("+++ b/"):
            current = line[6:]
        elif current and line.startswith("@@"):
            match = re.search(r"\+(\d+)(?:,\d+)?", line)
            if not match:
                fail(f"cannot parse diff hunk header: {line}")
            target_line = int(match.group(1))
            hunk_id += 1
            in_hunk = True
        elif current and in_hunk and line.startswith("+"):
            added.setdefault(current, []).append((target_line, line[1:], hunk_id))
            target_line += 1
        elif current and in_hunk and line.startswith("-"):
            continue
        elif current and in_hunk and line.startswith(" "):
            target_line += 1

    for path in untracked:
        candidate = ROOT / path
        if candidate.is_file():
            try:
                added[path] = [
                    (number, line, 0)
                    for number, line in enumerate(candidate.read_text(encoding="utf-8").splitlines(), 1)
                ]
            except UnicodeDecodeError:
                added[path] = []
    return statuses, added


def provider_identifier_header(cell: str) -> bool:
    """Return true only for an explicit provider/message/thread ID column."""

    normalized = cell.strip().strip("`*_\"'")
    normalized = re.sub(r"(?<=[a-záéíóúñ])(?=[A-ZÁÉÍÓÚÑ])", " ", normalized)
    normalized = normalized.lower()
    normalized = re.sub(r"[._/-]+", " ", normalized)
    normalized = re.sub(r"\s+", " ", normalized).strip()
    identifier = r"(?:id|identifier|identificador)"
    object_name = r"(?:message|mensaje|thread|hilo|provider|proveedor|gmail)"
    qualifier = r"(?:gmail|provider|proveedor|email|correo)"
    return bool(
        re.fullmatch(rf"(?:{qualifier}\s+)?{object_name}\s+{identifier}", normalized)
        or re.fullmatch(rf"{identifier}(?:\s+(?:de|del))?\s+(?:{qualifier}\s+)?{object_name}", normalized)
    )


def provider_identifier_value(cell: str) -> bool:
    """Recognise the opaque hexadecimal IDs already covered by the inline rule."""

    value = cell.strip().strip("`*_\"'").strip()
    return bool(re.fullmatch(r"[0-9a-f]{16,32}", value, flags=re.I))


def markdown_cells(line: str) -> list[str] | None:
    stripped = line.strip()
    if "|" not in stripped:
        return None
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]
    cells = [cell.strip() for cell in re.split(r"(?<!\\)\|", stripped)]
    return cells if len(cells) >= 2 else None


def markdown_separator(cells: list[str] | None) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell.strip()) for cell in cells)


def csv_cells(line: str) -> list[str] | None:
    if "," not in line:
        return None
    try:
        cells = next(csv.reader([line]))
    except (csv.Error, StopIteration):
        return None
    return [cell.strip() for cell in cells] if len(cells) >= 2 else None


def tabular_provider_identifier_rows(source_lines: list[str], changed_line_numbers: set[int]) -> set[int]:
    findings: set[int] = set()
    markdown_columns: tuple[int, ...] = ()
    markdown_width = 0
    csv_columns: tuple[int, ...] = ()
    csv_width = 0

    for offset, line in enumerate(source_lines):
        number = offset + 1
        md_row = markdown_cells(line)
        md_next = markdown_cells(source_lines[offset + 1]) if offset + 1 < len(source_lines) else None

        if md_row is not None and markdown_separator(md_next):
            markdown_columns = tuple(index for index, cell in enumerate(md_row) if provider_identifier_header(cell))
            markdown_width = len(md_row)
        elif markdown_columns:
            if markdown_separator(md_row):
                pass
            elif md_row is None or len(md_row) != markdown_width:
                markdown_columns = ()
                markdown_width = 0
            elif number in changed_line_numbers and any(
                provider_identifier_value(md_row[index]) for index in markdown_columns
            ):
                findings.add(number)

        csv_row = csv_cells(line)
        header_columns = (
            tuple(index for index, cell in enumerate(csv_row) if provider_identifier_header(cell))
            if csv_row is not None
            else ()
        )
        if header_columns:
            csv_columns = header_columns
            csv_width = len(csv_row)
        elif csv_columns:
            if not line.strip() or csv_row is None or len(csv_row) != csv_width:
                csv_columns = ()
                csv_width = 0
            elif number in changed_line_numbers and any(
                provider_identifier_value(csv_row[index]) for index in csv_columns
            ):
                findings.add(number)

    return findings


def tabular_provider_identifier_lines(path: str, changed_line_numbers: set[int]) -> set[int]:
    """Find added table rows that expose an ID under an explicit ID header.

    The complete current text supplies table context, but only changed target
    lines can be reported. This catches a row added beneath an unchanged header
    without treating an unrelated hexadecimal value elsewhere as a provider ID.
    """

    candidate = ROOT / path
    if not changed_line_numbers or not candidate.is_file():
        return set()
    try:
        source_lines = candidate.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError:
        return set()
    return tabular_provider_identifier_rows(source_lines, changed_line_numbers)


def validate_control_documents() -> None:
    markers = {
        VOICE_PROTOCOL: (
            "regla de pausa",
            "no se mezclan voces",
            "adopción",
            "excluir audio bruto",
        ),
        MAIL_PROTOCOL: (
            "más de 2.400",
            "más del 90%",
            "Google Takeout",
            "la autorización para preservar o revisar",
            "autorización para publicar",
        ),
        OSINT_PROTOCOL: (
            "O1",
            "NO LOCALIZADO",
            "no significa inexistencia",
            "derecho de respuesta",
        ),
    }
    for relative, required in markers.items():
        body = read(relative)
        for marker in required:
            require(marker.lower() in body.lower(), f"{relative}: missing marker {marker!r}")

    for relative in ("AGENTS.md", "archive/declarations/README.md"):
        body = read(relative)
        require("VOICE_TO_TEXT_STATEMENT_OF_FACT_AND_TRUTH_PROTOCOL_25AUG2026.md" in body, f"{relative}: voice protocol link missing")
        require("OPEN_SOURCE_INTELLIGENCE_NAMED_PERSON_ENTITY_PROTOCOL_25AUG2026.md" in body, f"{relative}: OSINT protocol link missing")

    mail_links = (
        "AGENTS.md",
        "archive/declarations/README.md",
        "archive/EVIDENCE_CUSTODY_AND_PRESERVATION_PROTOCOL_16AUG2026.md",
        "archive/CHATGPT_CONTINUOUS_INTELLIGENCE_PROTOCOL_15AUG2026.md",
    )
    for relative in mail_links:
        require(
            "RESERVED_DECLARANT_PRIVATE_MAILBOX_ACQUISITION_AND_CUSTODY_PROTOCOL_25AUG2026.md" in read(relative),
            f"{relative}: private-mail protocol link missing",
        )

    require(
        "OPEN_SOURCE_INTELLIGENCE_NAMED_PERSON_ENTITY_PROTOCOL_25AUG2026.md"
        in read("archive/CHATGPT_CONTINUOUS_INTELLIGENCE_PROTOCOL_15AUG2026.md"),
        "continuous-intelligence protocol: OSINT protocol link missing",
    )


def validate_added_material(statuses: dict[str, str], added: dict[str, list[tuple[int, str, int]]]) -> None:
    sensitive_suffixes = {".eml", ".msg", ".mbox", ".pst"}
    audio_suffixes = {".aac", ".flac", ".m4a", ".mp3", ".ogg", ".opus", ".wav", ".webm"}
    encoded_suffixes = {".b64", ".bz2", ".gz", ".tgz", ".zip", ".7z"}

    for path, status in statuses.items():
        if status.startswith("D"):
            continue
        suffixes = {suffix.lower() for suffix in Path(path).suffixes}
        if suffixes & sensitive_suffixes:
            fail(f"private mail container must not be tracked: {path}")
        if suffixes & audio_suffixes:
            fail(f"audio payload requires a separately reviewed public-media route: {path}")
        if path.startswith(("archive/evidence/", "evidence/")) and (suffixes & encoded_suffixes):
            fail(f"encoded evidence payload must remain outside public Git: {path}")

    provider_context = r"(?:gmail|message|thread|provider|correo|mensaje|hilo)"
    provider_value = r"[0-9a-f]{16,32}"
    provider_id = re.compile(
        rf"(?:{provider_context}.{{0,40}}\b{provider_value}\b|\b{provider_value}\b.{{0,40}}{provider_context})",
        re.I,
    )
    raw_header = re.compile(
        r"^\s*(?:>|[-*]\s*)?(?:from|to|cc|bcc|reply-to|message-id|in-reply-to|references|authentication-results|dkim-signature|received):\s+\S+",
        re.I,
    )
    oauth_account = r"accounts" + r"\.google\.com/o/oauth"
    oauth_token = r"oauth2" + r"\.googleapis\.com"
    structured_secret = r"[\"']?(?:access_token|refresh_token|client_secret)[\"']?\s*[:=]\s*[\"']?\S+"
    bearer_secret = r"authorization\s*:\s*bearer\s+\S+"
    vendor_secrets = (
        r"\bAIza[0-9A-Za-z_-]{20,}",
        r"\bya29\.[0-9A-Za-z_-]+",
        r"\bghp_[0-9A-Za-z]{20,}",
        r"\bxox[baprs]-[0-9A-Za-z-]+",
    )
    auth_or_secret = re.compile(
        "(?:" + "|".join((oauth_account, oauth_token, structured_secret, bearer_secret, *vendor_secrets)) + ")",
        re.I,
    )
    private_gmail = re.compile(r"\b[A-Z0-9._%+-]+@gmail\.com\b", re.I)
    gmail_url = re.compile(r"mail\.google\.com/mail/(?:u/\d+/)?(?:#|\?)[^\s)\]]+", re.I)
    base64_line = re.compile(r"^[A-Za-z0-9+/]{48,}={0,2}$")
    hash_line = re.compile(r"(?:[0-9a-f]{64}|[0-9a-f]{128})", re.I)
    data_url = re.compile(r"data:[^;,\s]+(?:;[^,\s]+)*;base64,", re.I)

    for path, lines in added.items():
        table_provider_ids = tabular_provider_identifier_lines(path, {number for number, _line, _hunk in lines})
        encoded_run = 0
        previous_number: int | None = None
        previous_hunk: int | None = None
        for number, line, hunk_id in lines:
            if previous_number is None or number != previous_number + 1 or hunk_id != previous_hunk:
                encoded_run = 0
            if private_gmail.search(line):
                fail(f"personal Gmail address added at {path}:{number}")
            if raw_header.search(line):
                fail(f"raw mail header added at {path}:{number}")
            if auth_or_secret.search(line):
                fail(f"authentication URL or credential-like material added at {path}:{number}")
            if gmail_url.search(line):
                fail(f"Gmail access URL added at {path}:{number}")
            if provider_id.search(line) or number in table_provider_ids:
                fail(f"provider/message identifier added at {path}:{number}")
            if data_url.search(line):
                fail(f"base64 data URL added at {path}:{number}")
            stripped = line.strip()
            if base64_line.fullmatch(stripped) and not hash_line.fullmatch(stripped):
                encoded_run += len(stripped.rstrip("="))
            else:
                encoded_run = 0
            if encoded_run >= 512:
                fail(f"encoded payload added at {path}:{number}")
            previous_number = number
            previous_hunk = hunk_id


def validate_voice_declarations(statuses: dict[str, str]) -> None:
    declaration_pattern = re.compile(r"^archive/declarations/\d{3}_.+\.md$")
    voice_cues = ("voice", "audio", "dictado", "voz", "transcri")
    required_groups = (
        ("modo de fuente", "modalidad de fuente", "source mode"),
        ("estado de adopción", "adoption status", "ratific"),
        ("atribución", "attribution"),
    )
    for path, status in statuses.items():
        if status.startswith("D") or not declaration_pattern.match(path):
            continue
        body = read(path).lower()
        if not any(cue in body for cue in voice_cues):
            continue
        for alternatives in required_groups:
            require(any(marker in body for marker in alternatives), f"{path}: missing voice source/adoption field {alternatives}")

    declaration_011 = read(
        "archive/declarations/011_WITNESS_GIL_PERIMETER_CAMPANARIO_PRIETO_NORIEGA_COMMUNITY_NETWORK_20260825.md"
    )
    for marker in (
        "no ratificada palabra por palabra",
        "no existe certificación conjunta ni de verdad final",
        "constancia editorial no adoptada",
        "VOICE_TO_TEXT_STATEMENT_OF_FACT_AND_TRUTH_PROTOCOL_25AUG2026.md",
    ):
        require(marker.lower() in declaration_011.lower(), f"Declaration 011 missing unratified-voice control: {marker}")
    require(
        "\ndeclaro, en el sentido limitado" not in declaration_011.lower(),
        "Declaration 011 retains an active first-person truth clause despite unratified status",
    )


def validate_osint_and_rdc() -> None:
    scan = read(OSINT_SCAN).lower()
    for marker in (
        "registro reproducible",
        "aplicación parcial",
        "corpus finito",
        "25 de agosto de 2026",
        "sin coincidencia exacta",
        "no prueba ausencia",
        "límite obligatorio",
        "derecho de respuesta",
    ):
        require(marker in scan, f"OSINT scan missing bounded-search marker: {marker}")

    ids = re.findall(r"^\|\s*(RDC-\d+)\s*\|", read(RDC_REGISTER), flags=re.M)
    duplicates = sorted(identifier for identifier, count in Counter(ids).items() if count > 1)
    require(not duplicates, f"duplicate RDC row IDs: {', '.join(duplicates)}")
    for identifier in range(30, 44):
        require(f"RDC-{identifier}" in ids, f"missing clarification row RDC-{identifier}")


def validate_optional_public_receipt() -> None:
    relative = "archive/RESERVED_DECLARANT_GMAIL_ACCESS_CUSTODY_PUBLIC_RECEIPT_25AUG2026.md"
    path = ROOT / relative
    if not path.exists():
        return
    body = path.read_text(encoding="utf-8").lower()
    for marker in ("opaque", "access authority", "preservation authority", "publication authority"):
        require(marker in body, f"{relative}: missing safe receipt marker {marker!r}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="HEAD", help="Git revision against which added lines are audited")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    git("rev-parse", "--verify", args.base)
    statuses, added = changed_paths(args.base)
    validate_control_documents()
    validate_added_material(statuses, added)
    validate_voice_declarations(statuses)
    validate_osint_and_rdc()
    validate_optional_public_receipt()
    print("PASS: private-source, voice-statement and OSINT governance validated")


if __name__ == "__main__":
    main()
