#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,time,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE="https://por-derecho-setup-or-gitlab-setup-c2b10f.gitlab.io/"
PREFIX="por-derecho-setup-or-gitlab-setup/"
PATHS=[
"assets/truth-machine-live.js",
"assets/data/truth-machine-methodology-v2.json",
"assets/data/truth-machine-methodology-v3.json",
"assets/data/truth-machine-priority-queue-v1.json",
"assets/data/r33-truth-machine-visual-20260925.json",
"assets/data/r33-forensic-method-pass-v1.json",
"assets/r33-truth-machine-visual-20260925.svg",
"assets/r33-method-stack-visual-20260925.svg",
"en/truth-machine/index.html",
"es/maquina-verdad/index.html",
"en/r33-truth-machine-visual/index.html",
"es/r33-maquina-verdad-visual/index.html",
"assets/por-derecho/the-pulse-mark.svg",
"assets/data/the-pulse-symbol-v1.json",
"en/por-derecho/the-pulse/index.html",
"es/por-derecho/el-pulso/index.html",
"en/por-derecho/index.html",
"es/por-derecho/index.html",
"en/index.html",
"es/index.html",
"en/future/index.html",
"es/futuro/index.html",
"en/institutional-capital/index.html",
"es/capital-institucional/index.html",
"en/private-note-programme-administration/index.html",
"es/administracion-programa-notas-privadas/index.html",
"en/montana-roja/index.html",
"es/montana-roja/index.html",
"en/capital-relationships/index.html",
"es/relaciones-de-capital/index.html",
"en/strategic-financial-relationship/index.html",
"es/relacion-financiera-estrategica/index.html",
"assets/institutional-capital-20260921.css",
"assets/capital-relationships-20260916.css",
"assets/strategic-financial-relationship-20260916.css",
"assets/montana-roja-capital-20260915.css",
"assets/platform-scale-20260916.css",
"assets/playa-blanca-return-poster.svg",
"assets/playa-blanca-arrival-poster.svg",
"assets/playa-blanca-oasis-poster.svg",
"assets/playa-blanca-location-diagram.svg",
"assets/playa-blanca-programme-section.svg",
"assets/project-horizon-masterplan.svg",
"assets/project-horizon-suite.svg",
"assets/project-horizon-evening.svg",
"assets/styles.css",
]
def sha(b):return hashlib.sha256(b).hexdigest()
def fetch(path):
  req=urllib.request.Request(BASE+path+"?tmverify="+str(int(time.time())),headers={"User-Agent":"PorDerecho-TruthMachine-Live/1","Cache-Control":"no-cache"})
  with urllib.request.urlopen(req,timeout=30) as r:return r.status,r.read()
def main():
  deadline=time.time()+180; last=[]
  while time.time()<deadline:
    last=[];ok=True
    for p in PATHS:
      exp=(ROOT/p).read_bytes()
      for served in (p,PREFIX+p):
        try:
          st,raw=fetch(served);match=st==200 and raw==exp;error=None
        except Exception as e:
          st=0;raw=b"";match=False;error=f"{type(e).__name__}: {e}"[:500]
        last.append({"path":served,"source_path":p,"http":st,"sha256":sha(raw) if raw else None,"expected":sha(exp),"exact":match,"error":error})
        ok &= match
    if ok:
      out={"status":"LIVE_VERIFIED_TRUTH_MACHINE_GITLAB","base":BASE,"checks":last}
      print("TRUTH_MACHINE_GITLAB_LIVE "+json.dumps(out,sort_keys=True));return
    time.sleep(10)
  print(json.dumps({"status":"LIVE_VERIFY_FAILED","checks":last},sort_keys=True))
  raise SystemExit(1)
if __name__=="__main__":main()
