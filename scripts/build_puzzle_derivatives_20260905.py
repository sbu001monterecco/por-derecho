#!/usr/bin/env python3
"""Generate identified reading derivatives; never replace or rewrite the master."""
from pathlib import Path
import argparse, hashlib, importlib.metadata, io, json, shutil
import fitz
from PIL import Image, ImageDraw, ImageFont
MASTER_SHA='e441bdb368c0092d5b15ca5ee911eeac266540bde54817e424f3075f4c5fdd47'
def digest(p):
    b=p.read_bytes(); return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def build(source, root):
    source=Path(source); root=Path(root); doc=fitz.open(source)
    if digest(source)!= {'bytes':50046618,'sha256':MASTER_SHA} or len(doc)!=32:
        raise ValueError('Not the authenticated 32-page master; no substitution permitted')
    target=root/'assets/docs/puzzle'; target.mkdir(parents=True,exist_ok=True)
    master=target/'PUZZLE-2024-original.pdf'
    if source.resolve()!=master.resolve():shutil.copyfile(source,master)
    pages=[]; pdf=fitz.open(); overview=Image.new('RGB',(4*760,8*610),'white')
    draw=ImageDraw.Draw(overview)
    try:font=ImageFont.truetype('DejaVuSans.ttf',22)
    except OSError:font=ImageFont.load_default()
    for index,page in enumerate(doc):
        n=index+1
        pix=page.get_pixmap(matrix=fitz.Matrix(2160/page.rect.width,2160/page.rect.width),alpha=False)
        image=Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
        path=target/f'page-{n:02d}.webp';image.save(path,'WEBP',quality=90,method=6)
        small=image.resize((1080,round(image.height/2)),Image.Resampling.LANCZOS)
        preview=target/f'page-{n:02d}-preview.webp';small.save(preview,'WEBP',quality=85,method=6)
        row={'page':n,'path':path.relative_to(root).as_posix(),'preview':preview.relative_to(root).as_posix(),'width':image.width,'height':image.height,**digest(path),'preview_integrity':digest(preview),'source_pages':[n],'derivative':'full-page raster, not a new evidential original'}
        pages.append(row)
        buf=io.BytesIO();image.save(buf,'JPEG',quality=87,optimize=True)
        new=pdf.new_page(width=page.rect.width,height=page.rect.height);new.insert_image(new.rect,stream=buf.getvalue())
        thumb=image.copy();thumb.thumbnail((740,555),Image.Resampling.LANCZOS)
        x=(index%4)*760+10;y=(index//4)*610+45
        draw.text((x,y-34),f'PUZZLE 2024 | p. {n:02d}',font=font,fill='black');overview.paste(thumb,(x,y))
        if n==2:
            large=page.get_pixmap(matrix=fitz.Matrix(4320/page.rect.width,4320/page.rect.width),alpha=False)
            large.save(target/'PUZZLE-2024-chronology-page-02.png')
    web=target/'PUZZLE-2024-web-reading-copy.pdf';pdf.set_metadata({'title':'PUZZLE 2024 — raster web-reading derivative','subject':'32 full source pages. Historical exhibit. Original SHA-256 '+MASTER_SHA,'author':'Por Derecho — source-derived rendering','creator':'PyMuPDF / Pillow; no synthetic evidence'});pdf.save(web,garbage=4,deflate=True);pdf.close()
    overview_path=target/'PUZZLE-2024-overview.jpg';overview.save(overview_path,'JPEG',quality=92,optimize=True)
    assets=[]
    for path,role,label in [(master,'archival_master','Unchanged 32-page original'),(web,'reading_pdf','32-page raster reading PDF; links/text layer not preserved'),(overview_path,'overview','Labelled 32-page contact sheet'),(target/'PUZZLE-2024-chronology-page-02.png','large_image','High-resolution original chronology page 2')]:
        assets.append({'path':path.relative_to(root).as_posix(),'role':role,'label':label,**digest(path)})
    manifest={'schema':'por-derecho.puzzle-assets.v1','control_id':'PD-PUZZLE-CONTINUITY-20260905-01','source_sha256':MASTER_SHA,'source_pages':32,'scope':'Every image is rendered from the complete corresponding master page; no generated/reconstructed evidence. Page 1 is the original sparse cover, not a load failure.','renderer':{'pymupdf':importlib.metadata.version('PyMuPDF'),'pillow':importlib.metadata.version('Pillow')},'assets':assets,'pages':pages,'public_deployment':'NOT_ESTABLISHED_BY_GENERATION','google_slides':'NOT_PUBLICLY_VERIFIED_NO_PUBLIC_LINK'}
    out=root/'data/puzzle/puzzle-assets-20260905.json';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    assert len(fitz.open(web))==32
    print(json.dumps({'pages':len(pages),'assets':assets,'manifest':str(out)},ensure_ascii=False,indent=2))
    return manifest
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--source',required=True);parser.add_argument('--root',default='.');args=parser.parse_args();build(args.source,args.root)
