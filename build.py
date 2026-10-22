"""Publish only the preserved encrypted banking package; never decrypt on the server."""
from pathlib import Path
import os, json, io, zipfile, hashlib, base64, re, urllib.request, shutil
ARCHIVE_SHA = '57324b710a4baa4eb5d3374bcbea80e6197e358e672fd92969b4b90f2f2ecaa8'
HTML_SHA = '212db0a397afe5126d15fbc43952d2ba617c7f59631112edf1087748c0ff629d'
source = Path('encrypted-source.zip')
if source.exists():
    archive = source.read_bytes()
    origin = 'versioned-repository'
else:
    url = os.environ.get('SOURCE_ARCHIVE_URL', '')
    if not url.startswith('https://'):
        raise RuntimeError('Verified encrypted source unavailable; refusing to publish')
    with urllib.request.urlopen(url, timeout=60) as response:
        archive = response.read(2_000_000)
    origin = 'initial-verified-import'
if hashlib.sha256(archive).hexdigest() != ARCHIVE_SHA:
    raise RuntimeError('Encrypted archive integrity mismatch')
with zipfile.ZipFile(io.BytesIO(archive)) as z:
    raw = z.read('index.html')
if hashlib.sha256(raw).hexdigest() != HTML_SHA:
    raise RuntimeError('Original encrypted HTML integrity mismatch')
html = raw.decode('utf-8')
pack = json.loads(re.search(r'<script id="encryptedPayload" type="application/json">(.*?)</script>', html, re.S).group(1))
assert pack['iterations'] >= 600000 and len(pack['ciphertext']) > 300000
scripts = [(a,b) for a,b in re.findall(r'<script([^>]*)>(.*?)</script>',html,re.S) if 'application/json' not in a]
assert len(scripts) == 1
script_hash = base64.b64encode(hashlib.sha256(scripts[0][1].encode()).digest()).decode()
csp = "default-src 'none'; script-src 'sha256-" + script_hash + "'; style-src 'unsafe-inline'; img-src data: blob:; connect-src blob:; font-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'; upgrade-insecure-requests"
html = html.replace('<head>', '<head><meta http-equiv="Content-Security-Policy" content="' + csp + '">', 1)
# Only these explicit assets enter the public directory. Repository and counsel records are excluded.
out = Path('_site')
if out.exists(): shutil.rmtree(out)
(out/'assets').mkdir(parents=True)
(out/'index.html').write_text(html, encoding='utf-8')
(out/'robots.txt').write_text('User-agent: *\nDisallow: /\n', encoding='utf-8')
(out/'assets'/'banking-encrypted-source.zip').write_bytes(archive)
(out/'404.html').write_text('<!doctype html><html lang="en"><head><meta name="robots" content="noindex,nofollow"><title>Sun Rock</title></head><body><h1>Page not found</h1><a href="/">Return to the private briefing</a></body></html>',encoding='utf-8')
release = {'reference':'SRLN-2026-WEB-SANTANDER-20261022-001/RENDER-002','version':'2.0','encrypted_source_sha256':HTML_SHA,'archive_sha256':ARCHIVE_SHA,'deployed_html_sha256':hashlib.sha256((out/'index.html').read_bytes()).hexdigest(),'source':origin,'script_sha256_base64':script_hash,'password_in_source':False}
(out/'version.json').write_text(json.dumps(release,indent=2),encoding='utf-8')
print(json.dumps(release))
