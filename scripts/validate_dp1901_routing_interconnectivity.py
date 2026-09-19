#!/usr/bin/env python3
from pathlib import Path
import json, sys

ROOT=Path(__file__).resolve().parents[1]
MODULE="dp1901-routing-collision-20260919.js"
TARGETS=[
"en/dp-1901-2026/index.html","es/dp-1901-2026/index.html",
"en/dp-1901-2026-order-14-september-2026/index.html","es/dp-1901-2026-auto-14-septiembre-2026/index.html",
"en/fiscalia-dip-2-2026/index.html","es/fiscalia-dip-2-2026/index.html",
"en/control-24-insolvency-judge-complaint-36-2012/index.html","es/control-24-denuncia-juez-concurso-36-2012/index.html",
"en/proceedings/gc-hc-010/index.html","es/procedimientos/gc-hc-010/index.html",
"en/proceedings/gc-cri-008/index.html","es/procedimientos/gc-cri-008/index.html",
"en/cgpj-permanent-commission-reader-room/index.html","es/cgpj-comision-permanente-sala-lectura/index.html",
"en/cgpj-public-prosecution-routing-update-20-august-2026/index.html","es/actualizacion-cgpj-fiscalia-20-agosto-2026/index.html",
"en/tsj-canarias-exp-gub-38-2026/index.html","es/tsj-canarias-exp-gub-38-2026/index.html",
]
errors=[]
for rel in TARGETS:
    p=ROOT/rel
    if not p.exists(): errors.append(f"missing target: {rel}"); continue
    txt=p.read_text(encoding="utf-8")
    if MODULE not in txt: errors.append(f"missing shared module include: {rel}")

checks={
"en/control-24-insolvency-judge-complaint-36-2012/index.html":["13-page self-contained dependent supplement","27-page principal pleading"],
"es/control-24-denuncia-juez-concurso-36-2012/index.html":["13 páginas","escrito principal de 27 páginas"],
"en/dp-1901-2026/index.html":["1901: Contra CAM y otras partes de la Comunidad de Propietarios","state transition"],
"es/dp-1901-2026/index.html":["1901: Contra CAM y otras partes de la Comunidad de Propietarios","transición de identidad procesal"],
}
for rel, needles in checks.items():
    txt=(ROOT/rel).read_text(encoding="utf-8")
    for n in needles:
        if n not in txt: errors.append(f"{rel}: missing {n!r}")

trans=(ROOT/"evidence/judicial/dp-1901-2026/full-text/auto-14sep2026-public-transcription.md").read_text(encoding="utf-8")
for n in ["no constituyo el objeto delimitado","y ello pese que reconocía","argumento objetivable","ante este Órgano Judicial","paper copy received on 18 September 2026"]:
    if n not in trans: errors.append(f"transcription missing {n!r}")

graph=json.loads((ROOT/"assets/data/dp1901-routing-collision-v1.json").read_text(encoding="utf-8"))
if graph.get("controlling_state")!="REF21_TO_DP1901_CONTEMPORANEOUSLY_CORROBORATED_OFFICIAL_REPARTO_AND_REF24_ASSOCIATION_HISTORY_OUTSTANDING": errors.append("routing graph controlling state")
node_ids={n["id"] for n in graph.get("nodes",[])}
for n in ["REF21","REF24","DP1901","DIP2","FISCAL29","AUTO14","ALZADA286","EXPGUB38"]:
    if n not in node_ids: errors.append(f"routing graph missing node {n}")

continuity=json.loads((ROOT/"assets/data/control-21-22-24-continuity-v1.json").read_text(encoding="utf-8"))
if continuity.get("as_of")!="2026-09-19": errors.append("continuity as_of not 2026-09-19")
if "state_transition_audit_20260919" not in continuity: errors.append("missing state transition audit")
control21=next((x for x in continuity.get("controls",[]) if x.get("id")=="CONTROL-21"),{})
if control21.get("bridge_status")!="UNVERIFIED_CANDIDATE_BRIDGE": errors.append("Control21 formal bridge must remain uncertified")
if control21.get("origin_chronology_evidential_state")!="CONTEMPORANEOUSLY_CORROBORATED": errors.append("Control21 origin chronology support missing")
if "email_20260625_to_procuradora" not in control21.get("contemporaneous_july_evidence",{}): errors.append("Control21 missing 25-Jun procuradora support")

svg=(ROOT/"assets/visuals/dp1901-routing-collision-20260919.svg").read_text(encoding="utf-8")
for n in ["REF. 21","REF. 24","DP 1901/2026","DOCUMENTO / EVENTO PUENTE NO LOCALIZADO","29 JUL 2026","14 SEP 2026"]:
    if n not in svg: errors.append(f"visual missing {n!r}")

if errors:
    print("\n".join("ERROR: "+e for e in errors))
    sys.exit(1)
print(f"PASS: {len(TARGETS)} reciprocal surfaces + source/graph/visual controls")
