"""Build the encrypted Sun Rock Santander static site plus a separate encrypted supplement.

The original approved letter and its two PDFs remain in the unmodified versioned archive.
The supplement's diagrams, project factsheet and narrative are individually encrypted
using the same shared password, without storing that password or plaintext in GitHub/Render.
"""
from pathlib import Path
import os, json, io, zipfile, hashlib, base64, re, shutil, subprocess, sys

ARCHIVE_SHA = '45d6bffcfb0176756d2763cacdd8c2ad798e09c08dd3cdfb6632986fd362f4f0'
HTML_SHA = 'fe7797fc25cb3fd80910a7a5534f67ef534c4bc13ca8825bf9b68658d56239b5'

archive=Path('encrypted-source.zip').read_bytes()
if hashlib.sha256(archive).hexdigest()!=ARCHIVE_SHA: raise RuntimeError('Original encrypted archive integrity mismatch')
with zipfile.ZipFile(io.BytesIO(archive)) as z: raw=z.read('index.html')
if hashlib.sha256(raw).hexdigest()!=HTML_SHA: raise RuntimeError('Original encrypted HTML integrity mismatch')
html=raw.decode('utf-8')

# Check the existing approved encrypted package without exposing its plaintext.
pack=json.loads(re.search(r'<script id="encryptedPayload" type="application/json">(.*?)</script>',html,re.S).group(1))
assert pack['iterations']>=600000 and len(pack['ciphertext'])>300000

# This supplemental JSON is ciphertext. Its key is derived in the browser from
# the same visitor-supplied password, using an independent PBKDF2 salt and AES-GCM IV.
addon=json.loads(Path('supplement.enc.json').read_text(encoding='utf-8'))
assert addon['iterations']>=600000 and len(addon['ciphertext'])>8000
assert re.fullmatch(r'[A-Za-z0-9+/=]+',addon['ciphertext'])
addon_raw=json.dumps(addon,separators=(',',':'))
addon_html='<script id="bankSupplement" type="application/json">'+addon_raw+'</script>'
anchor='</script><script>(()=>{"use strict";'
if html.count(anchor)!=1: raise RuntimeError('Encrypted application script anchor changed')
html=html.replace(anchor,'</script>'+addon_html+'<script>(()=>{"use strict";',1)

# CSS is public presentation scaffolding only; all narrative and account/project
# substance is in the separately encrypted supplement, not in plaintext source.
css=Path('supplement.css').read_text(encoding='utf-8')
assert '</style>' not in css and '<script' not in css
html=html.replace('</style>','\n'+css+'\n</style>',1)

# Augment the same existing encrypted unlock process, preserving original PDFs
# and the 20-minute lock behaviour. No new analytics, cookies or network calls.
old='$("content").innerHTML=data.html;'
if html.count(old)!=1: raise RuntimeError('Original unlock insertion point changed')
extra=r'''const extraPack=JSON.parse($("bankSupplement").textContent);const extraKey=await crypto.subtle.deriveKey({name:"PBKDF2",salt:b64(extraPack.salt),iterations:extraPack.iterations,hash:"SHA-256"},material,{name:"AES-GCM",length:256},false,["decrypt"]);const extraZip=await crypto.subtle.decrypt({name:"AES-GCM",iv:b64(extraPack.iv),additionalData:new TextEncoder().encode("SunRockSupplement-v1"),tagLength:128},extraKey,b64(extraPack.ciphertext));const extraStream=new Blob([extraZip]).stream().pipeThrough(new DecompressionStream("gzip"));const supplement=JSON.parse(await new Response(extraStream).text());$("content").innerHTML=data.html;const insertion=$("content").querySelector(".capital-flow");if(!insertion)throw new Error("structure_changed");insertion.insertAdjacentHTML("afterend",supplement.html);Object.assign(data.files,supplement.files||{});const nav=$("content").querySelector(".section-nav");if(nav)nav.innerHTML='<a href="#route">Next step</a><a href="#roles">Five roles</a><a href="#structure">Group map</a><a href="#money-flow">Funds flow</a><a href="#project-economics">Project model</a><a href="#fy2026">Accounts</a><a href="#spanish-support">Incentives</a><a href="#execution">Roadmap</a><a href="#letter">Full letter</a><a href="#documents">Documents</a><a href="#contact">Contact</a>';const labels=[[".letter-section .eyebrow","10 / THE COMPLETE LETTER"],[".documents .eyebrow","11 / BANKER-FACING DOCUMENTS"],[".contact .eyebrow","12 / CONTINUE THE CONVERSATION"]];labels.forEach(([sel,v])=>{const e=$("content").querySelector(sel);if(e)e.textContent=v});const docsIntro=$("content").querySelector(".documents>p");if(docsIntro)docsIntro.textContent="Three documents for this discussion, including a new one-page structure and funding factsheet. No private repository, privileged legal advice or personal-account records are included.";const dl=$("content").querySelector(".documents .doc-grid");if(dl)dl.insertAdjacentHTML("beforeend",'<div class="doc-card"><span class="file-label">PDF · ONE-PAGE FACT SHEET</span><h3>Structure &amp; funding summary</h3><p>Illustrated UK Sponsor / NewCo / Spanish ProjectCo architecture, treasury rationale and screened support routes. Management-prepared, not a bank commitment.</p><div class="doc-actions"><a data-file="structure" data-mode="open" target="_blank" rel="noopener noreferrer">Open PDF ↗</a><a class="button secondary" data-file="structure" data-mode="download">Download</a></div></div>');'''
html=html.replace(old,extra,1)

scripts=[(a,b) for a,b in re.findall(r'<script([^>]*)>(.*?)</script>',html,re.S) if 'application/json' not in a]
assert len(scripts)==1
script_hash=base64.b64encode(hashlib.sha256(scripts[0][1].encode()).digest()).decode()
csp="default-src 'none'; script-src 'sha256-"+script_hash+"'; style-src 'unsafe-inline'; img-src data: blob:; connect-src blob:; font-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'; upgrade-insecure-requests"
html=html.replace('<head>','<head><meta http-equiv="Content-Security-Policy" content="'+csp+'">',1)

out=Path('_site')
if out.exists():shutil.rmtree(out)
(out/'assets').mkdir(parents=True)
(out/'index.html').write_text(html,encoding='utf-8')
(out/'robots.txt').write_text('User-agent: *\nDisallow: /\n',encoding='utf-8')
(out/'assets'/'banking-encrypted-source.zip').write_bytes(archive)
(out/'404.html').write_text('<!doctype html><html lang="en"><head><meta name="robots" content="noindex,nofollow"><title>Sun Rock</title></head><body><h1>Page not found</h1><a href="/">Return to the private briefing</a></body></html>',encoding='utf-8')
release={'reference':'SRLN-2026-WEB-SANTANDER-20261022-001/RENDER-004','version':'4.0','encrypted_source_sha256':HTML_SHA,'archive_sha256':ARCHIVE_SHA,'supplement_encrypted_sha256':hashlib.sha256(Path('supplement.enc.json').read_bytes()).hexdigest(),'deployed_html_sha256':hashlib.sha256((out/'index.html').read_bytes()).hexdigest(),'source':'versioned-repository','script_sha256_base64':script_hash,'password_in_source':False,'contents':'protected charts / screened Spain incentives / FY2026 accountant-preparation status / retained original downloads'}
(out/'version.json').write_text(json.dumps(release,indent=2),encoding='utf-8')
print(json.dumps(release))
if os.environ.get('QA_PASSWORD'):
    subprocess.run([sys.executable,'-m','pip','install','--quiet','playwright==1.55.0'],check=True)
    subprocess.run([sys.executable,'-m','playwright','install','chromium'],check=True)
    subprocess.run([sys.executable,'qa.py'],check=True)
