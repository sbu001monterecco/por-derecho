#!/usr/bin/env python3
"""Build only owned press-desk additions; never import a contact or mailbox file."""
from pathlib import Path
import argparse, json, re, sys
ROOT = Path(__file__).resolve().parents[2]
BASE = 'https://sbu001monterecco.github.io/por-derecho/'
ROUTES = {'es':'es/medios-trazabilidad-relato-publico/', 'en':'en/media-public-narrative-traceability/'}
MARK = 'PD-MEDIA-DASHBOARD-20260905-01'

def owned(text, key, value, before):
    start, end = f'<!-- {MARK}:{key}:START -->', f'<!-- {MARK}:{key}:END -->'
    block = start + '\n' + value.strip() + '\n' + end
    if start in text:
        if text.count(start)!=1 or text.count(end)!=1: raise ValueError('Ambiguous owned block '+key)
        return re.sub(re.escape(start)+r'.*?'+re.escape(end), lambda _: block, text, count=1, flags=re.S)
    if text.count(before)!=1: raise ValueError('Ambiguous insertion target '+before)
    return text.replace(before, block+'\n'+before,1)

def outputs(root=ROOT):
    result={}
    for lang, route in ROUTES.items():
        other='en' if lang=='es' else 'es'
        path=route+'index.html';text=(root/path).read_text(encoding='utf-8')
        meta=(f'<link rel="canonical" href="{BASE}{route}">\n'
              f'<link rel="alternate" hreflang="{lang}" href="{BASE}{route}">\n'
              f'<link rel="alternate" hreflang="{other}" href="{BASE}{ROUTES[other]}">\n'
              '<link rel="stylesheet" href="../../assets/media-desk.css">\n'
              '<script src="../../assets/media-desk.js" defer></script>')
        text=owned(text,'head',meta,'</head>')
        template=(root/f'ops/media-dashboard/section-{lang}.html').read_text(encoding='utf-8')
        target='<section class="section"><div class="shell"><h2>'+('Prioridad 1 · mensaje abierto ahora' if lang=='es' else 'Priority 1 · open message now')+'</h2>'
        text=owned(text,'desk',template,target)
        label='Sala de prensa' if lang=='es' else 'Press desk'
        text=owned(text,'nav',f'<a href="#media-desk">{label}</a>','</nav>')
        if 'class="dossier-page"' in text:text=text.replace('class="dossier-page"','class="dossier-page media-desk-page"',1)
        result[path]=text
    path='assets/data/unitary-route-registry-sync-20260819.json'
    text=(root/path).read_text(encoding='utf-8');rows=json.loads(text)
    for lang,route in ROUTES.items():
        row={'lang':lang,'path':route,'title':('Sala de prensa documental y trazabilidad editorial' if lang=='es' else 'Documentary press desk and editorial traceability'),'type':'evidence','summary':('Fuentes públicas para periodistas, lectura de resoluciones, límites probatorios, correcciones y consultas privadas. Sin directorio ni historial de contactos.' if lang=='es' else 'Public sources for journalists, court-decision reading, evidence limits, corrections and private enquiries. No contact directory or correspondence history.'),'tags':['media','press','prensa','periodistas','dashboard'],'aliases':['sala de prensa','media dashboard','press desk','journalist briefing','Pregunta al expediente','Ask the Record']}
        matches=[i for i,r in enumerate(rows) if r['path']==route]
        if len(matches)>1:raise ValueError('Duplicate canonical route')
        if matches:
            if rows[matches[0]] != row: raise ValueError('Existing route changed: reconcile explicitly before regeneration')
        else:
            idx=text.rfind(']');text=text[:idx].rstrip()+',\n'+json.dumps(row,ensure_ascii=False,indent=2)+'\n'+text[idx:];rows.append(row)
    result[path]=text
    path='sitemap-discovery-navigation.xml';text=(root/path).read_text(encoding='utf-8')
    for lang,route in ROUTES.items():
        if f'<loc>{BASE}{route}</loc>' not in text:
            other='en' if lang=='es' else 'es'
            row=f'<url><loc>{BASE}{route}</loc><lastmod>2026-09-05</lastmod><xhtml:link rel="alternate" hreflang="{lang}" href="{BASE}{route}"/><xhtml:link rel="alternate" hreflang="{other}" href="{BASE}{ROUTES[other]}"/></url>\n'
            text=text.replace('</urlset>',row+'</urlset>')
    result[path]=text
    return result

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    changed=[]
    for path,text in outputs().items():
        dest=ROOT/path
        if dest.read_text(encoding='utf-8')!=text:
            changed.append(path)
            if not args.check:dest.write_text(text,encoding='utf-8')
    print(json.dumps({'mode':'check' if args.check else 'build','changed_paths':changed,'deployment_proof':False}))
    return int(bool(changed)) if args.check else 0
if __name__=='__main__':raise SystemExit(main())
