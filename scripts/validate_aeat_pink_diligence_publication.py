#!/usr/bin/env python3
"""Validate the controlled publication of the 6 April 2022 AEAT diligence."""

from __future__ import annotations

import hashlib
import json
import sys
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_ID = "EVID-AEAT-PINK-VA-20220406-001"
PDF_HASH = "1698a0800c477b526c3b1f1f5ca8ab55fc07a1248a0cc112fe2d42f175dbf2c9"
PREVIEW_HASH = "b321db0392cf9f5bda97bc4f629f018a127c368881a43d26b716be95d5d25843"
NATIVE_HASH = "b6ffc7cf29928a41bac7a466d16e513cc5e2f1c8d8db5069ae86ba64e117bb16"

FILES = {
    "pdf": ROOT / "evidence/aeat/pink/2022-04-06-vigilancia-aduanera/public-pdfs/diligencia-aeat-vigilancia-aduanera-sun-park-6abril2022-public-redacted.pdf",
    "preview": ROOT / "evidence/aeat/pink/2022-04-06-vigilancia-aduanera/public-pages/diligencia-aeat-vigilancia-aduanera-sun-park-6abril2022-page1-public.png",
    "transcript": ROOT / "evidence/aeat/pink/2022-04-06-vigilancia-aduanera/full-text/diligencia-aeat-vigilancia-aduanera-sun-park-6abril2022-public-transcription.md",
    "translation": ROOT / "evidence/aeat/pink/2022-04-06-vigilancia-aduanera/full-text/diligencia-aeat-vigilancia-aduanera-sun-park-6abril2022-english-translation.md",
    "readme": ROOT / "evidence/aeat/pink/2022-04-06-vigilancia-aduanera/README.md",
    "redactions": ROOT / "evidence/aeat/pink/2022-04-06-vigilancia-aduanera/redaction-log.md",
    "data": ROOT / "assets/data/aeat-pink-vigilancia-aduanera-2022-04-06-v1.json",
    "manifest": ROOT / "publication-manifests/aeat-pink-vigilancia-aduanera-20220406-publication-20260828.json",
    "es": ROOT / "es/evidencia/diligencia-aeat-vigilancia-aduanera-sun-park-6abril2022/index.html",
    "en": ROOT / "en/evidence/aeat-customs-surveillance-sun-park-diligence-6april2022/index.html",
    "es_compat": ROOT / "es/evidencia/aeat-pink-496-2026-alegaciones/index.html",
    "en_compat": ROOT / "en/evidence/aeat-pink-496-2026-allegations/index.html",
    "sitemap": ROOT / "sitemap-pink-aeat.xml",
}

RECIPROCAL = {
    "es/pink-canary-aeat-496-2026/index.html": "diligencia-aeat-vigilancia-aduanera-sun-park-6abril2022/",
    "en/pink-canary-aeat-496-2026/index.html": "aeat-customs-surveillance-sun-park-diligence-6april2022/",
    "es/pink-canary-aeat-audiencia-nacional/index.html": "evidencia/diligencia-aeat-vigilancia-aduanera-sun-park-6abril2022/",
    "en/pink-canary-aeat-national-court/index.html": "evidence/aeat-customs-surveillance-sun-park-diligence-6april2022/",
    "es/toma-control-sun-park-7-junio-2018/index.html": "diligencia-aeat-vigilancia-aduanera-sun-park-6abril2022/",
    "en/sun-park-takeover-7-june-2018/index.html": "aeat-customs-surveillance-sun-park-diligence-6april2022/",
    "es/adjudicacion-2022-reconstruccion-documental/index.html": "diligencia-aeat-vigilancia-aduanera-sun-park-6abril2022/",
    "en/2022-adjudication-documentary-reconstruction/index.html": "aeat-customs-surveillance-sun-park-diligence-6april2022/",
    "es/comunidad-instrumentalizacion/actas-2011-2022/index.html": "diligencia-aeat-vigilancia-aduanera-sun-park-6abril2022/",
    "en/community-instrumentalisation/minutes-2011-2022/index.html": "aeat-customs-surveillance-sun-park-diligence-6april2022/",
    "es/actualizaciones/index.html": "diligencia-aeat-vigilancia-aduanera-sun-park-6abril2022/",
    "en/updates/index.html": "aeat-customs-surveillance-sun-park-diligence-6april2022/",
}


class IdParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []

    def handle_starttag(self, _tag: str, attrs: list[tuple[str, str | None]]) -> None:
        identifier = dict(attrs).get("id")
        if identifier:
            self.ids.append(identifier)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(errors: list[str], condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    errors: list[str] = []
    for label, path in FILES.items():
        require(errors, path.is_file(), f"missing {label}: {path.relative_to(ROOT)}")
    if errors:
        print("AEAT / PINK DILIGENCE PUBLICATION: FAIL")
        print("\n".join(f" - {error}" for error in errors))
        return 1

    require(errors, sha256(FILES["pdf"]) == PDF_HASH, "public PDF hash drift")
    require(errors, sha256(FILES["preview"]) == PREVIEW_HASH, "public preview hash drift")

    data = json.loads(FILES["data"].read_text(encoding="utf-8"))
    require(errors, data.get("evidence_id") == EVIDENCE_ID, "structured evidence ID drift")
    source = data.get("source", {})
    require(errors, source.get("page_count") == 5, "structured source page count must be five")
    require(errors, source.get("native_sha256") == NATIVE_HASH, "native source hash drift")
    require(errors, source.get("public_pdf_sha256") == PDF_HASH, "structured public PDF hash drift")
    require(errors, source.get("native_public") is False, "native source must remain non-public")
    require(errors, len(data.get("propositions", [])) >= 6, "proposition matrix is incomplete")

    for label in ("transcript", "translation"):
        text = FILES[label].read_text(encoding="utf-8")
        require(errors, EVIDENCE_ID in text, f"{label}: evidence ID missing")
        for page in range(1, 6):
            require(errors, f"{page} of 5" in text or f"{page} de 5" in text, f"{label}: page {page} not accounted for")

    page_markers = {
        "es": (
            "Laura Acosta Matos",
            "Interlocutor empresarial masculino no nombrado",
            "no pudieron causar la selección de 2020",
            "Certificación Cabildo recitada, no anexa",
            "1698a080…5dbf2c9",
        ),
        "en": (
            "Laura Acosta Matos",
            "Unnamed male corporate interlocutor",
            "could not have caused the 2020 selection",
            "Recited, unappended Cabildo certificate",
            "1698a080…5dbf2c9",
        ),
    }
    for label, markers in page_markers.items():
        text = FILES[label].read_text(encoding="utf-8")
        parser = IdParser()
        parser.feed(text)
        require(errors, len(parser.ids) == len(set(parser.ids)), f"{label}: duplicate HTML ids")
        for marker in markers:
            require(errors, marker in text, f"{label}: missing marker {marker!r}")

    for label in ("es_compat", "en_compat"):
        text = FILES[label].read_text(encoding="utf-8")
        for forbidden in ("Javier Sixto", ".docx", ".DOCX"):
            require(errors, forbidden not in text, f"{label}: private-draft marker leaked: {forbidden}")
        require(errors, "496/2026" in text, f"{label}: public proceeding identity missing")

    for rel, marker in RECIPROCAL.items():
        path = ROOT / rel
        require(errors, path.is_file(), f"missing reciprocal page {rel}")
        if path.is_file():
            require(errors, marker in path.read_text(encoding="utf-8"), f"missing reciprocal evidence link in {rel}")

    sitemap = FILES["sitemap"].read_text(encoding="utf-8")
    require(errors, sitemap.count("aeat-customs-surveillance-sun-park-diligence-6april2022") >= 2, "English evidence route missing from sitemap")
    require(errors, sitemap.count("diligencia-aeat-vigilancia-aduanera-sun-park-6abril2022") >= 2, "Spanish evidence route missing from sitemap")

    if errors:
        print("AEAT / PINK DILIGENCE PUBLICATION: FAIL")
        print("\n".join(f" - {error}" for error in errors))
        return 1
    print("AEAT / PINK DILIGENCE PUBLICATION: PASS (5 pages, 2 languages, 12 reciprocal routes, hashes and confidentiality boundary controlled)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
