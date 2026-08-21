#!/usr/bin/env python3
"""Prevent unqualified whole-hotel insolvency shorthand from returning."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_ROOTS = (ROOT / "en", ROOT / "es", ROOT / "assets")
SUFFIXES = {".html", ".js", ".svg"}

FORBIDDEN = (
    "lpb was insolvent",
    "lpb era insolvente",
    "the insolvent hotel",
    "the hotel was insolvent",
    "el hotel era insolvente",
    "sun park insolvency life",
    "vida concursal de sun park",
    "the same hotel’s insolvency and investor lives",
    "the same hotel's insolvency and investor lives",
    "la vida concursal y la vida inversora del mismo hotel",
)

CANONICAL = {
    ROOT / "en" / "lpb-insolvency" / "index.html": (
        "LPB as the only debtor",
        "not 100% of Sun Park",
        "Not: “Sun Park was insolvent”",
    ),
    ROOT / "es" / "insolvencia-lpb" / "index.html": (
        "LPB como única deudora",
        "no del 100% de Sun Park",
        "No: “Sun Park estaba en concurso”",
    ),
}


def public_files() -> list[Path]:
    files: list[Path] = []
    for root in PUBLIC_ROOTS:
        files.extend(path for path in root.rglob("*") if path.suffix.lower() in SUFFIXES)
    return sorted(files)


def main() -> int:
    errors: list[str] = []

    for path in public_files():
        text = path.read_text(encoding="utf-8", errors="replace")
        lower = text.lower()
        for phrase in FORBIDDEN:
            if phrase in lower:
                errors.append(f"{path.relative_to(ROOT)}: forbidden unqualified wording {phrase!r}")

    for path, markers in CANONICAL.items():
        if not path.is_file():
            errors.append(f"missing canonical insolvency-perimeter page: {path.relative_to(ROOT)}")
            continue
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                errors.append(f"{path.relative_to(ROOT)}: canonical marker missing: {marker!r}")

    if errors:
        print("INSOLVENCY-PERIMETER LANGUAGE GATE: FAIL")
        for item in errors:
            print(f" - {item}")
        return 1

    print(f"INSOLVENCY-PERIMETER LANGUAGE GATE: PASS ({len(public_files())} public files inspected)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
