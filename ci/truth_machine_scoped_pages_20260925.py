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
PREFIX="por-derecho-setup-or-gitlab-setup"
HOMEPAGE_REVIEW="ops/gitlab-pages-recovery/GITLAB_HOMEPAGE_SCOPED_RELEASE_20260925.json"
HOMEPAGE_SCHEMA="por-derecho.gitlab-homepage-scoped-release.v1"
HOMEPAGE_PATHS=("en/index.html","es/index.html","en/future/index.html","es/futuro/index.html","en/start/index.html","es/inicio/index.html","en/evidence/index.html","es/evidencia/index.html","assets/styles.css")
OVERLAY=[
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
"en/insolvency-36-2012-ac-opposition-lpb-appeal-september-2026/index.html",
"es/concurso-36-2012-oposicion-ac-apelacion-lpb-septiembre-2026/index.html",
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
"en/start/index.html",
"es/inicio/index.html",
"en/evidence/index.html",
"es/evidencia/index.html",
"en/institutional-capital/index.html",
"es/capital-institucional/index.html",
"en/montana-roja/index.html",
"es/montana-roja/index.html",
"en/private-note-programme-administration/index.html",
"es/administracion-programa-notas-privadas/index.html",
"en/capital-relationships/index.html",
"es/relaciones-de-capital/index.html",
"en/strategic-financial-relationship/index.html",
"es/relacion-financiera-estrategica/index.html",
"assets/montana-roja-capital-20260915.css",
"assets/platform-scale-20260916.css",
"assets/playa-blanca-return-poster.svg",
"assets/playa-blanca-arrival-poster.svg",
"assets/playa-blanca-oasis-poster.svg",
"assets/playa-blanca-location-diagram.svg",
"assets/playa-blanca-programme-section.svg",
"assets/project-horizon-masterplan.svg",
"assets/project-horizon-hero.svg",
"assets/project-horizon-location.svg",
"assets/project-horizon-suite.svg",
"assets/project-horizon-club.svg",
"assets/project-horizon-evening.svg",
"assets/project-horizon-active.svg",
"assets/institutional-capital-20260921.css",
"assets/capital-relationships-20260916.css",
"assets/strategic-financial-relationship-20260916.css",
"assets/styles.css",
]

def digest(b:bytes): return hashlib.sha256(b).hexdigest()

def safe(name:str):
    p=Path(name)
    if p.is_absolute() or ".." in p.parts: raise ValueError("unsafe artifact path "+name)

def load_homepage_review():
    review=json.loads((ROOT/HOMEPAGE_REVIEW).read_text(encoding="utf-8"))
    if review.get("schema")!=HOMEPAGE_SCHEMA or review.get("public_release_approved") is not True:
        raise ValueError("homepage scoped-release authority changed")
    if tuple(review.get("exact_path_set") or ())!=HOMEPAGE_PATHS:
        raise ValueError("homepage scoped-release path set changed")
    files=review.get("files") or {}
    if set(files)!=set(HOMEPAGE_PATHS):
        raise ValueError("homepage scoped-release file pins changed")
    for rel in HOMEPAGE_PATHS:
        src=ROOT/rel;pin=files[rel]
        raw=src.read_bytes()
        if (not src.is_file() or src.is_symlink() or pin.get("mode")!="100644"
            or len(raw)!=pin.get("bytes") or digest(raw)!=pin.get("sha256")):
            raise ValueError("homepage reviewed bytes changed: "+rel)
    return review

def write_overlay(public:Path,rel:str)->dict:
    src=ROOT/rel
    if not src.is_file() or src.is_symlink(): raise ValueError("missing overlay "+rel)
    raw=src.read_bytes()
    root_target=public/rel
    canonical_target=public/PREFIX/rel
    root_target.parent.mkdir(parents=True,exist_ok=True)
    canonical_target.parent.mkdir(parents=True,exist_ok=True)
    root_target.write_bytes(raw)
    canonical_target.write_bytes(raw)
    if root_target.read_bytes()!=canonical_target.read_bytes():
        raise ValueError("root/canonical alias mismatch: "+rel)
    return {"sha256":digest(raw),"bytes":len(raw)}

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
    homepage_review=load_homepage_review()
    pins={}
    for rel in OVERLAY:
        pins[rel]=write_overlay(public,rel)
    receipt={
      "schema":"por-derecho.truth-machine-scoped-pages.v1",
      "status":"SCOPED_TRUTH_MACHINE_OVERLAY_OVER_LAST_VERIFIED_GITLAB_PAGES",
      "source_commit":os.environ.get("CI_COMMIT_SHA"),
      "baseline_source":BASELINE_SOURCE,
      "baseline_pipeline":BASELINE_PIPELINE,
      "baseline_job":BASELINE_JOB,
      "baseline_files":BASELINE_FILES,
      "overlay":pins,
      "canonical_prefix":PREFIX,
      "root_and_canonical_aliases_updated":True,
      "homepage_repair_control":homepage_review["control_id"],
      "homepage_repair_paths":list(HOMEPAGE_PATHS),
      "private_evidence_published":False,
      "boundary":"Last verified GitLab Pages baseline plus exact Truth Machine/R33/Pulse overlay and the explicitly approved homepage/Future regression repair. Every overlay is written byte-identically to root and canonical-prefixed aliases; unrelated main failures remain isolated."
    }
    out=public/"assets/data/truth-machine-gitlab-scoped-release.json"
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("TRUTH_MACHINE_SCOPED_PAGES "+json.dumps(receipt,sort_keys=True))

if __name__=="__main__": main()
