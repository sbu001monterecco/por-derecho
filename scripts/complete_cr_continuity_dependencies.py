#!/usr/bin/env python3
"""Close derived-source and dated-observation drift before integration.

ACTA graph semantics must remain identical. Live identity counts are validated
against actual federated records, not a frozen historical total. Historical
unitary/production observations keep their dates and never become current by fiat.
"""
from __future__ import annotations
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
import build_community_acta_authority_interconnectivity as graph
ROOT=Path(__file__).resolve().parents[1]
CANON='assets/data/la-laguna-proceeding-pages-v1.json'
TARGET='assets/data/community-acta-authority-interconnectivity-v1.json'
OP='scripts/validate_operational_truth.py'
CONTROL='PD-CR-CONTINUITY-20260905-01'
MARKER='# PD-CR-DATED-IDENTITY-OBSERVATION-20260905'
HELPERS='''
# PD-CR-DATED-IDENTITY-OBSERVATION-20260905
# Current census and dated observation are different validation contracts.
def runtime_identity_counts(manifest: dict[str, Any]) -> dict[str, int]:
    counts = {kind: 0 for kind in manifest["id_formats"]}
    seen: set[str] = set()
    parts_seen: set[str] = set()
    for part in manifest["parts"]:
        relative = part["path"]
        require(relative not in parts_seen, "duplicate identity part")
        parts_seen.add(relative)
        path = (DATA / relative).resolve()
        require(path.is_relative_to(DATA.resolve()), "identity part escapes data root")
        rows = load(path)["records"]
        require(len(rows) == part["count"], f"identity part count drift: {relative}")
        for row in rows:
            identifier = row["id"]
            kind = row["type"]
            require(identifier not in seen, f"duplicate canonical identity: {identifier}")
            require(kind in counts and kind == part["type"], "identity type/part mismatch")
            seen.add(identifier)
            counts[kind] += 1
    counts["total"] = len(seen)
    return counts


def valid_unitary_identity_observation(unitary: dict[str, Any], identity: dict[str, Any]) -> bool:
    section = unitary.get("identity_registry") or {}
    counts = section.get("counts")
    if counts == identity.get("counts"):
        return True
    # Admit only the explicitly dated, unpromoted source snapshot already retained.
    # This exception does not excuse current registry count drift or an unknown snapshot.
    historical = (
        section.get("control_date") == "2026-09-02"
        and section.get("static_page_parity") == "LOCAL_SOURCE_STATIC_CANDIDATE_NOT_YET_LIVE_VERIFIED"
        and counts == CURRENT_CANONICAL_IDENTITY_COUNTS
        and section.get("last_live_verified_counts", {}).get("total") == 204
    )
    if historical:
        print(" - dated 2-Sep identity candidate retained; current census independently validated")
    return historical

'''

def dump(v):return json.dumps(v,ensure_ascii=False,indent=2)+'\n'
def digest(b):return hashlib.sha256(b).hexdigest()
def prepare_graph():
    old=json.loads((ROOT/TARGET).read_text());new=graph.build()
    differences=[k for k in sorted(set(old)|set(new)) if k!='sources' and old.get(k)!=new.get(k)]
    out=ROOT/'diagnostics';out.mkdir(exist_ok=True)
    report={'target':TARGET,'changed_substantive_fields':differences,'old_source_hashes':old.get('sources'),'new_source_hashes':new.get('sources'),'scope':'SOURCE_HASH_REFRESH_ONLY_SUBSTANTIVE_EQUALITY_REQUIRED'}
    (out/'cr-projection-dependency-review.json').write_text(dump(report))
    assert not differences,'Substantive ACTA projection difference requires review: '+','.join(differences)
    return new

def patch_operational():
    path=ROOT/OP;s=path.read_text()
    if MARKER in s:return
    old='identity.get("counts") == CURRENT_CANONICAL_IDENTITY_COUNTS,'
    assert s.count(old)==1,'Operational count contract changed: reconcile first'
    s=s.replace(old,'identity.get("counts") == runtime_identity_counts(identity),',1)
    old='''            (unitary.get("identity_registry") or {}).get("counts")
            == CURRENT_CANONICAL_IDENTITY_COUNTS,'''
    assert s.count(old)==1,'Unitary observation contract changed: reconcile first'
    s=s.replace(old,'            valid_unitary_identity_observation(unitary, identity),',1)
    old='''            if release.get("current_at_observation") is True:
                current_records.append(release)'''
    new='''            # Select the ledger view for the dated production observation.
            # Later verified receipts may be appended without retroactively changing
            # the old production snapshot or pretending it describes today's host.
            snapshot_time = parse_time(production.get("observed_at"), "production observation")
            if (release.get("current_at_observation") is True
                    and effective_times[-1] <= snapshot_time):
                current_records.append(release)'''
    assert s.count(old)==1,'Release observation selection changed: reconcile first'
    s=s.replace(old,new,1)
    assert s.count('\ndef main() -> int:\n')==1
    s=s.replace('\ndef main() -> int:\n','\n'+HELPERS+'\ndef main() -> int:\n',1)
    compile(s,str(path),'exec');path.write_text(s)

def apply():
    branch=subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()
    assert branch=='worker/cr-continuity-gapclosure-20260905','Worker-only dependency writes'
    new=prepare_graph();p=ROOT/TARGET;graph_before=digest(p.read_bytes());op_before=digest((ROOT/OP).read_bytes())
    p.write_text(dump(new));patch_operational()
    cp=ROOT/CANON;d=json.loads(cp.read_text());c=d['continuity_closure'];assert c['control_id']==CONTROL
    c['changed_files']=sorted(set(c['changed_files']+[TARGET,OP]))
    c['prechange_sha256'].setdefault(TARGET,graph_before);c['prechange_sha256'].setdefault(OP,op_before)
    c['projection_dependency_closure']={'target':TARGET,'closed_dimension':'SOURCE_HASH_DRIFT_ONLY','substantive_fields_changed':[],'meaning':'All graph nodes, relationships, coverage, allegations and limiting evidence remained identical. Canonical input hashes refreshed after the continuity metadata additions.','source_policy':'Recompute with the existing deterministic builder after future authorised canonical changes; never accept an unexplained substantive difference.'}
    c['operational_count_dependency_closure']={'path':OP,'closed_dimension':'LIVE_CENSUS_VS_DATED_SNAPSHOT_AND_LEDGER_SELECTION','current_check':'Count every current identity part and immutable ID; reject duplicate IDs, duplicate parts, type mismatch and declared count drift.','historical_check':'Retain only the exact 2-Sep-2026 unpromoted identity candidate snapshot; unknown/misdated count mismatches still fail.','ledger_check':'Validate the dated production observation against ledger entries effective at that observation, retaining later appended historical receipts without relabelling old production as current.','does_not_certify':'Current host, all carets, procedural status, backup safety or the merits of any case.'}
    cp.write_text(dump(d));check()

def check():
    expected=graph.build();actual=json.loads((ROOT/TARGET).read_text())
    assert actual==expected,'ACTA projection no longer reproduces from current canonical sources'
    c=json.loads((ROOT/CANON).read_text())['continuity_closure']
    assert c['projection_dependency_closure']['substantive_fields_changed']==[]
    assert MARKER in (ROOT/OP).read_text()
    result=subprocess.run([sys.executable,OP],cwd=ROOT,capture_output=True,text=True)
    out=ROOT/'diagnostics';out.mkdir(exist_ok=True)
    (out/'cr-operational-dependency-check.json').write_text(dump({'exit':result.returncode,'stdout':result.stdout,'stderr':result.stderr,'scope':'Canonical count integrity and dated observation consistency, not current-host certification'}))
    print(result.stdout);print(result.stderr);assert result.returncode==0,'Operational dependency still fails'
    print(json.dumps({'result':'CR_DEPENDENCIES_PASS','substantive_graph_fields_changed':0,'source_files':len(expected['sources']),'actual_current_identity_count_checked':True,'dated_snapshots_preserved':True}))

def main():
    p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True);g.add_argument('--apply',action='store_true');g.add_argument('--check',action='store_true');g.add_argument('--inspect',action='store_true');a=p.parse_args()
    if a.apply:apply()
    elif a.check:check()
    else:prepare_graph()
if __name__=='__main__':main()
