#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

V2 = ROOT / "assets/data/concurso36-what-court-ordered-v2.json"
DUAL = ROOT / "assets/data/concurso36-procedural-taxonomy-judicial-ac-dual-lens-20260829.json"
START = ROOT / "CHATGPT_START_HERE_CONCURSO36_DUAL_LENS_GOVERNANCE.md"
CLOSEOUT = ROOT / "archive/CONCURSO36_DUAL_LENS_PROCEDURAL_TAXONOMY_CLOSEOUT_29AUG2026.md"
JS = ROOT / "assets/concurso36-continuity-governance.js"
ES_PAGE = ROOT / "es/concurso-36-2012-que-ordeno-el-juzgado/index.html"
EN_PAGE = ROOT / "en/concurso-36-2012-what-the-court-ordered/index.html"


def load_json(path: Path):
    assert path.exists(), f"missing required file: {path.relative_to(ROOT)}"
    return json.loads(path.read_text(encoding="utf-8"))


def text(path: Path) -> str:
    assert path.exists(), f"missing required file: {path.relative_to(ROOT)}"
    return path.read_text(encoding="utf-8")


def require(haystack: str, needle: str, label: str):
    assert needle in haystack, f"{label}: missing {needle!r}"


def main() -> None:
    v2 = load_json(V2)
    dual = load_json(DUAL)

    assert v2.get("schema_version") == "2.0"
    sup = v2.get("supersession", {})
    assert sup.get("legacy_file") == "assets/data/concurso36-what-court-ordered-v1.json"

    c = v2.get("primary_date_control", {})
    assert c.get("id") == "C36-2018-02-08-CREDITOR"
    assert c.get("body_date") == "2018-02-08"
    assert str(c.get("judge_signature", "")).startswith("2018-02-09")
    assert str(c.get("laj_signature", "")).startswith("2018-02-14")
    assert c.get("notification_annotation") == "NOTIFICADO 15/02/2018"
    assert abs(float(c.get("special_privilege_total_eur")) - 9052251.69) < 0.01
    require(c.get("critical_rule_es", ""), "no de cuantía", "8-Feb rule ES")
    require(c.get("critical_rule_en", ""), "not the amount", "8-Feb rule EN")

    j = v2.get("critical_comparator_4_june_2018", {})
    assert j.get("body_date") == "2018-06-04"
    assert j.get("not_an_incidente_concursal") is True
    assert j.get("not_verified_as_definitive_text_modification") is True
    assert abs(float(j.get("operative_total_eur")) - 13165832.36) < 0.01
    require(j.get("remedy_feature", ""), "214.4", "4-Jun remedy control")
    require(j.get("user_position_es", ""), "no era un incidente concursal", "4-Jun user position ES")

    community = v2.get("community_fees_comparator", {})
    assert community.get("date") == "2017-01-20"
    assert community.get("procedural_class") == "MODIFICACION_TEXTOS_DEFINITIVOS"
    require(community.get("status", ""), "SEPARATE INCIDENT DOCKET NOT YET VERIFIED", "Community taxonomy")

    pieces = {x.get("piece") for x in v2.get("verified_incidentes_concursales_located", [])}
    assert "0000007/2012" in pieces and "0000008/2012" in pieces

    assert len(v2.get("definitive_text_change_gate", [])) >= 8
    gov = v2.get("judicial_review_governance", {})
    require(gov.get("declared_position_es", ""), "patrón acumulativo", "multi-act allegation ES")
    require(gov.get("declared_position_en", ""), "cumulative pattern", "multi-act allegation EN")

    assert dual.get("critical_4_june_2018_comparator", {}).get("4_june_2018", {}).get("status", "").startswith("LIQUIDATION-PLAN CLARIFICATION")
    assert len(dual.get("definitive_text_change_gate", {}).get("required_fields", [])) >= 8
    dual_pieces = {x.get("piece") for x in dual.get("verified_incidentes_concursales_located", [])}
    assert pieces.issubset(dual_pieces)
    require(dual.get("declared_position", {}).get("en", ""), "cumulative pattern", "dual-lens allegation")

    start = text(START)
    closeout = text(CLOSEOUT)
    js = text(JS)
    es_page = text(ES_PAGE)
    en_page = text(EN_PAGE)

    for label, body in [("start", start), ("closeout", closeout), ("js", js), ("ES page", es_page), ("EN page", en_page)]:
        require(body, "9.052", label)
        require(body, "13.165", label)

    require(start, "NOTIFICADO 15/02/2018", "start notification layer")
    require(closeout, "NOTIFICADO 15/02/2018", "closeout notification layer")
    require(es_page, "8 de febrero de 2018", "ES corrected order date")
    require(es_page, "notificación", "ES notification distinction")
    require(en_page, "8 February 2018", "EN corrected order date")
    require(en_page, "notification", "EN notification distinction")

    for label, body in [("ES page", es_page), ("EN page", en_page)]:
        require(body, "Article 59", label)
        require(body, "97 bis", label)
        require(body, "0000007/2012", label)
        require(body, "0000008/2012", label)

    require(js, "concurso36-procedural-taxonomy-judicial-ac-dual-lens-20260829.json", "continuity renderer")
    require(js, "dual-lens-governance", "continuity renderer")

    print("OK: Concurso 36/2012 primary creditor-order date, 4-June taxonomy, final-text gate and dual-lens governance validated.")


if __name__ == "__main__":
    main()
