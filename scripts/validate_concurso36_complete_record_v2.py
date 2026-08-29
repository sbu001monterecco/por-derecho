#!/usr/bin/env python3
"""Run the historical complete-record gate without reintroducing a disproved date rule.

The August-23 complete-record validator remains valuable for catalogue counts,
privacy, publication manifests, bilingual source links, security derivatives,
discovery and completeness caveats.  Its only superseded control is the rule
that treated 15 February 2018 as the date of the creditor-substitution Auto and
prohibited the true 8 February date from the critical reader pages.

Primary reinspection on 29 August 2026 established:
  Auto body: 8 February 2018
  judge signature: 9 February 2018
  LAJ signature: 14 February 2018
  copy annotation: NOTIFICADO 15/02/2018

This wrapper preserves all other historical controls, filters only the obsolete
"8 February is superseded" failures, and adds the current v2 source controls.
"""

from __future__ import annotations

import json
import pathlib
import sys

import validate_concurso36_complete_record as legacy

ROOT = pathlib.Path(__file__).resolve().parents[1]
V2 = ROOT / "assets/data/concurso36-what-court-ordered-v2.json"
DUAL = ROOT / "assets/data/concurso36-procedural-taxonomy-judicial-ac-dual-lens-20260829.json"
ES = ROOT / "es/concurso-36-2012-que-ordeno-el-juzgado/index.html"
EN = ROOT / "en/concurso-36-2012-what-the-court-ordered/index.html"

OBSOLETE_DATE_FAILURE = "republishes the superseded creditor-date layer"


def run_legacy_check(fn, failures: list[str]) -> None:
    local: list[str] = []
    fn(local)
    for item in local:
        if OBSOLETE_DATE_FAILURE in item:
            continue
        failures.append(item)


def load(path: pathlib.Path, failures: list[str]):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        failures.append(f"current control unreadable: {path.relative_to(ROOT)}: {exc}")
        return {}


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def check_current_date_and_taxonomy(failures: list[str]) -> None:
    v2 = load(V2, failures)
    dual = load(DUAL, failures)
    if not isinstance(v2, dict) or not isinstance(dual, dict):
        return

    date = v2.get("primary_date_control", {})
    require(date.get("body_date") == "2018-02-08",
            "current control must identify the creditor-substitution Auto as 8 February 2018", failures)
    require(str(date.get("judge_signature", "")).startswith("2018-02-09"),
            "current control must preserve the 9-Feb judge signature layer", failures)
    require(str(date.get("laj_signature", "")).startswith("2018-02-14"),
            "current control must preserve the 14-Feb LAJ signature layer", failures)
    require(date.get("notification_annotation") == "NOTIFICADO 15/02/2018",
            "current control must preserve 15-Feb as notification/custody layer", failures)
    require(abs(float(date.get("special_privilege_total_eur", 0)) - 9052251.69) < 0.01,
            "current control must preserve the €9,052,251.69 fixed special-privilege comparator", failures)

    june = v2.get("critical_comparator_4_june_2018", {})
    require(june.get("not_an_incidente_concursal") is True,
            "4-June control must state that no insolvency-incident route is verified", failures)
    require(june.get("not_verified_as_definitive_text_modification") is True,
            "4-June control must not be recorded as a verified definitive-text modification", failures)
    require(abs(float(june.get("operative_total_eur", 0)) - 13165832.36) < 0.01,
            "4-June control must preserve the €13,165,832.36 operative comparator", failures)

    community = v2.get("community_fees_comparator", {})
    require(community.get("procedural_class") == "MODIFICACION_TEXTOS_DEFINITIVOS",
            "Community comparator must remain an Article-97-bis final-text modification", failures)
    require("SEPARATE INCIDENT DOCKET NOT YET VERIFIED" in str(community.get("status", "")),
            "Community comparator must not be relabelled an insolvency incident without a separate primary docket", failures)

    pieces = {item.get("piece") for item in v2.get("verified_incidentes_concursales_located", []) if isinstance(item, dict)}
    require({"0000007/2012", "0000008/2012"}.issubset(pieces),
            "current located-incident denominator must preserve Pieces 7 and 8", failures)

    require(len(v2.get("definitive_text_change_gate", [])) >= 8,
            "current control must preserve the definitive-text modification proof gate", failures)
    require("cumulative pattern" in str(dual.get("declared_position", {}).get("en", "")),
            "dual-lens control must preserve the cumulative multi-act allegation", failures)

    es = ES.read_text(encoding="utf-8") if ES.is_file() else ""
    en = EN.read_text(encoding="utf-8") if EN.is_file() else ""
    for marker in (
        "8 de febrero de 2018",
        "15/02/2018",
        "INVENTARIO PARCIAL",
        "concurso36-complete-record-v1.json",
        "C36-SUP-ACSEC-2018-02-27",
        "2018-02-27-ac-community-security-request-redacted-searchable.pdf",
        "transcript.es.md",
    ):
        require(marker.lower() in es.lower(), f"Spanish critical reader missing current marker: {marker}", failures)
    for marker in (
        "8 February 2018",
        "15 Feb 2018",
        "INVENTORY PARTIAL",
        "concurso36-complete-record-v1.json",
        "C36-SUP-ACSEC-2018-02-27",
        "2018-02-27-ac-community-security-request-redacted-searchable.pdf",
        "transcript.en.md",
    ):
        require(marker.lower() in en.lower(), f"English critical reader missing current marker: {marker}", failures)
    require("no es un expediente completo" in es.lower(),
            "Spanish critical reader must deny whole-file completeness", failures)
    require("not a complete court file" in en.lower(),
            "English critical reader must deny whole-file completeness", failures)
    require("notificación/custodia" in es.lower(),
            "Spanish reader must distinguish the 15-Feb notification layer", failures)
    require("notification/custody" in en.lower(),
            "English reader must distinguish the 15-Feb notification layer", failures)


def main() -> int:
    failures: list[str] = []

    # Preserve every complete-record control other than the single superseded
    # prohibition on publishing the true 8-February date.
    for fn in (
        legacy.check_catalogue,
        legacy.check_publication_manifest,
        legacy.check_security_publication,
        legacy.check_analytical_artifacts,
        legacy.check_live_closeout_controls,
        legacy.check_route_pages,
        legacy.check_implementation_register,
        legacy.check_discovery,
    ):
        run_legacy_check(fn, failures)

    check_current_date_and_taxonomy(failures)

    if failures:
        print(f"Concurso 36/2012 complete-record v2 validation failed ({len(failures)} issue(s)):")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(
        "Concurso 36/2012 complete-record v2 validation passed: historical denominator/privacy/discovery controls preserved; "
        "8-Feb Auto / 9-Feb judge signature / 14-Feb LAJ signature / 15-Feb notification layers locked; "
        "4-June taxonomy and dual-lens governance preserved."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
