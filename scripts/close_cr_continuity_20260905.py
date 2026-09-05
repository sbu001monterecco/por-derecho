#!/usr/bin/env python3
"""Current-main CR continuity repair. Apply only on the declared worker branch.

No private originals or provider locators are inputs. Review labels are not new
historical events. Source, registration, publication and proof closure differ.
"""
from __future__ import annotations
import argparse,copy,hashlib,html,json,re,subprocess,time
from pathlib import Path
from urllib.parse import urlsplit,urljoin,unquote
from urllib.request import Request,urlopen
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[1]
BASE='090a678ad53cd9216e673b0cfc643cd084e5286c'
CONTROL='PD-CR-CONTINUITY-20260905-01'
ANCHOR='cr-continuity-closure-20260905'
RID='PD-SP-O-0084'
CANON='assets/data/la-laguna-proceeding-pages-v1.json'
GAPS='assets/data/unitary-multitrack-criminal-first-gap-closure-v1.json'
ORG='assets/data/matter-identity-registry-v1.organisations.json'
INDEX='assets/data/matter-identity-registry-v1.json'
QUEUE='assets/data/matter-identity-operational-control-v1.json'
COMMS='assets/data/institutional-communications-register-v1.json'
ROSTER='assets/data/matter-identity-registry-v1.professional-organisations.json'
NOTE='ops/CUATRECASAS_RAUDA_CONTINUITY_20260905.md'
AUDIT='ops/CUATRECASAS_RAUDA_RELEASE_20260905.json'
MANIFEST='publication-manifests/cuatrecasas-rauda-recovery-review-20260905.json'
HIST='publication-manifests/historic-proceedings-authority-reintegration-20260903.json'
WORKFLOW='.github/workflows/cuatrecasas-rauda-publication.yml'
SITE='https://sbu001monterecco.github.io/por-derecho/'
SOURCES=[
 {'id':'BORME-A-2021-152-08:376093','url':'https://www.boe.es/diario_borme/txt.php?id=BORME-A-2021-152-08','issuer':'AEBOE / Registro Mercantil de Barcelona','record':'B566926 / inscription 1','registration_date':'2021-07-30','commencement_date':'2021-04-19','class':'DOC','proves':'RAUDA ALSP S.L.P. corporate identity; original sole professional shareholder and sole administrator recorded as CUATRECASAS GONCALVES PEREIRA SLP.','does_not_prove':'Current ownership, precise 2022 mandate, debt ownership, acquisition or wrongdoing.'},
 {'id':'BORME-A-2026-96-08:242206','url':'https://www.boe.es/diario_borme/txt.php?id=BORME-A-2026-96-08','issuer':'AEBOE / Registro Mercantil de Barcelona','record':'B566926 / inscription 6','registration_date':'2026-05-14','class':'DOC','proves':'Later RAUDA ALSP S.L.P. entry on the same registry sheet, concerning representation of the corporate administrator.','does_not_prove':'Complete current company extract, matter-specific act, client status, debt ownership or liability.'}
]
# Review keys already carried by the private handoffs, not new primary events.
C1=[
 ('Source baseline','Base de fuentes','current_status'),
 ('Historical mandate and billing','Mandato y facturación históricos','mandate_handover'),
 ('Actual work and advice','Trabajo y asesoramiento realizados','duty_and_loss'),
 ('Rescue development versus completion','Desarrollo del rescate frente a consumación','duty_and_loss'),
 ('Disclosed recovery involvement','Intervención de recobro comunicada','mandate_handover'),
 ('Itemization referral','Remisión de la petición de desglose','single_satisfaction'),
 ('Two claims kept distinct','Dos reclamaciones diferenciadas','single_satisfaction'),
 ('Invoice and instrument reconciliation','Conciliación de facturas e instrumentos','single_satisfaction'),
 ('Petition versus completed transfer','Petición frente a transmisión consumada','current_status'),
 ('Authorship versus authentication','Autoría frente a autenticación','current_status'),
 ('Separate property identifiers','Identificadores inmobiliarios separados','property_identity'),
 ('Provisional dismissal retained','Sobreseimiento provisional preservado','current_status'),
 ('Notification and time limits','Notificación y plazos','current_status'),
 ('Chronology and knowledge test','Test de cronología y conocimiento','current_status'),
 ('Actual cessionary requires evidence','El cesionario real exige prueba','beneficiary'),
 ('Money-judgment countercase','Posición contraria basada en sentencia dineraria','single_satisfaction'),
 ('Physical and legal property identity','Identidad física y jurídica del inmueble','property_identity'),
 ('Court knowledge of disputed facts','Conocimiento judicial de los hechos discutidos','current_status'),
 ('Complaint chronology source check','Fuentes de cronología de denuncias','current_status'),
 ('Later acts and limitation periods','Actos posteriores y prescripción','current_status'),
 ('Exact client and company perimeter','Perímetro exacto de clientes y sociedades','mandate_handover'),
 ('Lawful recovery alternative','Explicación alternativa de recobro lícito','single_satisfaction'),
 ('Access, disclosure and information use','Acceso, revelación y uso de información','mandate_handover'),
 ('Separate professional offence tests','Requisitos penales profesionales diferenciados','duty_and_loss'),
 ('Claimant-specific wider loss','Daño propio de cada reclamante','duty_and_loss'),
 ('No automatic enforcement stay','Ausencia de suspensión automática','current_status'),
 ('Property disclosure and current orders','Información inmobiliaria y resoluciones actuales','property_identity'),
 ('Transaction-specific acquisition rules','Reglas de adquisición por operación','beneficiary'),
 ('Other advisers: actual mandates','Otros asesores: mandatos reales','wider_connection'),
 ('Regulator-specific competence','Competencia específica del supervisor','wider_connection'),
 ('Separate estates and owners','Masas y propietarios separados','property_identity'),
 ('No responsibility by association','Sin responsabilidad por asociación','wider_connection'),
 ('Public and private custody boundary','Límite de custodia pública y privada','mandate_handover'),
 ('Legal-name succession source check','Fuentes de sucesión de denominación social','mandate_handover'),
 ('Disciplinary status and competence','Estado y competencia disciplinarios','current_status'),
 ('Notification is not inferred knowledge','Notificación no es conocimiento inferido','current_status')]
C2=[
 ('Disclosed role versus concealed interest','Función comunicada frente a interés oculto','mandate_handover'),
 ('Later affirmative procedural act','Acto procesal positivo posterior','current_status'),
 ('Claim-by-claim docket allocation','Expediente por reclamación','single_satisfaction'),
 ('Attempted communication versus delivery','Intento de comunicación frente a entrega','current_status'),
 ('Recovery demand: finite search limits','Requerimiento de cobro: límites de búsqueda','single_satisfaction'),
 ('Invoice recipient versus instrument obligor','Destinatario de factura frente a obligado cambiario','single_satisfaction'),
 ('Reservation versus completed assignment','Reserva frente a cesión consumada','beneficiary'),
 ('Discrepancy versus knowing deception','Discrepancia frente a engaño consciente','current_status'),
 ('Do not erase work already performed','No borrar el trabajo realizado','duty_and_loss'),
 ('Modification versus creditor succession','Modificación frente a sucesión del acreedor','wider_connection'),
 ('Judicial amount source versus legal function','Fuente judicial del importe frente a función jurídica','wider_connection'),
 ('Known response versus missing content','Respuesta conocida frente a contenido no localizado','wider_connection'),
 ('Developed rescue and causal attribution','Rescate desarrollado y atribución causal','duty_and_loss'),
 ('No whole-hotel estate conflation','No confundir todo el hotel con una masa','property_identity'),
 ('Exact court and proceeding','Órgano y procedimiento exactos','current_status'),
 ('Internal note is not filed appeal','Nota interna no es recurso presentado','current_status'),
 ('RAUDA corporate identity and case role','Identidad societaria y función de RAUDA','mandate_handover'),
 ('No collective liability inference','Sin responsabilidad colectiva inferida','wider_connection'),
 ('Applicable historical procedural law','Derecho procesal temporalmente aplicable','current_status'),
 ('No counsel adoption without source','Sin atribuir adopción al letrado sin fuente','duty_and_loss'),
 ('Acquisition rules and exceptions','Reglas de adquisición y excepciones','beneficiary'),
 ('Targeted review is not universal census','Revisión dirigida no es censo universal','current_status')]
PRODUCTION=[
 ('current_status','PD-GAP-UCF-015','Current procedure, service and decisions','Procedimiento, notificación y decisiones actuales','P0','Court/LAJ records; each party’s valid service record; instructed counsel','Expediente judicial/LAJ; notificación válida de cada parte; letrado encargado','Certified current DP/ETJ docket; exact act and receipt; service to each party; appeal processing; actual adjudication/cession if any. Separate dispatch, receipt, notice, examination and decision.','Expediente DP/ETJ certificado y actual; acto y justificante; notificación a cada parte; tramitación del recurso; adjudicación/cesión efectiva, si existe. Separar envío, recepción, notificación, examen y decisión.'),
 ('mandate_handover','PD-GAP-UCF-013','Mandates, recovery handover and information','Mandatos, traspaso al recobro e información','P1','Engagement parties; professional firm; recovery entity; lawful file custodians','Partes del encargo; despacho; entidad de recobro; custodios legítimos','Accepted engagement, legal client, task, dated instructions, handover, file access and remuneration/conflict controls. Corporate identity does not establish the case mandate.','Encargo aceptado, cliente jurídico, tarea, instrucciones fechadas, traspaso, acceso y controles de remuneración/conflicto. La identidad societaria no acredita el mandato del asunto.'),
 ('single_satisfaction','PD-GAP-UCF-013','Separate claims and single satisfaction','Reclamaciones separadas y satisfacción única','P1','Each creditor/obligor; accounts custodian; civil court','Cada acreedor/obligado; custodio contable; órgano civil','Map each invoice/work item, note and authority to its obligor, claim, judgment, enforcement, interest/costs, payment/realization credit and residual. Confirm both dockets; a matching sum is a locator, not proof of duplication.','Vincular factura/trabajo, pagaré y poder con obligado, demanda, sentencia, ejecución, intereses/costas, pago/abono de realización y saldo. Confirmar ambos expedientes; coincidir en importe no prueba duplicidad.'),
 ('property_identity','PD-GAP-UCF-011','Property, rights and estate boundaries','Inmueble, derechos y límites de la masa','P1','Registry; notary; court; owner; independent surveyor/valuer','Registro; notaría; juzgado; propietario; técnico/tasador independiente','Certified history and physical/cadastral/registry crosswalk for each lot and right, possession, valuation and use. Keep fincas 8584/8588 and LPB/Matkator/third-party rights separate.','Historial certificado y correspondencia física/catastral/registral por lote y derecho, posesión, valoración y uso. Separar fincas 8584/8588 y derechos LPB/Matkator/terceros.'),
 ('beneficiary','PD-GAP-UCF-011','Actual transfer, price and beneficiary','Transmisión, precio y beneficiario efectivos','P1','Court; identified assignor/assignee; notary/Registry; payment custodian','Juzgado; cedente/cesionario identificado; notaría/Registro; custodio de pagos','Actual negotiation/assignment instrument, order, price, funding, acceptance, registration/possession and debtor credit. Preserve the possibility that no transfer occurred.','Instrumento real de negociación/cesión, resolución, precio, financiación, aceptación, inscripción/posesión y abono al deudor. Preservar la posibilidad de que no hubiera transmisión.'),
 ('duty_and_loss','PD-GAP-UCF-013','Individual duty, counterfactual and loss','Deber individual, contrafactual y daño','P1','Engagement parties; professionals; independent accounting/valuation evidence','Partes del encargo; profesionales; prueba contable/tasadora independiente','Actor, dated capacity, accepted task, available protective step, performance/breach, causation, claimant-specific loss and strongest lawful alternative. Avoid duplicate damages and automatic whole-hotel valuation.','Actor, capacidad fechada, tarea aceptada, protección disponible, cumplimiento/incumplimiento, causalidad, daño de cada reclamante y mejor explicación lícita. Evitar daños duplicados o valor automático de todo el hotel.'),
 ('wider_connection','PD-GAP-UCF-009','Connection to wider control and funding','Conexión con control y financiación más amplios','P2','Relevant court/administrator; transaction parties; financiers; programme authorities','Juzgado/AC pertinente; partes; financiadores; órganos del programa','Exact transmitted instrument, accepted mandate, instruction/payment or decision-use link for each claimed connection. Preserve developed-rescue, historical-credit and known-response corrections; do not transfer intent through association.','Instrumento transmitido exacto, mandato aceptado, instrucción/pago o uso decisorio por conexión. Conservar correcciones sobre rescate desarrollado, crédito histórico y respuesta conocida; no transmitir dolo por asociación.')]

def git(*a):return subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()
def load(p):return json.loads((ROOT/p).read_text())
def text(p):return (ROOT/p).read_text()
def js(d):return json.dumps(d,ensure_ascii=False,indent=2)+'\n'
def sha(b):return hashlib.sha256(b).hexdigest()
def save(p,v):
 f=ROOT/p;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(v if isinstance(v,str) else js(v));return p
def production():
 keys=['key','gap_id','title_en','title_es','priority','custodian_en','custodian_es','closure_en','closure_es']
 return [dict(zip(keys,r),obligation_id=r[1]+'/CR/'+r[0],status='OPEN_SOURCE_REQUIRED',record_state='REGISTERED_AND_LINKED',merits_closed=False,source_control=CANON) for r in PRODUCTION]
def rows():
 out=[]
 for family,items in [('PD-CR-20260905-01',C1),('PD-CR-UNITARY-20260905-01',C2)]:
  for i,(en,es,key) in enumerate(items,1):
   out.append({'review_key':family+(':C' if 'UNITARY' in family else '-C')+f'{i:02d}','title_en':en,'title_es':es,'obligation_key':key,'record_state':'RECONCILED_TO_CANONICAL_CONTROL','source_class':'PRIVATE_REVIEW_CONTROL_NOT_A_NEW_PRIMARY_EVENT','publication':'MINIMIZED_CONTROL_LABEL_ONLY_PRIVATE_SOURCE_CUSTODY_RETAINED','proposition_status':'NOT_UPGRADED_BY_REGISTRATION'})
 assert len(out)==58
 return out

def panel(lang):
 es=lang=='es';other='en' if es else 'es';t=lambda a,b:a if es else b
 out=[f'<section id="{ANCHOR}" class="section pd-cr-review"><div class="shell record">',
 '<h2>'+t('Continuidad: correcciones registradas y prueba pendiente','Continuity: registered corrections and outstanding proof')+'</h2>',
 '<p><strong>'+t('Identidad societaria resuelta; función en el asunto pendiente.','Corporate identity resolved; case-specific role remains open.')+'</strong> '+t('El BORME identifica a RAUDA ALSP S.L.P. bajo la hoja B566926. El asiento inicial, de 30 de julio de 2021, registra a Cuatrecasas como socio único profesional y administrador único; señala el comienzo de operaciones el 19 de abril de 2021. El asiento de 14 de mayo de 2026 repite la misma hoja. Son datos societarios fechados, no una certificación de titularidad actual ni prueba del mandato de recobro, propiedad del crédito, adquisición o responsabilidad en este asunto.','BORME identifies RAUDA ALSP S.L.P. under registry sheet B566926. The initial entry, dated 30 July 2021, records Cuatrecasas as sole professional shareholder and sole administrator, with commencement of operations on 19 April 2021. The 14 May 2026 entry repeats that sheet. These are dated corporate facts, not certification of current ownership or proof of this matter’s recovery mandate, debt ownership, acquisition or liability.')+'</p>',
 f'<p data-caepr-id="{RID}" data-caret-state="CARET_CONFIRMED"><strong>RAUDA ALSP S.L.P.^</strong> · {RID}. '+t('El signo ^ confirma aquí solo la identidad de la sociedad. Se conserva la referencia histórica abreviada RAUDA; no se atribuye automáticamente a esta persona jurídica todo acto asociado a la marca.','Here ^ confirms only the company’s identity. The historical short label RAUDA is retained; not every brand-associated act is automatically attributed to this legal person.')+'</p>']
 for s in SOURCES:out.append(f'<p id="{s["id"].replace(":","-")}"><a href="{s["url"]}">{s["id"]}</a> · {s["record"]} · {s["registration_date"]}.</p>')
 out+=['<p>'+t('Los dos paquetes se reconcilian como 36 + 22 controles de revisión, no como 58 hechos nuevos. Los documentos judiciales y las dos comunicaciones de recobro ya registrados conservan sus identidades. Los originales, claves privadas y estrategia no se publican.','The two packages are reconciled as 36 + 22 review controls, not 58 new facts. Previously registered court documents and two recovery communications retain their identities. Originals, private locators and strategy are not published.')+'</p>',
 '<h3>'+t('Siete obligaciones: registro cerrado, fondo abierto','Seven obligations: tracking completed, proof still open')+'</h3>']
 for p in production():
  out += [f'<article id="CR-GAP-{p["key"]}" data-gap-id="{p["gap_id"]}"><h4>{html.escape(p["title_"+lang])}</h4>',f'<p><strong>{p["gap_id"]} · {p["priority"]} · OPEN_SOURCE_REQUIRED</strong></p>','<p>'+t('Custodio/fuente: ','Custodian/source: ')+html.escape(p['custodian_'+lang])+'.</p>','<p>'+t('Cierre probatorio: ','Proof-closure test: ')+html.escape(p['closure_'+lang])+'</p></article>']
 out+=['<h3>'+t('Correspondencia completa de controles de revisión','Complete review-control crosswalk')+'</h3>','<p>'+t('Cada clave conserva su paquete y enlaza la obligación pertinente. Registrar una corrección no acredita por sí mismo la hipótesis.','Each key retains its package and links the relevant obligation. Registering a correction does not itself prove the hypothesis.')+'</p>','<div class="tablewrap"><table><thead><tr><th>Control</th><th>'+t('Objeto de revisión y enlace','Review subject and link')+'</th></tr></thead><tbody>']
 for row in rows():out.append(f'<tr id="{row["review_key"].replace(":","-")}"><th>{row["review_key"]}</th><td><a href="#CR-GAP-{row["obligation_key"]}">{html.escape(row["title_"+lang])}</a></td></tr>')
 out+=['</tbody></table></div>','<p>'+t('Cierre técnico, publicación y cierre probatorio son estados distintos. No se afirma que todo el repositorio o todas las identidades estén completos. Verificar de nuevo expediente, notificaciones y plazos antes de cualquier actuación.','Technical repair, publication and proof closure are distinct states. No entire-repository or all-identities completeness claim is made. Verify current dockets, service and time limits again before any procedural action.')+'</p>',f'<p><a href="/por-derecho/{CANON}">'+t('Control y fuentes','Control and sources')+f'</a> · <a href="/por-derecho/{GAPS}">'+t('Registro central de prueba pendiente','Central evidence-gap register')+f'</a> · <a href="/por-derecho/{lang}/'+('registro-identidad-materia/' if es else 'matter-identity-registry/')+'">'+t('Identidades','Identities')+f'</a> · <a href="/por-derecho/{other}/cuatrecasas-sun-park/#{ANCHOR}">'+t('English','Español')+'</a></p>','</div></section>']
 return '\n'.join(out)

def method_page(lang):
 es=lang=='es';t=lambda a,b:a if es else b;title=t('Metodología y niveles de prueba','Methodology and evidence levels');unit='ingenieria-inversa-criminal-unitaria' if es else 'unitary-criminal-reverse-engineering';identity='registro-identidad-materia' if es else 'matter-identity-registry';own='metodologia' if es else 'methodology';other='en/methodology' if es else 'es/metodologia'
 return f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title} — Por Derecho</title><link rel="canonical" href="{SITE}{lang}/{own}/"><style>body{{font:18px/1.65 system-ui,sans-serif;max-width:70ch;margin:2rem auto;padding:0 1rem;overflow-wrap:anywhere}}a{{text-underline-offset:.2em}}h1,h2{{line-height:1.2}}nav{{margin:1.5rem 0}}</style></head><body><header><nav><a href="/por-derecho/{lang}/">Por Derecho</a> · <a href="/por-derecho/{other}/">{'English' if es else 'Español'}</a></nav></header><main><h1>{title}</h1><p>{t('Una reconstrucción conectada no equivale a una conclusión colectiva. Cada acto, capacidad, fecha y relación conserva su fuente y sus límites.','A connected reconstruction is not a collective conclusion. Every act, capacity, date and relationship retains its source and limits.')}</p><h2>{t('Estados de la prueba','Evidence states')}</h2><p><strong>DOC</strong> — {t('apoyo documental limitado','limited documentary support')}; <strong>HIP</strong> — {t('hipótesis atribuida','attributed hypothesis')}; <strong>OPEN</strong> — {t('dependencia no acreditada','unproved reliance')}; <strong>NOTICE</strong> — {t('aviso o recepción, no adopción','notice or receipt, not adoption')}; <strong>CONTRARY</strong> — {t('explicación contraria o lícita','contrary or lawful explanation')}; <strong>ADVERSE</strong> — {t('resultado adverso preservado','preserved adverse outcome')}; <strong>GAP</strong> — {t('fuente pendiente con prueba de cierre','outstanding source with a closure test')}.</p><h2>{t('Qué significa ^','What ^ means')}</h2><p>{t('En una etiqueta, ^ verifica la identidad canónica, no culpabilidad, mandato, conocimiento ni resultado. Como instrucción de auditoría exige además registro, procedencia, relaciones, cronología, publicación, enlaces recíprocos y continuidad.','On a label, ^ verifies canonical identity, not guilt, mandate, knowledge or outcome. As an audit instruction it additionally requires registration, provenance, relationships, chronology, publication, reciprocal links and continuity.')}</p><h2>{t('Cierre verificable','Verifiable closure')}</h2><p>{t('Fuente localizada, registro actualizado, página publicada y hecho acreditado son resultados diferentes. Un hueco solo se cierra en el nivel probado. No se publican originales privados para simular integridad.','A located source, updated record, published page and established fact are different results. A gap is closed only at the level proved. Private originals are not published to simulate completeness.')}</p><nav><a href="/por-derecho/{lang}/{unit}/">{t('Reconstrucción unitaria','Unitary reconstruction')}</a> · <a href="/por-derecho/{lang}/{identity}/">{t('Registro de identidades','Identity registry')}</a> · <a href="/por-derecho/{lang}/cuatrecasas-sun-park/#{ANCHOR}">{t('Controles Cuatrecasas–RAUDA','Cuatrecasas–RAUDA controls')}</a></nav></main></body></html>\n'''

class Links(HTMLParser):
 def __init__(self,s):super().__init__();self.ids=[];self.links=[];self.feed(s)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if a.get('id'):self.ids.append(a['id'])
  if tag=='a' and a.get('href'):self.links.append(a['href'])

def apply():
 raise SystemExit('Historical writer retired. Reconcile the reviewed canonical delta on current main; do not replay this snapshot.')

def check():
 d=load(CANON);c=d['continuity_closure'];assert c['control_id']==CONTROL
 assert len(c['review_controls'])==58 and len({x['review_key'] for x in c['review_controls']})==58
 assert c['review_control_denominator']['new_primary_events_inferred']==0
 assert c['production_obligations']==production();g=load(GAPS)
 for p in production():
  parent=next(x for x in g['gaps'] if x['id']==p['gap_id']);assert sum(x['obligation_id']==p['obligation_id'] for x in parent['specialist_obligations'])==1;assert next(x for x in parent['specialist_obligations'] if x['obligation_id']==p['obligation_id'])==p
 q=load(QUEUE);assert not any(x['id']==RID for x in q['exact_identity_queue']);assert sum(x['id']==RID for x in q['completed_exact_identity_tasks'])==1
 r=next(x for x in load(ORG)['records'] if x['id']==RID);assert r['name']=='RAUDA ALSP S.L.P.' and r['identity_resolution']=='CARET_CONFIRMED' and r['registry_sheet']=='Barcelona B566926' and not r.get('status')
 assert sha((ROOT/ROSTER).read_bytes())==c['original_professional_roster_sha256']
 cm=load(COMMS);n=c['institutional_events_count'];assert sha(js(cm['events'][:n]).encode())==c['institutional_events_sha256']
 assert {x['control_id'] for x in d['professional_recovery_communications']} >= {'PD-CR-COM-20220218','PD-CR-COM-20220307'}
 checks=20;links=0
 for lang in ['es','en']:
  p=f'{lang}/cuatrecasas-sun-park/index.html';s=text(p);expected=panel(lang);assert expected in s;assert s.count('id="'+ANCHOR+'"')==1;assert 'data-cr-continuity-jump' in s;assert re.search(r'class="pd-cr-identity"[^>]*data-caret-state="CARET_CONFIRMED"',s)
  for href in Links(expected).links:
   u=urlsplit(urljoin(SITE+p,href))
   if u.netloc!='sbu001monterecco.github.io':continue
   rel=unquote(u.path).removeprefix('/por-derecho/');rel=rel+'index.html' if rel.endswith('/') else rel;assert (ROOT/rel).is_file(),'Missing '+rel
   if u.fragment and rel.endswith('.html'):assert unquote(u.fragment) in Links(text(rel)).ids,'Missing anchor '+href
   links+=1
  assert not re.search(r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}',expected);checks+=6
 for p in c['new_routes']:assert (ROOT/p).is_file()
 assert (ROOT/HIST).read_bytes()==subprocess.check_output(['git','show','adc8c87585609709caafdd90f03ffbb4a4687d83'+':'+HIST],cwd=ROOT),'Historical source was changed';assert load(MANIFEST)['completion_record']['pull_request']==1465
 for lang in ['es','en']:
  path=f'{lang}/cuatrecasas-sun-park/index.html';original=subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT,text=True);now=text(path)
  now=re.sub(r'<!-- '+CONTROL+r':PANEL:BEGIN -->.*?<!-- '+CONTROL+r':PANEL:END -->','',now,flags=re.S);now=re.sub(r'<p data-cr-continuity-jump>.*?</p>','',now,flags=re.S)
  prior=re.search(r'<p class="pd-cr-identity"[^>]*>.*?</p>',original,re.S).group();now=re.sub(r'<p class="pd-cr-identity"[^>]*>.*?</p>',lambda m:prior,now,flags=re.S)
  if now!=original:
   it=iter(now.splitlines());assert all(any(a==b for b in it) for a in original.splitlines()),'Prior page content lost: '+path
  checks+=1
 print(json.dumps({'result':'CR_CONTINUITY_SCOPED_PASS','checks':checks,'links':links,'review_controls':58,'production_obligations':7,'proof_obligations_closed':0,'rauda_corporate_identity_resolved':True,'institutional_events_preserved':n,'whole_repository_certified':False}))

def live():
 c=load(CANON)['continuity_closure'];paths=[p for p in c['changed_files'] if not p.startswith(('.github/','scripts/'))];paths=sorted(set(paths+[r['path'] for r in load(AUDIT)['pages']]));pending=set(paths);results=[];head=git('rev-parse','HEAD');until=time.monotonic()+480
 while pending and time.monotonic()<until:
  for p in list(pending):
   try:
    url=SITE+(p[:-10] if p.endswith('index.html') else p)+'?cr-continuity='+head
    with urlopen(Request(url,headers={'Cache-Control':'no-cache','User-Agent':'PorDerecho-Scoped-Continuity'}),timeout=20) as resp:b=resp.read()
    if b==(ROOT/p).read_bytes():results.append({'path':p,'sha256':sha(b),'status':'EXACT_MATCH'});pending.remove(p)
   except Exception:pass
  if pending:time.sleep(10)
 save('diagnostics/cr-continuity-live.json',{'head':head,'results':results,'pending':sorted(pending),'scope':'Exact current public resources; no legal-proof completion claim'});assert not pending,'Public readback incomplete: '+str(sorted(pending));print(json.dumps({'result':'CR_CONTINUITY_LIVE_VERIFIED','sha':head,'resources':len(results)}))

def legacy_entry():
 import sys
 if '--write' in sys.argv:raise SystemExit('Historical CR writer retired. Use current-main scoped integration, never replay old whole-file outputs.')
 if '--live' in sys.argv:return live()
 return check()
def main():
 p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True);g.add_argument('--apply',action='store_true');g.add_argument('--check',action='store_true');g.add_argument('--live',action='store_true');a=p.parse_args()
 if a.apply:apply()
 elif a.check:check()
 else:live()
if __name__=='__main__':main()
