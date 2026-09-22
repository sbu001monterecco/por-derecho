#!/usr/bin/env python3
import json, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MODEL=ROOT/"assets/data/methodology-transparency-v1.json"
MANIFEST=ROOT/"publication-manifests/methodology-transparency-20260922.json"
CSS=ROOT/"assets/methodology-transparency-20260922.css"
EXPECTED=["observe","manifest","compare","classify","traverse","adversarial","reconcile","verify","deploy","readback","envelope"]
REQUIRED_INVARIANTS=["source_not_assertion","assertion_not_finding","authentication_not_truth","relationship_not_liability_transfer","chronology_not_causation","private_evidence_not_public_by_default"]
PRIVATE_PATTERNS=[r"drive\.google\.com",r"message[-_ ]?id",r"provider[-_ ]?id",r"storage[-_ ]?locator",r"api[_ -]?key",r"bearer\s+[A-Za-z0-9._-]+"]

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def fail(kind,path,observed,expected,next_step):
    raise ValueError(f"class={kind} path={path} observed={observed!r} expected={expected!r} next={next_step}")

def validate(root=ROOT):
    m=load(root/"assets/data/methodology-transparency-v1.json")
    manifest=load(root/"publication-manifests/methodology-transparency-20260922.json")
    ids=[x.get("id") for x in m.get("recursive_sequence",[])]
    if ids!=EXPECTED: fail("STAGE_ORDER_DRIFT","recursive_sequence",ids,EXPECTED,"restore_exact_public_method_sequence")
    if [x.get("order") for x in m["recursive_sequence"]]!=list(range(1,12)):
        fail("STAGE_ORDER_DRIFT","recursive_sequence.order",[x.get("order") for x in m["recursive_sequence"]],list(range(1,12)),"restore_contiguous_stage_order")
    c=m.get("constitutional",{})
    for key in REQUIRED_INVARIANTS:
        if c.get(key) is not True: fail("CONSTITUTIONAL_REGRESSION",f"constitutional.{key}",c.get(key),True,"restore_truth_seeking_invariant")
    if c.get("safeguards_self_modify") is not False: fail("CONSTITUTIONAL_REGRESSION","constitutional.safeguards_self_modify",c.get("safeguards_self_modify"),False,"restore_non_self_modifying_safeguards")
    if c.get("no_numeric_truth_score") is not True: fail("CONSTITUTIONAL_REGRESSION","constitutional.no_numeric_truth_score",c.get("no_numeric_truth_score"),True,"remove_numeric_truth_scoring")
    statuses=[x.get("status") for x in m.get("architecture_history",[])]
    if statuses!=["HISTORICAL_DESIGN","CONTROLLING_ACCEPTED","DRAFT_REVIEW"]:
        fail("ARCHITECTURE_HISTORY_DRIFT","architecture_history.status",statuses,["HISTORICAL_DESIGN","CONTROLLING_ACCEPTED","DRAFT_REVIEW"],"preserve_explicit_supersession_history")
    if m.get("public_release_approved") is not False or m.get("live_verified") is not False:
        fail("FALSE_RELEASE_PROMOTION","methodology_model",(m.get("public_release_approved"),m.get("live_verified")),(False,False),"obtain_authorised_merge_deploy_and_live_readback_first")
    if manifest.get("public_release_approved") is not False or manifest.get("live_verified") is not False:
        fail("FALSE_RELEASE_PROMOTION","publication_manifest",(manifest.get("public_release_approved"),manifest.get("live_verified")),(False,False),"keep_candidate_state_until_separate_release_closeout")
    if manifest.get("routes")!=["en/methodology/index.html","es/metodologia/index.html"]:
        fail("ROUTE_SET_DRIFT","publication_manifest.routes",manifest.get("routes"),["en/methodology/index.html","es/metodologia/index.html"],"restore_bilingual_route_set")
    if "method-loop" not in (root/"assets/methodology-transparency-20260922.css").read_text(encoding="utf-8"):
        fail("VISUAL_CONTRACT_DRIFT","assets/methodology-transparency-20260922.css","method-loop missing","method-loop present","restore_recursive_loop_visual")
    results=[]
    for lang,path in m["routes"].items():
        text=(root/path).read_text(encoding="utf-8")
        last=-1
        for order,stage_id in enumerate(EXPECTED,1):
            token=f'data-method-stage="{stage_id}" data-method-order="{order}"'
            pos=text.find(token)
            if pos<0 or pos<=last: fail("RENDERED_STAGE_DRIFT",path,stage_id,f"ordered stage {order}","regenerate_from_canonical_method_model")
            last=pos
        for marker in [f'data-methodology-control="{m["control_id"]}"','data-publication-status="PUBLIC_SAFE_CANDIDATE"','data-private-boundary="true"','data-live-verified="false"']:
            if marker not in text: fail("RENDERED_MARKER_MISSING",path,marker,"present","regenerate_candidate_page")
        for pattern in PRIVATE_PATTERNS:
            if re.search(pattern,text,re.I): fail("PUBLIC_PRIVATE_BOUNDARY",path,pattern,"absent","remove_private_locator_or_identifier")
        results.append(path)
    return {"status":"PASS","control_id":m["control_id"],"stages":len(EXPECTED),"routes":results,"architecture_records":len(m["architecture_history"]),"roles":len(m["supervised_roles"])}

def main():
    try: result=validate()
    except ValueError as exc: raise SystemExit(f"Methodology transparency: FAIL {exc}") from exc
    print("Methodology transparency: PASS")
    print(json.dumps(result,sort_keys=True))

if __name__=="__main__": main()
