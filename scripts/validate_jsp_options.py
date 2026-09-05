#!/usr/bin/env python3
"""Read-only, bounded validation; no publication or universal evidence certificate."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import argparse, json, re

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.ids=[]; self.links=[]; self.lang=None; self.headers=0; self.scripts=0
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag=='a' and 'href' in a:self.links.append(a['href'])
        if tag=='html':self.lang=a.get('lang')
        if tag=='h1':self.headers+=1
        if tag=='script':self.scripts+=1

p=argparse.ArgumentParser();p.add_argument('--root',default='.');p.add_argument('--full-repository',action='store_true');a=p.parse_args()
root=Path(a.root).resolve()
paths=['es/jsp-montelanza-concurso-liquidacion/opciones-multimatrix.html','en/jsp-montelanza-insolvency-liquidation/multimatrix-options.html']
controls=['attributed-position','ownership','documents','deed-correction','contrary','proof','law','sources']+[f'P{i}' for i in range(1,9)]
checks=[];parsed=[]
def check(label,condition):
    checks.append({'check':label,'pass':bool(condition)})
for rel in paths:
    f=root/rel;text=f.read_text();page=Page(text);parsed.append(page)
    check(rel+':language',page.lang==rel.split('/')[0]);check(rel+':one-h1',page.headers==1)
    check(rel+':no-JavaScript',page.scripts==0);check(rel+':unique-ids',len(page.ids)==len(set(page.ids)))
    for i in controls:check(rel+':anchor:'+i,i in page.ids)
    for href in page.links:
        u=urlsplit(href)
        if u.scheme:continue
        if not u.path:check(rel+':fragment:'+u.fragment,unquote(u.fragment) in page.ids);continue
        dest=(f.parent/unquote(u.path)).resolve()
        check(rel+':inside-repository:'+href,root==dest or root in dest.parents)
        if dest.is_file():
            if u.fragment and dest.suffix=='.html':check(rel+':cross-fragment:'+href,u.fragment in Page(dest.read_text()).ids)
        elif a.full_repository:
            check(rel+':destination:'+href,dest.is_dir() and (dest/'index.html').is_file())
    check(rel+':no-private-locators',not re.search(r'mail\.google|[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}|download_url|sk-proj-|\b[XYZ][0-9]{7}[A-Z]\b',text))
    check(rel+':whole-hotel-denominator','262' in text)
    check(rel+':deed-separation',all(x in text for x in ['8499','8500','8498','2016']))
check('bilingual-anchor-parity',set(parsed[0].ids)==set(parsed[1].ids))
check('control-exists',(root/'archive/JSP_OPTIONS_FRUSTRATION_05SEP2026.md').is_file())
result={'status':'PASS' if all(x['pass'] for x in checks) else 'FAIL','checks':len(checks),'failures':[x for x in checks if not x['pass']], 'scope':'Two static readers; anchor and local-link integrity, minimisation indicators. Not full source authenticity, canonical registration, browser or live Pages verification.','full_repository':a.full_repository}
print(json.dumps(result,ensure_ascii=False,indent=2));raise SystemExit(0 if result['status']=='PASS' else 1)
