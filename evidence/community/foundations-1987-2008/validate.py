#!/usr/bin/env python3
"""Verify this bounded source-reader edition. No network calls or source execution."""
import hashlib
import json
import re
from pathlib import Path
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parent

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            self.ids.append(a['id'])

def validate(root=ROOT):
    manifest = json.loads((root / 'MANIFEST.json').read_text(encoding='utf-8'))
    for item in manifest['files']:
        path = root / item['path']
        if path.is_symlink() or root.resolve() not in path.resolve().parents:
            raise ValueError('Unsafe file: ' + item['path'])
        data = path.read_bytes()
        if len(data) != item['bytes'] or hashlib.sha256(data).hexdigest() != item['sha256']:
            raise ValueError('Byte mismatch: ' + item['path'])
    for name, total in [('CEXP_2008_TRANSCRIPCION_ES.md', 15), ('ESTATUTOS_1987_TRANSCRIPCION_ES.md', 24)]:
        text = (root / name).read_text(encoding='utf-8')
        numbers = list(map(int, re.findall(r'^## Página fuente (\d+) de \d+', text, re.M)))
        if numbers != list(range(1, total + 1)):
            raise ValueError('Page sequence: ' + name)
        if not all(x.strip() for x in re.split(r'^## Página fuente .+$', text, flags=re.M)[1:]):
            raise ValueError('Empty source page: ' + name)
    page = Page()
    page.feed((root / 'index.html').read_text(encoding='utf-8'))
    if len(page.ids) != len(set(page.ids)):
        raise ValueError('Duplicate HTML IDs')
    if len(manifest['missing_contract_annexes']) != 3:
        raise ValueError('Annex state changed: requires reviewed reconciliation')
    return {'status': 'PASS', 'hashed_files': len(manifest['files']), 'held_pages': 39,
            'unique_static_html_ids': len(page.ids), 'scope': 'Bytes, page sequence and structure only; not authentication, semantic certification or live rendering.'}

if __name__ == '__main__':
    print(json.dumps(validate(), ensure_ascii=False, indent=2))
