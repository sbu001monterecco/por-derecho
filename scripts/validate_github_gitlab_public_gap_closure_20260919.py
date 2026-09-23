#!/usr/bin/env python3
"""Validate the GitHub-native public gap-closure control."""
from __future__ import annotations
import json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parents[1]
CONTROL = ROOT / "ops" / "continuity" / "GITHUB_GITLAB_PUBLIC_GAP_CLOSURE_20260919.json"
ALLOWED = {"EXACT_GITLAB_RECOVERY","EXACT_ALREADY_MIRRORED","FUNCTIONAL_GITHUB_EQUIVALENT","PENDING_GITLAB_RESTORATION"}

def validate() -> list[str]:
    failures=[]
    data=json.loads(CONTROL.read_text(encoding="utf-8"))
    if data.get("schema")!="por-derecho.github-gitlab-public-gap-closure.v1":
        failures.append("schema_mismatch")
    if data.get("status")!="CURRENT_GITHUB_FUNCTIONAL_SUCCESSORS_ADDED_EXACT_GITLAB_SOURCE_STILL_PENDING":
        failures.append("status_mismatch")
    if not re.fullmatch(r"[0-9a-f]{40}",data.get("github_base_sha","")):
        failures.append("github_base_sha_invalid")
    if data.get("authenticated_gitlab_restoration_verified") is not False:
        failures.append("authenticated_gitlab_restoration_must_remain_false")

    items={x.get("id"):x for x in data.get("items",[])}
    required={
        "IDENTITY_REGISTRY_515_VS_380",
        "RICPE_27AUG_STATUS",
        "PORTFOLIO_11SEP_STATUS",
        "RECOVERY_COMMAND_CENTER",
        "ASSET_RECOVERY_SITUATION_ROOM",
        "CONNECTIONS_EXPLORER",
        "DEEP_TEXT_SEARCH",
        "POR_DERECHO_OPERATING_STANDARD",
        "SPECIALIST_SEPTEMBER_PRESENTATION_ROUTES",
        "GITLAB_NATIVE_PLATFORM_STATE",
    }
    if not required.issubset(items):
        failures.append("required_item_missing")

    for ident,item in items.items():
        status=item.get("status")
        if status not in ALLOWED:
            failures.append(f"invalid_status:{ident}:{status}")
        if not item.get("boundary"):
            failures.append(f"boundary_missing:{ident}")
        routes=item.get("github_routes") or ([item["github_route"]] if item.get("github_route") else [])
        for route in routes:
            if not (ROOT/route).is_file():
                failures.append(f"github_route_missing:{ident}:{route}")

    if items["IDENTITY_REGISTRY_515_VS_380"].get("status")!="PENDING_GITLAB_RESTORATION":
        failures.append("identity_gap_must_remain_pending")
    en_identity=(ROOT/"en/matter-identity-registry/index.html").read_text(encoding="utf-8")
    es_identity=(ROOT/"es/registro-identidad-materia/index.html").read_text(encoding="utf-8")
    for text,label in ((en_identity,"en"),(es_identity,"es")):
        if "515" not in text or "380" not in text or "1535" not in text:
            failures.append(f"identity_gap_disclosure_missing:{label}")

    ric=(ROOT/"en/ric-private-equity-sun-park/index.html").read_text(encoding="utf-8")
    if "27 AUGUST 2026" not in ric or "Responsable del Sistema Interno de Información" not in ric:
        failures.append("ricpe_status_refresh_missing")
    portfolio=(ROOT/"en/portfolio-orion-traceability/index.html").read_text(encoding="utf-8")
    if "11 SEPTEMBER 2026" not in portfolio or "reported transmission of their content to CNMV" not in portfolio:
        failures.append("portfolio_status_refresh_missing")

    for route in (
        "en/recovery-command-center/index.html",
        "es/centro-mando-recuperacion/index.html",
        "en/asset-recovery-situation-room/index.html",
        "es/sala-situacion-recuperacion-activos/index.html",
        "en/connections-explorer/index.html",
        "es/explorador-conexiones/index.html",
    ):
        text=(ROOT/route).read_text(encoding="utf-8").lower()
        if "gitlab" not in text or ("byte" not in text and "bytes" not in text):
            failures.append(f"truth_boundary_missing:{route}")

    deep=items["DEEP_TEXT_SEARCH"]
    if deep.get("status")!="FUNCTIONAL_GITHUB_EQUIVALENT":
        failures.append("deep_text_search_status_invalid")
    deep_control=ROOT/deep.get("github_control","")
    if not deep_control.is_file():
        failures.append("deep_text_search_control_missing")
    else:
        deep_text=deep_control.read_text(encoding="utf-8").lower()
        for token in ("does not query gitlab", "discovery aid", "same-project links"):
            if token not in deep_text:
                failures.append(f"deep_text_search_boundary_missing:{token}")
    for route in ("en/search/index.html","es/buscar/index.html"):
        text=(ROOT/route).read_text(encoding="utf-8")
        if "connected-search-20260919.js" not in text:
            failures.append(f"deep_text_search_not_loaded:{route}")

    specialist=items["SPECIALIST_SEPTEMBER_PRESENTATION_ROUTES"]
    if specialist.get("status")!="FUNCTIONAL_GITHUB_EQUIVALENT":
        failures.append("specialist_routes_not_functional")
    if specialist.get("exact_gitlab_source_state")!="PENDING_GITLAB_RESTORATION":
        failures.append("specialist_exact_gitlab_source_state_not_pending")
    specialist_control=ROOT/specialist.get("github_control","")
    if not specialist_control.is_file():
        failures.append("specialist_route_control_missing")
    native=items["GITLAB_NATIVE_PLATFORM_STATE"]
    if native.get("status")!="PENDING_GITLAB_RESTORATION":
        failures.append("gitlab_native_state_must_remain_pending")

    rules=" ".join(data.get("rules",[])).lower()
    for token in (
        "not exact gitlab byte parity",
        "cannot supply unavailable exact source bytes",
        "do not create missing identity ids",
        "reconciled additively",
    ):
        if token not in rules:
            failures.append(f"rule_missing:{token}")
    return failures

def main() -> int:
    failures=validate()
    print(json.dumps({
        "schema":"por-derecho.github-gitlab-public-gap-closure-validation.v1",
        "status":"PASS" if not failures else "FAIL",
        "control":str(CONTROL.relative_to(ROOT)),
        "failures":failures,
    },indent=2,ensure_ascii=False,sort_keys=True))
    return 0 if not failures else 1

if __name__=="__main__":
    raise SystemExit(main())
