#!/usr/bin/env python3
"""Materialise the reviewed 25-Sep platform delta on a non-main branch.

No network, account actions, commits, refs, publication or private-source ingest.
The existing institutional register remains canonical; the input below is a
bounded source crosswalk, not a competing communications register.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import html
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTROL = 'PD-CPA-20260925-07'
INPUT = 'ops/continuity/PLATFORM_INTEGRITY_SOURCE_DELTA_20260925.json'
REGISTER = 'assets/data/institutional-communications-register-v1.json'
PLATFORM = 'assets/data/platform-integrity-events-v1.json'
BUILDER = 'scripts/reconcile_institutional_communications.py'
QUEUE = 'ops/continuity/GITHUB_DRIVE_GITLAB_RECOVERY_QUEUE_20260921.json'
RECORD = 'ops/continuity/PLATFORM_INTEGRITY_LINKEDIN_INCIDENT_20260923.md'
PAGES = {'en':'en/platform-integrity-evidence/index.html', 'es':'es/integridad-plataformas-evidencia/index.html'}
PATHS = [__file__.split(str(ROOT)+'/')[-1], INPUT, REGISTER, PLATFORM, BUILDER,
         'ops/INSTITUTIONAL_COMMUNICATIONS_SCAN_CHECKPOINT.json', QUEUE, RECORD, *PAGES.values()]

# Each row describes one actual communication, not one alleged attack.
ROWS = [
 ('github-review','2026-09-06','GitHub','INBOUND',
  'GitHub said account activity had been flagged by its abuse-detection systems for manual review. The holder contemporaneously reported loss of access to the account, repository and associated Pages site.',
  'GitHub indicó que sus sistemas de detección de abuso habían marcado actividad de la cuenta para revisión manual. El titular comunicó contemporáneamente la pérdida de acceso a la cuenta, al repositorio y al sitio Pages asociado.',
  'The provider did not identify the triggering activity or confirm a third-party report. The Pages impact is the holder\'s contemporaneous report, not an independent provider uptime measurement.',
  'El proveedor no identificó la actividad desencadenante ni confirmó una denuncia de tercero. El efecto en Pages es el relato contemporáneo del titular, no una medición independiente del proveedor.'),
 ('github-restoration','2026-09-11','GitHub','INBOUND',
  'Following review, GitHub confirmed that it had cleared the account restrictions and restored full access.',
  'Tras la revisión, GitHub confirmó que había retirado las restricciones de la cuenta y restablecido el acceso completo.',
  'Restoration does not identify an outside actor or prove retaliation. GitHub did not expressly classify this event as a false positive.',
  'El restablecimiento no identifica un actor externo ni acredita represalia. GitHub no calificó expresamente este episodio como falso positivo.'),
 ('gitlab-restoration','2026-09-22','GitLab','INBOUND',
  'GitLab Support relayed Trust & Safety\'s confirmation that the account had been automatically flagged by anti-abuse tools, was reinstated, and detections had been updated to avoid similar false-positive alerts.',
  'Soporte de GitLab trasladó la confirmación de Trust & Safety: la cuenta había sido marcada automáticamente por herramientas antiabuso, se había restablecido y se habían ajustado las detecciones para evitar avisos falsos positivos similares.',
  'The specific internal signals were withheld. This later explanation supersedes the earlier suggested temporary login-lock mechanism; it does not identify an outside actor. Subsequent compute quota failures are separate.',
  'No se facilitaron las señales internas concretas. Esta explicación posterior sustituye como explicación actual la hipótesis inicial de bloqueo temporal por acceso; no identifica actor externo. Los fallos posteriores por cuota de cómputo son distintos.'),
 ('linkedin-policy','2026-09-23','LinkedIn','INBOUND',
  'LinkedIn stated after another review that the account did not comply with its Professional Community Policies or User Agreement and that the restriction would remain. Later appeal and identity-verification steps are separate process events.',
  'LinkedIn indicó tras otra revisión que la cuenta no cumplía sus políticas profesionales o acuerdo de usuario y que mantendría la restricción. Los pasos posteriores de apelación y verificación de identidad son eventos procesales separados.',
  'This is a provider policy statement, not a particularised identification of content, reporting source, technical trigger or independently established misconduct by the holder.',
  'Es una declaración normativa del proveedor, no la identificación concreta del contenido, origen de denuncia, disparador técnico o conducta irregular del titular acreditada independientemente.'),
 ('incibe-intake','2026-09-25','INCIBE-CERT','INBOUND',
  'INCIBE-CERT assigned an incident reference and supplied general device-security guidance. The assigned reference is retained in private custody.',
  'INCIBE-CERT asignó una referencia de incidente y facilitó orientación general sobre seguridad de dispositivos. La referencia asignada se conserva en custodia privada.',
  'The initial response does not diagnose malware and predates the two later supplements. It is not acknowledgment or acceptance of those attachments.',
  'La respuesta inicial no diagnostica malware y precede a los dos complementos posteriores. No acredita recepción ni aceptación de esos adjuntos.'),
 ('incibe-technical','2026-09-25','INCIBE-CERT','OUTBOUND',
  'A corrective technical supplement was sent in the existing incident thread with three attachments. It separates GitHub, GitLab, LinkedIn, Google and X events, preserves provider explanations, and expressly corrects the earlier photo-change premise.',
  'Se remitió una ampliación técnica correctiva en el hilo del incidente existente con tres adjuntos. Separa los eventos de GitHub, GitLab, LinkedIn, Google y X, conserva las explicaciones de los proveedores y rectifica expresamente la premisa anterior sobre el cambio de foto.',
  'Sent-state and attachment inclusion are verified. Recipient acknowledgment, internal incorporation, technical assessment, malware and a common actor are not established by this transmission.',
  'Se verifican el estado enviado y la inclusión de adjuntos. Este envío no acredita acuse del destinatario, incorporación interna, valoración técnica, malware ni autor común.'),
 ('incibe-context','2026-09-25','INCIBE-CERT','OUTBOUND',
  'A separate institutional-context supplement was sent in the same incident thread with three attachments. It explains the broader asset-tracing context beyond one fundraising vehicle or subsidy and identifies CNMV, RICPE, Intervención General de Canarias, Fondos Europeos, BOE and SNCA/IGAE sources with their limits.',
  'Se remitió un complemento institucional separado en el mismo hilo con tres adjuntos. Explica el contexto de trazabilidad patrimonial más amplio que un vehículo de captación o subvención e identifica fuentes de CNMV, RICPE, Intervención General de Canarias, Fondos Europeos, BOE y SNCA/IGAE con sus límites.',
  'Transmission is not institutional endorsement of the underlying portfolio allegation. No consolidated illicit AUM, grant payment, digital attacker or common campaign is established. Restricted documents and the detailed allegation remain privately preserved.',
  'El envío no es aval institucional de la alegación patrimonial subyacente. No se acredita patrimonio ilícito consolidado, pago de ayuda, atacante digital ni campaña común. Los documentos restringidos y la alegación detallada permanecen preservados privadamente.'),
 ('google-sunrockers','2022-08-08','Google Business Profile','INBOUND',
  'A provider notice records suspension of the SunRockers Cafe - Community Social Lounge profile following a suspicious-activity flag.',
  'Un aviso del proveedor documenta la suspensión del perfil SunRockers Cafe - Community Social Lounge tras una señal de actividad sospechosa.',
  'The notice does not identify a third-party cause or establish later restoration. Associated listing notices are not automatically separate attacks.',
  'El aviso no identifica una causa de tercero ni acredita un restablecimiento posterior. Los avisos sobre fichas asociadas no son automáticamente ataques separados.'),
 ('google-u3a','2022-08-08','Google Business Profile','INBOUND',
  'A provider notice records suspension of the U3A Lanzarote profile following a suspicious-activity flag.',
  'Un aviso del proveedor documenta la suspensión del perfil U3A Lanzarote tras una señal de actividad sospechosa.',
  'The notice does not establish who caused the flag or whether it shares a mechanism with other profiles. Sun Park\'s reinstatement cannot be applied to this profile without its own record.',
  'El aviso no acredita quién causó la señal ni si comparte mecanismo con otras fichas. El restablecimiento de Sun Park no se extiende a esta ficha sin registro propio.'),
 ('google-wi','2022-08-08','Google Business Profile','INBOUND',
  'A provider notice records suspension of The Women’s Institute - Lanzarote profile following a suspicious-activity flag.',
  'Un aviso del proveedor documenta la suspensión del perfil The Women’s Institute - Lanzarote tras una señal de actividad sospechosa.',
  'This is a separately identified notification, not independent corroboration of a common attack. Its subsequent outcome remains unverified in this selected record.',
  'Es una notificación individualizada, no corroboración independiente de un ataque común. Su resultado posterior no está verificado en este registro seleccionado.'),
 ('x-notice','2024-12-19','X','INBOUND',
  'X notified an automatic account suspension, invoking its rules against inauthentic behaviours.',
  'X notificó una suspensión automática de cuenta, invocando sus reglas contra comportamientos no auténticos.',
  'This is the provider\'s stated classification, not an independently established violation. Current account status, an outside actor and linkage to other platforms are not verified.',
  'Es la clasificación declarada por el proveedor, no una infracción acreditada independientemente. No se verifican el estado actual de la cuenta, un actor externo ni vínculos con otras plataformas.')
]


def encoded(value):
    return (json.dumps(value,ensure_ascii=False,indent=2,sort_keys=True)+'\n').encode()

def save(path,value):
    p=ROOT/path; p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(encoded(value))

def load_events(root):
    """Canonical-builder extension; no actions or writes during import."""
    path=Path(root)/INPUT
    spec=json.loads(path.read_text())
    if spec['control_id']!=CONTROL or len(spec['communications'])!=len(ROWS):
        raise ValueError('Platform source cohort identity/count mismatch')
    out=[]
    for row in spec['communications']:
        key=row['key']; outbound=row['direction']=='OUTBOUND'
        e={
          'event_id':row['event_id'], 'cohort':'CURATED_SOURCE_PROVED_EVENT',
          'layer':'OFFICIAL_ACT_OR_CORRESPONDENCE', 'source_key':CONTROL+':'+key,
          'record_type':'OUTBOUND_COMMUNICATION' if outbound else 'OFFICIAL_NOTIFICATION',
          'event_date':row['date'], 'direction':'OUTBOUND_TO_INSTITUTION' if outbound else 'INBOUND_FROM_INSTITUTION',
          'channel':'EMAIL', 'office':row['office'], 'official_reference':'REFERENCE_RETAINED_PRIVATELY',
          'matter_references':['PD-PLATFORM-INTEGRITY-20260923-01',CONTROL],
          'source_integrity':{'status':'SOURCE_REVIEWED_PUBLIC_SAFE_DERIVATIVE','repository_anchor':INPUT,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()},
          'attribution_state':'INSTITUTIONAL_NOTICE_NO_PERSONAL_SIGNATORY_ASSERTED',
          'linked_transport_event_ids':[], 'transport_link_state':'NATIVE_LOCATORS_PRIVATE_NO_SYNTHETIC_MAILBOX_ROW',
          'proof_level':'SENT_EMAIL_VERIFIED' if outbound else 'RETAINED_OFFICIAL_NOTIFICATION',
          'evidence_state':{
             'transmission':'SENT_VERIFIED' if outbound else 'INBOUND_REPLY_RETAINED',
             'registration':'NOT_A_FORMAL_REGISTRY_FILING', 'filing':'NO_NEW_COURT_FILING',
             'destination':'ONLY_AS_STATED_IN_SOURCE',
             'delivery':'RECIPIENT_ACKNOWLEDGMENT_NOT_VERIFIED' if outbound else 'INBOUND_FROM_INSTITUTION_VERIFIED',
             'internal_association':'NOT_ESTABLISHED_BY_THIS_SOURCE',
             'substantive_examination':'ONLY_PROVIDER_REVIEW_EXPRESSLY_STATED_IN_SUMMARY',
             'merits':'NO_FINDING_ON_UNDERLYING_ECONOMIC_ALLEGATIONS'},
          'public_summary':row['en'], 'public_summary_es':row['es'],
          'proves':[row['en']], 'proves_es':row['es'],
          'does_not_prove':[row['limit_en']], 'does_not_prove_es':row['limit_es'],
          'canonical_anchor_en':'en/institutional-records/#communication-'+row['event_id'],
          'canonical_anchor_es':'es/registros-institucionales/#communication-'+row['event_id'],
          'source_timezone':'DATE_ONLY_PUBLIC_PROJECTION_EXACT_TIMESTAMP_PRIVATE',
          'criminal_responsibility_transfer':False, 'public_derivative_state':'PUBLIC_SAFE_MINIMISED_DERIVATIVE'}
        if key.startswith('incibe-') and outbound:
            e['attachment_count']=3
            e['attachment_count_basis']='VERIFIED_SENT_ATTACHMENT_OCCURRENCES_NOT_INDEPENDENT_CORROBORATIONS'
            e['matter_references'].extend(x['id'] for x in spec['attachments'] if x['parent_key']==key)
        out.append(e)
    return out


def allocate_spec():
    if (ROOT/INPUT).exists():
        spec=json.loads((ROOT/INPUT).read_text())
        if [r['key'] for r in spec['communications']]!=[r[0] for r in ROWS]:
            raise ValueError('Existing cohort differs; reconcile rather than reallocate')
        return spec
    used=set()
    names=subprocess.check_output(['git','ls-files','-z'],cwd=ROOT).decode().split('\0')
    for name in names:
        p=ROOT/name
        if not name or not p.is_file() or p.suffix.lower() not in {'.json','.md','.html','.js','.py','.csv','.yml','.yaml','.txt'}: continue
        if p.stat().st_size>5_000_000: continue
        used.update(int(x) for x in re.findall(r'PD-SP-EVT-(\d{4})\b',p.read_text(errors='replace')))
    number=max(used)+1
    items=[]
    for row in ROWS:
        if number>9999: raise ValueError('Event namespace exhausted')
        items.append(dict(zip(['key','date','office','direction','en','es','limit_en','limit_es'],row),event_id=f'PD-SP-EVT-{number:04d}'))
        number+=1
    attachments=[]
    for n,(key,kind,pages) in enumerate([
       ('incibe-technical','CORRECTIVE_REPORT',4),('incibe-technical','IDENTIFIED_EVIDENCE_EXTRACTS',11),('incibe-technical','CHECKSUM_CONTROL',None),
       ('incibe-context','INSTITUTIONAL_CONTEXT_NOTE',4),('incibe-context','INDEXED_SOURCE_READING_BOOK',36),('incibe-context','CHECKSUM_AND_PROVENANCE_CONTROL',None)],1):
        attachments.append({'id':CONTROL+f'-ATT-{n:02d}','parent_key':key,'kind':kind,'pages':pages,'custody':'EXACT_SENT_BYTES_PRESERVED_PRIVATELY','public_bytes':False})
    spec={'schema':'por-derecho.platform-source-crosswalk.v1','control_id':CONTROL,'review_date':'2026-09-25','canonical_register':REGISTER,
      'communications':items,'attachments':attachments,'coverage':{'communications':len(items),'sent_supplements':2,'attachment_occurrences':6,'universal_completeness_claim':False},
      'private_custody':{'state':'DRIVE_AND_LIBRARY_RETRIEVAL_HASH_VERIFIED_20260925','locators_public':False,'native_emails_remain_in_authorised_mailbox':True},
      'institutional_context':{'scope':'BROADER_ASSET_TRACING_NOT_LIMITED_TO_ONE_FUNDRAISE_OR_GRANT','detailed_portfolio_allegation':'PRESERVED_IN_PRIVATE_SENT_SUPPLEMENT_NOT_ADJUDICATED','consolidated_illicit_AUM_proved':False,
        'source_families':['CNMV','RICPE_2021_CERTIFICATE','IG_CANARIAS','DG_FONDOS_EUROPEOS','BOE','SNCA_IGAE'],
        'limits':['specified_document_absence_is_not_universal_absence','supervisory_consideration_is_not_disclosed_merits','competence_limit_is_not_a_blanket_no_aid_certificate','published_award_is_not_payment_or_loss','SNCA_noncontinuation_is_preserved','funding_layers_are_not_automatically_additive','identity_request_is_not_identity_disclosure_or_cyber_attribution'],
        'remaining_primary_copy_gaps':['TESORO_SALIDA_499980_2026','DGFE_AC2000001007594']},
      'publication_boundary':'NO_NATIVE_EMAILS_PRIVATE_CASE_NUMBERS_PROVIDER_IDS_AUTH_URLS_OR_UNREDACTED_ATTACHMENTS',
      'status_boundaries':['SENT_NOT_ACKNOWLEDGED','ACKNOWLEDGED_NOT_INCORPORATED','INSTITUTIONAL_CONTEXT_NOT_CRIMINAL_FINDING','GITHUB_COMPLETION_NOT_GITLAB_PARITY','RESTORATION_NOT_CAUSAL_ATTRIBUTION']}
    save(INPUT,spec); return spec


def patch_once(path,old,new):
    p=ROOT/path; text=p.read_text()
    if new in text:return
    if text.count(old)!=1:raise ValueError('Non-unique patch anchor: '+path+' / '+old[:70])
    p.write_text(text.replace(old,new,1))


def page_block(spec,lang):
    es=lang=='es'; fields=('es','limit_es') if es else ('en','limit_en')
    title='Actualización documentada: proveedores, correcciones y consulta a INCIBE' if es else 'Documented update: providers, corrections and the INCIBE consultation'
    lead='Revisión de 25 septiembre 2026. Cada comunicación tiene su propia referencia; una cronología conjunta no presupone una causa común.' if es else 'Review of 25 September 2026. Each communication has its own reference; a shared chronology does not presume a common cause.'
    note='Los dos complementos se enviaron en el caso existente. La respuesta inicial de INCIBE no es un acuse de esos envíos posteriores. Los seis adjuntos y los originales se conservan privadamente.' if es else 'The two supplements were sent in the existing case. INCIBE’s initial response is not acknowledgment of those later transmissions. The six attachments and source originals remain in private custody.'
    out=['<!-- PD-CPA-20260925-07:START -->',f'<section class="section recipient-section-alt" id="platform-update-20260925" data-control-id="{CONTROL}"><div class="shell recipient-record">',f'<p class="kicker">25 SEP 2026 · {CONTROL}</p><h2>{title}</h2><p>{lead}</p>',f'<p class="recipient-notice">{note}</p>','<div class="recipient-grid">']
    ordered=sorted(spec['communications'],key=lambda x:(x['date'],x['event_id']))
    for row in ordered:
        out.extend([f'<article class="recipient-card" id="communication-{row["event_id"]}">',f'<span class="label">{html.escape(row["date"])} · {html.escape(row["office"])}</span>',f'<h3>{row["event_id"]}</h3><p>{html.escape(row[fields[0]])}</p>',f'<p class="recipient-small"><strong>{"Límite" if es else "Limit"}.</strong> {html.escape(row[fields[1]])}</p>',f'<a href="../../assets/data/institutional-communications-register-v1.json">{"Registro canónico" if es else "Canonical register"}</a></article>'])
    out.append('</div>')
    if es:
        out.append('<h3>Contexto económico e institucional sin atribución digital automática</h3><p>La comunicación institucional explica una alegación de trazabilidad sobre una base patrimonial adquirida más amplia que la captación de un fondo o una subvención. La alegación detallada está conservada en el complemento privado: no se sustituye por una cifra de captación ni se presenta como patrimonio ilícito ya probado. CNMV, Intervención General, Fondos Europeos y SNCA mantienen sus respectivas competencias, respuestas y límites; el contexto no acredita quién causó las interrupciones digitales.</p><p>RIC, financiación privada, incentivos regionales y cofinanciación FEDER deben conciliarse por activo y gasto, sin sumarse automáticamente. Una concesión no acredita pago, correcta aplicación, pérdida o valoración de cartera.</p><p><strong>Separación operativa:</strong> el fallo posterior de ejecución de GitLab por <code>ci_quota_exceeded</code> y el aviso de facturación de Google Cloud son categorías distintas del bloqueo antiabuso. No se cuentan como ataques sin evidencia adicional.</p>')
    else:
        out.append('<h3>Economic and institutional context without automatic digital attribution</h3><p>The institutional communication explains an asset-tracing allegation concerning an acquired asset base broader than one fundraise or subsidy. The detailed allegation remains preserved in the private supplement: it is not reduced to fundraising totals or presented as proved illicit assets. CNMV, Intervención General, Fondos Europeos and SNCA retain their separate remits, responses and limitations; the context does not identify who caused the digital interruptions.</p><p>RIC, private financing, regional incentives and FEDER co-financing require asset-and-expenditure reconciliation, not automatic addition. An award does not establish payment, proper use, loss or portfolio valuation.</p><p><strong>Operational separation:</strong> the subsequent GitLab execution failure due to <code>ci_quota_exceeded</code> and the Google Cloud billing notice are different categories from the anti-abuse block. They are not counted as attacks without additional evidence.</p>')
    out.append('<div class="recipient-links">')
    for route,label in [('ric-private-equity-sun-park','RICPE / Sun Park'),('cnmv-ricpe-verificacion' if es else 'cnmv-ricpe-verification','CNMV'),('snca-trazabilidad-fondos-europeos' if es else 'snca-eu-funds-traceability','SNCA / fondos europeos' if es else 'SNCA / European funds'),('google-sun-park-cooperacion-evidencia' if es else 'google-sun-park-evidence-cooperation','Google')]:
        if (ROOT/lang/route/'index.html').exists(): out.append(f'<a href="../{route}/">{label}</a>')
    out.extend([f'<a href="../../{INPUT}">{"Fuentes y límites" if es else "Sources and limits"}</a>','</div></div></section>','<!-- PD-CPA-20260925-07:END -->'])
    return '\n'.join(out)+'\n'


def update_pages(spec):
    for lang,path in PAGES.items():
        p=ROOT/path; text=p.read_text(); es=lang=='es'
        if '<!-- PD-CPA-20260925-07:START -->' in text: continue
        if text.count('<main id="content">')!=1:raise ValueError('Missing unique main anchor '+path)
        section='<section class="section recipient-section-alt" id="'+('actual' if es else 'current')+'">'
        if text.count(section)!=1:raise ValueError('Current section boundary drift')
        text=text.replace(section,page_block(spec,lang)+section,1)
        # Preserve prior observations explicitly as historical, not current truth.
        if es:
            text=text.replace('Un evento de seguridad confirmado por el proveedor; una restricción actual aún sin explicación.','Aviso de cambio propio y restricción: leer junto a la actualización documentada de 25 septiembre.')
            text=text.replace('<strong>GitLab · 17–18 sep 2026</strong>','<strong>GitLab · 17–22 sep 2026</strong>')
            text=text.replace('El workspace conectado de GitLab vuelve a estar operativo el 23 septiembre.','GitLab confirmó el restablecimiento el 22 septiembre; el workspace conectado se observó operativo el 23 septiembre.')
            old='Soporte indicó que intentos repetidos de acceso pueden provocar un bloqueo temporal que normalmente debería despejarse automáticamente; ese mecanismo sugerido no resolvió el 403 observado dentro del intervalo indicado, por lo que siguió siendo pertinente la revisión humana.'
            new='La sugerencia inicial de bloqueo temporal por intentos repetidos queda como antecedente histórico. El 22 septiembre GitLab confirmó una detección antiabuso automática, el restablecimiento y ajustes para evitar avisos falsos positivos similares; no reveló las señales internas.'
            if old not in text:raise ValueError('Spanish GitLab explanation anchor drift')
            text=text.replace(old,new,1)
            historical='<p class="recipient-notice"><strong>Observación histórica, actualizada el 25 septiembre:</strong> las menciones siguientes a una explicación no localizada describen la primera búsqueda, no el estado actual de las fuentes. Ya se conserva la respuesta de LinkedIn de 23 septiembre que invoca sus políticas, además de los pasos posteriores de apelación y Persona. El disparador concreto sigue sin determinarse. El cambio de foto fue propio.</p>'
        else:
            text=text.replace('One provider-confirmed security event; one current restriction awaiting explanation.','A self-authored change alert and a restriction: read with the documented 25 September update.')
            text=text.replace('<strong>GitLab · 17–18 Sep 2026</strong>','<strong>GitLab · 17–22 Sep 2026</strong>')
            text=text.replace('The connected GitLab workspace is operational again by 23 September.','GitLab confirmed restoration on 22 September; the connected workspace was observed operational by 23 September.')
            old='Support advised that repeated login attempts can cause a temporary lock normally expected to clear automatically; that suggested mechanism did not clear the observed 403 within the stated interval, so human review remained relevant.'
            new='The earlier suggested temporary repeated-login lock is historical context. On 22 September GitLab confirmed automatic anti-abuse flagging, reinstatement and detection adjustments to avoid similar false-positive alerts; the specific internal signals were withheld.'
            if old not in text:raise ValueError('English GitLab explanation anchor drift')
            text=text.replace(old,new,1)
            historical='<p class="recipient-notice"><strong>Historical observation, updated on 25 September:</strong> the references below to an explanation not located describe the initial search, not the current source record. LinkedIn’s 23 September policy-based restriction response is now retained, alongside later appeal and Persona steps. The specific trigger remains unresolved. The photo change was self-authored.</p>'
        target='id="actual"' if es and 'id="actual"' in text else 'id="current"'
        pos=text.find(target)
        if pos<0:raise ValueError('Current section missing '+path)
        grid=text.find('<div class="recipient-grid">',pos)
        if grid<0:raise ValueError('Current cards missing '+path)
        text=text[:grid]+historical+text[grid:]
        # Original later partial-access event is preserved and expressly delimited.
        if es:
            text=text.replace('El control de continuidad rechaza por ello describir GitHub como universalmente inaccesible y preserva la distinción entre vías de acceso.','Esto delimita únicamente el evento del 19 septiembre. No sustituye el bloqueo anterior: GitHub explicó la revisión antiabuso el 6 septiembre y confirmó el restablecimiento el 11 septiembre, registrados en la actualización superior.')
        else:
            text=text.replace('The continuity record therefore rejects describing GitHub as universally unavailable and preserves the access-path distinction.','This limits only the 19 September event. It does not replace the earlier restriction: GitHub explained the anti-abuse review on 6 September and confirmed restoration on 11 September, recorded in the update above.')
        p.write_text(text)


def update_platform(spec):
    data=json.loads((ROOT/PLATFORM).read_text()); events=data['events']; by={e['id']:e for e in events}
    rows={r['key']:r for r in spec['communications']}
    gl=by['PD-PLAT-GITLAB-20260917-403']
    if not gl.get('supersession_history'):
        gl['supersession_history']=[{'recorded_state':'PRE_25SEP_SOURCE_RECONCILIATION','date_range':gl['date_range'],'summary':gl['summary'],'attribution':gl['attribution'],'status':'HISTORICAL_PRELIMINARY_EXPLANATION_SUPERSEDED'}]
    gl.update(date_range='2026-09-17/2026-09-22',status='PROVIDER_CONFIRMED_RESTORED_FALSE_POSITIVE',summary=rows['gitlab-restoration']['en'],attribution=rows['gitlab-restoration']['limit_en'],communication_event_id=rows['gitlab-restoration']['event_id'])
    li=by['PD-PLAT-LI-20260923-RESTRICT']
    if not li.get('supersession_history'):
        li['supersession_history']=[{'summary':li['summary'],'status':li['status'],'meaning':'INITIAL_HOLDER_REPORT_PRESERVED'}]
    li.update(status='PROVIDER_POLICY_STATEMENT_APPEAL_OPEN',summary=rows['linkedin-policy']['en'],attribution=rows['linkedin-policy']['limit_en'],communication_event_id=rows['linkedin-policy']['event_id'])
    for row in spec['communications']:
        pid='PD-PLAT-CPA-20260925-'+row['key'].upper()
        if pid in by:continue
        events.append({'id':pid,'platform':row['office'],'date':row['date'],'status':'OUTBOUND_VERIFIED_RESPONSE_PENDING' if row['direction']=='OUTBOUND' else 'SOURCE_REVIEWED_PROVIDER_OR_INSTITUTION_STATEMENT','summary':row['en'],'summary_es':row['es'],'attribution':row['limit_en'],'attribution_es':row['limit_es'],'communication_event_id':row['event_id'],'source_control':CONTROL,'sequence_role':'LATER_PROVIDER_EXPLANATION' if row['key']=='gitlab-restoration' else 'INDIVIDUAL_COMMUNICATION'})
    quota='PD-PLAT-GITLAB-20260925-COMPUTE-QUOTA'
    if quota not in by:events.append({'id':quota,'platform':'GitLab CI','date':'2026-09-25','status':'OPERATIONAL_CAPACITY_LIMIT_SEPARATE_FROM_ACCOUNT_BLOCK','summary':'An inspected existing job failed before execution with ci_quota_exceeded and no runner assigned while repository/API access was operational.','attribution':'Quota is the recorded failure reason, not proof of external interference or a renewed account block. Current capacity must be rechecked before later execution.','source_control':CONTROL})
    data['as_of']='2026-09-25'; data['latest_source_control']=INPUT
    data['interpretation_boundaries']=['communication_count_is_not_attack_count','GitHub_reinstatement_is_not_GitLab_false_positive','provider_statement_is_not_independent_merits_finding','initial_incident_reference_is_not_acknowledgment_of_later_attachments']
    save(PLATFORM,data)


def prepare():
    branch=subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()
    if branch in {'main','master',''}:raise ValueError('Use an explicit isolated non-main branch')
    before=json.loads((ROOT/REGISTER).read_text()); old_events={e['event_id']:e for e in before['events']}
    spec=allocate_spec()
    ids={r['event_id'] for r in spec['communications']}
    for eid in ids:
        if eid in old_events and old_events[eid].get('source_key','').split(':')[0]!=CONTROL:raise ValueError('Canonical ID collision '+eid)
    anchor='def _existing_receipt_ids(register:'
    addition='from prepare_platform_incibe_20260925 import load_events as load_platform_incibe_events\nKEY_EVENTS.extend(load_platform_incibe_events(REPO_ROOT))\n\n\n'+anchor
    patch_once(BUILDER,anchor,addition)
    patch_once(BUILDER,'register["control_date"] = "2026-09-24" if supplemental_events else "2026-09-21"','register["control_date"] = "2026-09-25" if any(e.get("source_key", "").split(":")[0] == "PD-CPA-20260925-07" for e in key_events) else ("2026-09-24" if supplemental_events else "2026-09-21")')
    subprocess.run(['python3',BUILDER,'--apply'],cwd=ROOT,check=True)
    after=json.loads((ROOT/REGISTER).read_text()); new_events={e['event_id']:e for e in after['events']}
    for eid,e in old_events.items():
        if e.get('source_key','').split(':')[0]!=CONTROL and new_events.get(eid)!=e:raise ValueError('Unrelated canonical event changed '+eid)
    if len(after['events'])!=len([e for e in before['events'] if e.get('source_key','').split(':')[0]!=CONTROL])+len(ROWS):raise ValueError('Canonical count mismatch')
    update_platform(spec); update_pages(spec)
    record=(ROOT/RECORD).read_text()
    marker='## 25 September 2026 — completed INCIBE supplements and source reconciliation'
    if marker not in record:
        (ROOT/RECORD).write_text(record+'\n\n'+marker+'\n\n**Control: '+CONTROL+'.** This dated addendum controls over preliminary cross-platform explanations above; historical observations are retained.\n\nGitHub\'s original September restriction/review and 11-Sep restoration are separate from the bounded 19-Sep browser path episode. On 22-Sep GitLab expressly confirmed automatic anti-abuse flagging, restoration and adjustment of false-positive detections; its earlier temporary-login-lock suggestion is not the current provider explanation. The later compute-quota failure remains a separate operational constraint. LinkedIn\'s 23-Sep policy reply is now source-located; the photo edit remains self-attributed and the specific restriction trigger remains open.\n\nThe existing INCIBE consultation now has two separate sent supplements: technical correction and institutional context, each with three verified attachments. Initial case assignment is not acknowledgment of these later transmissions. No new case, subsequent receipt, malware diagnosis, common actor, merits finding or asset valuation is inferred. The wider portfolio allegation is preserved in the private institutional supplement, not limited to one fundraise or grant; private documents are not published to achieve continuity.\n\nThe bounded crosswalk `'+INPUT+'` feeds the existing canonical institutional communications register. It individualises all eleven selected communications and six attachment occurrences. The earlier source IDs and events survive unchanged. CNMV, IG Canarias, DGFE, BOE and SNCA sources retain their distinct and limiting meanings.\n\nPrivate Drive/Library retrieval and hash verification are preserved under the same audit key. The public source register and both existing language routes carry the minimised derivative. This source record does not itself certify a main merge or live deployment. GitLab replay is explicitly queued in the existing dual-write register; no CI-minute purchase, quota probe or gate weakening is requested. Thread deletion state remains ORANGE until applicable cross-host and task-dependency checks are independently closed. Future work must not resend the completed correspondence merely to preserve it.\n')
    q=json.loads((ROOT/QUEUE).read_text())
    if not any(x['id']=='PD-GL-REC-CPA-20260925-07' for x in q['replay_items']):
        q['replay_items'].append({'id':'PD-GL-REC-CPA-20260925-07','scope':'Source-qualified cross-platform chronology and completed institutional correspondence','recovery_class':'GITHUB_NEWER_OR_EQUIVALENT','github_branch':'integration/platform-integrity-incibe-20260925','github_state':'SOURCE_CANDIDATE_REQUIRE_EXACT_MAIN_AND_LIVE_RECEIPT','public_paths':PATHS,'private_native_disposition':'PRIVATE_OR_RESTRICTED_NO_PUBLIC_GIT_TRANSFER','private_custody_state':'DRIVE_LIBRARY_RETRIEVAL_HASH_VERIFIED','gitlab_state':'ADDITIVE_REPLAY_PENDING_NO_PARITY_CLAIM','replay_rule':'Refresh both heads; preserve newer GitLab source and merge only this reviewed net delta through normal gates. No quota-probe pipeline or paid action. Do not port the temporary preparation workflow.','closure':'Record exact merged GitHub head/readback separately; GitLab remains pending until exact relevant source/release checks pass.'})
        save(QUEUE,q)
    return spec


def validated_platform_event_ids(events, root=ROOT):
    """Fail closed on a missing, duplicated, altered or unsolicited cohort row."""
    expected = {e['event_id']: e for e in load_events(root)}
    selected = [e for e in events if str(e.get('source_key', '')).startswith(CONTROL + ':')]
    actual = {e['event_id']: e for e in selected}
    if len(selected) != len(actual) or actual != expected:
        raise ValueError('Platform communication cohort differs from its reviewed source crosswalk')
    return set(expected)


def validate():
    spec=json.loads((ROOT/INPUT).read_text()); ev=load_events(ROOT)
    assert len(ev)==11 and len({e['event_id'] for e in ev})==11
    reg=json.loads((ROOT/REGISTER).read_text()); actual={e['event_id']:e for e in reg['events']}
    for e in ev:assert actual[e['event_id']]==e,e['event_id']
    assert len(spec['attachments'])==6
    assert len([e for e in ev if e['record_type']=='OUTBOUND_COMMUNICATION'])==2
    assert all(e['evidence_state']['delivery']=='RECIPIENT_ACKNOWLEDGMENT_NOT_VERIFIED' for e in ev if e['record_type']=='OUTBOUND_COMMUNICATION')
    for path in [INPUT,*PAGES.values()]:
        text=(ROOT/path).read_text()
        for forbidden in ['mail.google.com','drive.google.com/file','incidencias@']:
            assert forbidden not in text,(path,forbidden)
    for lang,path in PAGES.items():
        text=(ROOT/path).read_text(); assert text.count('id="platform-update-20260925"')==1
        for e in ev:assert text.count('id="communication-'+e['event_id']+'"')==1
        assert ('falsos positivos' if lang=='es' else 'false-positive') in text
    data=json.loads((ROOT/PLATFORM).read_text()); by={e['id']:e for e in data['events']}
    assert len(by)==len(data['events'])
    assert by['PD-PLAT-GITLAB-20260917-403']['status']=='PROVIDER_CONFIRMED_RESTORED_FALSE_POSITIVE'
    assert by['PD-PLAT-GITLAB-20260917-403']['supersession_history']
    assert 'PD-PLAT-GITHUB-20260919-ACCESS' in by
    assert 'PD-PLAT-CPA-20260925-GITHUB-RESTORATION' in by
    print('PASS: eleven canonical communications, six private attachment occurrences, bilingual anchors, source limits and separation controls')

if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--apply',action='store_true'); parser.add_argument('--check',action='store_true'); args=parser.parse_args()
    if args.apply:prepare()
    validate()
