#!/usr/bin/env python3
"""Finish static EN/ES landing views; preserve the source dossier and hash links."""
from pathlib import Path
import json, re, hashlib, html
root=Path.cwd()
base='https://sbu001monterecco.github.io/por-derecho/'
pub='PD-SAT-DP1901-SHAME-20260921'
anchor='shame-has-left-the-building'
image='assets/visuals/dp1901-shame-20260921/shame-exits-the-courthouse.png'
css='assets/dp1901-shame-linkedin-20260921.css'
data_path=root/'assets/data/dp1901-shame-linkedin-20260921.json'
data=json.loads(data_path.read_text())
media_path=root/'data/digital-media-asset-register-v1.json'
media=json.loads(media_path.read_text())
compliance_path=root/'data/satire-publication-compliance-v1.json'
compliance=json.loads(compliance_path.read_text())
entry=next(x for x in compliance['publications'] if x['publication_id']==pub)
logical=entry['logical_assets'][0]
new_surfaces=[]
for lang in ('en','es'):
    es=lang=='es'; other='en' if es else 'es'
    source=root/f'{lang}/dp-1901-2026/index.html'
    text=source.read_text()
    start=text.index('<!-- dp1901-shame-landing-20260921:start -->')
    end=text.index('<!-- dp1901-shame-landing-20260921:end -->',start)
    section=text[start:end]
    section=section.replace('<div id="pd-shame-existing-dossier"></div>','')
    section=section.replace('<h2 id="pd-shame-title">','<h1 id="pd-shame-title">').replace('</h2>','</h1>')
    section=section.replace('href="../../','href="../../../').replace('src="../../','src="../../../')
    section=section.replace(f'href="../../../{other}/dp-1901-2026/#{anchor}"',f'href="../../../{other}/dp-1901-2026/{anchor}/"')
    section=section.replace('href="#pd-shame-existing-dossier"','href="../"')
    title=data['posts'][lang].splitlines()[0]
    url=base+f'{lang}/dp-1901-2026/{anchor}/'
    other_url=base+f'{other}/dp-1901-2026/{anchor}/'
    description=('Sátira editorial y texto completo sobre DP1901, con fuentes, resolución adversa y preguntas pendientes.' if es else 'Editorial satire and full DP1901 post, with sources, the adverse decision and unresolved questions.')
    document=f'''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} — DP1901 | Por Derecho</title>
<meta name="description" content="{description}"><link rel="canonical" href="{url}">
<link rel="alternate" hreflang="{lang}" href="{url}"><link rel="alternate" hreflang="{other}" href="{other_url}">
<meta property="og:type" content="article"><meta property="og:title" content="{html.escape(title,quote=True)}"><meta property="og:description" content="{description}"><meta property="og:url" content="{url}"><meta property="og:image" content="{base+image}"><meta property="og:image:width" content="1055"><meta property="og:image:height" content="1491"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{base+image}">
<link rel="stylesheet" href="../../../{css}">
<style>body{{margin:0;background:#faf7f1}}*{{box-sizing:border-box}}.pd-shame-breadcrumb{{padding:16px 24px;background:#18262b;color:#fff;font:650 14px/1.5 system-ui,sans-serif}}.pd-shame-breadcrumb a{{color:inherit}}.pd-shame-landing h1{{font:800 clamp(32px,4.7vw,64px)/1.06 Georgia,serif;letter-spacing:-.03em;margin:12px 0;max-width:850px}}.pd-shame-layout figure{{position:static}}.pd-shame-landing{{border-bottom:0}}</style>
</head><body><nav class="pd-shame-breadcrumb" aria-label="{'Expediente completo' if es else 'Full documentary dossier'}"><a href="../">← {'DP1901 · Abrir el expediente documental completo' if es else 'DP1901 · Open the complete documentary dossier'}</a></nav><main id="content">{section}</main></body></html>
'''
    path=f'{lang}/dp-1901-2026/{anchor}/index.html'
    target=root/path; target.parent.mkdir(parents=True,exist_ok=True); target.write_text(document)
    new_surfaces.append({'path':path,'language':lang,'required_disclosure':('CARICATURA / REPRESENTACIÓN SATÍRICA — NO ES UN ANUNCIO REAL' if es else 'SATIRICAL / CARICATURE REPRESENTATION — NOT A REAL ADVERTISEMENT')})
    # The newly introduced fragment remains a compatibility entry for saved LinkedIn drafts.
    # This affects only that exact fragment, not any previous dossier URL/anchor.
    redirect=f'''\n<!-- dp1901-shame-hash-compatibility-20260921 -->
<script>if(window.location.hash==="#{anchor}"){{const target=new URL("{anchor}/",window.location.href);target.search=window.location.search;window.location.replace(target.href);}}</script>\n'''
    assert 'dp1901-shame-hash-compatibility-20260921' not in text
    source.write_text(text.replace('</head>',redirect+'</head>',1))
    # Candidate media context is the new static landing, not a frequently updated whole dossier.
    context=next(x for x in media['files'] if x['reference']==logical+'-'+lang.upper()+'-PAGE^')
    b=target.read_bytes(); context.update({'repository_path':path,'public_url':url,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
entry['public_surfaces'].extend(new_surfaces)
entry['source_refs'].extend(x['path'] for x in new_surfaces)
media_path.write_text(json.dumps(media,ensure_ascii=False,indent=2)+'\n')
compliance_path.write_text(json.dumps(compliance,ensure_ascii=False,indent=2)+'\n')
data['dedicated_landing_routes']={lang:f'{lang}/dp-1901-2026/{anchor}/' for lang in ('en','es')}
data['compatibility']='The newly introduced #shame-has-left-the-building links redirect only that fragment to the corresponding static landing; other dossier URLs and historical anchors are unchanged.'
data_path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
record=root/'archive/DP1901_LINKEDIN_LANDING_EN_ES_20260921.md'
record.write_text(record.read_text()+'''\n## Stable landing correction after actual viewport inspection\n\nThe pre-existing dossier runtime asynchronously inserts other public material, moving a hash visitor away from the intended section. Complete-section screenshots and text checks alone were insufficient to catch this. Two dedicated, script-free EN/ES landing pages now present the image and full post without that runtime. The newly introduced hash links in the saved drafts redirect to those views; no prior dossier anchor is redirected. The dossier retains the full added section and all previous text. Actual viewport checks must prove the title and image are on screen after following the saved hash link, not merely present in the DOM.\n\nStatic media-page fingerprints refer to the new focused pages, rather than making the frequently updated whole dossier an immutable media-page object. This is a candidate-stage correction; no previously published canonical file identity is reassigned.\n''')
print(json.dumps({'focused_routes':[x['path'] for x in new_surfaces],'legacy_dossier_preserved':True,'saved_hash_links_preserved':True},indent=2))
