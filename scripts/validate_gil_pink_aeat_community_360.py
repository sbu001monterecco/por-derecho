#!/usr/bin/env python3
"""Anti-regression gate for the 22-Aug-2026 Gil/Pink/AEAT/Community control set."""

from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


def text(rel: str) -> str:
    path = ROOT / rel
    if not path.is_file():
        raise AssertionError(f"missing required file: {rel}")
    return path.read_text(encoding="utf-8")


def require(rel: str, *markers: str) -> None:
    body = text(rel)
    for marker in markers:
        if marker not in body:
            raise AssertionError(f"{rel}: missing marker {marker!r}")


require(
    "CHATGPT_START_HERE.md",
    "Declarations 005–010",
    "BOE-A-2019-14965 records Pink's NIF revocation",
    "repository arithmetic totals approximately 75.671%",
    "no institutional AEAT conflict is proved",
)
require(
    "archive/declarations/010_GIL_PRESSURE_CONTEXT_PINK_ADMINISTRATION_NULLITY_AEAT_COMMUNITY_PUBLICATION_20260822.md",
    "pudo contribuir",
    "No afirmo sin prueba",
    "revocación del NIF B76564517",
    "no equivale a extinción societaria",
    "sentencia de 24 de noviembre de 2015",
    "No existe actualmente prueba actor-específica bastante",
)
require(
    "archive/CORRECTION_REGISTER.md",
    "| CR-067 |",
    "| CR-068 |",
    "| CR-069 |",
    "| CR-070 |",
)
require("archive/MISSING_EVIDENCE_REGISTER.md", "| ME-069 | Current Pink corporate")
require(
    "evidence/community/ACTA_22JUN2011_PUBLIC_REDACTED_EDITION.md",
    "2e30ad64047b10a79d12de9c5eee0202f31e9b0c14ed26de14e57767d21c896a",
    "75.671%",
    "6.930%",
    "two full-time workers",
    "does **not** prove actual workers",
    "structured editorial digest",
    "€1,040 plus tax for the 2011 property-administration package",
)
require(
    "evidence/community/COMMUNITY_PAMANIL_COMMUNICATIONS_PUBLIC_DIGITAL_INDEX.md",
    "Structured public redacted digest",
    "public communications index",
    "does not establish that figure as recurring annually",
)
require(
    "archive/GIL_PINK_TOTAL_NULLITY_AEAT_NEUTRALITY_COMMUNITY_360_REVERSE_ENGINEERING_22AUG2026.md",
    "whole-nullity theory is serious but unadjudicated",
    "24-November-2015",
    "No actor-specific proof presently establishes institutional AEAT conflict",
    "Revocation is not extinction",
)

for rel, markers in {
    "en/community-instrumentalisation/communications-pamanil/index.html": (
        "75.671%",
        "6.930%",
        "structured public redacted digest",
        "COMMUNITY_PAMANIL_COMMUNICATIONS_PUBLIC_DIGITAL_INDEX.md",
    ),
    "es/comunidad-instrumentalizacion/comunicaciones-pamanil/index.html": (
        "75,671%",
        "6,930%",
        "síntesis pública estructurada y redactada",
        "COMMUNITY_PAMANIL_COMMUNICATIONS_PUBLIC_DIGITAL_INDEX.md",
    ),
    "en/pink-canary-aeat-national-court/index.html": (
        "29 Jul 2020",
        "4 / 15 Mar 2022",
        "No actor-specific evidence presently proves institutional AEAT conflict",
        "BOE-A-2019-14965",
    ),
    "es/pink-canary-aeat-audiencia-nacional/index.html": (
        "29 jul 2020",
        "4 / 15 mar 2022",
        "No existe hoy prueba actor-específica de conflicto institucional",
        "BOE-A-2019-14965",
    ),
}.items():
    require(rel, *markers)

for rel in ("sitemap.xml", "sitemap-community-governance.xml"):
    ET.parse(ROOT / rel)
    require(
        rel,
        "communications-pamanil",
        "comunicaciones-pamanil",
        "pink-canary-aeat-national-court",
        "pink-canary-aeat-audiencia-nacional",
        "two-competing-governance-records",
        "dos-registros-gobernanza-competidores",
    )

print("GIL / PINK / AEAT / COMMUNITY 360 GATE: PASS")
