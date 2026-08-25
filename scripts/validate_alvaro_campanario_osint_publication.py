#!/usr/bin/env python3
"""Validate the bilingual Campanario/Declaration 011 public-safe publication."""

from __future__ import annotations

import html
from html.parser import HTMLParser
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
        "más de 2.400 mensajes relacionados",
        "aproximadamente mil contienen adjuntos",
        "más del 90% se concentran en 2011–2019",
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
        "more than 2,400 related messages",
        "approximately one thousand include attachments",
        "more than 90% fall in 2011–2019",
        "has not been acquired",
        "not ratified",
        "AP 89/2014",
        "Not located ≠ nonexistent",
    ),
}

PROFILE_LINKS = (
    "../alvaro-campanario-hernandez/",
    "../juan-carlos-prieto-puente/",
    "../esteban-lopez-noriega/",
    "../millan-and-miners-slp/",
    "../antonio-cogolludo-rojas/",
    "../pamanil-sl/",
    "../pamalexsha-servicios-integrales-sl/",
    "../explotaciones-noalpa-sl/",
    "../santa-lucia-real-estate-sl/",
    "../shaila-maria-cogolludo-ramos/",
    "../francisco-mario-matos-matas/",
    "../francisco-de-borja-rodriguez-batllori-laffitte/",
    "../asuncion-aizpurua-sanchez/",
    "../montelanza-monte-lanza-sl/",
    "../inversiones-salinetas-sl/",
)

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
REQUIRED_PROTOCOL_LINKS = (
    "../../archive/declarations/VOICE_TO_TEXT_STATEMENT_OF_FACT_AND_TRUTH_PROTOCOL_25AUG2026.md",
    "../../archive/RESERVED_DECLARANT_PRIVATE_MAILBOX_ACQUISITION_AND_CUSTODY_PROTOCOL_25AUG2026.md",
    "../../archive/OPEN_SOURCE_INTELLIGENCE_NAMED_PERSON_ENTITY_PROTOCOL_25AUG2026.md",
)
MAILBOX_SECTION = {
    "es/alvaro-campanario-prieto-puente-lopez-noriega/index.html": (
        "buzon",
        (
            "más de 2.400 mensajes relacionados",
            "aproximadamente mil contienen adjuntos",
            "más del 90% se concentran en 2011–2019",
        ),
    ),
    "en/alvaro-campanario-prieto-puente-lopez-noriega/index.html": (
        "mailbox",
        (
            "more than 2,400 related messages",
            "approximately one thousand include attachments",
            "more than 90% fall in 2011–2019",
        ),
    ),
}
MAILBOX_ALLOWED_HREFS = (
    "../../archive/RESERVED_DECLARANT_PRIVATE_MAILBOX_ACQUISITION_AND_CUSTODY_PROTOCOL_25AUG2026.md",
    "../../archive/MISSING_EVIDENCE_REGISTER_VOICE_OSINT_MAILBOX_ADDENDUM_25AUG2026.md",
)
UNAPPROVED_COUNT_DETAIL = re.compile(
    r"\d|\b(?:hundred|hundreds|thousand|thousands|million|millions|"
    r"cien|ciento|cientos|mil|miles|mill[oó]n|millones)\b",
    re.IGNORECASE,
)
MAILBOX_TERM = (
    r"(?:private\s+(?:mailbox|account)|mailbox|buz[oó]n(?:\s+privado)?|cuenta\s+privada|"
    r"connected\s+counterpart|contraparte\s+conectad[oa]|related\s+messages|mensajes\s+relacionados)"
)
MAILBOX_COUNT_CONTEXT = re.compile(
    rf"(?:{MAILBOX_TERM}[^.!?]{{0,120}}(?:{UNAPPROVED_COUNT_DETAIL.pattern})|"
    rf"(?:{UNAPPROVED_COUNT_DETAIL.pattern})[^.!?]{{0,120}}{MAILBOX_TERM})",
    re.IGNORECASE,
)


class AttributeCommentInspector(HTMLParser):
    """Collect attribute/comment fragments without treating tag names as data."""

    def __init__(self, allowed_hrefs: tuple[str, ...] = ()) -> None:
        super().__init__(convert_charrefs=True)
        self.allowed_hrefs = set(allowed_hrefs)
        self.fragments: list[str] = []

    def handle_starttag(self, _tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for name, value in attrs:
            if name.lower() == "href" and value in self.allowed_hrefs:
                continue
            self.fragments.append(f"{name} {value or ''}")

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)

    def handle_comment(self, data: str) -> None:
        self.fragments.append(data)


def attribute_comment_fragments(document: str) -> list[str]:
    inspector = AttributeCommentInspector(MAILBOX_ALLOWED_HREFS)
    inspector.feed(document)
    return inspector.fragments


def section_source(document: str, section_id: str) -> str | None:
    match = re.search(
        rf'<section\b[^>]*\bid="{re.escape(section_id)}"[^>]*>.*?</section>',
        document,
        flags=re.IGNORECASE | re.DOTALL,
    )
    return match.group(0) if match else None


def remove_approved_phrases(text: str, approved_phrases: tuple[str, ...]) -> str:
    for phrase in approved_phrases:
        text = re.sub(re.escape(phrase), "", text, flags=re.IGNORECASE)
    return text


def visible_section_text(document: str, section_id: str) -> str | None:
    source = section_source(document, section_id)
    if source is None:
        return None
    without_tags = re.sub(r"<[^>]+>", " ", source)
    return " ".join(html.unescape(without_tags).split())


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
        for link in PROFILE_LINKS:
            if f'href="{link}"' not in text:
                errors.append(f"{relative}: missing dedicated-profile link {link!r}")
        for link in REQUIRED_PROTOCOL_LINKS:
            if f'href="{link}"' not in text:
                errors.append(f"{relative}: missing canonical protocol link {link!r}")

        section_id, approved_phrases = MAILBOX_SECTION[relative]
        mailbox_text = visible_section_text(text, section_id)
        if mailbox_text is None:
            errors.append(f"{relative}: missing private-mailbox section #{section_id}")
        else:
            residual = remove_approved_phrases(mailbox_text, approved_phrases)
            # Coarse-only publication rule: after removing the three approved
            # aggregate phrases, no other numeric detail may remain. This
            # blocks exact totals and year-bucket tables without storing any
            # private exact value in the public validator itself.
            if UNAPPROVED_COUNT_DETAIL.search(residual):
                errors.append(f"{relative}: unapproved numeric detail in private-mailbox section")

            mailbox_source = section_source(text, section_id) or ""
            if any(
                UNAPPROVED_COUNT_DETAIL.search(fragment)
                for fragment in attribute_comment_fragments(mailbox_source)
            ):
                errors.append(f"{relative}: numeric mailbox detail hidden in markup")

        # The aggregate must not be moved to another visible element, comment
        # or attribute to bypass the dedicated-section rule.
        document_visible = " ".join(html.unescape(re.sub(r"<[^>]+>", " ", text)).split())
        document_residual = remove_approved_phrases(document_visible, approved_phrases)
        hidden_context = any(
            MAILBOX_COUNT_CONTEXT.search(fragment)
            for fragment in attribute_comment_fragments(text)
        )
        if MAILBOX_COUNT_CONTEXT.search(document_residual) or hidden_context:
            errors.append(f"{relative}: unapproved mailbox count outside approved aggregate wording")

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
