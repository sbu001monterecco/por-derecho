#!/usr/bin/env python3
"""Reconcile the existing CajaSiete worker on current main, never publish main.
Stops on identity collisions, changed source, failed tests or concurrent ref moves.
"""
from __future__ import annotations
import ast
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

BRANCH='worker/cajasiete-board-visuals-20260905'
GENERATOR='scripts/prepare_cajasiete_board_visuals_20260905.py'
CHECKER='scripts/check_cajasiete_board_browser_20260905.py'
SELF='scripts/reconcile_cajasiete_documentary_review_20260905.py'
WORKFLOW='.github/workflows/cajasiete-board-visuals-20260905.yml'
CROSS='ops/CAJASIETE_BOARD_VISUAL_CROSSWALK_20260905.json'
INPUT='ops/cajasiete-board-source-input-20260905.json'
REG='assets/data/institutional-communications-register-v1.json'
BUILDER='scripts/reconcile_institutional_communications.py'
REPORT='ops/CAJASIETE_REVIEW_RECONCILIATION_20260905.json'
CONTROL='PD-CAJASIETE-BOARD-VISUALS-20260905'
OVERRIDE={
'es':{
'intro':'La gestión del canal de información se examina por sus propios documentos. La consulta comercial genuina es independiente y debe valorarse por sus propios méritos; su resultado no determina la evaluación del canal.',
 'timeline':[['10 DIC 2025','Independencia declarada','Se anunciaron medidas de inhibición y reasignación ante posibles conflictos para garantizar una evaluación objetiva.'],['9 ABR 2026','Comunicación recibida','El canal confirmó la recepción. El acuse no acredita admisión, contenido completo ni examen sustantivo.'],['28 ABR 2026','Inadmisión comunicada','El canal declaró un examen preliminar y anunció destruir la información conforme a la normativa aplicable.']],
'oriontitle':'ORION: RAMA DISTINTA, INTERCONECTADA',
'orion':'Cajasiete ↔ Orion ↔ Grupo Patrimonial Acosta Matos. Relación societaria fechada: no acredita una transmisión de Sun Park a Orion ni coordinación ilícita.',
'review':'<h3>Qué acredita cada documento</h3><p>La respuesta de independencia describe una garantía de procedimiento, no una promesa de admisión. El acuse acredita recepción. La decisión declara un examen preliminar: la pregunta es qué se examinó y qué sustentó cada motivo, no afirmar que no hubo examen alguno. Cada hito remite a su propio evento y fuente en esta sección.</p><p><strong>Extracto literal de la decisión de inadmisión:</strong> «Se procederá a destruir la información en cumplimiento de la normativa aplicable». <a href="/por-derecho/es/registros-institucionales/#source-PD-SP-SRC-0015">PD-SP-SRC-0015</a>. No acredita destrucción efectiva ni su ilicitud. Las figuras son síntesis editoriales de Por Derecho, no reproducciones de documentos oficiales.</p><p><strong>Título y financiación:</strong> deben distinguirse la fecha de la escritura, la inscripción y la expedición de la nota; titular registral, hipotecante y prestatario; responsabilidad hipotecaria, desembolso y valoración. Los extractos informativos parciales no son certificaciones completas. No se atribuye la reconstrucción agregada del proyecto a un préstamo de CajaSiete.</p><p><strong>Rama Orion:</strong> se conservan las conexiones societarias documentadas, sus fechas y las identidades de las distintas sociedades. Una participación histórica no se presenta como participación actual. Cualquier flujo concreto de activos, ingresos o garantías desde Sun Park requiere prueba propia.</p><p><strong>Respuesta y corrección:</strong> se invita a aportar explicación, prueba contraria y corrección documentada. El silencio no equivale a admisión. La preservación, transferencia, anonimización y supresión se examinan conforme a las reglas aplicables y con acceso restringido, no mediante publicación de datos protegidos.</p>'},
'en':{
'intro':'Reporting-channel handling is examined on its own documents. The genuine commercial enquiry is independent and must be assessed on its own merits; its outcome does not determine the assessment of channel handling.',
 'timeline':[['10 DEC 2025','Independence stated','Recusal and reassignment measures for potential conflicts were described to secure an objective assessment.'],['9 APR 2026','Communication received','The channel confirmed receipt. The acknowledgement does not establish admission, complete contents or substantive review.'],['28 APR 2026','Inadmission communicated','The channel stated a preliminary examination and announced destruction under the applicable rules.']],
'oriontitle':'ORION: DISTINCT, INTERCONNECTED BRANCH',
'orion':'Cajasiete ↔ Orion ↔ Grupo Patrimonial Acosta Matos. A dated corporate relationship, not proof of a Sun Park transfer to Orion or unlawful coordination.',
'review':'<h3>What each document establishes</h3><p>The independence response describes a procedural safeguard, not a promise of admission. The acknowledgement establishes receipt. The decision states a preliminary examination: the question is what was examined and what supported each ground, not an assertion that no examination occurred. Each stage resolves to its own event and source in this section.</p><p><strong>Original Spanish extract from the inadmission decision:</strong> «Se procederá a destruir la información en cumplimiento de la normativa aplicable». <a href="/por-derecho/en/institutional-records/#source-PD-SP-SRC-0015">PD-SP-SRC-0015</a>. Translation: the information will be destroyed in accordance with the applicable rules. This does not establish actual or unlawful destruction. The figures are Por Derecho editorial summaries, not reproductions of official documents.</p><p><strong>Title and financing:</strong> distinguish deed date, registration and issue of the note; registered owner, mortgagor and borrower; mortgage liability, cash advanced and valuation. Partial informational extracts are not complete certificates. The aggregate project reconstruction is not attributed to a CajaSiete loan.</p><p><strong>Orion branch:</strong> documented corporate connections, source dates and distinct legal persons are preserved. A historical shareholding is not presented as current ownership. Any specific flow of assets, income or guarantees from Sun Park requires its own evidence.</p><p><strong>Response and correction:</strong> explanations, contrary evidence and documented corrections are invited. Silence is not admission. Preservation, transfer, anonymisation and deletion are assessed under the applicable rules and restricted access, not by publishing protected data.</p>'}}

def git(*args:str,cwd:Path|None=None)->str:
    return subprocess.check_output(['git',*args],cwd=cwd,text=True).strip()
def save(path:Path,value:object)->None:
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
def digest(path:Path)->str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def adapt_builder(path:Path)->str:
    text=path.read_text()
    tree=ast.parse(text)
    functions=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='reconcile_register']
    assert len(functions)==1, 'Expected one canonical reconciler'
    fn=functions[0]
    assignments=[n for n in fn.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='key_events' for t in n.targets)]
    assert len(assignments)==1 and ast.unparse(assignments[0].value)=='deepcopy(KEY_EVENTS)', 'Inspect changed canonical key-event construction'
    assert 'def load_cajasiete_board_events(' not in text, 'Existing adapter requires fresh review'
    declared={a.value for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='add_argument' for a in n.args if isinstance(a,ast.Constant) and isinstance(a.value,str)}
    assert '--check' in declared
    mode='--apply' if '--apply' in declared else '--write' if '--write' in declared else ''
    lines=text.splitlines(keepends=True)
    assignment=assignments[0]
    indent=' '*assignment.col_offset
    lines.insert(assignment.end_lineno,indent+'key_events.extend(load_cajasiete_board_events(REPO_ROOT))\n')
    adapter='def load_cajasiete_board_events(root: Path) -> list[dict]:\n    from prepare_cajasiete_board_visuals_20260905 import load_cajasiete_events\n    return load_cajasiete_events(root)\n\n\n'
    lines.insert(fn.lineno-1,adapter)
    result=''.join(lines)
    compile(result,str(path),'exec')
    path.write_text(result)
    return mode

def patch_generator(path:Path,mode:str)->None:
    text=path.read_text()
    begin='# DOCUMENTARY-REVIEW-20260905:START\n';end='# DOCUMENTARY-REVIEW-20260905:END\n'
    patch=begin+'for _language, _changes in '+repr(OVERRIDE)+'.items():\n COPY[_language].update(_changes)\n'+end
    if begin in text:
        assert text.count(begin)==text.count(end)==1
        text=text[:text.index(begin)]+patch+text[text.index(end)+len(end):]
    else:
        marker='def vector(lang,n,logical,x):'
        assert text.count(marker)==1
        text=text.replace(marker,patch+marker,1)
    old='<h3>{c["sources"]}</h3><p>{source_links(lang,x)}</p>'
    assert text.count(old)==1
    if old+'{c["review"]}' not in text:text=text.replace(old,old+'{c["review"]}',1)
    replacement='[sys.executable,BUILDER'+(','+repr(mode) if mode else '')+']'
    candidates=["[sys.executable,BUILDER,'--write']","[sys.executable,BUILDER,'--apply']",'[sys.executable,BUILDER]']
    present=[s for s in candidates if s in text]
    assert len(present)==1, 'Inspect generator canonical write invocation'
    text=text.replace(present[0],replacement)
    compile(text,str(path),'exec');path.write_text(text)

def main()->None:
    root=Path(git('rev-parse','--show-toplevel'));seed=os.environ['GITHUB_SHA']
    assert os.environ['GITHUB_REF_NAME']==BRANCH and git('rev-parse','HEAD')==seed
    subprocess.run(['git','fetch','--quiet','origin','main'],cwd=root,check=True)
    base=git('rev-parse','origin/main',cwd=root)
    assert git('ls-remote','origin','refs/heads/'+BRANCH,cwd=root).split()[0]==seed
    work=Path(os.environ['RUNNER_TEMP'])/('cajasiete-review-'+seed[:12]);assert not work.exists()
    subprocess.run(['git','worktree','add','--detach',str(work),base],cwd=root,check=True)
    out=root/'qa-cajasiete-review';out.mkdir(exist_ok=True)
    save(out/'attempt.json',{'seed':seed,'base':base,'status':'PREPARING_NOT_PUBLISHED'})
    cross=json.loads((root/CROSS).read_text());before=json.loads((work/REG).read_text())
    assert not {e['event_id'] for e in before['events']} & {v['event_id'] for v in cross['events'].values()}, 'Canonical event collision or already integrated'
    media=json.loads((work/'data/digital-media-asset-register-v1.json').read_text())
    assert not set(cross['assets'].values()) & {a['reference'] for a in media['logical_assets']}, 'Media collision'
    for rel in [GENERATOR,CHECKER,SELF,WORKFLOW,INPUT,CROSS]:
        target=work/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(root/rel,target)
    cross.setdefault('baseline_reconciliation_history',[]).append({'prior_page_hashes':cross['baseline_pages'].copy(),'source_worker':seed,'new_main':base,'reason':'Preserve all current-main bytes outside existing owned blocks.'})
    for rel in cross['baseline_pages']:
        assert b'<!-- CAJASIETE-BOARD-VISUALS-20260905:START -->' not in (work/rel).read_bytes()
        cross['baseline_pages'][rel]=digest(work/rel)
    cross['review_base_sha']=base;save(work/CROSS,cross)
    try:
        mode=adapt_builder(work/BUILDER)
        patch_generator(work/GENERATOR,mode)
        save(out/'adapter.json',{'builder_mode':mode,'builder_source_sha256':digest(root/BUILDER),'current_main_builder_sha256':digest(work/BUILDER),'method':'AST insertion after preserved KEY_EVENTS copy'})
        commands=[[sys.executable,GENERATOR,'apply'],[sys.executable,BUILDER,'--check'],[sys.executable,'scripts/validate_institutional_communications.py'],[sys.executable,GENERATOR,'check'],[sys.executable,CHECKER]]
        for i,cmd in enumerate(commands,1):
            r=subprocess.run(cmd,cwd=work,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            (out/f'check-{i}.txt').write_text(r.stdout);print(r.stdout,flush=True)
            assert r.returncode==0,f'Check {i} failed ({r.returncode}); no push'
        after=json.loads((work/REG).read_text());amap={e['event_id']:e for e in after['events']}
        assert all(amap.get(e['event_id'])==e for e in before['events']), 'Existing event changed'
        br=json.loads((work/'ops/CAJASIETE_BOARD_BROWSER_20260905.json').read_text())
        assert br['status']=='PASS' and br['case_count']==br['passed']==24
        acceptance=json.loads((work/'ops/CAJASIETE_BOARD_VISUAL_ACCEPTANCE_20260905.json').read_text())
        allowed=set(acceptance['paths'])|{GENERATOR,CHECKER,SELF,WORKFLOW,CROSS,INPUT,REPORT,'ops/CAJASIETE_BOARD_VISUAL_ACCEPTANCE_20260905.json','ops/CAJASIETE_BOARD_BROWSER_20260905.json'}
        status=subprocess.check_output(['git','status','--porcelain','--untracked-files=all'],cwd=work,text=True)
        changed=[s[3:] for s in status.splitlines() if not s[3:].startswith(('qa-cajasiete/','__pycache__/','scripts/__pycache__/'))]
        assert set(changed)<=allowed,('Unexpected changes',sorted(set(changed)-allowed))
        assert not any(s[:2].strip()=='D' for s in status.splitlines()),'No deletion permitted'
        record={'control_id':CONTROL,'status':'CURRENT_MAIN_RECONCILED_STATIC_AND_24_BROWSER_PASS_NOT_DEPLOYED','source_worker_sha':seed,'base_sha':base,'preserved_canonical_events':len(before['events']),'candidate_event_count':len(after['events']),'native_private_sources_published':False,'source_crops_published':False,'source_crop_status':'WITHHELD_PENDING_CANONICAL_IDENTITY_AND_PUBLICATION_REVIEW','main_not_modified':True,'changed_paths':sorted(set(changed)|{REPORT}),'browser_report':'ops/CAJASIETE_BOARD_BROWSER_20260905.json','open_gaps':acceptance.get('open_proof',[]),'writer_retirement_required':True,'remaining_acceptance':['Retire writer','Exact-head release/publication checks','Single integrator permit','Merge and exact Pages/live readback']}
        save(work/REPORT,record)
        subprocess.run(['git','add','--',*sorted(allowed)],cwd=work,check=True)
        tree=git('write-tree',cwd=work)
        commit=subprocess.check_output(['git','commit-tree',tree,'-p',seed,'-p',base,'-m','Reconcile CajaSiete reader on current main; preserve records and pass 24 browser cases'],cwd=work,text=True).strip()
        record.update(prepared_tree=tree,candidate_sha=commit);save(out/'preparation-receipt.json',record)
        for rel in sorted(allowed):
            if (work/rel).is_file():
                target=out/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(work/rel,target)
        assert git('ls-remote','origin','refs/heads/'+BRANCH,cwd=root).split()[0]==seed,'Concurrent worker moved; artifact only'
        assert git('ls-remote','origin','refs/heads/main',cwd=root).split()[0]==base,'Main moved; artifact only'
        subprocess.run(['git','push','origin',commit+':refs/heads/'+BRANCH],cwd=root,check=True)
        print(json.dumps({'status':'WORKER_UPDATED_NOT_PUBLISHED','candidate':commit,'base':base,'tree':tree}))
    finally:
        for rel in [BUILDER,GENERATOR]:
            target=out/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(work/rel,target)
        if (work/'qa-cajasiete').exists():shutil.copytree(work/'qa-cajasiete',out/'screenshots',dirs_exist_ok=True)

if __name__=='__main__':main()
