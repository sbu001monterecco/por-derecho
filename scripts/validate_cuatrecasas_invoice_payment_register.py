#!/usr/bin/env python3
import json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
d=json.loads((R/"assets/data/cuatrecasas-invoice-payment-register-v1.json").read_text(encoding="utf-8"))
def fail(x): print("FAIL:",x); sys.exit(1)
inv=d.get("invoices",[])
if len(inv)!=22 or len({x[0] for x in inv})!=22: fail("22 unique invoices required")
face=round(sum(x[3] for x in inv),2); settled=round(sum(x[3] for x in inv if x[5]=="S"),2); out=round(sum(x[3] for x in inv if x[5]=="O"),2)
if (face,settled,out)!=(327608.32,190777.60,136830.72): fail((face,settled,out))
if len(d.get("predecessors",[]))!=6: fail("six predecessors required")
if round(sum(x[2] for x in d.get("payments",[])),2)!=175265.52: fail("payment event total")
if d.get('related_registers',{}).get('wip_unbilled')!='/assets/data/cuatrecasas-wip-reconciliation-v1.json': fail('WIP register link required')
if not (R/'assets/data/cuatrecasas-wip-reconciliation-v1.json').exists(): fail('WIP register missing')
pub="".join((R/p).read_text(encoding="utf-8") for p in ["assets/data/cuatrecasas-invoice-payment-register-v1.json","en/cuatrecasas-invoices-payments/index.html","es/cuatrecasas-facturas-pagos/index.html"]).lower()
for bad in ("mail.google","link_6a9","@cuatrecasas","iban","swift"):
    if bad in pub: fail("private pattern "+bad)
for p,m in [("en/cuatrecasas-invoices-payments/index.html","€86,119.03"),("es/cuatrecasas-facturas-pagos/index.html","86.119,03 EUR")]:
    s=(R/p).read_text(encoding="utf-8")
    if m not in s or "data-invoice-ledger" not in s or "cuatrecasas-invoice-viewer" not in s: fail(p)
js=(R/'assets/cuatrecasas-invoice-viewer.js').read_text(encoding='utf-8')
if 'cuatrecasas-wip-unbilled' not in js or 'cuatrecasas-wip-no-facturado' not in js: fail('WIP page link injection')
print("PASS: Cuatrecasas invoice/payment track 2014-end + WIP adjacency")