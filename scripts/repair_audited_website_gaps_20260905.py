#!/usr/bin/env python3
"""Bounded website repairs with unchanged narrative and source-grade checks."""
from __future__ import annotations
import argparse,hashlib,html,json,re,subprocess,sys
from pathlib import Path
from urllib.parse import urlsplit,unquote
ROOT=Path(__file__).resolve().parents[1]
BRANCH='worker/audited-gaps-reconcile-20260905'
BASE='adc8c87585609709caafdd90f03ffbb4a4687d83'
CONTROL='PD-AUDITED-GAPS-20260905-01'
MANIFEST='ops/AUDITED_WEBSITE_REPAIRS_20260905.json'
GRAPH='assets/data/acosta-matos-functional-convergence-map-v2.json'
QUEUE='assets/data/matter-identity-operational-control-v1.json'
TAG=re.compile(r'<(?:[A-Za-z][^<>]*?)>',re.S)
ATTR=re.compile(r'\b(href|src|poster)\s*=\s*([\"\x27])(.*?)\2',re.S|re.I)
MARKER='pd-audit-convergence-documentary-20260905'
GRAPH_PAGES={'en/unitary-criminal-hypothesis-2011-present/acosta-matos-convergence/index.html','es/hipotesis-criminal-unitaria-2011-presente/convergencia-acosta-matos/index.html'}
EXCLUDED=('caixabank','meeting-point-357','meeting-point-espana-357')
NO_REWRITE={'es/cuatrecasas-sun-park/index.html','en/cuatrecasas-sun-park/index.html'}

def sha(s):return hashlib.sha256(s.encode() if isinstance(s,str) else s).hexdigest()
def load(p):return json.loads((ROOT/p).read_text())
def dump(d):return json.dumps(d,ensure_ascii=False,indent=2)+'\n'
def git(*a):return subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()
def save(p,s):
 f=ROOT/p;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(s)
def local(v,lang):
 if isinstance(v,dict):return str(v.get(lang,v.get('en',v.get('es',''))))
 if isinstance(v,list):return '; '.join(local(x,lang) for x in v)
 return str(v) if v is not None else ''
def field(v,name,lang):return local(v.get(name+'_'+lang,v.get(name,'')),lang)
def key(n):return str(n.get('key',n.get('id')))
def target(source,value):
 u=urlsplit(value);path=unquote(u.path)
 if u.scheme or u.netloc:return None
 if path.startswith('/por-derecho/'):p=ROOT/path[len('/por-derecho/'):]
 elif path.startswith('/'):p=ROOT/path[1:]
 else:p=(ROOT/source).parent/path
 p=p.resolve()
 if not p.is_relative_to(ROOT):return None
 if p.is_dir() or path.endswith('/'):p=p/'index.html'
 return p

def unchanged_narrative(text):
 text=re.sub(r'<!-- '+MARKER+r':BEGIN -->.*?<!-- '+MARKER+r':END -->','',text,flags=re.S)
 text=TAG.sub(lambda m:ATTR.sub(lambda a:a.group(1)+'="ATTRIBUTE"',m.group(0)),text)
 return re.sub(r'neutralisation-continuity-\d+','neutralisation',text)

def repair_attributes(path,text):
 edits=[]
 def tag_replace(m):
  def attr_replace(a):
   name,q,raw=a.groups();value=html.unescape(raw);new=value
   u=urlsplit(value)
   if u.scheme or u.netloc:return a.group(0)
   resolved=target(path,value)
   if resolved and resolved.is_relative_to(ROOT/'.github') and resolved.is_file():
    new='https://github.com/sbu001monterecco/por-derecho/blob/main/'+resolved.relative_to(ROOT).as_posix()
    if u.fragment:new+='#'+u.fragment
   elif value.startswith('/') and not value.startswith(('/por-derecho/','//')) and resolved and resolved.is_file():
    new='/por-derecho'+value
   if new==value:return a.group(0)
   old=a.group(0);encoded=html.escape(new,quote=True)
   replacement=old[:a.start(3)-a.start()]+encoded+old[a.end(3)-a.start():]
   edits.append({'old':old,'new':replacement,'target':str(resolved.relative_to(ROOT)),'kind':'GITHUB_SOURCE_DESTINATION' if '/blob/main/.github/' in new else 'PROJECT_BASE_PREFIX'})
   return replacement
  return ATTR.sub(attr_replace,m.group(0))
 return TAG.sub(tag_replace,text),edits

def graph_data():
 d=load(GRAPH);base=Path(GRAPH).parent
 def rows(kind):
  if isinstance(d.get(kind),list):return d[kind]
  out=[]
  for p in d.get(('node' if kind=='nodes' else 'edge')+'_parts',[]):
   x=load(str(base/p['path']));part=x.get(kind,x.get('records',[]))
   assert len(part)==p.get('count',len(part));out.extend(part)
  return out
 n,e=rows('nodes'),rows('edges');assert n and e
 ids={key(x) for x in n};assert len(ids)==len(n)
 assert all(str(x.get('from') or x.get('source')) in ids and str(x.get('to') or x.get('target')) in ids for x in e)
 return d,n,e

def documentary(lang):
 d,nodes,edges=graph_data();names={key(n):field(n,'label',lang) or key(n) for n in nodes}
 t=lambda es,en:es if lang=='es' else en
 parts=[f'<!-- {MARKER}:BEGIN -->',f'<section id="{MARKER}" class="pd-audit-graph-documentary">',f'<h2>{t("Edición documental de las relaciones","Documentary relationship edition")}</h2>']
 parts.append('<p>'+t('Esta edición reproduce las relaciones y límites del registro existente. La dirección de una flecha no acredita causalidad, conocimiento o culpabilidad. Los filtros de la visualización no ocultan esta edición completa.','This edition reproduces the existing registry relationships and limits. Arrow direction does not establish causation, knowledge or guilt. Visualization filters do not hide this complete edition.')+'</p>')
 source_map={x['id']:x for x in d.get('sources',[]) if isinstance(x,dict) and 'id' in x}
 for e in edges:
  fromid=str(e.get('from') or e.get('source'))
  toid=str(e.get('to') or e.get('target'))
  eid=str(e.get('id',''))
  parts.append('<details data-audit-edge="'+html.escape(eid,quote=True)+'"><summary>'+html.escape(names[fromid]+' → '+names[toid])+'</summary>')
  caption=' · '.join([eid,str(e.get('grade') or e.get('type') or ''),str(e.get('period') or e.get('date') or '')])
  parts.append('<p>'+html.escape(caption)+'</p>')
  for f in ['proposition','label','investigative_significance','limit','limitation','contrary','open_proof']:
   text=field(e,f,lang)
   if text:parts.append('<p>'+html.escape(text)+'</p>')
  for raw in e.get('sources',e.get('source_ids',[])):
   s=source_map.get(raw,{'path':raw}) if isinstance(raw,str) else raw
   value=s.get('url') or s.get('path') or s.get('route') or ''
   title=field(s,'title',lang) or s.get('id') or str(raw)
   href=None
   if isinstance(value,str) and value:
    if value.startswith(('https://','http://')):href=value
    else:
     p=ROOT/value.lstrip('/').removeprefix('por-derecho/')
     if p.is_file():
      rel=p.relative_to(ROOT).as_posix()
      href=('https://github.com/sbu001monterecco/por-derecho/blob/main/' if rel.startswith('.github/') else '/por-derecho/')+rel
   if href:parts.append('<p><a href="'+html.escape(href,quote=True)+'">'+html.escape(str(title))+'</a></p>')
   else:parts.append('<p><code>'+html.escape(str(title))+'</code></p>')
  parts.append('</details>')
 parts.extend([f'<p><a href="/por-derecho/{GRAPH}">{t("Registro canónico de la visualización","Canonical visualization registry")}</a></p>','</section>',f'<!-- {MARKER}:END -->'])
 return '\n'.join(parts)

def prepare():
 assert git('branch','--show-current')==BRANCH
 assert git('rev-parse','origin/main')==BASE,'Main advanced: reconcile before generating'
 assert not (ROOT/MANIFEST).exists(),'Already prepared'
 modified=[];deferred=[];counts={'PROJECT_BASE_PREFIX':0,'GITHUB_SOURCE_DESTINATION':0,'DUPLICATE_ANCHOR':0}
 for path in git('ls-files','*.html').splitlines():
  if not path.startswith(('es/','en/','de/')):continue
  text=(ROOT/path).read_text();base=text
  if path in NO_REWRITE or any(x in path for x in EXCLUDED):
   _,changes=repair_attributes(path,text)
   if changes:deferred.append({'path':path,'reason':'SCOPED_REGRESSION_OR_ACTIVE_PARALLEL_OWNER','attribute_candidates':len(changes)})
   continue
  text,edits=repair_attributes(path,text)
  matches=list(re.finditer(r'\bid\s*=\s*([\"\x27])neutralisation\1',text))
  for index,m in reversed(list(enumerate(matches[1:],2))):
   replacement=m.group(0).replace('neutralisation','neutralisation-continuity-'+str(index))
   text=text[:m.start()]+replacement+text[m.end():]
   edits.append({'old':m.group(0),'new':replacement,'kind':'DUPLICATE_ANCHOR','target':path})
  for item in edits:counts[item['kind']]+=1
  if path in GRAPH_PAGES:
   assert MARKER not in text and text.count('</main>')==1,'Unexpected canonical graph-page structure: '+path
   text=text.replace('</main>',documentary(path.split('/')[0])+'</main>')
   edits.append({'kind':'DOCUMENTARY_FALLBACK','source':GRAPH})
  if text!=base:
   assert unchanged_narrative(text)==unchanged_narrative(base),'Narrative changed: '+path
   save(path,text);modified.append({'path':path,'before_sha256':sha(base),'after_sha256':sha(text),'narrative_sha256':sha(unchanged_narrative(base)),'edits':edits})
 alias='assets/site.css';assert not (ROOT/alias).exists()
 save(alias,'/* Compatibility for historic public routes. Canonical stylesheet remains unchanged. */\n@import url("./styles.css");\n')
 extra=[alias]
 queue=load(QUEUE);before=sha((ROOT/QUEUE).read_text());manifest=load('assets/data/matter-identity-registry-v1.json');identities={}
 for p in manifest['parts']:
  for r in load('assets/data/'+p['path'])['records']:identities[r['id']]=r
 added=[]
 for ident in ['PD-SP-P-0138','PD-SP-P-0139','PD-SP-P-0143']:
  assert ident in identities
  if any(row.get('id')==ident for row in queue['exact_identity_queue']):continue
  row=identities[ident]
  assert any(x in json.dumps(row) for x in ['PENDING','UNRESOLVED']),'Only unresolved identities may enter this queue'
  queue['exact_identity_queue'].append({'id':ident,'priority':'P1','question_es':'Resolver la identidad exacta desde la fuente primaria y conservar las variantes/limitaciones existentes; no atribuir capacidad, conocimiento o responsabilidad por el nombre.','question_en':'Resolve the exact identity from the primary source while preserving existing variants and limitations; infer no role, knowledge or liability from the name.','review_control':CONTROL,'source_registry':'assets/data/matter-identity-registry-v1.json','closure_test':'An authoritative primary source matches the immutable identity and dated source literal; update the same record and every affected projection. No automatic caret.'});added.append(ident)
 save(QUEUE,dump(queue));extra.append(QUEUE)
 sys.path.insert(0,str(ROOT/'scripts'));import build_community_acta_authority_interconnectivity as graph
 p=ROOT/'assets/data/community-acta-authority-interconnectivity-v1.json';old=json.loads(p.read_text());new=graph.build()
 assert all(old.get(k)==new.get(k) for k in set(old)|set(new) if k!='sources'),'Substantive graph drift'
 p.write_text(dump(new));extra.append(p.relative_to(ROOT).as_posix())
 dispositions={'G01_CR_CONTINUITY':'RECONCILED_REQUIRES_INTEGRATION_AND_LIVE_READBACK','G02_MISSING_ASSETS':'REPAIRED_SOURCE_REQUIRES_BROWSER_AND_LIVE','G03_PROJECT_BASE':'VERIFIED_LOCAL_TARGETS_REPAIRED_PARALLEL_PATHS_EXPLICIT','G04_ANCHORS':'DUPLICATE_FIXED_DYNAMIC_ABSENCE_CANDIDATES_NOT_DECLARED_BROKEN','G05_RAUDA_URIA_COLLISION':'MAIN_RAUDA_ID_PRESERVED_URIA_DRAFT_HOLD_FOR_REMAP','G06_IDENTITY_TASKS':'THREE_PENDING_IDENTITIES_FEDERATED_NO_CARET_UPGRADE','G07_22_AGGREGATE_COMMUNICATIONS':'PRIMARY_RECEIPTS_REQUIRED_NO_SYNTHETIC_EVENTS','G08_UCF_AND_CR_PROOF':'SOURCE_REQUIRED_TRACKING_NOT_MERITS_CLOSURE','G09_CI_LEGACY':'ACTIVE_CONTROLLER_REPAIR_OWNS_OVERLAP','G10_OLD_PRS':'CANONICAL_DELTA_REVIEW_REQUIRED_NO_BLIND_MERGE','G11_MEDIA_LINKS':'SOURCE_WORKER_1462_AND_MEDIA_DESK_SEQUENCED_SEPARATELY_NO_SEND','G12_ADMIN_RULESET':'ADMINISTRATION_AUTHORITY_AND_READBACK_REQUIRED','G13_PRIVACY':'ACTIVE_CAIXABANK_PRIVACY_WORKER_NOT_OVERRIDDEN','G14_PLATFORM_CONTINUITY':'INSTALLATION_AND_PRIVATE_CUSTODY_TESTS_NOT_ASSUMED','G15_DEPLOYMENT':'EXACT_MERGE_PAGES_AND_RESOURCE_READBACK_REQUIRED'}
 record={'schema':'por-derecho.audited-website-repairs.v1','control_id':CONTROL,'source_base':BASE,'state':'PREPARED_NOT_MERGED_OR_LIVE','attribute_changes':counts,'modified_html':modified,'additional_generated_paths':extra,'deferred_parallel_or_regression_paths':deferred,'identity_tasks_added':added,'prior_identity_queue_sha256':before,'graph_source':GRAPH,'graph_counts':{'nodes':len(graph_data()[1]),'edges':len(graph_data()[2])},'evidential_boundary':'Rendering and registration repairs do not prove pending facts, identity, institutional action, fraud or liability. Existing source grades and limits remain controlling.','open_dispositions':dispositions}
 save(MANIFEST,dump(record));check();print('WEBSITE_GENERATED',dump([r['path'] for r in modified]+extra+[MANIFEST]))

def check():
 d=load(MANIFEST);checks=0
 for r in d['modified_html']:
  text=(ROOT/r['path']).read_text();assert sha(text)==r['after_sha256'],r['path'];checks+=1
  assert sha(unchanged_narrative(text))==r['narrative_sha256'];checks+=1
  for change in r['edits']:
   if change['kind'] in ['PROJECT_BASE_PREFIX','GITHUB_SOURCE_DESTINATION']:
    assert change['new'] in text and (ROOT/change['target']).is_file();checks+=1
  if MARKER in text:
   assert text.count('data-audit-edge=')==d['graph_counts']['edges'];assert 'convergence-graph.js' in text;checks+=1
 q=load(QUEUE)
 for ident in ['PD-SP-P-0138','PD-SP-P-0139','PD-SP-P-0143']:assert sum(x.get('id')==ident for x in q['exact_identity_queue'])==1;checks+=1
 for p in ['assets/convergence-graph.js','assets/convergence-graph.css','assets/site.css']:assert (ROOT/p).is_file();checks+=1
 subprocess.run(['node','--check','assets/convergence-graph.js'],check=True,cwd=ROOT)
 print(dump({'result':'WEBSITE_SOURCE_PASS','checks':checks,'changed_html':len(d['modified_html']),'attribute_changes':d['attribute_changes'],'deferred_paths':len(d['deferred_parallel_or_regression_paths']),'graph_counts':d['graph_counts']}))

if __name__=='__main__':
 p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True);g.add_argument('--prepare',action='store_true');g.add_argument('--check',action='store_true');a=p.parse_args()
 prepare() if a.prepare else check()
