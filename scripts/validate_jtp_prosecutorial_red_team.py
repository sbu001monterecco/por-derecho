#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
errors: list[str] = []

def read(path: str) -> str:
    p = ROOT / path
    if not p.exists():
        errors.append(f"missing file: {path}")
        return ""
    return p.read_text(encoding="utf-8")

def require(path: str, markers: list[str]) -> None:
    text = read(path)
    for marker in markers:
        if marker not in text:
            errors.append(f"{path}: missing marker {marker!r}")

require("en/estate-payment-counsel-independence/index.html", [
    "This is not presented as a fee dispute.",
    'id="prosecutorial-spine"',
    "CRIMINAL-PROSECUTORIAL SPINE",
    "Criminal first means element first, not offence-label first.",
    'id="adversarial-test"',
    "The strongest adverse reading is shown, not hidden.",
    'id="proof-plan"',
    "Evidence that would narrow or falsify material parts",
    "Priority prosecutor production",
    "The 28 May reply was conditional and information-seeking and is not used as consent or ratification.",
    "Parrilla’s final 11 June proposal was expressly rejected on 12 June.",
    "no direct transfer",
    "bank trace is incomplete",
    "Closing was not guaranteed.",
    "Criminal / prosecutorial spine",
    "Civil / mercantile / insolvency predicates and remedies",
    "JTP_PAYMENT_FUNDED_EXIT_HOSTILE_READER_RED_TEAM_24SEP2026.md",
    "Contemporaneous criminal lens — 4 January 2019.",
    "By 1 June incoming counsel was already treating Parrilla as no longer LPB counsel",
    "24 September 2026 deep-source sweep:",
    "JTP_ONA_DEEP_SOURCE_SWEEP_24SEP2026.md",
])

require("es/pago-masa-independencia-defensa/index.html", [
    "No se presenta como una disputa de honorarios.",
    'id="prosecutorial-spine"',
    "EJE PENAL-FISCAL",
    "Penal primero significa elementos primero, no etiquetas delictivas primero.",
    'id="adversarial-test"',
    "La mejor lectura adversa se muestra, no se oculta.",
    'id="proof-plan"',
    "Prueba que reduciría o falsaría partes materiales",
    "Producción prioritaria para Fiscalía",
    "La respuesta del 28 de mayo fue condicional e informativa y no se usa como consentimiento o ratificación.",
    "La propuesta final de 11 de junio fue rechazada expresamente el 12 de junio.",
    "No existe transferencia CAM→JTP.",
    "trazabilidad bancaria está incompleta",
    "El cierre no estaba garantizado.",
    "Eje penal / fiscal",
    "Presupuestos y remedios civil / mercantil / concursal",
    "JTP_PAYMENT_FUNDED_EXIT_HOSTILE_READER_RED_TEAM_24SEP2026.md",
    "Óptica penal contemporánea — 4 de enero de 2019.",
    "Ya el 1 de junio el letrado entrante trataba a Parrilla como antiguo letrado de LPB",
    "Barrido profundo de fuentes · 24 septiembre 2026:",
    "JTP_ONA_DEEP_SOURCE_SWEEP_24SEP2026.md",
])

require("en/pre-7-june-2018-funded-ona-exit/index.html", [
    "../estate-payment-counsel-independence/",
])
require("es/salida-financiada-ona-antes-7-junio-2018/index.html", [
    "../pago-masa-independencia-defensa/",
])
require("en/counsel-defence-continuity/index.html", [
    "../estate-payment-counsel-independence/",
])
require("es/continuidad-defensa-letrados/index.html", [
    "../pago-masa-independencia-defensa/",
])
require("assets/optimum-reader-journey-finish-20260818.js", [
    "const jtpPaymentUrl",
    "estate-payment-counsel-independence/",
    "pago-masa-independencia-defensa/",
    "navLink(jtpPaymentUrl",
])
require("CHATGPT_START_HERE.md", [
    "PD-JTP-REDTEAM-20260924-01",
    "Criminal first means element first, not offence-label first.",
])

control_path = "assets/data/jtp-payment-funded-exit-red-team-20260924.json"
try:
    control = json.loads(read(control_path))
except json.JSONDecodeError as exc:
    errors.append(f"{control_path}: invalid JSON: {exc}")
    control = {}

if control:
    if control.get("status") != "SIMULATED_ADVERSARIAL_REVIEW_NOT_ACTUAL_PARTY_STATEMENTS":
        errors.append(f"{control_path}: simulation-status lock missing")
    if control.get("criminal_first_rule") != "element-first, not offence-label-first":
        errors.append(f"{control_path}: criminal-first rule changed")
    concessions = set(control.get("mandatory_concessions", []))
    required_concessions = {
        "no proved direct CAM→JTP transfer",
        "incomplete €400,000→€26,750 bank trace",
        "estate counsel payment can be lawful in principle",
        "client substitution is formal immediate transition act",
        "JTP protective work preserved",
        "chronology is not causation",
        "ONA closing not guaranteed",
        "later lawful outcomes preserved as contrary evidence",
        "28-May reply not consent/waiver/ratification/validation",
        "12-Jun final fee proposal expressly rejected",
        "no adjudicated bribery/collusion/recipient-knowledge/common-plan finding",
    }
    missing = sorted(required_concessions - concessions)
    if missing:
        errors.append(f"{control_path}: missing mandatory concessions: {missing}")
    gates = set(control.get("a_plus_target_gates", []))
    for gate in (
        "criminal spine before civil/concursal",
        "hostile defence adjacent",
        "public falsification tests",
        "public P0 production",
        "reciprocal ONA/7June/counsel/payment links",
        "capacity/proceeding non-fusion",
    ):
        if gate not in gates:
            errors.append(f"{control_path}: missing A+ target gate: {gate}")

require("archive/JTP_ONA_DEEP_SOURCE_SWEEP_24SEP2026.md", [
    "PD-JTP-SOURCE-SWEEP-20260924-01",
    "JTP's own 4-Jan-2019 draft used a criminal / prosecutorial frame",
    "By 1 June 2020 successor counsel was already disputing JTP's authority / entitlement position",
    "TARGETED_NEGATIVE_SEARCH_RESULT / OPEN_PROOF",
    "failure to retrieve a record in this bounded search is not proof that the record does not exist",
])
require("assets/data/jtp-ona-deep-source-sweep-20260924.json", [
    '"control_id": "PD-JTP-SOURCE-SWEEP-20260924-01"',
    '"classification": "TARGETED_NEGATIVE_SEARCH_RESULT_OPEN_PROOF"',
    '"Non-retrieval in this bounded connected-source search is not proof of non-existence."',
])
require("governance/JTP_PAYMENT_FUNDED_EXIT_HOSTILE_READER_RED_TEAM_24SEP2026.md", [
    "simulated adversarial review; not statements by any named adverse party",
    "Criminal first means element first, not offence-label first.",
    "Mandatory hostile-reader concessions",
    "Falsification gates",
    "Priority prosecution production",
    "A+ target gates",
    "No simulated score substitutes for an actual prosecutor",
    "## 24-September deep-source supplement",
    "negative search",
])

require("assets/data/legal-representation-ac-causation-v1.json", [
    '"status": "UPDATED_WITH_24SEP2026_JTP_DEEP_SOURCE_SWEEP"',
    '"id": "LRAC-OF-011"',
    "archive/JTP_ONA_DEEP_SOURCE_SWEEP_24SEP2026.md",
    "Non-retrieval is not proof of non-existence",
])
require("assets/data/ac-counsel-interference-unitary-v1.json", [
    '"control_id": "PD-JTP-SOURCE-SWEEP-20260924-01"',
    "1-Jun-2020 successor counsel treated JTP as no longer LPB counsel",
    "bank-complete €400,000→€26,750 trace",
])
require("archive/AC_COUNSEL_INTERFERENCE_UNITARY_REDIGEST_21SEP2026.md", [
    "## 24 September 2026 — JTP deep-source supplement",
    "1-Jun-2020 successor counsel treated JTP as no longer LPB counsel",
])
require("archive/CORRECTION_REGISTER.md", [
    "| CR-163 |",
    "JTP / ONA history read as a fee-only dispute",
    "Non-retrieval is not proof of non-existence",
])
require("CHATGPT_START_HERE.md", [
    "PD-JTP-SOURCE-SWEEP-20260924-01",
    "JTP deep-source companion",
])

if errors:
    print("JTP PROSECUTORIAL RED-TEAM CONTRACT: FAIL")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print("JTP PROSECUTORIAL RED-TEAM CONTRACT: PASS")
