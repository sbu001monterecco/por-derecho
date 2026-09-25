#!/usr/bin/env python3
"""Read-only exact-block parity gate for the 26-Aug unitary allegation.

The historical ``sync`` name is retained because CI and handovers route through
it.  This program never rewrites source.  It verifies that all eighteen public
source blocks carry the same attributed theory, non-finding/statutory boundary,
individual-proof rule and temporal disclaimer in their real containing block.
"""
from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ATTRIBUTION = {
    "es": "Gil Marer y Aweswell alegan una sola empresa continuada de criminalidad económica, desarrollada mediante adopción sucesiva y división de funciones.",
    "en": "Gil Marer and Aweswell allege one continuing economic-criminal enterprise, advanced through successive adoption and divided functions.",
}
TEMPORAL = {
    "es": "Esta es solo una alegación fáctica de conexión: no califica los hechos como delito continuado o permanente ni altera la consumación, la ventana de participación o la prescripción de ningún delito concreto.",
    "en": "This is only a factual allegation of connection: it does not characterise the conduct as a continuing or permanent offence or alter completion, any participation window or limitation period for any specific offence.",
}

HTML_FILES = {
    "es": (
        "es/index.html",
        "es/mapa-probatorio-penal-unitario/index.html",
        "es/ingenieria-inversa-criminal-unitaria/index.html",
        "es/ingenieria-forense-criminal-sun-park/index.html",
        "es/registro-unitario/index.html",
        "es/actualizaciones/index.html",
    ),
    "en": (
        "en/index.html",
        "en/unitary-criminal-evidence-map/index.html",
        "en/unitary-criminal-reverse-engineering/index.html",
        "en/sun-park-criminal-engineering-investigation/index.html",
        "en/unitary-record/index.html",
        "en/updates/index.html",
    ),
}
FEED_FILES = {
    "es": "es/actualizaciones/feed.xml",
    "en": "en/updates/feed.xml",
}
PROSECUTION = ROOT / "assets/prosecution-public-entry-20260821.js"
CRIMINAL_ENGINEERING = ROOT / "assets/criminal-engineering-investigation-20260819.js"

STALE = (
    "organised criminal course",
    "curso delictivo organizado",
    "completed criminal scheme",
    "concluded criminal scheme",
    "present record does not close the legal elements of one criminal enterprise",
    "expediente actual no cierra los elementos jurídicos",
)


class _ContainingBlockParser(HTMLParser):
    """Capture actual p/figcaption blocks without manufacturing a text window."""

    TARGET_TAGS = {"p", "figcaption"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[tuple[str, list[str]] | None] = []
        self.blocks: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in self.TARGET_TAGS:
            self.stack.append((tag, []))
        elif self.stack:
            self.stack.append(None)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        return

    def handle_data(self, data: str) -> None:
        for item in self.stack:
            if item is not None:
                item[1].append(data)

    def handle_endtag(self, tag: str) -> None:
        if not self.stack:
            return
        item = self.stack.pop()
        if item is not None and item[0] == tag:
            self.blocks.append((tag, " ".join("".join(item[1]).split())))


def _normalise(value: str) -> str:
    return " ".join(value.split())


def _require_boundaries(label: str, lang: str, block: str, errors: list[str]) -> None:
    compact = _normalise(block)
    lowered = compact.lower()
    for exact in (ATTRIBUTION[lang], TEMPORAL[lang]):
        if exact not in compact:
            errors.append(f"{label}: exact same-block marker missing: {exact}")

    if "570 bis" not in lowered or "570 ter" not in lowered:
        errors.append(f"{label}: Articles 570 bis/ter boundary is not in the containing block")

    if lang == "en":
        groups = {
            "non-finding": ("not a judicial finding", "not a finding"),
            "original-pact boundary": ("original pact",),
            "individual participation": ("participation",),
            "individual guilt": ("guilt",),
            "actor-specific proof": ("actor",),
            "offence-specific proof": ("offence",),
            "separate proof": ("separate", "separately"),
        }
    else:
        groups = {
            "non-finding": ("no hallazgo judicial", "no un hallazgo judicial", "no es un hallazgo judicial", "no es una declaración judicial", "no constituye un hallazgo judicial"),
            "original-pact boundary": ("pacto originario", "pacto original"),
            "individual participation": ("participación",),
            "individual guilt": ("culpabilidad",),
            "actor-specific proof": ("actor",),
            "offence-specific proof": ("delito",),
            "separate proof": ("separad",),
        }
    for description, alternatives in groups.items():
        if not any(item in lowered for item in alternatives):
            errors.append(f"{label}: {description} is not in the containing block")


def _html_block(path: Path, lang: str, errors: list[str]) -> str:
    if not path.is_file():
        errors.append(f"missing {path.relative_to(ROOT)}")
        return ""
    parser = _ContainingBlockParser()
    parser.feed(path.read_text(encoding="utf-8"))
    hits = [(tag, block) for tag, block in parser.blocks if ATTRIBUTION[lang] in block]
    if len(hits) != 1:
        errors.append(f"{path.relative_to(ROOT)}: expected one real p/figcaption attribution block, found {len(hits)}")
        return ""
    tag, block = hits[0]
    expected_tag = "figcaption" if "registro-unitario" in str(path) or "unitary-record" in str(path) else "p"
    if tag != expected_tag:
        errors.append(f"{path.relative_to(ROOT)}: attribution belongs in {expected_tag}, found {tag}")
    return block


def _feed_block(path: Path, lang: str, errors: list[str]) -> str:
    if not path.is_file():
        errors.append(f"missing {path.relative_to(ROOT)}")
        return ""
    try:
        root = ET.parse(path).getroot()
    except Exception as exc:
        errors.append(f"{path.relative_to(ROOT)}: invalid XML: {exc}")
        return ""
    summaries = ["".join(node.itertext()) for node in root.findall("{http://www.w3.org/2005/Atom}entry/{http://www.w3.org/2005/Atom}summary")]
    hits = [value for value in summaries if ATTRIBUTION[lang] in _normalise(value)]
    if len(hits) != 1:
        errors.append(f"{path.relative_to(ROOT)}: expected one Atom entry summary attribution block, found {len(hits)}")
        return ""
    return hits[0]


def _prosecution_blocks(errors: list[str]) -> dict[str, str]:
    if not PROSECUTION.is_file():
        errors.append(f"missing {PROSECUTION.relative_to(ROOT)}")
        return {}
    text = PROSECUTION.read_text(encoding="utf-8")
    match = re.search(r"section\.innerHTML\s*=\s*isEn\s*\?\s*`(?P<en>.*?)`\s*:\s*`(?P<es>.*?)`;", text, re.S)
    if not match:
        errors.append(f"{PROSECUTION.relative_to(ROOT)}: bilingual runtime template blocks not found")
        return {}
    return {"en": match.group("en"), "es": match.group("es")}


def _engineering_blocks(errors: list[str]) -> dict[str, str]:
    if not CRIMINAL_ENGINEERING.is_file():
        errors.append(f"missing {CRIMINAL_ENGINEERING.relative_to(ROOT)}")
        return {}
    text = CRIMINAL_ENGINEERING.read_text(encoding="utf-8")
    values = re.findall(r"\bbody\s*:\s*'([^']*)'", text)
    result: dict[str, str] = {}
    for lang, exact in ATTRIBUTION.items():
        hits = [value for value in values if exact in value]
        if len(hits) != 1:
            errors.append(f"{CRIMINAL_ENGINEERING.relative_to(ROOT)}: expected one {lang} body string attribution block, found {len(hits)}")
        else:
            result[lang] = hits[0]
    return result


def main() -> int:
    errors: list[str] = []
    blocks: list[tuple[str, str, str]] = []

    for lang, relatives in HTML_FILES.items():
        for relative in relatives:
            blocks.append((relative, lang, _html_block(ROOT / relative, lang, errors)))
    for lang, relative in FEED_FILES.items():
        blocks.append((relative, lang, _feed_block(ROOT / relative, lang, errors)))

    for lang, block in _prosecution_blocks(errors).items():
        blocks.append((f"{PROSECUTION.relative_to(ROOT)}:{lang}-runtime-template", lang, block))
    for lang, block in _engineering_blocks(errors).items():
        blocks.append((f"{CRIMINAL_ENGINEERING.relative_to(ROOT)}:{lang}-body-string", lang, block))

    for label, lang, block in blocks:
        if block:
            _require_boundaries(label, lang, block, errors)

    source_files = {relative for values in HTML_FILES.values() for relative in values}
    source_files.update(FEED_FILES.values())
    source_files.update((str(PROSECUTION.relative_to(ROOT)), str(CRIMINAL_ENGINEERING.relative_to(ROOT))))
    full_source = "\n".join((ROOT / relative).read_text(encoding="utf-8") for relative in sorted(source_files) if (ROOT / relative).is_file())
    for phrase in STALE:
        if phrase.lower() in full_source.lower():
            errors.append(f"stale unitary-attribution phrase remains in controlled public sources: {phrase!r}")

    for lang, exact in ATTRIBUTION.items():
        occurrences = full_source.count(exact)
        if occurrences != 9:
            errors.append(f"{lang}: expected exactly 9 attribution occurrences across controlled sources, found {occurrences}")
    for lang, exact in TEMPORAL.items():
        occurrences = full_source.count(exact)
        if occurrences != 9:
            errors.append(f"{lang}: expected exactly 9 temporal-disclaimer occurrences across controlled sources, found {occurrences}")

    if len(blocks) != 18:
        errors.append(f"expected 18 real containing blocks, constructed {len(blocks)}")

    if errors:
        print("UNITARY ENTERPRISE EXACT-BLOCK SYNC: FAIL", file=sys.stderr)
        for error in errors:
            print(f" - {error}", file=sys.stderr)
        return 1

    print("UNITARY ENTERPRISE EXACT-BLOCK SYNC: PASS")
    print(" - 18 real containing blocks")
    print(" - 9 Spanish + 9 English exact attributions")
    print(" - same-block non-finding, statutory, individual-proof and temporal boundaries")
    print(" - read-only validation; no source mutation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
