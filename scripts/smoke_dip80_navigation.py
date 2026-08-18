#!/usr/bin/env python3
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin,urlparse
import sys
R=Path(__file__).resolve().parents[1]
roots=[R/'es/icalpa-mesa-del-ponente/dip-80-2026',R/'en/icalpa-rapporteur-workbench/dip-80-2026']
pages=[]
for root in roots:
    pages.extend(root.rglob('index.html'))
errors=[]
class P(HTMLParser):
    def __init__(self): super().__init__();self.hrefs=[];self.viewport=False
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='a' and a.get('href'): self.hrefs.append(a['href'])
        if tag=='meta' and a.get('name')=='viewport': self.viewport=True

def local_target(page,href):
    if href.startswith('#') or href.startswith('mailto:') or href.startswith('tel:'): return None
    u=urlparse(href)
    if u.scheme or u.netloc:return None
    rel=page.relative_to(R).as_posix()
    base='https://example.invalid/por-derecho/'+rel
    target=urlparse(urljoin(base,href)).path
    prefix='/por-derecho/'
    if not target.startswith(prefix):return None
    rp=target[len(prefix):]
    if not rp or rp.endswith('/'):rp+='index.html'
    return R/rp
for page in pages:
    text=page.read_text(encoding='utf-8');p=P();p.feed(text)
    if not p.viewport:errors.append(f'missing viewport: {page.relative_to(R)}')
    for href in p.hrefs:
        t=local_target(page,href)
        if t is not None and not t.exists(): errors.append(f'broken internal link: {page.relative_to(R)} -> {href} -> {t.relative_to(R)}')
css=(R/'assets/dip80-casebook.css').read_text(encoding='utf-8')
if '@media(max-width:900px)' not in css:errors.append('responsive mobile media query missing')
if errors:
    print('DIP80 NAV/MOBILE STRUCTURE SMOKE: FAIL');[print(' - '+e) for e in errors];sys.exit(1)
print(f'DIP80 NAV/MOBILE STRUCTURE SMOKE: PASS ({len(pages)} pages; viewport + internal targets + responsive media query)')
