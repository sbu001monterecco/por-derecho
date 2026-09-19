#!/usr/bin/env python3
from pathlib import Path
import json, sys

ROOT=Path(__file__).resolve().parents[1]
errors=[]

def need(path, *needles):
    p=ROOT/path
    if not p.exists():
        errors.append(f"missing {path}"); return ""
    text=p.read_text(encoding="utf-8")
    for n in needles:
        if n not in text: errors.append(f"{path}: missing {n!r}")
    return text

def forbid(path,*needles):
    p=ROOT/path
    if not p.exists(): return
    text=p.read_text(encoding="utf-8")
    for n in needles:
        if n in text: errors.append(f"{path}: forbidden stale text {n!r}")

data=json.loads(need("assets/data/dp1901-routing-collision-v1.json","PROCEDURAL_IDENTITY_COLLISION_OPEN_DIRECTION_NOT_CERTIFIED"))
ids={x["id"] for x in data["nodes"]}
for req in {"REF21","REF24","DP1901_JUL9","DP1901_JUL12","FISCAL29","AUTO14","CGPJ286","TSJGUB38"}:
    if req not in ids: errors.append(f"routing graph missing node {req}")

for path in [
 "assets/visuals/dp1901-double-file-grave.svg",
 "assets/visuals/dp1901-registry-routing.svg",
 "assets/visuals/dp1901-fiscal-corpus.svg",
 "assets/visuals/dp1901-atlante-black-box.svg",
]:
    need(path,"DP 1901")

shared_pages=[
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
for path in shared_pages:
    need(path,"dp1901-routing-collision-20260919.js","data-dp1901-collision")

need("en/daily-reference-21-private-actor-complaint/index.html","DP 1901","Daily Ref. 24","data-dp1901-collision")
need("es/referencia-21-denuncia-actores-privados/index.html","DP 1901","Ref. diaria 24","data-dp1901-collision")
need("sitemap-control-22-24.xml","daily-reference-21-private-actor-complaint","referencia-21-denuncia-actores-privados")
need("assets/control-22-24-search-extension-20260904.js","CONTROL-21-PRIVATE-20260919")

forbid("en/control-24-insolvency-judge-complaint-36-2012/index.html","10-page supplement")
forbid("es/control-24-denuncia-juez-concurso-36-2012/index.html","complemento de 10 páginas","ampliación de 10 páginas")
need("en/control-24-insolvency-judge-complaint-36-2012/index.html","13-page dependent supplement")
need("es/control-24-denuncia-juez-concurso-36-2012/index.html","13 páginas")

trans=need("evidence/judicial/dp-1901-2026/full-text/auto-14sep2026-public-transcription.md",
 "no constituyo","y ello pese que","objetivable","ante este Órgano Judicial","paper copy on 18 September 2026")
for stale in ("no constituyen el objeto delimitado","argumento objetivado","ante éste Órgano Judicial"):
    if stale in trans: errors.append(f"Auto transcription still contains stale reading: {stale}")

need("en/cgpj-permanent-commission-reader-room/index.html","SUPERVENING EVENT · 14–18 SEPTEMBER 2026")
need("es/cgpj-comision-permanente-sala-lectura/index.html","HECHO SOBREVINIENTE · 14–18 SEPTIEMBRE 2026")
need("publication-manifests/dp1901-routing-interconnectivity-20260919.json","PREPARED_PENDING_MERGE")

if errors:
    print("\n".join("ERROR: "+e for e in errors))
    sys.exit(1)
print(f"PASS: DP1901 routing interconnectivity ({len(shared_pages)} shared pages, 4 visuals, Ref21 bilingual routes)")
