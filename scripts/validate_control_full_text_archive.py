#!/usr/bin/env python3
"""Validate completeness, integrity and public-redaction gates for the control archive."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "archive" / "controls"
MANIFEST = ARCHIVE / "master-manifest.json"

FORBIDDEN_PATTERNS = (
    (re.compile(r"\b(?:[XYZ][0-9]{7}[A-Z]|[0-9]{8}[A-Z])\b", re.I), "NIE/DNI"),
    (
        re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
        "email address",
    ),
    (
        re.compile(
            r"domicilio[^\n]{0,120}(?:\n\s*)?Calle\s+|"
            r"efectos de (?:comunicaciones|notificaciones) en Calle\s+",
            re.I,
        ),
        "personal service address",
    ),
    (
        re.compile(r"(?<!\d)(?:\+34[ -]?)?[6-9][0-9]{2}[ .-]?[0-9]{3}[ .-]?[0-9]{3}(?!\d)"),
        "telephone number",
    ),
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fail(message: str, failures: list[str]) -> None:
    failures.append(message)


def main() -> int:
    failures: list[str] = []
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if data.get("schema") != "por-derecho.control-full-text-manifest.v1":
        fail("unexpected manifest schema", failures)

    for item in data.get("documents", []):
        path = ARCHIVE / item["public_text"]
        if not path.is_file():
            fail(f"missing public text: {path.relative_to(ROOT)}", failures)
            continue
        actual_hash = sha256(path)
        if actual_hash != item["public_text_sha256"]:
            fail(
                f"public hash mismatch: {path.relative_to(ROOT)} "
                f"({actual_hash} != {item['public_text_sha256']})",
                failures,
            )

        text = path.read_text(encoding="utf-8")
        first, last = (int(value) for value in item["published_source_range"].split("-"))
        markers = [int(value) for value in re.findall(r"^## Página fuente (\d+) de \d+$", text, re.M)]
        expected = list(range(first, last + 1))
        if markers != expected:
            fail(f"page marker mismatch: {path.relative_to(ROOT)}", failures)
        if len(re.findall(r"^```", text, re.M)) != 2 * len(expected):
            fail(f"unbalanced page text fences: {path.relative_to(ROOT)}", failures)

        page_text = text.split("## Página fuente", 1)[-1]
        for pattern, label in FORBIDDEN_PATTERNS:
            if pattern.search(page_text):
                fail(f"unredacted {label} in {path.relative_to(ROOT)}", failures)

    forbidden_binaries = sorted(ARCHIVE.rglob("*.pdf")) + sorted(ARCHIVE.rglob("*.jpeg"))
    if forbidden_binaries:
        fail(
            "private-format binaries present under public control archive: "
            + ", ".join(str(path.relative_to(ROOT)) for path in forbidden_binaries),
            failures,
        )

    if failures:
        print("Control archive validation FAILED", file=sys.stderr)
        for message in failures:
            print(f"- {message}", file=sys.stderr)
        return 1
    print(f"Control archive validation passed: {len(data['documents'])} public texts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
