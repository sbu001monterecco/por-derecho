#!/usr/bin/env python3
from pathlib import Path
import hashlib, json, struct, sys

ROOT=Path(__file__).resolve().parents[1]
FAIL=[]

def must(cond,msg):
    if not cond: FAIL.append(msg)

def sha(path):
    return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()

response={
"drafts/cgpj/2026-09-19_DP1901_CGPJ_RESPONSE_PROPOSED.docx":"81e9d6afaabeab00a343fc9e96d372e0ae88f78b734f1a72e1edb94b33d14ffc",
"drafts/cgpj/2026-09-19_DP1901_CGPJ_RESPONSE_PROPOSED.pdf":"cc72caa9884b1cd362687525c7d086533f8c0a2ab5e0621a68b025975dd9586c",
"drafts/cgpj/2026-09-19_DP1901_CGPJ_RESPONSE_PROPOSED.md":"5264a784d74da5da51e779a08dee086e21234d1e837aeed2e5932178a05eb2b1",
}
images={
"assets/visuals/dp1901-20260919/01-single-grave.png":"a6bbe9e4f53fd2e1c6566454bd9d32b7860ffdee78eded2394be8d8244cf6dea",
"assets/visuals/dp1901-20260919/02-decanato.png":"9d06dc1340f8aa050ae71780eb24a265b7b5ce467e9178c7b1aa976a4ddfd54a",
"assets/visuals/dp1901-20260919/03-fiscal-corpus.png":"c3c5c5783f949f0e6b8af7010313ccc5e30e708e98e64ba4e59bf23ca7657b88",
"assets/visuals/dp1901-20260919/04-atlante.png":"ddbc5e4a5f25f025d5577b7efcd0f7fb84dd36d65732a915288db3a608305e4e",
"assets/visuals/dp1901-20260919/05-composite-annex.png":"329eb2050a8ba0f5a15138d34261cf73d4f257f18cd5ed3f1b8ec5f3e472b554",
"assets/visuals/dp1901-20260919/06-traceability-overview.png":"0a196b6cf699a9171ad98b44b00bc12faf87e86bc33cf1b09ba3795e18c92ee9",
}
for p,h in {**response,**images}.items():
    must((ROOT/p).is_file(),f"missing {p}")
    if (ROOT/p).is_file(): must(sha(p)==h,f"hash mismatch {p}")

md=(ROOT/"drafts/cgpj/2026-09-19_DP1901_CGPJ_RESPONSE_PROPOSED.md").read_text(encoding="utf-8")
for needle in [
"BORRADOR PROPUESTO - NO PRESENTADO / NO REMITIDO",
"intacto, sin escanear y sin asignar",
"no como alegación autónoma de falsificación",
"DP 1901 se originó en la denuncia autónoma contra actores privados",
"independiente de los recursos judiciales",
"independiente de la respuesta prevista en E.G. 745/2026",
]:
    must(needle in md,f"response missing control: {needle}")

reader=(ROOT/"assets/dp1901-cgpj-response-reader-20260919.js").read_text(encoding="utf-8")
for needle in ["response-pdf","response-full","visual-gallery","PROPOSED DRAFT · NOT FILED · NOT SENT","BORRADOR PROPUESTO · NO PRESENTADO · NO REMITIDO"]:
    must(needle in reader,f"reader missing {needle}")
for p in images:
    must(Path(p).name in reader,f"reader does not expose {p}")

for p in [
"es/dp-1901-2026-auto-14-septiembre-2026/index.html",
"en/dp-1901-2026-order-14-september-2026/index.html",
]:
    t=(ROOT/p).read_text(encoding="utf-8")
    must("dp1901-cgpj-response-reader-20260919.js" in t,f"reader script absent from {p}")
    must('id="response-package-entry"' in t,f"response entry absent from {p}")

for p in [
"es/control-21-denuncia-actores-privados-25-junio-2026/index.html",
"en/control-21-private-actors-complaint-25-june-2026/index.html",
"es/control-24-denuncia-juez-concurso-36-2012/index.html",
"en/control-24-insolvency-judge-complaint-36-2012/index.html",
"es/dp-1901-2026/index.html","en/dp-1901-2026/index.html",
"es/cgpj-comision-permanente-sala-lectura/index.html","en/cgpj-permanent-commission-reader-room/index.html",
"es/procedimientos/gc-gov-020/index.html","en/proceedings/gc-gov-020/index.html",
]:
    t=(ROOT/p).read_text(encoding="utf-8")
    must('id="dp1901-19sep-response-backlink"' in t,f"static backlink absent from {p}")

dma=json.loads((ROOT/"data/digital-media-asset-register-v1.json").read_text(encoding="utf-8"))
ids={x.get("reference") for x in dma.get("logical_assets",[])}
for n in range(7,13): must(f"PD-DMA-{n:04d}" in ids,f"DMA missing PD-DMA-{n:04d}")
files={x.get("reference"):x for x in dma.get("files",[])}
for n,p in zip(range(7,13),images):
    ref=f"PD-DMA-{n:04d}^"; must(ref in files,f"DMA file missing {ref}")
    if ref in files: must(files[ref].get("repository_path")==p,f"DMA path mismatch {ref}")

routing=(ROOT/"assets/dp1901-routing-collision-20260919.js").read_text(encoding="utf-8")
for needle in ["Respuesta CGPJ propuesta · 19 sep","Proposed CGPJ response · 19 Sep","E.G. 745/2026","unscanned and unallocated"]:
    must(needle in routing,f"routing bridge missing {needle}")

eg=(ROOT/"assets/eg745-fiscalia-interconnectivity-20260918.js").read_text(encoding="utf-8")
for needle in ["Respuesta CGPJ propuesta · 19 sep","Proposed CGPJ response · 19 Sep","Ref. 21","Ref. 24","CGPJ","TSJC"]:
    must(needle in eg,f"EG745 bridge missing {needle}")

manifest=json.loads((ROOT/"publication-manifests/dp1901-cgpj-response-images-20260919.json").read_text(encoding="utf-8"))
must(manifest.get("publication_is_filing") is False,"manifest filing boundary lost")
must(manifest.get("visual_control",{}).get("formal_evidentiary_annex") is False,"visual annex boundary lost")

if FAIL:
    print("\n".join("ERROR: "+x for x in FAIL),file=sys.stderr)
    sys.exit(1)
print("OK: DP1901 CGPJ response package, image corrections, hashes and backlinks validated")
