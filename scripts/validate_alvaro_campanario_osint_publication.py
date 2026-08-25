#!/usr/bin/env python3
"""Validate the bilingual Campanario/Declaration 011 public-safe publication."""

from __future__ import annotations

from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]

ROUTES = {
    "es/alvaro-campanario-prieto-puente-lopez-noriega/index.html": (
        "Álvaro Campanario Hernández",
        "Juan Carlos Prieto Puente",
        "Esteban López Noriega",
        "MILLAN AND MINERS SOCIEDAD LIMITADA PROFESIONAL",
        "EXPLOTACIONES NOALPA, S.L.",
        "PAMALEXSHA SERVICIOS INTEGRALES, S.L.",
        "SANTA LUCIA REAL ESTATE, S.L.",
        "2.413 mensajes",
        "no ha sido adquirido",
        "no ratificada",
        "AP 89/2014",
        "No localizado ≠ inexistente",
    ),
    "en/alvaro-campanario-prieto-puente-lopez-noriega/index.html": (
        "Álvaro Campanario Hernández",
        "Juan Carlos Prieto Puente",
        "Esteban López Noriega",
        "MILLAN AND MINERS SOCIEDAD LIMITADA PROFESIONAL",
        "EXPLOTACIONES NOALPA, S.L.",
        "PAMALEXSHA SERVICIOS INTEGRALES, S.L.",
        "SANTA LUCIA REAL ESTATE, S.L.",
        "2,413 messages",
        "has not been acquired",
        "not ratified",
        "AP 89/2014",
        "Not located ≠ nonexistent",
    ),
}

DISCOVERY = {
    "es/actualizaciones/index.html": "campanario-osint-declaracion011-25ago",
    "en/updates/index.html": "campanario-osint-declaration011-25aug",
    "es/actualizaciones/feed.xml": "es/alvaro-campanario-prieto-puente-lopez-noriega/",
    "en/updates/feed.xml": "en/alvaro-campanario-prieto-puente-lopez-noriega/",
    "sitemap.xml": "es/alvaro-campanario-prieto-puente-lopez-noriega/",
}

PUBLIC_SURFACES = tuple(ROUTES) + tuple(DISCOVERY)
FORBIDDEN = (
    re.compile(r"[A-Z0-9._%+-]+@gmail\.com", re.IGNORECASE),
    re.compile(r"\b(?:message[_-]?id|thread[_-]?id|x-gm-msgid|x-gm-thrid)\b", re.IGNORECASE),
    re.compile(r"mail\.google\.com/mail/u/", re.IGNORECASE),
)


def main() -> int:
    errors: list[str] = []
    texts: dict[str, str] = {}

    for relative, markers in ROUTES.items():
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"missing route: {relative}")
            continue
        text = path.read_text(encoding="utf-8")
        texts[relative] = text
        for marker in markers:
            if marker not in text:
                errors.append(f"{relative}: missing marker {marker!r}")
        if len(re.findall(r"<li>", text)) != 11:
            errors.append(f"{relative}: expected exactly 11 future-action list items")
        if text.count('rel="canonical"') != 1:
            errors.append(f"{relative}: expected one canonical link")
        if 'hreflang="es"' not in text or 'hreflang="en"' not in text:
            errors.append(f"{relative}: bilingual hreflang parity missing")

    for relative, marker in DISCOVERY.items():
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"missing discovery surface: {relative}")
            continue
        text = path.read_text(encoding="utf-8")
        texts[relative] = text
        if marker not in text:
            errors.append(f"{relative}: missing discovery marker {marker!r}")

    for relative in ("es/actualizaciones/feed.xml", "en/updates/feed.xml", "sitemap.xml"):
        try:
            ET.parse(ROOT / relative)
        except Exception as exc:
            errors.append(f"{relative}: invalid XML: {exc}")

    for relative in PUBLIC_SURFACES:
        text = texts.get(relative, "")
        for pattern in FORBIDDEN:
            if pattern.search(text):
                errors.append(f"{relative}: forbidden message-level private locator pattern")

    if errors:
        print("FAIL: Campanario / Declaration 011 publication")
        print("\n".join(f"- {error}" for error in errors))
        return 1

    print("PASS: Campanario / Declaration 011 bilingual routes, discovery, privacy and 11-action continuation")
    return 0


if __name__ == "__main__":
    sys.exit(main())
