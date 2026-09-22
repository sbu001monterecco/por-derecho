#!/usr/bin/env python3
from pathlib import Path
import json, sys

ROOT=Path(__file__).resolve().parents[1]
errors=[]
def check(cond,msg):
    if not cond: errors.append(msg)
def read(p): return (ROOT/p).read_text(encoding="utf-8")

source=json.loads(read("assets/data/2018-06-19-contemporaneous-question-bank-v2.json"))
current=json.loads(read("assets/data/2018-question-bank-current-verification-v2.json"))
manifest=json.loads(read("publication-manifests/question-bank-20180619-20260922.json"))

check(source.get("question_total")==251,"source question_total must be 251")
sets=source.get("sets",[])
counts={x.get("target_id"):x.get("question_count") for x in sets}
expected={"PD-SP-P-0011":76,"PD-SP-P-0007":49,"PD-SP-P-0009":50,"PD-SP-P-0012":76}
check(counts==expected,f"source target counts mismatch: {counts}")
check(sum(len(x.get("questions",[])) for x in sets)==251,"question array denominator must be 251")
check(len(current.get("universal_questions",[]))==14,"must retain 14 universal current questions")
targets=current.get("targets",[])
ids={x.get("id") or x.get("target_id") for x in targets}
required={"PD-SP-P-0011","PD-SP-P-0012","PD-SP-P-0009","PD-SP-P-0007","PD-SP-P-0008","PD-SP-P-0010","PD-SP-P-0057","PD-SP-P-0004","PD-SP-P-0014","PD-SP-O-0007"}
check(required.issubset(ids),f"missing current targets: {sorted(required-ids)}")
check(manifest.get("release_id")=="PD-SP-QBANK-20180619-01","manifest release ID mismatch")
for p in manifest.get("controlled_files",[])+manifest.get("public_routes",[]):
    check((ROOT/p).is_file(),f"missing controlled file: {p}")
for p in ["en/contemporaneous-questions-19-june-2018/index.html","es/preguntas-contemporaneas-19-junio-2018/index.html"]:
    t=read(p)
    check("251" in t,f"{p}: 251 denominator missing")
    check("question-bank-2018-public-pdf-v1.js" in t,f"{p}: embedded PDF asset not loaded")
    check("question-bank-2018-viewer.js" in t,f"{p}: viewer JS missing")
    check("2018-question-bank-current-verification-v2.json" in t,f"{p}: current matrix link missing")
for p in [
 "en/fmmm-shaila-antonio-family-community-corporate-continuity/index.html",
 "es/fmmm-shaila-antonio-continuidad-familiar-comunitaria-societaria/index.html",
 "en/sun-park-takeover-7-june-2018/index.html",
 "es/toma-control-sun-park-7-junio-2018/index.html",
 "en/community-instrumentalisation/index.html",
 "es/comunidad-instrumentalizacion/index.html",
 "en/acosta-matos-perimeter/index.html","es/acosta-matos-perimetro/index.html",
 "en/francisco-mario-matos-matas/index.html","es/francisco-mario-matos-matas/index.html",
 "en/antonio-cogolludo-rojas/index.html","es/antonio-cogolludo-rojas/index.html",
 "en/shaila-maria-cogolludo-ramos/index.html","es/shaila-maria-cogolludo-ramos/index.html",
 "en/francisco-de-borja-rodriguez-batllori-laffitte/index.html",
 "es/francisco-de-borja-rodriguez-batllori-laffitte/index.html",
 "en/acosta-matos-family/index.html","es/acosta-matos-familia/index.html",
 "en/unitary-criminal-hypothesis-2011-present/institutional-action/index.html",
 "es/hipotesis-criminal-unitaria-2011-presente/accion-institucional/index.html"
]:
    check("PD-SP-QBANK-20180619-01" in read(p),f"{p}: reciprocal source control missing")
check("QB-COR-001" in read("archive/CORRECTION_REGISTER.md"),"correction controls missing")
check("ME-QBANK-20180619" in read("archive/MISSING_EVIDENCE_REGISTER.md"),"missing-evidence control missing")
check("window.PD_QBANK_PDF_BASE64" in read("assets/data/question-bank-2018-public-pdf-v1.js"),"embedded PDF payload missing")
check("/es/preguntas-contemporaneas-19-junio-2018/" in read("sitemap.xml"),"ES sitemap route missing")
check("/en/contemporaneous-questions-19-june-2018/" in read("sitemap.xml"),"EN sitemap route missing")
if errors:
    print("ERRORS:")
    for e in errors: print(" -",e)
    sys.exit(1)
print("19-Jun-2018 question-bank validation passed: 251 historic questions, 10 current targets, 14 universal questions, reciprocal links present.")
