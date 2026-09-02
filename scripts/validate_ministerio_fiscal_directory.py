#!/usr/bin/env python3
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT / 'assets/data/ministerio-fiscal-directory-v1.json'
COMMUNICATIONS = ROOT / 'assets/data/institutional-communications-register-v1.json'
MASTER = ROOT / 'archive/PROCEEDINGS_MASTER_REGISTER.csv'
PAGES = [
    ROOT / 'es/ministerio-fiscal/index.html',
    ROOT / 'en/ministerio-fiscal/index.html',
    ROOT / 'es/ministerio-fiscal/oficinas/index.html',
    ROOT / 'en/ministerio-fiscal/offices/index.html',
]

def require(cond, message):
    if not cond:
        raise SystemExit(f'FAIL: {message}')

def unique(values, label):
    vals = list(values)
    require(len(vals) == len(set(vals)), f'duplicate {label}')

def main():
    d = json.loads(DIRECTORY.read_text(encoding='utf-8'))
    c = json.loads(COMMUNICATIONS.read_text(encoding='utf-8'))
    with MASTER.open(encoding='utf-8', newline='') as fh:
        master_rows = list(csv.DictReader(fh))
    office_ids = [o['canonical_id'] for o in d['offices']]
    unique(office_ids, 'PD-MF office directory ID')
    require(all(re.fullmatch(r'PD-MF-OFF-\d{4}', x) for x in office_ids), 'office directory ID format')
    office_set = set(office_ids)
    master_ids = [f['master_id'] for f in d['expedientes']]
    unique(master_ids, 'directory expediente Master_ID')
    master_register_ids = {r['Master_ID'] for r in master_rows}
    require(not sorted(set(master_ids) - master_register_ids), 'directory Master_ID missing from master register')
    for f in d['expedientes']:
        require(set(f.get('office_ids', [])) <= office_set, f'unknown office ID in {f["master_id"]}')
        caret = f.get('caret_id')
        if caret:
            require(re.fullmatch(r'PD-SP-R-\d{4}', caret), f'bad CAEPR/caret ID format in {f["master_id"]}')
    events = c.get('events', [])
    event_ids = [e.get('event_id') for e in events]
    require(all(event_ids), 'every communications row must have event_id')
    unique(event_ids, 'PD-SP-EVT event ID')
    require(all(re.fullmatch(r'PD-SP-EVT-\d{4}', x) for x in event_ids), 'event ID format')
    require(not any(x.startswith('REGAGE') for x in event_ids), 'event IDs must remain separate from REGAGE')
    baseline = [e for e in events if e.get('cohort') == 'BASELINE_REDSARA_ANEXO4_75' and e.get('record_type') == 'REGISTRATION_RECEIPT']
    require(len(baseline) == d['coverage_baseline']['detailed_redsara_receipts_source_proved'], f'baseline receipt mismatch: {len(baseline)}')
    refs = [e.get('official_reference') for e in baseline]
    require(all(r and r.startswith('REGAGE') for r in refs), 'baseline receipt must retain REGAGE official reference')
    unique(refs, 'baseline REGAGE reference')
    require(all(e['event_id'] != e['official_reference'] for e in baseline), 'canonical event ID must not equal REGAGE reference')
    inbound = [e for e in events if e.get('direction') == 'INBOUND_FROM_INSTITUTION']
    require(inbound, 'no inbound institution events found')
    require(all(e.get('event_id') for e in inbound), 'every inbound response/transport row must carry a unique canonical event ID')
    require(d['coverage_baseline']['universal_historical_completeness_claim'] is False, 'directory must not claim universal historical completeness')
    for page in PAGES:
        text = page.read_text(encoding='utf-8')
        require('ministerio-fiscal-directory-20260902.js' in text, f'missing directory renderer on {page}')
        require('institutional-communications-register-v1.json' in text, f'missing canonical communications source on {page}')
    print('PASS: Ministerio Fiscal canonical directory')
    print(f'  offices: {len(office_ids)} unique PD-MF-OFF IDs')
    print(f'  expedientes: {len(master_ids)} reconciled Master_ID rows')
    print(f'  communications events: {len(events)} unique PD-SP-EVT IDs')
    print(f'  detailed RedSARA receipts: {len(baseline)} with separate REGAGE + PD-SP-EVT identities')
    print(f'  inbound institution events: {len(inbound)} uniquely event-registered')

if __name__ == '__main__':
    main()
