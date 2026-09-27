#!/usr/bin/env python3
"""Final editorial corrections and independent scoped source-preservation checks."""
from pathlib import Path
import hashlib
import json
import subprocess
import re
import sys
from html.parser import HTMLParser

ROOT=Path(__file__).resolve().parents[1]
BASE='b15f253850ba3445fc995b50dd482209add8b3db'
BRANCH='agent/cuatrecasas-position-status-20260927'
MARKER='cuatrecasas-position-status-20260927'
RECEIPT='ops/cuatrecasas-position-status-source-receipt-20260927.json'
class IDs(HTMLParser):
    def __init__(self): super().__init__(); self.values=set()
    def handle_starttag(self,tag,attrs):
        self.values.update(v for k,v in attrs if k=='id' and v)
def ids(s):
    p=IDs();p.feed(s);return p.values
def original(path):
    return subprocess.check_output(['git','show',f'{BASE}:{path}'],cwd=ROOT).decode()
def sha(s): return hashlib.sha256(s.encode()).hexdigest()
def dump(v): return json.dumps(v,ensure_ascii=False,indent=2)+'\n'
def main():
    assert subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()==BRANCH
    en=ROOT/'en/cuatrecasas-sun-park/index.html'; es=ROOT/'es/cuatrecasas-sun-park/index.html'
    old='while its Gil Marer categorically denies any Matkator engagement; any asserted instrument or assumption basis requires separate evidence'
    new='Gil Marer categorically denies that Matkator ever engaged the firm; any asserted instrument-based obligation or assumption of fees requires separate evidence'
    txt=en.read_text(); assert txt.count(old)==1;en.write_text(txt.replace(old,new))
    old_es='mientras que su condición de cliente formal varía según workstream y debe probarse'
    new_es='Gil Marer niega categóricamente que Matkator contratara al despacho; cualquier obligación cambiaria o asunción de honorarios que se alegue requiere prueba separada'
    txt=es.read_text();assert txt.count(old_es)==1;es.write_text(txt.replace(old_es,new_es))
    generator=ROOT/'scripts/reconcile_cuatrecasas_position_status_20260927.py'
    txt=generator.read_text()
    txt=txt.replace("'formal client status varies by workstream and remains to be proved':'Gil Marer categorically denies any Matkator engagement; any asserted instrument or assumption basis requires separate evidence',", "'while its formal client status varies by workstream and remains to be proved':"+repr(new)+",\n          "+repr(old_es)+':'+repr(new_es)+',')
    generator.write_text(txt)
    receipt=json.loads((ROOT/RECEIPT).read_text())
    checked=[]
    for row in receipt['changed']:
        path=row['path'];text=(ROOT/path).read_text()
        if path.endswith('.html'):
            prev=original(path)
            assert ids(prev).issubset(ids(text)),path+' lost anchor'
            assert text.count('id="'+MARKER+'"')==1,path+' missing/duplicate panel'
            assert 'varía según workstream' not in text,path+' stale Spanish position'
            assert 'while its Gil Marer' not in text,path+' malformed replacement'
            # Original figures, evidence routes, images and historical source text
            # remain intact apart from the explicitly reviewed editorial sentence.
            block=re.search(r'<section class="section" id="'+MARKER+r'".*?</section>',text,re.S)
            assert block,path
            for token in ['mail.google.com','attachment_id','@sixtoabogados','@carlosllamas','IdLexNet']:
                assert token not in block.group(),path+' private locator'
            checked.append(path)
        row['after_sha256']=sha(text)
    # Financial control invariants are checked against immutable pre-task main.
    for path in ['assets/data/cuatrecasas-invoice-payment-register-v1.json','assets/data/cuatrecasas-wip-reconciliation-v1.json']:
        old_obj=json.loads(original(path));new_obj=json.loads((ROOT/path).read_text())
        new_obj.pop('current_position_status_control',None)
        assert old_obj==new_obj,path+' altered pre-existing financial/source fields'
    p='assets/data/cuatrecasas-whole-claim-architecture-v1.json'
    current=json.loads((ROOT/p).read_text());prior=json.loads(original(p))
    assert prior['billing_snapshot']==current['billing_snapshot'],'financial snapshot changed'
    assert current['current_procedural_state']['dp748']['last_verified_event']=='2026-09-16'
    assert current['current_position_20260927']['status']=='ATTRIBUTED_FIRST_HAND_CLIENT_STATEMENT_NOT_JUDICIAL_FINDING'
    receipt['editorial_review']={'date':'2026-09-27','static_pages_checked':len(checked),'all_prior_html_anchors_preserved':True,'invoice_wip_existing_fields_identical':True,'financial_snapshot_identical':True,'en_es_client_position_corrected':True,'deployment_not_established':True}
    receipt['exact_editorial_replacements']['es/cuatrecasas-sun-park/index.html']=1
    (ROOT/RECEIPT).write_text(dump(receipt))
    subprocess.run(['git','diff','--check'],cwd=ROOT,check=True)
    subprocess.run(['git','add','--','en/cuatrecasas-sun-park/index.html','es/cuatrecasas-sun-park/index.html','scripts/reconcile_cuatrecasas_position_status_20260927.py',RECEIPT],cwd=ROOT,check=True)
    subprocess.run(['git','commit','-m','Complete bilingual client correction and verify financial/source preservation'],cwd=ROOT,check=True)
    print(dump(receipt['editorial_review']))
if __name__=='__main__':main()
