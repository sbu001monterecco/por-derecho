#!/usr/bin/env python3
"""Validate the bilingual David Espejo evidence node and its structured register."""
from __future__ import annotations

import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ES = ROOT / "es/david-espejo-perito-forense/index.html"
EN = ROOT / "en/david-espejo-expert-witness/index.html"
DATA = ROOT / "assets/data/david-espejo-expert-evidence-v2.json"
SITEMAP = ROOT / "sitemap-david-espejo.xml"
ROBOTS = ROOT / "robots.txt"
ES_NOTEBOOK = ROOT / "es/cuaderno-juridico/index.html"
EN_NOTEBOOK = ROOT / "en/legal-notebook/index.html"


def fail(message: str) -> None:
    raise AssertionError(message)


def require(text: str, fragment: str, label: str) -> None:
    if fragment not in text:
        fail(f"{label}: missing required fragment: {fragment!r}")


def forbid(text: str, fragment: str, label: str) -> None:
    if fragment in text:
        fail(f"{label}: forbidden fragment found: {fragment!r}")


def main() -> int:
    paths = [ES, EN, DATA, SITEMAP, ROBOTS, ES_NOTEBOOK, EN_NOTEBOOK]
    missing = [str(p.relative_to(ROOT)) for p in paths if not p.exists()]
    if missing:
        fail(f"missing required files: {missing}")

    es = ES.read_text(encoding="utf-8")
    en = EN.read_text(encoding="utf-8")
    robots = ROBOTS.read_text(encoding="utf-8")
    es_notebook = ES_NOTEBOOK.read_text(encoding="utf-8")
    en_notebook = EN_NOTEBOOK.read_text(encoding="utf-8")
    data = json.loads(DATA.read_text(encoding="utf-8"))

    require(es, "Cuatro preguntas que nunca deben fundirse", "Spanish page")
    require(en, "Four questions must never be collapsed", "English page")
    forbid(es, "Tres preguntas que nunca deben fundirse", "Spanish page")
    forbid(en, "Three questions must never be collapsed", "English page")
    forbid(es, "Expejo", "Spanish public page")
    forbid(es, "Esperjo", "Spanish public page")

    shared_markers = [
        ("documento 3", "document 3"),
        ("documento 5", "document 5"),
        ("24 julio 2023", "24 July 2023"),
        ("42 minutos", "42 minutes"),
        ("VIDISPIR", "VIDISPIR"),
        ("JSON v2", "JSON v2"),
    ]
    for es_marker, en_marker in shared_markers:
        require(es, es_marker, "Spanish page")
        require(en, en_marker, "English page")

    for fragment in [
        "el soporte era corrupto",
        "la grabación fue manipulada",
        "los cuatro informes fueron presentados como cuatro anexos",
        "declaró sin revisar los informes",
    ]:
        forbid(es.lower(), fragment.lower(), "Spanish page")
    for fragment in [
        "the medium was corrupt",
        "the recording was manipulated",
        "all four reports were filed as four annexes",
        "gave evidence without reviewing the reports",
    ]:
        forbid(en.lower(), fragment.lower(), "English page")

    if data.get("schema") != "por-derecho.expert-evidence-status.v2":
        fail("structured register schema must be v2")
    if data.get("status") != "controlling_structured_register":
        fail("v2 register must declare itself controlling")

    report_ids = {item["report_id"] for item in data.get("reports", [])}
    required_reports = {
        "DES-2018-05-10-VALUATION-LIQUIDATION-DRAFT",
        "DES-2018-06-11-CEXP-RIGHTS",
        "DES-2018-07-10-COMMUNITY-DEBT",
        "DES-2018-SWAP-PLEDGED-DEPOSIT",
        "DES-2018-GENERAL-ECONOMIC-NOTE",
    }
    if not required_reports.issubset(report_ids):
        fail(f"missing report IDs: {sorted(required_reports - report_ids)}")

    event_ids = {item["event_id"] for item in data.get("events", [])}
    required_events = {
        "DES-EVT-2019-04-23-FOUR-SIGNED-FINALS",
        "DES-EVT-2019-04-24-LPB-OPPOSITION",
        "DES-EVT-2023-07-24-COURT-FILE-ACCESS",
        "DES-EVT-2023-07-25-WITNESS-EXPERT",
        "DES-EVT-2023-09-28-JUDGMENT-USE",
    }
    if not required_events.issubset(event_ids):
        fail(f"missing event IDs: {sorted(required_events - event_ids)}")

    audiovisual = data.get("audiovisual_control", {})
    if audiovisual.get("raw_difference_minutes") != 42:
        fail("raw audiovisual arithmetic difference must remain 42 minutes")
    if audiovisual.get("current_status") != "unresolved_not_proof_of_manipulation":
        fail("audiovisual status must remain unresolved, not proof of manipulation")

    if len(data.get("open_evidence_tasks", [])) < 6:
        fail("open evidence register must preserve all current recovery tasks")

    ET.parse(SITEMAP)
    sitemap_text = SITEMAP.read_text(encoding="utf-8")
    require(sitemap_text, "/es/david-espejo-perito-forense/", "Dedicated sitemap")
    require(sitemap_text, "/en/david-espejo-expert-witness/", "Dedicated sitemap")
    require(
        robots,
        "Sitemap: https://sbu001monterecco.github.io/por-derecho/sitemap-david-espejo.xml",
        "robots.txt",
    )
    require(es_notebook, "../david-espejo-perito-forense/", "Spanish legal notebook")
    require(en_notebook, "../david-espejo-expert-witness/", "English legal notebook")

    print("David Espejo evidence sync validation passed")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
