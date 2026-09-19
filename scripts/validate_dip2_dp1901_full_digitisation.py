#!/usr/bin/env python3
"""Validate the 18-Sep-2026 DIP2 / DP1901 full available-corpus digitisation."""

from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FILES = {
    "evidence/fiscalia/dip-2-2026/full-text/denuncia-inicial-13ene2026-public-transcription.md": {
        "id": "EVID-2026-FISCALIA-DIP2-DENUNCIA-013JAN-001",
        "hash": "d42051eea0ff28bc230ef58315333729a84454b8376b23ad7bbc5db35e3a77a4",
        "pages": 5,
        "required": ["DENUNCIA PENAL POR INDICIOS DE PREVARICACIÓN JUDICIAL", "## Página 5 de 5"],
    },
    "evidence/fiscalia/dip-2-2026/full-text/ampliacion-08feb2026-public-transcription.md": {
        "id": "EVID-2026-FISCALIA-DIP2-AMPLIACION-08FEB-002",
        "hash": "07dc79179397f680f0201075618d6782af31a6432c823a1addf341a0f75bf1be",
        "pages": 5,
        "required": ["AMPLIACIÓN DE DENUNCIA PENAL", "## Página 5 de 5"],
    },
    "evidence/fiscalia/dip-2-2026/full-text/decreto-archivo-dip-2-2026-06mar2026-public-transcription.md": {
        "id": "EVID-2026-FISCALIA-DIP2-DECRETO-002",
        "hash": None,
        "pages": 10,
        "required": ["## Página 10 de 10", "Juan Manuel González-Casanova Ruiz"],
    },
    "evidence/fiscalia/dip-2-2026/full-text/oficio-notificacion-dip-2-2026-09mar2026-public-transcription.md": {
        "id": "EVID-2026-FISCALIA-DIP2-OFICIO-001",
        "hash": None,
        "pages": 1,
        "required": ["## Página 1 de 1", "Ernesto Vieira Morante"],
    },
    "evidence/fiscalia/dip-2-2026/full-text/actualizacion-11mar2026-public-transcription.md": {
        "id": "EVID-2026-FISCALIA-DIP2-ACTUALIZACION-11MAR-005",
        "hash": "0c3116c35b7dea1976dd39ee043898d0aa6b5b1164c36c9b014b4c3ca70d85b9",
        "pages": 4,
        "required": ["## Página 4 de 4", "han sido recurridas en apelación"],
    },
    "evidence/fiscalia/dip-2-2026/full-text/registro-11mar2026-public-transcription.md": {
        "id": "EVID-2026-FISCALIA-DIP2-REGAGE-11MAR-006",
        "hash": "102d2f407cc33f0398d45239d94fe56a80246e645191e5e987e430b5c533b289",
        "pages": 2,
        "required": ["REGAGE26e00026303869", "## Página 2 de 2", "391e7e2b85dc51caa1e71ecfcfb121668edb6cb4b6f5d9fe20a6dd64d21f154df45c9ed753b15b7993ae23a1cd774340c1e1f00c9ba3a1f426941c6b8a3b6578"],
    },
    "evidence/fiscalia/dip-2-2026/full-text/registro-tramitacion-12mar2026-email-public-transcription.md": {
        "id": "EVID-2026-FISCALIA-DIP2-REGAGE-TRAMITACION-007",
        "hash": None,
        "pages": 0,
        "required": ["08:25:36", "informational and has no legal", "does **not** establish"],
    },
    "evidence/judicial/dp-1901-2026/full-text/auto-14sep2026-public-transcription.md": {
        "id": "EVID-2026-DP1901-AUTO-14SEP-001",
        "hash": None,
        "pages": 3,
        "required": ["## Página 3 de 3", "29/07/2026 solicitó el archivo", "SOBRESEIMIENTO LIBRE", "Luis Francisco Galván Mesa", "b4259b179e36a263a2c16818d2f90543105ea400fffdda532c43a342bb513513"],
    },
}

AUTO_PDF = "evidence/judicial/dp-1901-2026/public-pdfs/auto-14sep2026-public-controlled-transcription.pdf"
SOURCE_CLOSURE = "evidence/judicial/dp-1901-2026/PROCEDURAL_IDENTITY_SOURCE_CLOSURE_18SEP2026.md"

PUBLIC_PAGES = [
    "es/fiscalia-dip-2-2026/index.html",
    "en/fiscalia-dip-2-2026/index.html",
    "es/dp-1901-2026-auto-14-septiembre-2026/index.html",
    "en/dp-1901-2026-order-14-september-2026/index.html",
    "es/procedimientos/gc-fis-017/index.html",
    "en/proceedings/gc-fis-017/index.html",
    "es/procedimientos/gc-cri-008/index.html",
    "en/proceedings/gc-cri-008/index.html",
]

FORBIDDEN_PUBLIC = [
    "Y2231410X",
    "sbu001@monterecco.com",
    "Calle Pozo Cabildo 34",
    "357bfa7692450dac8cab2269fb61773051453501",
]

def fail(msg: str) -> None:
    raise SystemExit("FAIL: " + msg)

def main() -> None:
    for rel, spec in FILES.items():
        p = ROOT / rel
        if not p.is_file():
            fail(f"missing digitised source: {rel}")
        text = p.read_text(encoding="utf-8")
        if spec["id"] not in text:
            fail(f"{rel}: missing evidence ID {spec['id']}")
        if spec["hash"] and spec["hash"] not in text:
            fail(f"{rel}: missing source SHA-256")
        for marker in spec["required"]:
            if marker not in text:
                fail(f"{rel}: missing marker {marker!r}")
        for n in range(1, spec["pages"] + 1):
            if f"## Página {n} de {spec['pages']}" not in text:
                fail(f"{rel}: page-accounting marker missing for page {n}")
        for token in FORBIDDEN_PUBLIC:
            if token.casefold() in text.casefold():
                fail(f"{rel}: forbidden private token leaked: {token}")

    if not (ROOT/AUTO_PDF).is_file():
        fail(f"missing DP1901 public PDF derivative: {AUTO_PDF}")

    source_closure_path=ROOT/SOURCE_CLOSURE
    if not source_closure_path.is_file():
        fail(f"missing DP1901 procedural-identity source closure: {SOURCE_CLOSURE}")
    source_closure=source_closure_path.read_text(encoding="utf-8")
    for marker in [
        "REF21_TO_DP1901_CONTEMPORANEOUSLY_CORROBORATED — OFFICIAL_REPARTO_AND_REF24_ASSOCIATION_HISTORY_OUTSTANDING",
        "dfad6f405b7a2ec047a98a7183a9cbfd0698427d3925d02b2a50b4de76de8f71",
        "2f9b7015598094c68f6408b68a776073de1d7d2fa248169be46fd57bf3bad6c3",
        "8ee03884d32b6b3d9e8377a646eca3d79a7ae199aebc8cc378a9180ba2aef846",
        "does **not** prove",
    ]:
        if marker not in source_closure:
            fail(f"source closure missing marker {marker!r}")
    for token in FORBIDDEN_PUBLIC:
        if token.casefold() in source_closure.casefold():
            fail(f"{SOURCE_CLOSURE}: forbidden private token leaked: {token}")

    for rel in PUBLIC_PAGES:
        p=ROOT/rel
        if not p.is_file():
            fail(f"missing public page: {rel}")

    readme=(ROOT/"evidence/fiscalia/dip-2-2026/README.md").read_text(encoding="utf-8")
    for marker in [
        "EVID-2026-FISCALIA-DIP2-DENUNCIA-013JAN-001",
        "EVID-2026-FISCALIA-DIP2-AMPLIACION-08FEB-002",
        "EVID-2026-FISCALIA-DIP2-ACTUALIZACION-11MAR-005",
        "EVID-2026-FISCALIA-DIP2-REGAGE-11MAR-006",
        "EVID-2026-FISCALIA-DIP2-REGAGE-TRAMITACION-007",
        "full digitisation of the **available located corpus**",
    ]:
        if marker not in readme:
            fail(f"DIP2 README missing {marker!r}")

    for rel in [
        "es/fiscalia-dip-2-2026/index.html",
        "en/fiscalia-dip-2-2026/index.html",
    ]:
        page=(ROOT/rel).read_text(encoding="utf-8")
        if "registro-tramitacion-12mar2026-email-public-transcription.md" not in page:
            fail(f"{rel}: missing registry-processing trace link")
        if "decreto-archivo-dip-2-2026-06mar2026-public-redacted.pdf" not in page:
            fail(f"{rel}: missing embedded DIP2 Decree PDF")
        if not any(marker in page.casefold() for marker in ["crítica", "critique"]):
            fail(f"{rel}: missing contextual critique layer")

    for rel, source_boundary_marker in [
        ("es/dp-1901-2026-auto-14-septiembre-2026/index.html", "nativo"),
        ("en/dp-1901-2026-order-14-september-2026/index.html", "native"),
    ]:
        page=(ROOT/rel).read_text(encoding="utf-8")
        if "auto-14sep2026-public-controlled-transcription.pdf" not in page:
            fail(f"{rel}: missing embedded DP1901 PDF derivative")
        if source_boundary_marker not in page.casefold():
            fail(f"{rel}: missing non-native source boundary")
        if not any(marker in page.casefold() for marker in ["crítica", "critique"]):
            fail(f"{rel}: missing contextual critique layer")
        if "PROCEDURAL_IDENTITY_SOURCE_CLOSURE_18SEP2026.md" not in page:
            fail(f"{rel}: missing DP1901 source-closure link")

    divergence=(ROOT/"ops/GITLAB_PUBLIC_PAGES_DIVERGENCE_18SEP2026.md").read_text(encoding="utf-8")
    for marker in ["PROCEDURAL_IDENTITY_COLLISION_OPEN", "29 July 2026", "read-only comparator"]:
        if marker not in divergence:
            fail(f"GitLab divergence control missing {marker!r}")

    ledger=(ROOT/"evidence/fiscalia/2026/DIP2_INACCURACY_ANALYTICAL_ERROR_LEDGER_18SEP2026.md").read_text(encoding="utf-8")
    for marker in ["DIP2-ERR-01","DOCUMENTED SOURCE-TO-PREMISE DISCREPANCY","PROPAGATION QUESTION"]:
        if marker not in ledger:
            fail(f"error ledger missing {marker!r}")

    three_track=json.loads((ROOT/"data/three-track-full-digitisation-20260904.json").read_text(encoding="utf-8"))
    tracks={item["track_id"]: item for item in three_track.get("tracks", [])}
    private_track=tracks.get("DP1901-C21", {})
    if private_track.get("base_filing",{}).get("pages") != 86:
        fail("three-track DP1901 private base source must be 86 pages")
    if private_track.get("immediate_amplification",{}).get("pages") != 26:
        fail("three-track DP1901 immediate amplification must be 26 pages")
    if private_track.get("expansion",{}).get("pages") != 19:
        fail("three-track DP1901 9-Jul amplification must be 19 pages")
    judge_track=tracks.get("C24-JUDGE", {})
    if judge_track.get("base_filing",{}).get("pages") != 79:
        fail("three-track judge package must be 79 pages total")
    if judge_track.get("base_filing",{}).get("principal_document_bundle_pages") != 31:
        fail("three-track judge principal document bundle must be 31 pages")
    if judge_track.get("base_filing",{}).get("principal_pleading_pages") != 27:
        fail("three-track judge pleading must be 27 pages")
    if judge_track.get("base_filing",{}).get("presentation_front_matter_pages") != 4:
        fail("three-track judge front matter must be 4 pages")
    if judge_track.get("supplement",{}).get("pages") != 13:
        fail("three-track judge dependent supplement must be 13 pages")
    if "REF21_TO_DP1901_CONTEMPORANEOUSLY_CORROBORATED" not in judge_track.get("status_control",{}).get("supervening_status_20260918",""):
        fail("three-track judge/DP1901 state must preserve Ref21 contemporaneous corroboration")
    if "REF24_ASSOCIATION_HISTORY_OUTSTANDING" not in judge_track.get("status_control",{}).get("supervening_status_20260918",""):
        fail("three-track judge/DP1901 state must preserve the outstanding later Ref24 association history")

    for rel in [
        "es/dp-1901-2026/index.html",
        "en/dp-1901-2026/index.html",
    ]:
        gateway=(ROOT/rel).read_text(encoding="utf-8")
        if "PROCEDURAL_IDENTITY_SOURCE_CLOSURE_18SEP2026.md" not in gateway:
            fail(f"{rel}: missing DP1901 source-closure link")
        if "principally a private-actor/CAM route" in gateway:
            fail(f"{rel}: stale settled private-actor route assertion")
        if "principalmente una vía privada/CAM" in gateway:
            fail(f"{rel}: stale settled private-actor route assertion")

    manifest=json.loads((ROOT/"evidence/fiscalia/2026/DIP2_DP1901_FULL_DIGITISATION_STATE_18SEP2026.json").read_text(encoding="utf-8"))
    if manifest.get("publication_id")!="FISCALIA_DIP2_DP1901_FULL_DIGITISATION_20260918":
        fail("unexpected publication manifest ID")
    if manifest.get("privacy",{}).get("raw_private_native_sources_committed") is not False:
        fail("manifest must preserve private-native-source boundary")

    print("PASS: DIP2 available corpus and DP1901 14-Sep order are page-accounted, linked and privacy-controlled")

if __name__ == "__main__":
    main()
