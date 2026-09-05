#!/usr/bin/env python3
"""Atomic publication permits and recoverable readback; never edits main or merges.

Only exact owner commands in Control Tower1428 are accepted. The connected app
performs the normal protected merge after this controller records an exact-SHA
permit. Exclusive server enforcement requires Administration access separately.
"""
from __future__ import annotations
import base64
from copy import deepcopy
import json
import os
from pathlib import Path
import re
import time
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen, HTTPRedirectHandler, build_opener
from pd_release_contract import TERMINAL, advance, safe_path, sha256, utc_now

REPO = 'sbu001monterecco/por-derecho'
OWNER = 'sbu001monterecco'
STATE_BRANCH = 'pd-publication-state'
STATE_FILE = 'state.json'
HOST = 'https://sbu001monterecco.github.io/por-derecho/'
API = 'https://api.github.com/repos/'+REPO+'/'
PATTERN = re.compile(r'^/pd-release (claim|verify|recover|abort) ([1-9][0-9]*) ([a-f0-9]{40})\s*$')
CHECKS = {'PD release acceptance', 'publication-integrity'}


class NoApiRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError("Authenticated API redirects are not allowed")


class GitHub:
    def __init__(self):
        self.token = os.environ['GH_TOKEN']
    def request(self, path, data=None, method=None):
        if data is not None:
            allowed = (
                (path == 'contents/'+STATE_FILE and method == 'PUT' and data.get('branch') == STATE_BRANCH)
                or (path == 'git/refs' and data.get('ref') == 'refs/heads/'+STATE_BRANCH)
                or (path == 'git/trees' and len(data.get('tree', [])) == 1 and data['tree'][0].get('path') == STATE_FILE)
                or (path == 'git/commits' and data.get('parents') == [] and data.get('tree'))
            )
            if not allowed:
                raise ValueError('Controller writes are confined to its state-only branch; main/merge writes are prohibited')
        request = Request(API+path, data=None if data is None else json.dumps(data).encode(),
                          method=method, headers={'Authorization':'Bearer '+self.token,
                          'Accept':'application/vnd.github+json','Content-Type':'application/json'})
        with build_opener(NoApiRedirect()).open(request, timeout=40) as response:
            raw = response.read()
            return json.loads(raw) if raw else None
    def pages(self, path, key=None):
        for number in range(1,101):
            value = self.request(path+('&' if '?' in path else '?')+f'per_page=100&page={number}')
            rows = value[key] if key else value
            yield from rows
            if len(rows) < 100:
                return
        raise ValueError('Pagination cap reached; incomplete data cannot authorize publication')
    def state(self):
        try:
            value = self.request('contents/'+STATE_FILE+'?ref='+STATE_BRANCH)
            return json.loads(base64.b64decode(value['content'])), value['sha']
        except HTTPError as error:
            if error.code != 404:
                raise
            # Orphan state-only branch. Concurrent initialization fails rather than
            # overwriting the winning ref; subsequent reads always use its blob SHA.
            initial = {'schema':'por-derecho.publication-runtime.v1','fence':0,'phase':'ABORTED_BEFORE_MERGE','receipts':[]}
            tree = self.request('git/trees',{'tree':[{'path':STATE_FILE,'mode':'100644','type':'blob','content':json.dumps(initial)}]})
            commit = self.request('git/commits',{'message':'Initialize publication runtime; no website content','tree':tree['sha'],'parents':[]})
            try:
                self.request('git/refs',{'ref':'refs/heads/'+STATE_BRANCH,'sha':commit['sha']})
            except HTTPError as race:
                if race.code != 422:
                    raise
            value = self.request('contents/'+STATE_FILE+'?ref='+STATE_BRANCH)
            return json.loads(base64.b64decode(value['content'])), value['sha']
    def save(self, state, expected_sha):
        body = json.dumps(state,ensure_ascii=False,indent=2)+'\n'
        result = self.request('contents/'+STATE_FILE,{'branch':STATE_BRANCH,'sha':expected_sha,
                    'message':'Publication runtime checkpoint: '+state['phase'],
                    'content':base64.b64encode(body.encode()).decode()},'PUT')
        return result['content']['sha']


def command(event: dict) -> tuple[str,int,str]:
    if event.get('repository',{}).get('full_name') != REPO or event.get('issue',{}).get('number') != 1428:
        raise ValueError('Wrong repository/control issue')
    comment = event.get('comment',{})
    if comment.get('user',{}).get('login') != OWNER or comment.get('author_association') != 'OWNER':
        raise ValueError('Only the repository owner may authorize a publication command')
    match = PATTERN.fullmatch(comment.get('body','').strip())
    if not match:
        raise ValueError('Command must identify an exact operation, PR and candidate SHA')
    return match[1], int(match[2]), match[3]


def successful_checks(api, sha):
    latest = {}
    for check in api.pages('commits/'+sha+'/check-runs', 'check_runs'):
        if check['name'] not in CHECKS:
            continue
        if check.get('app',{}).get('slug') != 'github-actions' or check.get('head_sha') != sha:
            continue
        if check['name'] not in latest or check['id'] > latest[check['name']]['id']:
            latest[check['name']] = check
    missing = [name for name in CHECKS if name not in latest or latest[name]['status'] != 'completed' or latest[name]['conclusion'] != 'success']
    if missing:
        raise ValueError('Required exact-SHA successful checks missing: '+', '.join(sorted(missing)))
    return [{'name':x['name'],'id':x['id'],'conclusion':x['conclusion']} for x in latest.values()]


def previous_run_stopped(api, state):
    run = state.get('run_id')
    if run and str(run) != os.environ.get('GITHUB_RUN_ID'):
        if api.request('actions/runs/'+str(run))['status'] != 'completed':
            raise ValueError('Previous publication controller is still active')


def verify(api, state, blob, pr):
    if not pr['merged'] or pr['head']['sha'] != state['candidate_sha']:
        raise ValueError('No merge for the claimed exact candidate')
    merge = pr['merge_commit_sha']
    if api.request('git/ref/heads/main')['object']['sha'] != merge:
        raise ValueError('Main advanced: investigate successor bytes; never roll back')
    def checkpoint(phase,evidence):
        nonlocal state,blob
        state=advance(state,phase,state['owner'],state['fence'],evidence)
        state['run_id']=int(os.environ['GITHUB_RUN_ID']);blob=api.save(state,blob)
    if state['phase'] == 'ACCEPTED':
        checkpoint('MERGE_PENDING',{'pr':pr['number']})
    if state['phase'] in {'MERGE_PENDING','RECOVERY_REQUIRED'}:
        checkpoint('MERGED',{'merge_sha':merge})
    until=time.monotonic()+480
    pages_run=None
    while time.monotonic()<until:
        candidates=[r for r in api.pages('actions/runs?head_sha='+merge,'workflow_runs')
                    if r['name']=='pages build and deployment' and r['head_sha']==merge]
        if candidates:
            latest=max(candidates,key=lambda r:r['id'])
            if latest['status']=='completed':
                if latest['conclusion']!='success':
                    raise ValueError('Exact Pages deployment failed')
                pages_run=latest;break
        time.sleep(10)
    if not pages_run:
        raise ValueError('Exact Pages deployment is missing or incomplete')
    if state['phase']=='MERGED':
        checkpoint('DEPLOYED',{'pages_run_id':pages_run['id'],'merge_sha':merge})
    files=list(api.pages('pulls/'+str(pr['number'])+'/files'))
    if len(files)!=pr['changed_files']:
        raise ValueError('Incomplete changed-file scope')
    paths={'en/index.html','es/index.html'}
    for row in files:
        path=safe_path(row['filename'])
        if row['status']=='removed':
            raise ValueError('Deletion requires a dedicated approved live compatibility scope')
        if path.startswith(('en/','es/','assets/','ops/','publication-manifests/')):
            paths.add(path)
    # Request expected bytes from exact Git blobs; tokens never go to public host.
    expected={}
    for path in sorted(paths):
        value=api.request('contents/'+quote(path,safe='/')+'?ref='+merge)
        if value.get('encoding')!='base64':
            raise ValueError('Explicit byte-verification capability needed for large file: '+path)
        expected[path]=base64.b64decode(value['content'])
    results=[];pending=set(expected);until=time.monotonic()+300
    while pending and time.monotonic()<until:
        for path in sorted(pending):
            try:
                with urlopen(Request(HOST+quote(path,safe='/')+'?pd_release='+merge,
                             headers={'Cache-Control':'no-cache','User-Agent':'PorDerecho-Release-Readback'}),timeout=25) as response:
                    actual=response.read()
                if actual==expected[path]:
                    results.append({'path':path,'sha256':sha256(actual),'bytes':len(actual)})
                    pending.remove(path)
            except (OSError,HTTPError):
                continue
        if pending:
            time.sleep(10)
    Path('/tmp/pd-release-controller/readback.json').write_text(json.dumps({'merge_sha':merge,'pages_run_id':pages_run['id'],'exact_matches':results,'pending':sorted(pending)},indent=2)+'\n')
    if pending:
        raise ValueError('Public byte mismatch/missing resources: '+', '.join(sorted(pending)))
    if api.request('git/ref/heads/main')['object']['sha']!=merge:
        raise ValueError('Main advanced during verification; successor review required')
    receipt={'merge_sha':merge,'pages_run_id':pages_run['id'],'exact_matches':results,'pending':[],
             'scope':'Changed readable public resources plus ES/EN entrypoints. Browser checks are separate premerge evidence; not a whole-site or legal-proof certificate.'}
    state=advance(state,'VERIFIED_FOR_SCOPE',state['owner'],state['fence'],receipt)
    state['run_id']=int(os.environ['GITHUB_RUN_ID'])
    state.setdefault('receipts',[]).append({'pr':pr['number'],'candidate_sha':state['candidate_sha'],'at':utc_now(),**receipt})
    blob=api.save(state,blob)
    return state,blob


def main() -> int:
    output=Path('/tmp/pd-release-controller');output.mkdir(exist_ok=True)
    event=json.loads(Path(os.environ['GITHUB_EVENT_PATH']).read_text())
    operation, number, sha=command(event)
    api=GitHub();state,blob=api.state();task=f'{number}:{sha}'
    pr=api.request('pulls/'+str(number))
    if pr['head']['repo']['full_name']!=REPO or pr['head']['sha']!=sha or pr['base']['ref']!='main':
        raise ValueError('Wrong source/base or stale candidate SHA')
    previous_run_stopped(api,state)
    if operation=='recover' and state['phase'] in TERMINAL and pr['merged']:
        merge=pr['merge_commit_sha']
        if api.request('git/ref/heads/main')['object']['sha']!=merge:
            raise ValueError('Bootstrap recovery requires the exact current merged PR')
        checks=successful_checks(api,sha)
        parent=api.request('commits/'+merge)['parents'][0]['sha']
        state={'schema':'por-derecho.publication-runtime.v1','fence':state['fence']+1,
               'owner':task,'phase':'CLAIMED','pr':number,'base_sha':parent,'candidate_sha':sha,
               'run_id':int(os.environ['GITHUB_RUN_ID']),'claimed_at':utc_now(),
               'receipts':state.get('receipts',[]),'checkpoints':[],
               'recovery_basis':'Explicit owner recovery of exact completed merge; not a retrospective exclusive-lock claim.'}
        blob=api.save(state,blob)
        state=advance(state,'ACCEPTED',task,state['fence'],{'checks':checks,'bootstrap_recovery':True});blob=api.save(state,blob)
    if operation=='claim':
        if state['phase'] not in TERMINAL:
            if state.get('owner')==task and state['phase']=='ACCEPTED':
                print('Existing exact permit retained; no duplicate claim')
                return 0
            raise ValueError('Publication ownership is occupied; explicit recovery is required')
        if pr['state']!='open' or pr['draft']:
            raise ValueError('Only reviewed nondraft open PRs are eligible')
        base=api.request('git/ref/heads/main')['object']['sha']
        comparison=api.request('compare/'+base+'...'+sha)
        if comparison['merge_base_commit']['sha']!=base or comparison['behind_by']!=0:
            raise ValueError('Candidate does not incorporate current main')
        checks=successful_checks(api,sha)
        state={'schema':'por-derecho.publication-runtime.v1','fence':state['fence']+1,
               'owner':task,'phase':'CLAIMED','pr':number,'base_sha':base,'candidate_sha':sha,
               'run_id':int(os.environ['GITHUB_RUN_ID']),'claimed_at':utc_now(),
               'expiry_policy':'Never silently expire into free; recover after inspecting actual merge/deployment.',
               'receipts':state.get('receipts',[]),'checkpoints':[]}
        blob=api.save(state,blob)
        state=advance(state,'ACCEPTED',task,state['fence'],{'checks':checks});blob=api.save(state,blob)
    else:
        if state.get('owner')!=task:
            raise ValueError('Only the exact held publication may be verified/recovered/aborted')
        if state['phase']=='VERIFIED_FOR_SCOPE' and operation in {'verify','recover'}:
            print('Previously verified exact-scope receipt retained; not a new current-host certification')
        elif operation=='recover' and not pr['merged'] and state['phase'] in {'CLAIMED','ACCEPTED'}:
            base=api.request('git/ref/heads/main')['object']['sha']
            if base!=state['base_sha'] or pr['state']!='open' or pr['draft']:
                raise ValueError('Unmerged recovery requires the same main base and reviewed PR')
            checks=successful_checks(api,sha)
            if state['phase']=='CLAIMED':
                state=advance(state,'ACCEPTED',task,state['fence'],{'checks':checks,'recovered_before_merge':True})
                state['run_id']=int(os.environ['GITHUB_RUN_ID']);blob=api.save(state,blob)
        elif operation=='abort':
            if pr['merged'] or state['phase'] in {'MERGED','DEPLOYED','VERIFIED_FOR_SCOPE'}:
                raise ValueError('Merged publication cannot be aborted as unmerged')
            state=advance(state,'ABORTED_BEFORE_MERGE',task,state['fence'],{'pr_unmerged':True});blob=api.save(state,blob)
        else:
            try:
                state,blob=verify(api,state,blob,pr)
            except Exception:
                current,current_blob=api.state()
                if current.get('owner')==task and current['phase'] in {'MERGE_PENDING','MERGED','DEPLOYED'}:
                    current=advance(current,'RECOVERY_REQUIRED',task,current['fence'],{'failed_run':os.environ['GITHUB_RUN_ID']})
                    api.save(current,current_blob)
                raise
    (output/'result.json').write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'pr':number,'candidate_sha':sha,'phase':state['phase'],'fence':state['fence']}))
    return 0

if __name__=='__main__':
    raise SystemExit(main())
