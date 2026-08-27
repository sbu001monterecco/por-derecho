#!/usr/bin/env python3
"""Create the public RICPE certificate derivative with its private ID removed."""

from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path

import fitz


PUBLIC_FINGERPRINT = "e53bda34973e530520bde39648768a1e32a358d8984294b21258789faebe6a24"
UUID_RE = re.compile(
    r"(?<![0-9a-f])[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-"
    r"[89ab][0-9a-f]{3}-[0-9a-f]{12}(?![0-9a-f])",
    re.IGNORECASE,
)


def is_private_identifier(value: str) -> bool:
    normalized = value.lower()
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest() == PUBLIC_FINGERPRINT


def redact(source: Path, destination: Path) -> int:
    document = fitz.open(source)
    matches = 0

    for page in document:
        candidates = {
            match.group(0)
            for match in UUID_RE.finditer(page.get_text("text"))
            if is_private_identifier(match.group(0))
        }
        for candidate in candidates:
            rectangles = page.search_for(candidate)
            if not rectangles:
                raise RuntimeError("protected identifier found in text but not on page")
            for rectangle in rectangles:
                rectangle.x0 -= 1.5
                rectangle.y0 -= 1.0
                rectangle.x1 += 1.5
                rectangle.y1 += 1.0
                page.add_redact_annot(
                    rectangle,
                    text="ID PRIVADO REDACTADO",
                    fontname="helv",
                    fontsize=7.5,
                    fill=(1, 1, 1),
                    text_color=(0.22, 0.25, 0.29),
                    align=fitz.TEXT_ALIGN_LEFT,
                    cross_out=False,
                )
                matches += 1
        if candidates:
            page.apply_redactions()

    if matches != 1:
        raise RuntimeError(f"expected exactly one protected identifier, found {matches}")

    destination.parent.mkdir(parents=True, exist_ok=True)
    document.set_metadata(
        {
            **document.metadata,
            "title": "RICPE Canal Etico - certificado publico con ID privado redactado",
            "subject": "Derivado publico; el original integro se conserva bajo custodia privada",
        }
    )
    document.save(destination, garbage=4, clean=True, deflate=True)
    document.close()

    verification = fitz.open(destination)
    residual = [
        match.group(0)
        for page in verification
        for match in UUID_RE.finditer(page.get_text("text"))
        if is_private_identifier(match.group(0))
    ]
    verification.close()
    if residual:
        raise RuntimeError("protected identifier remains in redacted PDF text")
    return matches


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    count = redact(args.source, args.destination)
    print(f"RICPE public PDF redaction: PASS ({count} protected identifier removed)")


if __name__ == "__main__":
    main()
