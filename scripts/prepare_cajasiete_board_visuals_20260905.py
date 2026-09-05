#!/usr/bin/env python3
"""Bounded additive CajaSiete release. No email, private-source upload or merge.
Apply on a reviewed branch; the existing event/media registers stay authoritative.
"""
from __future__ import annotations
import argparse,copy,hashlib,html,json,re,subprocess,sys,textwrap,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CONTROL='PD-CAJASIETE-BOARD-VISUALS-20260905'
INPUT='ops/cajasiete-board-source-input-20260905.json'
CROSS='ops/CAJASIETE_BOARD_VISUAL_CROSSWALK_20260905.json'
REPORT='ops/CAJASIETE_BOARD_VISUAL_ACCEPTANCE_20260905.json'
REG='assets/data/institutional-communications-register-v1.json'
MEDIA='data/digital-media-asset-register-v1.json'
BUILDER='scripts/reconcile_institutional_communications.py'
START='<!-- CAJASIETE-BOARD-VISUALS-20260905:START -->'
END='<!-- CAJASIETE-BOARD-VISUALS-20260905:END -->'
BASE='/por-derecho/'
ROUTES={
'es':{'caja':'es/cajasiete-sun-park-financiacion-comparabilidad/','register':'es/registros-institucionales/','orion':'es/orion-rental-socimi/','media':'es/registro-activos-digitales/'},
'en':{'caja':'en/cajasiete-sun-park-financing-comparability/','register':'en/institutional-records/','orion':'en/orion-rental-socimi/','media':'en/digital-media-asset-register/'}}
SPEC={'control_id':CONTROL,'source_boundary':'Reviewed minimised descriptors; retained native messages and access credentials are not published. Descriptor hashes are not native-message hashes.','items':[
{'key':'CAJASIETE-RECEIPT-20260409','date':'2026-04-09','type':'INSTITUTIONAL_ACKNOWLEDGEMENT','direction':'INBOUND_FROM_INSTITUTION','reference':'Communication 6','en':"Cajasiete's reporting channel acknowledged receipt of communication 6.",'es':'El canal de información de Cajasiete acusó recibo de la comunicación 6.','limit_en':'Receipt does not establish the complete submission or attachment inventory, formal admissibility, substantive review, board circulation or the truth of allegations. Access credentials are withheld.','limit_es':'El acuse no acredita el contenido íntegro o inventario de anexos, admisión formal, examen sustantivo, circulación al consejo ni veracidad de las alegaciones. Se excluyen las credenciales de acceso.'},
{'key':'CAJASIETE-FORWARD-20260827','date':'2026-08-27','type':'OUTBOUND_COMMUNICATION','direction':'OUTBOUND_TO_INSTITUTION','reference':'Separate forwarding of financing enquiry','en':'Gil separately forwarded the genuine financing meeting request through previously used institutional channels, asking for acknowledgement and internal referral to the appropriate functions.','es':'Gil reenvió separadamente la solicitud real de reunión de financiación por los canales institucionales utilizados, pidiendo acuse y remisión interna a las funciones competentes.','limit_en':'A separate sent forwarding does not establish receipt, circulation to named officers, a meeting, a credit decision, refusal or retaliation. It remains separate from protected-channel handling.','limit_es':'El reenvío enviado no acredita recepción, circulación a los cargos indicados, reunión, decisión crediticia, denegación ni represalia. Se mantiene separado de la gestión del canal de información.'}],
'reused_events':['PD-SP-EVT-0168','PD-SP-EVT-0169','PD-SP-EVT-0170','PD-SP-EVT-0176'],
'open_proof':['Complete original submission and attachment inventory','Conflict screening and reasons for inadmission','Lawful retention, anonymisation, transfer and deletion audit','Exact borrower, facility, advances, title, collateral, valuation and third-party rights','Earlier knowledge and later conduct must be separately proved; relationships do not transfer responsibility']}
def raw(v):return (json.dumps(v,ensure_ascii=False,indent=2,sort_keys=True)+'\n').encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads((ROOT/p).read_text())
def save(p,v):
 p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw(v))
def url(lang,key,fragment=''):return BASE+ROUTES[lang][key]+('#'+fragment if fragment else '')
def used(prefix):
 pat=re.compile(re.escape(prefix)+r'(\d{4})\b');out=set()
 for p in ROOT.rglob('*'):
  if not p.is_file() or '.git' in p.parts or p.suffix not in {'.json','.md','.html','.js','.py','.csv','.yml','.yaml','.txt','.svg'} or p.stat().st_size>4_000_000:continue
  out.update(int(n) for n in pat.findall(p.read_text(errors='ignore')))
 return out
def allocate(prefix,seen):
 for i in range(1,10000):
  if i not in seen:seen.add(i);return prefix+f'{i:04d}'
 raise ValueError('namespace exhausted')
def plan():
 save(INPUT,SPEC)
 if (ROOT/CROSS).exists():
  x=read(CROSS);assert x['input_sha256']==sha((ROOT/INPUT).read_bytes()),'descriptor drift';return x
 e,s,d=used('PD-SP-EVT-'),used('PD-SP-SRC-'),used('PD-DMA-');current=read(REG)
 assert not any(x.get('source_batch_id')==CONTROL for x in current['events']),'cohort without crosswalk'
 x={'control_id':CONTROL,'input_sha256':sha((ROOT/INPUT).read_bytes()),'canonical_register':REG,'baseline_event_count':len(current['events']),'events':{},'assets':{},'baseline_pages':{},'universal_completeness_claim':False}
 for i in SPEC['items']:x['events'][i['key']]={'event_id':allocate('PD-SP-EVT-',e),'source_id':allocate('PD-SP-SRC-',s)}
 for lang in ['es','en']:
  for n in [1,2,3]:x['assets'][f'{lang}-{n}']=allocate('PD-DMA-',d)
  for k in ['caja','register','orion','media']:
   rel=ROUTES[lang][k]+'index.html';assert (ROOT/rel).exists(),rel;x['baseline_pages'][rel]=sha((ROOT/rel).read_bytes())
 save(CROSS,x);return x
def load_cajasiete_events(root):
 spec=json.loads((root/INPUT).read_text());x=json.loads((root/CROSS).read_text());assert x['input_sha256']==sha((root/INPUT).read_bytes());out=[]
 for i in spec['items']:
  m=x['events'][i['key']];state={k:'NOT_ESTABLISHED_BY_THIS_SOURCE' for k in ['transmission','registration','filing','destination','delivery','internal_association','substantive_examination','merits']}
  state.update(transmission='SOURCE_TRANSMISSION_OR_ACT_RETAINED',destination='STATED_IN_SOURCE',merits='NO_MERITS_FINDING_OR_CRIMINAL_ATTRIBUTION')
  if i['direction'].startswith('INBOUND'):state['delivery']='CHANNEL_RECEIPT_ACKNOWLEDGED';state['registration']='CHANNEL_REFERENCE_IN_NOTICE'
  out.append({'event_id':m['event_id'],'cohort':'CURATED_SOURCE_PROVED_EVENT','layer':'OFFICIAL_ACT_OR_CORRESPONDENCE','source_key':i['key'],'record_type':i['type'],'event_date':i['date'],'direction':i['direction'],'channel':'EMAIL','office':'Cajasiete','institution_key':'CAJASIETE','official_reference':i['reference'],'matter_references':['Sun Park / MYND Yaiza','Aweswell Limited / Matkator',m['source_id']],'source_batch_id':CONTROL,'source_integrity':{'status':'RETAINED_NATIVE_EMAIL; PUBLIC_SAFE_REVIEW_DESCRIPTOR','repository_anchor':INPUT,'sha256':x['input_sha256']},'evidence_state':state,'public_summary':i['en'],'public_summary_es':i['es'],'proves':[i['en']],'proves_es':i['es'],'does_not_prove':[i['limit_en']],'does_not_prove_es':i['limit_es'],'canonical_anchor_en':ROUTES['en']['register']+'#communication-'+m['event_id'],'canonical_anchor_es':ROUTES['es']['register']+'#communication-'+m['event_id'],'source_timezone':'CALENDAR_DATE_ONLY; no time or timezone inferred','criminal_responsibility_transfer':False,'public_derivative_state':'PUBLIC_SAFE_MINIMISED_DERIVATIVE','attribution_state':'INSTITUTIONAL_NOTICE_NO_PERSONAL_SIGNATORY_ASSERTED','linked_transport_event_ids':['PD-SP-EVT-0176'] if i['direction'].startswith('OUTBOUND') else [],'transport_link_state':'SEPARATE_SOURCE_PROVED_COMMUNICATION','proof_level':'RETAINED_RECEIVED_EMAIL' if i['direction'].startswith('INBOUND') else 'RETAINED_SENT_EMAIL'})
 return out
COPY={
'es':{
 'tag':'POR DERECHO  /  CAJASIETE  /  LECTURA DOCUMENTAL',
 'titles':['¿Qué se examinó antes de anunciar la destrucción?','Mismo complejo hotelero. Derechos distintos.','La reputación se protege con una respuesta verificable'],
 'kicker':['GARANTÍAS · RECEPCIÓN · DECISIÓN','¿QUÉ SE ACEPTÓ COMO GARANTÍA?','CONSEJO · CUMPLIMIENTO · RIESGOS'],
 'timeline':[('10 DIC 2025','Independencia asegurada','El banco afirmó independencia, confidencialidad e inhibición o reasignación ante potenciales conflictos.'),('9 ABR 2026','Comunicación recibida','El canal acusó recibo. El acuse no demuestra admisión ni examen sustantivo.'),('28 ABR 2026','Inadmisión comunicada','Se anunció la destrucción de la información «en cumplimiento de la normativa aplicable».')],
 'q1':'¿Qué se comprobó, quién decidió y qué trazabilidad se conserva?',
 'limit1':'Destrucción anunciada, no acreditada. Legalidad y alcance pendientes de verificación.',
 'asset':[('1  RESULTADO Y EXPLOTACIÓN','Hotel, ingresos y derechos de terceros: identificar cada derecho; no tratar todo el complejo como un único patrimonio.'),('2  GARANTÍA Y TÍTULO','Cargas hipotecarias reseñadas → fincas concretas → títulos y segregación CAMSA/HNT. Prestatario, desembolso y valoración siguen abiertos.'),('3  AUTORIDAD Y CONTROL PREVIOS','Contrastar los documentos y decisiones que hicieron posible ese resultado. La hipótesis criminal de Gil Marer requiere prueba actor por actor.')],
 'oriontitle':'ORION: RELACIÓN SEPARADA','orion':'Cajasiete ↔ Orion ↔ Grupo Patrimonial Acosta Matos. Coaccionariado descrito; no es una transmisión del hotel a Orion ni prueba de coordinación.',
 'limit2':'Hipoteca ≠ principal desembolsado. Aviso posterior ≠ conocimiento anterior. Proximidad ≠ responsabilidad.',
 'checks':[('INDEPENDENCIA','¿Qué controles de conflicto y reasignación se aplicaron?'),('EXAMEN','¿Qué se revisó y qué sustentó cada motivo de inadmisión?'),('EXPOSICIÓN DEL BANCO','¿Se examinaron de forma independiente títulos, financiación y relaciones relevantes?'),('TRAZABILIDAD','¿Qué registro lícito se conserva de recepción, revisión, decisión, traslado, anonimización o borrado?')],
 'limit3':'Evaluación independiente · respuesta motivada · preservación lícita · corrección cuando proceda.',
 'intro':'La gestión del canal de información se examina por sus propios documentos. La consulta comercial genuina continúa separada: ninguna financiación se exige a cambio de silencio, y una denegación no demuestra una infracción.',
 'allegation':'Posición atribuida de Gil Marer: denuncia un mecanismo criminal organizado, coordinado y continuado que habría conectado autoridad de la Comunidad, deuda/voto, acceso, concurso, título, explotación y beneficio. No es una declaración judicial de culpabilidad. Para Cajasiete se exige probar por separado información recibida, conocimiento, conducta, deber aplicable y contribución; una relación mercantil no transmite responsabilidad.',
 'legal':'La Ley 2/2023 contempla límites de ámbito y reglas de conservación, supresión y anonimización. Su aplicación concreta exige el expediente: el anuncio de borrado no prueba por sí solo una infracción.',
 'open':'Siguen abiertos el contenido y anexos de la presentación original, la evaluación de conflictos y de admisión, el registro de conservación/borrado y los documentos exactos de financiación, título y garantías.',
 'head':'Consejo, cumplimiento y riesgos: tres preguntas documentadas','sources':'Fuentes y límites','openpng':'Abrir PNG a resolución completa','vector':'Versión vectorial','register':'Registro de comunicaciones','media':'Identidad exacta de los gráficos','old':'Consulta comercial original — conservada por separado'},
'en':{
 'tag':'POR DERECHO  /  CAJASIETE  /  DOCUMENTARY REVIEW',
 'titles':['What was examined before destruction was announced?','One hotel complex. Distinct rights.','Protect reputation with a verifiable response'],
 'kicker':['ASSURANCES · RECEIPT · DECISION','WHAT WAS ACCEPTED AS SECURITY?','GOVERNING BODY · COMPLIANCE · RISK'],
 'timeline':[('10 DEC 2025','Independence assured','The bank stated independence, confidentiality and recusal or reassignment for potential conflicts.'),('9 APR 2026','Communication received','The channel acknowledged receipt. Receipt does not establish admission or substantive examination.'),('28 APR 2026','Inadmission communicated','Destruction of the information was announced, subject to the applicable rules.')],
 'q1':'What was checked, who decided, and what audit trail remains?',
 'limit1':'Destruction announced, not established. Lawfulness and scope remain to be verified.',
 'asset':[('1  OUTCOME AND OPERATION','Hotel, income and third-party rights: identify each right; do not treat the entire complex as one estate.'),('2  SECURITY AND TITLE','Reported mortgage charges → exact properties → titles and CAMSA/HNT segregation. Borrower, advances and valuation remain open.'),('3  EARLIER AUTHORITY AND CONTROL',"Test the documents and decisions that enabled the outcome. Gil Marer's criminal allegation requires actor-specific evidence.")],
 'oriontitle':'ORION: A SEPARATE RELATIONSHIP','orion':'Cajasiete ↔ Orion ↔ Grupo Patrimonial Acosta Matos. Reported co-shareholding; not a transfer of the hotel into Orion or proof of coordination.',
 'limit2':'Mortgage ≠ cash advanced. Later notice ≠ earlier knowledge. Proximity ≠ responsibility.',
 'checks':[('INDEPENDENCE','What conflict screening and reassignment safeguards were applied?'),('EXAMINATION','What was reviewed and what supported each inadmission ground?'),('BANK EXPOSURE','Were title, financing and relevant relationships independently assessed?'),('TRACEABILITY','What lawful record remains of receipt, review, decision, transfer, anonymisation or deletion?')],
 'limit3':'Independent assessment · reasoned response · lawful preservation · correction where warranted.',
 'intro':'Reporting-channel handling is examined on its own documentary basis. The genuine commercial enquiry remains separate: financing is not demanded in exchange for silence, and a refusal does not establish wrongdoing.',
 'allegation':"Gil Marer's attributed position alleges an organised, coordinated and continuing criminal mechanism connecting Community authority, debt/voting, access, insolvency, title, operation and benefit. This is not an adjudicated finding of guilt. For Cajasiete, information received, knowledge, conduct, any applicable duty and contribution must be proved separately; commercial relationships do not transfer responsibility.",
 'legal':'Law 2/2023 includes scope limits and retention, deletion and anonymisation rules. Their application here requires the file: an announced deletion does not by itself prove a breach.',
 'open':'The original submission and attachments, conflict/admissibility assessment, retention/deletion audit, and exact financing, title and security documents remain open evidence.',
 'head':'Governing body, compliance and risk: three documentary questions','sources':'Sources and limits','openpng':'Open full-resolution PNG','vector':'Vector version','register':'Communications register','media':'Exact graphic identities','old':'Original commercial enquiry — preserved separately'}}
def vector(lang,n,logical,x):
 c=COPY[lang];out=[];H=1740 if n==2 else 1640
 def box(y,h,fill='#ffffff',stroke='#d8e1e7'):out.append(f'<rect x="56" y="{y}" width="968" height="{h}" rx="20" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
 def txt(text,y,size=38,bold=False,colour='#152d3b',width=42,xpos=84):
  for line in textwrap.wrap(text,width=width,break_long_words=False,break_on_hyphens=False):
   out.append(f'<text x="{xpos}" y="{y}" font-family="DejaVu Sans,Arial,sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" fill="{colour}">{html.escape(line)}</text>');y+=int(size*1.26)
  return y
 out.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="{H}" viewBox="0 0 1080 {H}" role="img" aria-labelledby="title desc"><title id="title">{html.escape(c["titles"][n-1])}</title><desc id="desc">Documentary infographic; questions and evidence states, not a finding of wrongdoing.</desc><rect width="1080" height="{H}" fill="#f1f5f7"/><rect width="1080" height="300" fill="#132b3a"/>')
 txt(c['tag'],48,22,True,'#d4e5ed',80,56);txt(c['titles'][n-1],115,55,True,'#ffffff',31,56);txt(c['kicker'][n-1],270,25,True,'#f3c35c',65,56)
 if n==1:
  ids=['PD-SP-EVT-0169',x['events']['CAJASIETE-RECEIPT-20260409']['event_id'],'PD-SP-EVT-0170']
  for i,(date,title,body) in enumerate(c['timeline']):
   y=332+i*294;box(y,270);out.append(f'<a href="{url(lang,"register","communication-"+ids[i])}">');txt(date+'  ·  '+ids[i],y+42,26,True,'#825d0b',65);out.append('</a>');txt(title,y+98,42,True,width=37);txt(body,y+150,35,width=45)
  box(1220,300,'#fff3d5','#d4a33e');txt(c['q1'],1275,39,True,width=42);txt(c['limit1'],1430,31,width=51)
 elif n==2:
  for i,(title,body) in enumerate(c['asset']):
   y=328+i*294;box(y,272);txt(title,y+43,29,True,'#825d0b',52);txt(body,y+103,35,width=45)
  box(1220,282,'#e5eff6','#7492a5');txt(c['oriontitle'],1270,31,True,width=47);txt(c['orion'],1322,35,width=45);txt(c['limit2'],1557,32,True,width=48,xpos=56)
 else:
  for i,(title,body) in enumerate(c['checks']):
   y=332+i*250;box(y,230);txt(title,y+49,30,True,'#825d0b',55);txt(body,y+109,38,width=42)
  box(1360,162,'#fff3d5','#d4a33e');txt(c['limit3'],1412,32,True,width=50)
 txt(logical+'  ·  '+CONTROL,H-64,19,False,'#415666',100,56)
 txt('Fuentes y límites en el dossier · No acredita culpabilidad' if lang=='es' else 'Sources and limits in the dossier · Not a finding of guilt',H-27,24,True,'#415666',85,56)
 out.append('</svg>');return '\n'.join(out)+'\n'
CSS='''<style>.caja-board{max-width:1120px;margin:2rem auto;padding:1.25rem;box-sizing:border-box;color:#172b35;background:#f4f7f9;border:1px solid #cfdae0;border-radius:16px;line-height:1.6}.caja-board *{box-sizing:border-box}.caja-board h2{font-size:clamp(1.55rem,4vw,2.2rem)}.caja-board h3{font-size:1.35rem}.caja-board p,.caja-board a,.caja-board code{overflow-wrap:anywhere}.caja-board nav{display:flex;flex-wrap:wrap;gap:.8rem}.caja-board figure{background:white;border:1px solid #ccd8df;border-radius:12px;padding:1rem;margin:1.2rem 0}.caja-board img{display:block;width:100%;max-width:650px;height:auto;margin:auto}.caja-board figcaption{font-size:1rem;padding-top:1rem}.caja-board .caja-boundary{background:#fff5df;border-left:5px solid #b18128;padding:1rem}.caja-board .caja-source{border-top:1px solid #ccd8df;padding-top:1rem}.caja-board :target{outline:3px solid #a4731f;outline-offset:3px}@media(max-width:600px){.caja-board{margin:1rem .25rem;padding:.85rem}.caja-board figure{padding:.5rem}.caja-board figcaption{font-size:1rem}}</style>'''
def block(rel,body,position='end'):
 p=ROOT/rel;t=p.read_text();b=START+CSS+body+END
 if START in t:
  assert t.count(START)==1 and t.count(END)==1;t=t[:t.index(START)]+b+t[t.index(END)+len(END):]
 else:
  if position=='top':
   m=re.search(r'<main\b[^>]*>',t);assert m,rel;t=t[:m.end()]+b+t[m.end():]
  else:assert '</main>' in t,rel;t=t.replace('</main>',b+'</main>',1)
 p.write_text(t)
def source_links(lang,x):
 items=[('10 diciembre 2025' if lang=='es' else '10 December 2025','PD-SP-EVT-0169'),('9 abril 2026' if lang=='es' else '9 April 2026',x['events']['CAJASIETE-RECEIPT-20260409']['event_id']),('28 abril 2026' if lang=='es' else '28 April 2026','PD-SP-EVT-0170')]
 return ' · '.join(f'<a href="{url(lang,"register","communication-"+i)}">{d} — {i}</a>' for d,i in items)
def render(x):
 import cairosvg
 media=read(MEDIA);oldlogical=copy.deepcopy(media['logical_assets']);oldfiles=copy.deepcopy(media['files']);files=[];logical=[]
 for lang in ['es','en']:
  c=COPY[lang]
  for n in [1,2,3]:
   identity=x['assets'][f'{lang}-{n}'];stem=f'assets/media/cajasiete-board-{n}-{lang}-20260905';svg=vector(lang,n,identity,x);p=ROOT/(stem+'.svg');p.parent.mkdir(parents=True,exist_ok=True);p.write_text(svg);cairosvg.svg2png(bytestring=svg.encode(),write_to=str(ROOT/(stem+'.png')))
   logical.append({'reference':identity,'family_id':'PD-DMA-FAM-CAJASIETE-001','title':c['titles'][n-1],'language':lang,'edition':'DOCUMENTARY_BOARD_COMPLIANCE_READER','publication_status':'PUBLICATION_AUTHORISED','web_file':identity+'^','outreach_png':identity+'-PNG^','sources':['PD-SP-SRC-0014','PD-SP-SRC-0015',x['events']['CAJASIETE-RECEIPT-20260409']['source_id']] if n==1 else ['SRC-CAJASIETE-DOSSIER-20260905','SRC-CAJASIETE-BOE-20260905'],'factual_status':'SOURCE_BOUNDED_SUMMARIES_AND_OPEN_QUESTIONS; NOT_A_FINDING','required_disclaimer':c[f'limit{n}'],'generation_method':'Deterministic source-controlled SVG typesetting and CairoSVG 2.8.2 PNG rendering; no fabricated document or portrait','correction_state':'NEW_ADDITIVE_READER','parent_asset':None,'material_limits':SPEC['open_proof']})
   for ext,mime,ref in [('svg','image/svg+xml',identity+'^'),('png','image/png',identity+'-PNG^')]:
    rel=stem+'.'+ext;b=(ROOT/rel).read_bytes();files.append({'reference':ref,'logical_asset':identity,'role':'PUBLIC_WEB_VECTOR' if ext=='svg' else 'PUBLIC_OUTREACH_PNG','repository_path':rel,'public_url':'/'+rel,'mime':mime,'viewbox_width':1080,'viewbox_height':1740 if n==2 else 1640,'bytes':len(b),'sha256':sha(b),'repository_mirror':True,'publication_status':'PUBLICATION_AUTHORISED','factual_status':'NOT_AN_ADJUDICATED_FINDING','source_control':INPUT})
  figures=[]
  for n in [1,2,3]:
   stem=f'assets/media/cajasiete-board-{n}-{lang}-20260905';figures.append(f'<figure id="caja-visual-{n}"><h3>{html.escape(c["titles"][n-1])}</h3><a href="{BASE+stem}.png"><img src="{BASE+stem}.png" width="1080" height="{1740 if n==2 else 1640}" loading="lazy" alt="{html.escape(c["titles"][n-1]+". "+c[f"limit{n}"])}"></a><figcaption><strong>{x["assets"][f"{lang}-{n}"]}</strong> · <a href="{BASE+stem}.png">{c["openpng"]}</a> · <a href="{BASE+stem}.svg">{c["vector"]}</a><p>{html.escape(c[f"limit{n}"])}</p></figcaption></figure>')
  transcript=''.join(f'<p><strong>{html.escape(d+" — "+t)}</strong>: {html.escape(b)}</p>' for d,t,b in c['timeline'])
  transcript+=''.join(f'<p><strong>{html.escape(t)}</strong>: {html.escape(b)}</p>' for t,b in c['asset'])+f'<p><strong>{c["oriontitle"]}</strong>: {html.escape(c["orion"])}</p>'
  transcript+=''.join(f'<p><strong>{html.escape(t)}</strong>: {html.escape(b)}</p>' for t,b in c['checks'])
  branchlabel='Orion: rama corporativa separada' if lang=='es' else 'Orion: separate corporate branch';questions='Preguntas existentes sobre financiación y título' if lang=='es' else 'Existing financing/title questions'
  body=f'<section class="caja-board" id="board-compliance"><p>{CONTROL}</p><h2>{c["head"]}</h2><p>{c["intro"]}</p><nav><a href="#caja-visual-1">1 · {c["kicker"][0]}</a><a href="#caja-visual-2">2 · {c["kicker"][1]}</a><a href="#caja-visual-3">3 · {c["kicker"][2]}</a><a href="#caja-commercial-original">{c["old"]}</a></nav><p class="caja-boundary">{c["allegation"]}</p>'+''.join(figures)+f'<section class="caja-source" id="board-source-record"><h3>{c["sources"]}</h3><p>{source_links(lang,x)}</p><p><a href="https://www.boe.es/diario_borme/txt.php?id=BORME-C-2022-7271">BORME-C-2022-7271 · CAMSA / HNT</a> · <a href="{url(lang,"orion")}">{branchlabel}</a> · <a href="#notice-20260905">{questions}</a></p><p>{c["legal"]} <a href="https://www.boe.es/buscar/act.php?id=BOE-A-2023-4513">Ley 2/2023 — BOE</a></p><p>{c["open"]}</p><details><summary>Texto accesible / Accessible text</summary>{transcript}</details><nav><a href="{url(lang,"register","cajasiete-board-records")}">{c["register"]}</a><a href="{url(lang,"media","cajasiete-board-assets")}">{c["media"]}</a><a href="{BASE+REG}">Canonical JSON</a></nav></section></section><span id="caja-commercial-original"></span>'
  block(ROUTES[lang]['caja']+'index.html',body,'top');records=[]
  for i in SPEC['items']:
   m=x['events'][i['key']];records.append(f'<article id="communication-{m["event_id"]}"><h3>{i["date"]} · {m["event_id"]}</h3><p>{html.escape(i[lang])}</p><p>{html.escape(i["limit_"+lang])}</p><p id="source-{m["source_id"]}">{m["source_id"]} · retained native email / minimised descriptor. <a href="{BASE+INPUT}">Source control</a></p></article>')
  block(ROUTES[lang]['register']+'index.html',f'<section class="caja-board" id="cajasiete-board-records"><h2>{c["head"]}</h2><p>{source_links(lang,x)}</p>'+''.join(records)+f'<p><a href="{url(lang,"caja","board-compliance")}">Cajasiete · {c["head"]}</a></p></section>')
  block(ROUTES[lang]['orion']+'index.html',f'<aside class="caja-board" id="cajasiete-board-reader"><h2>Cajasiete · {c["head"]}</h2><p>{html.escape(c["orion"])}</p><p>{html.escape(c["limit2"])}</p><a href="{url(lang,"caja","board-compliance")}">{c["head"]}</a></aside>');rows=[]
  for n in [1,2,3]:
   a=x['assets'][f'{lang}-{n}'];f=next(f for f in files if f['reference']==a+'-PNG^');rows.append(f'<article><h3>{a} · {html.escape(c["titles"][n-1])}</h3><p>{a}-PNG^ · {f["bytes"]} bytes · image/png · {f["viewbox_width"]} × {f["viewbox_height"]}</p><p>SHA-256 <code>{f["sha256"]}</code></p><a href="{BASE+f["repository_path"]}">PNG</a></article>')
  block(ROUTES[lang]['media']+'index.html',f'<section class="caja-board" id="cajasiete-board-assets"><h2>Cajasiete · {c["media"]}</h2><p>Identidad de archivo, no verificación de culpabilidad / File identity, not proof of guilt.</p>'+''.join(rows)+f'<p><a href="{url(lang,"caja","board-compliance")}">{c["head"]}</a></p></section>')
 ids=set(x['assets'].values());media['logical_assets']=[a for a in media['logical_assets'] if a.get('reference') not in ids]+logical;media['files']=[f for f in media['files'] if f.get('logical_asset') not in ids]+files
 if not any(a.get('family_id')=='PD-DMA-FAM-CAJASIETE-001' for a in media['families']):media['families'].append({'family_id':'PD-DMA-FAM-CAJASIETE-001','title':'CajaSiete documentary board and compliance reader','scope':'Assurances, receipt, inadmission, title/security reconstruction and independent response; no satire or portraits','current_primary_es':x['assets']['es-1'],'current_primary_en':x['assets']['en-1'],'mandatory_boundary':'Announced destruction is not proved destruction or illegality. Commercial enquiry and reporting-channel handling remain separate.'})
 for ident,link,claim in [('SRC-CAJASIETE-DOSSIER-20260905',url('es','caja'),'Existing source-bounded public dossier: registry summary and separate Orion relationship; exact facility and knowledge unresolved.'),('SRC-CAJASIETE-BOE-20260905','https://www.boe.es/buscar/act.php?id=BOE-A-2023-4513','Official Law 2/2023 reference; no case-specific breach is found.')]:
  if not any(s['id']==ident for s in media['source_claims']):media['source_claims'].append({'id':ident,'source_type':'CONTROLLED_DOSSIER' if 'DOSSIER' in ident else 'OFFICIAL_LEGISLATION','publisher':'Por Derecho' if 'DOSSIER' in ident else 'BOE','claim':claim,'url':link})
 save(MEDIA,media)
 assert all(a in media['logical_assets'] for a in oldlogical if a['reference'] not in ids)
 assert all(f in media['files'] for f in oldfiles if f.get('logical_asset') not in ids)
 return [f['repository_path'] for f in files]
def check():
 from bs4 import BeautifulSoup
 from PIL import Image
 x=read(CROSS);j=read(REG);events=load_cajasiete_events(ROOT);byid={e['event_id']:e for e in j['events']};assert len(byid)==len(j['events'])
 assert all(byid.get(e['event_id'])==e for e in events),'new event drift'
 assert j['denominator_control']['event_rows_total']==len(j['events']);links=set()
 report={'control_id':CONTROL,'status':'SCOPED_STATIC_PASS_NOT_DEPLOYMENT','canonical_total':len(j['events']),'new_events':len(events),'graphics':6,'exact_graphic_files':12,'page_count':8,'paths':{},'universal_completeness_claim':False}
 for rel,oldhash in x['baseline_pages'].items():
  t=(ROOT/rel).read_text();assert t.count(START)==1 and t.count(END)==1
  stripped=t[:t.index(START)]+t[t.index(END)+len(END):];assert sha(stripped.encode())==oldhash,'prior page bytes changed: '+rel
  frag=t.split(START,1)[1].split(END,1)[0]
  assert not re.search(r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}|mail\.google|canaletico-cajarural\.com|password|contraseña',frag,re.I),'private data'
  soup=BeautifulSoup(t,'html.parser');ids=[a['id'] for a in soup.select('[id]')]
  if '/cajasiete-' in rel:assert ids.count('board-compliance')==1;assert len(soup.select('#board-compliance figure img'))==3
  for a in BeautifulSoup(frag,'html.parser').select('[href],[src]'):
   u=a.get('href') or a.get('src')
   if u.startswith(BASE):links.add(u)
   elif u.startswith('#'):links.add(BASE+rel.removesuffix('index.html')+u)
  report['paths'][rel]=sha((ROOT/rel).read_bytes())
 for u in links:
  path,_,fragment=u.removeprefix(BASE).partition('#');p=ROOT/path
  if p.is_dir():p=p/'index.html'
  assert p.is_file(),'missing target '+u
  if fragment:assert BeautifulSoup(p.read_text(),'html.parser').find(id=fragment),'missing fragment '+u
 media=read(MEDIA);ids=set(x['assets'].values())
 for f in media['files']:
  if f.get('logical_asset') not in ids:continue
  p=ROOT/f['repository_path'];b=p.read_bytes();assert sha(b)==f['sha256'] and len(b)==f['bytes']
  if f['mime']=='image/png':
   with Image.open(p) as im:im.load();assert im.size==(f['viewbox_width'],f['viewbox_height'])
  report['paths'][f['repository_path']]=sha(b)
 for rel in [INPUT,CROSS,REG,MEDIA,BUILDER,'ops/INSTITUTIONAL_COMMUNICATIONS_SCAN_CHECKPOINT.json']:report['paths'][rel]=sha((ROOT/rel).read_bytes())
 report['checked_internal_links']=len(links);return report
def apply():
 x=plan();old={e['event_id']:e for e in read(REG)['events'] if e.get('source_batch_id')!=CONTROL}
 p=ROOT/BUILDER;t=p.read_text();hook='from prepare_cajasiete_board_visuals_20260905 import load_cajasiete_events\nKEY_EVENTS.extend(load_cajasiete_events(REPO_ROOT))\n\n\n'
 if hook not in t:
  assert t.count('def _existing_receipt_ids(register:')==1;t=t.replace('def _existing_receipt_ids(register:',hook+'def _existing_receipt_ids(register:',1);p.write_text(t)
 subprocess.run([sys.executable,str(p),'--apply'],check=True,cwd=ROOT)
 now={e['event_id']:e for e in read(REG)['events']};assert all(now.get(k)==v for k,v in old.items()),'existing canonical event changed or ID collision'
 render(x);r=check();r['existing_events_preserved']=len(old);r['open_proof']=SPEC['open_proof'];save(REPORT,r);print(json.dumps(r,ensure_ascii=False,indent=2))
def live():
 r=check();fail=[]
 for path,want in r['paths'].items():
  if path.startswith(('ops/','scripts/')):continue
  try:
   req=urllib.request.Request('https://sbu001monterecco.github.io/por-derecho/'+path,headers={'Cache-Control':'no-cache'})
   with urllib.request.urlopen(req,timeout=30) as response:data=response.read()
   assert sha(data)==want,'live bytes mismatch'
  except Exception as exc:fail.append(path+': '+str(exc))
 assert not fail,'; '.join(fail)
 print(json.dumps({'status':'LIVE_BYTES_VERIFIED','sha':subprocess.check_output(['git','rev-parse','HEAD']).decode().strip(),'paths':len(r['paths']),'scope':CONTROL}))
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('mode',choices=['apply','check','live']);a=parser.parse_args()
 if a.mode=='apply':apply()
 elif a.mode=='check':print(json.dumps(check(),indent=2))
 else:live()
