#!/usr/bin/env python3
"""Finite MASTER MYND publication contract; no writes, network or proof upgrades."""
from __future__ import annotations
import argparse, hashlib, json, subprocess
from pathlib import Path
from urllib.parse import urljoin,urlparse,unquote
from bs4 import BeautifulSoup
from PIL import Image

def validate(root: Path) -> dict:
    profile=json.loads((root/'assets/data/sun-park-mynd-yaiza-site-v1.json').read_text())
    hotel='PD-SP-O-0042'; address='Calle Janubio 3, Playa Blanca, Lanzarote 35580, Spain'
    assert profile['canonical_id']==hotel
    assert profile['canonical_address']['display']==address
    org=json.loads((root/'assets/data/matter-identity-registry-v1.organisations.json').read_text())
    rows=[r for r in org['records'] if r['id']==hotel];assert len(rows)==1
    assert rows[0]['type']=='ORGANISATION'
    assert rows[0]['object_kind']=='HOTEL_ESTABLISHMENT_AND_PHYSICAL_SITE'
    assert rows[0]['canonical_address']['display']==address
    assert rows[0]['legacy']==['ricpe_hnt_mynd']
    assert profile['plan_identification']['status']=='AUTHOR_ASSERTED_IDENTIFICATION_INDEPENDENT_MATCH_NOT_COMPLETED'
    result={'status':'PASS_FOR_FINITE_SOURCE_CONTRACT','images':[],'routes':[],'backlinks':[],'surface_carets':[]}
    for record in profile['images']:
        p=root/record['path'];data=p.read_bytes()
        assert len(data)==record['bytes']
        assert hashlib.sha256(data).hexdigest()==record['sha256']
        with Image.open(p) as im:
            im.load();assert (im.width,im.height)==(record['width'],record['height'])
        result['images'].append({'path':record['path'],'sha256':record['sha256'],'decoded':True})
    disclosures={'es':'CARICATURA / REPRESENTACIÓN SATÍRICA — NO ES UN ANUNCIO REAL','en':'SATIRICAL / CARICATURE REPRESENTATION — NOT A REAL ADVERTISEMENT'}
    for lang in ['es','en']:
        routes=[profile['routes'][lang],profile['family_routes'][lang]]
        for route in routes:
            p=root/route.lstrip('/')/'index.html';s=BeautifulSoup(p.read_text(),'html.parser')
            assert len(s.find_all('h1'))==1
            assert s.find('link',rel='canonical')['href']=='https://sbu001monterecco.github.io/por-derecho'+route
            assert {x.get('hreflang') for x in s.find_all('link',rel='alternate')}=={'es','en'}
            assert address in s.get_text(' ',strip=True)
            ids=[x['id'] for x in s.find_all(id=True)];assert len(ids)==len(set(ids)),(route,'duplicate anchors')
            for a in s.find_all(['a','img','script','link']):
                u=a.get('href',a.get('src',''))
                dest=urlparse(urljoin('https://sbu001monterecco.github.io/por-derecho'+route,u))
                if dest.netloc!='sbu001monterecco.github.io' or not dest.path.startswith('/por-derecho/'):continue
                local=root/unquote(dest.path.removeprefix('/por-derecho/'))
                if local.is_dir():local/= 'index.html'
                assert local.is_file(),(route,u,'missing local route')
            if route==profile['family_routes'][lang]:
                assert disclosures[lang] in s.get_text()
                sources=[i.get('src','') for i in s.find_all('img')]
                for im in profile['images']:assert any(im['path'] in src for src in sources)
                if lang=='en':assert s.find(id='aguiar-acosta-proposed-witness-pair')
            result['routes'].append(route)
        for edge in profile['discovery_routes'][lang]:
            p=root/edge['route'].lstrip('/')/'index.html';s=BeautifulSoup(p.read_text(),'html.parser')
            urls=[urlparse(urljoin('https://sbu001monterecco.github.io/por-derecho'+edge['route'],a['href'])).path for a in s.find_all('a',href=True)]
            assert '/por-derecho'+profile['routes'][lang] in urls,(edge['route'],'missing backlink')
            result['backlinks'].append(edge['route'])

    # Every caret denotes one immutable byte object. Resolve the old page bytes
    # at the fixed source commit and the successor bytes in this working tree.
    digital=json.loads((root/'data/digital-media-asset-register-v1.json').read_text())
    source_head='6411d28961ac0de052f163c3363489e752de548f'
    def historic(path: str) -> bytes:
        return subprocess.run(
            ['git','show',f'{source_head}:{path}'],cwd=root,check=True,
            stdout=subprocess.PIPE,stderr=subprocess.PIPE,
        ).stdout
    old_register=json.loads(historic('data/digital-media-asset-register-v1.json'))
    assert old_register['control_date']=='2026-10-01'
    assert digital['control_date']=='2026-11-23'
    files=digital['files'];old_files=old_register['files']
    page_rows=[f for f in files if f.get('logical_asset')=='PD-DMA-0005' and
               f.get('role')=='DISCLOSED_EDITORIAL_PUBLICATION_SURFACE']
    assert len(page_rows)==4, 'expected two current and two historic page carets'
    asset=next(a for a in digital['logical_assets'] if a['reference']=='PD-DMA-0005')
    for lang,path in [('ES','es/acosta-matos-familia/index.html'),
                      ('EN','en/acosta-matos-family/index.html')]:
        old_ref=f'PD-DMA-0005-{lang}-PAGE^'
        new_ref=f'PD-DMA-0005-{lang}-PAGE-20261123^'
        prior=[f for f in page_rows if f['reference']==old_ref]
        current=[f for f in page_rows if f['reference']==new_ref and
                 f.get('publication_status')=='PUBLIC' and f.get('repository_mirror') is True]
        assert len(prior)==len(current)==1, (lang,'ambiguous page carets')
        assert sum(f.get('publication_status')=='PUBLIC' and f.get('repository_path')==path
                   for f in page_rows)==1, (lang,'multiple current pages')
        old,new=prior[0],current[0]
        base=next(f for f in old_files if f['reference']==old_ref)
        assert old['bytes']==base['bytes'] and old['sha256']==base['sha256']
        assert old['prior_surface_versions']==base['prior_surface_versions']
        assert old['public_url']==new['public_url']==base['public_url']
        assert old['repository_path']==old['source_path']==new['repository_path']==path
        assert old['source_head']==source_head
        assert old['publication_status']=='SUPERSEDED_PUBLIC_URL_SERVES_REPLACEMENT'
        assert old['repository_mirror'] is False
        assert old['superseded_by']==new_ref and new['supersedes']==old_ref
        assert old['correction_date']==new['control_date']=='2026-11-23'
        before=historic(path);after=(root/path).read_bytes()
        assert len(before)==old['bytes'] and hashlib.sha256(before).hexdigest()==old['sha256'],old_ref
        assert len(after)==new['bytes'] and hashlib.sha256(after).hexdigest()==new['sha256'],new_ref
        result['surface_carets'].append({'current':new_ref,'supersedes':old_ref,
                                         'source_head':source_head})
        assert asset['web_file' if lang=='ES' else 'web_file_en']==new_ref
    # Keep the unchanged image-byte checks, including the original photograph.
    for f in files:
        if f.get('logical_asset') in {'PD-DMA-0005','PD-DMA-0006'} and \
           f.get('role')!='DISCLOSED_EDITORIAL_PUBLICATION_SURFACE':
            b=(root/f['repository_path']).read_bytes()
            assert len(b)==f['bytes'] and hashlib.sha256(b).hexdigest()==f['sha256'],f['reference']
    return result

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);a=ap.parse_args()
    print(json.dumps(validate(a.root),indent=2,ensure_ascii=False))
if __name__=='__main__':main()
