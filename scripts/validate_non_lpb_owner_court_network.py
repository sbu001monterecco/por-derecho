#!/usr/bin/env python3
from __future__ import annotations
import json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'assets'/'data'
def load(p): return json.loads(p.read_text(encoding='utf-8'))
def req(c,m):
    if not c: raise AssertionError(m)
def main():
  try:
    idx=load(DATA/'matter-identity-registry-v1.json'); records={}
    for part in idx['parts']:
      payload=load(DATA/part['path']); req(len(payload['records'])==part['count'],f"count mismatch {part['path']}")
      for r in payload['records']:
        req(r['id'] not in records,f"duplicate ID {r['id']}"); records[r['id']]=r
    req(idx['counts']['total']==187 and idx['counts']['PERSON']==88 and idx['counts']['ORGANISATION']==66,'canonical counts mismatch')
    req(records['PD-SP-P-0087']['name']=='Gerardo Zacarías Acosta Matos','P0087 identity mismatch')
    req(records['PD-SP-P-0088']['name']=='Javier Acosta Matos','P0088 identity mismatch')
    net=load(DATA/'non-lpb-matkator-owner-court-network-v1.json'); req(net['control_id']=='PD-SP-OWNER-COURT-NETWORK-001','wrong control ID')
    layers={x['layer_id']:x for x in net['layers']}; req(len(layers)==7,'expected seven evidence layers')
    for layer in layers.values():
      for rid in layer.get('members',[]): req(rid in records,f"unknown member {rid} in {layer['layer_id']}")
      if layer.get('counsel'): req(layer['counsel'] in records,f"unknown counsel {layer['counsel']}")
    ap=set(layers['L1_JV1260_AP89_CLAIMANTS']['members'])
    expected={'PD-SP-O-0015','PD-SP-O-0011','PD-SP-O-0012','PD-SP-O-0009','PD-SP-O-0010','PD-SP-P-0025','PD-SP-P-0020'}
    req(ap==expected,f'AP89 claimant-owner core mismatch: {sorted(ap)}')
    family=set(layers['L7_LATER_ACOSTA_MATOS_FAMILY_BUSINESS']['members'])
    req({'PD-SP-P-0011','PD-SP-P-0012','PD-SP-P-0087','PD-SP-P-0088'}.issubset(family),'Acosta Matos family/business cluster incomplete')
    edge_ids=set(); edge_by_relation={}
    for e in net['edges']:
      req(e['id'] not in edge_ids,f"duplicate edge {e['id']}"); edge_ids.add(e['id'])
      req(e['from'] in records or e['from'] in layers,f"unknown source {e['from']}"); req(e['to'] in records or e['to'] in layers,f"unknown target {e['to']}")
      edge_by_relation.setdefault(e['relation'],[]).append(e)
    req(len(edge_ids)==20,'expected 20 typed edges')
    req(any(e['from']=='PD-SP-P-0027' for e in edge_by_relation.get('SPECIFIC_VOTE_PROPOSITION_IN_COMPLAINANT_RECONSTRUCTION',[])),'Celia vote edge missing')
    req(any(e['from']=='PD-SP-P-0031' for e in edge_by_relation.get('PRESENT_AND_REQUESTED_EXPLANATION_OF_DEBT_BALANCES',[])),'Manuel debt edge missing')
    text=json.dumps(net,ensure_ascii=False)
    for forbidden in ['Josep Ponsirenas','Oriol Huguet','José Miguel Molina Petit','Anastasio Molina López','Lourdes Moreno']:
      req(forbidden not in text,f'privacy-gated name leaked: {forbidden}')
    surfaces={
      ROOT/'es/registro-identidad-materia/perimetro-propietarios-no-lpb-matkator/index.html':['PD-SP-OWNER-COURT-NETWORK-001','Los siete actores propietarios','Celia Guillén Pérez','PD-SP-P-0087','PD-SP-P-0088'],
      ROOT/'en/matter-identity-registry/non-lpb-matkator-owner-network/index.html':['PD-SP-OWNER-COURT-NETWORK-001','The seven actors who owned','Celia Guillén Pérez','PD-SP-P-0087','PD-SP-P-0088'],
      ROOT/'assets/owner-court-network.css':['.ocn-layers','.ocn-family','.ocn-highlight-grid'],
      ROOT/'sitemap-owner-court-network.xml':['perimetro-propietarios-no-lpb-matkator','non-lpb-matkator-owner-network'],
      ROOT/'robots.txt':['sitemap-owner-court-network.xml']}
    for p,markers in surfaces.items():
      req(p.is_file(),f'missing {p.relative_to(ROOT)}'); t=p.read_text(encoding='utf-8')
      for m in markers:req(m in t,f"missing {m!r} in {p.relative_to(ROOT)}")
  except AssertionError as e:
    print(f'OWNER COURT NETWORK: FAIL\n - {e}',file=sys.stderr); return 1
  print('OWNER COURT NETWORK: PASS'); print(f' - identities: {len(records)}'); print(' - AP89 claimant-owner core: 7'); print(f' - layers: {len(layers)}; edges: {len(edge_ids)}'); return 0
if __name__=='__main__': raise SystemExit(main())