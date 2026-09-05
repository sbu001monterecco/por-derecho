#!/usr/bin/env python3
"""Read-only, scoped JSP publication QA; never writes tracked repository files."""
from __future__ import annotations
import argparse, collections, json, re, subprocess, unicodedata, zipfile
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'assets/data'
MANIFEST = 'assets/data/matter-identity-registry-v1.json'
PREFIX = 'PD-JSP-2017-DOSSIER-20260905'
ROUTES = ['es/jsp-montelanza-concurso-liquidacion/index.html', 'en/jsp-montelanza-insolvency-liquidation/index.html']

def load(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))

def norm(value: str) -> str:
    value = ''.join(c for c in unicodedata.normalize('NFKD', value) if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9]', '', value.lower())

class Page(HTMLParser):
    def __init__(self, text: str):
        super().__init__(); self.ids = []; self.links = []; self.lang = ''; self.feed(text)
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get('id'): self.ids.append(a['id'])
        if tag == 'html': self.lang = a.get('lang', '')
        for key in ('href', 'src'):
            if a.get(key): self.links.append(a[key])

def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument('--base', required=True); ap.add_argument('--output', default='jsp-qa')
    args = ap.parse_args(); out = ROOT / args.output; out.mkdir(exist_ok=True)
    report = {'control_id': PREFIX, 'base': args.base, 'checks': [], 'failures': [], 'limitations': ['No court-file or whole-perimeter completion certified', 'No merge, deployment or live verification certified', 'Incoming contextual integration and proceeding master-row review remain open']}
    def check(label, condition, details=None):
        report['checks'].append(label)
        if not condition: report['failures'].append({'check': label, 'details': details})
    before = json.loads(subprocess.check_output(['git', 'show', f'{args.base}:{MANIFEST}'], cwd=ROOT, text=True))
    manifest = load(ROOT / MANIFEST)
    for key, value in before.items():
        if key not in ('parts', 'counts'):
            check('preserve manifest field ' + key, manifest.get(key) == value)
    old_paths = {p['path']: p for p in before['parts']}
    for p in manifest['parts']:
        if p['path'] in old_paths: check('preserve old part metadata ' + p['path'], p == old_paths[p['path']])
    check('all original parts preserved', set(old_paths).issubset({p['path'] for p in manifest['parts']}))
    records = []; new_records = []; part_paths = []
    for part in manifest['parts']:
        path = DATA / part['path']; part_paths.append(path)
        obj = load(path); rows = obj['records']; records.extend(rows)
        check('part count ' + part['path'], len(rows) == part['count'], [len(rows), part['count']])
        check('typed part ' + part['path'], all(r['type'] == part['type'] for r in rows))
        if part['path'] not in old_paths: new_records.extend(rows)
    ids = [r['id'] for r in records]; by_id = {r['id']: r for r in records}
    check('unique global IDs', len(ids) == len(set(ids)))
    check('ID format', all(re.fullmatch(r'PD-SP-[POSIR]-\d{4}', i) for i in ids))
    counts = dict(collections.Counter(r['type'] for r in records)); counts['total'] = len(records)
    check('manifest counts match actual records', counts == manifest['counts'], counts)
    new_ids = {r['id'] for r in new_records}; old_records = [r for r in records if r['id'] not in new_ids]
    old_names = collections.defaultdict(set)
    for r in old_records:
        for name in [r['name'], *r.get('aliases', [])]: old_names[norm(name)].add(r['id'])
    for r in new_records:
        check('new ID has source ' + r['id'], bool(r.get('identity_sources')))
        check('new name has no existing match ' + r['id'], not old_names.get(norm(r['name'])), sorted(old_names.get(norm(r['name']), set())))
    evidence = load(DATA / 'jsp-2017-source-relationship-register.json')
    for reused in evidence['existing_id_reuse']:
        found = by_id.get(reused['id'])
        check('existing identity reuse ' + reused['id'], bool(found) and norm(found['name']) == norm(reused['name']), found['name'] if found else None)
    sources = {s['id'] for s in evidence['sources']}
    for edge in evidence['edges']:
        check('edge endpoints ' + edge['id'], edge['from'] in by_id and edge['to'] in by_id)
        check('edge source ' + edge['id'], edge['source'] in sources)
    check('corrected equity label', any(e['relation'] == 'DIRECT_EQUITY_RECORDED_26_82_PERCENT' for e in evidence['edges']))
    check('Community to CAM unproved', all(e['status'] == 'UNPROVED_RESEARCH_QUESTION' for e in evidence['edges'] if e['from'] == 'PD-SP-O-0005' and e['to'] == 'PD-SP-O-0007'))
    check('finca 8499 conditional', any(e['relation'] == 'FINCA_8499_CONDITIONAL_ALLOCATION' and e['status'] == 'CONDITIONAL_FULFILMENT_UNPROVED' for e in evidence['edges']))
    check('sixths no fake meeting-held event', all('HELD' not in e['kind'] or 'NOT_PROVED_HELD' in e['kind'] for e in evidence['events']))
    check('new scoped denominator', len(new_records) == 29)
    check('reused denominator', len(evidence['existing_id_reuse']) == 16)
    pages = {}
    for route in ROUTES:
        path = ROOT / route; text = path.read_text(encoding='utf-8'); page = Page(text); pages[route] = page
        check('unique page anchors ' + route, len(page.ids) == len(set(page.ids)))
        check('page language ' + route, page.lang == route[:2])
        check('source control visible ' + route, PREFIX in text)
        check('equity correction visible ' + route, '26.82%' in text or '26,82%' in text)
        check('2017 official original link ' + route, 'BORME-C-2017-7368.pdf' in text)
        check('conditional deed numbers visible ' + route, all(v in text for v in ['8498', '8499', '8500', '2026']))
        check('no private mail or secret in new page ' + route, not re.search(r'@monterecco|gmail\.com|sk-proj-|mailbox_id|message_id', text, re.I))
        for href in page.links:
            url = urlparse(href)
            if url.scheme or url.netloc: continue
            target = (path.parent / unquote(url.path)).resolve() if url.path else path
            if target.is_dir(): target /= 'index.html'
            check('local target ' + route + ' -> ' + href, target.exists())
            if not url.path and url.fragment:
                check('local anchor ' + route + ' -> ' + href, url.fragment in page.ids or url.fragment in sources or url.fragment in new_ids)
    check('bilingual anchor parity', set(pages[ROUTES[0]].ids) == set(pages[ROUTES[1]].ids))
    changed = subprocess.check_output(['git', 'diff', '--name-status', args.base, 'HEAD'], cwd=ROOT, text=True).splitlines()
    for row in changed:
        status, path = row.split('\t', 1)
        check('no deletion/rename ' + path, status in ('A', 'M'))
        check('only existing manifest modified ' + path, status != 'M' or path == MANIFEST)
    subprocess.run(['node', '--check', str(ROOT / 'assets/jsp-dossier-2017.js')], check=True)
    report['actual_counts'] = counts
    report['new_records'] = len(new_records)
    report['new_identity_confirmed'] = sum(r.get('identity_resolution') == 'CARET_CONFIRMED' for r in new_records)
    report['result'] = 'PASS_SCOPED_ONLY' if not report['failures'] else 'FAIL'
    (out / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    files = {ROOT / row.split('\t', 1)[1] for row in changed if row.split('\t', 1)[0] in ('A', 'M')}
    files.update(part_paths)
    with zipfile.ZipFile(out / 'review-source.zip', 'w', zipfile.ZIP_DEFLATED) as z:
        for path in sorted(files):
            if path.is_file(): z.write(path, path.relative_to(ROOT))
        z.write(out / 'report.json', 'jsp-qa/report.json')
    print(json.dumps({'result': report['result'], 'checks': len(report['checks']), 'failures': report['failures'], 'counts': counts}, ensure_ascii=False, indent=2))
    return int(bool(report['failures']))

if __name__ == '__main__':
    raise SystemExit(main())
