#!/usr/bin/env python3
import json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
d=json.loads((R/'assets/data/cuatrecasas-wip-reconciliation-v1.json').read_text(encoding='utf-8'))
def fail(x): print('FAIL:',x); sys.exit(1)
cp=d.get('checkpoints',[])
if len(cp)!=4 or len({x['id'] for x in cp})!=4: fail('four unique WIP checkpoints required')
for x in cp:
    if x.get('issued_invoice') or x.get('cash_paid'): fail('WIP/estimate cannot be invoice or paid: '+x['id'])
vals={x['id']:x['amount_eur'] for x in cp}
if round(vals['CUA-WIP-001']+vals['CUA-WIP-002']+vals['CUA-WIP-003'],2)!=152424.95: fail('2019 WIP+estimate total')
if vals['CUA-WIP-004']!=161738.75: fail('2020 work carried out')
h=d['headline_reconciliations']
if h['headline_delta_eur']!=9313.80 or h['2020_unpaid_issued_invoices_eur']!=136830.72: fail('headline controls')
if h['2020_two_stated_components_before_vat_eur']!=298569.47 or h['mechanical_21pct_if_applied_eur']!=361269.06: fail('2020 arithmetic controls')
p=d['partial_invoice_bridge']
if round(p['accrued_work_stated_eur']-p['issued_invoice_face_eur'],2)!=67492.50: fail('partial invoice remainder')
if round(p['mechanical_unbilled_remainder_eur']-p['2019_row_2018_works_to_be_invoiced_eur'],2)!=6087.55: fail('2018 WIP delta')
i=d['instrument_bridge']
if round(i['issued_invoices_unpaid_2019_eur']+i['proformas_total_eur'],2)!=i['claim_1_principal_eur']: fail('claim 1 bridge')
if i['wip_to_pagare_mapping']!='OPEN' or i['single_satisfaction_status']=='PROVED_COMPLETE': fail('open bridge required')
q=d['quarterly_control']
if 'NOT CUATRECASAS-AUTHORED' not in q['publication_label'] or q['author_class']!='ADMINISTRACION_CONCURSAL_THIRD_PARTY': fail('quarterly authorship guard')
g={x['id']:x for x in d['gaps']}
if g['ME-083']['current_status']!='PARTIALLY_CLOSED_2026-09-13': fail('ME-083 correction')
public=''.join((R/p).read_text(encoding='utf-8') for p in ['assets/data/cuatrecasas-wip-reconciliation-v1.json','en/cuatrecasas-wip-unbilled/index.html','es/cuatrecasas-wip-no-facturado/index.html']).lower()
for bad in ('mail.google','link_6a9','gmail message id','iban','swift','@cuatrecasas'):
    if bad in public: fail('private pattern '+bad)
for page,markers in [('en/cuatrecasas-wip-unbilled/index.html',['€161,738.75','€9,313.80','€6,087.55']),('es/cuatrecasas-wip-no-facturado/index.html',['161.738,75 EUR','9.313,80 EUR','6.087,55 EUR'])]:
    s=(R/page).read_text(encoding='utf-8')
    for m in markers:
        if m not in s: fail(page+' missing '+m)
print('PASS: Cuatrecasas WIP/unbilled reconciliation')
