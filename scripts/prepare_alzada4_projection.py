#!/usr/bin/env python3
"""Deterministically prepare one current-main-based Alzada4 projection before merge.

Only explicitly listed source-control/reader paths may change. The existing
canonical control and multi-lane parent are retained; no new evidence master,
public private-source export, deployment or main mutation occurs here.
"""
from __future__ import annotations
import copy
import csv
import hashlib
import html
import io
import json
import os
from pathlib import Path
import re
import subprocess
import sys

REPO = 'sbu001monterecco/por-derecho'
BRANCH = 'publication/alzada4-source-perimeter-20261013'
PLAN = Path('governance/continuity/2026-10-13-alzada4-publication-plan.json')
CONTROL = Path('assets/data/eg17-20-26-alzada-continuity-20260924.json')
CSV_PATH = Path('archive/PROCEEDINGS_MASTER_REGISTER.csv')
MARKER = 'PD-LAJ-20-26-20260924-01::13OCT2026'
STATUS = 'ALZADA4_DISMISSED_2026_10_13_RECEIPT_29SEP_RECORDED_COMPLETE_FILE_OPEN'
BACKLINKS = [f'{lang}/{slug}/index.html' for lang in ('es','en') for slug in ('ric-private-equity-sun-park','francisco-mario-matos-matas','antonio-cogolludo-rojas','shaila-maria-cogolludo-ramos')]
BACKLINKS += ['es/patron-efectos-favorables-acosta-matos/index.html','en/pattern-favourable-effects-acosta-matos/index.html','es/index.html','en/index.html']
MD_PATHS = ['archive/THREAD_DELETION_CONTINUITY_AUDIT_EG17_20_26_ALZADA_24SEP2026.md','docs/continuity/2026-09-24-eg17-20-26-alzada.md','archive/SUN_PARK_COMUNIDAD_PROCEEDINGS_REGISTER_CANARY_ISLANDS_15AUG2026.md']
JSON_PROJECTIONS = ['assets/data/proceedings-master-public-v1.json','assets/data/community-acta-authority-interconnectivity-v1.json','assets/data/concurso36-denominator-gap-v1.json']
RECEIPT = 'governance/continuity/2026-10-13-alzada4-projection-receipt.json'
ALLOW = set(BACKLINKS + MD_PATHS + JSON_PROJECTIONS + [str(CONTROL),str(CSV_PATH),'CHATGPT_START_HERE.md','assets/alzada4-viewer.css','es/alzada-4-2026/index.html','en/alzada-4-2026/index.html',RECEIPT])

CSS = '''*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#eef1f4;color:#1e2f40;font:17px/1.65 system-ui,-apple-system,Segoe UI,sans-serif}a{color:#155276;overflow-wrap:anywhere}.wrap{max-width:1180px;margin:auto;padding:30px 24px}header{background:#172b3e;color:#fff}header a{color:#dcf0ff}.top{display:flex;justify-content:space-between;gap:20px;flex-wrap:wrap}.eyebrow{font-size:13px;letter-spacing:.07em;text-transform:uppercase;font-weight:700}h1{font-size:clamp(32px,4.5vw,57px);line-height:1.1;max-width:950px;margin:20px 0}h2{font-size:clamp(24px,3vw,33px);line-height:1.2}h3{font-size:21px}section{scroll-margin-top:20px}.card{background:white;border:1px solid #d4dde5;border-radius:10px;padding:24px;margin:24px 0}.position{border-left:6px solid #843523}.status{background:#fff2e8;border-left:5px solid #ab542b;padding:15px 18px}.actors{font-weight:650}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));gap:16px}.small{font-size:14px}.toolbar{display:flex;flex-wrap:wrap;gap:12px;align-items:center;margin:16px 0}.button{display:inline-block;padding:10px 16px;border:1px solid #6c8396;border-radius:6px;background:#fff;text-decoration:none}.pdf{width:100%;height:85vh;min-height:600px;border:1px solid #aab9c7;background:white}details{margin-top:16px}summary{font-weight:700;cursor:pointer}.paper{position:relative;width:100%;aspect-ratio:1191/1684;overflow:hidden;background:#fff;margin:14px 0 28px;box-shadow:0 3px 14px #14283b22}.strip{position:absolute;left:0;width:100%;height:500%;max-width:none}.p1{top:0}.p2{top:-100%}.p3{top:-200%}.p4{top:-300%}.p5{top:-400%}.table-scroll{overflow-x:auto}table{border-collapse:collapse;width:100%;min-width:620px;font-size:15px}th,td{text-align:left;vertical-align:top;padding:14px 12px;border-bottom:1px solid #d5dde5}th{background:#e9eef3}.timeline{list-style:none;padding:0}.timeline li{border-left:3px solid #a0b4c5;padding:0 0 20px 20px}.timeline time{font-weight:750}.bounds{background:#e8eff3;padding:17px 20px;border-radius:8px}code{font-size:12px;overflow-wrap:anywhere}footer{border-top:1px solid #bccbd6}.source-note{font-size:15px}.source-note p{margin:8px 0}@media(max-width:620px){.wrap{padding:22px 15px}.card{padding:18px}.pdf{min-height:480px;height:70vh}}@media print{header,footer,.not-print,.card:not(.source-card),.pdf,.source-intro,.toolbar,summary,.page-label{display:none!important}body,.wrap,.source-card{margin:0;padding:0;border:0;background:#fff}details{display:block;margin:0}details>*{display:block}.paper{width:210mm;height:297mm;box-shadow:none;margin:0;break-after:page}.paper:last-child{break-after:auto}@page{size:A4;margin:0}}'''


def enc(text: str) -> bytes:
    return text.encode('utf-8')


def json_bytes(obj: object) -> bytes:
    return enc(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def reader(plan: dict, lang: str) -> str:
    e = html.escape
    es = lang == 'es'
    title = 'Alzada 4/2026: resolución íntegra y exigencia de esclarecimiento institucional' if es else 'Alzada 4/2026: the complete decision and the demand for institutional accountability'
    label = lambda a,b: a if es else b
    source = '../../' + plan['source']['public_pdf_path']
    image = '../../' + plan['source']['public_raster_path']
    timeline = ''.join('<li><time>'+e(x['date'])+'</time><br>'+e(x[lang])+'</li>' for x in plan['chronology'])
    actions = ''.join('<tr id="action-'+e(x['key'])+'"><td><strong>'+e(x['priority'])+'</strong></td><td>'+e(x[lang])+'</td><td>'+e(x['owner'])+'<br><span class="small">'+e(x['state'])+'</span></td></tr>' for x in plan['actions'])
    pages = ''.join('<p class="page-label">'+label('Página','Page')+' '+str(i)+' / 5</p><figure class="paper" id="page-'+str(i)+'"><img class="strip p'+str(i)+'" src="'+image+'" loading="lazy" alt="'+label('Página íntegra','Complete page')+' '+str(i)+' / 5 — Alzada 4/2026"></figure>' for i in range(1,6))
    actorlinks = [('francisco-mario-matos-matas','Francisco Mario Matos Matas'),('antonio-cogolludo-rojas','Antonio Cogolludo Rojas'),('shaila-maria-cogolludo-ramos','Shaila María Cogolludo Ramos')]
    links = ' · '.join('<a href="../'+p+'/">'+e(n)+'</a>' for p,n in actorlinks)
    laws = ' · '.join('<a href="'+u+'" rel="noreferrer">'+n+'</a>' for u,n in zip(plan['law_sources'],['RD 1608/2005','Ley 39/2015','Ley 29/1998','Instrucción 1/2025']))
    return '<!doctype html>\n<html lang="'+lang+'"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+e(title)+' | Por Derecho</title><meta name="description" content="'+e(label('Las cinco páginas completas de la desestimación de 13 octubre 2026, con posición atribuida, límites probatorios y acciones.','All five pages of the 13 October 2026 dismissal, with the attributed position, evidential limits and actions.'))+'"><link rel="stylesheet" href="../../assets/alzada4-viewer.css"><link rel="alternate" hreflang="'+('en' if es else 'es')+'" href="../../'+('en' if es else 'es')+'/alzada-4-2026/"></head><body><header><div class="wrap"><div class="top"><a href="../">Por Derecho</a><a href="../../'+('en' if es else 'es')+'/alzada-4-2026/">'+('English' if es else 'Español')+'</a></div><p class="eyebrow">PD-LAJ-20-26-20260924-01 · GC-LAJ-021 · 13 OCT 2026</p><h1>'+e(title)+'</h1><p>'+e(label('Cinco de cinco páginas. Sin abreviar la motivación adversa. Alegación, acto institucional y responsabilidad individual permanecen diferenciados.','Five of five pages. The adverse reasoning is not abridged. Allegation, institutional act and individual responsibility remain distinct.'))+'</p><nav class="toolbar"><a href="#position">'+label('Posición','Position')+'</a><a href="#source">'+label('PDF íntegro','Complete PDF')+'</a><a href="#actions">'+label('Acciones','Actions')+'</a><a href="#chronology">'+label('Cronología','Chronology')+'</a></nav></div></header><main class="wrap"><section class="card position" id="position"><p class="eyebrow">'+label('Posición expresa del reclamante — no hallazgo judicial','Express claimant position — not a judicial finding')+'</p><h2>'+label('Captura de activos e ingresos e instrumentalización institucional alegadas','Alleged asset and income capture and institutional instrumentalisation')+'</h2><p>'+e(plan['position_'+lang])+'</p><p class="actors">'+e(plan['perimeter_'+lang])+'</p><h3>'+label('Inclusión predatoria y protección de todas las partes afectadas','Predatory inclusion and protection of all affected parties')+'</h3><p>'+e(plan['predatory_inclusion_'+lang])+'</p><p class="small">'+links+' · <a href="../ric-private-equity-sun-park/">'+label('Acosta Matos / RICPE / Sun Park: contexto existente','Acosta Matos / RICPE / Sun Park: existing context')+'</a></p></section><section class="card"><h2>'+label('Lo que sí decide la autoridad','What the authority actually decides')+'</h2><p class="status">'+e(plan['decision_summary_'+lang])+'</p><p>'+e(plan['contrary_'+lang])+'</p><div class="bounds">'+e(label('Esta publicación no declara captura institucional, corrupción, ocultación, falsedad, represalia, causalidad o responsabilidad personal como hechos probados. Tampoco diluye la posición expresa del reclamante ni trata la desestimación como exoneración de todos los hechos subyacentes.','This publication does not present institutional capture, corruption, concealment, falsity, retaliation, causation or personal liability as proved facts. Nor does it dilute the claimant’s express position or treat this dismissal as exoneration of all underlying events.'))+'</div></section><section class="card source-card" id="source"><div class="source-intro"><h2>'+label('Resolución íntegra: las cinco páginas','Complete decision: all five pages')+'</h2><p>'+e(label('Se publica un facsímil completo en PDF, no una selección de páginas. Se han retirado únicamente el código marginal y QR de recuperación y los metadatos/campos de firma no necesarios. Se conservan el texto sustantivo, los nombres en capacidad relevante, la apariencia de firma, todos los fundamentos y el pie de recurso. La copia de imagen no sustituye al original firmado.','This is a complete PDF facsimile, not a selection of pages. Only the marginal recovery code/QR and unnecessary embedded signature metadata/fields were removed. Substantive text, relevant-capacity names, visible signature appearance, every ground and the appeal notice are preserved. The image copy does not replace the signed original.'))+'</p></div><div class="toolbar"><a class="button" href="'+source+'" target="_blank" rel="noopener">'+label('Abrir las 5 páginas en PDF','Open all 5 pages as PDF')+'</a><a class="button" href="'+source+'" download>'+label('Descargar PDF completo','Download complete PDF')+'</a><a class="button" href="#page-1">'+label('Ver facsímiles sin visor PDF','View page facsimiles without PDF support')+'</a></div><object class="pdf" data="'+source+'#view=FitH" type="application/pdf" aria-label="'+label('Resolución completa de cinco páginas','Complete five-page decision')+'"><p><a href="'+source+'">'+label('Abrir el PDF completo','Open the complete PDF')+'</a></p></object><details open><summary>'+label('Alternativa accesible: visualizar cada una de las cinco páginas','Alternative view: display each of the five pages')+'</summary>'+pages+'</details></section><section class="card" id="chronology"><h2>'+label('Genealogía y estados comprobables','Genealogy and verifiable states')+'</h2><ol class="timeline">'+timeline+'</ol><p>'+e(label('La hora 20:46:23 del justificante se conserva tal como está impresa: no se le añade un huso horario no acreditado. El traslado originalmente ordenado y la remisión de la alzada no se identifican como una misma operación sin sus registros.','The receipt time 20:46:23 is retained as printed: no unverified time-zone offset is appended. The originally ordered transfer and the appeal transmission are not treated as the same operation without their records.'))+'</p></section><section class="card" id="actions"><h2>'+label('Acciones inmediatas — estado real','Immediate actions — actual status')+'</h2><p>'+e(label('La publicación prepara y conecta estas acciones; no equivale a instrucción profesional, presentación ni notificación a terceros.','Publication prepares and connects these actions; it is not a professional instruction, filing or service on third parties.'))+'</p><div class="table-scroll"><table><thead><tr><th>'+label('Prioridad','Priority')+'</th><th>'+label('Actuación','Action')+'</th><th>'+label('Responsable propuesto / estado','Proposed owner / status')+'</th></tr></thead><tbody>'+actions+'</tbody></table></div></section><section class="card source-note" id="provenance"><h2>'+label('Proveniencia, integridad y límites','Provenance, integrity and limits')+'</h2><p>'+e(label('Original: 5 páginas, 326.792 bytes; conservado sin cambios en custodia privada. La igualdad de huellas acredita consistencia binaria, no validación independiente de firma ni integridad del expediente de la autoridad.','Original: 5 pages, 326,792 bytes; preserved unchanged in private custody. Hash equality establishes byte consistency, not independent signature validation or completeness of the authority’s file.'))+'</p><p>Original SHA-256: <code>'+plan['source']['original_sha256']+'</code></p><p>PDF SHA-256: <code>'+plan['source']['public_pdf_sha256']+'</code></p><p><a href="../../evidence/public/2026-10-13-alzada4/admission-receipt.json">'+label('Manifiesto de admisión del facsímil','Facsimile admission manifest')+'</a> · <a href="../../assets/data/eg17-20-26-alzada-continuity-20260924.json">'+label('Control canónico existente actualizado','Updated existing canonical control')+'</a></p><p>'+laws+'</p></section></main><footer><div class="wrap"><strong>Por Derecho — '+label('registro fuente-controlado','source-controlled record')+'</strong><p>'+e(label('Derecho de rectificación y contraste: los hechos, alegaciones, explicaciones lícitas, resultados adversos y cuestiones abiertas deben conservarse separadamente. Publicar no es notificar, y conectar no es atribuir culpabilidad.','Correction and scrutiny: facts, allegations, lawful explanations, adverse outcomes and open questions must remain separate. Publishing is not service, and linking is not attributing guilt.'))+'</p></div></footer></body></html>\n'


def prepare() -> tuple[dict[str,bytes],dict]:
    plan = json.loads(PLAN.read_text(encoding='utf-8'))
    if plan['control_id'] != 'PD-LAJ-20-26-20260924-01' or len(set(plan['private_actors'])) != 5:
        raise ValueError('Canonical scope/actor denominator mismatch')
    for path,key,size in [(plan['source']['public_pdf_path'],'public_pdf_sha256',1583908),(plan['source']['public_raster_path'],'public_raster_sha256',1581748)]:
        raw = Path(path).read_bytes()
        if len(raw) != size or sha(raw) != plan['source'][key]:
            raise ValueError('Exact admitted source missing: '+path)
    outputs = {}
    original_control = CONTROL.read_bytes()
    control = json.loads(original_control)
    if control.get('control_id') != plan['control_id']:
        raise ValueError('Wrong existing canonical control')
    control['status'] = STATUS
    control['latest_control_date'] = plan['as_of']
    control['latest_decision'] = {**plan['source'], 'outcome':'DISMISSED', 'appeal_receipt_stated_in_decision':'2026-09-29', 'mandatory_report_text':'REPRODUCED_IN_DECISION', 'complete_administrative_file':'NOT_VERIFIED', 'native_separate_mandatory_report':'NOT_OBTAINED', 'eg38_appeal':'SEPARATE_NOT_DECIDED_BY_THIS_DISMISSAL'}
    control['current_attributed_position'] = {k:plan[k] for k in ('speaker','position_status','private_actors','position_es','position_en','perimeter_es','perimeter_en','predatory_inclusion_es','predatory_inclusion_en','output_context_rule')}
    control['public_readers'] = {'es':'/es/alzada-4-2026/','en':'/en/alzada-4-2026/','publication_state':'SOURCE_PROJECTION_NOT_DEPLOYMENT_ATTESTATION'}
    control['immediate_actions'] = plan['actions']
    appeal = control.get('filed_appeal',{})
    old_time = appeal.get('presented_at_local')
    if old_time == '2026-09-24T20:46:23+01:00':
        appeal['superseded_time_literal'] = old_time
        appeal['presented_at_local'] = '2026-09-24T20:46:23'
        appeal['time_zone_status'] = 'OFFSET_NOT_PRINTED_IN_RECEIPT_NOT_VERIFIED'
    control['latest_corrections'] = ['Provincial visible signature 21Sep; input20Sep; notification22Sep; appellate description20Sep retained as discrepancy, not falsification finding.','Receipt of appeal with report on29Sep is stated in13Oct decision; old universal forwarding/outcome-pending wording is superseded within this child appeal.','Separate EG38 follow-up draft is not sent; distinct provincial post-filing follow-up was sent.','Report text is reproduced; separately native signed report/full transmitted corpus remain open.','No new judicial appeal, service, counsel mandate or reminder is proved by publication.']
    old_gaps = control.get('open_gaps',[])
    control['open_gaps'] = ['ALZADA4_COMPLETE_INDEXED_FILE_AND_NATIVE_PROVINCIAL_REPORT' if x=='ALZADA_83460291_FORWARDING_TO_SECRETARIO_GOBIERNO_AND_ORDERED_FILE' else x for x in old_gaps]
    control['source_event_keys'] = [plan['source']['event_key'], plan['source']['notification_key']]
    outputs[str(CONTROL)] = json_bytes(control)
    text = CSV_PATH.read_text(encoding='utf-8')
    rows = list(csv.DictReader(io.StringIO(text)))
    matches = [r for r in rows if r.get('Master_ID')=='GC-LAJ-021']
    if len(matches)!=1:
        raise ValueError('Master parent denominator not one')
    row = matches[0]
    updates = {'Record_Type':'GOVERNANCE_SUPERVISION','Secondary_Reference':'Alzada 4/2026 — separately identified provincial-appeal child','Date_or_Period':'15/08/2026–13/10/2026','Status':'Alzada 4/2026 dismissed 13 Oct 2026; receipt with prescribed report on29Sep stated in decision; complete transmitted file remains unverified','Latest_Known_Event':'13/10/2026 signed dismissal and notification; complete five-page public facsimile','Appeal_or_Review':'Administrative appeal decided; judicial review notice two months; counsel/valid notification require separate verification','Primary_Source_Anchor':plan['source']['public_pdf_path'],'Repo_Canonical_Source':str(CONTROL),'Open_Reference_Gap':'Complete indexed administrative file/native prescribed provincial report; distinct transfer records; notification/preservation evidence; separate EG38 status; asset-income and individual-attribution proof','Last_Scan_Date':'2026-10-13','Notes':'Multi-lane parent retained; Alzada4/2026 is its separately identified child, not EG38 appeal or DP1901. Current attributed capture/predatory-inclusion position is an allegation, not adjudication. The report text is reproduced in the dismissal; full transmitted corpus is not verified. Filing-time offset is not source-verified.'}
    row.update(updates)
    out=io.StringIO(newline='')
    writer=csv.DictWriter(out,fieldnames=list(rows[0]),lineterminator='\n')
    writer.writeheader();writer.writerows(rows)
    outputs[str(CSV_PATH)]=enc(out.getvalue())
    projection_counts = {}
    exceptions = []
    for name in JSON_PROJECTIONS:
        p=Path(name)
        if not p.exists():
            exceptions.append(name+': not present on this host');continue
        obj=json.loads(p.read_text(encoding='utf-8'))
        count=[0]
        def visit(node):
            if isinstance(node,dict):
                own_id=node.get('Master_ID',node.get('master_id',node.get('canonical_master_id')))
                direct_registration=any(isinstance(v,str) and 'REGAGE26e00083460291' in v for v in node.values())
                if own_id=='GC-LAJ-021' or (name.endswith('concurso36-denominator-gap-v1.json') and direct_registration and 'status' in node):
                    count[0]+=1
                    for key,value in updates.items():
                        if key in node:node[key]=value
                        elif key.lower() in node:node[key.lower()]=value
                    if 'status' in node:node['status']=updates['Status']
                    node['latest_alzada4_control']={'date':'2026-10-13','reference':'Alzada 4/2026','outcome':'DISMISSED','control':str(CONTROL),'full_source':plan['source']['public_pdf_path'],'complete_authority_file':'OPEN'}
                    return
                for value in list(node.values()):visit(value)
            elif isinstance(node,list):
                for value in node:visit(value)
        visit(obj)
        projection_counts[name]=count[0]
        if count[0]:outputs[name]=json_bytes(obj)
        else:exceptions.append(name+': no unambiguous parent record matched; not rewritten')
    addendum='\n\n<!-- '+MARKER+' -->\n## 13 October 2026 — controlling Alzada 4/2026 successor\n\nThe limited provincial appeal was **dismissed on 13 October 2026**. The decision records receipt on **29 September with the prescribed report**, whose text it reproduces. The complete indexed authority file and separately native report remain open. This supersedes the older current-outcome/wholly-unverified-forwarding shorthand for this child appeal only; it does not decide the separate EG38 appeal or merge any judicial/prosecutorial route.\n\nCurrent control: `assets/data/eg17-20-26-alzada-continuity-20260924.json`. Complete five-page source: `evidence/public/2026-10-13-alzada4/decision-full-public-facsimile.pdf`. Readers: [ES](https://sbu001monterecco.github.io/por-derecho/es/alzada-4-2026/) / [EN](https://sbu001monterecco.github.io/por-derecho/en/alzada-4-2026/). Native original remains private; public copy is a privacy-only image facsimile, not the signed original.\n\n'+plan['position_en']+'\n\n'+plan['perimeter_en']+'\n\n'+plan['predatory_inclusion_en']+'\n\nPreserve the source adverse reasoning and lawful alternatives. Publication does not establish underlying guilt, complete administrative-file production, counsel instruction, filing, service or production RAG ingestion. Source projection, merge and verified deployment remain separate states.\n'
    for name in MD_PATHS:
        p=Path(name)
        if not p.exists():exceptions.append(name+': not present');continue
        text=p.read_text(encoding='utf-8')
        if MARKER not in text:outputs[name]=enc(text+addendum)
    p=Path('CHATGPT_START_HERE.md')
    text=p.read_text(encoding='utf-8')
    if MARKER not in text:
        banner='<!-- '+MARKER+' -->\n> **13-Oct-2026 Alzada4 / existing PD-LAJ-20-26-20260924-01 update:** first read `assets/data/eg17-20-26-alzada-continuity-20260924.json` and `governance/continuity/2026-10-13-alzada4-publication-plan.json`. Alzada4 is DISMISSED;29Sep receipt/report text are recorded, complete file is OPEN. Preserve the strong attributed administrative-capture, asset/income and predatory-inclusion position, the five named private actors and all evidenced affected rights; never convert it into an official finding or guilt by association. Full five-page privacy facsimile/readers are linked in that existing control. GitHub paths must be host-qualified when absent from private GitLab; no private sources or counsel advice are published.\n\n'
        outputs[str(p)]=enc(banner+text)
    outputs['assets/alzada4-viewer.css']=enc(CSS+'\n')
    for lang in ('es','en'):
        outputs[f'{lang}/alzada-4-2026/index.html']=enc(reader(plan,lang))
    linked=[]
    for name in BACKLINKS:
        p=Path(name)
        if not p.exists():exceptions.append(name+': optional backlink target not present');continue
        text=p.read_text(encoding='utf-8')
        if MARKER in text:continue
        lang=name.split('/')[0]
        prefix='alzada-4-2026/' if name==lang+'/index.html' else '../alzada-4-2026/'
        heading='13 octubre: resolución íntegra y posición sobre captura institucional' if lang=='es' else '13 October: full decision and the institutional-capture allegation'
        message='Gil Marer y AWESWELL sostienen una captura ilícita continuada de activos e ingresos e instrumentalización institucional en el perímetro Sun Park. El núcleo privado identificado comprende a '+', '.join(plan['private_actors'])+'. La inclusión predatoria alegada abarca a participantes posteriores potencialmente desinformados o afectados; la conexión no prueba culpabilidad. La desestimación y sus cinco páginas adversas se conservan íntegramente.' if lang=='es' else 'Gil Marer and AWESWELL allege continuing illicit asset and income capture and institutional instrumentalisation in the Sun Park perimeter. The identified private core comprises '+', '.join(plan['private_actors'])+'. Alleged predatory inclusion encompasses potentially uninformed or affected later participants; connection does not prove guilt. The dismissal and all five adverse source pages are retained in full.'
        block='\n<!-- '+MARKER+' -->\n<section data-pd-alzada4-update="2026-10-13" style="margin:24px auto;padding:22px;max-width:1180px;border:1px solid #bbc9d4;border-left:5px solid #843523;background:#f5f7f9;color:#182b3d"><h2>'+html.escape(heading)+'</h2><p>'+html.escape(message)+'</p><p><a href="'+prefix+'">'+('Leer la posición, el PDF completo y las acciones' if lang=='es' else 'Read the position, complete PDF and actions')+'</a></p></section>\n'
        starts=list(re.finditer(r'<main\b[^>]*>',text,re.I))
        if len(starts)!=1:
            exceptions.append(name+': main element not uniquely identified; not edited');continue
        pos=starts[0].end()
        outputs[name]=enc(text[:pos]+block+text[pos:]);linked.append(name)
    if not set(outputs).issubset(ALLOW):raise ValueError('Output allowlist violation')
    # Reject accidental private provider/identifier payloads in new position/readers.
    for name in ['es/alzada-4-2026/index.html','en/alzada-4-2026/index.html']:
        value=outputs[name].decode('utf-8')
        for token in ['Y2231410X','1a1347d83ada3eeb','1vKuhUiw5v8fWN8EAEp5qEpt5unH3IgCs','secgob.tsjc@','E04799402-PF:ZXJJ']:
            if token in value:raise ValueError('Private source locator leaked: '+name)
        if value.count('class="paper"')!=5 or '<object class="pdf"' not in value:
            raise ValueError('Complete viewer contract failed')
        for actor in plan['private_actors']:
            if html.escape(actor) not in value:raise ValueError('Private actor context missing')
    receipt={'control_id':plan['control_id'],'date':'2026-10-13','status':'PREMERGE_PROJECTION_PREPARED_NOT_DEPLOYMENT','master_parent_count':1,'source_pages':5,'private_actor_count':5,'projection_matches':projection_counts,'backlinks':linked,'exceptions':exceptions,'files':[{'path':k,'bytes':len(v),'sha256':sha(v)} for k,v in sorted(outputs.items())]}
    outputs[RECEIPT]=json_bytes(receipt)
    return outputs,receipt


def gh(endpoint,method='GET',payload=None):
    args=['gh','api','--method',method,'repos/'+REPO+'/'+endpoint]
    data=None
    if payload is not None:args+=['--input','-'];data=json_bytes(payload)
    done=subprocess.run(args,input=data,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=90,check=False)
    if done.returncode:raise RuntimeError(endpoint+': '+done.stderr.decode('utf-8','replace')[:700])
    return json.loads(done.stdout)


def main():
    outputs,receipt=prepare()
    if '--commit' not in sys.argv:
        for name,raw in outputs.items():
            p=Path(name);p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
        print(json.dumps(receipt,ensure_ascii=False,indent=2));return
    if os.environ.get('GITHUB_REPOSITORY')!=REPO or os.environ.get('GITHUB_REF')!='refs/heads/'+BRANCH:
        raise RuntimeError('Commit refused outside exact non-main branch')
    expected=os.environ['GITHUB_SHA']
    head=gh('git/ref/heads/'+BRANCH)['object']['sha']
    if head!=expected:raise RuntimeError('Branch lease changed')
    commit=gh('git/commits/'+head)
    changed={name:raw for name,raw in outputs.items() if not Path(name).exists() or Path(name).read_bytes()!=raw}
    if not changed:print('No unique projection delta');return
    if not set(changed).issubset(ALLOW):raise ValueError('Output scope violation')
    entries=[]
    import base64
    for name,raw in sorted(changed.items()):
        blob=gh('git/blobs','POST',{'content':base64.b64encode(raw).decode('ascii'),'encoding':'base64'})
        expected_blob=hashlib.sha1(b'blob '+str(len(raw)).encode('ascii')+b'\0'+raw).hexdigest()
        if blob['sha']!=expected_blob:raise RuntimeError('Blob byte identity failed: '+name)
        entries.append({'path':name,'mode':'100644','type':'blob','sha':blob['sha']})
    tree=gh('git/trees','POST',{'base_tree':commit['tree']['sha'],'tree':entries})
    new=gh('git/commits','POST',{'message':'Reconcile Alzada4 source, attributed capture position and existing canonical projections','tree':tree['sha'],'parents':[head]})
    if gh('git/ref/heads/'+BRANCH)['object']['sha']!=head:raise RuntimeError('Branch moved; refusing ref mutation')
    gh('git/refs/heads/'+BRANCH,'PATCH',{'sha':new['sha'],'force':False})
    if gh('git/ref/heads/'+BRANCH)['object']['sha']!=new['sha']:raise RuntimeError('Readback mismatch')
    print(json.dumps({'new_head':new['sha'],'files':list(changed),'exceptions':receipt['exceptions'],'status':'NON_MAIN_PROJECTION_COMMITTED'},ensure_ascii=False,indent=2))


if __name__=='__main__':main()
