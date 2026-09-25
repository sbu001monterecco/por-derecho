#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, os, shutil, stat, tempfile, urllib.request, zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PROJECT="86151898"
BASELINE_SOURCE="b631dca8829eb3d3a60f17eeb13e3ea3a769045d"
BASELINE_PIPELINE="2881426843"
BASELINE_JOB="16728345228"
BASELINE_FILES=2114
OVERLAY=[
"assets/truth-machine-live.js",
"assets/data/truth-machine-methodology-v2.json",
"assets/data/truth-machine-priority-queue-v1.json",
"assets/data/r33-truth-machine-visual-20260925.json",
"assets/r33-truth-machine-visual-20260925.svg",
"en/truth-machine/index.html",
"es/maquina-verdad/index.html",
"en/r33-truth-machine-visual/index.html",
"es/r33-maquina-verdad-visual/index.html",
"en/insolvency-36-2012-ac-opposition-lpb-appeal-september-2026/index.html",
"es/concurso-36-2012-oposicion-ac-apelacion-lpb-septiembre-2026/index.html",
"assets/por-derecho/the-pulse-mark.svg",
"assets/data/the-pulse-symbol-v1.json",
"en/por-derecho/the-pulse/index.html",
"es/por-derecho/el-pulso/index.html",
"en/por-derecho/index.html",
"es/por-derecho/index.html",
]

def digest(b:bytes): return hashlib.sha256(b).hexdigest()

def safe(name:str):
    p=Path(name)
    if p.is_absolute() or ".." in p.parts: raise ValueError("unsafe artifact path "+name)

def main():
    token=os.environ.get("CI_JOB_TOKEN")
    if not token: raise SystemExit("CI_JOB_TOKEN required")
    public=ROOT/"public"
    if public.exists(): shutil.rmtree(public)
    with tempfile.TemporaryDirectory(prefix="truth-machine-pages-") as td:
        z=Path(td)/"base.zip"
        req=urllib.request.Request(
          f"https://gitlab.com/api/v4/projects/{PROJECT}/jobs/{BASELINE_JOB}/artifacts",
          headers={"JOB-TOKEN":token,"User-Agent":"PorDerecho-TruthMachine-Scoped/1"})
        with urllib.request.urlopen(req,timeout=90) as r, z.open("wb") as f:
            if r.status!=200: raise ValueError("baseline artifact unavailable")
            shutil.copyfileobj(r,f)
        with zipfile.ZipFile(z) as ar:
            names=[]
            for m in ar.infolist():
                if m.is_dir() or not m.filename.startswith("public/"): continue
                safe(m.filename); mode=stat.S_IFMT(m.external_attr>>16)
                if mode not in (0,stat.S_IFREG): raise ValueError("non-regular artifact member")
                names.append(m.filename)
                target=ROOT/m.filename; target.parent.mkdir(parents=True,exist_ok=True)
                with ar.open(m) as a,target.open("wb") as b: shutil.copyfileobj(a,b)
        if len(names)!=BASELINE_FILES: raise ValueError(f"baseline file count changed: {len(names)}")
    pins={}
    for rel in OVERLAY:
        src=ROOT/rel
        if not src.is_file() or src.is_symlink(): raise ValueError("missing overlay "+rel)
        dst=public/rel; dst.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(src,dst)
        pins[rel]={"sha256":digest(src.read_bytes()),"bytes":src.stat().st_size}
    receipt={
      "schema":"por-derecho.truth-machine-scoped-pages.v1",
      "status":"SCOPED_TRUTH_MACHINE_OVERLAY_OVER_LAST_VERIFIED_GITLAB_PAGES",
      "source_commit":os.environ.get("CI_COMMIT_SHA"),
      "baseline_source":BASELINE_SOURCE,
      "baseline_pipeline":BASELINE_PIPELINE,
      "baseline_job":BASELINE_JOB,
      "baseline_files":BASELINE_FILES,
      "overlay":pins,
      "private_evidence_published":False,
      "boundary":"Last verified GitLab Pages baseline plus exact Truth Machine/R33 public-safe overlay only; unrelated main failures isolated."
    }
    out=public/"assets/data/truth-machine-gitlab-scoped-release.json"
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("TRUTH_MACHINE_SCOPED_PAGES "+json.dumps(receipt,sort_keys=True))

if __name__=="__main__": main()
