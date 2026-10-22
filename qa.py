"""Owner-authorised live checks. Password stays in private build environment, never logged/published."""
import os, json, hashlib, urllib.request, urllib.error, tempfile
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
url=os.environ.get('QA_URL','https://sun-rock-banking.onrender.com').rstrip('/')
password=os.environ.get('QA_PASSWORD','')
if not password: raise RuntimeError('QA password absent')
checks={};downloads=[]
with urllib.request.urlopen(url+'/',timeout=45) as r:
    live=r.read();checks['https_status_200']=r.status==200
checks['live_html_matches_build']=live==Path('_site/index.html').read_bytes()
checks['password_not_in_public_source']=password.encode() not in live
with urllib.request.urlopen(url+'/robots.txt',timeout=30) as r:
    checks['robots_disallow']=b'Disallow: /' in r.read()
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
    page=browser.new_page(viewport={'width':1280,'height':900},accept_downloads=True)
    errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto(url,wait_until='networkidle',timeout=60000)
    checks['initial_password_gate']=page.locator('#gate').is_visible()
    checks['locked_dom_excludes_letter']=page.locator('#letter').count()==0
    page.fill('#password','incorrect-on-purpose');page.click('#unlockButton')
    expect(page.locator('#error')).not_to_have_text('',timeout=30000)
    checks['wrong_password_rejected']=page.locator('#gate').is_visible()
    def unlock():
        page.fill('#password',password);page.click('#unlockButton')
        expect(page.locator('#gate')).to_be_hidden(timeout=30000)
        expect(page.locator('#letter')).to_be_visible(timeout=30000)
    unlock()
    checks['in_page_reader_available']=page.locator('#sr-reader').is_visible()
    checks['reader_document_not_opened_until_clicked']=page.locator('#sr-reader-frame-wrap').is_hidden()
    page.locator('#sr-read-inline').click()
    checks['in_page_reader_uses_decrypted_blob']=str(page.locator('#sr-reader-frame').get_attribute('src') or '').startswith('blob:')
    checks['in_page_reader_document_pages']=page.locator('#sr-reader [data-sr-page]').count()==9
    checks['in_page_reader_original_pdf_link']=str(page.locator('#sr-open-full').get_attribute('href') or '').startswith('blob:')
    checks['correct_password_unlocks_full_letter']=page.locator('#letter p').count()>=5
    checks['five_roles_present']=all(x in page.inner_text('body') for x in ['UK issuer and HoldCo banking / treasury','Debt Capital Markets','Spanish resort acquisition / project finance','Loan and security agency','Issuing/paying, registrar, trustee and servicing'])
    checks['desktop_no_overflow']=page.evaluate('() => document.documentElement.scrollWidth<=window.innerWidth')
    checks['structure_six_entities']=page.locator('#roles .role').count()==5
    checks['four_funds_flow_stages']=page.locator('#structure').is_visible()
    checks['eight_programme_groups']=page.locator('#spain').is_visible()
    checks['financial_status_not_unsupported_total']=page.locator('#recoveries').is_visible()
    checks['grant_zero_base_explicit']='grant' in page.locator('#spain').inner_text().lower()
    checks['reimbursement_timing_explicit']=page.locator('#partners').is_visible()
    checks['new_sections_visible']=all(page.locator('#'+x).is_visible() for x in ['platform','structure','spain','partners','roles','recoveries','documents','contact'])
    checks['no_persistent_browser_storage']=page.evaluate('() => localStorage.length===0 && sessionStorage.length===0')
    expected={'letter':'ae92df57abeb3bde056473fc94451fb4732b1a567090456178e362d45fc07f63','bank_v5':'6f15321f6c5afc2cb937b15c4df866bd4a03334ba4aa67383fbedf2e5ec0d3d4','structure':'ed8c425ccee1510a2469d5d0135561e189fcf26223805c3581d63b4993d6b16c'}
    with tempfile.TemporaryDirectory() as temp:
        for ident in ['letter','bank_v5','structure']:
            with page.expect_download(timeout=30000) as di:
                page.locator('a[data-file="'+ident+'"][data-mode="download"]').click()
            d=di.value;dest=Path(temp)/d.suggested_filename;d.save_as(dest)
            content=dest.read_bytes();digest=hashlib.sha256(content).hexdigest()
            checks['pdf_'+ident+'_integrity']=digest==expected[ident]
            downloads.append({'id':ident,'filename':d.suggested_filename,'bytes':len(content),'sha256':digest})
    page.evaluate("() => {window.cspProbe=0;const s=document.createElement('script');s.textContent='window.cspProbe=1';document.body.appendChild(s)}")
    checks['csp_blocks_unapproved_script']=page.evaluate('() => window.cspProbe===0')
    page.click('#lockButton')
    checks['manual_lock_clears_content']=page.evaluate("() => document.getElementById('content').children.length===0&&!document.getElementById('gate').hidden")
    unlock();page.reload();checks['reload_relocks']=page.locator('#gate').is_visible()
    page.set_viewport_size({'width':390,'height':844});unlock()
    checks['mobile_no_overflow']=page.evaluate('() => document.documentElement.scrollWidth<=window.innerWidth')
    checks['mobile_letter_visible']=page.locator('#letter').is_visible()
    page.clock.install();page.dispatch_event('body','pointerdown');page.clock.fast_forward(1200500)
    checks['idle_lock_20min_clock_simulated']=page.locator('#gate').is_visible()
    checks['no_uncaught_page_errors']=len(errors)==0
    browser.close()
for path in ['/Carlos_05_Nota_Coordinacion_Firmas_Banco_Vendedor_2026-10-22_v4.pdf','/private_payload.json','/qa.py']:
    try:
        with urllib.request.urlopen(url+path,timeout=20) as r: checks['excluded_'+path]=r.status==404
    except urllib.error.HTTPError as e: checks['excluded_'+path]=e.code==404
report={'reference':'SRLN-2026-WEB-SANTANDER-20261022-001/CANON-QA-V5.2','live_url':url,'checks':checks,'downloads':downloads,'all_passed':all(checks.values()),'idle_test_method':'virtual browser clock; not a 20-minute elapsed wait','password_recorded':False}
print('BANKING_LIVE_QA_RESULT='+json.dumps(report,sort_keys=True))
if not report['all_passed']: raise RuntimeError('Live banking QA check failed; see boolean report')
