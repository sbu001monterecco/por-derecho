#!/usr/bin/env python3
"""Apply the owner-authorised 27-Sep Cuatrecasas correction to existing controls.

No network, private correspondence, filing, recipient contact or deployment.
Static source updates only. Historical source documents and financial amounts are
not rewritten. Run on an isolated review branch; review the resulting diff.
"""
from __future__ import annotations
import argparse
import hashlib
import html
import json
import os
import re
import subprocess
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATE = '2026-09-27'
MARKER = 'cuatrecasas-position-status-20260927'
CONTROL = 'assets/data/cuatrecasas-whole-claim-architecture-v1.json'
ARCHIVE = 'archive/CUATRECASAS_POSITION_STATUS_OUTCOME_UPDATE_27SEP2026.md'
RECEIPT = 'ops/cuatrecasas-position-status-source-receipt-20260927.json'
DP_SOURCE = 'docs/cuatrecasas/DP748/2026-09-16_diligencia_ordenacion_apelacion_subs_fulltext_source_safe.md'
ETJ_SOURCE = 'docs/cuatrecasas/ETJ163/2026-09-17_auto_reposicion_suspension_fulltext_source_safe.md'
BRANCH = 'agent/cuatrecasas-position-status-20260927'
PAGES = [
 'en/cuatrecasas-sun-park/index.html', 'es/cuatrecasas-sun-park/index.html',
 'en/cuatrecasas-matkator-whole-claim/index.html', 'es/cuatrecasas-matkator-reclamacion-integral/index.html',
 'en/cuatrecasas-wip-unbilled/index.html', 'es/cuatrecasas-wip-no-facturado/index.html',
 'en/cuatrecasas-invoices-payments/index.html', 'es/cuatrecasas-facturas-pagos/index.html',
 'en/cuatrecasas-dp748-civil-action/index.html', 'es/cuatrecasas-dp748-accion-civil/index.html',
 'en/proceedings/tf-civ-001/index.html', 'es/procedimientos/tf-civ-001/index.html',
 'en/proceedings/tf-civ-002/index.html', 'es/procedimientos/tf-civ-002/index.html',
 'en/proceedings/tf-cri-003/index.html', 'es/procedimientos/tf-cri-003/index.html',
 'en/cuatrecasas-etj163-dp748-18-september-2026/index.html',
 'es/cuatrecasas-etj163-dp748-18-septiembre-2026/index.html',
 'en/recovery-command-center/index.html', 'es/centro-mando-recuperacion/index.html'
]
DEPENDENTS = [
 'assets/data/cuatrecasas-wip-reconciliation-v1.json',
 'assets/data/cuatrecasas-invoice-payment-register-v1.json',
 'data/case-graph/cuatrecasas-whole-claim-v1.json',
 'data/case-graph/dp748-impulso-apelacion-signed-20260909-v1.json'
]

class IDs(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids = set()
    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key == 'id' and value: self.ids.add(value)

def ids(text):
    parser = IDs(); parser.feed(text); return parser.ids

def dump(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + '\n'

def digest(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def relative(page, target):
    return html.escape(os.path.relpath(target, str(Path(page).parent)), quote=True)

def statement():
    return {
        'date': DATE,
        'status': 'ATTRIBUTED_FIRST_HAND_CLIENT_STATEMENT_NOT_JUDICIAL_FINDING',
        'source_reference': 'GIL-MARER-DIRECT-CONFIRMATION-27SEP2026',
        'engaging_client': 'Gil Marer states categorically that AWESWELL LIMITED alone engaged Cuatrecasas and Matkator never engaged the firm in Spain or the United Kingdom.',
        'underlying_fee_debt': 'He states that Matkator owed no underlying professional-fee debt to Cuatrecasas.',
        'delivery_purpose': 'He states that Matkator pagarés were supplied for internal-accounting accommodation under a limited/residual-purpose arrangement, not to pay Matkator legal bills; expected payment sources were the financing/transaction and hotel income.',
        'proof_boundary': 'The exact agreed restrictions and legal effect of the instruments require the contemporaneous delivery/mandate record. No unrestricted guarantee, assumption of fees or Matkator retainer is conceded. The absence of a retainer alone does not decide instrument enforceability.',
        'documentary_anchor': 'The located July-2019 22-invoice schedule contains 20 AWESWELL recipients, two LPB recipients and no Matkator recipient.',
        'correction': 'Earlier editorial wording that Matkator formal client status varies by workstream does not accurately record this categorical account. Any person asserting a Matkator engagement or assumption must identify its evidential basis; non-location alone is not proof of non-existence.'
    }

def procedural_state():
    return {
        'reviewed_as_of': DATE,
        'dp748': {
            'last_verified_event': '2026-09-16',
            'state': 'SUBSIDIARY_APPEAL_PROCESSING_AT_ORIGIN_COURT_VERIFIED',
            'source': DP_SOURCE,
            'effect': 'Submissions and accompanying document joined; Ministerio Fiscal given five days to make submissions on the subsidiary appeal.',
            'not_established': ['Fiscal response', 'remittal to Audiencia Provincial', 'appellate roll', 'reopening', 'merits outcome']
        },
        'etj163': {
            'last_verified_event': '2026-09-17',
            'state': 'REPOSICION_AGAINST_REFUSAL_TO_SUSPEND_DISMISSED',
            'source': ETJ_SOURCE,
            'effect': 'Matkator reposición against the 19-June refusal to suspend was dismissed.',
            'not_established': ['completed adjudication', 'completed remate cession', 'whole-credit assignment', 'identity or Acosta Matos connection of any ultimate recipient'],
            'later_application_status': 'Complement, certification and subsequent protective-step filing require their own signed document and filing receipt; no completion inferred.'
        },
        'scope': 'This is a bounded update to identified documents, not certification that no later document exists. Criminal, civil, insolvency and professional routes remain distinct.'
    }

def panel(page):
    es = page.startswith('es/')
    whole = 'es/cuatrecasas-matkator-reclamacion-integral/index.html' if es else 'en/cuatrecasas-matkator-whole-claim/index.html'
    recovery = 'es/centro-mando-recuperacion/index.html' if es else 'en/recovery-command-center/index.html'
    doc_links = ('<a href="'+relative(page, DP_SOURCE)+'">DP 748 · 16-09-2026</a> · '
                 '<a href="'+relative(page, ETJ_SOURCE)+'">ETJ 163 · 17-09-2026</a>')
    if es:
        title = 'Posición del cliente, estado verificado y finalidad de recuperación'
        paragraphs = [
          '<strong>Confirmación de Gil Marer, no declaración judicial:</strong> afirma categóricamente que únicamente AWESWELL LIMITED contrató a Cuatrecasas, que Matkator nunca contrató al despacho en España ni en el Reino Unido y que no adeudaba honorarios profesionales propios. Describe los pagarés como una acomodación contable interna de finalidad limitada/residual; el cobro esperado procedía de la financiación/operación y de los ingresos del hotel. No se concede una garantía irrestricta ni una asunción de deuda ajena. Las restricciones pactadas y los efectos de los instrumentos requieren su propia prueba.',
          '<strong>Dato documental distinto:</strong> la relación localizada de julio de 2019 contiene 22 facturas: 20 dirigidas a AWESWELL, dos a LPB y ninguna a Matkator. La ausencia de un encargo no decide, por sí sola, la exigibilidad de los pagarés. Se mantiene abierta la comprobación de causa, autoridad, condiciones de entrega e imputación, sin presentar un encargo de Matkator como hecho admitido.',
          '<strong>Estado procesal verificado:</strong> el 16 de septiembre se acordó unir escritos/documento y dar traslado al Ministerio Fiscal por cinco días en DP 748/2026. Esto no acredita remisión a la Audiencia Provincial, rollo, reapertura ni resultado. El 17 de septiembre se desestimó la reposición contra la negativa a suspender ETJ 163/2020; no es una resolución de adjudicación o cesión. Un complemento, otra solicitud o una comunicación posterior exige su propio justificante antes de constar como presentado/enviado.',
          '<strong>Objeto integrado, responsabilidades diferenciadas:</strong> encargo protector → trabajo/facturación → finalidad y uso de pagarés → formación del título y emplazamiento → ejecución → eventual transmisión y beneficiario. La alegación de inversión del encargo se conserva. No se acredita aquí un acuerdo con Acosta Matos ni un cesionario vinculado a ese perímetro. Factura, WIP, estimación, proforma, pagaré y principal reclamado no se suman de nuevo si incorporan el mismo trabajo; un importe descrito por el despacho no es una admisión de deuda por el cliente.'
        ]
        footer = 'Finalidades: proteger bienes y prueba; obtener el expediente y la conciliación por partida; identificar cualquier transmisión/beneficiario; y documentar decisiones e implementación. La web no sustituye presentación, notificación ni decisión judicial. Los bloques históricos fechados conservan su contexto; este panel corrige las referencias anteriores a una tramitación aún no localizada.'
        links = '<a href="'+relative(page, whole)+'">Reclamación integral</a> · <a href="'+relative(page, recovery)+'">Objetivos de recuperación</a>'
    else:
        title = 'Client position, verified status and recovery purpose'
        paragraphs = [
          '<strong>Gil Marer’s factual confirmation, not a judicial finding:</strong> he states categorically that AWESWELL LIMITED alone engaged Cuatrecasas, Matkator never engaged the firm in Spain or the United Kingdom, and Matkator owed no underlying professional-fee debt of its own. He describes the notes as an internal-accounting accommodation with a limited/residual purpose; expected payment came from financing/the transaction and hotel income. No unrestricted guarantee or assumption of another entity’s fees is conceded. The agreed restrictions and legal effect of the instruments need their own evidence.',
          '<strong>Separate documentary anchor:</strong> the located July-2019 schedule contains 22 invoices: 20 addressed to AWESWELL, two to LPB and none to Matkator. The absence of a retainer alone does not decide enforceability of the notes. Cause, authority, delivery conditions and allocation remain to be examined without describing a Matkator engagement as an admitted fact.',
          '<strong>Verified procedural state:</strong> on 16 September DP 748/2026 ordered joinder of submissions/document and a five-day transfer to the Ministerio Fiscal. This does not establish remittal to the Audiencia Provincial, an appellate roll, reopening or outcome. On 17 September the reposición against refusal to suspend ETJ 163/2020 was dismissed; that is not an adjudication or cession order. A later complement request, other application or notice needs its own receipt before it is described as filed/sent.',
          '<strong>Joined factual inquiry; separate responsibilities:</strong> protective mandate → work/billing → purpose and use of notes → title formation and service → enforcement → any transfer and beneficiary. The allegation of mandate inversion is preserved. No agreement with Acosta Matos or perimeter-connected assignee is established here. Invoice, WIP, estimate, proforma, note and claimed principal must not be added again where they incorporate the same work; a firm-stated amount is not the client’s admission of debt.'
        ]
        footer = 'Objectives: protect assets and evidence; obtain the docket and item-by-item reconciliation; identify any transfer/beneficiary; and record decisions and implementation. The website does not replace filing, service or judicial decision. Dated historical blocks retain their context; this panel corrects earlier references to court processing not yet located.'
        links = '<a href="'+relative(page, whole)+'">Whole claim</a> · <a href="'+relative(page, recovery)+'">Recovery objectives</a>'
    return ('\n<section class="section" id="'+MARKER+'" data-source-control="CUA-CLAIM-POS-20260927" aria-label="'+title+'"><div class="shell record" style="max-width:1140px;border-left:5px solid #1d5c4a;padding:1.25rem;overflow-wrap:anywhere">'
            '<p class="eyebrow">27 · 09 · 2026</p><h2>'+title+'</h2>'
            + ''.join('<p>'+p+'</p>' for p in paragraphs)
            + '<p>'+footer+'</p><p>'+doc_links+' · '+links+' · <a href="'+relative(page, CONTROL)+'">JSON</a></p></div></section>\n')

def edit_control(value):
    value['reconciled_as_of'] = DATE
    value['current_position_20260927'] = statement()
    value['current_procedural_state'] = procedural_state()
    value['current_dp748_filing_status'] = '16-SEP-2026_ORIGIN_COURT_JOINDER_AND_FISCAL_TRANSFER_VERIFIED_APPELLATE_REMITTAL_OUTCOME_OPEN'
    for role in value.get('entity_roles', []):
        if 'matkator' in role.get('entity', '').lower():
            role['entity'] = 'Matkator, S.L.U.'
            role['client_position'] = 'NO_ENGAGEMENT_AND_NO_UNDERLYING_FEE_DEBT_CATEGORICALLY_ASSERTED_BY_GIL_MARER'
            role['open'] = 'Evidential basis of any alleged assumption/guarantee, signing authority, cause, delivery restrictions and work allocation; a Matkator retainer is disputed, not presumed.'
    for gap in value.get('gaps', []):
        if gap.get('id') == 'CUA-CLAIM-GAP-008':
            gap['item'] = 'After verified 16-September origin-court processing: Fiscal response, further transfers, remittal, appellate roll, reopening and outcome; each needs its own source.'
            gap['partly_closed_by'] = DP_SOURCE
    value['outcome_controls_20260927'] = {
        'authority': 'One evidence map with separate competent procedural/professional outputs. Publication is not service or a filing.',
        'objectives': ['asset and evidence protection', 'title/service examination', 'single-satisfaction reconciliation', 'assignment and beneficiary traceability', 'professional responsibility by act and capacity', 'recovery and verified implementation'],
        'required_action_states': ['INSTRUCTED', 'ACKNOWLEDGED', 'DECLINED', 'DEFERRED', 'DRAFT', 'APPROVED', 'SIGNED', 'FILED_WITH_RECEIPT', 'SERVED', 'DECIDED', 'IMPLEMENTED', 'NOT_VERIFIED'],
        'confidentiality': 'Private instructions, legal advice, working drafts and mailbox locators remain outside public repositories. Existing expressly authorised public disclosures keep their original scope; they do not authorise later disclosures.',
        'financial_boundary': 'Firm-stated figures are attributed claims, not client admissions. Preserve work/invoice/WIP/proforma/instrument/claim lineage and single satisfaction.',
        'source_control': ARCHIVE
    }
    return value

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--commit', action='store_true')
    args = parser.parse_args()
    if args.commit and not args.apply: parser.error('--commit requires --apply')
    branch = subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()
    if args.apply and branch != BRANCH:
        raise SystemExit('Apply only on the explicitly reviewed task branch; never main.')
    for required in [CONTROL, DP_SOURCE, ETJ_SOURCE, *PAGES[:4]]:
        if not (ROOT/required).is_file(): raise SystemExit('Required source absent: '+required)
    before = {}; outputs = {}; missing = []; replacement_counts = {}
    def stage(path, text):
        old = (ROOT/path).read_text(encoding='utf-8') if (ROOT/path).exists() else ''
        if old != text: before[path]=old; outputs[path]=text
    data = json.loads((ROOT/CONTROL).read_text(encoding='utf-8'))
    stage(CONTROL, dump(edit_control(data)))
    for path in DEPENDENTS:
        if not (ROOT/path).exists(): missing.append(path); continue
        item = json.loads((ROOT/path).read_text(encoding='utf-8'))
        item['current_position_status_control'] = {'as_of': DATE, 'path': CONTROL, 'source_control': ARCHIVE, 'rule':'Historical events and financial values preserved. Current status and attributed client position are resolved through the existing whole-claim control.'}
        stage(path,dump(item))
    work = 'assets/data/legal-professional-work-product-master-v1.json'
    if (ROOT/work).exists():
        item=json.loads((ROOT/work).read_text(encoding='utf-8'))
        item['instruction_implementation_control_20260927']={
          'purpose':'Reconcile professional work privately through instruction, supplied evidence, reply, draft, approval, signature, filing, service, decision and implementation.',
          'states':data['outcome_controls_20260927']['required_action_states'],
          'public_boundary':'Publish only approved source-safe descriptions. Current counsel advice, differences of emphasis and unfiled working documents remain private; no current adviser is adverse merely because of advice or procedural narrowing.',
          'attribution':'Client, instructing entity, matter, capacity, date, authorship, filing and billing are separate fields. Acknowledgement is not adoption; a proposed step is not a completed filing.'}
        stage(work,dump(item))
    for page in PAGES:
        if not (ROOT/page).exists(): missing.append(page); continue
        old=(ROOT/page).read_text(encoding='utf-8')
        if MARKER in old: continue
        changed=old
        replacements={
          'while its formal client status varies by workstream and remains to be proved':'Gil Marer categorically denies that Matkator ever engaged the firm; any asserted instrument-based obligation or assumption of fees requires separate evidence',
          'mientras que su condición de cliente formal varía según workstream y debe probarse':'Gil Marer niega categóricamente que Matkator contratara al despacho; cualquier obligación cambiaria o asunción de honorarios que se alegue requiere prueba separada',
          'No later reposición ruling, adjudication decree, cession, registration or possession act has been located.':'Historical 9-September checkpoint, superseded as to reposición by the 17-September order: see the current status panel. Completed adjudication, cession, registration and possession still require their own source.',
          'no se ha localizado una resolución posterior de reposición, decreto de adjudicación, cesión, inscripción o acto de posesión':'corte histórico de 9 de septiembre, superado en cuanto a la reposición por el Auto de 17 de septiembre; véase el panel actual. Adjudicación, cesión, inscripción y posesión requieren su propia fuente'
        }
        count=0
        for source, target in replacements.items():
            changed,n=re.subn(re.escape(source),lambda match,t=target:t,changed,flags=re.IGNORECASE); count+=n
        replacement_counts[page]=count
        matches=list(re.finditer(r'<main(?:\s[^>]*)?>',changed,re.IGNORECASE))
        if len(matches)!=1: raise SystemExit('Expected one main element: '+page)
        end=matches[0].end(); changed=changed[:end]+panel(page)+changed[end:]
        if not ids(old).issubset(ids(changed)): raise SystemExit('Existing anchor lost: '+page)
        if changed.count('id="'+MARKER+'"')!=1: raise SystemExit('Current panel missing/duplicate: '+page)
        stage(page,changed)
    archive='''# Cuatrecasas: client position, procedural status and recovery outcomes — 27 September 2026

Continuation of the existing whole-claim, WIP, invoice/payment, DP748 and professional-work controls. No competing case architecture is created.

## Authority and bounded source basis
The owner expressly instructed updates to both repositories and websites following review of the proposed correction programme. This authorises public-safe source changes and normal review/merge/publication, not any email, legal filing or professional contact.

Gil Marer categorically states that AWESWELL LIMITED alone engaged Cuatrecasas; Matkator never engaged it in Spain or the UK and owed no underlying professional-fee debt. He describes the notes as internal-accounting accommodation under a limited/residual arrangement. This is attributed first-hand testimony, not a judicial finding or an inference merely from absent invoices. The exact agreed restrictions and legal consequences require the contemporaneous record. Neither unrestricted guarantee nor assumption of another entity's fees is conceded.

The existing 22-invoice schedule and whole-claim/WIP controls remain the bounded documentary/accounting basis. Amounts are unchanged and are not converted into admissions. The firm-stated 2022 grouped clearance proposition must be reconciled with any alleged surviving WIP or residual claim.

## Procedural correction
- DP 748: the 16-September order verifies joinder and five-day transfer to the Ministerio Fiscal at the originating court. Subsequent Fiscal response, remittal, roll, reopening and outcome are separate unclosed states.
- ETJ 163: the 17-September order dismisses reposición against refusal to suspend. It is not an adjudication/cession order or a decision establishing a criminal outcome.
- A contemplated complement, docket-certification request, preservation communication or protective application requires its own signed document and transmission/filing proof. Publication does not establish completion or formal service.

## Joined inquiry and separate legal outputs
Protective mandate → work/billing → purpose and use of notes → title formation/service → enforcement → any assignment/beneficiary. Preserve the allegation of mandate inversion without treating assignment, Acosta Matos destination, misuse of confidential information or criminal participation as proved. Claim perimeter is broader than the present finca 8.584 realization target. Each liability, proceeding and remedy retains its own test.

## Instructions and work-product method
Extend the existing professional-work master, not an adverse-actor classification: instruction and evidence supplied → response → draft → approval → signature → filing/attachments → service → decision → implementation. Declined, deferred, superseded, missing and unverified states remain distinct. Current counsel's private advice and differences of emphasis are not published. Earlier expressly authorised public strategy remains bounded to its original date/scope.

## Publication and preservation
Static panels supplement existing pages without deleting routes, evidence, contrary records, right-of-reply material, images or anchors. The capital site, homepages, shared loaders and existing release/verification configuration are not altered. Original court-source files and financial amounts are not rewritten. The source-receipt file records actual changed paths and hashes; it is not a deployment receipt. Every host needs separate merge, deployment and live verification.

Overall: AMBER — source package prepared; remote review and live closeout require independent evidence.
GitHub repository: AMBER — review/merge pending at generation.
GitHub website: AMBER — deployment/live verification pending.
GitLab repository: AMBER — separate host reconciliation pending.
GitLab website: AMBER — separate build/publication/live verification pending.
THREAD: AMBER — retain private counsel recommendations and final execution results outside chat before deletion.

Source documents: docs/cuatrecasas/DP748/2026-09-16_diligencia_ordenacion_apelacion_subs_fulltext_source_safe.md; docs/cuatrecasas/ETJ163/2026-09-17_auto_reposicion_suspension_fulltext_source_safe.md. Underlying signed court documents remain controlling.
'''
    stage(ARCHIVE,archive)
    receipt={
      'control':'CUA-CLAIM-POS-20260927','date':DATE,'status':'SOURCE_CHANGE_NOT_DEPLOYMENT',
      'scope':'Existing Cuatrecasas claim, public readers, proceeding pages and professional-work method only',
      'source_base':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
      'changed':[{'path':p,'before_sha256':digest(before[p]) if before[p] else None,'after_sha256':digest(t)} for p,t in sorted(outputs.items())],
      'not_present_on_this_host':missing,'exact_editorial_replacements':replacement_counts,
      'no_global_parity_claim':True,'no_external_email_or_filing':True
    }
    stage(RECEIPT,dump(receipt))
    # New HTML additions may contain only public-safe content. Existing source
    # bodies are preserved, not indiscriminately copied into this control.
    for page in PAGES:
        if page in outputs:
            addition=panel(page)
            for forbidden in ['mail.google.com','@sixtoabogados','@carlosllamas','IdLexNet','attachment_id','link_6a']:
                if forbidden in addition: raise SystemExit('Private locator in addition: '+page)
    for path,text in outputs.items():
        if Path(path).is_absolute() or '..' in Path(path).parts: raise SystemExit('Unsafe path')
        if path.endswith('.json'): json.loads(text)
    if not outputs: print('No source changes required.'); return
    print(dump({'planned_paths':list(outputs),'missing':missing,'editorial_replacements':replacement_counts}))
    if args.apply:
        for path,text in outputs.items():
            dest=ROOT/path; dest.parent.mkdir(parents=True,exist_ok=True); dest.write_text(text,encoding='utf-8')
        subprocess.run(['git','diff','--check'],cwd=ROOT,check=True)
    if args.commit:
        subprocess.run(['git','add','--',*outputs],cwd=ROOT,check=True)
        subprocess.run(['git','commit','-m','Reconcile Cuatrecasas client position, verified procedure and recovery outcomes'],cwd=ROOT,check=True)

if __name__=='__main__': main()
