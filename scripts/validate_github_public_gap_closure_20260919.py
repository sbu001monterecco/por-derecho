#!/usr/bin/env python3
"""Validate the 19 Sep GitHub-native public gap closure."""
from __future__ import annotations
import json, pathlib, re, sys

ROOT=pathlib.Path(__file__).resolve().parents[1]
LEDGER=ROOT/"ops/continuity/GITHUB_PUBLIC_GAP_CLOSURE_20260919.json"

def read(path:str)->str:
    p=ROOT/path
    if not p.is_file():
        raise FileNotFoundError(path)
    return p.read_text(encoding="utf-8")

def validate()->list[str]:
    f=[]
    try:
        data=json.loads(LEDGER.read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"ledger_unreadable:{exc}"]
    if data.get("schema")!="por-derecho.github-public-gap-closure.v1": f.append("schema_mismatch")
    if data.get("status")!="ACTIVE_GITHUB_NATIVE_GAP_CLOSURE": f.append("status_mismatch")
    if data.get("base_main_sha")!="bebedf4cc1d1321f00072d2d2d53536505611363": f.append("base_sha_drift")
    closures={x.get("id"):x for x in data.get("closures",[])}
    for ident in ("REGISTRY_FRESHNESS_DISCLOSURE","PORTFOLIO_SEPTEMBER_STATUS","RICPE_27AUG_RESOLVER_IDENTITY","RECOVERY_COMMAND_CENTER","DEEP_TEXT_CONNECTION_SCAN","POR_DERECHO_OPERATING_STANDARD"):
        if ident not in closures: f.append(f"closure_missing:{ident}")

    required=[
      "en/recovery-command-center/index.html","es/centro-mando-recuperacion/index.html",
      "assets/connected-search-20260919.js","en/search/index.html","es/buscar/index.html",
      "en/matter-identity-registry/index.html","es/registro-identidad-materia/index.html",
      "en/portfolio-orion-traceability/index.html","es/portfolio-orion-trazabilidad/index.html",
      "en/ric-private-equity-sun-park/index.html","es/ric-private-equity-sun-park/index.html",
      "en/por-derecho/index.html","es/por-derecho/index.html",
      "assets/data/unitary-route-registry-v1.json","sitemap-unitary-shell.xml"
    ]
    blobs={}
    for path in required:
        try: blobs[path]=read(path)
        except FileNotFoundError: f.append(f"missing:{path}")

    for path in ("en/matter-identity-registry/index.html","es/registro-identidad-materia/index.html"):
        c=blobs.get(path,"")
        for token in ("379","515","136","#1535","data-gitlab-registry-freshness-gap"):
            if token not in c: f.append(f"registry_gap_missing:{path}:{token}")
    en=blobs.get("en/portfolio-orion-traceability/index.html","")
    es=blobs.get("es/portfolio-orion-trazabilidad/index.html","")
    for token in ("11 SEPTEMBER 2026","reported transmission of their content to CNMV","does not establish"):
        if token.lower() not in en.lower(): f.append(f"portfolio_en_missing:{token}")
    for token in ("11 SEPTIEMBRE 2026","transmisión comunicada de su contenido a CNMV","no acredita"):
        if token.lower() not in es.lower(): f.append(f"portfolio_es_missing:{token}")

    en=blobs.get("en/ric-private-equity-sun-park/index.html","")
    es=blobs.get("es/ric-private-equity-sun-park/index.html","")
    for token in ("27 AUGUST 2026","does not prove unauthorised access","native audit trail"):
        if token.lower() not in en.lower(): f.append(f"ricpe_en_missing:{token}")
    for token in ("27 AGOSTO 2026","no prueba acceso no autorizado","audit trail nativo"):
        if token.lower() not in es.lower(): f.append(f"ricpe_es_missing:{token}")

    for path, tokens in {
      "en/recovery-command-center/index.html":["trace → preserve → protect → recover → reconcile","../search/","../matter-identity-registry/","second-pair-of-eyes"],
      "es/centro-mando-recuperacion/index.html":["trazar → preservar → proteger → recuperar → reconciliar","../buscar/","../registro-identidad-materia/","segundo-par-de-ojos"]
    }.items():
        c=blobs.get(path,"").lower()
        for token in tokens:
            if token.lower() not in c: f.append(f"command_route_missing:{path}:{token}")

    for path in ("en/search/index.html","es/buscar/index.html"):
        if "connected-search-20260919.js" not in blobs.get(path,""): f.append(f"deep_search_not_loaded:{path}")
    js=blobs.get("assets/connected-search-20260919.js","")
    for token in ("PorDerechoUnitaryShell","loadEntries","u.origin!==location.origin","projectMarker='/por-derecho/'","credentials:'same-origin'"):
        if token not in js: f.append(f"deep_search_control_missing:{token}")
    if "gitlab.com" in js.lower() or "gitlab.io" in js.lower(): f.append("deep_search_gitlab_dependency_present")

    for path,marker in (("en/por-derecho/index.html","operating-standard-20260919"),("es/por-derecho/index.html","estandar-operativo-20260919")):
        if marker not in blobs.get(path,""): f.append(f"operating_standard_missing:{path}")

    try:
        routes=json.loads(blobs.get("assets/data/unitary-route-registry-v1.json","[]"))
        paths={x.get("path") for x in routes}
        for p in ("en/recovery-command-center/","es/centro-mando-recuperacion/"):
            if p not in paths: f.append(f"route_registry_missing:{p}")
    except Exception as exc: f.append(f"route_registry_invalid:{exc}")
    sitemap=blobs.get("sitemap-unitary-shell.xml","")
    for p in ("/en/recovery-command-center/","/es/centro-mando-recuperacion/"):
        if p not in sitemap: f.append(f"sitemap_missing:{p}")

    rules=" ".join(data.get("rules",[])).lower()
    for token in ("no private recovery corpus","no unavailable gitlab bytes","functional equivalents","exact-head outage backend parity"):
        if token not in rules: f.append(f"rule_missing:{token}")
    return f

def main()->int:
    failures=validate()
    print(json.dumps({"schema":"por-derecho.github-public-gap-closure-validation.v1","status":"PASS" if not failures else "FAIL","failures":failures},indent=2,ensure_ascii=False))
    return 0 if not failures else 1

if __name__=="__main__":
    raise SystemExit(main())
