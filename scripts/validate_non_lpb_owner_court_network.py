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
      for r in load(DATA/part['path'])['records']: records[r['id']]=r
    net=load(DATA/'non-lpb-matkator-owner-court-network-v1.json')
    req(net.get('control_id')=='PD-SP-OWNER-COURT-NETWORK-001','wrong control ID')
    layers={x['layer_id']:x for x in net['layers']}; req(len(layers)==len(net['layers']),'duplicate layer IDs')
    for layer in net['layers']:
      for rid in layer.get('members',[]): req(rid in records,f"unknown member {rid} in {layer['layer_id']}")
      if layer.get('counsel'): req(layer['counsel'] in records,f"unknown counsel {layer['counsel']}")
    edge_ids=set()
    for e in net['edges']:
      req(e['id'] not in edge_ids,f"duplicate edge {e['id']}"); edge_ids.add(e['id'])
      req(e['from'] in records or e['from'] in layers,f"unknown edge source {e['from']}")
      req(e['to'] in records or e['to'] in layers,f"unknown edge target {e['to']}")
    ap=set(layers['L1_JV1260_AP89_CLAIMANTS']['members'])
    expected={'PD-SP-O-0015','PD-SP-O-0011','PD-SP-O-0012','PD-SP-O-0009','PD-SP-O-0010','PD-SP-P-0025','PD-SP-P-0020'}
    req(ap==expected,f'AP89 claimant set mismatch: {sorted(ap)}')
    req('PD-SP-P-0027' in {e['from'] for e in net['edges'] if 'VOTE' in e['relation']},'Celia vote edge missing')
    req('PD-SP-P-0031' in {e['from'] for e in net['edges'] if 'DEBT_BALANCES' in e['relation']},'Manuel debt-explanation edge missing')
    family=set(layers['L7_LATER_ACOSTA_MATOS_FAMILY_BUSINESS']['members'])
    req({'PD-SP-P-0011','PD-SP-P-0012','PD-SP-P-0075','PD-SP-P-0076'}.issubset(family),'Acosta Matos family/business cluster incomplete')
    text=json.dumps(net,ensure_ascii=False)
    for forbidden in ['Josep Ponsirenas','Oriol Huguet','José Miguel Molina Petit','Anastasio Molina López','Lourdes Moreno']:
      req(forbidden not in text,f'privacy-gated name leaked into public network: {forbidden}')
    surfaces={
      ROOT/'es/registro-identidad-materia/perimetro-propietarios-no-lpb-matkator/index.html':['PD-SP-OWNER-COURT-NETWORK-001','Los siete propietarios/demandantes','Celia Guillén Pérez','Gerardo Zacarías Acosta Matos'],
      ROOT/'en/matter-identity-registry/non-lpb-matkator-owner-network/index.html':['PD-SP-OWNER-COURT-NETWORK-001','The seven owners/claimants','Celia Guillén Pérez','Gerardo Zacarías Acosta Matos'],
      ROOT/'assets/owner-court-network.css':['.ocn-layers','.ocn-family','.ocn-highlight-grid'],
      ROOT/'sitemap-spanish-professional-register.xml':['perimetro-propietarios-no-lpb-matkator','non-lpb-matkator-owner-network'],
      ROOT/'assets/spanish-professional-registry-integration-20260825.js':['Owner/court network','Red propietarios/autos']
    }
    for p,markers in surfaces.items():
      req(p.is_file(),f'missing {p.relative_to(ROOT)}'); t=p.read_text(encoding='utf-8')
      for m in markers:req(m in t,f"missing marker {m!r} in {p.relative_to(ROOT)}")
  except AssertionError as e:
    print(f'OWNER COURT NETWORK: FAIL\n - {e}',file=sys.stderr); return 1
  print('OWNER COURT NETWORK: PASS')
  print(f" - canonical identities available: {len(records)}")
  print(f" - evidence layers: {len(layers)}")
  print(f" - typed connections: {len(edge_ids)}")
  print(' - AP89 claimant-owner core: 7')
  return 0
if __name__=='__main__': raise SystemExit(main())