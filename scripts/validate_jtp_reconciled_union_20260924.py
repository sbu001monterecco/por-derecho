#!/usr/bin/env python3
"""Fail closed if either bilingual JTP page loses a reconciled evidence layer."""
from html.parser import HTMLParser
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
PAGES=('en/estate-payment-counsel-independence/index.html','es/pago-masa-independencia-defensa/index.html')
IDS=('prosecutorial-spine','visual','invoice-authority-source','record','source-close','reasons','adversarial-test','proof-plan','paths','sources')
class Page(HTMLParser):
    def __init__(self): super().__init__(); self.ids=[]; self.images=[]
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if attrs.get('id'): self.ids.append(attrs['id'])
        if tag=='img': self.images.append(attrs.get('src',''))
def check(text,path):
    p=Page(); p.feed(text)
    if len(p.ids)!=len(set(p.ids)) or any(p.ids.count(x)!=1 for x in IDS): raise ValueError('Missing/duplicated JTP chapter: '+path)
    for marker in ('data-jtp-reconciled="20260924"','data-jtp-visual-pair="PD-JTP-VIS-20260924"','data-jtp-source="20190104"','data-jtp-source="deep-sweep-20260924"','JTP_FEE_AUTHORITY_PAYMENT_SOURCE_CLOSE_24SEP2026.md','JTP_ONA_DEEP_SOURCE_SWEEP_24SEP2026.md'):
        if marker not in text: raise ValueError('Missing source layer: '+marker)
    lang=path[:2]
    if sum('jtp-money-route-context-v8-'+lang+'.svg' in s for s in p.images)!=2 or sum('jtp-representation-invoice-20260924-'+lang+'.svg' in s for s in p.images)!=1: raise ValueError('Paired image references changed')
    return p

def main():
    for path in PAGES:
        text=(ROOT/path).read_text(encoding='utf-8'); page=check(text,path)
        for anchor in IDS:
            try: check(text.replace('id="'+anchor+'"','data-removed="'+anchor+'"'),path)
            except ValueError: pass
            else: raise ValueError('Negative test failed: '+anchor)
        for src in page.images:
            if not (ROOT/path).parent.joinpath(src).resolve().is_file(): raise ValueError('Missing local image')
    print(json.dumps({'status':'PASS','pages':PAGES,'chapters':IDS,'negative_tests':20,'visuals_modified':False}))
if __name__=='__main__':
    try: main()
    except Exception as exc: print(str(exc),file=sys.stderr); raise SystemExit(1)
