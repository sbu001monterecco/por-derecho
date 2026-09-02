#!/usr/bin/env python3
from pathlib import Path
import csv, json
R=Path(__file__).resolve().parents[1]; D=R/'assets/data'
def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def save(p,o): Path(p).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# DP 748/2026: source-prove the 24-Mar-2026 signer.
ll=load(D/'matter-identity-registry-v1.la-laguna-judicial-people.json')
for x in ll['records']:
    if x['id']=='PD-SP-P-0147':
        s='Auto 454/2026 of 24-Mar-2026, physical original photographed 08-Apr-2026, naming Graciela Pérez-Valencia Díaz as Magistrada-Juez'
        if s not in x['identity_sources']: x['identity_sources'].insert(0,s)
        x['capacity_boundary']='Magistrada-Juez of Plaza nº 4 del Tribunal de Instancia (Sección Instrucción), San Cristóbal de La Laguna, for the source-verified DP 748/2026 acts dated 24-Mar-2026, 20-May-2026 and 16-Jul-2026. Identity does not transfer authorship to any other act.'
save(D/'matter-identity-registry-v1.la-laguna-judicial-people.json',ll)

# New exact Fiscal identity from signed E.G. 58/2026 source.
people=load(D/'matter-identity-registry-v1.people.json')
if not any(x.get('name')=='Fernando Rodríguez Rey' for x in people['records']):
    assert not any(x.get('id')=='PD-SP-P-0163' for x in people['records'])
    people['records'].append({'id':'PD-SP-P-0163','type':'PERSON','name':'Fernando Rodríguez Rey','aliases':['Fernando Rodriguez Rey'],'routes':{'es':'/es/registro-identidad-profesionales-justicia/#ministerio-fiscal','en':'/en/justice-professionals-identity-register/#prosecution-service'},'identity_resolution':'CARET_CONFIRMED','identity_sources':['Signed FGE Unidad de Delitos Económicos communication dated 11-Feb-2026 in E.G. 58/2026, acknowledging receipt on 10-Feb-2026, opening the governmental file and archiving it after taking cognisance of the communication'],'capacity_boundary':'Identity and signature as Fiscal de Sala Coordinador de Delitos Económicos on the cited 11-Feb-2026 E.G. 58/2026 communication only. It does not establish personal receipt of every annex, a merits finding, endorsement, wrongdoing, coordination or responsibility.'})
save(D/'matter-identity-registry-v1.people.json',people)

# Upgrade E.G. 58/2026 from unresolved reference to source-confirmed file.
pr=load(D/'matter-identity-registry-v1.proceedings.json')
for x in pr['records']:
    if x['id']=='PD-SP-R-0043':
        x.update({'name':'E.G. 58/2026 — FGE Unidad de Delitos Económicos','aliases':['EG 58/2026','E.G. 58/2026','Expediente Gubernativo 58/2026'],'identity_resolution':'CARET_CONFIRMED','competent_organ':'Fiscalía General del Estado — Unidad de Delitos Económicos','procedural_state':'OPENED_AND_ARCHIVED_11FEB2026_AFTER_TAKING_COGNISANCE','identity_sources':['Signed FGE Unidad de Delitos Económicos communication dated 11-Feb-2026; REGAGE 26e00013713834 / Registro Electrónico General 26e00013040021','evidence/fiscalia/2026/MF_MAILBOX_REGAGE_CONTROL_31AUG2026.md'],'source_identified_fiscals':['PD-SP-P-0163'],'identity_boundary':'Exact governmental-file identity, handling unit, 10/11-Feb-2026 receipt/opening/archive checkpoint and signatory only. The communication does not establish the allegations true or false, a criminal-investigation opening, a merits finding, coordination, wrongdoing or responsibility.'})
save(D/'matter-identity-registry-v1.proceedings.json',pr)

# Reconcile canonical counts.
idx=load(D/'matter-identity-registry-v1.json')
if idx['counts']['total']==343:
    idx['counts']['total']=344; idx['counts']['PERSON']=163
    for p in idx['parts']:
        if p.get('path')=='matter-identity-registry-v1.people.json': p['count']=121
idx['control_date']='2026-09-02'
save(D/'matter-identity-registry-v1.json',idx)

# Current justice denominator: 59 -> 60, confirmed 56 -> 57, Fiscal 17 -> 18.
ja=load(D/'justice-authority-register-current-v2.json')
ja['control_date']='2026-09-02'; dc=ja['derived_counts']; dc['unique_named_people']=60; dc['confirmed']=57; dc['by_role']['MINISTERIO_FISCAL']=18
ja['new_source_closures_2026_09_02']=[{'master_id':'TF-CRI-003','proceeding_id':'PD-SP-R-0003','closure':'Auto 454/2026 signer source-proved','person_id':'PD-SP-P-0147','act_date':'2026-03-24'},{'master_id':'UNK-FIS-001','proceeding_id':'PD-SP-R-0043','closure':'E.G. 58/2026 exact file and Fiscal signer source-proved','person_id':'PD-SP-P-0163','act_date':'2026-02-11'}]
ja['proceeding_authority_crosswalk']='assets/data/proceedings-authority-coverage-current-v1.json'
save(D/'justice-authority-register-current-v2.json',ja)

# Build no-silent-blank crosswalk for every judicial/appellate/Fiscalía Master row.
with (R/'archive/PROCEEDINGS_MASTER_REGISTER.csv').open(encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f))
KNOWN={
'GC-JUD-001':{'judges':[('PD-SP-P-0124','Juan Avello Formoso','2017-12-19'),('PD-SP-P-0057','Alberto López Villarrubia','2020-05-12;2021-02-24')],'lajs':[('PD-SP-P-0121','Eduardo José Rebollo Sanz','2017-12-20')],'fiscals':[]},
'TF-CRI-003':{'judges':[('PD-SP-P-0147','Graciela Pérez-Valencia Díaz','2026-03-24;2026-05-20;2026-07-16')],'lajs':[('PD-SP-P-0148','María del Pilar Luis Medina','2026-06-15;2026-09-01')],'fiscals':[]},
'TF-CIV-001':{'judges':[('PD-SP-P-0150','Carmen Rosa Marrero Fumero','2019-09-04;2025-06-03')],'lajs':[('PD-SP-P-0151','Juan Manuel Pérez Ramos','2019-09-02'),('PD-SP-P-0152','María del Pilar Parrilla Martín','2019-12-03/2020'),('PD-SP-P-0153','Marco Eulogio Chiang Rebolledo','2025-04-09')],'fiscals':[]},
'TF-CIV-002':{'judges':[('PD-SP-P-0150','Carmen Rosa Marrero Fumero','2026-06-19')],'lajs':[('PD-SP-P-0151','Juan Manuel Pérez Ramos','2024-09-18'),('PD-SP-P-0154','Cristina María Hernández Díaz','2026-07-06/07'),('PD-SP-P-0155','Francisco Martín Pozo','2026-07-28')],'fiscals':[]},
'TF-CIV-006':{'judges':[('PD-SP-P-0149','María Mercedes Santana Rodríguez','2014-02-18')],'lajs':[],'fiscals':[]},
'GC-FIS-013':{'judges':[],'lajs':[],'fiscals':[('PD-SP-P-0104','Elena Herrera Rodríguez','2019-05-07'),('PD-SP-P-0103','Beatriz Sánchez Carreras','2019-05-16')]},
'LZ-APP-004':{'judges':[('PD-SP-P-0096','José Luis Goizueta Adame','2018-11-13'),('PD-SP-P-0097','Nicolás Acosta González','2018-11-13'),('PD-SP-P-0098','María del Pilar Verástegui Hernández','2018-11-13')],'lajs':[],'fiscals':[]},
'UNK-FIS-001':{'judges':[],'lajs':[],'fiscals':[('PD-SP-P-0163','Fernando Rodríguez Rey','2026-02-11')]}}
name_to_id={}
for part in idx['parts']:
    if part.get('type')=='PERSON':
        for p in load(D/part['path']).get('records',[]): name_to_id[p.get('name')]=p.get('id')
for m,n in {'LZ-FIS-045':'Ramona Muñoz Casas','TF-FIS-007':'José Luis Sánchez-Jáuregui y Alcaide','GC-FIS-032':'Vicente Máximo Garrido García','GC-FIS-033':'Jaime Serrano-Jover González','NAT-FIS-004':'María José Osuna Cerezo'}.items():
    if name_to_id.get(n): KNOWN[m]={'judges':[],'lajs':[],'fiscals':[(name_to_id[n],n,'source-controlled signed act')]}

out=[]
for r in rows:
    m=r['Master_ID']; t=r['Record_Type'].upper(); stream=(r.get('Stream') or '').lower()
    if not ('JUDICIAL' in t or 'APPEAL' in t or 'FISCALIA' in t or 'FISCALÍA' in t or '-FIS-' in m or m in KNOWN): continue
    k=KNOWN.get(m,{'judges':[],'lajs':[],'fiscals':[]}); gaps=[]; isf=('FIS' in m or 'FISCAL' in t)
    if isf:
        if not k['fiscals']: gaps.append({'role':'FISCAL','state':'PERSON_NOT_YET_SOURCE_IDENTIFIED'})
    else:
        if not k['judges']: gaps.append({'role':'JUDGE_OR_PANEL','state':'PERSON_NOT_YET_SOURCE_IDENTIFIED'})
        if not k['lajs']: gaps.append({'role':'LAJ','state':'PERSON_NOT_YET_SOURCE_IDENTIFIED'})
        if 'criminal' in stream and not k['fiscals']: gaps.append({'role':'FISCAL','state':'PERSON_NOT_YET_SOURCE_IDENTIFIED'})
    conv=lambda z:[{'person_id':a,'name':b,'source_act_date':c,'state':'SOURCE_IDENTIFIED_CARET_REGISTERED'} for a,b,c in z]
    out.append({'master_id':m,'record_type':t,'reference':r.get('Reference',''),'nig':r.get('NIG',''),'origin_organ':r.get('Origin_Organ',''),'judges':conv(k['judges']),'lajs':conv(k['lajs']),'fiscals':conv(k['fiscals']),'explicit_gaps':gaps,'coverage_state':'CURRENT_RECOVERED_SOURCE_COMPLETE' if not gaps else 'SOURCE_ACTORS_REGISTERED_EXPLICIT_GAPS_PRESERVED','certified_complete_docket':False})
cover={'schema':'por-derecho.proceedings-authority-coverage.v1','control_id':'PD-SP-PROC-AUTH-COVERAGE-20260902-01','control_date':'2026-09-02','status':'CURRENT_RECOVERED_SOURCE_AUTHORITY_COVERAGE_VERIFIED_CERTIFIED_DOCKET_BACKFILL_OPEN','denominator':{'applicable_master_rows':len(out),'source_identified_people_current':60,'caret_confirmed':57,'caret_pending':3},'new_source_closures':['TF-CRI-003 Auto 454/2026 signer = PD-SP-P-0147','PD-SP-R-0043 / E.G. 58/2026 confirmed; signer = PD-SP-P-0163'],'rows':out,'global_boundary':'This closes registration/interlinking for every authority identity actually source-identified in the recovered corpus and converts all remaining applicable roles into explicit evidence gaps. It is not a certified all-history docket census.'}
save(D/'proceedings-authority-coverage-current-v1.json',cover)

# Public bilingual pages generated from the crosswalk.
def html(es=True):
    title='Cobertura de jueces, LAJ y Fiscales por procedimiento^' if es else 'Judge, LAJ and Fiscal coverage by proceeding^'
    intro='Cada fila judicial/Fiscalía del Registro Maestro tiene actores identificados por fuente o una brecha explícita; no hay blancos silenciosos.' if es else 'Every judicial/Fiscalía Master row has source-identified actors or an explicit evidence gap; there are no silent blanks.'
    trs=[]
    for x in out:
        acts=', '.join(a['name']+' ('+a['person_id']+')' for z in ('judges','lajs','fiscals') for a in x[z]) or ('Fuente primaria pendiente' if es else 'Primary source pending')
        gaps='; '.join(g['role'] for g in x['explicit_gaps']) or ('sin brecha en corpus recuperado' if es else 'no recovered-corpus gap')
        trs.append(f"<tr><td><code>{x['master_id']}</code></td><td>{x['reference'] or '—'}</td><td>{acts}</td><td>{gaps}</td></tr>")
    return f'''<!doctype html><html lang="{'es' if es else 'en'}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title} | Por Derecho</title><link rel="stylesheet" href="../../assets/site.css"></head><body><main><h1>{title}</h1><p>{intro}</p><p><strong>{'Denominador' if es else 'Denominator'}:</strong> 60 source-identified · 57 CARET_CONFIRMED · 3 CARET_PENDING.</p><table><thead><tr><th>Master</th><th>{'Referencia' if es else 'Reference'}</th><th>{'Actores' if es else 'Actors'}</th><th>{'Brechas' if es else 'Gaps'}</th></tr></thead><tbody>{''.join(trs)}</tbody></table><h2>{'Límite' if es else 'Boundary'}</h2><p>{cover['global_boundary']}</p></main><script src="../../assets/site.js"></script></body></html>'''
for es,path in [(True,R/'es/registro-autoridades-procedimientos/index.html'),(False,R/'en/proceeding-authority-register/index.html')]: path.parent.mkdir(parents=True,exist_ok=True); path.write_text(html(es),encoding='utf-8')

print('authority closure built',len(out),'Master rows')
