"""Build the encrypted static site from versioned bytes. No hosting/runtime decryption."""
from pathlib import Path
import os, json, io, zipfile, hashlib, base64, re, shutil, subprocess, sys
ARCHIVE_SHA = '45d6bffcfb0176756d2763cacdd8c2ad798e09c08dd3cdfb6632986fd362f4f0'
HTML_SHA = 'fe7797fc25cb3fd80910a7a5534f67ef534c4bc13ca8825bf9b68658d56239b5'
archive=Path('encrypted-source.zip').read_bytes()
if hashlib.sha256(archive).hexdigest()!=ARCHIVE_SHA: raise RuntimeError('Encrypted archive integrity mismatch')
with zipfile.ZipFile(io.BytesIO(archive)) as z: raw=z.read('index.html')
if hashlib.sha256(raw).hexdigest()!=HTML_SHA: raise RuntimeError('Encrypted HTML integrity mismatch')
html=raw.decode('utf-8')
pack=json.loads(re.search(r'<script id="encryptedPayload" type="application/json">(.*?)</script>',html,re.S).group(1))
assert pack['iterations']>=600000 and len(pack['ciphertext'])>300000
scripts=[(a,b) for a,b in re.findall(r'<script([^>]*)>(.*?)</script>',html,re.S) if 'application/json' not in a]
assert len(scripts)==1
script_hash=base64.b64encode(hashlib.sha256(scripts[0][1].encode()).digest()).decode()
csp="default-src 'none'; script-src 'sha256-"+script_hash+"'; style-src 'unsafe-inline'; img-src data: blob:; connect-src blob:; font-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'; upgrade-insecure-requests"
html=html.replace('<head>','<head><meta http-equiv="Content-Security-Policy" content="'+csp+'">',1)
out=Path('_site')
if out.exists(): shutil.rmtree(out)
(out/'assets').mkdir(parents=True)
(out/'index.html').write_text(html,encoding='utf-8')
(out/'robots.txt').write_text('User-agent: *\nDisallow: /\n',encoding='utf-8')
(out/'assets'/'banking-encrypted-source.zip').write_bytes(archive)
(out/'404.html').write_text('<!doctype html><html lang="en"><head><meta name="robots" content="noindex,nofollow"><title>Sun Rock</title></head><body><h1>Page not found</h1><a href="/">Return to the private briefing</a></body></html>',encoding='utf-8')
release={'reference':'SRLN-2026-WEB-SANTANDER-20261022-001/RENDER-003','version':'3.0','encrypted_source_sha256':HTML_SHA,'archive_sha256':ARCHIVE_SHA,'deployed_html_sha256':hashlib.sha256((out/'index.html').read_bytes()).hexdigest(),'source':'versioned-repository','script_sha256_base64':script_hash,'password_in_source':False}
(out/'version.json').write_text(json.dumps(release,indent=2),encoding='utf-8')
print(json.dumps(release))
# Optional owner-authorised live QA. Secret supplied only via private build environment,
# never included in published _site, repository, report, subprocess arguments or logs.
if os.environ.get('QA_PASSWORD'):
    subprocess.run([sys.executable,'-m','pip','install','--quiet','playwright==1.55.0'],check=True)
    subprocess.run([sys.executable,'-m','playwright','install','chromium'],check=True)
    subprocess.run([sys.executable,'qa.py'],check=True)
