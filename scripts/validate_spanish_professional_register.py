#!/usr/bin/env python3
"""Validate the Spanish counsel, professional adviser and participant register."""
from __future__ import annotations
import json, re, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'assets'/'data'
EMAIL_RE=re.compile(r'\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b',re.I)

def load(path:Path):
    try:return json.loads(path.read_text(encoding='utf-8'))
    except Exception as exc:raise AssertionError(f'Cannot parse {path.relative_to(ROOT)}: {exc}')
def req(cond,msg):
    if not cond:raise AssertionError(msg)

def main()->int:
  try:
    index=load(DATA/'matter-identity-registry-v1.json')
    req(index.get('counts',{}).get('total')==188,'Registry total must be 188')
    req(index.get('counts',{}).get('PERSON')==87,'Person count must be 87')
    req(index.get('counts',{}).get('ORGANISATION')==68,'Organisation count must be 68')
    records={}
    for part in index['parts']:
      payload=load(DATA/part['path'])
      req(len(payload.get('records',[]))==part['count'],f"Count mismatch in {part['path']}")
      for record in payload['records']:
        req(record['id'] not in records,f"Duplicate ID {record['id']}")
        records[record['id']]=record
    reg=load(DATA/'spanish-counsel-professional-owner-register-v1.json')
    req(reg.get('control_id')=='PD-SP-SPANISH-PROFESSIONAL-REGISTER-001','Wrong professional control ID')
    people=reg.get('records',[]); req(isinstance(people,list) and people,'Professional records missing')
    seen=set()
    allowed_categories={
      'CURRENT_SPANISH_COUNSEL','FORMER_SPANISH_COUNSEL','SPANISH_LEGAL_CONTACT_SCOPE_REVIEW','PROCURADOR',
      'OTHER_LAWYER_IN_MATTER','REPRESENTATIVE_IN_MATTER','OTHER_PROFESSIONAL_ADVISER','HOTEL_RECOVERY_PROFESSIONAL',
      'COMMUNITY_ORGAN_ACTOR','HISTORICAL_OWNER_COMMUNITY_PARTICIPANT','LATER_CORPORATE_PROJECT_OFFICER','HISTORICAL_CORPORATE_OFFICER'
    }
    for item in people:
      pid=item.get('id'); req(pid in records,f'Unknown professional record ID {pid}')
      req(pid not in seen,f'Duplicate professional record {pid}'); seen.add(pid)
      req(records[pid]['type']=='PERSON',f'Non-person in professional records: {pid}')
      req(item.get('category') in allowed_categories,f"Invalid category for {pid}: {item.get('category')}")
      for field in ('public_name','classification','display_state','evidence_status','role_es','role_en','boundary_es','boundary_en'):
        req(isinstance(item.get(field),str) and item[field].strip(),f'{pid}.{field} missing')
      req(not EMAIL_RE.search(json.dumps(item,ensure_ascii=False)),f'Private email leaked in {pid}')
      if item.get('firm_id'): req(item['firm_id'] in records and records[item['firm_id']]['type']=='ORGANISATION',f"Unknown firm ID for {pid}: {item['firm_id']}")
      req('uk lawyer' not in item['role_en'].casefold(),f'UK lawyer included in Spanish register: {pid}')
    current={i['public_name'] for i in people if i['category']=='CURRENT_SPANISH_COUNSEL'}
    req(current=={'Javier Sixto-Seijas','Estefanía Sixto Seijas','Carlos Llamas Sanz','Adriana Hernández Díaz'},f'Current team mismatch: {sorted(current)}')
    owners={'PD-SP-P-0015','PD-SP-P-0016','PD-SP-P-0017','PD-SP-P-0019','PD-SP-P-0020','PD-SP-P-0021','PD-SP-P-0022','PD-SP-P-0024','PD-SP-P-0025','PD-SP-P-0026','PD-SP-P-0027','PD-SP-P-0028','PD-SP-P-0030','PD-SP-P-0031','PD-SP-P-0032','PD-SP-P-0034'}
    req(owners.issubset(seen),f'Missing requested owner/community IDs: {sorted(owners-seen)}')
    requested_new={f'PD-SP-P-{n:04d}' for n in range(67,88)}
    req(requested_new.issubset(records),f'Missing new canonical IDs: {sorted(requested_new-set(records))}')
    for entity in reg.get('hotel_operator_entities',[]):
      req(entity.get('id') in records and records[entity['id']]['type']=='ORGANISATION',f"Unknown hotel/operator entity {entity.get('id')}")
      req(entity.get('capacity_es') and entity.get('capacity_en'),f"Missing bilingual entity capacity {entity.get('id')}")
    withdrawn={x.get('id'):x for x in reg.get('private_or_withdrawn_legal_registry_records',[])}
    req(set(withdrawn)=={'PD-SP-P-0065','PD-SP-P-0066'},'Transaction-only withdrawal set mismatch')
    req(all(x.get('classification')=='T_TRANSACTION_ONLY' and x.get('display_state')=='WITHDRAWN_PUBLIC' for x in withdrawn.values()),'Withdrawal classification mismatch')
    overrides=reg.get('canonical_name_overrides',{})
    expected_overrides={'PD-SP-P-0052':'Miguel Méndez Itarte','PD-SP-P-0054':'Zulay Carmen Rodríguez Cabrera','PD-SP-P-0060':'Javier Sixto-Seijas','PD-SP-P-0061':'Estefanía Sixto Seijas','PD-SP-P-0063':'Daniel Irigoyen Fujiwara'}
    req(overrides==expected_overrides,'Canonical display overrides mismatch')
    for item in reg.get('consulted_or_proposal_only_not_former_counsel',[]):
      req('retained' not in item.get('status','').casefold(),f"Proposal-only record misclassified: {item.get('label')}")
      req(item.get('boundary_es') and item.get('boundary_en'),'Proposal-only boundary missing')
    surface_checks={
      ROOT/'es/registro-identidad-materia/abogados-espanoles/index.html':['PD-SP-SPANISH-PROFESSIONAL-REGISTER-001','Abogados españoles, asesores y participantes','data-spanish-professional-register'],
      ROOT/'en/matter-identity-registry/spanish-lawyers/index.html':['PD-SP-SPANISH-PROFESSIONAL-REGISTER-001','Spanish lawyers, advisers and matter participants','data-spanish-professional-register'],
      ROOT/'assets/spanish-professional-register.js':['CURRENT_SPANISH_COUNSEL','renderRecords','hotel_operator_entities'],
      ROOT/'assets/spanish-professional-register.css':['.spr-grid','.spr-card','.spr-privacy'],
      ROOT/'assets/spanish-professional-registry-integration-20260825.js':['Javier Sixto-Seijas','PD-SP-P-0065','withdrawn-transaction-only'],
      ROOT/'sitemap-spanish-professional-register.xml':['abogados-espanoles','spanish-lawyers'],
      ROOT/'robots.txt':['sitemap-spanish-professional-register.xml'],
      ROOT/'.github/governance/PERSON_IDENTITY_ADMISSION_PRIVACY_AND_PUBLICATION_RULE.md':['PD-SP-IDENTITY-PRIVACY-001','UK lawyers are excluded']
    }
    for path,markers in surface_checks.items():
      req(path.is_file(),f'Missing surface {path.relative_to(ROOT)}')
      text=path.read_text(encoding='utf-8')
      for marker in markers:req(marker in text,f"Missing marker {marker!r} in {path.relative_to(ROOT)}")
  except AssertionError as exc:
    print(f'SPANISH PROFESSIONAL REGISTER: FAIL\n - {exc}',file=sys.stderr);return 1
  print('SPANISH PROFESSIONAL REGISTER: PASS')
  print(f' - canonical identities: {len(records)}')
  print(f' - classified people: {len(people)}')
  print(f" - current counsel: {sum(1 for i in people if i['category']=='CURRENT_SPANISH_COUNSEL')}")
  print(f" - former counsel: {sum(1 for i in people if i['category']=='FORMER_SPANISH_COUNSEL')}")
  print(f" - owners/community: {sum(1 for i in people if i['category'] in {'COMMUNITY_ORGAN_ACTOR','HISTORICAL_OWNER_COMMUNITY_PARTICIPANT'})}")
  return 0
if __name__=='__main__':raise SystemExit(main())