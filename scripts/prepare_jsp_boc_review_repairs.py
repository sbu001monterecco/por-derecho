#!/usr/bin/env python3
"""Explicit candidate repairs written only to a review directory, never to Git.
Preserves source-index/cache bytes. Each corrected file and diff is returned for
manual exact-object admission; no branch, token, filing or publication operation.
"""
from pathlib import Path
import difflib,hashlib,json
ROOT=Path(__file__).resolve().parents[1]
def patch_generator(source):
    s=source.replace('else1','else 1')
    old="href=source_links.get(sid,'../../'+CHILD[lang].replace('index.html','')+'#'+sid)"
    s=s.replace(old,"href=source_links.get(sid,('../../'+SUP) if extra else ('../../'+CHILD[lang].replace('index.html','')+'#'+sid))")
    old="n=next(n for n in range(1,1000) if f'PD-SP-EVT-{n:04d}' not in used)"
    new="n=max([int(i.rsplit('-',1)[1]) for i in used if i.startswith('PD-SP-EVT-') and int(i.rsplit('-',1)[1])<1000],default=0)+1"
    assert old in s;s=s.replace(old,new)
    helper='''
def readable_fragment(fragment):
    from bs4 import BeautifulSoup
    soup=BeautifulSoup(fragment,'html.parser')
    for node in list(soup.find_all(string=True)):
        if node.find_parent('code') or node.find_parent(attrs={'data-full-section':True}):continue
        text=str(node)
        protected={'A35020726':'ZZZAZZZ','B35279850':'ZZZBZZZ','GC1339':'ZZZCZZZ'}
        text=text.replace('taxID','tax ID ').replace('CIFB35279850','CIF B35279850').replace('conGC1339','con GC1339').replace('joinsB35279850andGC1339','joins B35279850 and GC1339')
        for original,token in protected.items():text=text.replace(original,token)
        text=re.sub(r'(?<=[A-Za-zÁÉÍÓÚÜÑáéíóúüñ])(?=[0-9])',' ',text)
        text=re.sub(r'(?<=[0-9])(?=[A-Za-zÁÉÍÓÚÜÑáéíóúüñ])',' ',text)
        for original,token in protected.items():text=text.replace(token,original)
        text=re.sub(r',(?=[A-Za-zÁÉÍÓÚÜÑáéíóúüñ])',', ',text)
        text=text.replace('MonteLanza','Monte Lanza').replace('SunPark','Sun Park')
        if text!=str(node):node.replace_with(text)
    return str(soup)
'''
    assert '\ndef prepare(out:Path):'in s;s=s.replace('\ndef prepare(out:Path):',helper+'\ndef prepare(out:Path):',1)
    s=s.replace("fragment='\\n'.join(s)","fragment=readable_fragment('\\n'.join(s))")
    s=s.replace("'</header>'+intro,1","'</header>'+readable_fragment(intro),1")
    s=s.replace("block+'</main>',1","readable_fragment(block)+'</main>',1")
    compile(s,'prepare_jsp_boc_release.py','exec');return s

def compatible_python():
    return '''
def compatible(a,b):
    if norm(a['name'])==norm(b['name']):return True
    # One reviewed source-name variant, not a new identity or caret promotion.
    return (a.get('id')==b.get('id')=='PD-SP-R-0044'
      and a.get('type')==b.get('type')=='PROCEEDING'
      and a.get('name')=='JSP / Celgán — concurso 440/2021'
      and b.get('name')=='Concurso 440/2021 — José Sánchez Peñate, S.A. y Celgán, S.A.'
      and a.get('organ_id')==b.get('court_id')=='PD-SP-I-0015'
      and b.get('reference')=='440/2021'
      and a.get('declaration_date')=='2021-07-21'
      and set(b.get('debtors',[]))=={'PD-SP-O-0085','PD-SP-O-0094'}
      and set(b['debtors']).issubset(set(a.get('related_ids',[])))
      and a.get('identity_resolution')==b.get('identity_resolution')=='CARET_PENDING'
      and all(any('445948' in str(x) for x in r.get('identity_sources',[])) for r in [a,b]))
'''

def patches():
    result={}
    path='assets/jsp-incident-reader.js';s=(ROOT/path).read_text()
    helper="""
 const compatible=(a,b)=>norm(a.name)===norm(b.name)||(a.id===b.id&&a.id==='PD-SP-R-0044'&&a.type===b.type&&a.type==='PROCEEDING'&&a.name==='JSP / Celgán — concurso 440/2021'&&b.name==='Concurso 440/2021 — José Sánchez Peñate, S.A. y Celgán, S.A.'&&a.organ_id===b.court_id&&a.organ_id==='PD-SP-I-0015'&&b.reference==='440/2021'&&a.declaration_date==='2021-07-21'&&JSON.stringify([...b.debtors].sort())===JSON.stringify(['PD-SP-O-0085','PD-SP-O-0094'])&&b.debtors.every(id=>a.related_ids.includes(id))&&a.identity_resolution==='CARET_PENDING'&&b.identity_resolution==='CARET_PENDING'&&[a,b].every(r=>r.identity_sources.some(x=>String(x).includes('445948'))));
 // Exact reviewed court/debtors/declaration/source match; not alias-by-number,
 // current-office certification, a merged estate or identity confirmation.
"""
    assert s.count('norm(a.name)!==norm(b.name)')==2
    s=s.replace(' const inline=',helper+' const inline=',1).replace('norm(a.name)!==norm(b.name)','!compatible(a,b)');result[path]=s
    path='scripts/validate_jsp_incident_reader.py';s=(ROOT/path).read_text();s=s.replace('def load(path):',compatible_python()+'\ndef load(path):',1)
    old="require(norm(records[i]['name'])==norm(candidates[i]['name']),'canonical conflict '+i)";assert old in s;s=s.replace(old,"require(compatible(records[i],candidates[i]),'canonical conflict '+i)")
    old="require(len(candidates)==59,'59 source proposals')";new=old+"\n        require(compatible(records['PD-SP-R-0044'],candidates['PD-SP-R-0044']),'reviewed proceeding name variant')\n        wrong=copy.deepcopy(candidates['PD-SP-R-0044']);wrong['court_id']='PD-SP-I-0001';require(not compatible(records['PD-SP-R-0044'],wrong),'wrong court variant rejected')\n        wrong=copy.deepcopy(candidates['PD-SP-R-0044']);wrong['debtors']=['PD-SP-O-0002'];require(not compatible(records['PD-SP-R-0044'],wrong),'wrong debtor variant rejected')";assert old in s;s=s.replace(old,new);compile(s,path,'exec');result[path]=s
    path='scripts/validate_jsp_2017_dossier.py';s=(ROOT/path).read_text()
    old="manifest = load(ROOT / MANIFEST)";new=old+"\n    maintenance = any(p['path'].startswith('matter-identity-registry-v1.jsp-') for p in before['parts'])\n    maintenance_paths = set()\n    if maintenance:\n        check('maintenance keeps the complete identity manifest unchanged', manifest == before)\n        frozen='assets/data/jsp-2017-source-relationship-register.json'\n        check('maintenance preserves all eight sources and eighteen original edges byte-for-byte', subprocess.check_output(['git','show',f'{base}:{frozen}'],cwd=ROOT)==(ROOT/frozen).read_bytes())\n        release=load(ROOT/'assets/data/jsp-boc-release-manifest-20260905.json')\n        check('explicit maintenance scope and no identity admissions', release['control_id']=='PD-JSP-BOC-SIX-20260905' and release['counts']['identity_admissions']==0)\n        import hashlib\n        for item in release['files']:\n            check('reviewed maintenance bytes '+item['path'], hashlib.sha256((ROOT/item['path']).read_bytes()).hexdigest()==item['sha256'])\n            maintenance_paths.add(item['path'])\n        maintenance_paths.update({'assets/jsp-dossier-2017.js','scripts/validate_jsp_2017_dossier.py'})"
    assert old in s;s=s.replace(old,new)
    s=s.replace("len(new_records) == 27","len(new_records) == (0 if maintenance else 27)")
    s=s.replace("== {'PERSON':11,'ORGANISATION':15,'PROCEEDING':1}","== ({} if maintenance else {'PERSON':11,'ORGANISATION':15,'PROCEEDING':1})")
    s=s.replace("path in ({MANIFEST} | PROJECTIONS)","path in ({MANIFEST} | PROJECTIONS | maintenance_paths)")
    compile(s,path,'exec');result[path]=s
    return result

def main():
    out=Path('/tmp/jsp-boc-review/release');out.mkdir(parents=True,exist_ok=True)
    path='scripts/prepare_jsp_boc_release.py';original=(ROOT/path).read_text();corrected=patch_generator(original)
    ns={'__name__':'prepared_review','__file__':str(ROOT/path)};exec(compile(corrected,path,'exec'),ns);ns['prepare'](out)
    changes={path:corrected,**patches()};objects=json.loads((out/'OBJECTS.json').read_text());diffs=[]
    for path,text in changes.items():
        dest=out/path;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(text);b=dest.read_bytes()
        objects=[r for r in objects if r['path']!=path];objects.append({'path':path,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'git_blob':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()})
        diffs.extend(difflib.unified_diff((ROOT/path).read_text().splitlines(True),text.splitlines(True),fromfile=path,tofile=path+' (prepared)'))
    (out/'OBJECTS.json').write_text(json.dumps(objects,indent=2));(out.parent/'generator-correction.diff').write_text(''.join(diffs))
    # Add repaired runtime/tests to the exact manifest, without altering old source caches.
    manifest_path='assets/data/jsp-boc-release-manifest-20260905.json';manifest=json.loads((out/manifest_path).read_text());manifest['files']=[r for r in objects if r['path']!=manifest_path];(out/manifest_path).write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    b=(out/manifest_path).read_bytes()
    for r in objects:
        if r['path']==manifest_path:r.update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),git_blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest())
    (out/'OBJECTS.json').write_text(json.dumps(objects,indent=2))
if __name__=='__main__':main()
