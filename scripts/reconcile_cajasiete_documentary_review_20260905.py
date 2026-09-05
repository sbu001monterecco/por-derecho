#!/usr/bin/env python3
"""Current-main reconstruction of existing CajaSiete worker; no main publication.
Use the generator's source-verified canonical hook and CLI, not a second adapter.
Fail on collisions, any changed prior event, unexpected paths or concurrent refs.
"""
from __future__ import annotations
import hashlib,json,os,shutil,subprocess,sys
from pathlib import Path
BRANCH='worker/cajasiete-board-visuals-20260905'
GEN='scripts/prepare_cajasiete_board_visuals_20260905.py'
CHECK='scripts/check_cajasiete_board_browser_20260905.py'
SELF='scripts/reconcile_cajasiete_documentary_review_20260905.py'
WF='.github/workflows/cajasiete-board-visuals-20260905.yml'
CROSS='ops/CAJASIETE_BOARD_VISUAL_CROSSWALK_20260905.json'
INPUT='ops/cajasiete-board-source-input-20260905.json'
REG='assets/data/institutional-communications-register-v1.json'
BUILD='scripts/reconcile_institutional_communications.py'
REPORT='ops/CAJASIETE_REVIEW_RECONCILIATION_20260905.json'
OVERRIDE={
'es':{'intro':'La gestión del canal se examina por sus propios documentos. La consulta comercial genuina es independiente y debe valorarse por sus propios méritos; su resultado no determina la evaluación del canal.', 'timeline':[('10 DIC 2025','Independencia declarada','El banco describió independencia y medidas de inhibición o reasignación ante potenciales conflictos.'),('9 ABR 2026','Comunicación recibida','El acuse acredita recepción, no admisión, contenido completo ni examen sustantivo.'),('28 ABR 2026','Inadmisión comunicada','El canal declaró un examen preliminar y anunció destruir la información conforme a la normativa aplicable.')], 'oriontitle':'ORION: RAMA DISTINTA, INTERCONECTADA', 'review':'<h3>Alcance documental y respuesta</h3><p>La independencia declarada no es una promesa de admisión. La decisión afirma que hubo un examen preliminar: se pregunta qué se examinó y qué sustentó cada motivo, no se afirma ausencia absoluta de examen.</p><p><strong>Extracto literal:</strong> «Se procederá a destruir la información en cumplimiento de la normativa aplicable». <a href="/por-derecho/es/registros-institucionales/#source-PD-SP-SRC-0015">Fuente PD-SP-SRC-0015</a>. Destrucción anunciada, no acreditada. Legalidad y alcance pendientes de verificación. Las figuras son síntesis editoriales de Por Derecho, no documentos oficiales reproducidos.</p><p>Distinguir escritura, inscripción y fecha de expedición; titular registral, hipotecante y prestatario; responsabilidad hipotecaria, desembolso y tasación. Una nota informativa parcial no es una certificación completa. La reconstrucción agregada del proyecto no equivale a un préstamo de CajaSiete.</p><p>Orion es una rama distinta pero interconectada: se conservan las relaciones documentadas y sus fechas, sin convertir una participación histórica en actual ni presumir un flujo de activos o ingresos desde Sun Park.</p><p>Se invita a una respuesta motivada, prueba contraria y corrección documentada. El silencio no equivale a admisión. Preservación, traslado, anonimización y supresión deben ser lícitos y de acceso restringido.</p>'},
'en':{'intro':'Channel handling is examined on its own documents. The genuine commercial enquiry is independent and must be assessed on its own merits; its outcome does not determine the assessment of channel handling.', 'timeline':[('10 DEC 2025','Independence stated','The bank described independence and recusal or reassignment safeguards for potential conflicts.'),('9 APR 2026','Communication received','The acknowledgement establishes receipt, not admission, complete contents or substantive review.'),('28 APR 2026','Inadmission communicated','The channel stated a preliminary examination and announced destruction under the applicable rules.')], 'oriontitle':'ORION: DISTINCT, INTERCONNECTED BRANCH', 'review':'<h3>Documentary scope and response</h3><p>Stated independence is not a promise of admission. The decision states a preliminary examination: the question is what was examined and what supported each ground, not an assertion that no examination occurred.</p><p><strong>Original Spanish extract:</strong> «Se procederá a destruir la información en cumplimiento de la normativa aplicable». <a href="/por-derecho/en/institutional-records/#source-PD-SP-SRC-0015">Source PD-SP-SRC-0015</a>. Translation: the information will be destroyed in accordance with the applicable rules. Destruction announced, not established. Lawfulness and scope remain to be verified. The figures are Por Derecho editorial summaries, not reproduced official documents.</p><p>Distinguish deed, registration and issue dates; registered owner, mortgagor and borrower; mortgage liability, advances and valuation. A partial informational note is not a complete certificate. Aggregate project reconstruction does not establish a CajaSiete loan amount.</p><p>Orion is a distinct but interconnected branch: dated documentary relationships are preserved, without treating historical ownership as current or assuming an asset or income flow from Sun Park.</p><p>A reasoned response, contrary evidence and documented correction are invited. Silence is not admission. Preservation, transfer, anonymisation and deletion must be lawful and access-restricted.</p>'}}
def git(*a,cwd=None):return subprocess.check_output(['git',*a],cwd=cwd,text=True).strip()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
def main():
 root=Path(git('rev-parse','--show-toplevel'));seed=os.environ['GITHUB_SHA'];assert os.environ['GITHUB_REF_NAME']==BRANCH and git('rev-parse','HEAD')==seed
 subprocess.run(['git','fetch','--quiet','origin','main'],cwd=root,check=True);base=git('rev-parse','origin/main',cwd=root)
 assert git('ls-remote','origin','refs/heads/'+BRANCH,cwd=root).split()[0]==seed
 work=Path(os.environ['RUNNER_TEMP'])/('cajasiete-review-'+seed[:12]);assert not work.exists()
 subprocess.run(['git','worktree','add','--detach',str(work),base],cwd=root,check=True)
 out=root/'qa-cajasiete-review';out.mkdir(exist_ok=True);save(out/'attempt.json',{'seed':seed,'base':base,'status':'PREPARING_NOT_PUBLISHED'})
 try:
  cross=json.loads((root/CROSS).read_text());before=json.loads((work/REG).read_text());ids={v['event_id'] for v in cross['events'].values()}
  assert not ids & {e['event_id'] for e in before['events']},'Event collision or already integrated'
  media=json.loads((work/'data/digital-media-asset-register-v1.json').read_text());assert not set(cross['assets'].values()) & {a['reference'] for a in media['logical_assets']},'Media collision'
  for rel in [GEN,CHECK,SELF,WF,INPUT,CROSS]:
   dst=work/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(root/rel,dst)
  cross.setdefault('baseline_reconciliation_history',[]).append({'prior_page_hashes':cross['baseline_pages'].copy(),'source_worker':seed,'new_main':base,'reason':'Preserve current-main bytes outside owned CajaSiete blocks.'})
  for rel in cross['baseline_pages']:
   assert b'<!-- CAJASIETE-BOARD-VISUALS-20260905:START -->' not in (work/rel).read_bytes();cross['baseline_pages'][rel]=sha(work/rel)
  cross['review_base_sha']=base;save(work/CROSS,cross)
  g=work/GEN;t=g.read_text();marker='def vector(lang,n,logical,x):';assert t.count(marker)==1
  patch='\n# Documentary review: summaries, not official facsimiles.\nfor _lang, _values in '+repr(OVERRIDE)+'.items():\n COPY[_lang].update(_values)\n\n'
  assert '# Documentary review: summaries, not official facsimiles.' not in t
  t=t.replace(marker,patch+marker,1)
  source='<h3>{c["sources"]}</h3><p>{source_links(lang,x)}</p>';assert t.count(source)==1;t=t.replace(source,source+'{c["review"]}',1)
  # The verified existing generator inserts its own KEY_EVENTS hook and uses --apply.
  assert "subprocess.run([sys.executable,str(p),'--apply']" in t
  b=(work/BUILD).read_text();assert b.count('def _existing_receipt_ids(register:')==1 and '"--apply"' in b
  compile(t,str(g),'exec');g.write_text(t)
  cmds=[[sys.executable,GEN,'apply'],[sys.executable,BUILD,'--check'],[sys.executable,'scripts/validate_institutional_communications.py'],[sys.executable,GEN,'check'],[sys.executable,CHECK]]
  for i,cmd in enumerate(cmds,1):
   r=subprocess.run(cmd,cwd=work,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(out/f'check-{i}.txt').write_text(r.stdout);print(r.stdout,flush=True);assert r.returncode==0,f'Check {i} failed; no push'
  after=json.loads((work/REG).read_text());byid={e['event_id']:e for e in after['events']};assert all(byid.get(e['event_id'])==e for e in before['events'])
  browser=json.loads((work/'ops/CAJASIETE_BOARD_BROWSER_20260905.json').read_text());assert browser['status']=='PASS' and browser['passed']==browser['case_count']==24
  acceptance=json.loads((work/'ops/CAJASIETE_BOARD_VISUAL_ACCEPTANCE_20260905.json').read_text());allowed=set(acceptance['paths'])|{GEN,CHECK,SELF,WF,INPUT,CROSS,REPORT,'ops/CAJASIETE_BOARD_BROWSER_20260905.json','ops/CAJASIETE_BOARD_VISUAL_ACCEPTANCE_20260905.json'}
  status=subprocess.check_output(['git','status','--porcelain','--untracked-files=all'],cwd=work,text=True);changed=[s[3:] for s in status.splitlines() if not s[3:].startswith(('qa-cajasiete/','scripts/__pycache__/','__pycache__/'))]
  assert set(changed)<=allowed,('Unexpected paths',sorted(set(changed)-allowed));assert not any(s[:2].strip()=='D' for s in status.splitlines())
  record={'control_id':'PD-CAJASIETE-BOARD-VISUALS-20260905','status':'CURRENT_MAIN_RECONCILED_STATIC_AND_24_BROWSER_PASS_NOT_DEPLOYED','source_worker_sha':seed,'base_sha':base,'preserved_canonical_events':len(before['events']),'candidate_event_count':len(after['events']),'native_private_sources_published':False,'source_crops_published':False,'source_crop_status':'WITHHELD_PENDING_CANONICAL_IDENTITY_AND_PUBLICATION_REVIEW','main_not_modified':True,'changed_paths':sorted(set(changed)|{REPORT}),'open_gaps':acceptance.get('open_proof',[]),'writer_retirement_required':True,'remaining_acceptance':['Retire writer','Exact-head acceptance','Active integrator permit','Merge and exact Pages/live verification']};save(work/REPORT,record)
  subprocess.run(['git','add','--',*sorted(allowed)],cwd=work,check=True);tree=git('write-tree',cwd=work)
  commit=subprocess.check_output(['git','commit-tree',tree,'-p',seed,'-p',base,'-m','Reconcile CajaSiete reader on current main; preserve source records and pass 24 browser cases'],cwd=work,text=True).strip()
  record.update(candidate_sha=commit,prepared_tree=tree);save(out/'preparation-receipt.json',record)
  for rel in sorted(allowed):
   if (work/rel).is_file():dst=out/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(work/rel,dst)
  assert git('ls-remote','origin','refs/heads/'+BRANCH,cwd=root).split()[0]==seed,'Concurrent worker moved; artifact only'
  assert git('ls-remote','origin','refs/heads/main',cwd=root).split()[0]==base,'Main moved; artifact only'
  subprocess.run(['git','push','origin',commit+':refs/heads/'+BRANCH],cwd=root,check=True);print(json.dumps({'status':'WORKER_UPDATED_NOT_PUBLISHED','candidate':commit,'base':base,'tree':tree}))
 finally:
  for rel in [GEN,BUILD]:
   if (work/rel).exists():dst=out/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(work/rel,dst)
  if (work/'qa-cajasiete').exists():shutil.copytree(work/'qa-cajasiete',out/'screenshots',dirs_exist_ok=True)
if __name__=='__main__':main()
