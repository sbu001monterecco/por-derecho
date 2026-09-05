#!/usr/bin/env python3
"""Complete the existing identity queue and formal publication manifest for PD-CR.

This supplements, rather than replaces, the source/page builder. Writes remain
integration-only. Every original operational-control field and queue row is
preserved; a new unresolved identity must have a corresponding verification task.
The institutional-communications register is outside this queue update and
remains unchanged: private professional recovery is not an authority notice.
"""
from __future__ import annotations
import argparse,json,subprocess,time
from pathlib import Path
from urllib.request import Request,urlopen
import build_cuatrecasas_rauda_20260905 as review

QUEUE='assets/data/matter-identity-operational-control-v1.json'
MANIFEST='publication-manifests/cuatrecasas-rauda-recovery-review-20260905.json'

def outputs():
    audit=json.loads((review.ROOT/review.AUDIT).read_text())
    rid=audit['rauda_identity_id']
    q=json.loads(review.original(QUEUE))
    assert not any(x['id']==rid for x in q['exact_identity_queue'])
    q['exact_identity_queue'].append({'id':rid,'priority':'P1','question_es':'Identificar la entidad jurídica y forma social exactas de RAUDA que intervinieron en el recobro de 2022; separar marca, empleador de los profesionales, mandante, titular del crédito y cualquier eventual cesionario. No inferir mandato anterior, adquisición ni responsabilidad.','question_en':'Identify the exact RAUDA legal entity and legal form involved in 2022 recovery; distinguish brand, professionals employer, instructing party, debt owner and any eventual cessionary. Do not infer an earlier mandate, acquisition or liability.','source_controls':['PD-CR-COM-20220218','PD-CR-COM-20220307'],'review_control':review.CONTROL})
    source=sorted(set(audit['outputs']+[review.AUDIT,QUEUE,'scripts/build_cuatrecasas_rauda_20260905.py','scripts/complete_cuatrecasas_rauda_controls_20260905.py','assets/content/cuatrecasas-rauda-20260905.es.html','assets/content/cuatrecasas-rauda-20260905.en.html','.github/workflows/cuatrecasas-rauda-publication.yml']))
    manifest={'schema':'por-derecho.publication-manifest.v1','publication_id':review.CONTROL,'current_state':'REMOTE_SOURCE','owner':'Por Derecho / Gil Marer authorised scoped integration','control_date':'2026-09-05','source_base':review.BASE,'source_branch':review.BRANCH,'external_mutation_authorized':True,'authority':'User instruction: Deployment of all; public-safe scope only.','expected_routes':{lang:[p['path'] for p in audit['pages'] if p['path'].startswith(lang+'/')] for lang in ('es','en')},'expected_source_files':source,'merge_sha':None,'publication_boundary':'No private handoff, native court files, original emails, provider locators, verification metadata or counsel-facing strategy. Existing public-safe court texts and canonical acts are referenced, not duplicated.','validation':{'commands':['python scripts/build_cuatrecasas_rauda_20260905.py --check','python scripts/complete_cuatrecasas_rauda_controls_20260905.py --check','python scripts/validate_operational_identity_registry.py'],'evidence':['Preparation run 33970163169: 206 source/preservation checks passed; this is not PR-CI or live certification.'],'inherited_baseline_gaps':['Existing historic-proceedings-authority-reintegration-20260903 manifest lacks required fields.','Existing es/acosta-matos-familia link points to missing es/metodologia.'],'state_boundary':'Final checks, exact merge, Pages deployment and live readback are reported in the PR and Control Tower; this manifest is a remote-source snapshot, not a self-certifying LIVE_VERIFIED claim.'},'closeout_tracker':{'control_tower_issue':1428,'pull_request':1464,'required':['Current main and exact reviewed head','No new preservation, identity or publication failures','Bilingual desktop/mobile/no-script checks','Successful Pages run for merged commit','Exact managed blocks and public control files read back']},'continuity':review.NOTE,'identity_queue':QUEUE,'source_control':review.CANON,'institutional_communications_preserved':333}
    return {QUEUE:review.dump(q),MANIFEST:review.dump(manifest)}

def check(out):
    for path,text in out.items():assert (review.ROOT/path).read_text()==text,'Control drift: '+path
    old=json.loads(review.original(QUEUE));new=json.loads(out[QUEUE])
    assert new['exact_identity_queue'][:len(old['exact_identity_queue'])]==old['exact_identity_queue']
    assert len(new['exact_identity_queue'])==len(old['exact_identity_queue'])+1
    for key,value in old.items():
        if key!='exact_identity_queue':assert new[key]==value,'Existing identity control changed: '+key
    m=json.loads(out[MANIFEST]);assert len(m['expected_routes']['es'])==len(m['expected_routes']['en'])==12
    for path in m['expected_source_files']:assert (review.ROOT/path).is_file(),path
    print(json.dumps({'result':'CONTROL_COMPLETENESS_PASS','identity_queue_rows':len(new['exact_identity_queue']),'new_identity_queue_entries':1,'formal_manifest':MANIFEST,'existing_controls_preserved':True}))

def main():
    p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True);g.add_argument('--write',action='store_true');g.add_argument('--check',action='store_true');g.add_argument('--live',action='store_true');a=p.parse_args();out=outputs()
    if a.write:
        assert review.git('branch','--show-current')==review.BRANCH
        assert review.git('rev-parse','origin/main')==review.BASE
        for path,text in out.items():
            f=review.ROOT/path;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(text)
        check(out)
    elif a.check:check(out)
    else:
        pending=dict(out);head=review.git('rev-parse','HEAD');deadline=time.monotonic()+600
        while pending and time.monotonic()<deadline:
            for path,text in list(pending.items()):
                try:
                    req=Request(review.SITE+path+'?pd-cr='+head,headers={'Cache-Control':'no-cache','User-Agent':'PorDerecho-Control-Verification'})
                    with urlopen(req,timeout=25) as response:actual=response.read().decode('utf-8')
                    if actual==text:print('LIVE_CONTROL_MATCH',path,head);del pending[path]
                except Exception as exc:print('LIVE_CONTROL_PENDING',path,type(exc).__name__)
            if pending:time.sleep(15)
        assert not pending,'Control readback incomplete: '+','.join(pending)
        print(json.dumps({'result':'LIVE_CONTROLS_VERIFIED','commit':head,'resources':len(out)}))

if __name__=='__main__':main()
