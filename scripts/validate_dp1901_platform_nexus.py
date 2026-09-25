#!/usr/bin/env python3
"""Manual scoped checks for the additive DP1901 platform/recovery reader layer.
No workflow or new required gate is installed by this script.
"""
from __future__ import annotations
import json
import re
from pathlib import Path
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'assets/data/dp1901-platform-recovery-nexus-20260920.json'

class Page(HTMLParser):
    def __init__(self, text: str):
        super().__init__(); self.ids=[]; self.links=[]; self.lang=''; self.h1=0
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if 'id' in a: self.ids.append(a['id'])
        if tag=='a' and 'href' in a: self.links.append(a['href'])
        if tag=='html': self.lang=a.get('lang','')
        if tag=='h1': self.h1+=1

def main() -> None:
    d=json.loads(DATA.read_text())
    assert d['source_copy_denominator']['files']==3
    assert d['source_copy_denominator']['pages']==131
    assert len(d['nodes'])==21
    ids={n['id'] for n in d['nodes']}; assert len(ids)==21
    routes=[p for n in d['nodes'] for p in n['routes'].values()]
    assert len(routes)==len(set(routes))==42
    for edge in d['edges']:
        assert edge['from'] in ids and edge['to'] in ids
        assert edge['reciprocal_navigation'] and not edge['merges_proceedings']
    for n in d['nodes']:
        assert n['relation'] and set(n['context'])=={'es','en'}
        for lang,path in n['routes'].items():
            f=ROOT/path/'index.html'; assert f.is_file(), f
            t=f.read_text(); assert Page(t).lang==lang, f
            if n['id']=='PRESIDENCIA':
                assert 'data-pd1901-platform-nexus-loader="20260920a"' in t
            else: assert re.search(r'src=["\'][^"\']*site\.js',t), f
    loader=(ROOT/'assets/site.js').read_text()
    assert loader.count('PD1901_PLATFORM_NEXUS_LOADER')==1
    for n in d['nodes']:
        if n['id']!='PRESIDENCIA':
            for route in n['routes'].values(): assert route in loader
    for lang,route in d['central_routes'].items():
        f=ROOT/route/'index.html'; p=Page(f.read_text())
        assert p.lang==lang and p.h1==1 and len(p.ids)==len(set(p.ids))
        for target in routes: 
            if target.startswith(lang+'/'): assert '../../'+target+'#pd1901-platform-nexus' in p.links
        assert (ROOT/d['archive']).is_file()
    for source in d['sources']: assert (ROOT/source['canonical_control']).is_file(), source
    state=json.loads((ROOT/'assets/data/dp1901-routing-collision-v1.json').read_text())
    assert state['controlling_state']=='REF21_TO_DP1901_CONTEMPORANEOUSLY_CORROBORATED_OFFICIAL_REPARTO_AND_REF24_ASSOCIATION_HISTORY_OUTSTANDING'
    assert state['substantive_recovery_nexus']['data']==str(DATA.relative_to(ROOT))
    outline=(ROOT/'archive/PRESIDENCIA_PUBLIC_THESIS_EXPONE_SOLICITA_20SEP2026.md').read_text()
    assert len(re.findall(r'^## E\d{2}\.',outline,re.M))==12
    assert len(re.findall(r'^## S\d{2}\.',outline,re.M))==14
    assert 'DP1901_PLATFORM_RECOVERY_NEXUS_THESIS_20SEP2026.md' in outline
    assert d['filing_states_changed'] is False and d['private_sources_published'] is False
    print(json.dumps({'status':'PASS','nodes':21,'typed_edges':len(d['edges']),
      'existing_route_pairs':21,'central_pages':2,'source_copies':3,'source_pages':131,
      'outline_expone':12,'outline_solicita':14,'scope':'static source/link checks; browser and release results separate'}))

if __name__=='__main__': main()
