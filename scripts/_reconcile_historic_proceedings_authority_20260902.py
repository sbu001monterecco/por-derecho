#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from collections import Counter
import csv
import hashlib
import json
import re
import shutil
import xml.etree.ElementTree as ET

ROOT = Path('.')
DATA = ROOT / 'assets' / 'data'
CSV = ROOT / 'archive' / 'PROCEEDINGS_MASTER_REGISTER.csv'
PUBLIC = DATA / 'proceedings-master-public-v1.json'
REG = DATA / 'matter-identity-registry-v1.json'
AUTH = DATA / 'justice-authority-register-current-v2.json'
COVERAGE = DATA / 'proceeding-justice-authority-coverage-20260902.json'

# 1. Reconcile the duplicate 1041/2017 row against the primary judicial copy.
with CSV.open(encoding='utf-8-sig', newline='') as f:
    reader = csv.DictReader(f)
    fields = reader.fieldnames
    rows = list(reader)
assert fields
rows = [r for r in rows if r['Master_ID'] != 'LZ-CIV-050']
by_id = {r['Master_ID']: r for r in rows}
assert 'GC-CIV-003' in by_id
r = by_id['GC-CIV-003']
r.update({
    'Origin_Organ': 'Juzgado de Primera Instancia nº 2 de Las Palmas de Gran Canaria',
    'Current_Custodian': 'Juzgado de Primera Instancia nº 2 de Las Palmas de Gran Canaria',
    'Reference': 'Diligencias Preliminares 1041/2017',
    'Secondary_Reference': '0001041/2017; Providencia 12/01/2018; IUP LR2017147858',
    'NIG': '3501642120170028407',
    'Date_or_Period': '2017-2018',
    'Connection': 'LPB v Construcciones Acosta Matos — assignment-document disclosure route',
    'Object_or_Purpose': 'Exhibition and complete-copy production of the 20-Oct-2017 credit-assignment deed and economic terms',
    'Status': 'Primary 12-Jan-2018 Providencia located; complete docket and later closure sequence remain incomplete',
    'Latest_Known_Event': '12-Jan-2018 Providencia fixed 19-Feb-2018 exhibition; electronic signatures identify Judge and LAJ',
    'Source_Status': 'VERIFIED_PRIMARY_COPY',
    'Primary_Source_Anchor': 'LPB - Proc 1041 MATOS debe aportar escritura el 19FEB - 12JAN18.pdf — authentic electronic judicial copy',
    'Repo_Canonical_Source': 'archive/handoffs/2026-09-02-deep-proceedings-authority-email-drive-scan-checkpoint.md',
    'Open_Reference_Gap': 'Preceding signed Auto; complete docket; evidence of 19-Feb-2018 appearance/production; later 5-Mar-2018 decree/closure; service and finality',
    'Public_Treatment': 'PUBLIC_SUMMARY_WITH_PROCEDURAL_LIMITS',
    'Last_Scan_Date': '2026-09-02',
    'Notes': 'Primary copy proves Las Palmas JPI nº2, NIG 3501642120170028407, Magistrado-Juez Juan Avello Formoso and LAJ Fernando Pérez Polo for the cited act. The historical-inventory Arrecife label was erroneous and the duplicate LZ-CIV-050 row is removed.'
})
with CSV.open('w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=fields, lineterminator='\n')
    w.writeheader(); w.writerows(rows)

# 2. Deterministically rebuild the public projection.
old = json.loads(PUBLIC.read_text(encoding='utf-8'))
allow = set(old['publication_policy']['public_treatment_allowlist'])
excluded_allow = set(old['publication_policy'].get('excluded_treatment_values', []))
field_allow = old['field_allowlist']
public_rows = []
excluded = 0
for row in rows:
    treatment = row.get('Public_Treatment', '')
    if treatment in allow:
        public_rows.append({k: row.get(k, '') for k in field_allow})
    elif treatment in excluded_allow:
        excluded += 1
    else:
        raise SystemExit(f'Unknown Public_Treatment {treatment!r} for {row["Master_ID"]}')
old['canonical_source_sha256'] = hashlib.sha256(CSV.read_bytes()).hexdigest()
old['source_record_count'] = len(rows)
old['public_record_count'] = len(public_rows)
old['excluded_record_count'] = excluded
old['records'] = public_rows
PUBLIC.write_text(json.dumps(old, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

# 3. Add the newly source-identified LAJ and exact Las Palmas civil court as immutable CAEPR identities.
person_path = DATA / 'matter-identity-registry-v1.historic-las-palmas-civil-judicial-people-20260902.json'
person_doc = {
    'schema': 'por-derecho.matter-identity-registry.part.v1',
    'registry_id': 'PD-SP-IDENTITY-REGISTRY-001',
    'type': 'PERSON',
    'scope': 'Historic Las Palmas civil judicial office-holders newly source-identified on 2-Sep-2026',
    'records': [{
        'id': 'PD-SP-P-0165', 'type': 'PERSON', 'name': 'Fernando Pérez Polo',
        'aliases': ['Fernando Perez Polo'], 'role': 'LAJ',
        'routes': {'es': '/es/registro-autoridad-historica-las-palmas-civil/#pd-sp-p-0165', 'en': '/en/historic-las-palmas-civil-justice-authority-register/#pd-sp-p-0165'},
        'identity_resolution': 'CARET_CONFIRMED',
        'identity_sources': ['Authentic electronic Providencia in Diligencias Preliminares 1041/2017, signed as Letrado de la Administración de Justicia on 15-Jan-2018'],
        'verification_detail': 'Primary authentic electronic judicial copy identifies the LAJ signatory',
        'capacity_boundary': 'Letrado de la Administración de Justicia signatory of the 12-Jan-2018 Providencia in Diligencias Preliminares 1041/2017, electronic signature timestamp 15-Jan-2018. No authorship or office-holding is inferred for any other act.'
    }]
}
person_path.write_text(json.dumps(person_doc, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

inst_path = DATA / 'matter-identity-registry-v1.historic-las-palmas-civil-judicial-institutions-20260902.json'
inst_doc = {
    'schema': 'por-derecho.matter-identity-registry.part.v1',
    'registry_id': 'PD-SP-IDENTITY-REGISTRY-001',
    'type': 'INSTITUTION',
    'scope': 'Historic Las Palmas civil court source-identified in Diligencias Preliminares 1041/2017',
    'records': [{
        'id': 'PD-SP-I-0048', 'type': 'INSTITUTION',
        'name': 'Juzgado de Primera Instancia nº 2 de Las Palmas de Gran Canaria',
        'aliases': ['JPI nº 2 Las Palmas', 'Juzgado de Primera Instancia número 2 de Las Palmas de Gran Canaria'],
        'routes': {'es': '/es/registro-autoridad-historica-las-palmas-civil/#pd-sp-i-0048', 'en': '/en/historic-las-palmas-civil-justice-authority-register/#pd-sp-i-0048'},
        'identity_resolution': 'CARET_CONFIRMED',
        'identity_sources': ['Authentic electronic Providencia, Diligencias Preliminares 1041/2017, 12-Jan-2018'],
        'identity_boundary': 'Exact historic court identity for the cited proceeding/source. It does not identify the judge or LAJ for every act and does not establish present successor allocation.'
    }]
}
inst_path.write_text(json.dumps(inst_doc, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

# Add explicit roles to current post-census judicial shards so role totals can be derived, not frozen.
role_map = {
    'PD-SP-P-0147':'JUDGE_OR_MAGISTRATE','PD-SP-P-0148':'LAJ','PD-SP-P-0149':'JUDGE_OR_MAGISTRATE',
    'PD-SP-P-0150':'JUDGE_OR_MAGISTRATE','PD-SP-P-0151':'LAJ','PD-SP-P-0152':'LAJ','PD-SP-P-0153':'LAJ',
    'PD-SP-P-0154':'LAJ','PD-SP-P-0155':'LAJ','PD-SP-P-0156':'LAJ','PD-SP-P-0157':'LAJ',
    'PD-SP-P-0163':'JUDGE_OR_MAGISTRATE','PD-SP-P-0164':'JUDGE_OR_MAGISTRATE'
}
for shard_name in ('matter-identity-registry-v1.la-laguna-judicial-people.json', 'matter-identity-registry-v1.historic-arrecife-judicial-people-20260902.json'):
    p = DATA / shard_name
    doc = json.loads(p.read_text(encoding='utf-8'))
    for row in doc.get('records', []):
        if row['id'] in role_map:
            row['role'] = role_map[row['id']]
    p.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

# 4. Reconcile root CAEPR by deriving counts from shards.
reg = json.loads(REG.read_text(encoding='utf-8'))
for desc in (
    {'path': person_path.name, 'type': 'PERSON', 'count': 1},
    {'path': inst_path.name, 'type': 'INSTITUTION', 'count': 1},
):
    current = next((x for x in reg['parts'] if x['path'] == desc['path']), None)
    if current:
        current.update(desc)
    else:
        reg['parts'].append(desc)
for name in ('Fernando Pérez Polo', 'Juzgado de Primera Instancia nº 2 de Las Palmas de Gran Canaria'):
    if name not in reg['coverage']['required_names']:
        reg['coverage']['required_names'].append(name)
counts = Counter()
seen = set()
for part in reg['parts']:
    doc = json.loads((DATA / part['path']).read_text(encoding='utf-8'))
    records = doc.get('records', [])
    assert len(records) == part['count'], part['path']
    for rec in records:
        assert rec['id'] not in seen, rec['id']
        seen.add(rec['id']); counts[rec['type']] += 1
reg['counts'] = {
    'total': sum(counts.values()), 'PERSON': counts['PERSON'], 'ORGANISATION': counts['ORGANISATION'],
    'STRUCTURE': counts['STRUCTURE'], 'INSTITUTION': counts['INSTITUTION'], 'PROCEEDING': counts['PROCEEDING']
}
reg['coverage']['state'] = 'COMPLETE_FOR_CURRENT_CANONICAL_ACTOR_REGISTER_SOURCE_IDENTIFIED_HISTORIC_AUTHORITY_BACKFILL_GLOBAL_DOCKET_BACKFILL_OPEN'
REG.write_text(json.dumps(reg, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

# 5. Recalculate the current justice denominator from source rows and explicit role data.
auth = json.loads(AUTH.read_text(encoding='utf-8'))
new_source = {
    'path': 'assets/data/' + person_path.name,
    'scope': 'Historic Las Palmas civil LAJ newly source-identified from primary Diligencias Preliminares 1041/2017 copy on 2-Sep-2026',
    'people': 1, 'confirmed': 1, 'pending': 0
}
existing_source = next((x for x in auth['person_sources'] if x['path'] == new_source['path']), None)
if existing_source: existing_source.update(new_source)
else: auth['person_sources'].append(new_source)
authority_ids = set(); confirmed = 0; role_counts = Counter()
for source_desc in auth['person_sources']:
    source = json.loads((ROOT / source_desc['path']).read_text(encoding='utf-8'))
    if isinstance(source.get('roles'), dict):
        source_rows = []
        for role, role_rows in source['roles'].items():
            for row in role_rows:
                source_rows.append((row['caepr_id'], row.get('state'), role))
    else:
        source_rows = [(row['id'], row.get('identity_resolution'), row.get('role')) for row in source.get('records', [])]
    ids = {x[0] for x in source_rows}
    assert authority_ids.isdisjoint(ids), source_desc['path']
    authority_ids |= ids
    confirmed += sum(state == 'CARET_CONFIRMED' for _, state, _ in source_rows)
    for _, _, role in source_rows:
        assert role in ('MINISTERIO_FISCAL','JUDGE_OR_MAGISTRATE','LAJ','NOTARY'), (source_desc['path'], role)
        role_counts[role] += 1
    source_desc['people'] = len(source_rows)
    source_desc['confirmed'] = sum(state == 'CARET_CONFIRMED' for _, state, _ in source_rows)
    source_desc['pending'] = sum(state == 'CARET_PENDING' for _, state, _ in source_rows)
assert authority_ids <= seen
pending = len(authority_ids) - confirmed
auth['derived_counts'] = {
    'unique_named_people': len(authority_ids), 'confirmed': confirmed, 'pending': pending, 'suspended': 0,
    'by_role': {role: role_counts[role] for role in ('MINISTERIO_FISCAL','JUDGE_OR_MAGISTRATE','LAJ','NOTARY')}
}
auth['status'] = 'CURRENT_DERIVED_REGISTER_SOURCE_LED_HISTORIC_AUTHORITY_BACKFILL_GLOBAL_DOCKET_BACKFILL_OPEN'
auth['completion_rule'] = f"The current derived {len(authority_ids)}-person denominator is complete only for the presently registered source-identified people. No global all-historic/all-current completeness statement is permitted until every applicable Master Proceedings Register row has populated authority coverage or an explicit source-defined gap and the certified complete docket denominator is closed."
AUTH.write_text(json.dumps(auth, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

# 6. Patch source-bounded proceeding -> authority coverage and institution IDs.
covdoc = json.loads(COVERAGE.read_text(encoding='utf-8'))
covrows = [x for x in covdoc.get('records', []) if x['master_id'] != 'LZ-CIV-050']
by_cov = {x['master_id']: x for x in covrows}
inst_by_mid = {
    'LZ-CIV-045':['PD-SP-I-0045'], 'LZ-CIV-035':['PD-SP-I-0046'], 'LZ-APP-046':['PD-SP-I-0014'],
    'LZ-JUD-047':['PD-SP-I-0047'], 'LZ-REF-038':['PD-SP-I-0047'], 'LZ-JUD-048':['PD-SP-I-0045'],
    'LZ-REF-039':['PD-SP-I-0046'], 'LZ-JUD-002':['PD-SP-I-0045'], 'LZ-JUD-003':['PD-SP-I-0024'],
    'LZ-APP-004':['PD-SP-I-0025'], 'LZ-FIS-049':['PD-SP-I-0020'], 'LZ-FIS-051':['PD-SP-I-0020'],
    'GC-CIV-003':['PD-SP-I-0048']
}
for mid, ids in inst_by_mid.items():
    if mid in by_cov:
        by_cov[mid]['institution_ids'] = ids
if 'GC-CIV-003' not in by_cov:
    by_cov['GC-CIV-003'] = {
        'master_id':'GC-CIV-003','reference':'Diligencias Preliminares 1041/2017','nig':'3501642120170028407',
        'court_or_fiscalia':'Juzgado de Primera Instancia nº 2 de Las Palmas de Gran Canaria','institution_ids':['PD-SP-I-0048'],
        'judge_or_magistrate':{},'laj':{},'fiscal':{},'source_status':'VERIFIED_PRIMARY_COPY','open_gap':r['Open_Reference_Gap']
    }
item = by_cov['GC-CIV-003']
item.update({'reference':'Diligencias Preliminares 1041/2017','nig':'3501642120170028407','court_or_fiscalia':'Juzgado de Primera Instancia nº 2 de Las Palmas de Gran Canaria','institution_ids':['PD-SP-I-0048'],'source_status':'VERIFIED_PRIMARY_COPY','open_gap':r['Open_Reference_Gap']})
item['judge_or_magistrate'] = {'state':'SOURCE_IDENTIFIED','person_ids':['PD-SP-P-0124'],'act':'Providencia','date':'2018-01-12'}
item['laj'] = {'state':'SOURCE_IDENTIFIED','person_ids':['PD-SP-P-0165'],'act':'Providencia (electronic LAJ signature)','date':'2018-01-15'}
item['fiscal'] = {'state':'NOT_APPLICABLE','person_ids':[]}
covdoc['records'] = list(by_cov.values())
covdoc['status'] = 'SOURCE_IDENTIFIED_EDGES_PLUS_EXPLICIT_GAPS_DUPLICATE_1041_RECONCILED'
COVERAGE.write_text(json.dumps(covdoc, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

# 7. Remove stale duplicate page directories and sitemap URLs before deterministic regeneration.
for stale in (ROOT/'es/procedimientos/lz-civ-050', ROOT/'en/proceedings/lz-civ-050'):
    if stale.exists(): shutil.rmtree(stale)
if (ROOT/'sitemap.xml').exists():
    ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    tree = ET.parse(ROOT/'sitemap.xml'); root = tree.getroot(); nsuri = 'http://www.sitemaps.org/schemas/sitemap/0.9'
    for url in list(root):
        loc = url.find(f'{{{nsuri}}}loc') if root.tag.startswith('{') else url.find('loc')
        if loc is not None and loc.text and '/lz-civ-050/' in loc.text: root.remove(url)
    tree.write(ROOT/'sitemap.xml', encoding='utf-8', xml_declaration=True)

# 8. Public authority page for the newly controlled Las Palmas civil act.
def authority_page(lang: str) -> str:
    es = lang == 'es'
    title = 'Autoridad judicial histórica — Diligencias Preliminares 1041/2017' if es else 'Historic justice authority — Diligencias Preliminares 1041/2017'
    body = ('La copia judicial electrónica auténtica de enero de 2018 fija el órgano, NIG y dos firmantes. El registro conserva la atribución por acto y no la extiende a otras actuaciones.' if es else 'The authentic January 2018 electronic judicial copy fixes the court, NIG and two signatories. Attribution is act-specific and is not extended to other acts.')
    proc = '/es/procedimientos/gc-civ-003/' if es else '/en/proceedings/gc-civ-003/'
    master = '/es/registro-maestro-procedimientos/' if es else '/en/master-proceedings-register/'
    other = '/en/historic-las-palmas-civil-justice-authority-register/' if es else '/es/registro-autoridad-historica-las-palmas-civil/'
    return f"""<!doctype html><html lang='{lang}'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>{title} · Por Derecho</title><link rel='stylesheet' href='../../assets/styles.css'><script src='../../assets/site.js' defer></script></head><body><header class='site-header'><div class='shell header-inner'><a class='brand' href='../'>Por Derecho</a><nav class='main-nav'><a href='{master}'>{'Registro Maestro' if es else 'Master Register'}</a><a href='{other}'>{'EN' if es else 'ES'}</a></nav></div></header><main><section class='section'><div class='shell'><p class='eyebrow'>CAEPR · SOURCE-BOUNDED · 02-SEP-2026</p><h1>{title}</h1><p>{body}</p><p><a href='{proc}'><code>GC-CIV-003</code> · Diligencias Preliminares 1041/2017</a></p></div></section><section class='section'><div class='shell grid'><article class='card' id='pd-sp-i-0048'><h2>Juzgado de Primera Instancia nº 2 de Las Palmas de Gran Canaria</h2><p><code>PD-SP-I-0048 ^</code></p><p>NIG 3501642120170028407</p><p><a href='{proc}'>{'Procedimiento vinculado' if es else 'Linked proceeding'}</a></p></article><article class='card' id='pd-sp-p-0124'><h2>Juan Avello Formoso</h2><p><code>PD-SP-P-0124 ^</code> · {'Magistrado-Juez' if es else 'Judge'}</p><p>{'Providencia de 12-ene-2018' if es else 'Order dated 12-Jan-2018'}</p><p><a href='{proc}'>{'Procedimiento vinculado' if es else 'Linked proceeding'}</a></p></article><article class='card' id='pd-sp-p-0165'><h2>Fernando Pérez Polo</h2><p><code>PD-SP-P-0165 ^</code> · LAJ</p><p>{'Firma electrónica 15-ene-2018 sobre la Providencia de 12-ene-2018' if es else 'Electronic signature 15-Jan-2018 on the 12-Jan-2018 order'}</p><p><a href='{proc}'>{'Procedimiento vinculado' if es else 'Linked proceeding'}</a></p></article></div></section></main></body></html>"""
for lang, path in [('es', ROOT/'es/registro-autoridad-historica-las-palmas-civil/index.html'), ('en', ROOT/'en/historic-las-palmas-civil-justice-authority-register/index.html')]:
    path.parent.mkdir(parents=True, exist_ok=True); path.write_text(authority_page(lang), encoding='utf-8')

# 9. Reconcile count-only current-state/static registry surfaces without changing historical handoff prose.
repls = {
    '348-164-83-11-47-43':'350-165-83-11-48-43',
    '348 canonical':'350 canonical', '348 CAEPR':'350 CAEPR', '348 records':'350 records',
    '164 personas':'165 personas', '164 people':'165 people', 'PERSON: 164':'PERSON: 165', '"PERSON": 164':'"PERSON": 165',
    '47 instituciones':'48 instituciones', '47 institutions':'48 institutions', 'INSTITUTION: 47':'INSTITUTION: 48', '"INSTITUTION": 47':'"INSTITUTION": 48'
}
for path in (ROOT/'ops/CURRENT_UNITARY_STATE.json', ROOT/'scripts/validate_operational_truth.py', ROOT/'scripts/validate_current_reverse_engineered_digest.py', ROOT/'scripts/validate_dp3205_2014_publication.py', ROOT/'es/registro-identidad-materia/index.html', ROOT/'en/matter-identity-registry/index.html'):
    if not path.exists(): continue
    text = path.read_text(encoding='utf-8')
    for oldv, newv in repls.items(): text = text.replace(oldv, newv)
    path.write_text(text, encoding='utf-8')

assert reg['counts'] == {'total':350,'PERSON':165,'ORGANISATION':83,'STRUCTURE':11,'INSTITUTION':48,'PROCEEDING':43}, reg['counts']
assert auth['derived_counts']['unique_named_people'] == 62
assert auth['derived_counts']['confirmed'] == 59
assert auth['derived_counts']['pending'] == 3
assert auth['derived_counts']['by_role'] == {'MINISTERIO_FISCAL':17,'JUDGE_OR_MAGISTRATE':20,'LAJ':17,'NOTARY':8}, auth['derived_counts']['by_role']
assert sum(1 for row in public_rows if row['Reference'] == 'Diligencias Preliminares 1041/2017') == 1
print('RECONCILE_OK', len(rows), len(public_rows), reg['counts'], auth['derived_counts'])
