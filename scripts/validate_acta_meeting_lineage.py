#!/usr/bin/env python3
"""Validate the ACTA/meeting perimeter map, individual pages and interlinks."""

from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


REPO = Path(__file__).resolve().parents[1]
INDEX = REPO / "evidence/community/actas/meeting-lineage-index-v1.json"
ALLOWED = {
    "pre_sale_montelanza",
    "project_lpb_aweswell_gil",
    "adverse_montelanza_molina",
    "adverse_acosta_matos",
    "mixed_or_contested",
    "unresolved",
}


class Links(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.values: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        key = "href" if tag in {"a", "link"} else "src" if tag in {"img", "script"} else None
        if key and values.get(key):
            self.values.append((tag, values[key] or ""))


def local_target(page: Path, value: str) -> Path | None:
    parsed = urlsplit(value)
    if parsed.scheme or parsed.netloc or value.startswith(("mailto:", "#")):
        return None
    relative = unquote(parsed.path)
    if not relative:
        return None
    target = (page.parent / relative).resolve()
    if relative.endswith("/"):
        target /= "index.html"
    return target


def main() -> int:
    errors: list[str] = []
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    events = data.get("events", [])
    if len(events) != 20:
        errors.append(f"expected 20 controlled events, found {len(events)}")
    ids = [event.get("id") for event in events]
    if len(ids) != len(set(ids)):
        errors.append("duplicate event IDs")
    routes: set[str] = set()
    located = 0
    for event in events:
        event_id = event.get("id", "<missing>")
        if event.get("perimeter") not in ALLOWED:
            errors.append(f"{event_id}: invalid perimeter {event.get('perimeter')}")
        for field in ("convener_es", "convener_en", "basis_es", "basis_en", "attribution_status", "confidence"):
            if not str(event.get(field, "")).strip():
                errors.append(f"{event_id}: missing {field}")
        for route_field, locale in (("detail_page_es", "es"), ("detail_page_en", "en")):
            route = event.get(route_field, "")
            if not route or route in routes:
                errors.append(f"{event_id}: missing/duplicate {route_field}")
                continue
            routes.add(route)
            page = REPO / route
            if not page.is_file():
                errors.append(f"{event_id}: missing page {route}")
                continue
            source = page.read_text(encoding="utf-8")
            required = [event_id, f'data-perimeter="{event["perimeter"]}"', "Attribution rule" if locale == "en" else "Regla de atribución"]
            for marker in required:
                if marker not in source:
                    errors.append(f"{route}: missing marker {marker}")
            if event.get("transcript_path"):
                located += locale == "es"
                if "acta-full-ocr" not in source:
                    errors.append(f"{route}: missing embedded full OCR")
                expected = len(event.get("source_preview_pages", []))
                actual = source.count('class="acta-source-page"')
                if expected != actual:
                    errors.append(f"{route}: source gallery {actual}/{expected}")
            else:
                if "acta-source-gap" not in source:
                    errors.append(f"{route}: missing explicit source-gap block")
            parser = Links()
            parser.feed(source)
            for tag, value in parser.values:
                target = local_target(page, value)
                if target is None:
                    continue
                try:
                    target.relative_to(REPO.resolve())
                except ValueError:
                    errors.append(f"{route}: link escapes repository: {value}")
                    continue
                if not target.exists():
                    errors.append(f"{route}: broken {tag} link {value}")

    if located != 17:
        errors.append(f"expected 17 digitised ACTA families, found {located}")
    for chronology in (
        REPO / "es/comunidad-instrumentalizacion/actas-2011-2022/index.html",
        REPO / "en/community-instrumentalisation/minutes-2011-2022/index.html",
    ):
        source = chronology.read_text(encoding="utf-8")
        if source.count("ACTA-LINEAGE-LINKS:START") != 1 or source.count("ACTA-LINEAGE-LINKS:END") != 1:
            errors.append(f"{chronology.relative_to(REPO)}: lineage block count invalid")
        if source.count("open complete record") + source.count("abrir ficha completa") != 20:
            errors.append(f"{chronology.relative_to(REPO)}: not all 20 event pages linked")
    js = (REPO / "assets/acta-document-room-20260822.js").read_text(encoding="utf-8")
    for perimeter in ALLOWED:
        if perimeter not in js:
            errors.append(f"document-room JS missing perimeter {perimeter}")
    for room in (
        REPO / "es/comunidad-instrumentalizacion/sala-documental-actas/index.html",
        REPO / "en/community-instrumentalisation/acta-document-room/index.html",
    ):
        source = room.read_text(encoding="utf-8")
        if "meeting-lineage-index-v1.json" not in source:
            errors.append(f"{room.relative_to(REPO)}: lineage index not wired")
        for perimeter in ALLOWED:
            if perimeter not in source:
                errors.append(f"{room.relative_to(REPO)}: legend/filter missing {perimeter}")
    sitemap = (REPO / "sitemap.xml").read_text(encoding="utf-8")
    for route in routes:
        url = "https://sbu001monterecco.github.io/por-derecho/" + route.removesuffix("index.html")
        if url not in sitemap:
            errors.append(f"sitemap missing {url}")
    if errors:
        print("ACTA meeting-lineage validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("ACTA meeting-lineage validation: PASS")
    print("- 20 controlled events / 40 bilingual pages")
    print("- 17 full public OCR + redacted source-gallery families")
    print("- 3 explicit non-complete event/source pages")
    print("- perimeter attribution, chronology, sitemap and local links reconciled")
    return 0


if __name__ == "__main__":
    sys.exit(main())
