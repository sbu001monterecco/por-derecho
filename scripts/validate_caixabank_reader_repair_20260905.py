#!/usr/bin/env python3
"""Read-only acceptance: known source paths, safe derivatives, and completed browser cases.
No user-provided private identifier or raw mailbox content is used by this validator.
"""
from pathlib import Path
from urllib.parse import urljoin,urlsplit,unquote
import argparse,hashlib,json,re,sys
import fitz
from PIL import Image
from bs4 import BeautifulSoup
ROOT=Path.cwd()
def source():
 m=json.loads((ROOT/'data/audits/caixabank-public-derivatives-20260905.json').read_text());tests=0
 for row in m['files']:
  p=ROOT/row['path'];b=p.read_bytes();assert len(b)==row['bytes'];assert hashlib.sha256(b).hexdigest()==row['sha256'];tests+=2
  if p.suffix=='.jpg':
   im=Image.open(p);assert im.width>1000 and im.height>1400;im.verify();tests+=2
  if p.suffix=='.pdf':
   d=fitz.open(p);assert len(d)==row['pages'];assert not d.embfile_count()
   assert not any(list(q.widgets() or []) or list(q.annots() or []) for q in d)
   text='\n'.join(q.get_text() for q in d)
   assert not re.search(r'\b\d{8}\s*-?\s*[A-Z]\b',text)
   for n in range(1,d.xref_length()):
    obj=d.xref_object(n);assert '/ByteRange' not in obj and '/Type /Sig' not in obj
   tests+=5
 for root in ['es/reclamacion-caixabank-valencia/','en/caixabank-valencia-claim/']:
  for p in (ROOT/root).rglob('index.html'):
   s=BeautifulSoup(p.read_text(),'html.parser');ids=[x['id'] for x in s.select('[id]')];assert len(ids)==len(set(ids)),str(p)+' duplicate IDs'
   for e in s.select('a[href],img[src],link[rel=stylesheet],script[src]'):
    u=urljoin('https://local/por-derecho/'+str(p.relative_to(ROOT)),e.get('href') or e.get('src'));parts=urlsplit(u)
    if parts.hostname!='local':continue
    rel=unquote(parts.path).removeprefix('/por-derecho/');target=ROOT/rel
    if target.is_dir():target=target/'index.html'
    assert target.is_file(),(str(p),rel)
    tests+=1
  s=BeautifulSoup((ROOT/root/'index.html').read_text(),'html.parser');assert s.select_one('#caixabank-lectura-inicial')
  for field in ['og:title','og:description','og:url','og:image']:assert s.find('meta',attrs={'property':field})
  tests+=5
 print('SOURCE_CHECKS_PASS',tests)
def browser(folder):
 r=json.loads((Path(folder)/'browser-results.json').read_text());rows=r['results'];errors=[]
 if r.get('engine_failures'):errors+=r['engine_failures']
 for engine in ['chromium','firefox','webkit']:
  got=[x for x in rows if x['engine']==engine]
  if len(got)!=20:errors.append({'engine':engine,'case_count':len(got)})
 for row in rows:
  if row.get('status')!=200 or row.get('error'):errors.append({'route':row['route'],'engine':row['engine'],'status':row.get('status'),'error':row.get('error')})
  if not row.get('javascript'):continue
  for shot in row.get('viewports',[]):
   if shot['bodyWidth']>shot['width']+2 or shot['documentWidth']>shot['width']+2 or shot['overflow']:
    errors.append({'route':row['route'],'engine':row['engine'],'width':shot['width'],'overflow':shot['overflow'],'body':shot['bodyWidth']})
   if shot['duplicateIds']:errors.append({'route':row['route'],'duplicates':shot['duplicateIds']})
   for image in shot['images']:
    if image['visible'] and image['naturalWidth']==0:errors.append({'route':row['route'],'broken_image':image['src']})
 http=json.loads((Path(folder)/'http-results.json').read_text())
 for row in http:
  if row.get('status')!=200 or row.get('soft_404_suspected') or row.get('image_decodes') is False:errors.append(row)
 out={'completed_cases':len(rows),'http_resources':len(http),'functional_errors':errors,'passed':not errors,'scope':'bounded CaixaBank source/browser/HTTP acceptance; external viewer HTML is not PDF byte certification'}
 (Path(folder)/'acceptance.json').write_text(json.dumps(out,indent=2));print('BROWSER_ACCEPTANCE',len(rows),len(http),'ERRORS',len(errors))
 if errors:raise SystemExit(1)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--browser-folder');a=p.parse_args();source()
 if a.browser_folder:browser(a.browser_folder)
