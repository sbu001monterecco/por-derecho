#!/usr/bin/env python3
"""Prepare this bounded notice release before merge; never push or mutate main.

The existing institutional register remains authoritative. The input describes
reviewed sources; the crosswalk reserves existing-policy IDs and stores no
provider locators. Public projections are derived from the canonical register.
"""
from __future__ import annotations
import argparse
import hashlib
import html
import json
import re
import subprocess
import sys
import time
import urllib.request
from pathlib import Path
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1]
CONTROL = 'PD-SP-ORION-NOTICE-20260905'
INPUT = 'ops/orion-notice-register-input-20260905.json'
CROSSWALK = 'ops/ORION_NOTICE_CANONICAL_CROSSWALK_20260905.json'
REGISTER = 'assets/data/institutional-communications-register-v1.json'
GRAPH = 'assets/data/orion-rental-socimi-governance-20260905.json'
RECORD = '.github/evidence-intelligence/records/PD-SP-EI-20260905-02-ORION-RENTAL-SOCIMI-GOVERNANCE.md'
REPORT = 'ops/ORION_NOTICE_PUBLICATION_AUDIT_20260905.json'
BUILDER = 'scripts/reconcile_institutional_communications.py'
VALIDATOR = 'scripts/validate_institutional_communications.py'
START = '<!-- ORION-NOTICE-20260905:START -->'
END = '<!-- ORION-NOTICE-20260905:END -->'
MDSTART = '<!-- ORION-NOTICE-CONTROL-20260905:START -->'
MDEND = '<!-- ORION-NOTICE-CONTROL-20260905:END -->'
ROUTES = {
 'en': {'register':'en/institutional-records/', 'orion':'en/orion-rental-socimi/', 'caja':'en/cajasiete-sun-park-financing-comparability/', 'portfolio':'en/portfolio-orion-traceability/', 'cnmv':'en/cnmv-ricpe-verification/', 'ricpe':'en/ric-private-equity-sun-park/', 'fmmm':'en/francisco-mario-matos-matas/', 'antonio':'en/antonio-cogolludo-rojas/', 'shaila':'en/shaila-maria-cogolludo-ramos/', 'pamalexsha':'en/pamalexsha-servicios-integrales-sl/', 'acosta':'en/acosta-matos-perimeter/'},
 'es': {'register':'es/registros-institucionales/', 'orion':'es/orion-rental-socimi/', 'caja':'es/cajasiete-sun-park-financiacion-comparabilidad/', 'portfolio':'es/portfolio-orion-trazabilidad/', 'cnmv':'es/cnmv-ricpe-verificacion/', 'ricpe':'es/ric-private-equity-sun-park/', 'fmmm':'es/francisco-mario-matos-matas/', 'antonio':'es/antonio-cogolludo-rojas/', 'shaila':'es/shaila-maria-cogolludo-ramos/', 'pamalexsha':'es/pamalexsha-servicios-integrales-sl/', 'acosta':'es/acosta-matos-perimetro/'}
}
LABELS = {'orion':'Orion','caja':'Cajasiete','portfolio':'Portfolio','cnmv':'CNMV','ricpe':'RICPE','fmmm':'FMMM','antonio':'Antonio Cogolludo','shaila':'Shaila Cogolludo','pamalexsha':'Pamalexsha','acosta':'Acosta Matos','register':'Register / Registro'}

def read(rel: str):
    return json.loads((ROOT / rel).read_text(encoding='utf-8'))

def encoded(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + '\n').encode('utf-8')

def digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()

def save(rel: str, value) -> None:
    p=ROOT/rel; p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(encoded(value))

def public_url(route: str, fragment: str='') -> str:
    return '/por-derecho/' + route + ('#'+fragment if fragment else '')

def anchor(lang: str, event_id: str) -> str:
    return ROUTES[lang]['register']+'#communication-'+event_id

def used_numbers(kind: str) -> set[int]:
    out=set(); pattern=re.compile(r'PD-SP-'+kind+r'-(\d{4})\b')
    paths=subprocess.check_output(['git','ls-files','-z'],cwd=ROOT).decode().split('\0')
    for name in paths:
        p=ROOT/name
        if not p.is_file() or p.suffix.lower() not in {'.json','.md','.html','.js','.py','.csv','.yml','.yaml','.txt'} or p.stat().st_size>4_000_000:
            continue
        text=p.read_text(encoding='utf-8',errors='ignore')
        out.update(int(x) for x in pattern.findall(text))
    return out

def allocate(kind: str, used: set[int]) -> str:
    for n in range(1,10000):
        if n not in used:
            used.add(n); return f'PD-SP-{kind}-{n:04d}'
    raise ValueError(f'{kind} namespace exhausted')

def prepare_crosswalk() -> dict:
    spec=read(INPUT)
    if len(spec['items'])!=20 or len({i['key'] for i in spec['items']})!=20:
        raise ValueError('This release requires exactly twenty individually described events')
    if (ROOT/CROSSWALK).exists():
        x=read(CROSSWALK)
        if x['input_sha256']!=digest((ROOT/INPUT).read_bytes()):
            raise ValueError('Source input changed after ID allocation: reconcile the crosswalk explicitly')
        return x
    existing=read(REGISTER)
    if any(e.get('source_batch_id')==CONTROL for e in existing['events']):
        raise ValueError('Existing cohort without allocation crosswalk; do not duplicate')
    eu,su,du=used_numbers('EVT'),used_numbers('SRC'),used_numbers('DOC')
    maps={i['key']:{'event_id':allocate('EVT',eu)} for i in spec['items']}
    sources={}
    for i in spec['items']:
        if 'source_same_as' not in i:
            sources[i['key']]={'source_id':allocate('SRC',su),'source_kind':i['source_kind']}
            if i['source_kind']=='RETAINED_SIGNED_THREE_PAGE_PDF':
                sources[i['key']]['document_id']=allocate('DOC',du)
                sources[i['key']]['sha256']=i['source_sha256']
    for a in spec['attachment_sources']:
        sources[a['key']]={'source_id':allocate('SRC',su),'source_kind':a['state'],'native_document_identity':'NO_DUPLICATE_DOCUMENT_ID_ALLOCATED; attachment/source occurrence only'}
        candidates=sorted((ROOT/'assets').rglob(a['source_name'])) if a['source_name'].endswith('.png') else []
        if candidates:
            p=candidates[0]
            sources[a['key']]['public_asset']=str(p.relative_to(ROOT))
            sources[a['key']]['public_asset_sha256']=digest(p.read_bytes())
            sources[a['key']]['attachment_equivalence']='EXISTING_PUBLIC_FIGURE; native email attachment hash equivalence not asserted'
        else:
            sources[a['key']]['public_asset_state']='SOURCE_DESCRIPTION_ONLY; retained original not newly published'
    for i in spec['items']:
        maps[i['key']]['source_id']=sources[i.get('source_same_as',i['key'])]['source_id']
    x={'control_id':CONTROL,'control_date':'2026-09-05','input_path':INPUT,'input_sha256':digest((ROOT/INPUT).read_bytes()),'canonical_register':REGISTER,'base_register_sha256':digest((ROOT/REGISTER).read_bytes()),'baseline_event_count':len(existing['events']),'mappings':maps,'sources':sources,'coverage':{'scoped_event_descriptors':20,'distinct_source_descriptors':len(sources),'attachment_descriptors':6,'native_private_material_published':False,'universal_completeness_claim':False},'gaps':spec['gaps']}
    save(CROSSWALK,x)
    return x

def load_notice_events(root: Path) -> list[dict]:
    """Called by the canonical builder; descriptors never become a second register."""
    spec=json.loads((root/INPUT).read_text(encoding='utf-8'))
    cross=json.loads((root/CROSSWALK).read_text(encoding='utf-8'))
    if cross['input_sha256']!=digest((root/INPUT).read_bytes()):
        raise ValueError('Notice input/crosswalk integrity mismatch')
    events=[]
    for i in spec['items']:
        mapping=cross['mappings'][i['key']]
        state={k:'NOT_ESTABLISHED_BY_THIS_SOURCE' for k in ['transmission','registration','filing','destination','delivery','internal_association','substantive_examination','merits']}
        state['transmission']='DATE_ATTESTED_BY_LINKED_SOURCE' if 'source_same_as' in i else 'SOURCE_TRANSMISSION_OR_ACT_RETAINED'
        state['destination']='STATED_IN_SOURCE'
        state['delivery']=i.get('receipt','NO_ADDITIONAL_DELIVERY_ASSERTION')
        state['internal_association']=i.get('incorporation','NOT_ESTABLISHED_BY_THIS_SOURCE')
        state['substantive_examination']=i.get('review','NOT_ESTABLISHED_BY_THIS_SOURCE')
        state['merits']='NO_MERITS_FINDING_OR_CRIMINAL_ATTRIBUTION'
        refs=['ORION Rental SOCIMI','Sun Park / MYND Yaiza','RICPE',mapping['source_id']]
        if i.get('reference'): refs.append(i['reference'])
        if i['key'] in {'N-20260825','N-20260904-DECISION'}: refs.append('PD-SP-EVT-0152: separate REGAGE entry; identity bridge unresolved')
        if i.get('decision'): state['registration']='CHANNEL_REFERENCE_IN_NOTICE' if i['key']=='C-20260428' else 'DOCUMENTED_OFFICIAL_ACT'
        e={'event_id':mapping['event_id'],'cohort':'CURATED_SOURCE_PROVED_EVENT','layer':'TRANSPORT' if i['type']=='EMAIL_TRANSPORT' else 'OFFICIAL_ACT_OR_CORRESPONDENCE','source_key':'ORION-NOTICE:'+i['key'],'record_type':i['type'],'event_date':i['date'],'direction':i['direction'],'channel':'DOCUMENT' if 'PDF' in i['source_kind'] else 'EMAIL','office':i['institution'],'institution_key':re.sub(r'[^A-Z0-9]+','_',i['institution'].upper()).strip('_'),'official_reference':i.get('reference','NO_OFFICIAL_REFERENCE_ASSERTED'),'matter_references':refs,'source_batch_id':CONTROL,'source_integrity':{'status':i['source_kind']+'; PUBLIC_SAFE_REVIEW_DESCRIPTOR','repository_anchor':INPUT,'sha256':cross['input_sha256']},'evidence_state':state,'public_summary':i['en'],'public_summary_es':i['es'],'proves':[i['en']],'proves_es':i['es'],'does_not_prove':[i['limit_en']],'does_not_prove_es':i['limit_es'],'canonical_anchor_en':anchor('en',mapping['event_id']),'canonical_anchor_es':anchor('es',mapping['event_id']),'source_timezone':'OFFSET_AS_RETURNED_IN_RETAINED_METADATA' if re.search(r'[+-]\d\d:\d\d$',i.get('timestamp','')) else 'NOT_STATED; no timezone conversion inferred','criminal_responsibility_transfer':False,'public_derivative_state':'PUBLIC_SAFE_MINIMISED_DERIVATIVE'}
        if i.get('timestamp'): e['event_timestamp']=i['timestamp']
        if i.get('source_pages'): e['source_pages']=i['source_pages'].split(';',1)[0]
        if i.get('source_sha256'): e['source_integrity']['controlling_source_pdf_sha256']=i['source_sha256']
        if i.get('attachments'): e['attachment_count']=len(i['attachments']); e['attachment_count_basis']='SOURCE_ATTACHMENT_DESCRIPTORS; decorative inline signatures excluded'
        e.update({'attribution_state':'INSTITUTIONAL_NOTICE_NO_PERSONAL_SIGNATORY_ASSERTED','linked_transport_event_ids':[],'transport_link_state':'SEPARATE_ACT_AND_TRANSPORT_LINKS_IN_CANONICAL_CROSSWALK','proof_level':i['source_kind']})
        events.append(e)
    return events

def replace_once(rel: str, old: str, new: str) -> None:
    p=ROOT/rel; text=p.read_text(encoding='utf-8')
    if new in text: return
    if text.count(old)!=1: raise ValueError('Patch anchor not unique: '+rel)
    p.write_text(text.replace(old,new,1),encoding='utf-8')

def patch_pipeline() -> None:
    replace_once(BUILDER,'def _existing_receipt_ids(register:', '# Source-controlled additive notice cohort; canonical register remains authoritative.\nfrom prepare_orion_notice_register_20260905 import load_notice_events\nKEY_EVENTS.extend(load_notice_events(REPO_ROOT))\n\n\ndef _existing_receipt_ids(register:')
    replace_once(VALIDATOR,'    if denominator.get("event_rows_total") != len(events) or len(events) != 313:\n        errors.append(f"event-row denominator drift: expected 313, found {len(events)}")','    expected_event_total = BASELINE_EXPECTED + MAILBOX_EXPECTED + len(KEY_EVENTS)\n    if denominator.get("event_rows_total") != len(events) or len(events) != expected_event_total:\n        errors.append(f"event-row denominator drift: expected {expected_event_total}, found {len(events)}")')

CSS='''<style>.notice-20260905{max-width:1120px;margin:2rem auto;padding:1.4rem;line-height:1.6}.notice-20260905 .notice-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1rem}.notice-20260905 article,.notice-20260905 figure{border:1px solid #ccd6db;border-radius:12px;padding:1rem;margin:.7rem 0;min-width:0;background:#fff;color:#172b35}.notice-20260905 .notice-boundary{border-left:5px solid #8c2f2c;background:#fff7f5;padding:1rem}.notice-20260905 .notice-tag{font-size:.75rem;font-weight:800;letter-spacing:.035em}.notice-20260905 .notice-flow{display:flex;flex-wrap:wrap;gap:.65rem;list-style:none;padding:0}.notice-20260905 .notice-flow li{border:1px solid #bcccd3;border-radius:10px;padding:.7rem;flex:1 1 170px}.notice-20260905 img{display:block;width:100%;height:auto}.notice-20260905 code{overflow-wrap:anywhere}.notice-20260905 a{overflow-wrap:anywhere}.notice-20260905 :target{outline:3px solid #ac7924;outline-offset:4px}.notice-20260905 details{margin:.8rem 0}.notice-20260905 figcaption{font-size:.9rem}.notice-20260905 nav{display:flex;flex-wrap:wrap;gap:.7rem}@media(max-width:740px){.notice-20260905 .notice-grid{grid-template-columns:1fr}.notice-20260905{padding:.8rem}}</style>'''

def textblock(lang: str, kind: str, plan: dict, events: dict) -> str:
    spec=read(INPUT); es=lang=='es'; items=spec['items']
    selected=items if kind in {'register','orion'} else [i for i in items if (i['key'].startswith('C-') if kind=='caja' else i['key'].startswith('P-') if kind=='portfolio' else i['key'].startswith('N-') if kind=='cnmv' else False)]
    title='Notificaciones, fuentes y decisiones — registro individual' if es else 'Notices, sources and decisions — individual registration'
    out=[START,CSS,f'<section class="notice-20260905" id="notice-20260905" data-notice-release="{CONTROL}"><p class="notice-tag">{CONTROL} · 2026-09-05</p><h2>{title}</h2>']
    bound=('Cada fecha enlaza con su evento y fuente. Envío, recepción, registro, incorporación, revisión y decisión no son equivalentes. Ni proximidad mercantil ni recepción de alegaciones transmiten responsabilidad penal. Las preguntas de diligencia y conducta posterior se examinan actor por actor.' if es else 'Every date links to its event and source. Sending, receipt, registration, incorporation, review and decision are different states. Commercial proximity and receipt of allegations do not transfer criminal responsibility. Due diligence and subsequent conduct are tested actor by actor.')
    out.append('<p class="notice-boundary">'+bound+'</p><nav aria-label="Related evidence">')
    for k in ['register','orion','caja','portfolio','cnmv','ricpe','fmmm','antonio','shaila','pamalexsha','acosta']:
        r=ROUTES[lang][k]
        if (ROOT/r/'index.html').exists(): out.append(f'<a href="{public_url(r,"notice-20260905")}">{html.escape(LABELS[k])}</a>')
    out.append('</nav>')
    if not selected:
        out.append('<p>'+('Este nodo conserva su cronología y atribución anteriores. La nueva capa enlaza conocimiento, información facilitada, notificaciones y actuaciones posteriores; no imputa al destinatario la conducta de otro actor.' if es else 'This node retains its earlier chronology and attribution. The new layer connects knowledge, information supplied, notices and subsequent actions; it does not attribute another actor\'s conduct to a recipient.')+'</p>')
    else:
        out.append('<ol class="notice-flow" aria-label="Evidence state pathway">')
        for a,b in [('Documento / hecho','Document / event'),('Envío → recepción','Sent → received'),('Revisión → decisión','Review → decision'),('Efectos: prueba separada','Effects: separate proof')]:out.append('<li>'+ (a if es else b)+'</li>')
        out.append('</ol><div class="notice-grid">')
        for i in selected:
            m=plan['mappings'][i['key']]; e=events[m['event_id']]
            frag='communication-'+m['event_id']; u=public_url(ROUTES[lang]['register'],frag)
            aid=f' id="{frag}"' if kind=='register' else ''
            out.append(f'<article{aid}><div class="notice-tag">{html.escape(i["institution"])} · {i["type"]}</div><h3><a href="{u}">{i["date"]}</a> · <code>{m["event_id"]}</code></h3><p>{html.escape(e["public_summary_es" if es else "public_summary"])}</p><p class="notice-boundary">{html.escape(i["limit_es" if es else "limit_en"])}</p>')
            out.append(f'<p><a href="{public_url(ROUTES[lang]["register"],"source-"+m["source_id"])}">Fuente / Source {m["source_id"]}</a></p>')
            if kind=='register':
                out.append('<details><summary>'+('Fecha, estado y conexiones' if es else 'Date, status and connections')+'</summary>')
                out.append('<p>'+html.escape(i.get('timestamp',i['date']))+' · '+html.escape(e['source_timezone'])+'</p>')
                out.append('<p>'+html.escape(i['source_kind'])+'</p>')
                same=[x for x in items if x['key'][0]==i['key'][0]]; pos=same.index(i)
                for other in same[max(0,pos-1):pos]+same[pos+1:pos+2]:
                    oid=plan['mappings'][other['key']]['event_id']; out.append(f'<p><a href="{public_url(ROUTES[lang]["register"],"communication-"+oid)}">↔ {other["date"]} · {oid}</a></p>')
                for ak in i.get('attachments',[]):
                    sk=plan['sources'][ak]['source_id']; out.append(f'<p><a href="{public_url(ROUTES[lang]["register"],"source-"+sk)}">Anexo / Attachment · {sk}</a></p>')
                for other in items:
                    if other.get('source_same_as')==i['key'] or i.get('source_same_as')==other['key']:
                        oid=plan['mappings'][other['key']]['event_id'];out.append(f'<p><a href="{public_url(ROUTES[lang]["register"],"communication-"+oid)}">Fuente compartida / Shared source → {oid}</a></p>')
                out.append('</details>')
            out.append('</article>')
        out.append('</div>')
    if kind in {'caja','orion'}:
        questions_es=['¿Qué prestatario, principal, escritura y fincas integraron exactamente la financiación de Cajasiete, y qué fechas documentan aprobación, desembolso e inscripción? El recuerdo aproximado de EUR1m no está cerrado documentalmente.','¿Qué títulos, resoluciones concursales, suspensión, documentación de salida financiada/Ona, litigios y tasaciones fueron examinados, por quién y cuándo? La pregunta no presume conocimiento previo del banco.','¿Qué controles de conflictos, partes vinculadas y diligencia respaldaron las relaciones con Orion, AGM, RICPE y Acosta Matos, y qué información material facilitaron los actores históricos?','¿Cómo se concilió la inadmisión de la comunicación 6 con las propias relaciones financieras o de inversión relevantes del banco? ¿Qué examinó efectivamente el órgano independiente?','¿Se conservó, trasladó o destruyó información tras la notificación? Facilitar la base y trazabilidad no confidenciales; la información protegida corresponde a los órganos competentes.','¿Qué revisión y remisión interna siguió a las comunicaciones posteriores? ¿Se aplican a la propuesta Aweswell/Matkator criterios de título, tasación, riesgo y litigios comparables, sin exigir datos confidenciales de otros clientes?']
        questions_en=['Which borrower, principal, deed and collateral properties formed the exact Cajasiete facility, and which dates document approval, drawdown and registration? The approximate EUR1m recollection is not yet documentarily settled.','Which title documents, insolvency orders, suspension, funded-exit/Ona materials, litigation and valuations were reviewed, by whom and when? The question does not presume the bank had prior knowledge.','Which conflict, related-party and due-diligence checks supported relationships involving Orion, AGM, RICPE and Acosta Matos, and what material history did legacy actors supply?','How was inadmission of communication 6 reconciled with the bank\'s own relevant financing or investment relationships? What did the independent reviewers actually examine?','Was information retained, transferred or destroyed after the notice? Explain the non-confidential basis and audit trail; protected information belongs with competent reviewers.','What reassessment and internal referral followed later notices? Are comparable title, valuation, risk and litigation criteria applied to the Aweswell/Matkator proposal, without seeking another client\'s confidential information?']
        out.append('<h3>'+('Preguntas públicas verificables a Cajasiete' if es else 'Verifiable public questions to Cajasiete')+'</h3><ol>')
        out.extend('<li>'+html.escape(q)+'</li>' for q in (questions_es if es else questions_en));out.append('</ol>')
    if kind in {'portfolio','orion'}:
        out.append('<h3>Portfolio — '+('actuación posterior al aviso' if es else 'conduct after notice')+'</h3><p>'+('La respuesta de marzo informa de revisión concluida y posibilidad de ampliación. La respuesta de agosto confirma preservación, incorporación y revisión contextual. La cuestión comprobable es qué análisis de información material, conflictos, asesor de mercado, órganos competentes y comunicaciones regulatorias se realizó. Ni silencio total ni circulación al consejo completo se presumen.' if es else 'The March response reports a completed review and possible extension. The August response confirms preservation, incorporation and contextual review. The testable issue is what material-disclosure, conflict, market-adviser, competent-function and regulatory-liaison analysis actually occurred. Neither total silence nor circulation to the full board is presumed.')+'</p>')
    if kind in {'cnmv','orion'}:
        out.append('<h3>CNMV — '+('canales y actos separados' if es else 'separate channels and acts')+'</h3><p>'+('Los reenvíos, el acuse de infracciones y la solicitud de transparencia no se funden en un único expediente probado. La resolución del 4 de septiembre amplía el plazo: no deniega acceso ni resuelve el fondo de las alegaciones.' if es else 'The forwards, infringement-reporting acknowledgement and transparency request are not collapsed into one proved case. The 4 September decision extends the deadline: it does not refuse access or decide the allegations.')+'</p>')
    if kind=='register':
        out.append('<h3>'+('Fuentes y anexos con referencia propia' if es else 'Individually referenced sources and attachments')+'</h3><div class="notice-grid">')
        lookup={i['key']:i for i in items}; lookup.update({a['key']:a for a in spec['attachment_sources']})
        for key,s in plan['sources'].items():
            item=lookup[key]; sid=s['source_id']
            out.append(f'<article id="source-{sid}"><h4><code>{sid}</code></h4><p>{html.escape(item.get("label", item.get("es" if es else "en","")))}</p><p>{html.escape(s["source_kind"])}</p>')
            if s.get('document_id'):out.append('<p>Documento / Document: <code>'+s['document_id']+'</code> · SHA-256 <code>'+s['sha256']+'</code></p>')
            if item.get('public_excerpt'):out.append('<blockquote lang="es">'+html.escape(item['public_excerpt'])+'</blockquote>')
            if s.get('public_asset'):
                asset='/por-derecho/'+s['public_asset']; caption=('Gráfico explicativo ya existente: índice de fuentes, no hallazgo de responsabilidad. No se afirma equivalencia hash con el adjunto nativo.' if es else 'Existing explanatory figure: source index, not a liability finding. Hash equivalence with the native email attachment is not asserted.')
                out.append(f'<figure><a href="{asset}"><img src="{asset}" loading="lazy" alt="{html.escape(item["label"],quote=True)}"></a><figcaption>{caption}</figcaption></figure>')
            if item.get('route') and (ROOT/item['route']/'index.html').exists():out.append(f'<p><a href="{public_url(item["route"])}">Contexto primario / Primary-source context</a></p>')
            uses=[i for i in items if plan['mappings'][i['key']]['source_id']==sid or key in i.get('attachments',[])]
            for i in uses:
                eid=plan['mappings'][i['key']]['event_id'];out.append(f'<p><a href="{public_url(ROUTES[lang]["register"],"communication-"+eid)}">↔ {i["date"]} · {eid}</a></p>')
            out.append('</article>')
        out.append('</div>')
    if kind in {'register','orion','caja','portfolio','cnmv'}:
        out.append('<details><summary>'+('Alcance y cuestiones pendientes' if es else 'Coverage and unresolved questions')+'</summary><p>'+('20 eventos individuales; seis descriptores de anexos. No es una certificación de exhaustividad histórica.' if es else '20 individual events; six attachment descriptors. This is not a certificate of historical completeness.')+'</p><ul>')
        out.extend('<li>'+html.escape(g['es' if es else 'en'])+'</li>' for g in spec['gaps']);out.append('</ul></details>')
    out.append(f'<p><a href="/por-derecho/{REGISTER}">Canonical communications register (JSON)</a> · <a href="/por-derecho/{CROSSWALK}">Source / event crosswalk</a></p></section>'+END)
    return '\n'.join(out)

def insert_block(path: str, block: str, start=START, end=END, close='</main>') -> None:
    p=ROOT/path; text=p.read_text(encoding='utf-8')
    if start in text:
        if text.count(start)!=1 or text.count(end)!=1:raise ValueError('Nonunique managed block '+path)
        a=text.index(start);b=text.index(end,a)+len(end);text=text[:a]+block+text[b:]
    else:
        if close not in text:raise ValueError('Missing insertion point '+path)
        text=text.replace(close,block+'\n'+close,1)
    p.write_text(text,encoding='utf-8')

def render(plan: dict) -> list[str]:
    canonical=read(REGISTER); events={e['event_id']:e for e in canonical['events']}; managed=[]
    for lang,routes in ROUTES.items():
        for kind,route in routes.items():
            p=route+'index.html'
            if not (ROOT/p).exists(): raise ValueError('Canonical route missing; do not invent a replacement: '+p)
            insert_block(p,textblock(lang,kind,plan,events));managed.append(p)
    graph=read(GRAPH)
    graph['notice_control']={'control_id':CONTROL,'canonical_register':REGISTER,'crosswalk':CROSSWALK,'event_ids':[v['event_id'] for v in plan['mappings'].values()],'evidence_boundary':'Notice, review and corporate relationships do not transfer criminal responsibility.'}
    graph['notice_edges']=[{'event_id':m['event_id'],'source_id':m['source_id'],'type':'SOURCE_TO_INDIVIDUAL_EVENT','route_en':anchor('en',m['event_id']),'route_es':anchor('es',m['event_id']),'attribution_boundary':'Use the event-specific proof ceiling; receipt is not merits adoption.'} for m in plan['mappings'].values()]
    graph['internal_routes']=list(dict.fromkeys(graph.get('internal_routes',[])+['/'+r for rr in ROUTES.values() for r in rr.values()]))
    save(GRAPH,graph);managed.append(GRAPH)
    lines=[MDSTART,'\n## Atomic notice integration — 5 September 2026\n',f'Control: `{CONTROL}`. Canonical events remain in `{REGISTER}`. Allocation/source crosswalk: `{CROSSWALK}`. Source input: `{INPUT}`.\n','Scope: 20 individually evidenced events, 24 source descriptors including six attachment descriptors; two dated events use the later recipient/official source rather than an unlocated native submission. No historical completeness claim.\n','| Source input | Event | Source |\n|---|---|---|']
    for key,m in plan['mappings'].items():lines.append(f'| {key} | {m["event_id"]} | {m["source_id"]} |')
    lines += ['\nEvery source has a stable bilingual source anchor on the institutional records pages, every event its own communication anchor, and reciprocal dossier/chronology/source links. Public originals are not inferred from attachment metadata. No private email body, provider locator or private contact field is published.\n','### Limiting and contrary evidence\n','Portfolio reports review and preservation, not silence. Its relevant-functions referral does not prove full-board circulation. Cajasiete announces intended destruction, not completed destruction. CNMV extends the deadline, not a refusal or merits determination. Exact bank facility/principal/date and its relationship to the suspension/Ona chronology remain unresolved.\n',MDEND]
    p=ROOT/RECORD; old=p.read_text(encoding='utf-8');block='\n'.join(lines)
    if MDSTART in old:old=old[:old.index(MDSTART)]+block+old[old.index(MDEND)+len(MDEND):]
    else:old+='\n'+block+'\n'
    p.write_text(old,encoding='utf-8');managed.append(RECORD)
    return managed

class Links(HTMLParser):
    def __init__(self):super().__init__();self.ids=[];self.urls=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        for key in ['href','src']:
            if a.get(key,'').startswith('/por-derecho/'):self.urls.append(a[key])

def check() -> dict:
    plan=read(CROSSWALK);spec=read(INPUT); actual=read(REGISTER); generated=load_notice_events(ROOT)
    byid={e['event_id']:e for e in actual['events']}
    if len(byid)!=len(actual['events']):raise ValueError('Duplicate canonical event IDs')
    if len(generated)!=20 or any(byid.get(e['event_id'])!=e for e in generated):raise ValueError('Canonical source/event crosswalk drift')
    if len(plan['sources'])!=24:raise ValueError('Distinct source denominator drift')
    urls=set();pages=[]
    for lang,routes in ROUTES.items():
        for route in routes.values():
            p=ROOT/route/'index.html';text=p.read_text(encoding='utf-8');block=text.split(START,1)[1].split(END,1)[0]
            if re.search(r'[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}|https?://(?:mail|drive|docs)\.google',block,re.I):raise ValueError('Private locator/contact in new page block')
            q=Links();q.feed(block);urls.update(q.urls);pages.append(route)
            if route==routes['register']:
                for e in generated:
                    if q.ids.count('communication-'+e['event_id'])!=1:raise ValueError('Missing/duplicate event anchor')
                for s in plan['sources'].values():
                    if q.ids.count('source-'+s['source_id'])!=1:raise ValueError('Missing/duplicate source anchor')
    for url in urls:
        rel=url.removeprefix('/por-derecho/');path,sep,fragment=rel.partition('#');target=ROOT/path
        if target.is_dir():target=target/'index.html'
        if not target.is_file():raise ValueError('Broken added link '+url)
        if sep:
            parser=Links();parser.feed(target.read_text(encoding='utf-8'))
            if fragment not in parser.ids:raise ValueError('Broken added fragment '+url)
    for p in [INPUT,CROSSWALK]:
        s=(ROOT/p).read_text(encoding='utf-8')
        if re.search(r'[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}|https?://(?:mail|drive|docs)\.google',s,re.I):raise ValueError('Private data in '+p)
    return {'control_id':CONTROL,'status':'SCOPED_STATIC_VALIDATION_PASS','event_count':20,'source_count':24,'attachment_descriptors':6,'canonical_total':len(actual['events']),'pages_checked':pages,'unique_added_links_checked':len(urls),'existing_public_figures':len([s for s in plan['sources'].values() if s.get('public_asset')]),'input_sha256':plan['input_sha256'],'register_sha256':digest((ROOT/REGISTER).read_bytes()),'universal_completeness_claim':False,'publication_status':'NOT_A_DEPLOYMENT_CERTIFICATE','remaining_gaps':spec['gaps']}

def live_check() -> None:
    report=check(); root='https://sbu001monterecco.github.io/por-derecho/'
    targets=[REGISTER]+[r+'index.html' for r in report['pages_checked']]
    failures=[]
    for attempt in range(18):
        failures=[]
        for rel in targets:
            try:
                req=urllib.request.Request(root+rel,headers={'Cache-Control':'no-cache','User-Agent':'PorDerecho-scoped-release-verifier'})
                with urllib.request.urlopen(req,timeout=25) as response:payload=response.read()
                if rel==REGISTER:
                    if digest(payload)!=report['register_sha256']:raise ValueError('register hash not deployed')
                elif CONTROL.encode() not in payload or START.encode() not in payload:raise ValueError('release block absent')
            except Exception as exc:failures.append(rel+': '+str(exc))
        if not failures:
            print(json.dumps({'status':'LIVE_CONTENT_VERIFIED','checked_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip(),'targets':len(targets),'register_sha256':report['register_sha256']},indent=2));return
        time.sleep(10)
    raise ValueError('Live release not verified: '+'; '.join(failures))

def apply() -> None:
    plan=prepare_crosswalk(); old={e['event_id']:e for e in read(REGISTER)['events'] if e.get('source_batch_id')!=CONTROL}
    patch_pipeline()
    subprocess.run([sys.executable,str(ROOT/BUILDER),'--apply'],check=True,cwd=ROOT)
    current={e['event_id']:e for e in read(REGISTER)['events']}
    if any(current.get(k)!=v for k,v in old.items()):raise ValueError('Pre-existing canonical event changed')
    managed=render(plan)
    subprocess.run([sys.executable,str(ROOT/BUILDER),'--check'],check=True,cwd=ROOT)
    report=check(); report['existing_event_rows_preserved']=len(old)
    report['managed_files']=managed+[CROSSWALK,REGISTER,'ops/INSTITUTIONAL_COMMUNICATIONS_SCAN_CHECKPOINT.json',BUILDER,VALIDATOR,REPORT]
    save(REPORT,report)
    print(json.dumps({k:v for k,v in report.items() if k!='remaining_gaps'},ensure_ascii=False,indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode',choices=['apply','check','live'])
    args=parser.parse_args()
    try:
        if args.mode=='apply':apply()
        elif args.mode=='check':print(json.dumps(check(),ensure_ascii=False,indent=2))
        else:live_check()
    except Exception as exc:
        print('ERROR:',exc,file=sys.stderr);raise SystemExit(1)
