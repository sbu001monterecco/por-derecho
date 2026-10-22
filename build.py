"""Reproducible Render build of Sun Rock Santander private banking v5 gateway.

Inputs are immutable prior encrypted archive + independent, newly encrypted v5 payload.
No password, plaintext briefing, PDF source, or sensitive commercial content is in
this build script or source repository. A password is supplied by each visitor only.
"""
from pathlib import Path
import os, io, re, json, zipfile, shutil, base64, hashlib

BASE_ARCHIVE_SHA='45d6bffcfb0176756d2763cacdd8c2ad798e09c08dd3cdfb6632986fd362f4f0'
BASE_HTML_SHA='fe7797fc25cb3fd80910a7a5534f67ef534c4bc13ca8825bf9b68658d56239b5'
SOURCE=Path('encrypted-source.zip')
RELEASE=Path('release-20261022-v5.enc.json')
if hashlib.sha256(SOURCE.read_bytes()).hexdigest()!=BASE_ARCHIVE_SHA:
    raise RuntimeError('Encrypted historical source archive checksum mismatch')
with zipfile.ZipFile(io.BytesIO(SOURCE.read_bytes())) as ar:
    raw=ar.read('index.html')
if hashlib.sha256(raw).hexdigest()!=BASE_HTML_SHA:
    raise RuntimeError('Original password-gate HTML checksum mismatch')
html=raw.decode('utf-8')

release_text=RELEASE.read_text(encoding='utf-8')
release=json.loads(release_text)
assert release['iterations']==600000
assert len(release['ciphertext'])>500000
assert len(base64.b64decode(release['salt']))>=16
assert len(base64.b64decode(release['iv']))==12
assert len(base64.b64decode(release['ciphertext']))>500000

# Replace only the original inert password-encrypted JSON. The original
# decrypted documents are preserved in the untouched source archive but are
# not present in this deployment's served encryptedPayload.
pattern=r'(<script id="encryptedPayload" type="application/json">)(.*?)(</script>)'
if len(re.findall(pattern,html,re.S))!=1:
    raise RuntimeError('Original encrypted JSON insertion point changed')
html=re.sub(pattern, lambda m:m.group(1)+release_text+m.group(3), html,count=1,flags=re.S)

# Reuse the exact original lock screen, 20-minute re-lock, PDF Blob handling
# and client-only PBKDF2/AES-256-GCM Web Crypto. v5 carries an independent
# authenticated associated-data label so that historical ciphertext cannot
# be substituted for this version.
old='new TextEncoder().encode("SunRockBanking-v1")'
new='new TextEncoder().encode("SunRockSupplement-v1")'
if html.count(old)!=1:
    raise RuntimeError('Authentication tag label insertion point changed')
html=html.replace(old,new,1)

# The protected content references these classes for bank diagrams. Styles
# are nonsensitive and visible to the public; no other assets or scripts are loaded.
css=Path('supplement.css').read_text(encoding='utf-8')
assert '</style>' not in css and '<script' not in css
if html.count('</style>')!=1:
    raise RuntimeError('CSS insertion point changed')
html=html.replace('</style>','\n'+css+'\n</style>',1)

# One executable inline script. Password data are never stored in the repo.
scripts=[b for a,b in re.findall(r'<script([^>]*)>(.*?)</script>',html,re.S) if 'application/json' not in a]
if len(scripts)!=1:
    raise RuntimeError('Unexpected inline script count')
hash_b64=base64.b64encode(hashlib.sha256(scripts[0].encode('utf-8')).digest()).decode('ascii')
policy=("default-src 'none'; script-src 'sha256-"+hash_b64+"'; "
        "style-src 'unsafe-inline'; img-src data: blob:; connect-src blob:; "
        "font-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'; "
        "upgrade-insecure-requests")
html=html.replace('<head>','<head><meta http-equiv="Content-Security-Policy" content="'+policy+'">',1)

# These substantive details are deliberately unavailable in the initial
# HTML. They exist only inside authenticated ciphertext until unlock.
public_shell=re.sub(pattern, r'\1[ENCRYPTED]\3', html, count=1, flags=re.S)
for forbidden in ['Montaña Roja','600-plus','2,000-unit','£500','€100','TUI','Jet2']:
    if forbidden.lower() in public_shell.lower():
        raise RuntimeError('Sensitive bank content leaked into the public pre-unlock shell: '+forbidden)
if 'noindex' not in html or 'id="gate"' not in html or 'id="password"' not in html:
    raise RuntimeError('Preserved lock or indexing controls missing')
if html.count('id="encryptedPayload"')!=1 or html.count('SunRockSupplement-v1')!=1:
    raise RuntimeError('Encrypted v5 release was not installed exactly once')

out=Path('_site')
if out.exists():shutil.rmtree(out)
out.mkdir()
(out/'index.html').write_text(html,encoding='utf-8')
(out/'robots.txt').write_text('User-agent: *\nDisallow: /\n',encoding='utf-8')
(out/'404.html').write_text('<!doctype html><html lang="en"><head><meta name="robots" content="noindex,nofollow"><title>Sun Rock</title></head><body><p>Page not found.</p><a href="/">Private briefing</a></body></html>',encoding='utf-8')
status={'reference':'SRLN-2026-WEB-SANTANDER-20261022-001/RENDER-V5',
        'version':'5.0','created_date':'2026-10-22',
        'archival_source_sha256':BASE_HTML_SHA,
        'encrypted_release_sha256':hashlib.sha256(RELEASE.read_bytes()).hexdigest(),
        'served_html_sha256':hashlib.sha256((out/'index.html').read_bytes()).hexdigest(),
        'script_sha256_base64':hash_b64,
        'credential_embedded':False,
        'download_files':'only in AES-256-GCM encrypted payload',
        'offer_status':'pre-admission / pre-issuance / not a securities offer'}
(out/'version.json').write_text(json.dumps(status,indent=2),encoding='utf-8')
print(json.dumps(status))