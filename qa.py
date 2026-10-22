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
    checks['correct_password_unlocks_full_letter']=page.locator('#letter p').count()>=6
    checks['five_roles_present']=all(x in page.inner_text('body') for x in ['Global Coordinator','Mandated Lead Arranger','Co-Structuring Agent','Facility Agent','Security Agent'])
    checks['desktop_no_overflow']=page.evaluate('() => document.documentElement.scrollWidth<=window.innerWidth')
    checks['structure_six_entities']=page.locator('.entity').count()==6
    checks['four_funds_flow_stages']=page.locator('.flow-track>div').count()==4
    checks['eight_programme_groups']=page.locator('.support-card').count()==8
    checks['financial_status_not_unsupported_total']='Adopted consolidated totals not yet available' in page.locator('#accounts').inner_text()
    checks['grant_zero_base_explicit']='Base-case grant reliance remains zero' in page.locator('#incentives').inner_text()
    checks['reimbursement_timing_explicit']='reimbursement grant paid after expenditure' in page.locator('#incentives').inner_text()
    checks['new_sections_visible']=all(page.locator('#'+x).is_visible() for x in ['structure','funds','project','incentives','accounts','sequence'])
    checks['no_persistent_browser_storage']=page.evaluate('() => localStorage.length===0 && sessionStorage.length===0')
    expected={'letter':'f5c4ba02d9e7bcf896e80d6bbf78cdfec57807da44545ebabed0f384b943191b','briefing':'85dbfc0a292877a7cef0db311fe168e979a51e8e1de389a0b74eda471a5f623e','supplement':'48bc8c7680bb73764dc67bd7eb611dbcb31bf194fa4934cd5ee9c76a5225c70b'}
    with tempfile.TemporaryDirectory() as temp:
        for ident in ['letter','briefing','supplement']:
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
report={'reference':'SRLN-2026-WEB-SANTANDER-20261022-001/RENDER-003','live_url':url,'checks':checks,'downloads':downloads,'all_passed':all(checks.values()),'idle_test_method':'virtual browser clock; not a 20-minute elapsed wait','password_recorded':False}
print('BANKING_LIVE_QA_RESULT='+json.dumps(report,sort_keys=True))
if not report['all_passed']: raise RuntimeError('Live banking QA check failed; see boolean report')
