#!/usr/bin/env python3
import argparse, hashlib, html, json, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
EXPECTED=["observe","manifest","compare","classify","traverse","adversarial","reconcile","verify","deploy","readback","envelope"]
REQUIRED_INVARIANTS=["source_not_assertion","assertion_not_finding","authentication_not_truth","relationship_not_liability_transfer","chronology_not_causation","private_evidence_not_public_by_default"]
ORIGINS={"github":"https://sbu001monterecco.github.io/por-derecho","gitlab":"https://por-derecho.gitlab.io/por-derecho-setup-or-gitlab-setup"}
PRIVATE_PATTERNS=[
    r"drive\.google\.com",r"(?:dropbox\.com|1drv\.ms|onedrive\.live\.com|[^/]+\.sharepoint\.com|s3[.-][^/]*amazonaws\.com)",
    r"message[-_ ]?id",r"provider[-_ ]?id",r"storage[-_ ]?locator",r"api[_ -]?key",r"bearer\s+[A-Za-z0-9._-]+",
    r"\bsk-[A-Za-z0-9_-]{16,}\b",r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}",
    r"https?://[^\s\"']+[?&](?:token|sig|key|auth|access_token)=",
    r"\b(?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}\.\d{1,3}|172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3})\b"
]

def load(path): return json.loads(path.read_text(encoding="utf-8"))
def git_blob_sha(path):
    data=path.read_bytes(); return hashlib.sha1(f"blob {len(data)}\0".encode()+data).hexdigest()
def fail(kind,path,observed,expected,next_step): raise ValueError(f"class={kind} path={path} observed={observed!r} expected={expected!r} next={next_step}")
def visible_text(text): return " ".join(html.unescape(re.sub(r"<[^>]+>"," ",text)).split())

def model_fragments(m,lang):
    out=[]
    for s in m["recursive_sequence"]: out += [s[lang]["title"],s[lang]["tagline"],s[lang]["body"],s[lang]["stop"]]
    for r in m["non_equivalences"]: out += [r[0] if lang=="en" else r[1],r[2] if lang=="en" else r[3]]
    for r in m["supervised_roles"]: out += [r[lang]["title"],r[lang]["body"]]
    for r in m["architecture_history"]: out += [r["control"],r[lang]]
    for r in m["host_states"]: out += [r[lang],r["body_"+lang]]
    for r in m["parity_states"]: out += [r[lang],r["body_"+lang]]
    out += [m["public_private"][lang],m["two_key"][lang]["a"]["title"],m["two_key"][lang]["a"]["body"],m["two_key"][lang]["b"]["title"],m["two_key"][lang]["b"]["body"],m["two_key"][lang]["rule"],m["challenge"][lang]["title"],m["challenge"][lang]["body"]]
    return out

def validate(root=ROOT,host=None):
    model_path=root/"assets/data/methodology-transparency-v1.json"; m=load(model_path); manifest=load(root/"publication-manifests/methodology-transparency-20260922.json")
    ids=[x.get("id") for x in m.get("recursive_sequence",[])]
    if ids!=EXPECTED: fail("STAGE_ORDER_DRIFT","recursive_sequence",ids,EXPECTED,"restore_exact_public_method_sequence")
    if [x.get("order") for x in m["recursive_sequence"]]!=list(range(1,12)): fail("STAGE_ORDER_DRIFT","recursive_sequence.order",[x.get("order") for x in m["recursive_sequence"]],list(range(1,12)),"restore_contiguous_stage_order")
    c=m.get("constitutional",{})
    for key in REQUIRED_INVARIANTS:
        if c.get(key) is not True: fail("CONSTITUTIONAL_REGRESSION",f"constitutional.{key}",c.get(key),True,"restore_truth_seeking_invariant")
    if c.get("safeguards_self_modify") is not False: fail("CONSTITUTIONAL_REGRESSION","constitutional.safeguards_self_modify",c.get("safeguards_self_modify"),False,"restore_non_self_modifying_safeguards")
    if c.get("no_numeric_truth_score") is not True: fail("CONSTITUTIONAL_REGRESSION","constitutional.no_numeric_truth_score",c.get("no_numeric_truth_score"),True,"remove_numeric_truth_scoring")
    statuses=[x.get("status") for x in m.get("architecture_history",[])]
    if statuses!=["HISTORICAL_DESIGN","CONTROLLING_ACCEPTED","DRAFT_REVIEW"]: fail("ARCHITECTURE_HISTORY_DRIFT","architecture_history.status",statuses,["HISTORICAL_DESIGN","CONTROLLING_ACCEPTED","DRAFT_REVIEW"],"preserve_explicit_supersession_history")
    if m.get("public_release_approved") is not False or m.get("live_verified") is not False: fail("FALSE_RELEASE_PROMOTION","methodology_model",(m.get("public_release_approved"),m.get("live_verified")),(False,False),"obtain_authorised_merge_deploy_and_live_readback_first")
    if manifest.get("schema")!="por-derecho.publication-state.v1" or manifest.get("schema_version")!="1.0.0": fail("PUBLICATION_SCHEMA_DRIFT","publication_manifest.schema",(manifest.get("schema"),manifest.get("schema_version")),("por-derecho.publication-state.v1","1.0.0"),"use_repository_publication_state_contract")
    if manifest.get("current_state")!="PR_OPEN": fail("FALSE_RELEASE_PROMOTION","publication_manifest.current_state",manifest.get("current_state"),"PR_OPEN","keep_candidate_at_pr_open_until_release_closeout")
    if manifest.get("public_release_approved") is not False or manifest.get("live_verified") is not False or manifest.get("deployed") is not False: fail("FALSE_RELEASE_PROMOTION","publication_manifest",(manifest.get("public_release_approved"),manifest.get("deployed"),manifest.get("live_verified")),(False,False,False),"keep_candidate_state_until_release_closeout")
    expected_routes={"en":["en/methodology/index.html"],"es":["es/metodologia/index.html"]}
    if manifest.get("expected_routes")!=expected_routes: fail("ROUTE_SET_DRIFT","publication_manifest.expected_routes",manifest.get("expected_routes"),expected_routes,"restore_bilingual_route_set")
    css=root/"assets/methodology-transparency-20260922.css"
    if not css.is_file(): fail("MISSING_ASSET",str(css),"absent","present","restore_methodology_css_asset")
    if "method-loop" not in css.read_text(encoding="utf-8"): fail("VISUAL_CONTRACT_DRIFT",str(css),"method-loop missing","method-loop present","restore_recursive_loop_visual")
    expected_blob=git_blob_sha(model_path); results=[]
    for lang,path in m["routes"].items():
        raw=(root/path).read_text(encoding="utf-8"); plain=visible_text(raw)
        last=-1
        for order,sid in enumerate(EXPECTED,1):
            token=f'data-method-stage="{sid}" data-method-order="{order}"'; pos=raw.find(token)
            if pos<0 or pos<=last: fail("RENDERED_STAGE_DRIFT",path,sid,f"ordered stage {order}","regenerate_from_canonical_method_model")
            last=pos
        for marker in [f'data-methodology-control="{m["control_id"]}"',f'data-methodology-model-blob="{expected_blob}"','data-publication-status="PUBLIC_SAFE_CANDIDATE"','data-private-boundary="true"','data-live-verified="false"']:
            if marker not in raw: fail("RENDERED_MARKER_MISSING",path,marker,"present","regenerate_candidate_page")
        projected=re.search(r'data-projection-host="(github|gitlab)"',raw)
        if not projected: fail("HOST_PROJECTION_MISSING",path,"absent","github_or_gitlab","regenerate_with_host_specific_projection")
        page_host=projected.group(1)
        if host and page_host!=host: fail("HOST_PROJECTION_MISMATCH",path,page_host,host,"render_pages_for_current_host")
        actual_host=host or page_host; origin=ORIGINS[actual_host]; route="/en/methodology/" if lang=="en" else "/es/metodologia/"
        if f'<link rel="canonical" href="{origin}{route}">' not in raw: fail("CANONICAL_ORIGIN_MISMATCH",path,"unexpected canonical",origin+route,"render_host_specific_canonical_urls")
        for frag in model_fragments(m,lang):
            if " ".join(str(frag).split()) not in plain: fail("MODEL_PROJECTION_DRIFT",path,frag,"visible model fragment","regenerate_page_from_model")
        for pattern in PRIVATE_PATTERNS:
            if re.search(pattern,raw,re.I): fail("PUBLIC_PRIVATE_SENTINEL",path,pattern,"absent","remove_private_locator_identifier_or_credential")
        results.append(path)
    return {"status":"PASS","control_id":m["control_id"],"stages":len(EXPECTED),"routes":results,"architecture_records":len(m["architecture_history"]),"roles":len(m["supervised_roles"]),"publication_state":manifest["current_state"],"model_blob":expected_blob,"host":host or "per_page_marker"}

def main():
    p=argparse.ArgumentParser(); p.add_argument("--host",choices=ORIGINS); args=p.parse_args()
    control_id="UNKNOWN"
    try:
        mp=ROOT/"assets/data/methodology-transparency-v1.json"
        if mp.is_file(): control_id=load(mp).get("control_id","UNKNOWN")
        result=validate(ROOT,args.host)
    except Exception as exc:
        raise SystemExit(f"Methodology transparency: FAIL script=validate_methodology_transparency.py control_id={control_id} {exc}") from exc
    print("Methodology transparency: PASS")
    print(json.dumps(result,sort_keys=True))

if __name__=="__main__": main()
