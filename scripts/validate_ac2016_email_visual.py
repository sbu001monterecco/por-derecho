#!/usr/bin/env python3
"""Validate the public AC2016-EMAIL-001 derivative and its propagation controls."""

from __future__ import annotations

import hashlib
import json
import re
import struct
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "assets/evidence/ac-email-21-april-2016"
SVG = ASSET_DIR / "ac2016-email-001-redacted-source-card-v2.svg"
PNG = ASSET_DIR / "ac2016-email-001-redacted-source-card-v2.png"
WEBP = ASSET_DIR / "ac2016-email-001-redacted-source-card-v2.webp"
NOTE = ASSET_DIR / "AC2016-EMAIL-001-PUBLIC.md"


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def require(path: Path, needles: list[str]) -> str:
    if not path.is_file():
        fail(f"missing {path.relative_to(ROOT)}")
    text = path.read_text(encoding="utf-8")
    for needle in needles:
        if needle not in text:
            fail(f"{path.relative_to(ROOT)} missing marker: {needle}")
    return text


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def png_dimensions(path: Path) -> tuple[int, int]:
    data = path.read_bytes()[:24]
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        fail("PNG signature invalid")
    return struct.unpack(">II", data[16:24])


def main() -> None:
    svg = require(
        SVG,
        [
            "AC2016-EMAIL-001 · V1.0",
            "NO AUTORIZO SU CONTRATACION",
            "prestar servicio alguno a Luchy",
            "Capacidades separadas: Matkator, CEXP o Comunidad.",
            "mensaje nativo pendiente",
        ],
    )
    visible_svg_text = re.sub(r"<[^>]+>", " ", svg)
    if "@" in visible_svg_text or re.search(r"\+?\d[\d .()-]{7,}\d", visible_svg_text):
        fail("source-card SVG contains an address or phone-like string")
    for forbidden in ("mail.google.com", "permmsgid", "attbid=", "mailto:", "tel:"):
        if forbidden in svg:
            fail(f"source-card SVG contains forbidden private token: {forbidden}")

    if png_dimensions(PNG) != (1350, 2400):
        fail("unexpected PNG dimensions")
    if not WEBP.read_bytes().startswith(b"RIFF"):
        fail("WebP signature invalid")

    require(
        NOTE,
        [
            "separate 2026 forward",
            "does not prove that the five PDFs",
            "d67f88c7243e84e1ceb89ecd0ef14dd4c199449d9fc6053282ddb7fc14b49c65",
            "legacy repository record contains a different carrier hash",
        ],
    )

    require(
        ROOT / "scripts/verify_san_telmo_source_stamp_live.py",
        [
            "site-pre-intervencion-highlight-20260820.js",
            "site-base-20260819.js",
            "BASE_SITE_MARKERS",
        ],
    )

    pages = {
        "en/evidence-pwc-sun-park-meeting-21-april-2016/index.html": [
            "Redacted visual exhibit",
            "Accessible material transcription",
            "Capacity and governance — not reducible to arithmetic",
            "Debt arithmetic may affect one vote; it does not manufacture Community authority.",
        ],
        "es/evidencia-pwc-junta-sun-park-21-abril-2016/index.html": [
            "Exhibición visual redactada",
            "Transcripción material accesible",
            "Capacidad y gobernanza — no reducibles a aritmética",
            "La aritmética de una deuda puede afectar a un voto; no crea la autoridad de la Comunidad.",
        ],
        "en/community-instrumentalisation/index.html": ["email-exhibit-link", "Community authority"],
        "es/comunidad-instrumentalizacion/index.html": ["email-exhibit-link", "autoridad de la Comunidad"],
        "en/community-instrumentalisation/minutes-2011-2022/index.html": ["email-exhibit-link", "Community governance is not arithmetic."],
        "es/comunidad-instrumentalizacion/actas-2011-2022/index.html": ["email-exhibit-link", "La gobernanza comunitaria no es aritmética."],
    }
    for name, markers in pages.items():
        text = require(ROOT / name, markers)
        if "ac2016-email-001-redacted-source-card-v2.webp" not in text:
            fail(f"{name} does not display the controlled visual")

    js = require(
        ROOT / "assets/sun-park-junta-pwc-warning-20260822.js",
        [
            "not to provide services to Luchy without consent",
            "Capacity and governance—not arithmetic",
            "separate carrier",
            "ac2016-email-001-redacted-source-card-v2.webp",
        ],
    )
    for forbidden in (
        "tells the three not to act",
        "ordena a los tres no actuar",
        "PwC agreed to attend. The next day",
        "PwC confirmó que asistiría. Al día siguiente",
    ):
        if forbidden in js:
            fail(f"route-scoped module retains overstatement: {forbidden}")

    registry = json.loads((ROOT / "assets/visual-asset-registry.json").read_text(encoding="utf-8"))
    record = registry["assets"]["document.ac2016-email-001.redacted-source-card-v2"]
    hashes = record["source_provenance"]
    expected = {
        "svg_sha256": sha256(SVG),
        "png_sha256": sha256(PNG),
        "webp_sha256": sha256(WEBP),
    }
    for key, value in expected.items():
        if hashes.get(key) != value:
            fail(f"visual registry {key} mismatch")

    route_registry = json.loads((ROOT / "assets/data/unitary-route-registry-v1.json").read_text(encoding="utf-8"))
    paths = {entry["path"] for entry in route_registry}
    for route in (
        "en/evidence-pwc-sun-park-meeting-21-april-2016/",
        "es/evidencia-pwc-junta-sun-park-21-abril-2016/",
    ):
        if route not in paths:
            fail(f"search registry missing {route}")

    sitemap = (ROOT / "sitemap-community-governance.xml").read_text(encoding="utf-8")
    if sitemap.count("evidence-pwc-sun-park-meeting-21-april-2016") < 2:
        fail("Community sitemap missing English canonical/alternate entries")
    if sitemap.count("evidencia-pwc-junta-sun-park-21-abril-2016") < 2:
        fail("Community sitemap missing Spanish canonical/alternate entries")

    manifest = json.loads((ROOT / "publication-manifests/ac2016-email-visual-propagation-20260822.json").read_text(encoding="utf-8"))
    if manifest["current_state"] != "PR_OPEN" or manifest["controlling_pr"] != 804:
        fail("publication manifest does not identify the open controlling PR")
    if manifest["publication_claims"]["merged"]:
        fail("publication manifest overclaims state")
    if not manifest["publication_claims"]["explicit_user_merge_approval_required"]:
        fail("manifest omits explicit merge-approval gate")

    print("PASS: AC2016 email visual, privacy, scope, links, registry and open-PR controls")


if __name__ == "__main__":
    main()
