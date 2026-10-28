"""Reproducible Render build of Sun Rock Santander private banking v5 gateway.

Inputs are immutable prior encrypted archive + independent, newly encrypted v5 payload.
The illustrated financing PDF is presented inside the unlocked website, with no additional email attachments.\nNo password, plaintext briefing, PDF source, or sensitive commercial content is in
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

# Post-unlock PDF reader. Uses only the existing authenticated PDF Blob URL;
# does not place PDFs, document text or the access key in public site assets.
reader_js = r'''try {
  const item = data.files && data.files.bank_v5;
  const anchor = document.querySelector('a[data-file="bank_v5"][data-mode="open"]');
  const pdfUrl = anchor && anchor.href;
  if (item && pdfUrl && pdfUrl.startsWith('blob:')) {
    const labels = ['Banking relationship and programme','UK legal entities and treasury','Spanish resort project finance','Spanish regional and public funding','Energy, employment and local support','Hotel platform, JV and recoveries','Five requested Santander roles','Mandate and due diligence','Sources and document control'];
    const toc = labels.map((label,i)=>'<button type="button" data-sr-page="'+(i+1)+'"><span>'+String(i+1).padStart(2,'0')+'</span>'+label+'</button>').join('');
    const reader = document.createElement('section');
    reader.id='sr-reader';
    reader.className='section sr-review-reader';
    reader.innerHTML = '<div class="sr-reader-wrap"><div class="eyebrow">Private banking review &middot; original illustrated document</div>'
      +'<div class="sr-reader-heading"><div><h2>Read the full banking presentation</h2>'
      +'<p class="sr-reader-lead">The full nine-page financing brief is available to read here without an email attachment. The original illustrations, tables, disclosures and source notes are preserved.</p></div>'
      +'<span class="sr-reader-version">Document V5.0</span></div>'
      +'<div class="sr-reader-actions"><button type="button" class="button" id="sr-read-inline">Read all pages here</button>'
      +'<a class="button secondary" target="_blank" rel="noopener noreferrer" id="sr-open-full">Open in separate tab</a>'
      +'<a class="button secondary" id="sr-download-full">Download for internal review</a></div>'
      +'<div class="sr-reader-toc-title">Navigate directly to a page</div><div class="sr-reader-toc" role="group" aria-label="Document sections">'+toc+'</div>'
      +'<div class="sr-reader-frame-wrap" id="sr-reader-frame-wrap" hidden><iframe title="Full confidential banking document" id="sr-reader-frame" loading="lazy"></iframe>'
      +'<p class="sr-reader-fallback">If your device cannot display an embedded PDF, select Open in separate tab. The source PDF remains inside this password-protected package.</p></div>'
      +'<p class="sr-reader-disclaimer">For preliminary professional discussion, subject to independent due diligence. This is not a committed financing, a bank approval, an issued security or an investment offer.</p></div>';
    const root = document.getElementById('content');
    const main = root.querySelector('main');
    const hero = main && main.querySelector('.hero');
    if (hero) hero.insertAdjacentElement('afterend',reader);
    else if (main) main.appendChild(reader);
    else root.appendChild(reader);
    const wrap=reader.querySelector('#sr-reader-frame-wrap');
    const frame=reader.querySelector('#sr-reader-frame');
    reader.querySelector('#sr-open-full').href=pdfUrl;
    const download=reader.querySelector('#sr-download-full');
    download.href=pdfUrl;
    download.download=item.name;
    const show=(page)=>{
      wrap.hidden=false;
      frame.src=pdfUrl+(page?'#page='+page+'&zoom=page-width':'');
      wrap.scrollIntoView({behavior:'smooth',block:'start'});
    };
    reader.querySelector('#sr-read-inline').addEventListener('click',()=>show(null));
    reader.querySelectorAll('[data-sr-page]').forEach(button=>button.addEventListener('click',()=>show(button.dataset.srPage)));
    const nav=root.querySelector('.section-nav');
    if(nav){const jump=document.createElement('a');jump.href='#sr-reader';jump.textContent='Complete presentation';nav.appendChild(jump);}
  }
} catch (readerError) {
  /* Preserves original decrypted document and PDFs if inline reading is unsupported. */
}'''
needle = '});$("password").value=""'
if html.count(needle) != 1:
    raise RuntimeError('Original PDF Blob initialization anchor not found exactly once')
html = html.replace(needle, '});' + reader_js + '$("password").value=""', 1)
reader_css = r'''.sr-review-reader{padding:30px 0 45px;border-bottom:1px solid #d7dfd7;scroll-margin-top:102px}
.sr-reader-wrap{padding:28px;border:1px solid #cbd9d2;background:linear-gradient(145deg,#f4f7f1,#fbfaf4);border-radius:10px}
.sr-reader-heading{display:flex;align-items:start;justify-content:space-between;gap:16px}
.sr-reader-heading h2{font-size:clamp(28px,3.2vw,40px);max-width:670px;margin-bottom:12px}
.sr-reader-lead{font-size:14px;color:#546c6c;max-width:730px}
.sr-reader-version{white-space:nowrap;font:600 11px Inter,Arial,sans-serif;color:#507477;padding:8px 11px;border:1px solid #c7d8cf;border-radius:30px}
.sr-reader-actions{display:flex;flex-wrap:wrap;gap:10px;margin:19px 0 25px}
.sr-reader-actions .button{padding:10px 14px;font-size:12px;white-space:normal}
.sr-reader-toc-title{font-size:12px;font-weight:700;color:#32545c;margin:0 0 10px}
.sr-reader-toc{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px}
.sr-reader-toc button{display:flex;gap:8px;align-items:center;text-align:left;color:#264751;background:#fff;border:1px solid #d5dfd7;border-radius:6px;padding:10px;font-size:12px;line-height:1.35;cursor:pointer}
.sr-reader-toc button:hover,.sr-reader-toc button:focus-visible{border-color:#477f85;background:#eff6f2}
.sr-reader-toc button span{color:#8b7846;font:17px Georgia,serif}
.sr-reader-frame-wrap{margin-top:20px;padding:8px;background:#edf1ec;border-radius:9px;border:1px solid #c8d6d0;scroll-margin-top:110px}
.sr-reader-frame-wrap iframe{width:100%;height:min(78vh,950px);min-height:490px;border:0;border-radius:5px;background:#fff;display:block}
.sr-reader-fallback,.sr-reader-disclaimer{font-size:11.5px;line-height:1.6;color:#637771;margin:13px 3px 0}
.sr-reader-disclaimer{margin-top:23px;padding-top:13px;border-top:1px solid #d5e0d6}
@media(max-width:800px){.sr-reader-toc{grid-template-columns:repeat(2,minmax(0,1fr))}.sr-reader-version{white-space:normal}}
@media(max-width:550px){.sr-reader-wrap{padding:18px}.sr-reader-heading{display:block}.sr-reader-version{display:inline-block;margin-bottom:6px}.sr-reader-toc{grid-template-columns:1fr}.sr-reader-actions .button{flex:1 1 100%;text-align:center}.sr-reader-frame-wrap iframe{height:64vh;min-height:390px}}
@media print{.sr-review-reader .sr-reader-actions,.sr-review-reader .sr-reader-toc,.sr-review-reader .sr-reader-frame-wrap{display:none!important}}'''
if html.count('</style>') != 1:
    raise RuntimeError('Styling insertion point not unique')
html = html.replace('</style>', '\n' + reader_css + '\n</style>', 1)

# One executable inline script. Password data are never stored in the repo.
scripts=[b for a,b in re.findall(r'<script([^>]*)>(.*?)</script>',html,re.S) if 'application/json' not in a]
if len(scripts)!=1:
    raise RuntimeError('Unexpected inline script count')
hash_b64=base64.b64encode(hashlib.sha256(scripts[0].encode('utf-8')).digest()).decode('ascii')
policy=("default-src 'none'; script-src 'sha256-"+hash_b64+"'; "
        "style-src 'unsafe-inline'; img-src data: blob:; connect-src blob:; "
        "font-src 'none'; frame-src blob:; object-src 'none'; base-uri 'none'; form-action 'none'; "
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
status={'reference':'SRLN-2026-WEB-SANTANDER-20261022-001/RENDER-V5-READER-FIX',
        'version':'5.2','document_version':'5.0','created_date':'2026-10-22',
        'archival_source_sha256':BASE_HTML_SHA,
        'encrypted_release_sha256':hashlib.sha256(RELEASE.read_bytes()).hexdigest(),
        'served_html_sha256':hashlib.sha256((out/'index.html').read_bytes()).hexdigest(),
        'script_sha256_base64':hash_b64,
        'credential_embedded':False,
        'post_unlock_pdf_reader':True,
        'download_files':'only in AES-256-GCM encrypted payload',
        'offer_status':'pre-admission / pre-issuance / not a securities offer'}
(out/'version.json').write_text(json.dumps(status,indent=2),encoding='utf-8')
print(json.dumps(status))

# Independent pre-NDA reader, published under /intro/ on the SAME Render host.
# Public source stores authenticated ciphertext only. No decryption key, access
# code, financial model, correspondent bank identity, contract or full-pack PDF.
# The existing protected V5.2 root and source archives are byte-for-byte intact.
INTRO_SOURCE = Path('pre-nda/index.html')
INTRO_SHA256 = '7f369a998ba45abcf53b1620cfdcbd984abfbdff8064dbf827376593c260ef2f'
intro_data=INTRO_SOURCE.read_bytes()
if hashlib.sha256(intro_data).hexdigest() != INTRO_SHA256:
    raise RuntimeError('Pre-NDA encrypted reader hash mismatch')
if b'id="cipherdata"' not in intro_data or b'noindex,nofollow' not in intro_data:
    raise RuntimeError('Pre-NDA reader missing authenticated payload or indexing controls')
for forbidden in (b'Montana Roja, Playa Blanca', b'fuentes y relaciones concretas', b'sun-rock-banking.onrender.com'):
    if forbidden in intro_data:
        raise RuntimeError('Pre-NDA plaintext/source routing is not isolated')
intro_out=out/'intro'
intro_out.mkdir(parents=True,exist_ok=True)
(intro_out/'index.html').write_bytes(intro_data)
intro_version={'reference':'SRLN-2026-SANTANDER-PRENDA-INTRO-20261028-V1',
               'access':'independent encrypted pre-NDA only',
               'created_date':'2026-10-28',
               'html_sha256':INTRO_SHA256,
               'root_full_pack_unchanged':True,
               'funding_or_mandate_status':'not committed / not appointed'}
(intro_out/'version.json').write_text(json.dumps(intro_version,indent=2),encoding='utf-8')
print(json.dumps(intro_version))
