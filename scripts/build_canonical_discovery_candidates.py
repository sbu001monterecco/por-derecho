#!/usr/bin/env python3
"""Build a public-safe review queue of names/entities not in the canonical registry.

Discovery is deliberately separated from canonical admission. The report is a
review artifact: it never allocates IDs and never infers client, mandate,
knowledge, intent, control, wrongdoing or liability.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import unicodedata
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "assets/data/matter-identity-registry-v1.json"
DEFAULT_OUTPUT = ROOT / "artifacts/canonical-discovery/repository-candidates-generated.json"

TEXT_SUFFIXES = {".html", ".htm", ".md", ".txt", ".json", ".csv", ".js", ".mjs"}
SKIP_PARTS = {
    ".git", "node_modules", "vendor", "artifacts", "coverage", "dist", "build",
    "resolution-pages-public-redacted", "screenshots", "playwright-report",
}
STRONG_SOURCE_PARTS = {"evidence", "archive", "data", "publication-manifests", "ops"}

PARTICLES = {"de", "del", "la", "las", "los", "y", "da", "do", "dos", "van", "der", "von"}
TITLE_WORDS = {
    "Sr", "Sra", "D", "Dª", "Don", "Doña", "Dr", "Dra", "Ilmo", "Ilma",
    "Magistrado", "Juez", "Fiscal", "Abogado", "Procurador", "Procuradora",
}
COMMON_FALSE = {
    "Project Sun Rock", "Por Derecho", "Sun Park", "Google Drive", "GitHub Pages",
    "Legal Tech", "LegalTech", "Canary Islands", "Islas Canarias", "Las Palmas",
    "Gran Canaria", "Playa Blanca", "San Cristóbal", "La Laguna", "Santa Cruz",
    "Audiencia Provincial", "Tribunal Supremo", "Ministerio Fiscal", "Guardia Civil",
    "Policía Nacional", "Administración Concursal", "Administrador Concursal",
    "Registro Mercantil", "Registro Público", "Comisión Nacional", "Gobierno Canarias",
    "English Translation", "Spanish Original", "Public Record", "Open Evidence",
    "Source Status", "Current Status", "Evidence Register", "Master Register",
    "Documentary Record", "Legal Boundary", "Publication Boundary", "Right Reply",
}

PERSON_RE = re.compile(
    r"(?<![\w@])(?:D\.?|Dª\.?|Don|Doña|Sr\.?|Sra\.?)?\s*"
    r"([A-ZÁÉÍÓÚÜÑ][a-záéíóúüñ]+(?:[-'][A-ZÁÉÍÓÚÜÑ]?[a-záéíóúüñ]+)?"
    r"(?:\s+(?:de|del|la|las|los|y|da|do|dos|van|der|von))?"
    r"(?:\s+[A-ZÁÉÍÓÚÜÑ][a-záéíóúüñ]+(?:[-'][A-ZÁÉÍÓÚÜÑ]?[a-záéíóúüñ]+)?){1,4})"
)
ALL_CAPS_PERSON_RE = re.compile(
    r"(?<![\w@])(?:D\.?|Dª\.?)?\s*([A-ZÁÉÍÓÚÜÑ]{2,}(?:\s+(?:DE|DEL|LA|LAS|LOS|Y))?"
    r"(?:\s+[A-ZÁÉÍÓÚÜÑ]{2,}){1,4})(?![\w@])"
)
ORG_RE = re.compile(
    r"(?<![\w@])([A-ZÁÉÍÓÚÜÑ][A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9&'().,\- ]{2,90}?\s+"
    r"(?:S\.?\s*L\.?\s*U?\.?|S\.?\s*A\.?\s*U?\.?|S\.?\s*L\.?\s*P\.?|S\.?\s*C\.?\s*R\.?|"
    r"B\.?\s*V\.?|L\.?\s*P\.?|L\.?\s*L\.?\s*P\.?|Limited|Ltd\.?|Socimi|SCR))(?!\w)",
    re.IGNORECASE,
)
EMAIL_RE = re.compile(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"(?<!\w)(?:\+?\d[\d .()/-]{7,}\d)(?!\w)")
UUID_RE = re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I)
HTML_TAG_RE = re.compile(r"<[^>]+>")
SCRIPT_RE = re.compile(r"<(script|style)\b[^>]*>.*?</\1>", re.I | re.S)
WHITESPACE_RE = re.compile(r"\s+")


def norm(value: str) -> str:
    value = unicodedata.normalize("NFD", value or "")
    value = "".join(ch for ch in value if unicodedata.category(ch) != "Mn")
    value = value.lower().replace("–", "-").replace("—", "-")
    value = re.sub(r"\b(s\.?l\.?u?|s\.?a\.?u?|s\.?l\.?p|s\.?c\.?r|b\.?v|l\.?p|ltd|limited)\b", " ", value)
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return WHITESPACE_RE.sub(" ", value).strip()


def safe_context(text: str, start: int, end: int, width: int = 150) -> str:
    left = max(0, start - width)
    right = min(len(text), end + width)
    value = text[left:right]
    value = EMAIL_RE.sub("[email redacted]", value)
    value = PHONE_RE.sub("[number redacted]", value)
    value = UUID_RE.sub("[identifier redacted]", value)
    value = re.sub(r"https?://\S+", "[url]", value)
    return WHITESPACE_RE.sub(" ", value).strip()[:360]


def visible_text(path: Path, raw: str) -> str:
    if path.suffix.lower() in {".html", ".htm"}:
        raw = SCRIPT_RE.sub(" ", raw)
        raw = HTML_TAG_RE.sub(" ", raw)
    elif path.suffix.lower() == ".json":
        try:
            raw = " ".join(str(v) for v in flatten(json.loads(raw)))
        except (ValueError, TypeError):
            pass
    return WHITESPACE_RE.sub(" ", raw)


def flatten(value: object) -> Iterable[object]:
    if isinstance(value, dict):
        for item in value.values():
            yield from flatten(item)
    elif isinstance(value, list):
        for item in value:
            yield from flatten(item)
    elif isinstance(value, (str, int, float)):
        yield value


def tracked_files() -> list[Path]:
    try:
        output = subprocess.check_output(["git", "-C", str(ROOT), "ls-files", "-z"], stderr=subprocess.DEVNULL)
        paths = [ROOT / item.decode("utf-8", "replace") for item in output.split(b"\0") if item]
    except (OSError, subprocess.CalledProcessError):
        paths = list(ROOT.rglob("*"))
    result: list[Path] = []
    for path in paths:
        try:
            rel = path.relative_to(ROOT)
        except ValueError:
            continue
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if any(part in SKIP_PARTS for part in rel.parts):
            continue
        try:
            if path.stat().st_size > 2_000_000:
                continue
        except OSError:
            continue
        result.append(path)
    return result


def load_registry() -> tuple[set[str], dict[str, str]]:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    known: set[str] = set()
    ids: dict[str, str] = {}
    for part in data.get("parts", []):
        path = REGISTRY.parent / part["path"]
        shard = json.loads(path.read_text(encoding="utf-8"))
        for record in shard.get("records", []):
            record_id = str(record.get("id", ""))
            for value in [record.get("name"), *(record.get("aliases") or []), *(record.get("legacy_ambiguous_aliases") or [])]:
                if value:
                    key = norm(str(value))
                    known.add(key)
                    ids[key] = record_id
    return known, ids


def clean_person(value: str) -> str | None:
    value = WHITESPACE_RE.sub(" ", value).strip(" .,:;–—-()[]{}\"'")
    words = value.split()
    if len(words) < 2 or len(words) > 7:
        return None
    while words and words[0].rstrip(".") in TITLE_WORDS:
        words.pop(0)
    if len(words) < 2:
        return None
    value = " ".join(words)
    if value in COMMON_FALSE or norm(value) in {norm(item) for item in COMMON_FALSE}:
        return None
    content_words = [w for w in words if w.lower() not in PARTICLES]
    if len(content_words) < 2 or any(len(w) == 1 and not w.endswith(".") for w in content_words):
        return None
    if sum(ch.isdigit() for ch in value):
        return None
    return value


def clean_org(value: str) -> str | None:
    value = WHITESPACE_RE.sub(" ", value).strip(" .,:;–—-()[]{}\"'")
    if len(value) < 5 or len(value) > 110:
        return None
    return value


@dataclass
class Candidate:
    label: str
    kind: str
    paths: set[str] = field(default_factory=set)
    contexts: list[dict[str, str]] = field(default_factory=list)
    occurrences: int = 0
    strong_source_hits: int = 0

    def add(self, rel: str, context: str) -> None:
        self.paths.add(rel)
        self.occurrences += 1
        if any(part in Path(rel).parts for part in STRONG_SOURCE_PARTS):
            self.strong_source_hits += 1
        if len(self.contexts) < 3 and context and all(context != row["context"] for row in self.contexts):
            self.contexts.append({"path": rel, "context": context})

    def confidence(self) -> str:
        if self.strong_source_hits >= 2 or len(self.paths) >= 5:
            return "HIGH_REVIEW_PRIORITY"
        if self.strong_source_hits >= 1 or len(self.paths) >= 2:
            return "MEDIUM_REVIEW_PRIORITY"
        return "LOW_REVIEW_PRIORITY"


def scan() -> dict[str, object]:
    known, known_ids = load_registry()
    candidates: dict[tuple[str, str], Candidate] = {}
    files_scanned = 0
    bytes_scanned = 0

    for path in tracked_files():
        try:
            raw = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        rel = path.relative_to(ROOT).as_posix()
        text = visible_text(path, raw)
        files_scanned += 1
        bytes_scanned += len(raw.encode("utf-8", "replace"))

        for regex, kind, cleaner in ((PERSON_RE, "PERSON", clean_person), (ALL_CAPS_PERSON_RE, "PERSON", clean_person), (ORG_RE, "ORGANISATION", clean_org)):
            for match in regex.finditer(text):
                label = cleaner(match.group(1))
                if not label:
                    continue
                key = norm(label)
                if not key or key in known:
                    continue
                # Suppress very broad title-like two-word phrases unless they recur.
                item = candidates.setdefault((kind, key), Candidate(label=label, kind=kind))
                item.add(rel, safe_context(text, match.start(1), match.end(1)))

    rows = []
    for (kind, key), candidate in candidates.items():
        if len(candidate.paths) < 2 and candidate.strong_source_hits < 1:
            continue
        # Exclude near-exact canonical variations; retain the mapping in diagnostics.
        near = [(name, record_id) for name, record_id in known_ids.items() if name and (name in key or key in name) and min(len(name), len(key)) >= 8]
        rows.append({
            "candidate_key": f"AUTO-{kind}-{abs(hash((kind, key))) % 10**10:010d}",
            "name": candidate.label,
            "normalized_name": key,
            "candidate_type": kind,
            "confidence": candidate.confidence(),
            "occurrences": candidate.occurrences,
            "distinct_paths": len(candidate.paths),
            "strong_source_hits": candidate.strong_source_hits,
            "paths": sorted(candidate.paths)[:20],
            "contexts": candidate.contexts,
            "possible_existing_identity": [{"normalized_alias": name, "canonical_id": record_id} for name, record_id in near[:5]],
            "decision": "REVIEW_REQUIRED",
            "publication_boundary": "Discovery only; identity, capacity, relationship, knowledge, intent and liability are not established."
        })

    rows.sort(key=lambda row: (
        {"HIGH_REVIEW_PRIORITY": 0, "MEDIUM_REVIEW_PRIORITY": 1, "LOW_REVIEW_PRIORITY": 2}[str(row["confidence"])],
        -int(row["distinct_paths"]), -int(row["occurrences"]), str(row["name"]).lower()
    ))
    return {
        "schema": "por-derecho.canonical-discovery.repository-scan.v1",
        "generated_at": date.today().isoformat(),
        "status": "DISCOVERY_ONLY_REVIEW_REQUIRED",
        "scanner": "scripts/build_canonical_discovery_candidates.py",
        "privacy": "Contexts are bounded and automatically redact email addresses, phone-like numbers, UUIDs and URLs.",
        "files_scanned": files_scanned,
        "bytes_scanned": bytes_scanned,
        "canonical_alias_count": len(known),
        "candidate_count": len(rows),
        "candidates": rows[:500],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--stdout", action="store_true")
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()

    report = scan()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.stdout:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    if args.summary or not args.stdout:
        print(
            "CANONICAL DISCOVERY SCAN: "
            f"{report['files_scanned']} files; {report['canonical_alias_count']} canonical aliases; "
            f"{report['candidate_count']} review candidates; output={args.output}"
        )
        for row in report["candidates"][:25]:
            print(f" - {row['confidence']}: {row['name']} ({row['candidate_type']}; {row['distinct_paths']} paths; {row['occurrences']} hits)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
