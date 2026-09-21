#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
REG = ROOT / "assets/data/por-derecho-second-pair-applications.json"
ES = ROOT / "es/por-derecho/aplicaciones-y-colaboracion/index.html"
EN = ROOT / "en/por-derecho/applications-and-collaboration/index.html"
STD = ROOT / "research/por-derecho/second-pair-of-eyes/case-application-standard.md"

errors = []

def require(condition, message):
    if not condition:
        errors.append(message)

for path in (REG, ES, EN, STD):
    require(path.exists(), f"missing required file: {path.relative_to(ROOT)}")

if REG.exists():
    data = json.loads(REG.read_text(encoding="utf-8"))
    require(data.get("method") == "Por Derecho — El Segundo Par de Ojos", "unexpected method identity")
    require(data.get("coreChecks") == ["source","authority","perimeter","contradiction","consequence","reversibility"], "core six-check sequence changed")
    cases = {c["id"]: c for c in data.get("cases", [])}
    for cid in ("ICALPA-DIP-80-2026", "ICALPA-DIP-79-2026", "ICAM-PILOT", "CCACM-PILOT"):
        require(cid in cases, f"missing application registry entry: {cid}")
    require(cases.get("ICALPA-DIP-80-2026", {}).get("state") == "reference-implementation", "DIP 80 must remain reference implementation")
    require(cases.get("ICALPA-DIP-79-2026", {}).get("state") == "next-live-application", "DIP 79 must remain next live application")
    require(cases.get("ICAM-PILOT", {}).get("state") == "synthetic-institutional-pilot", "ICAM must remain synthetic-pilot until expressly changed")
    require(cases.get("CCACM-PILOT", {}).get("state") == "synthetic-institutional-pilot", "CCACM must remain synthetic-pilot until expressly changed")
    for c in data.get("cases", []):
        require(c.get("officialAdoptionClaimed") is False, f"institutional adoption must not be implied for {c.get('id')}")
    gov = data.get("governance", {})
    for key in ("humanDecisionOnly", "noGuiltScoring", "silenceIsNotAdmission", "noCrossCaseEvidenceReuseWithoutHumanRelevanceDecision", "publicMethodProtectedFile", "institutionalEndorsementNeverImplied"):
        require(gov.get(key) is True, f"governance safeguard disabled: {key}")

if ES.exists():
    text = ES.read_text(encoding="utf-8")
    for token in ("Fuente", "Autoridad", "Perímetro", "Contradicción", "Consecuencia", "Reversibilidad", "DIP 80/2026", "DIP 79/2026", "ICAM", "CCACM"):
        require(token in text, f"ES hub missing: {token}")
    require("No se afirma colaboración" in text or "No se afirma adopción" in text, "ES institutional non-endorsement boundary missing")

if EN.exists():
    text = EN.read_text(encoding="utf-8")
    for token in ("Source", "Authority", "Perimeter", "Contradiction", "Consequence", "Reversibility", "DIP 80/2026", "DIP 79/2026", "ICAM", "CCACM"):
        require(token in text, f"EN hub missing: {token}")
    require("No collaboration" in text or "No adoption" in text, "EN institutional non-endorsement boundary missing")

if errors:
    print("Second Pair application validation FAILED")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print("Second Pair application validation PASSED")
