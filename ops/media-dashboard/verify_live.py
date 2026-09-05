"""Compare deployed bytes and all new internal source links; never write repository content."""
import hashlib, json, os, pathlib, time, urllib.request
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse, urldefrag, unquote
ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = pathlib.Path('/tmp/media-release/live'); OUT.mkdir(parents=True, exist_ok=True)
BASE = 'https://sbu001monterecco.github.io/por-derecho/'
PATHS = ['es/medios-trazabilidad-relato-publico/index.html', 'en/media-public-narrative-traceability/index.html', 'assets/media-desk.css', 'assets/media-desk.js', 'assets/optimum-reader-journey-finish-20260818.js', 'assets/data/unitary-route-registry-sync-20260819.json', 'sitemap-discovery-navigation.xml']
sha = os.environ['GITHUB_SHA']; matches = {}; pending = {}
for attempt in range(60):
    for path in PATHS:
        if path in matches: continue
        try:
            request = urllib.request.Request(BASE + path + '?media_release=' + sha + '&attempt=' + str(attempt), headers={'Cache-Control': 'no-cache'})
            with urllib.request.urlopen(request, timeout=25) as r:
                data = r.read(); status = r.status
            expected = (ROOT / path).read_bytes()
            if status == 200 and data == expected:
                matches[path] = {'path': path, 'status': status, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
                pending.pop(path, None)
            else: pending[path] = 'HTTP response or bytes differ'
        except Exception as e: pending[path] = str(e)
    if len(matches) == len(PATHS): break
    time.sleep(6)
report = {'expected_merge_sha': sha, 'base_url': BASE, 'matched': list(matches.values()), 'pending': pending, 'status': 'PASS' if len(matches) == len(PATHS) else 'FAIL', 'scope': 'Seven exact public resources; Pages run and browser acceptance are separate.'}
(OUT / 'exact-bytes.json').write_text(json.dumps(report, indent=2)); print(json.dumps(report, indent=2))
assert report['status'] == 'PASS', 'Deployed media bytes not verified'

class Links(HTMLParser):
    def __init__(self): super().__init__(); self.hrefs = []; self.ids = set()
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'a' and a.get('href'): self.hrefs.append(a['href'])
        if a.get('id'): self.ids.add(a['id'])

targets = set()
for lang, route in [('es', 'es/medios-trazabilidad-relato-publico/'), ('en', 'en/media-public-narrative-traceability/')]:
    parser = Links(); parser.feed((ROOT / f'ops/media-dashboard/section-{lang}.html').read_text())
    for href in parser.hrefs:
        url = urljoin(BASE + route, href)
        if urlparse(url).scheme == 'https' and url.startswith(BASE): targets.add(url)
assert len(targets) == 13, 'Internal-source link denominator changed; review explicitly'
results = []
for target in sorted(targets):
    url, fragment = urldefrag(target)
    row = {'url': target}
    try:
        request = urllib.request.Request(url + '?media_link_check=' + sha, headers={'Cache-Control': 'no-cache'})
        with urllib.request.urlopen(request, timeout=30) as r:
            body = r.read(); status = r.status; final_url = r.geturl()
        assert status == 200 and final_url.startswith(BASE) and b'<html' in body.lower(), 'Expected an internal HTML response'
        page = Links(); page.feed(body.decode('utf-8', errors='replace'))
        assert not fragment or unquote(fragment) in page.ids, 'Missing public static fragment'
        row.update(status='PASS', http=status, fragment_verified=bool(fragment))
    except Exception as e: row.update(status='FAIL', error=str(e))
    results.append(row)
links = {'expected_merge_sha': sha, 'total': len(results), 'passed': sum(r['status'] == 'PASS' for r in results), 'results': results, 'external_webinar_playback_verified': False}
(OUT / 'source-links.json').write_text(json.dumps(links, indent=2)); print(json.dumps(links, indent=2))
assert links['passed'] == 13, 'One or more new public source links failed'
