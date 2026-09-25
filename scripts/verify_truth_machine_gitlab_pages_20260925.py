#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,time,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE="https://por-derecho-setup-or-gitlab-setup-c2b10f.gitlab.io/por-derecho-setup-or-gitlab-setup/"
PATHS=[
"assets/truth-machine-live.js",
"assets/data/truth-machine-methodology-v2.json",
"assets/data/truth-machine-priority-queue-v1.json",
"assets/data/r33-truth-machine-visual-20260925.json",
"assets/r33-truth-machine-visual-20260925.svg",
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
      try:
        st,raw=fetch(p);match=st==200 and raw==exp
      except Exception as e:
        st=0;raw=b"";match=False
      last.append({"path":p,"http":st,"sha256":sha(raw) if raw else None,"expected":sha(exp),"exact":match})
      ok &= match
    if ok:
      out={"status":"LIVE_VERIFIED_TRUTH_MACHINE_GITLAB","base":BASE,"checks":last}
      print("TRUTH_MACHINE_GITLAB_LIVE "+json.dumps(out,sort_keys=True));return
    time.sleep(10)
  print(json.dumps({"status":"LIVE_VERIFY_FAILED","checks":last},sort_keys=True))
  raise SystemExit(1)
if __name__=="__main__":main()
