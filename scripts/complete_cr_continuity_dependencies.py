#!/usr/bin/env python3
"""Close derivative-hash drift without rewriting the ACTA evidential graph.

An inherited substantive difference is a review stop, not permission to silently
regenerate it. Run only before integration on the declared worker; CI --check is
read-only. Later integrators recompute the dependency after canonical reconciliation.
"""
from __future__ import annotations
import argparse,copy,hashlib,json,subprocess
from pathlib import Path
import build_community_acta_authority_interconnectivity as graph
ROOT=Path(__file__).resolve().parents[1]
CANON='assets/data/la-laguna-proceeding-pages-v1.json'
TARGET='assets/data/community-acta-authority-interconnectivity-v1.json'
CONTROL='PD-CR-CONTINUITY-20260905-01'

def dump(v):return json.dumps(v,ensure_ascii=False,indent=2)+'\n'
def digest(b):return hashlib.sha256(b).hexdigest()
def prepare():
    old=json.loads((ROOT/TARGET).read_text());new=graph.build()
    substantive_old={k:v for k,v in old.items() if k!='sources'}
    substantive_new={k:v for k,v in new.items() if k!='sources'}
    differences=[k for k in sorted(set(substantive_old)|set(substantive_new)) if substantive_old.get(k)!=substantive_new.get(k)]
    out=ROOT/'diagnostics';out.mkdir(exist_ok=True)
    report={'target':TARGET,'changed_substantive_fields':differences,'old_source_hashes':old.get('sources'),'new_source_hashes':new.get('sources'),'scope':'SOURCE_HASH_REFRESH_ONLY_SUBSTANTIVE_EQUALITY_REQUIRED'}
    (out/'cr-projection-dependency-review.json').write_text(dump(report))
    assert not differences,'Substantive ACTA projection difference requires review: '+','.join(differences)
    return new

def apply():
    branch=subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()
    assert branch=='worker/cr-continuity-gapclosure-20260905','Worker-only dependency writes'
    new=prepare();p=ROOT/TARGET;before=digest(p.read_bytes());p.write_text(dump(new))
    cp=ROOT/CANON;d=json.loads(cp.read_text());c=d['continuity_closure'];assert c['control_id']==CONTROL
    c['changed_files']=sorted(set(c['changed_files']+[TARGET]))
    c['prechange_sha256'].setdefault(TARGET,before)
    c['projection_dependency_closure']={'target':TARGET,'closed_dimension':'SOURCE_HASH_DRIFT_ONLY','substantive_fields_changed':[],'meaning':'All graph nodes, relationships, coverage, allegations and limiting evidence remained identical. Canonical input hashes refreshed after the continuity metadata additions.','source_policy':'Recompute with the existing deterministic builder after future authorised canonical changes; never accept an unexplained substantive difference.'}
    cp.write_text(dump(d));check()

def check():
    expected=graph.build();actual=json.loads((ROOT/TARGET).read_text())
    assert actual==expected,'ACTA projection no longer reproduces from current canonical sources'
    c=json.loads((ROOT/CANON).read_text())['continuity_closure']
    assert c['projection_dependency_closure']['substantive_fields_changed']==[]
    print(json.dumps({'result':'CR_PROJECTION_DEPENDENCY_PASS','substantive_fields_changed':0,'source_files':len(expected['sources']),'target':TARGET}))

def main():
    p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True);g.add_argument('--apply',action='store_true');g.add_argument('--check',action='store_true');g.add_argument('--inspect',action='store_true');a=p.parse_args()
    if a.apply:apply()
    elif a.check:check()
    else:prepare()
if __name__=='__main__':main()
