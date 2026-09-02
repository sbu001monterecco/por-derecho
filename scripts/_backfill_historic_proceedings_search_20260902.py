#!/usr/bin/env python3
from pathlib import Path
import csv, json, hashlib, re

ROOT=Path('.')
CSV=ROOT/'archive/PROCEEDINGS_MASTER_REGISTER.csv'
PUBLIC=ROOT/'assets/data/proceedings-master-public-v1.json'
REG=ROOT/'assets/data/matter-identity-registry-v1.json'
AUTH=ROOT/'assets/data/justice-authority-register-current-v2.json'

with CSV.open(encoding='utf-8-sig', newline='') as f:
    reader=csv.DictReader(f); fields=reader.fieldnames; rows=list(reader)
by_id={r['Master_ID']:r for r in rows}
by_ref={r['Reference']:r for r in rows}

def patch(mid, **kw):
    r=by_id[mid]
    for k,v in kw.items(): r[k]=v

def add(mid, **kw):
    if mid in by_id: raise SystemExit(f'duplicate {mid}')
    r={k:'' for k in fields}; r['Master_ID']=mid
    for k,v in kw.items(): r[k]=v
    rows.append(r); by_id[mid]=r; by_ref[r['Reference']]=r
    return r

# Upgrade rows already present: never duplicate aliases already canonically represented.
patch('LZ-CIV-035', Origin_Organ='Juzgado de Primera Instancia nº 4 de Arrecife', Current_Custodian='Juzgado de Primera Instancia nº 4 de Arrecife', Reference='Juicio Verbal 1260/2011', Secondary_Reference='0001260/2011-00; historical file-name conflict 1240/2011 preserved', NIG='3500442120110008131', Status='First-instance judgment 7-May-2012; appellate judgment 13-Jan-2014 located', Latest_Known_Event='AP Las Palmas Sección Cuarta Sentencia 89/2014 in Rollo 793/2012', Appeal_or_Review='Rollo 793/2012 / Sentencia 89/2014', Source_Status='VERIFIED_PRIMARY_APPELLATE_COPY', Primary_Source_Anchor='Sentencia Proc1260-2011 13ENE2014.pdf — primary appellate copy', Open_Reference_Gap='First-instance signed judgment identifying Judge/LAJ; complete first-instance docket and service/finality record', Public_Treatment='PUBLIC_SUMMARY_WITH_PROCEDURAL_LIMITS', Last_Scan_Date='2026-09-02', Notes='Primary appellate copy fixes origin court, NIG and appellate panel. It does not identify the first-instance Judge/LAJ. Historical 1240/2011 filename conflict is retained only as a retrieval alias.')
patch('LZ-REF-038', Record_Type='JUDICIAL_PROCEEDING', Is_Proceeding='TRUE', Proceeding_Class='DIRECT', Stream='Criminal', Geography='Lanzarote', Origin_Organ='Juzgado de Instrucción nº 4 de Arrecife', Current_Custodian='Juzgado de Instrucción nº 4 de Arrecife', Reference='DP 168/2015', Secondary_Reference='Reported accumulated into DP 3017/2014', Date_or_Period='2015-2017', Connection='Community / April-2014 events; later accumulation reported in controlled litigation inventory', Object_or_Purpose='Attempted-fraud allegations reported in controlled historical litigation inventory', Status='Proceeding identity and court recovered from controlled historical inventory; signed accumulation order still primary-pending', Appeal_or_Review='', Linked_Proceedings='LZ-JUD-047', Source_Status='CORPUS_REPORTED_PRIMARY_PENDING', Primary_Source_Anchor='Procedimientos Gil Marer — ES controlled historical litigation inventory', Open_Reference_Gap='NIG; complaint/querella; signed 15-Jul-2017 accumulation/extension act; Judge; LAJ; prosecutor; final disposition and notice', Public_Treatment='PUBLIC_SUMMARY_WITH_IDENTITY_GAP', Last_Scan_Date='2026-09-02', Notes='Do not transfer facts/parties/merits from DP 3017/2014. Accumulation is recorded as a source-reported procedural relationship pending the signed act.')
patch('LZ-REF-039', Record_Type='JUDICIAL_PROCEEDING', Is_Proceeding='TRUE', Proceeding_Class='DIRECT', Stream='Civil', Geography='Lanzarote', Origin_Organ='Juzgado de Primera Instancia nº 4 de Arrecife', Current_Custodian='Juzgado de Primera Instancia nº 4 de Arrecife', Reference='Juicio Verbal 268/2016', Date_or_Period='2016-2017', Status='Controlled historical inventory reports judgment 18-Apr-2017; primary signed judgment pending', Source_Status='CORPUS_REPORTED_PRIMARY_PENDING', Primary_Source_Anchor='Procedimientos Gil Marer — ES controlled historical litigation inventory; Sentencia 2017 source family located in Gmail', Open_Reference_Gap='NIG; signed judgment; Judge; LAJ; pleadings; service/finality', Public_Treatment='PUBLIC_SUMMARY_WITH_IDENTITY_GAP', Last_Scan_Date='2026-09-02')

# Missing genuine proceedings/appeals: separate rows, no silent mergers.
add('LZ-CIV-045', Record_Type='JUDICIAL_PROCEEDING', Is_Proceeding='TRUE', Proceeding_Class='DIRECT', Stream='Civil', Geography='Lanzarote', Origin_Organ='Juzgado de Instrucción nº 3 de Arrecife (antiguo Mixto nº 8; civil function in source)', Current_Custodian='Arrecife civil court — successor allocation not inferred', Reference='Procedimiento Ordinario 467/2010', Secondary_Reference='Sentencia 39/2011', NIG='3500441120100004798', Date_or_Period='2010-2011', Connection='Community governance / 28-May-2009 resolutions', Object_or_Purpose='Challenge to Community resolutions', Status='Sentencia 39/2011 dated 14-Mar-2011 located; claim dismissed', Latest_Known_Event='14-Mar-2011 Sentencia 39/2011', Source_Status='VERIFIED_PRIMARY_COPY', Primary_Source_Anchor='Sentencia 2011 - Minorías Morosas.pdf / 1. SENTENCIA Desestimación Minorías vs Cdad Prop 467-2010.pdf', Repo_Canonical_Source='archive/handoffs/2026-09-02-deep-proceedings-authority-email-drive-scan-checkpoint.md', Open_Reference_Gap='LAJ identity; complete docket; appeal/finality/service record', Public_Treatment='PUBLIC_SUMMARY_WITH_PROCEDURAL_LIMITS', Last_Scan_Date='2026-09-02', Notes='Primary judgment identifies Magistrada-Juez Ángela López-Yuste Padial. No LAJ is inferred from the judgment.')
add('LZ-APP-046', Record_Type='APPEAL_ROLL', Is_Proceeding='TRUE', Proceeding_Class='DIRECT', Stream='Civil appellate', Geography='Lanzarote / AP Las Palmas', Origin_Organ='Audiencia Provincial de Las Palmas — Sección Cuarta', Current_Custodian='Audiencia Provincial de Las Palmas — Sección Cuarta', Reference='Rollo 793/2012', Secondary_Reference='Sentencia 89/2014; appeal from Juicio Verbal 1260/2011', NIG='3500442120110008131', Date_or_Period='2012-2014', Connection='Appeal from Juicio Verbal 1260/2011', Object_or_Purpose='Appeal concerning desahucio por precario and Monterecco Sun Park S.L.', Status='Sentencia 89/2014 issued 13-Jan-2014', Latest_Known_Event='13-Jan-2014 Sentencia 89/2014', Parent_Master_ID='LZ-CIV-035', Linked_Proceedings='LZ-CIV-035', Source_Status='VERIFIED_PRIMARY_COPY', Primary_Source_Anchor='Sentencia Proc1260-2011 13ENE2014.pdf', Repo_Canonical_Source='archive/handoffs/2026-09-02-deep-proceedings-authority-email-drive-scan-checkpoint.md', Open_Reference_Gap='LAJ identity; court-certified complete roll; service/finality record', Public_Treatment='PUBLIC_SUMMARY_WITH_PROCEDURAL_LIMITS', Last_Scan_Date='2026-09-02', Notes='Primary judgment identifies Presidenta Emma Galcerán Solsona and Magistrates María Elena Corral Losada and Jesús Ángel Suárez Ramos (ponente).')
add('LZ-JUD-047', Record_Type='JUDICIAL_PROCEEDING', Is_Proceeding='TRUE', Proceeding_Class='DIRECT', Stream='Criminal', Geography='Lanzarote', Origin_Organ='Juzgado de Instrucción nº 4 de Arrecife', Current_Custodian='Juzgado de Instrucción nº 4 de Arrecife', Reference='DP 3017/2014', Secondary_Reference='Diligencias Previas 0003017/2014', NIG='3500443220140012080', Date_or_Period='2014-', Connection='Access/occupation dispute; later accumulation relationship reported with DP 168/2015', Object_or_Purpose='Criminal investigation initiated on complaint by Richard Daughety; exact offence framing requires complete complaint/docket', Status='Primary citation dated 14-Oct-2014 located; complete later docket/status primary-pending', Latest_Known_Event='14-Oct-2014 citation for 5-Nov-2014 statements in located primary copy', Linked_Proceedings='LZ-REF-038', Source_Status='VERIFIED_PRIMARY_IDENTITY_COPY', Primary_Source_Anchor='CITACION Procedimiento 3017-2014 (GM y PDM).pdf', Repo_Canonical_Source='archive/handoffs/2026-09-02-deep-proceedings-authority-email-drive-scan-checkpoint.md', Open_Reference_Gap='Signed initiating order/complaint; Judge; LAJ; prosecutor; accumulation act with DP 168/2015; final disposition, notice and finality', Public_Treatment='PUBLIC_SUMMARY_WITH_PROCEDURAL_LIMITS', Last_Scan_Date='2026-09-02', Notes='Primary citation proves reference, court and NIG but does not name Judge/LAJ. No later office-holder is inferred.')
add('LZ-JUD-048', Record_Type='JUDICIAL_PROCEEDING', Is_Proceeding='TRUE', Proceeding_Class='DIRECT', Stream='Criminal', Geography='Lanzarote', Origin_Organ='Juzgado de Instrucción nº 3 de Arrecife', Current_Custodian='Juzgado de Instrucción nº 3 de Arrecife', Reference='DP 2084/2016', Date_or_Period='2016-', Connection='LPB / Community / dissident-owner dispute', Object_or_Purpose='Historical inventory reports allegations including procedural fraud, fraud, falsity, misappropriation, disloyal administration, calumny and false accusation', Status='Controlled historical proceeding inventory located; primary docket and disposition pending', Source_Status='CORPUS_REPORTED_PRIMARY_PENDING', Primary_Source_Anchor='Procedimientos Gil Marer — ES controlled historical litigation inventory', Repo_Canonical_Source='archive/handoffs/2026-09-02-deep-proceedings-authority-email-drive-scan-checkpoint.md', Open_Reference_Gap='NIG; querella/complaint; exact parties/capacities; Judge; LAJ; prosecutor; archive order and finality', Public_Treatment='PUBLIC_SUMMARY_WITH_IDENTITY_GAP', Last_Scan_Date='2026-09-02', Notes='Allegation labels are historical source characterisations, not findings.')
add('LZ-FIS-049', Record_Type='FISCALIA_FILE', Is_Proceeding='TRUE', Proceeding_Class='DIRECT', Stream='Fiscalía / criminal precursor', Geography='Las Palmas / Lanzarote', Origin_Organ='Fiscalía Provincial de Las Palmas', Current_Custodian='Historical destination court/file pending certified linkage', Reference='273/2013', Secondary_Reference='Querella Fiscalía 273-2013 dated 27-Dec-2013', Date_or_Period='2013-2014', Connection='Precursor Fiscalía frame later associated in historical inventory with DP 332/2014', Object_or_Purpose='Fiscalía investigation/querella concerning alleged corporate/asset-concealment offences; exact judicial conversion requires primary linkage', Status='Primary querella file located in Drive; complete extraction and judicial destination linkage pending', Linked_Proceedings='LZ-JUD-002', Source_Status='VERIFIED_PRIMARY_FILE_LOCATED_CONTENT_EXTRACTION_PENDING', Primary_Source_Anchor='1.5. Querella Fiscalia 273-2013 27DIC2013.pdf', Repo_Canonical_Source='archive/handoffs/2026-09-02-deep-proceedings-authority-email-drive-scan-checkpoint.md', Open_Reference_Gap='Assigned Fiscal/signatory extraction; judicial destination/NIG; complete investigation file; disposition/finality', Public_Treatment='PUBLIC_SUMMARY_WITH_PROCEDURAL_LIMITS', Last_Scan_Date='2026-09-02', Notes='Historical linkage to DP 332/2014 is preserved as a source-reported relationship, not treated as same identity absent certified conversion record.')
add('LZ-CIV-050', Record_Type='JUDICIAL_PROCEEDING', Is_Proceeding='TRUE', Proceeding_Class='DIRECT', Stream='Civil preliminary proceedings', Geography='Lanzarote', Origin_Organ='Juzgado de Primera Instancia nº 2 de Arrecife', Current_Custodian='Juzgado de Primera Instancia nº 2 de Arrecife', Reference='Diligencias Preliminares 1041/2017', Date_or_Period='2017-2018', Connection='LPB / CAM / tanteo-retracto transaction-document request', Object_or_Purpose='Historical inventory describes preliminary diligences seeking transaction documentation', Status='Controlled historical inventory and source-family attachment located; signed complete docket pending', Source_Status='CORPUS_REPORTED_PRIMARY_PENDING', Primary_Source_Anchor='LPB - Proc 1041 MATOS debe aportar escritura el 19FEB - 12JAN18.pdf; controlled historical litigation inventory', Open_Reference_Gap='NIG; signed first/last acts; Judge; LAJ; exact parties/capacities; finality', Public_Treatment='PUBLIC_SUMMARY_WITH_IDENTITY_GAP', Last_Scan_Date='2026-09-02')
add('LZ-FIS-051', Record_Type='FISCALIA_FILE', Is_Proceeding='TRUE', Proceeding_Class='DIRECT', Stream='Fiscalía', Geography='Las Palmas', Origin_Organ='Fiscalía Provincial de Las Palmas', Current_Custodian='Fiscalía Provincial de Las Palmas', Reference='302/2018', Date_or_Period='2018-', Connection='GM/Aweswell complaint concerning AC/CAM reported in historical inventory', Object_or_Purpose='Historical inventory reports allegations of disloyal administration, damage, arbitrary exercise of rights and false testimony', Status='Controlled historical inventory identifies reference; complete Fiscalía file pending', Source_Status='CORPUS_REPORTED_PRIMARY_PENDING', Primary_Source_Anchor='Procedimientos Gil Marer — ES controlled historical litigation inventory', Open_Reference_Gap='Exact Fiscalía file class; assigned Fiscal/signatory; opening and archive decrees; annexes; notice/finality', Public_Treatment='PUBLIC_SUMMARY_WITH_IDENTITY_GAP', Last_Scan_Date='2026-09-02', Notes='Allegations are source characterisations, not findings.')
add('LZ-REF-052', Record_Type='JUDICIAL_PROCEEDING', Is_Proceeding='UNVERIFIED', Proceeding_Class='DIRECT', Stream='Judicial — criminal/civil classification unresolved', Geography='Lanzarote', Origin_Organ='Juzgado de Instrucción nº 4 de Arrecife — historical inventory label', Current_Custodian='Exact successor/custodian pending', Reference='49/2018', Date_or_Period='2018', Connection='LPB / Bankia / swap dispute', Object_or_Purpose='Historical inventory labels this as a Bankia swap matter; exact procedural class requires primary docket', Status='Reference registered from controlled historical inventory; primary docket pending', Source_Status='OPEN_REFERENCE', Primary_Source_Anchor='Procedimientos Gil Marer — ES controlled historical litigation inventory', Open_Reference_Gap='Exact proceeding class/title; NIG; parties/capacities; Judge; LAJ; pleadings; disposition/finality', Public_Treatment='PUBLIC_SUMMARY_WITH_IDENTITY_GAP', Last_Scan_Date='2026-09-02', Notes='Do not infer criminal classification from the inventory section heading or civil classification from the word demanda.')
add('LZ-REF-053', Record_Type='JUDICIAL_PROCEEDING', Is_Proceeding='UNVERIFIED', Proceeding_Class='DIRECT', Stream='Mortgage enforcement / exact historical classification unresolved', Geography='Lanzarote', Origin_Organ='Juzgado de Instrucción nº 2 de Arrecife — historical inventory label', Current_Custodian='Exact successor/custodian pending', Reference='92/2012', Date_or_Period='2012-', Connection='Bankia / LPB mortgage enforcement', Object_or_Purpose='Historical inventory describes mortgage enforcement by Bankia against LPB', Status='Reference registered from controlled historical inventory; primary docket pending', Source_Status='OPEN_REFERENCE', Primary_Source_Anchor='Procedimientos Gil Marer — ES controlled historical litigation inventory', Open_Reference_Gap='Exact court/jurisdiction; NIG; enforcement title; Judge; LAJ; parties; signed termination/disposition; finality', Public_Treatment='PUBLIC_SUMMARY_WITH_IDENTITY_GAP', Last_Scan_Date='2026-09-02', Notes='The inventory places this under penal matters but describes mortgage enforcement; classification is therefore deliberately unresolved pending primary source.')
add('LZ-APP-054', Record_Type='APPEAL_ROLL', Is_Proceeding='TRUE', Proceeding_Class='DIRECT', Stream='Civil appellate', Geography='Lanzarote / AP Las Palmas', Origin_Organ='Audiencia Provincial de Las Palmas — Sección Quinta', Current_Custodian='Audiencia Provincial de Las Palmas — Sección Quinta', Reference='Rollo 526/2013', Secondary_Reference='Desistimiento / transacción reported from P.O. 1241/2011', Date_or_Period='2013-2014', Connection='Appeal/desistimiento lane arising from P.O. 1241/2011', Object_or_Purpose='Historical inventory describes desistimiento and disputed transaction/debt-zero wording', Status='Primary source-family documents located including 25-Jul-2014 opposition/allegations; signed final decree/order and panel identities pending', Parent_Master_ID='LZ-CIV-040', Linked_Proceedings='LZ-CIV-040', Source_Status='CORPUS_REPORTED_PRIMARY_PENDING', Primary_Source_Anchor='ALEGACIONES CDAD ref DESISTIMIENTO LPB 526-2013 25JUL2014.pdf; Desistimiento LPb vs CP 2014.pdf', Open_Reference_Gap='NIG; exact final signed resolution; panel/Judge identities if judicial act applicable; LAJ; service/finality', Public_Treatment='PUBLIC_SUMMARY_WITH_IDENTITY_GAP', Last_Scan_Date='2026-09-02', Notes='No individual judicial office-holder is inferred from the section name.')

# Cross-links after new rows exist.
by_id['LZ-CIV-035']['Linked_Proceedings']='LZ-APP-046'
by_id['LZ-CIV-040']['Linked_Proceedings']='; '.join(filter(None,[by_id['LZ-CIV-040'].get('Linked_Proceedings',''),'LZ-APP-054']))

# Stable output ordering: preserve existing order and append only.
with CSV.open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n'); w.writeheader(); w.writerows(rows)

# Rebuild deterministic public projection from canonical CSV using existing publication policy/field allowlist.
old=json.loads(PUBLIC.read_text(encoding='utf-8'))
allow=set(old['publication_policy']['public_treatment_allowlist'])
field_allow=old['field_allowlist']
public_rows=[]; excluded=0
for r in rows:
    t=r.get('Public_Treatment','')
    if t in allow:
        public_rows.append({k:r.get(k,'') for k in field_allow})
    elif t in set(old['publication_policy'].get('excluded_treatment_values',[])):
        excluded+=1
    else:
        raise SystemExit(f'Unknown Public_Treatment {t!r} for {r["Master_ID"]}')
raw=CSV.read_bytes()
old['canonical_source_sha256']=hashlib.sha256(raw).hexdigest()
old['source_record_count']=len(rows); old['public_record_count']=len(public_rows); old['excluded_record_count']=excluded; old['records']=public_rows
PUBLIC.write_text(json.dumps(old,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# New source-verified people. IDs checked against current registry; immutable and unique.
people_path=ROOT/'assets/data/matter-identity-registry-v1.historic-arrecife-judicial-people-20260902.json'
people={
 'schema':'por-derecho.matter-identity-registry.part.v1','registry_id':'PD-SP-IDENTITY-REGISTRY-001','type':'PERSON',
 'scope':'Historic Arrecife/AP Las Palmas judicial office-holders newly source-identified on 2-Sep-2026',
 'records':[
  {'id':'PD-SP-P-0163','type':'PERSON','name':'Ángela López-Yuste Padial','aliases':['Angela Lopez-Yuste Padial','Ángela López Yuste Padial'],'routes':{'es':'/es/registro-autoridad-historica-arrecife/#pd-sp-p-0163','en':'/en/historic-arrecife-justice-authority-register/#pd-sp-p-0163'},'identity_resolution':'CARET_CONFIRMED','identity_sources':['Sentencia 39/2011, Procedimiento Ordinario 467/2010, dated 14-Mar-2011, primary judicial copy'],'verification_detail':'Primary signed judicial judgment identifies the Magistrada-Juez','capacity_boundary':'Magistrada-Juez deciding Sentencia 39/2011 in P.O. 467/2010 only. Identity does not establish authorship of any other act, LAJ identity, later office, knowledge, merits correctness, wrongdoing or liability.'},
  {'id':'PD-SP-P-0164','type':'PERSON','name':'Emma Galcerán Solsona','aliases':['Emma Galceran Solsona'],'routes':{'es':'/es/registro-autoridad-historica-arrecife/#pd-sp-p-0164','en':'/en/historic-arrecife-justice-authority-register/#pd-sp-p-0164'},'identity_resolution':'CARET_CONFIRMED','identity_sources':['Sentencia 89/2014, Rollo de Apelación 793/2012, dated 13-Jan-2014, primary judicial copy'],'verification_detail':'Primary appellate judgment identifies Presidenta of the panel','capacity_boundary':'Presidenta of the Sección Cuarta panel recorded in Sentencia 89/2014 / Rollo 793/2012 only. This does not establish participation in any other appeal, vote beyond the signed panel act, knowledge, wrongdoing or liability.'}
 ]}
people_path.write_text(json.dumps(people,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

inst_path=ROOT/'assets/data/matter-identity-registry-v1.historic-arrecife-judicial-institutions-20260902.json'
inst={'schema':'por-derecho.matter-identity-registry.part.v1','registry_id':'PD-SP-IDENTITY-REGISTRY-001','type':'INSTITUTION','scope':'Historic Arrecife courts source-identified in the 2-Sep-2026 backfill','records':[
 {'id':'PD-SP-I-0045','type':'INSTITUTION','name':'Juzgado de Instrucción nº 3 de Arrecife (antiguo Mixto nº 8)','aliases':['Juzgado de Instruccion nº 3 de Arrecife','Antiguo Mixto nº 8 de Arrecife'],'routes':{'es':'/es/registro-autoridad-historica-arrecife/#pd-sp-i-0045','en':'/en/historic-arrecife-justice-authority-register/#pd-sp-i-0045'},'identity_resolution':'CARET_CONFIRMED','identity_sources':['Sentencia 39/2011 P.O. 467/2010 primary judicial copy'],'identity_boundary':'Historic organ identity as printed on the source. The civil function in P.O. 467/2010 does not establish present successor allocation.'},
 {'id':'PD-SP-I-0046','type':'INSTITUTION','name':'Juzgado de Primera Instancia nº 4 de Arrecife','aliases':['JPI nº 4 de Arrecife'],'routes':{'es':'/es/registro-autoridad-historica-arrecife/#pd-sp-i-0046','en':'/en/historic-arrecife-justice-authority-register/#pd-sp-i-0046'},'identity_resolution':'CARET_CONFIRMED','identity_sources':['Sentencia 89/2014 / Rollo 793/2012 identifies origin JPI nº4 and Juicio Verbal 1260/2011'],'identity_boundary':'Historic first-instance organ identity only; the appellate copy does not identify the first-instance Judge or LAJ.'},
 {'id':'PD-SP-I-0047','type':'INSTITUTION','name':'Juzgado de Instrucción nº 4 de Arrecife','aliases':['JI nº 4 de Arrecife'],'routes':{'es':'/es/registro-autoridad-historica-arrecife/#pd-sp-i-0047','en':'/en/historic-arrecife-justice-authority-register/#pd-sp-i-0047'},'identity_resolution':'CARET_CONFIRMED','identity_sources':['DP 3017/2014 citation dated 14-Oct-2014, primary judicial copy'],'identity_boundary':'Historic criminal-investigation organ identity for the cited source. The citation does not identify Judge or LAJ.'}
]}
inst_path.write_text(json.dumps(inst,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# Update CAEPR index only; new proceedings remain canonically governed by Master Proceedings IDs.
reg=json.loads(REG.read_text(encoding='utf-8'))
existing_ids=set()
for part in reg['parts']:
    p=ROOT/'assets/data'/part['path']
    if p.exists():
        try: existing_ids|={x['id'] for x in json.loads(p.read_text(encoding='utf-8')).get('records',[])}
        except Exception: pass
for nid in ['PD-SP-P-0163','PD-SP-P-0164','PD-SP-I-0045','PD-SP-I-0046','PD-SP-I-0047']:
    if nid in existing_ids: raise SystemExit(f'ID collision {nid}')
reg['required_names'] if False else None
required=reg['coverage']['required_names']
for n in ['Ángela López-Yuste Padial','Emma Galcerán Solsona','Juzgado de Instrucción nº 3 de Arrecife (antiguo Mixto nº 8)','Juzgado de Primera Instancia nº 4 de Arrecife','Juzgado de Instrucción nº 4 de Arrecife']:
    if n not in required: required.append(n)
reg['counts']['total']+=5; reg['counts']['PERSON']+=2; reg['counts']['INSTITUTION']+=3
reg['parts'].append({'path':people_path.name,'type':'PERSON','count':2})
reg['parts'].append({'path':inst_path.name,'type':'INSTITUTION','count':3})
reg['coverage']['state']='COMPLETE_FOR_CURRENT_CANONICAL_ACTOR_REGISTER_SOURCE_IDENTIFIED_HISTORIC_ARRECIFE_AUTHORITY_BACKFILL_GLOBAL_DOCKET_BACKFILL_OPEN'
REG.write_text(json.dumps(reg,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# Current authority denominator: only newly source-identified people are added; unknown historic office-holders remain explicit gaps.
auth=json.loads(AUTH.read_text(encoding='utf-8'))
auth['person_sources'].append({'path':'assets/data/'+people_path.name,'scope':'Historic Arrecife/AP Las Palmas judges newly source-identified from primary judicial copies on 2-Sep-2026','people':2,'confirmed':2,'pending':0})
auth['derived_counts']['unique_named_people']+=2; auth['derived_counts']['confirmed']+=2; auth['derived_counts']['by_role']['JUDGE_OR_MAGISTRATE']+=2
auth['status']='CURRENT_DERIVED_REGISTER_LIVE_RELEASE_HISTORIC_ARRECIFE_SOURCE_BACKFILL_GLOBAL_HISTORIC_DOCKET_BACKFILL_OPEN'
AUTH.write_text(json.dumps(auth,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# Explicit proceeding -> authority coverage. SOURCE_GAP is a first-class state, never a silent blank.
refs=['Procedimiento Ordinario 467/2010','Juicio Verbal 1260/2011','Rollo 793/2012','DP 3017/2014','DP 168/2015','DP 2084/2016','Rollo 526/2013','Procedimiento Ordinario 1241/2011','Medidas cautelares 1355/2011','Procedimiento Ordinario 562/2014','Procedimiento Ordinario 213/2015','Juicio Verbal 268/2016','DP 332/2014','DP 1132/2018','Rollo 1010/2018','Diligencias Preliminares 1041/2017','273/2013','302/2018','49/2018','92/2012']
# tolerant matching aliases for existing Master references
aliases={'Procedimiento Ordinario 1241/2011':'P.O. 1241/2011','Medidas cautelares 1355/2011':'Medidas cautelares 1355/2011','Procedimiento Ordinario 562/2014':'P.O. 562/2014','Procedimiento Ordinario 213/2015':'P.O. 213/2015'}
def lookup(ref):
    for r in rows:
        if r['Reference']==ref or r['Reference']==aliases.get(ref): return r
    return None
cov=[]
for ref in refs:
    r=lookup(ref)
    if not r: continue
    item={'master_id':r['Master_ID'],'reference':r['Reference'],'nig':r['NIG'],'court_or_fiscalia':r['Origin_Organ'],'judge_or_magistrate':{'state':'SOURCE_GAP','person_ids':[]},'laj':{'state':'SOURCE_GAP','person_ids':[]},'fiscal':{'state':'NOT_APPLICABLE_OR_SOURCE_GAP','person_ids':[]},'source_status':r['Source_Status'],'open_gap':r['Open_Reference_Gap']}
    if r['Master_ID']=='LZ-CIV-045': item['judge_or_magistrate']={'state':'SOURCE_IDENTIFIED','person_ids':['PD-SP-P-0163'],'act':'Sentencia 39/2011','date':'2011-03-14'}
    if r['Master_ID']=='LZ-APP-046': item['judge_or_magistrate']={'state':'SOURCE_IDENTIFIED_PANEL','person_ids':['PD-SP-P-0164','PD-SP-P-0130','PD-SP-P-0129'],'act':'Sentencia 89/2014','date':'2014-01-13','roles':{'PD-SP-P-0164':'Presidenta','PD-SP-P-0130':'Magistrada','PD-SP-P-0129':'Magistrado ponente'}}
    if r['Master_ID']=='LZ-APP-004': item['judge_or_magistrate']={'state':'SOURCE_IDENTIFIED_PANEL','person_ids':['PD-SP-P-0096','PD-SP-P-0097','PD-SP-P-0098'],'act':'Auto 804/2018','date':'2018-11-13'}
    cov.append(item)
coverage={'schema':'por-derecho.proceeding-justice-authority-coverage.v1','control_id':'PD-SP-PROCEEDING-AUTHORITY-BACKFILL-20260902-01','control_date':'2026-09-02','status':'SOURCE_IDENTIFIED_EDGES_PLUS_EXPLICIT_GAPS','completion_boundary':'This backfill covers the recovered historical inventory denominator only. SOURCE_GAP means the current controlled source does not identify the office-holder and no inference is permitted.','records':cov}
(ROOT/'assets/data/proceeding-justice-authority-coverage-20260902.json').write_text(json.dumps(coverage,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# Bilingual public page: searchable people/institutions plus proceeding/gap matrix.
def page(lang):
    es=lang=='es'; title='Registro histórico de autoridad judicial — Arrecife' if es else 'Historic justice-authority register — Arrecife'
    intro=('Backfill de 2 de septiembre de 2026. Distingue identidad fuente-confirmada y huecos documentales; un hueco nunca se completa por inferencia.' if es else '2 September 2026 backfill. It distinguishes source-confirmed identity from documentary gaps; a gap is never filled by inference.')
    rows_html=''.join(f"<tr id='{x['master_id'].lower()}'><td><code>{x['master_id']}</code></td><td>{x['reference']}</td><td>{x['court_or_fiscalia']}</td><td>{', '.join(x['judge_or_magistrate']['person_ids']) or 'SOURCE_GAP'}</td><td>{', '.join(x['laj']['person_ids']) or 'SOURCE_GAP'}</td></tr>" for x in cov)
    names=[('pd-sp-p-0163','PD-SP-P-0163 ^','Ángela López-Yuste Padial','Sentencia 39/2011 · P.O. 467/2010'),('pd-sp-p-0164','PD-SP-P-0164 ^','Emma Galcerán Solsona','Sentencia 89/2014 · Rollo 793/2012'),('pd-sp-i-0045','PD-SP-I-0045 ^','Juzgado de Instrucción nº 3 de Arrecife (antiguo Mixto nº 8)','P.O. 467/2010'),('pd-sp-i-0046','PD-SP-I-0046 ^','Juzgado de Primera Instancia nº 4 de Arrecife','Juicio Verbal 1260/2011'),('pd-sp-i-0047','PD-SP-I-0047 ^','Juzgado de Instrucción nº 4 de Arrecife','DP 3017/2014')]
    cards=''.join(f"<article class='card' id='{a}'><h2>{c}</h2><p><code>{b}</code></p><p>{d}</p></article>" for a,b,c,d in names)
    return f"<!doctype html><html lang='{lang}'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>{title} · Por Derecho</title><link rel='stylesheet' href='../../assets/site.css'></head><body><header class='site-header'><div class='shell'><a href='../'>Por Derecho</a></div></header><main><section class='section'><div class='shell'><p class='eyebrow'>CAEPR · MASTER PROCEEDINGS · 02-SEP-2026</p><h1>{title}</h1><p>{intro}</p><p><a href='../registro-maestro-procedimientos/'>{'Registro Maestro de Procedimientos' if es else 'Master Proceedings Register'}</a></p></div></section><section class='section'><div class='shell grid'>{cards}</div></section><section class='section'><div class='shell'><h2>{'Cobertura procedimiento → autoridad' if es else 'Proceeding → authority coverage'}</h2><div class='table-wrap'><table><thead><tr><th>Master ID</th><th>{'Referencia' if es else 'Reference'}</th><th>{'Órgano' if es else 'Court/office'}</th><th>{'Juez/Magistrado' if es else 'Judge/Magistrate'}</th><th>LAJ</th></tr></thead><tbody>{rows_html}</tbody></table></div></div></section></main><script src='../../assets/site.js'></script></body></html>"
for lang,path in [('es',ROOT/'es/registro-autoridad-historica-arrecife/index.html'),('en',ROOT/'en/historic-arrecife-justice-authority-register/index.html')]:
    path.parent.mkdir(parents=True,exist_ok=True); path.write_text(page(lang),encoding='utf-8')

# Reconcile unitary count surfaces previously gated by exact canonical totals.
for path in [ROOT/'ops/CURRENT_UNITARY_STATE.json', ROOT/'scripts/validate_operational_truth.py', ROOT/'scripts/validate_current_reverse_engineered_digest.py', ROOT/'scripts/validate_dp3205_2014_publication.py', ROOT/'es/registro-identidad-materia/index.html', ROOT/'en/matter-identity-registry/index.html']:
    if not path.exists(): continue
    s=path.read_text(encoding='utf-8')
    s=s.replace('343','348').replace('162 personas','164 personas').replace('162 people','164 people').replace('PERSON: 162','PERSON: 164').replace('"PERSON": 162','"PERSON": 164').replace('44 instituciones','47 instituciones').replace('44 institutions','47 institutions').replace('INSTITUTION: 44','INSTITUTION: 47').replace('"INSTITUTION": 44','"INSTITUTION": 47')
    path.write_text(s,encoding='utf-8')

# Machine smoke assertions for exactly the newly searchable denominator.
pub=json.loads(PUBLIC.read_text(encoding='utf-8'))
hay='\n'.join(json.dumps(x,ensure_ascii=False) for x in pub['records'])
for q in ['Procedimiento Ordinario 467/2010','3500441120100004798','Rollo 793/2012','DP 3017/2014','3500443220140012080','DP 2084/2016','Rollo 526/2013','Diligencias Preliminares 1041/2017','273/2013','302/2018','49/2018','92/2012']:
    assert q in hay, q
reg2=json.loads(REG.read_text(encoding='utf-8')); assert reg2['counts']=={'total':348,'PERSON':164,'ORGANISATION':83,'STRUCTURE':11,'INSTITUTION':47,'PROCEEDING':43}
print('BACKFILL_OK',len(rows),len(pub['records']),reg2['counts'],len(cov))
