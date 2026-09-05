"""Compare finite deployed bytes to this checkout; never write repository content."""
import hashlib, json, os, pathlib, time, urllib.request
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
