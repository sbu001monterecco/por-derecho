#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
errors=[]

def read(path):
    p=ROOT/path
    if not p.exists():
        errors.append(f"missing {path}")
        return ""
    return p.read_text(encoding="utf-8")

def req(path, markers):
    t=read(path)
    for m in markers:
        if m not in t:
            errors.append(f"{path}: missing {m!r}")

req("archive/JTP_FEE_AUTHORITY_PAYMENT_SOURCE_CLOSE_24SEP2026.md",[
    "PD-JTP-SOURCE-CLOSE-20260924-01",
    "Original fee baseline",
    "written approval",
    "12-Jun-2020 rejection",
    "18-Jun-2020 incoming-counsel assessment",
    "bounded search",
    "bank debit",
])
req("en/estate-payment-counsel-independence/index.html",[
    'id="source-close"',
    "11 June: written approval required",
    "18 June: incoming-counsel assessment",
    "Bounded negative search",
])
req("es/pago-masa-independencia-defensa/index.html",[
    'id="source-close"',
    "11 junio: exigencia de visto bueno escrito",
    "18 junio: valoración del letrado entrante",
    "Búsqueda negativa acotada",
])
req("governance/JTP_PAYMENT_FUNDED_EXIT_HOSTILE_READER_RED_TEAM_24SEP2026.md",[
    "24-Sep native-source close",
    "Arithmetic lock",
])
data_path="assets/data/jtp-fee-authority-source-close-20260924.json"
try:
    data=json.loads(read(data_path))
except Exception as e:
    errors.append(f"{data_path}: invalid JSON: {e}")
    data={}
if data:
    if data.get("control_id")!="PD-JTP-SOURCE-CLOSE-20260924-01":
        errors.append("source-close control ID changed")
    props={p.get("id"):p for p in data.get("propositions",[])}
    for pid in ("JTP-SC-001","JTP-SC-002","JTP-SC-003","JTP-SC-004","JTP-SC-006","JTP-SC-007","JTP-SC-008"):
        if pid not in props:
            errors.append(f"missing proposition {pid}")
    if "bounded" not in props.get("JTP-SC-007",{}).get("limit","").lower():
        errors.append("mailbox negative-search boundary missing")
    if "open" not in props.get("JTP-SC-008",{}).get("limit","").lower():
        errors.append("bank-trace open boundary missing")
for path in ("en/counsel-defence-continuity/index.html","es/continuidad-defensa-letrados/index.html"):
    t=read(path)
    if "€9,000" in t or "9.000 €</strong> el saldo base" in t:
        errors.append(f"{path}: erroneous JTP arithmetic is present")
if errors:
    print("JTP SOURCE-CLOSE CONTRACT: FAIL")
    for e in errors: print("-",e)
    raise SystemExit(1)
print("JTP SOURCE-CLOSE CONTRACT: PASS")
