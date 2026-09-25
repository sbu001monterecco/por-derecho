#!/usr/bin/env python3
"""Fail closed on the controlled five-private-actor visual architecture."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRIO_ASSET = "assets/actors/fmmm-shaila-antonio-family-editorial-display-20260922.jpg"
ACOSTA_ASSET = "assets/acosta-matos-family-hotel-plans.jpg"
ACTOR_ORDER = ("fmmm", "smcr", "acr", "jdam", "lpam")


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def require(errors: list[str], condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    errors: list[str] = []
    registry = json.loads(read("assets/visual-asset-registry.json"))
    contract = json.loads(read("ops/REPOSITORY_PRESERVATION_CONTRACT.json"))

    asset = registry["assets"].get("document.fmmm-shaila-antonio-family-editorial-display-20260922", {})
    require(errors, asset.get("path") == TRIO_ASSET, "visual registry does not lock the editorial trio asset")
    basis = asset.get("identity_basis", "")
    for marker in ("Patricia Domínguez", "Gil Marer", "No facial recognition"):
        require(errors, marker.lower() in basis.lower(), f"visual registry identity basis missing {marker}")
    require(errors, asset.get("source_provenance", {}).get("facial_recognition_used") is False, "facial-recognition flag must be false")

    lock = contract["five_actor_front_page_lock"]["required_homepage_structure"]
    require(errors, lock.get("trio_visual_asset") == TRIO_ASSET, "preservation contract trio asset mismatch")
    require(errors, lock.get("acosta_visual_asset") == ACOSTA_ASSET, "preservation contract Acosta asset mismatch")
    require(errors, tuple(lock.get("stable_actor_ids", [])) == ACTOR_ORDER, "preservation contract actor order/identity mismatch")

    # 25 Sep 2026 owner-authorised orientation-first homepage:
    # controlled actor visuals stay out of the root homepages and remain
    # source-controlled through the dedicated dossiers, actor pages and runtime.
    for route in ("en/index.html", "es/index.html"):
        text = read(route)
        require(errors, "data-private-actor-card=" not in text, f"{route}: actor-card dossier content returned to orientation homepage")
        require(errors, TRIO_ASSET.split("assets/", 1)[1] not in text, f"{route}: trio dossier visual returned to orientation homepage")
        require(errors, ACOSTA_ASSET.split("assets/", 1)[1] not in text, f"{route}: Acosta dossier visual returned to orientation homepage")


    dossier_rules = {
        "en/fmmm-shaila-antonio-family-community-corporate-continuity/index.html": "not derived from facial recognition",
        "es/fmmm-shaila-antonio-continuidad-familiar-comunitaria-societaria/index.html": "no procede de reconocimiento facial",
    }
    for route, marker in dossier_rules.items():
        text = read(route)
        require(errors, TRIO_ASSET.split("assets/", 1)[1] in text, f"{route}: editorial trio visual missing")
        require(errors, "Patricia Domínguez" in text and "Gil Marer" in text and marker in text, f"{route}: controlled identification provenance missing")

    for lang, boundary in (
        ("en", "The photograph establishes identity/relationship context only."),
        ("es", "La fotografía aporta únicamente contexto de identidad y relación."),
    ):
        for actor, crop_class in (("shaila-maria-cogolludo-ramos", "cpn-source-crop--shaila"), ("antonio-cogolludo-rojas", "cpn-source-crop--antonio")):
            route = f"{lang}/{actor}/index.html"
            text = read(route)
            require(errors, TRIO_ASSET.split("assets/", 1)[1] in text, f"{route}: source-derived crop asset missing")
            require(errors, crop_class in text, f"{route}: actor-specific source crop missing")
            require(errors, "Patricia Domínguez" in text and "Gil Marer" in text, f"{route}: crop provenance missing")
            require(errors, boundary in text, f"{route}: crop evidence boundary missing")

    for route in ("en/francisco-mario-matos-matas/index.html", "es/francisco-mario-matos-matas/index.html"):
        text = read(route)
        require(errors, "assets/actors/francisco-mario-matos-matas.jpg" in text, f"{route}: canonical individual portrait missing")
        require(errors, TRIO_ASSET.split("assets/", 1)[1] not in text, f"{route}: shared derivative replaced the canonical individual portrait")

    generator = read("assets/homepage-actor-family-pwc-note-20260819.js")
    for marker in (TRIO_ASSET.split("assets/", 1)[1], ACOSTA_ASSET.split("assets/", 1)[1], "Patricia Domínguez", "not derived from facial recognition", "no procede de reconocimiento facial"):
        require(errors, marker in generator, f"homepage generator missing visual control marker {marker}")
    require(errors, "portrait awaiting verification" not in generator.lower(), "homepage generator retains a stale portrait-awaiting state")

    css = read("assets/five-actor-accountability-20260824.css")
    for marker in (".pd-five-ac__actor-architecture", ".pd-five-ac__cluster-cards--trio", ".pd-five-ac__cluster-cards--pair", ".pd-five-ac__image-boundary"):
        require(errors, marker in css, f"responsive five-actor stylesheet missing {marker}")

    if errors:
        print("FIVE-PRIVATE-ACTOR VISUAL INTEGRATION: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("FIVE-PRIVATE-ACTOR VISUAL INTEGRATION: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
