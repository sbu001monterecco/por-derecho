#!/usr/bin/env python3
from __future__ import annotations
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "assets/data/concurso36-unitary-prosecutorial-theory-20260829.json"
MANIFEST = ROOT / "publication-manifests/concurso36-unitary-prosecutorial-20260829.json"
JS = ROOT / "assets/concurso36-unitary-prosecutorial.js"
PAGES = [
    ROOT / "es/concurso-36-2012/index.html",
    ROOT / "en/insolvency-36-2012/index.html",
    ROOT / "es/concurso-36-2012-analisis-penal-forense-unitario/index.html",
    ROOT / "en/insolvency-36-2012-unitary-criminal-forensic-analysis/index.html",
]
SPECIALIST = [
    ROOT / "es/control-acreedor-cam-administracion-hecho-omision-judicial/index.html",
    ROOT / "en/cam-creditor-control-shadow-administration-judicial-omission/index.html",
    ROOT / "es/concurso-36-2012-escritos-tratamiento-sobreextension/index.html",
    ROOT / "en/insolvency-36-2012-filings-court-treatment-overreach/index.html",
    ROOT / "es/ric-private-equity-sun-park/index.html",
    ROOT / "en/ric-private-equity-sun-park/index.html",
    ROOT / "es/reclamacion-caixabank-valencia/index.html",
    ROOT / "en/caixabank-valencia-claim/index.html",
    ROOT / "es/calificacion-concurso-36-2012-vidas-paralelas/index.html",
    ROOT / "en/insolvency-classification-parallel-lives/index.html",
    ROOT / "es/concurso-36-2012-autos-resoluciones/index.html",
    ROOT / "en/insolvency-36-2012-orders-decisions/index.html",
]

def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)

def require(cond: bool, msg: str) -> None:
    if not cond:
        fail(msg)

def load(path: pathlib.Path):
    require(path.exists(), f"missing {path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))

def main() -> None:
    d = load(DATA)
    m = load(MANIFEST)
    require(d.get("schema") == "por-derecho.concurso36-unitary-prosecutorial-theory.v1", "unexpected schema")
    require(d.get("unitary_thesis", {}).get("criminal_finding") is False, "criminal_finding must remain false")
    require(d.get("repository_audit", {}).get("certified_docket") is False, "certified docket must remain false")
    require(len(d.get("evidence_tiers", [])) == 5, "expected 5 evidence tiers")
    require(len(d.get("prosecutorial_stages", [])) == 14, "expected 14 prosecutorial stages")
    require(len(d.get("criminal_hypothesis_tests", [])) == 8, "expected 8 criminal hypothesis tests")
    require(d.get("repository_audit", {}).get("p0_open_families") == 9, "expected 9 P0 families")
    require(d.get("repository_audit", {}).get("p1_open_families") == 2, "expected 2 P1 families")
    p = d.get("fixed_perimeter", {}).get("ricpe_20jul2021_262_fincas", {})
    require(p.get("cam_owned") == 54, "CAM perimeter must be 54")
    require(p.get("lpb_components") == 190, "LPB perimeter must be 190")
    require(p.get("third_party_fincas") == 18, "third-party perimeter must be 18")
    require(p.get("cam_owned", 0) + p.get("lpb_components", 0) + p.get("third_party_fincas", 0) == 262, "RICPE perimeter must total 262")
    for stage in d.get("prosecutorial_stages", []):
        require(stage.get("documented"), f"stage {stage.get('id')} missing documented")
        require(stage.get("prosecutorial_question"), f"stage {stage.get('id')} missing prosecutorial question")
        require(stage.get("counterweight"), f"stage {stage.get('id')} missing counterweight")
    for h in d.get("criminal_hypothesis_tests", []):
        require(h.get("must_prove"), f"hypothesis {h.get('id')} missing must_prove")
        require(h.get("not_enough"), f"hypothesis {h.get('id')} missing not_enough")
    require(len(d.get("highest_leverage_gaps", [])) >= 10, "gap list unexpectedly short")
    require(len(d.get("prosecutorial_production_requests", [])) == 10, "expected 10 production blocks")
    for path in PAGES + SPECIALIST + [JS]:
        require(path.exists(), f"missing linked file {path.relative_to(ROOT)}")
    js = JS.read_text(encoding="utf-8")
    require("concurso36-unitary-prosecutorial-theory-20260829.json" in js, "renderer does not load unitary JSON")
    combined = "\n".join(path.read_text(encoding="utf-8") for path in PAGES) + "\n" + DATA.read_text(encoding="utf-8")
    banned = [
        "the judge ignored everything",
        "el juez ignoró todo",
        "criminal liability is established",
        "la responsabilidad penal está establecida",
        "investors were complicit",
        "los inversores fueron cómplices",
    ]
    low = combined.lower()
    for phrase in banned:
        require(phrase.lower() not in low, f"unsafe categorical phrase present: {phrase}")
    expected = m.get("expected_controls", {})
    require(expected.get("prosecutorial_stages") == 14, "manifest stage count mismatch")
    require(expected.get("criminal_hypothesis_tests") == 8, "manifest hypothesis count mismatch")
    require(expected.get("fixed_ricpe_perimeter_total") == 262, "manifest perimeter mismatch")
    print("OK: Concurso 36/2012 unitary prosecutorial publication validated")

if __name__ == "__main__":
    main()
