#!/usr/bin/env python3
from pathlib import Path
import json,re,sys
ROOT=Path(__file__).resolve().parents[1]
ROUTES=[
"es/icalpa-mesa-del-ponente/dip-80-2026/manual-vivo/index.html",
"es/icalpa-mesa-del-ponente/dip-80-2026/manual-vivo/cronologia/index.html",
"es/icalpa-mesa-del-ponente/dip-80-2026/manual-vivo/arbol-decision/index.html",
"es/icalpa-mesa-del-ponente/dip-80-2026/manual-vivo/atlas-prueba/index.html",
"es/icalpa-mesa-del-ponente/dip-80-2026/manual-vivo/proteccion-urgente/index.html",
"es/icalpa-mesa-del-ponente/dip-80-2026/manual-vivo/modelos/index.html",
"es/icalpa-mesa-del-ponente/dip-80-2026/manual-vivo/aula/index.html",
"en/icalpa-rapporteur-workbench/dip-80-2026/living-casebook/index.html",
"en/icalpa-rapporteur-workbench/dip-80-2026/living-casebook/chronology/index.html",
"en/icalpa-rapporteur-workbench/dip-80-2026/living-casebook/decision-tree/index.html",
"en/icalpa-rapporteur-workbench/dip-80-2026/living-casebook/evidence-atlas/index.html",
"en/icalpa-rapporteur-workbench/dip-80-2026/living-casebook/urgent-protection/index.html",
"en/icalpa-rapporteur-workbench/dip-80-2026/living-casebook/models/index.html",
"en/icalpa-rapporteur-workbench/dip-80-2026/living-casebook/classroom/index.html"]
errors=[]
def need(cond,msg):
    if not cond: errors.append(msg)
for r in ROUTES:
    p=ROOT/r
    need(p.exists(),f"missing route {r}")
    if p.exists():
        t=p.read_text(encoding="utf-8")
        need('<meta name="robots" content="noindex,follow,noarchive">' in t,f"robots missing {r}")
        need('dip80-open-kimono.js' in t and 'dip80-open-kimono.css' in t,f"assets missing {r}")
        need('Alegaciones ≠ hallazgos' in t or 'Allegations ≠ findings' in t,f"boundary missing {r}")
data_path=ROOT/"assets/data/dip-80-2026-open-kimono.json"
need(data_path.exists(),"missing data")
if data_path.exists():
    d=json.loads(data_path.read_text(encoding="utf-8"))
    need(d.get("caseId")=="DIP-80-2026","wrong caseId")
    required=["officialStatus","proceduralActs","allegations","duties","acts","omissions","documents","evidenceLinks","respondentPosition","counterEvidence","temporalIssues","competenceIssues","decisionNodes","urgentProtection","humanGates","modelDecisions","corrections","publicRedactions"]
    for k in required: need(k in d,f"missing schema key {k}")
    need(len(d.get("modules",[]))==11,"modules not 11")
    cv={"strengthen","weaken","resolve","verify","missing","alternative"}
    for m in d.get("modules",[]): need(cv<=set(m.get("changeView",{})),f"changeView incomplete {m.get('id')}")
    gates={g["id"] for g in d.get("humanGates",[])}
    for n in d.get("decisionNodes",[]): need(n.get("humanGateId") in gates,f"human gate missing {n.get('id')}")
    sep=next((x for x in d.get("documents",[]) if x.get("id")=="SRC-D79-7476"),None)
    need(bool(sep),"DIP79 separation document missing")
    if sep: need("DIP-79" in sep.get("file","") and "blocked" in json.dumps(sep.get("status",{})).lower(),"DIP79 separation not enforced")
    need(len(d.get("modelDecisions",[]))>=16,"model library incomplete")
    need(len(d.get("classroom",{}).get("chapters",[]))>=20,"classroom chapters incomplete")
    need(len(d.get("acceptanceSections",[]))==28 and all(x.get("status")=="pass" for x in d["acceptanceSections"]),"28-section acceptance incomplete")

for gp,needle in [
    (ROOT/"es/icalpa-recorrido-denuncia-deontologica/index.html","icalpa-mesa-del-ponente/dip-80-2026/manual-vivo/"),
    (ROOT/"en/icalpa-complaint-roadmap/index.html","icalpa-rapporteur-workbench/dip-80-2026/living-casebook/")
]:
    need(gp.exists(),f"missing relevant ICALPA layer {gp.relative_to(ROOT)}")
    if gp.exists():
        need(needle in gp.read_text(encoding="utf-8"),f"casebook link missing from {gp.relative_to(ROOT)}")

for p in [ROOT/"assets/dip80-open-kimono.js",ROOT/"assets/dip80-open-kimono.css",
          ROOT/"archive/ICALPA_DIP80_OPEN_KIMONO_IMPLEMENTATION_CONTROL_18AUG2026.md",
          ROOT/"archive/ICALPA_DIP80_OPEN_KIMONO_DELETION_CONTINUITY_18AUG2026.md"]:
    need(p.exists(),f"missing {p.relative_to(ROOT)}")
PRIVACY_PATHS=[ROOT/r for r in ROUTES]+[
    ROOT/"es/icalpa-mesa-del-ponente/dip-80-2026/index.html",
    ROOT/"en/icalpa-rapporteur-workbench/dip-80-2026/index.html",
    ROOT/"es/icalpa-recorrido-denuncia-deontologica/index.html",
    ROOT/"en/icalpa-complaint-roadmap/index.html",
    ROOT/"assets/data/dip-80-2026-open-kimono.json",
    ROOT/"assets/dip80-open-kimono.js",
    ROOT/"assets/dip80-open-kimono.css",
    ROOT/"archive/ICALPA_DIP80_OPEN_KIMONO_IMPLEMENTATION_CONTROL_18AUG2026.md",
    ROOT/"archive/ICALPA_DIP80_OPEN_KIMONO_DELETION_CONTINUITY_18AUG2026.md",
    ROOT/"archive/ICALPA_DIP80_OPEN_KIMONO_MASTER_EXECUTION_PROMPT_18AUG2026.md",
    ROOT/"archive/ICALPA_DIP80_OPEN_KIMONO_FILE_MANIFEST_18AUG2026.json",
]
joined="\n".join(p.read_text(encoding="utf-8",errors="ignore") for p in PRIVACY_PATHS if p.exists())
for banned in ["Y2231410X","43263235M","sbu001@monterecco.com","REGTEL-"]:
    need(banned not in joined,f"personal/private token present: {banned}")
need("caseId\": \"DIP-80-2026\"" in data_path.read_text(encoding="utf-8"),"literal caseId missing")
if errors:
    print("FAIL")
    print("\n".join(f"- {e}" for e in errors))
    sys.exit(1)
print(f"PASS: {len(ROUTES)} routes, 28/28 master sections, full data schema, noindex, human gates and DIP79 separation.")
