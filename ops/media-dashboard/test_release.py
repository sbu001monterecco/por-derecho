import importlib.util, json, re, unittest
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('release',Path(__file__).with_name('build_release.py')); module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.ids=[];self.forbidden=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if a.get('href'):self.links.append(a['href'])
  if a.get('id'):self.ids.append(a['id'])
  if tag in ('form','input','textarea','iframe','script'):self.forbidden.append(tag)
class ReleaseTests(unittest.TestCase):
 def test_deterministic(self):
  for path,text in module.outputs().items():self.assertEqual((ROOT/path).read_text(),text,path)
 def test_owned_blocks_once(self):
  for route in module.ROUTES.values():
   text=(ROOT/route/'index.html').read_text()
   for key in ('head','desk','nav'):
    self.assertEqual(text.count(f'{module.MARK}:{key}:START'),1)
    self.assertEqual(text.count(f'{module.MARK}:{key}:END'),1)
 def test_source_only_sections(self):
  for lang in ('es','en'):
   text=(ROOT/f'ops/media-dashboard/section-{lang}.html').read_text(); parser=Links();parser.feed(text)
   self.assertFalse(parser.forbidden)
   self.assertNotRegex(text,r'@[a-zA-Z0-9]|mail\.google\.com|1drv\.ms|contacto@|investigacion@|gmail_id|draft_id|dispatch_authorized|SENT|local-contact-')
   self.assertEqual(len(parser.ids),len(set(parser.ids)))
   self.assertGreaterEqual(len(parser.links),10)
 def test_controlled_webinar(self):
  for lang in ('es','en'):
   p=Links();p.feed((ROOT/f'ops/media-dashboard/section-{lang}.html').read_text())
   self.assertEqual(sum(x=='https://www.youtube.com/watch?v=mHn9IJU0qI4&t=488s' for x in p.links),1)
 def test_local_source_routes_exist(self):
  for lang,route in module.ROUTES.items():
   p=Links();p.feed((ROOT/f'ops/media-dashboard/section-{lang}.html').read_text())
   for href in p.links:
    url=urlparse(urljoin(module.BASE+route,href))
    if url.netloc!='sbu001monterecco.github.io':continue
    path=url.path.removeprefix('/por-derecho/');file=ROOT/path/('index.html' if path.endswith('/') else '')
    self.assertTrue(file.is_file(),str(file))
    if url.fragment:
     q=Links();q.feed(file.read_text());self.assertIn(url.fragment,q.ids)
 def test_search_existing_registry(self):
  rows=json.loads((ROOT/'assets/data/unitary-route-registry-sync-20260819.json').read_text())
  for route in module.ROUTES.values():
   found=[r for r in rows if r['path']==route];self.assertEqual(len(found),1);self.assertIn('media dashboard',found[0]['aliases'])
 def test_declared_sitemap(self):
  text=(ROOT/'sitemap-discovery-navigation.xml').read_text();ET.fromstring(text)
  for route in module.ROUTES.values():self.assertEqual(text.count(f'<loc>{module.BASE}{route}</loc>'),1)
  self.assertIn('sitemap-discovery-navigation.xml',(ROOT/'robots.txt').read_text())
 def test_no_parallel_route(self):
  self.assertFalse((ROOT/'es/medios/index.html').exists());self.assertFalse((ROOT/'en/media/index.html').exists())
 def test_bilingual_structure(self):
  for lang in ('es','en'):
   text=(ROOT/f'ops/media-dashboard/section-{lang}.html').read_text()
   self.assertEqual(text.count('<article class="card">'),6);self.assertIn('id="media-desk"',text)
  text=(ROOT/'ops/media-dashboard/section-en.html').read_text()
  self.assertEqual(text.count('Spanish source'),3);self.assertIn('remains unimplemented',text)
 def test_no_preview_claim_in_release(self):
  for lang,route in module.ROUTES.items():
   text=(ROOT/route/'index.html').read_text()
   self.assertNotIn('preview-es.html',text);self.assertNotIn('preview-en.html',text)
   self.assertIn('media-desk.css',text);self.assertIn('assets/site.js',text)
 def test_marker_collision_fails(self):
  with self.assertRaises(ValueError):module.owned('<main></main><main></main>','x','safe','<main>')
if __name__=='__main__':unittest.main()
