#!/usr/bin/env python3
"""Read-only finite JSP QA. No writes to tracked files and no publication authority."""
from __future__ import annotations
import argparse,collections,json,re,subprocess,unicodedata,zipfile
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote,urlparse
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'assets/data'
MANIFEST='assets/data/matter-identity-registry-v1.json'
ROUTES=['es/jsp-montelanza-concurso-liquidacion/index.html','en/jsp-montelanza-insolvency-liquidation/index.html']
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def norm(s):return re.sub(r'[^a-z0-9]','',unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower())
class Page(HTMLParser):
 def __init__(self,text):super().__init__();self.ids=[];self.links=[];self.lang='';self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if a.get('id'):self.ids.append(a['id'])
  if tag=='html':self.lang=a.get('lang','')
  for k in ('href','src'):
   if a.get(k):self.links.append(a[k])
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--base',required=True);ap.add_argument('--output',default='jsp-qa');args=ap.parse_args();out=ROOT/args.output;out.mkdir(exist_ok=True)
 report={'control_id':'PD-JSP-CANONICAL-20260905','base':args.base,'checks':[],'failures':[],'limitations':['Finite source-qualified registration; no full original-file completion','No current court-file or final-extinction certification','No merge, deployment or live verification certified','Full docket and proceeding master-row reconciliation remain open']}
 def check(label,condition,details=None):
  report['checks'].append(label)
  if not condition:report['failures'].append({'check':label,'details':details})
 def at_base(path):return json.loads(subprocess.check_output(['git','show',f'{args.base}:{path}'],cwd=ROOT,text=True))
 before=at_base(MANIFEST);manifest=load(ROOT/MANIFEST)
 for k,v in before.items():
  if k not in ('parts','counts','control_date'):check('preserve manifest '+k,manifest.get(k)==v)
 check('dated admission control',manifest['control_date']=='2026-09-05')
 old_paths={p['path']:p for p in before['parts']};records=[];new_records=[];part_paths=[]
 check('all old parts retained',set(old_paths).issubset({p['path'] for p in manifest['parts']}))
 for part in manifest['parts']:
  path=DATA/part['path'];obj=load(path);rows=obj['records'];part_paths.append(path);records.extend(rows)
  check('count '+part['path'],len(rows)==part['count']);check('type '+part['path'],all(r['type']==part['type'] for r in rows))
  if part['path'] in old_paths:
   check('old part metadata '+part['path'],part==old_paths[part['path']]);check('old part values '+part['path'],obj==at_base('assets/data/'+part['path']))
  else:new_records.extend(rows)
 ids=[r['id'] for r in records];by_id={r['id']:r for r in records};new_ids={r['id'] for r in new_records}
 check('global unique IDs',len(ids)==len(set(ids)));check('ID syntax',all(re.fullmatch(r'PD-SP-[POSIR]-\d{4}',i) for i in ids))
 counts=dict(collections.Counter(r['type'] for r in records));counts['total']=len(records);check('global counts',counts==manifest['counts'],counts)
 old_names=collections.defaultdict(set)
 for r in records:
  if r['id'] not in new_ids:
   for name in [r['name'],*r.get('aliases',[])]:old_names[(r['type'],norm(name))].add(r['id'])
 for r in new_records:
  check('source '+r['id'],bool(r.get('identity_sources')));check('no old-name duplicate '+r['id'],not old_names.get((r['type'],norm(r['name']))))
  check('explicit role boundary '+r['id'],bool(r.get('capacity_boundary')))
 supplement=load(DATA/'jsp-canonical-supplement-20260905.json');evidence=load(DATA/'jsp-2017-source-relationship-register.json')
 check('new denominator',len(new_records)==59==supplement['expected_new_records']);check('new typed counts',dict(collections.Counter(r['type'] for r in new_records))=={'PERSON':30,'ORGANISATION':21,'STRUCTURE':7,'PROCEEDING':1})
 check('reuse denominator',len(supplement['reused_records'])==19==supplement['expected_reused_records'])
 for r in supplement['reused_records']:
  check('actual existing reuse '+r['id'],r['id'] not in new_ids and r['id'] in by_id and norm(by_id[r['id']]['name'])==norm(r['name']))
 for retired,canonical in supplement['retired_candidate_ids'].items():check('retired duplicate '+retired,retired not in by_id and canonical in by_id and canonical not in new_ids)
 sources={s['id'] for s in evidence['sources']}
 for e in evidence['edges']:
  check('edge endpoints '+e['id'],e['from'] in by_id and e['to'] in by_id);check('edge source '+e['id'],e['source'] in sources)
 check('dated minority correction',any(e['relation']=='DIRECT_EQUITY_RECORDED_26_82_PERCENT' for e in evidence['edges']))
 check('Community CAM unproved',all(e['status']=='UNPROVED_RESEARCH_QUESTION' for e in evidence['edges'] if e['from']=='PD-SP-O-0005' and e['to']=='PD-SP-O-0007'))
 check('8499 conditional',any(e['relation']=='FINCA_8499_CONDITIONAL_ALLOCATION' and e['status']=='CONDITIONAL_FULFILMENT_UNPROVED' for e in evidence['edges']))
 check('no false meeting-held event',all('HELD' not in e['kind'] or 'NOT_PROVED_HELD' in e['kind'] for e in evidence['events']))
 pages={}
 for route in ROUTES:
  path=ROOT/route;text=path.read_text(encoding='utf-8');page=Page(text);pages[route]=page
  check('unique anchors '+route,len(page.ids)==len(set(page.ids)));check('language '+route,page.lang==route[:2]);check('source control visible '+route,'PD-JSP-2017-DOSSIER-20260905' in text)
  check('minority visible '+route,'26.82%' in text or '26,82%' in text);check('official original '+route,'BORME-C-2017-7368.pdf' in text);check('finca corrections '+route,all(x in text for x in ['8498','8499','8500','2026']))
  check('private-data boundary '+route,not re.search(r'@monterecco|gmail\.com|sk-proj-|mailbox_id|message_id',text,re.I))
  for href in page.links:
   u=urlparse(href)
   if u.scheme or u.netloc:continue
   target=(path.parent/unquote(u.path)).resolve() if u.path else path
   if target.is_dir():target/='index.html'
   check('local target '+route+' '+href,target.exists())
   if not u.path and u.fragment:check('local anchor '+route+' '+href,u.fragment in page.ids or u.fragment in sources or u.fragment in new_ids)
 check('bilingual anchor parity',set(pages[ROUTES[0]].ids)==set(pages[ROUTES[1]].ids))
 changed=subprocess.check_output(['git','diff','--name-status',args.base,'HEAD'],cwd=ROOT,text=True).splitlines()
 allowed_existing={MANIFEST,'en/matter-identity-registry/index.html','es/registro-identidad-materia/index.html','ops/CURRENT_UNITARY_STATE.json','assets/data/matter-identity-operational-control-v1.json','assets/data/matter-identity-control-matrix-v1.json'}
 for row in changed:
  st,path=row.split('\t',1);check('no deletion or rename '+path,st in ('A','M'));check('bounded existing modification '+path,st!='M' or path in allowed_existing)
 subprocess.run(['node','--check',str(ROOT/'assets/jsp-dossier-2017.js')],check=True)
 check('supplement source control exists',(ROOT/supplement['source_control']).is_file())
 report.update(actual_counts=counts,new_records=len(new_records),new_identity_confirmed=sum(r.get('identity_resolution')=='CARET_CONFIRMED' for r in new_records));report['result']='FAIL' if report['failures'] else 'PASS_SCOPED_ONLY'
 (out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 files={ROOT/row.split('\t',1)[1] for row in changed if row.split('\t',1)[0] in ('A','M')};files.update(part_paths)
 with zipfile.ZipFile(out/'review-source.zip','w',zipfile.ZIP_DEFLATED) as z:
  for path in sorted(files):
   if path.is_file():z.write(path,path.relative_to(ROOT))
  z.write(out/'report.json','jsp-qa/report.json')
 print(json.dumps({'result':report['result'],'checks':len(report['checks']),'failures':report['failures'],'counts':counts},ensure_ascii=False,indent=2));return int(bool(report['failures']))
if __name__=='__main__':raise SystemExit(main())
