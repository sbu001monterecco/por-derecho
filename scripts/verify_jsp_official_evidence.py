#!/usr/bin/env python3
"""Read-only source/image integrity check, optionally against the actual public host."""
from __future__ import annotations
import argparse, hashlib, io, json, subprocess, urllib.request
from pathlib import Path
import fitz
from PIL import Image
ROOT = Path(__file__).resolve().parents[1]
MANIFEST = 'assets/data/jsp-official-images-provenance-20260905.json'
LIVE = 'https://sbu001monterecco.github.io/por-derecho/'

def validate_bytes(raw, record):
    assert len(raw) == record['bytes'], 'Byte count: ' + record['path']
    assert hashlib.sha256(raw).hexdigest() == record['sha256'], 'SHA256: ' + record['path']
    assert hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest() == record['git_blob_sha'], 'Git blob: ' + record['path']

def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={'Cache-Control':'no-cache','User-Agent':'PorDerecho-ReadOnlyEvidenceVerification/1.0'}), timeout=45) as response:
        assert response.status == 200
        return response.read(2_000_001)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--live',action='store_true');ap.add_argument('--output',default='/tmp/jsp-evidence-verification.json');args=ap.parse_args()
    d=json.loads((ROOT/MANIFEST).read_text());src=d['source'];raw=(ROOT/src['path']).read_bytes();validate_bytes(raw,src)
    assert raw.startswith(b'%PDF-')
    doc=fitz.open(stream=raw,filetype='pdf');assert len(doc)==src['page_count']==1
    page=doc[0];text=page.get_text()
    assert all(x in text for x in ['Quinto:', 'Explobeach', 'Sun Park', 'JOSILAC'])
    records=[]
    for item in d['derivatives']:
        data=(ROOT/item['path']).read_bytes();validate_bytes(data,item)
        img=Image.open(io.BytesIO(data));img.load();assert img.format=='WEBP' and img.size==(item['width'],item['height'])
        pix=page.get_pixmap(matrix=fitz.Matrix(item['scale'],item['scale']),clip=fitz.Rect(item['clip_points']),alpha=False,colorspace=fitz.csRGB)
        assert img.convert('RGB').tobytes()==pix.samples, 'Rendered pixel difference: '+item['path']
        records.append({'path':item['path'],'dimensions':list(img.size),'sha256':item['sha256'],'pixels_match_source':True})
    bad=raw[:-1]+bytes([raw[-1]^1])
    try:validate_bytes(bad,src)
    except AssertionError:negative=True
    else:raise AssertionError('Corruption negative test failed')
    report={'control_id':d['control_id'],'source_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'source':src,'images':records,'negative_corruption_rejected':negative,'mode':'LIVE' if args.live else 'CANDIDATE','result':'PASS','live_checks':[]}
    if args.live:
        paths=[src['path'],*[x['path'] for x in d['derivatives']],MANIFEST,'assets/jsp-dossier-2017.js','assets/jsp-dossier-2017.css','es/jsp-montelanza-concurso-liquidacion/index.html','en/jsp-montelanza-insolvency-liquidation/index.html']
        for path in paths:
            actual=fetch(LIVE+path);expected=(ROOT/path).read_bytes();assert actual==expected,'Public bytes differ: '+path
            report['live_checks'].append({'path':path,'status':200,'bytes':len(actual),'sha256':hashlib.sha256(actual).hexdigest(),'exact_match':True})
        original=fetch(src['url']);validate_bytes(original,src);report['current_boe_source_matches']=True
    out=Path(args.output);assert '/tmp/' in str(out.resolve()),'Output must be outside tracked worktree';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
