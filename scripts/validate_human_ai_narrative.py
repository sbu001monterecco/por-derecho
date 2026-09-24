#!/usr/bin/env python3
"""Deterministic structural guard for the Por Derecho human-story / AI narrative.

This validator checks publication structure and required evidential boundaries.
It does not adjudicate factual truth or legal conclusions.
"""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]

RULE = ROOT / "governance/HUMAN_STORY_AI_LEGAL_RECOVERY_NARRATIVE_PROTOCOL_24SEP2026.md"
AGENTS = ROOT / "AGENTS.md"
EN = ROOT / "en/one-person-one-record-ai-legal-recovery/index.html"
ES = ROOT / "es/una-persona-un-expediente-ia-recuperacion-juridica/index.html"
EN_SUPPORT = ROOT / "en/public-interest-support/index.html"
ES_SUPPORT = ROOT / "es/apoyo-interes-publico/index.html"

CONTROL_ID = "PD-GOV-HUMAN-AI-20260924-01"


def read(path: Path) -> str:
    if not path.exists():
        raise ValueError(f"Missing required file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def validate() -> dict:
    errors = []
    rule = read(RULE)
    agents = read(AGENTS)
    en = read(EN)
    es = read(ES)
    en_support = read(EN_SUPPORT)
    es_support = read(ES_SUPPORT)

    for label, body in (("rule", rule), ("AGENTS", agents)):
        if CONTROL_ID not in body:
            errors.append(f"{label} missing control ID {CONTROL_ID}")

    required_en = [
        "I did not set out to build legal AI",
        "6 June 2018",
        "7 June 2018",
        "12 June 2018",
        "13 June 2018",
        "provisionally dismissed",
        "one person against the",
        "not a claim that every judge, prosecutor, lawyer, official or company",
        "AI asks. Humans decide.",
        "Help the capacity. Do not buy the answer.",
        "historical snapshot figures",
    ]
    required_es = [
        "No me propuse construir IA jurídica",
        "6 junio 2018",
        "7 junio 2018",
        "12 junio 2018",
        "13 junio 2018",
        "archivada provisionalmente",
        "una persona contra el",
        "No es una afirmación de que todos los jueces, fiscales, abogados, funcionarios o empresas",
        "La IA pregunta. Los humanos deciden.",
        "Ayude a la capacidad. No compre la respuesta.",
        "cifras históricas",
    ]

    for phrase in required_en:
        if phrase not in en:
            errors.append(f"English story missing required control phrase: {phrase}")
    for phrase in required_es:
        if phrase not in es:
            errors.append(f"Spanish story missing required control phrase: {phrase}")

    if "../one-person-one-record-ai-legal-recovery/" not in en_support:
        errors.append("English support page does not link to human story")
    if "../una-persona-un-expediente-ia-recuperacion-juridica/" not in es_support:
        errors.append("Spanish support page does not link to human story")

    for rel in (
        "en/ona-hotels-insolvency-exit-36-2012/index.html",
        "es/ona-hotels-salida-concurso-36-2012/index.html",
        "en/sun-park-takeover-7-june-2018/index.html",
        "es/toma-control-sun-park-7-junio-2018/index.html",
    ):
        if not (ROOT / rel).exists():
            errors.append(f"Required story destination missing: {rel}")

    forbidden_en = [
        "everyone was in on it",
        "all local institutions acted together",
        "ai proved the crime",
    ]
    forbidden_es = [
        "todas las instituciones locales actuaron juntas",
        "la ia probó el delito",
    ]
    low_en, low_es = en.lower(), es.lower()
    for phrase in forbidden_en:
        if phrase in low_en:
            errors.append(f"English story contains prohibited inflation: {phrase}")
    for phrase in forbidden_es:
        if phrase in low_es:
            errors.append(f"Spanish story contains prohibited inflation: {phrase}")

    return {
        "schema": "por-derecho.human-ai-narrative-validation.v1",
        "control_id": CONTROL_ID,
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "checked": [
            str(p.relative_to(ROOT))
            for p in (RULE, AGENTS, EN, ES, EN_SUPPORT, ES_SUPPORT)
        ],
        "boundary": "Structural publication guard only; not factual or legal adjudication.",
    }


if __name__ == "__main__":
    result = validate()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if result["errors"]:
        sys.exit(1)
