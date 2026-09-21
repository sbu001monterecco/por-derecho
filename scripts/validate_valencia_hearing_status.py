#!/usr/bin/env python3
"""Lock the public-safe Valencia hearing chronology and reject superseded drift."""

from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "assets/data/valencia-hearing-status-v1.json"

EXPECTED = {
    ("proceeding", "court"): "Juzgado de Primera Instancia nº 27 de Valencia",
    ("proceeding", "number"): "1859/2023-9",
    ("proceeding", "nig"): "46250-42-1-2023-0049579",
    ("original_hearing", "date"): "2025-11-06",
    ("original_hearing", "time"): "10:00",
    ("relisted_hearing", "date"): "2027-01-28",
    ("relisted_hearing", "time"): "10:00",
}

REQUIRED = {
    "en/index.html": ("6 November 2025 at 10:00", "28 January 2027 at 10:00"),
    "es/index.html": ("6 de noviembre de 2025 a las 10:00", "28 de enero de 2027 a las 10:00"),
    "en/caixabank-valencia-claim/index.html": (
        "6 November 2025 at 10:00",
        "28 January 2027 at 10:00",
        "46250-42-1-2023-0049579",
        "cancelled flight the evening before",
    ),
    "es/reclamacion-caixabank-valencia/index.html": (
        "6 de noviembre de 2025 a las 10:00",
        "28 de enero de 2027 a las 10:00",
        "46250-42-1-2023-0049579",
        "cancelación de su vuelo la tarde anterior",
    ),
    "en/lender-of-record/index.html": ("6 November 2025 at 10:00", "28 January 2027 at 10:00"),
    "es/acreedor-de-registro/index.html": ("6 de noviembre de 2025 a las 10:00", "28 de enero de 2027 a las 10:00"),
    "assets/caixabank-borja-witness-context-20260816.js": (
        "6 November 2025 at 10:00",
        "28 January 2027 at 10:00",
        "6 de noviembre de 2025 a las 10:00",
        "28 de enero de 2027 a las 10:00",
    ),
    "en/updates/index.html": ("valencia-hearing-chronology-24aug", "28 January 2027 at 10:00"),
    "es/actualizaciones/index.html": ("cronologia-vista-valencia-24ago", "28 de enero de 2027 a las 10:00"),
}

FORBIDDEN = (
    "9 October 2026",
    "9 de octubre de 2026",
    "9-Oct-2026",
    "9 octubre 2026",
    "46250-42-1-2023-0057718",
    "Juzgado de Primera Instancia e Instrucción nº 27 de Valencia",
)

TEXT_SUFFIXES = {".html", ".js", ".json", ".md", ".xml", ".yml", ".yaml", ".txt", ".csv"}
SKIP_PARTS = {".git"}


def main() -> int:
    errors: list[str] = []
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    for path, expected in EXPECTED.items():
        actual = data[path[0]][path[1]]
        if actual != expected:
            errors.append(f"data {'.'.join(path)}: expected {expected!r}, got {actual!r}")

    for relative, markers in REQUIRED.items():
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"missing {relative}")
            continue
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                errors.append(f"{relative}: missing {marker!r}")

    scanned = 0
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if any(part in SKIP_PARTS for part in path.parts):
            continue
        if path.resolve() == Path(__file__).resolve():
            continue
        scanned += 1
        text = path.read_text(encoding="utf-8", errors="replace")
        for marker in FORBIDDEN:
            if marker in text:
                errors.append(f"{path.relative_to(ROOT)}: forbidden superseded marker {marker!r}")

    if errors:
        print("FAIL: Valencia hearing chronology")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print(f"PASS: Valencia hearing chronology locked across {scanned} repository text files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
