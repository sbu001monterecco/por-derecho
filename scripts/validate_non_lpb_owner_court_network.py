#!/usr/bin/env python3
"""Validate the non-LPB/Matkator owner and court-party network."""
from __future__ import annotations
import json, re, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'assets'/'data'

def load(path): return json.loads(Path(path).read_text(encoding='utf-8'))
def req(cond,msg):
    if not cond: raise AssertionError(msg)

def main():
  try:
    index=load(DATA/'matter-identity-registry-v1.json')
    counts=index['counts']; req(counts=={'total':187,'PERSON':88,'ORGANISATION':66,'STRUCTURE':10,'INSTITUTION':13,'PROCEEDING':10},f'identity counts drift: {counts}')
    identities={}
    for part in index['parts']:
      payload=load(DATA/part['path']); records=payload.get('records',[]); req(len(records)==part['count'],f"part count mismatch {part['path']}")
      for record in records:
        req(record['id'] not in identities,f"duplicate ID {record['id']}"); identities[record['id']]=record
    req(len(identities)==187,'identity total mismatch')
    req(identities['PD-SP-P-0087']['name']=='Gerardo Zacarías Acosta Matos','Gerardo Z identity mismatch')
    req(identities['PD-SP-P-0088']['name']=='Javier Acosta Matos','Javier identity mismatch')
    req('PD-SP-P-0013' in identities['PD-SP-P-0087'].get('not_same_as',[]),'Gerardo distinction missing')

    network=load(DATA/'non-lpb-matkator-owner-court-network-v1.json')
    req(network.get('control_id')=='PD-SP-OWNER-COURT-NETWORK-001','unexpected network control')
    req(network['counts']['layers']==7,'layer count mismatch')
    req(network['counts']['relationships']==31,'relationship count mismatch')
    req(network['counts']['ap89_claimant_owners']==7 and network['counts']['ap89_bungalows']==18,'AP89 denominator mismatch')
    claimant_ids=[x['id'] for x in network['ap89_claimant_owner_core']]
    expected={'PD-SP-O-0015','PD-SP-O-0011','PD-SP-O-0012','PD-SP-O-0009','PD-SP-O-0010','PD-SP-P-0025','PD-SP-P-0020'}
    req(set(claimant_ids)==expected,'AP89 claimant set must remain exactly seven')
    req(all(i in identities for i in claimant_ids),'unknown claimant ID')
    layer_ids={x['id'] for x in network['layers']}
    edge_ids=set()
    for edge in network['relationships']:
      req(edge['id'] not in edge_ids,f"duplicate edge {edge['id']}"); edge_ids.add(edge['id'])
      req(edge['from'] in identities or edge['from'] in layer_ids,f"unknown edge source {edge['from']}")
      req(edge['to'] in identities or edge['to'] in layer_ids,f"unknown edge target {edge['to']}")
    req({'PD-SP-OCN-E016','PD-SP-OCN-E023','PD-SP-OCN-E027','PD-SP-OCN-E028','PD-SP-OCN-E031'}.issubset(edge_ids),'individualised or identity edges missing')
    family={x['id'] for x in network['acosta_matos_family_business_block']}
    req(family=={'PD-SP-P-0011','PD-SP-P-0012','PD-SP-P-0087','PD-SP-P-0088'},'Acosta Matos block mismatch')
    req(len(network['evidence_program'])==6,'P0 programme must contain six actions')

    forbidden=['Josep Ponsirenas','Oriol Huguet','José Miguel Molina Petit','Anastasio Molina López','Lourdes Moreno']
    public_files=[DATA/'non-lpb-matkator-owner-court-network-v1.json',ROOT/'es/registro-identidad-materia/perimetro-propietarios-no-lpb-matkator/index.html',ROOT/'en/matter-identity-registry/non-lpb-matkator-owner-network/index.html']
    for path in public_files:
      text=path.read_text(encoding='utf-8')
      for name in forbidden:req(name not in text,f'private/unapproved name leaked: {name}')
    surfaces={
      ROOT/'es/registro-identidad-materia/perimetro-propietarios-no-lpb-matkator/index.html':['PD-SP-OWNER-COURT-NETWORK-001','Los siete actores propietarios','Celia Guillén Pérez','Manuel Molina Climent','Gerardo Zacarías Acosta Matos','Javier Acosta Matos'],
      ROOT/'en/matter-identity-registry/non-lpb-matkator-owner-network/index.html':['PD-SP-OWNER-COURT-NETWORK-001','The seven actors who owned','Celia Guillén Pérez','Manuel Molina Climent','Gerardo Zacarías Acosta Matos','Javier Acosta Matos'],
      ROOT/'es/jv1260-ap89-continuidad-cam/index.html':['JV 1260/2011','red canónica'],
      ROOT/'en/jv1260-ap89-cam-continuity/index.html':['JV 1260/2011','canonical owner'],
      ROOT/'sitemap-owner-court-network.xml':['perimetro-propietarios-no-lpb-matkator','non-lpb-matkator-owner-network']}
    for path,markers in surfaces.items():
      req(path.is_file(),f'missing surface {path.relative_to(ROOT)}'); text=path.read_text(encoding='utf-8')
      for marker in markers:req(marker in text,f"missing {marker!r} in {path.relative_to(ROOT)}")
  except AssertionError as exc:
    print(f'NON-LPB OWNER COURT NETWORK: FAIL\n - {exc}',file=sys.stderr); return 1
  print('NON-LPB OWNER COURT NETWORK: PASS')
  print(' - identities: 187; people: 88')
  print(' - AP89 core: 7 claimant-owners / 18 bungalows')
  print(' - relationships: 31; P0 actions: 6')
  print(' - Acosta Matos block: José Daniel / Laura Patricia / Gerardo Zacarías / Javier')
  return 0
if __name__=='__main__': raise SystemExit(main())