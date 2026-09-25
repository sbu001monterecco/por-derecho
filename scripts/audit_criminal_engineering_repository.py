#!/usr/bin/env python3
"""Unitary public-repository audit for the alleged criminal-engineering investigation.

This audit scans every public Spanish/English HTML page and runtime JavaScript file.
It identifies publication architecture, actor coverage, genuinely unqualified high-risk
wording, judge/LAJ conflation risk and privacy leakage. It does not decide criminal
liability or treat term frequency, institutional names or source quotations as proof.
"""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = {
    "es": ROOT / "es" / "ingenieria-forense-criminal-sun-park" / "index.html",
    "en": ROOT / "en" / "sun-park-criminal-engineering-investigation" / "index.html",
}
MODULE = ROOT / "assets" / "criminal-engineering-investigation-20260819.js"
LOADER = ROOT / "assets" / "reverse-engineering-360-20260819.js"
DATA = ROOT / "assets" / "data" / "criminal-engineering-investigation-v1.json"

REQUIRED_MARKERS = {
    CANONICAL["es"]: [
        "ALEGACIÓN CENTRAL DE POR DERECHO",
        "NO HALLAZGO JUDICIAL",
        "Gil Marer y Aweswell alegan una sola empresa continuada de criminalidad económica, desarrollada mediante adopción sucesiva y división de funciones.",
        "no califica los hechos como delito continuado o permanente",
        "Las ocho fases de la presunta ingeniería",
        "LAJ / oficina judicial",
        "Escala de facilitación E0–E7",
        "Prueba en entorno hostil",
        "Beneficio y daño",
        "Derecho de respuesta",
    ],
    CANONICAL["en"]: [
        "POR DERECHO CENTRAL ALLEGATION",
        "NOT A JUDICIAL FINDING",
        "Gil Marer and Aweswell allege one continuing economic-criminal enterprise, advanced through successive adoption and divided functions.",
        "does not characterise the conduct as a continuing or permanent offence",
        "The eight phases of the alleged engineering",
        "LAJ / judicial office",
        "E0–E7 enabler ladder",
        "Evidence in a hostile environment",
        "Benefit and harm",
        "Right of response",
    ],
    MODULE: [
        "data-criminal-engineering-gateway",
        "allegation, not finding",
        "una sola empresa continuada de criminalidad económica",
        "one continuing economic-criminal enterprise",
        "no califica los hechos como delito continuado o permanente",
        "does not characterise the conduct as a continuing or permanent offence",
        "authority + knowledge + duty",
    ],
    LOADER: [
        "criminal-engineering-investigation-20260819.js",
        "data-criminal-engineering-investigation-loader",
    ],
}

ACTOR_PATTERNS = {
    "acosta_matos_cam_hnt": re.compile(r"Acosta Matos|\bCAM\b|Hotel New Trend|\bHNT\b", re.I),
    "ricpe": re.compile(r"RIC Private Equity|\bRICPE\b", re.I),
    "insolvency_administration": re.compile(r"Administraci[oó]n Concursal|Insolvency Administration|Administrador Concursal|Insolvency Administrator", re.I),
    "judge": re.compile(r"\bjuez\b|\bjudge\b|magistrad[oa]|Mercantile Court", re.I),
    "laj_judicial_office": re.compile(r"\bLAJ\b|oficina judicial|judicial office|Letrad[oa] de la Administraci[oó]n de Justicia", re.I),
    "notary_registry": re.compile(r"notar(?:io|ia|y)|Registro de la Propiedad|Land Registry|registrador", re.I),
    "valuers_experts": re.compile(r"ACT[ÚU]A|GESVALT|tasador|valuer|perito|expert", re.I),
    "authorities_supervisors": re.compile(r"CNMV|Fiscal[ií]a|prosecution|CGPJ|supervisor|autoridad|authority|FEDER|ERDF", re.I),
}

ARCHITECTURE_PATTERNS = {
    "eight_phase_sequence": re.compile(r"entrada estrat[eé]gica|strategic entry|normalizaci[oó]n operativa|operational normalisation", re.I),
    "enabler_ladder": re.compile(r"E0.{0,120}E7|enabler ladder|escala de facilitaci[oó]n", re.I | re.S),
    "false_premise_propagation": re.compile(r"premisa.{0,60}(?:cadena|formal|aguas arriba)|false[- ]premise|upstream premise", re.I | re.S),
    "evidence_preservation": re.compile(r"preservaci[oó]n de (?:la )?prueba|evidence preservation|hostile environment|entorno hostil", re.I),
    "retaliation": re.compile(r"represalia|retaliation|informant|informante|whistleblower", re.I),
    "benefit_flow": re.compile(r"flujo.{0,35}(?:beneficio|dinero|valor)|benefit.{0,35}flow|follow value|seguir valor", re.I | re.S),
    "irreversibility": re.compile(r"irreversibil|harder to reverse|dif[ií]cil de revertir", re.I),
    "strongest_defence": re.compile(r"defensa m[aá]s fuerte|strongest defence|strongest alternative", re.I),
    "right_of_response": re.compile(r"derecho de respuesta|right of response", re.I),
}

HIGH_RISK_PATTERNS = {
    "economic_criminal_enterprise": re.compile(r"empresa continuada de criminalidad econ[oó]mica|continuing economic-criminal enterprise", re.I),
    "criminal_organisation": re.compile(r"organizaci[oó]n criminal|criminal organi[sz]ation", re.I),
    "proven_conspiracy": re.compile(r"conspiraci[oó]n (?:probada|demostrada)|proven conspiracy", re.I),
    "bribery_or_corruption": re.compile(r"soborno|cohecho|bribery|corrupci[oó]n", re.I),
    "judicial_prevarication": re.compile(r"prevaricaci[oó]n judicial|judicial prevarication", re.I),
    "money_laundering": re.compile(r"blanqueo de capitales|money laundering", re.I),
    "collective_guilt": re.compile(r"todos (?:son|fueron) (?:culpables|c[oó]mplices)|all (?:are|were) (?:guilty|complicit)", re.I),
}

QUALIFIERS = re.compile(
    r"alegaci[oó]n|acusaci[oó]n|hip[oó]tesis|presunt[oa]|no hallazgo|no judicial finding|"
    r"allegation|accusation|i accuse|my accusation|alleged|hypothesis|not a finding|"
    r"no se afirma|no afirma|no establece|no prueba|no constituye|no basta|no equivale|"
    r"does not allege|does not establish|does not prove|does not constitute|not by itself|"
    r"requires evidence|requires separate|exige prueba|elemento subjetivo|subjective element|"
    r"umbral penal|criminal threshold|strongest defence|defensa m[aá]s fuerte",
    re.I,
)

OFFICIAL_NAME_OR_NEUTRAL_CONTEXT = re.compile(
    r"Fiscal[ií]a Especial contra la Corrupci[oó]n y la Criminalidad Organizada|"
    r"Special Prosecutor(?:'s)? Office against Corruption|"
    r"Comisi[oó]n para la Integridad P[uú]blica y Lucha contra la Corrupci[oó]n|"
    r"Servicio Ejecutivo de la Comisi[oó]n de Prevenci[oó]n del Blanqueo de Capitales|"
    r"SEPBLAC|anti-corruption authority|anti-money laundering authority|"
    r"data-search=.{0,120}(?:corrupci[oó]n|blanqueo de capitales)",
    re.I | re.S,
)

SOURCE_QUOTE_CONTEXT = re.compile(
    r"<blockquote|</blockquote>|original-note|translation:|traducci[oó]n:|"
    r"el decreto dijo|the decree said|texto literal|verbatim|source quote",
    re.I,
)

# Exact office-function tests. Word boundaries prevent false hits such as "preserved"
# being mistaken for the verb "served", and "judges" being mistaken for "the judge".
JUDGE_LAJ_CONFLATION = re.compile(
    r"\b(?:el juez|la jueza|the judge)\b"
    r"(?:(?!\bLAJ\b|oficina judicial|judicial office|Letrad[oa] de la Administraci[oó]n de Justicia).){0,100}"
    r"\b(?:notific[oó]|certific[oó] la firmeza|tramit[oó]|dio traslado|served|certified finality|docketed)\b|"
    r"\b(?:la LAJ|el LAJ|the LAJ)\b"
    r"(?:(?!\bjuez\b|\bjudge\b).){0,100}"
    r"\b(?:decidi[oó] el fondo|sentenci[oó]|autoriz[oó] la adjudicaci[oó]n|authorised the adjudication|decided the merits|entered judgment)\b",
    re.I | re.S,
)

PRIVATE_PATTERNS = {
    "gmail_message_id": re.compile(r"\b[0-9a-f]{16}\b"),
    "drive_document_id": re.compile(r"\b1[A-Za-z0-9_-]{24,}\b"),
    "sha256_private_source": re.compile(r"SHA-256\s*[:=]\s*[0-9a-f]{64}", re.I),
    "attachment_identifier": re.compile(r"ANGjdJ[A-Za-z0-9_-]{25,}"),
}


def public_files() -> list[Path]:
    files: list[Path] = []
    for base, suffixes in ((ROOT / "es", {".html"}), (ROOT / "en", {".html"}), (ROOT / "assets", {".js"})):
        if not base.exists():
            continue
        files.extend(path for path in base.rglob("*") if path.is_file() and path.suffix in suffixes)
    return sorted(files)


def context(text: str, start: int, end: int, radius: int = 240) -> str:
    return re.sub(r"\s+", " ", text[max(0, start-radius):min(len(text), end+radius)]).strip()


def is_reviewable_high_risk(snippet: str) -> bool:
    if OFFICIAL_NAME_OR_NEUTRAL_CONTEXT.search(snippet):
        return False
    if SOURCE_QUOTE_CONTEXT.search(snippet) and not re.search(r"adopt(?:o|s)|endorse|sostengo|i accuse|acuso", snippet, re.I):
        return False
    return not QUALIFIERS.search(snippet)


def main() -> int:
    failures: list[dict[str, str]] = []
    review_items: list[dict[str, str]] = []
    actor_files: dict[str, set[str]] = defaultdict(set)
    architecture_files: dict[str, set[str]] = defaultdict(set)
    scanned = 0

    for path, markers in REQUIRED_MARKERS.items():
        if not path.is_file():
            failures.append({"type": "missing_required_file", "path": str(path.relative_to(ROOT))})
            continue
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            if marker.lower() not in text.lower():
                failures.append({"type": "missing_required_marker", "path": str(path.relative_to(ROOT)), "marker": marker})

    try:
        data = json.loads(DATA.read_text(encoding="utf-8"))
        if len(data.get("phases", [])) != 8:
            failures.append({"type": "data_phase_count", "path": str(DATA.relative_to(ROOT)), "detail": "expected exactly 8 phases"})
        if len(data.get("enabler_ladder", [])) != 8:
            failures.append({"type": "data_enabler_count", "path": str(DATA.relative_to(ROOT)), "detail": "expected E0-E7"})
    except Exception as exc:
        failures.append({"type": "invalid_data_json", "path": str(DATA.relative_to(ROOT)), "detail": repr(exc)})

    for path in public_files():
        scanned += 1
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        rel = str(path.relative_to(ROOT))

        for actor, pattern in ACTOR_PATTERNS.items():
            if pattern.search(text):
                actor_files[actor].add(rel)
        for topic, pattern in ARCHITECTURE_PATTERNS.items():
            if pattern.search(text):
                architecture_files[topic].add(rel)

        for risk_id, pattern in HIGH_RISK_PATTERNS.items():
            for match in pattern.finditer(text):
                snippet = context(text, match.start(), match.end())
                if is_reviewable_high_risk(snippet):
                    review_items.append({
                        "type": "high_risk_language_without_nearby_qualifier",
                        "risk": risk_id,
                        "path": rel,
                        "match": match.group(0),
                        "context": snippet,
                    })

        for match in JUDGE_LAJ_CONFLATION.finditer(text):
            review_items.append({
                "type": "possible_judge_laj_conflation",
                "path": rel,
                "match": re.sub(r"\s+", " ", match.group(0)).strip(),
                "context": context(text, match.start(), match.end()),
            })

    new_public_text = "\n".join([
        CANONICAL["es"].read_text(encoding="utf-8") if CANONICAL["es"].is_file() else "",
        CANONICAL["en"].read_text(encoding="utf-8") if CANONICAL["en"].is_file() else "",
        MODULE.read_text(encoding="utf-8") if MODULE.is_file() else "",
    ])
    for private_id, pattern in PRIVATE_PATTERNS.items():
        match = pattern.search(new_public_text)
        if match:
            failures.append({"type": "private_identifier_leak", "pattern": private_id, "match": match.group(0)})

    required_actor_coverage = [
        "acosta_matos_cam_hnt", "ricpe", "insolvency_administration", "judge",
        "laj_judicial_office", "notary_registry", "valuers_experts", "authorities_supervisors",
    ]
    for actor in required_actor_coverage:
        if not actor_files.get(actor):
            failures.append({"type": "missing_actor_coverage", "actor": actor})

    required_architecture = [
        "eight_phase_sequence", "enabler_ladder", "false_premise_propagation",
        "evidence_preservation", "retaliation", "benefit_flow", "irreversibility",
        "strongest_defence", "right_of_response",
    ]
    for topic in required_architecture:
        if not architecture_files.get(topic):
            failures.append({"type": "missing_architecture_coverage", "topic": topic})

    report = {
        "audit": "sun-park-criminal-engineering-public-repository",
        "control_date": "2026-08-19",
        "scanned_public_files": scanned,
        "status": "FAIL" if failures else ("PASS_WITH_REVIEW" if review_items else "PASS"),
        "failures": failures,
        "review_item_count": len(review_items),
        "review_items": review_items[:100],
        "actor_coverage": {key: {"file_count": len(value), "sample": sorted(value)[:12]} for key, value in actor_files.items()},
        "architecture_coverage": {key: {"file_count": len(value), "sample": sorted(value)[:12]} for key, value in architecture_files.items()},
        "interpretation": "Coverage and wording audit only; no criminal liability is inferred from term frequency or route presence. Official names, source quotations and expressly qualified allegations are excluded from the high-risk review count."
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
