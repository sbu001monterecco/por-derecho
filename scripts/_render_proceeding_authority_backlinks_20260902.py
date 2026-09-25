#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import json
import re
from html import escape

ROOT = Path('.')
DATA = ROOT / 'assets' / 'data'
index = json.loads((DATA/'matter-identity-registry-v1.json').read_text(encoding='utf-8'))
records = {}
for part in index['parts']:
    doc = json.loads((DATA/part['path']).read_text(encoding='utf-8'))
    for row in doc.get('records', []): records[row['id']] = row
coverage_doc = json.loads((DATA/'proceeding-justice-authority-coverage-20260902.json').read_text(encoding='utf-8'))
coverage = {row['master_id']: row for row in coverage_doc.get('records', [])}
routes = json.loads((DATA/'proceeding-page-routes-20260902.json').read_text(encoding='utf-8'))['routes']


def href_for(identifier: str, lang: str) -> str:
    rec = records.get(identifier, {})
    route = (rec.get('routes') or {}).get(lang)
    if route: return route
    return ('/es/registro-identidad-materia/' if lang == 'es' else '/en/matter-identity-registry/') + '#' + identifier.lower()


def links(ids: list[str], lang: str) -> str:
    if not ids: return '<span>SOURCE_GAP</span>'
    out=[]
    for identifier in ids:
        rec=records.get(identifier, {})
        name=rec.get('name') or identifier
        out.append(f"<a href='{escape(href_for(identifier,lang))}'><code>{escape(identifier)} ^</code> · {escape(name)}</a>")
    return '<br>'.join(out)


def row_html(label: str, value: dict, lang: str) -> str:
    state=value.get('state','SOURCE_GAP'); ids=value.get('person_ids') or []
    return f"<div class='pd-authority-row'><strong>{escape(label)}</strong><span>{links(ids,lang)}</span><small>{escape(state)}</small></div>"

for mid, item in coverage.items():
    if mid not in routes: continue
    for lang in ('es','en'):
        path=ROOT/routes[mid][lang]/'index.html'
        if not path.is_file(): continue
        html=path.read_text(encoding='utf-8')
        court_label='Órgano ^' if lang=='es' else 'Court / office ^'
        court_ids=item.get('institution_ids') or []
        court_state='SOURCE_IDENTIFIED' if court_ids else 'SOURCE_GAP_OR_NOT_CANONICALLY_ALLOCATED'
        court=f"<div class='pd-authority-row'><strong>{court_label}</strong><span>{links(court_ids,lang)}</span><small>{court_state}</small></div>"
        block=court
        block+=row_html('Juez / magistrado' if lang=='es' else 'Judge / magistrate', item.get('judge_or_magistrate',{}), lang)
        block+=row_html('LAJ', item.get('laj',{}), lang)
        block+=row_html('Fiscal', item.get('fiscal',{}), lang)
        heading='Autoridad identificada' if lang=='es' else 'Identified authority'
        pattern=re.compile(r"<article class='pd-proc-card'><h2>"+re.escape(heading)+r"</h2>.*?</article>", re.S)
        replacement=f"<article class='pd-proc-card'><h2>{heading}</h2>{block}</article>"
        html2, n=pattern.subn(replacement, html, count=1)
        assert n==1, (mid,lang,'authority article not found')
        path.write_text(html2, encoding='utf-8')

# Validate that every source-identified person/institution edge on a covered proceeding is an actual hyperlink.
for mid,item in coverage.items():
    if mid not in routes: continue
    expected=[]
    expected.extend(item.get('institution_ids') or [])
    for key in ('judge_or_magistrate','laj','fiscal'):
        expected.extend((item.get(key) or {}).get('person_ids') or [])
    for lang in ('es','en'):
        html=(ROOT/routes[mid][lang]/'index.html').read_text(encoding='utf-8')
        for identifier in expected:
            assert f'<code>{identifier} ^</code>' in html, (mid,lang,identifier)
            assert href_for(identifier,lang) in html, (mid,lang,identifier,'href')
print('AUTHORITY_BACKLINKS_OK', len(coverage))
