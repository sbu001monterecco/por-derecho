#!/usr/bin/env python3
"""Finite MASTER MYND contract; immutable Git fetch if needed, no working-tree writes or proof upgrades."""
from __future__ import annotations
import argparse, hashlib, json, re, subprocess
from pathlib import Path
from urllib.parse import urljoin,urlparse,unquote
from bs4 import BeautifulSoup
from PIL import Image

def historical_git_blob(root: Path, commit: str, path: str) -> bytes:
    """Read one immutable public Git object even in a shallow Actions checkout."""
    present=subprocess.run(['git','cat-file','-e',commit+'^{commit}'],
                           cwd=root,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    if present.returncode:
        subprocess.run(['git','fetch','--no-tags','--depth=1','origin',commit],
                       cwd=root,check=True,stdout=subprocess.DEVNULL)
        subprocess.run(['git','cat-file','-e',commit+'^{commit}'],cwd=root,check=True)
    return subprocess.check_output(['git','show',commit+':'+path],cwd=root)

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
    result={'status':'PASS_FOR_FINITE_SOURCE_CONTRACT','images':[],'routes':[],'backlinks':[]}
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
    # Check every newly admitted byte-object rather than treating HTTP existence as decoding proof.
    digital=json.loads((root/'data/digital-media-asset-register-v1.json').read_text())
    for f in digital['files']:
        if f.get('logical_asset') in {'PD-DMA-0005','PD-DMA-0006'}:
            if f['reference']=='PD-DMA-0005-EN-PAGE^':
                # The register seals the original public page, not a mutable current
                # page fingerprint. Verify those exact bytes at their Git origin.
                origin='19a71c941c76d1fd73eb654f55a74fadb5ea5590'
                assert f['repository_path']=='en/acosta-matos-family/index.html'
                # Both reader workflows use a one-commit checkout. The helper
                # fetches only this immutable base object when absent.
                b=historical_git_blob(root,origin,f['repository_path'])
                current=(root/f['repository_path']).read_text()
                old=b.decode('utf-8')
                pair=re.compile(r'<section\b[^>]*\bid="aguiar-acosta-proposed-witness-pair"[^>]*>.*?</section>',re.S)
                style=re.compile(r'<style data-aguiar-text-only="20261121">.*?</style>\n',re.S)
                old_pair=pair.findall(old);new_pair=pair.findall(current);styles=style.findall(current)
                assert len(old_pair)==len(new_pair)==len(styles)==1
                assert hashlib.sha256(old_pair[0].encode()).hexdigest()=='4076f3c861e832942c974aef3ee2150ac489150d9ee5c61b64c0d9bd47fc0c19'
                assert hashlib.sha256(new_pair[0].encode()).hexdigest()=='189c9fedd2344ae2aea150e6b75581806bf62d64ffe9c843618879192a76a358'
                assert hashlib.sha256(styles[0].encode()).hexdigest()=='bb756ea367a5cca506181a1a592a58e7bbf2cc40cbbf49aeb367057481283e5e'
                # The reviewed pair and style are the entire byte delta; the
                # original H1, source links, address and disclosure remain exact.
                assert pair.sub('',old)==pair.sub('',style.sub('',current))
                assert 'data-relationship-status="FAMILY_RELATIONSHIP_NOT_ESTABLISHED"' in current
                assert 'aguiar-no-family-edge' in current
                for capture in ('fernando-aguiar-acosta--linkedin-profile--20260828.png',
                                'laura-aguiar-acosta--linkedin-profile--20260828.jpg',
                                'laura-aguiar-acosta-linkedin-experience-user-supplied-20260828.jpg'):
                    assert capture not in current
            else:
                b=(root/f['repository_path']).read_bytes()
            assert len(b)==f['bytes'] and hashlib.sha256(b).hexdigest()==f['sha256'],f['reference']
    return result

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);a=ap.parse_args()
    print(json.dumps(validate(a.root),indent=2,ensure_ascii=False))
if __name__=='__main__':main()
