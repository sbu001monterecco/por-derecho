#!/usr/bin/env python3
"""Activate operative wording on the twenty reviewed Cuatrecasas readers.

This is a source transformation, not a filing, service, deployment or outcome.
No network calls. Existing historical source words and financial data survive.
"""
from __future__ import annotations
import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BRANCH = 'agent/cuatrecasas-operative-closeout-20260927'
OLD_MARKER = 'cuatrecasas-position-status-20260927'
MARKER = 'cuatrecasas-operative-programme-20260927'
POLICY = 'governance/OPERATIVE_ACTION_LANGUAGE_AND_EVIDENCE_STATE_27SEP2026.md'
CONTROL = 'assets/data/cuatrecasas-whole-claim-architecture-v1.json'
RECEIPT = 'ops/cuatrecasas-operative-source-receipt-20260927.json'
EN = ('<p id="'+MARKER+'"><strong>Programme in motion.</strong> The documentary reconciliation, preservation and public-record correction programme is active. We are maintaining the joined mandate, billing, instrument, title/service, enforcement and beneficiary record, and pursuing protection, accountability and recovery through the appropriate distinct channels. Each action is recorded at its evidenced stage: instruction, preparation, transmission, filing, decision or implementation. An active programme is not a representation that every requested step has been filed, ordered, served or completed. Private advice remains private; historical quotations and court decisions retain their original wording and date.</p>')
ES = ('<p id="'+MARKER+'"><strong>Programa en marcha.</strong> Está activado el programa de conciliación documental, preservación y corrección del registro público. Mantenemos integrado el expediente de encargo, facturación, instrumentos, formación del título y emplazamiento, ejecución y beneficiario, e impulsamos protección, responsabilidad y recuperación por sus cauces competentes y diferenciados. Cada actuación consta en su fase acreditada: instrucción, preparación, remisión, presentación, resolución o ejecución material. La activación del programa no significa que todas las medidas solicitadas hayan sido presentadas, acordadas, notificadas o completadas. El asesoramiento privado sigue siendo privado; las citas históricas y resoluciones conservan su texto y fecha originales.</p>')
POLICY_TEXT = '''# Operative action language and evidence state — 27 September 2026

Control: PD-OPERATIVE-LANGUAGE-20260927. Status: ACTIVE. Parent: existing Por Derecho / Project Sun Rock source, publication and professional-work controls.

The owner has activated the programme and directs that current work is described as work in motion, not as a repeatedly hypothetical proposal. This rule changes editorial posture, not underlying facts, legal status or authority.

## Operative wording
Use direct, stage-correct language: “the programme is active”; “we are reconciling the record”; “the correction has been committed”; “the application is in preparation”; “the request has been sent” only with transmission evidence; “the application was filed” only with the signed filing and receipt; “the court ordered” only with the order; “implemented” only with implementation evidence.

Do not reframe an activated and authorised workstream as merely something we could consider. Name the actual current act and its next controlled step. A blocked workstream remains active with an explicit blocker; it does not become completed by changing its tense or colour.

## Non-conversion rules
ACTIVE is not SENT, FILED, ADMITTED, ORDERED, DEPLOYED or IMPLEMENTED. Owner instructions to the assistant are not proof that counsel received or adopted them. A prepared counsel message is not a sent instruction. A procedural request is not an order. An order is not proof of compliance. A repository merge is not a live deployment. Published allegations are not findings.

Historical emails, quotations, signed filings, judgments, invoices and source transcripts retain their original wording, dates and evidential status. Do not silently rewrite their conditional or future language as a completed historical event. Add a dated status update instead.

Keep documentary fact, the client's categorical first-hand account, attributed allegation, inference, contrary evidence and missing proof separate. Preserve entity, capacity, proceeding and source distinctions. Current counsel advice, unfiled working papers and private communications remain in controlled private custody unless the exact disclosure is separately authorised.

## Colour and closeout rule
GREEN requires evidence that the specified gate passed. Track source preparation, review, merge, deployment and live verification independently for GitHub and GitLab. A paid-compute, permission, CI, missing-source or external-response blocker remains AMBER/RED at the affected gate. Never change a status, skip a validator, change a permission or assert parity merely to meet a green target.

## Spanish publication rule
Redactar la actuación actual como programa activado y trabajo en curso, identificando su fase acreditada. “En marcha” no equivale a remitido, presentado, admitido, acordado, publicado o ejecutado. Las citas y fuentes históricas no se reescriben. Las limitaciones operativas se expresan de forma concreta y no se ocultan mediante el tiempo verbal.

This policy does not authorise emails, filings, payments, account changes or disclosure of private material. It governs the wording of actions separately authorised and actually undertaken.
'''

class Document(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids=[]; self.images=[]
    def handle_starttag(self, tag, attrs):
        data=dict(attrs)
        if 'id' in data:self.ids.append(data['id'])
        if tag=='img':self.images.append(data)

def transform(text: str, spanish: bool) -> str:
    if 'id="'+MARKER+'"' in text:return text
    match=re.search(r'<section\b[^>]*\bid="'+OLD_MARKER+r'"[^>]*>',text)
    if not match:raise ValueError('Reviewed current-status panel is absent')
    heading=re.search(r'</h2\s*>',text[match.end():],re.I)
    if not heading:raise ValueError('Current-status heading is absent')
    pos=match.end()+heading.end()
    addition=ES if spanish else EN
    result=text[:pos]+addition+text[pos:]
    old=Document();old.feed(text);new=Document();new.feed(result)
    if not set(old.ids)<=set(new.ids) or old.images!=new.images:
        raise ValueError('Historical anchors or images changed')
    if result.replace(addition,'',1)!=text:
        raise ValueError('Transformation is not strictly additive')
    return result

def sha(text:str)->str:return hashlib.sha256(text.encode()).hexdigest()
def dump(item)->str:return json.dumps(item,ensure_ascii=False,indent=2)+'\n'

def main()->None:
    parser=argparse.ArgumentParser();parser.add_argument('--apply',action='store_true');parser.add_argument('--commit',action='store_true');args=parser.parse_args()
    if args.commit and not args.apply:parser.error('--commit requires --apply')
    if args.apply and subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()!=BRANCH:
        raise SystemExit('Apply only on the authorised operative-closeout branch')
    previous=json.loads((ROOT/'ops/cuatrecasas-position-status-source-receipt-20260927.json').read_text())
    pages=sorted(row['path'] for row in previous['changed'] if row['path'].endswith('.html'))
    if len(pages)!=20:raise SystemExit('Unexpected existing scope')
    outputs={};before={}
    def stage(path,text):
        old=(ROOT/path).read_text() if (ROOT/path).exists() else ''
        if old!=text:outputs[path]=text;before[path]=old
    for path in pages:stage(path,transform((ROOT/path).read_text(),path.startswith('es/')))
    stage(POLICY,POLICY_TEXT)
    for path in ['AGENTS.md','CHATGPT_START_HERE.md']:
        old=(ROOT/path).read_text()
        if POLICY not in old:
            stage(path,'> **Operative-language rule — PD-OPERATIVE-LANGUAGE-20260927:** current authorised work is described as an active programme at its evidenced stage. Read ['+POLICY+']('+POLICY+'). Active does not mean sent, filed, ordered, deployed or implemented; preserve historical source words and disclose blocked gates.\n\n'+old)
    obj=json.loads((ROOT/CONTROL).read_text());financial=json.dumps(obj['billing_snapshot'],sort_keys=True)
    obj['active_workprogramme_20260927']={
      'status':'ACTIVE_SOURCE_RECONCILIATION_PRESERVATION_AND_PUBLIC_RECORD_CORRECTION',
      'authority':'Owner instruction of 27 September 2026 to execute the repository/website programme and use operative language.',
      'language_control':POLICY,
      'programme':'The documentary programme is in motion. The client pursues protection, accountability and recovery through distinct competent channels.',
      'external_action_rule':'Every counsel instruction, transmission, filing, service, decision and implementation keeps its own evidenced state. This update certifies none of the still-unverified external steps.',
      'host_rule':'GitHub and GitLab source, review, merge, deployment and live verification are separate gates. Failed compute or checks are not relabelled green.',
      'preserved_financial_snapshot':True}
    assert json.dumps(obj['billing_snapshot'],sort_keys=True)==financial
    stage(CONTROL,dump(obj))
    receipt={'control':'PD-OPERATIVE-LANGUAGE-20260927','date':'2026-09-27','stage':'SOURCE_PREPARATION_NOT_DEPLOYMENT','base_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'pages':pages,'changed':[{'path':p,'before_sha256':sha(before[p]) if before[p] else None,'after_sha256':sha(t)} for p,t in sorted(outputs.items())],'historical_html_body_retained':True,'image_and_anchor_sets_retained':True,'financial_snapshot_retained':True,'no_private_advice_added':True,'no_external_email_or_filing':True}
    stage(RECEIPT,dump(receipt))
    print(dump({'changed':list(outputs),'pages':len(pages)}))
    if args.apply:
        for p,t in outputs.items():
            dest=ROOT/p;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(t)
        subprocess.run(['git','diff','--check'],cwd=ROOT,check=True)
    if args.commit and outputs:
        subprocess.run(['git','add','--',*outputs],cwd=ROOT,check=True)
        subprocess.run(['git','commit','-m','Activate evidence-correct operative wording across twenty bilingual readers'],cwd=ROOT,check=True)

if __name__=='__main__':main()
