#!/usr/bin/env python3
"""PD-CR-20260905-01: additive publication; never uploads private work product.

--write is integration-branch-only. --check and --live never write repository files.
Existing court controls are reused; private-professional correspondence is indexed
in the existing La Laguna specialist source control, not misclassified as an
authority communication. Original institutional communications remain untouched.
RAUDA is a general organisation identity, not an addition to our closed counsel roster.
"""
from __future__ import annotations
import argparse, copy, hashlib, html, json, re, subprocess, sys, time
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
BASE = 'e482e29325091bcc32af3fd2b2624335c6699e19'
BRANCH = 'integration/cuatrecasas-rauda-20260905'
CONTROL = 'PD-CR-20260905-01'
ANCHOR = 'cuatrecasas-rauda-revision-20260905'
SITE = 'https://sbu001monterecco.github.io/por-derecho/'
CANON = 'assets/data/la-laguna-proceeding-pages-v1.json'
IDENTITY = 'assets/data/matter-identity-registry-v1.json'
ORG = 'assets/data/matter-identity-registry-v1.organisations.json'
PRO_ROSTER = 'assets/data/matter-identity-registry-v1.professional-organisations.json'
INSTITUTIONAL = 'assets/data/institutional-communications-register-v1.json'
AUDIT = 'ops/CUATRECASAS_RAUDA_RELEASE_20260905.json'
NOTE = 'ops/CUATRECASAS_RAUDA_CONTINUITY_20260905.md'
CSS = 'assets/cuatrecasas-rauda-20260905.css'
PAIRS = [
 ('cuatrecasas-sun-park','cuatrecasas-sun-park','main'),
 ('cuatrecasas-icam-ccacm-2026','cuatrecasas-icam-ccacm-2026','discipline'),
 ('ingenieria-inversa-criminal-unitaria','unitary-criminal-reverse-engineering','unitary'),
 ('cuatrecasas-dp748-accion-civil','cuatrecasas-dp748-civil-action','civil'),
 ('etj-163-2020','etj-163-2020','execution'),
 ('dp-748-2026','dp-748-2026','criminal'),
 ('cambiario-1048-2019','cambiario-1048-2019','debt'),
 ('cuatrecasas-mandato-continuidad-ric','cuatrecasas-mandate-ric-continuity','mandate'),
 ('matkator-8584-titulo-hotel-remate-restitucion','matkator-8584-hotel-title-remate-restitution','property'),
 ('cnmv-ricpe-verificacion','cnmv-ricpe-verification','regulatory'),
 ('pwc-canarias-carlos-saavedra-sun-park','pwc-canarias-carlos-saavedra-sun-park','advisers'),
 ('uria-menendez-sun-park','uria-menendez-sun-park','advisers'),
]
MAIL = [
 {'control_id':'PD-CR-COM-20220218','date':'2022-02-18','source_class':'ORIGINAL_RECOVERY_CORRESPONDENCE','source_review':'PRIMARY_CORRESPONDENCE_REVIEW_RECORDED_IN_PD_CR_20260905_01','source_entity_id':'PD-SP-O-0049','title':'Cuatrecasas recovery communication identifying RAUDA-addressed collection colleagues','proves':['A recovery role was identified and disclosed in the correspondence.','Two claims were asserted; no consolidated liability of all named companies is established by the email.'],'does_not_prove':['Debt validity or allocation.','A RAUDA advisory mandate, debt acquisition, intended property purchase or unlawful common plan.'],'public_custody':'REDACTED_FACTUAL_SUMMARY_ONLY_NATIVE_CORRESPONDENCE_RETAINED_PRIVATELY'},
 {'control_id':'PD-CR-COM-20220307','date':'2022-03-07','source_class':'ORIGINAL_RECOVERY_CORRESPONDENCE','source_review':'PRIMARY_CORRESPONDENCE_REVIEW_RECORDED_IN_PD_CR_20260905_01','source_entity_id':'PD-SP-O-0049','title':'Referral of request for itemized claim information to the collection professionals','proves':['The request was referred to the identified professionals because of their involvement in proceedings.'],'does_not_prove':['That the information was subsequently supplied or withheld.','Misuse of confidential information, a remate assignment or criminality.'],'public_custody':'REDACTED_FACTUAL_SUMMARY_ONLY_NATIVE_CORRESPONDENCE_RETAINED_PRIVATELY'}
]
GAPS = [
 ('current_status','Current certified court status, effective service, appeal processing and any actual adjudication, assignment, registration or possession.'),
 ('mandate_handover','Client, instructions, accepted work, recovery handover, personnel, access, remuneration and dated conflict controls.'),
 ('single_satisfaction','Invoice, note, judgment, interest, costs, payment and realization reconciliation for each legally distinct obligor.'),
 ('property_identity','Certified title and independent physical, cadastral and registry crosswalk; finca 8584 remains distinct from 8588.'),
 ('beneficiary','Actual assignment or negotiations, price, funder, instructions and economic beneficiary; no buyer inferred from association.'),
 ('duty_and_loss','Specific duty, available protective step, breach, counterfactual, causation and claimant-specific remedy; avoid duplicate damages.'),
 ('wider_connection','A transaction- and actor-specific evidential link before extending attribution to other firms, regulated entities, public authorities or later beneficiaries.')
]

def git(*args):
    return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()

def original(path):
    return subprocess.check_output(['git','show',f'{BASE}:{path}'],cwd=ROOT).decode('utf-8')

def dump(value):
    return json.dumps(value,ensure_ascii=False,indent=2)+'\n'

def sha(value):
    return hashlib.sha256(value.encode('utf-8')).hexdigest()

def block(key,body):
    return f'<!-- {CONTROL}:{key}:BEGIN -->\n{body}\n<!-- {CONTROL}:{key}:END -->'

def managed(text):
    return re.findall(r'<!-- '+CONTROL+r':[A-Z]+:BEGIN -->.*?<!-- '+CONTROL+r':[A-Z]+:END -->',text,re.S)

def remove_managed(text):
    return re.sub(r'<!-- '+CONTROL+r':[A-Z]+:BEGIN -->.*?<!-- '+CONTROL+r':[A-Z]+:END -->','',text,flags=re.S)

class Parser(HTMLParser):
    def __init__(self,text):
        super().__init__();self.ids=[];self.hrefs=[];self.images=[];self.scripts=[];self.feed(text)
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if 'id' in d:self.ids.append(d['id'])
        if tag in ('a','link') and d.get('href'):self.hrefs.append(d['href'])
        if tag=='img':self.images.append(d.get('src',''))
        if tag=='script':self.scripts.append(d.get('src','INLINE'))

def identity_outputs():
    manifest=json.loads(original(IDENTITY));orgs=json.loads(original(ORG));allrows=[]
    for part in manifest['parts']:
        allrows.extend(json.loads(original('assets/data/'+part['path']))['records'])
    hits=[r for r in allrows if r.get('type')=='ORGANISATION' and any(v.casefold()=='rauda' for v in [r.get('name',''),*r.get('aliases',[])])]
    assert len(hits)<=1,'Ambiguous RAUDA identity: stop for reconciliation'
    if hits:return {},hits[0]['id']
    n=max(int(r['id'].rsplit('-',1)[-1]) for r in allrows if r.get('type')=='ORGANISATION')+1
    rid=f'PD-SP-O-{n:04d}'
    assert not any(r['id']==rid for r in allrows)
    orgs['records'].append({'id':rid,'type':'ORGANISATION','name':'RAUDA','aliases':['Rauda'],'status':'CONTROLLED_PERIMETER_LABEL_EXACT_ENTITY_MAY_REQUIRE_SOURCE','identity_resolution':'CARET_PENDING','identity_sources':[m['control_id'] for m in MAIL],'routes':{lang:f'/{lang}/cuatrecasas-sun-park/#{ANCHOR}' for lang in ('es','en')},'capacity_boundary':'Source-literal professional recovery label from 2022 correspondence. Exact legal entity and legal-form history remain unverified. No original advisory mandate, ownership of the debt, purchaser identity, confidentiality misuse, group-wide knowledge or liability is inferred.'})
    for part in manifest['parts']:
        if part['path']==Path(ORG).name:part['count']=len(orgs['records'])
    manifest['counts']['ORGANISATION']+=1;manifest['counts']['total']+=1
    manifest['coverage']['required_names'].append('RAUDA')
    manifest['recovery_identity_control']={'control_id':CONTROL,'as_of':'2026-09-05','identity_id':rid,'state':'SOURCE_LITERAL_ONLY_NO_CARET_OR_EXACT_LEGAL_ENTITY_UPGRADE'}
    return {ORG:dump(orgs),IDENTITY:dump(manifest)},rid

def canonical_output(rid):
    d=json.loads(original(CANON));text=dump(d)
    for key in ['PD-ETJ163-FIL-20260903','PD-DP748-ACT-004','PD-DP748-NOT-001']:
        assert key in text,'Missing existing procedural control '+key
    existing=d.setdefault('professional_recovery_communications',[])
    for row in MAIL:
        collision=[x for x in existing if x.get('control_id')==row['control_id'] or (x.get('date')==row['date'] and 'RAUDA' in dump(x))]
        assert not collision,'Existing communication needs explicit reconciliation, not duplication'
        row=copy.deepcopy(row);row['related_identity_ids']=['PD-SP-O-0049',rid];existing.append(row)
    d['professional_recovery_review']={'control_id':CONTROL,'review_date':'2026-09-05','scope':'PUBLIC_SAFE_SOURCE_SUMMARY_AND_REVERSE_ENGINEERED_MULTITRACK_REVIEW','communications_control_ids':[m['control_id'] for m in MAIL],'reused_procedural_controls':['PD-ETJ163-FIL-20260903','PD-DP748-ACT-004','PD-DP748-NOT-001'],'procedural_status_changed':False,'institutional_register_changed':False,'canonical_boundary':'Private-professional source controls are kept here; they are not relabelled as public-authority communications. Existing court acts are referenced rather than created again. Email wrappers and internal strategy are not new judicial acts.','identity_id':rid,'routes':{lang:f'/{lang}/cuatrecasas-sun-park/#{ANCHOR}' for lang in ('es','en')},'open_evidence':[{'key':key,'requirement':value} for key,value in GAPS],'no_external_action':True}
    return dump(d)

def source_rows(lang):
    if lang=='en':
        a='18 February 2022 · original recovery correspondence';b='7 March 2022 · request for itemized claim information';c='3 September 2026 · ETJ 163/2020 party pleading';e='16 July 2026 · DP 748/2026 order'
        ap='A disclosed collection role and asserted claims; not proof of debt validity, a RAUDA purchase or a concealed common plan.';bp='Referral to the collection professionals; not proof that records were later supplied, withheld or misused.'
        cp='Existing control PD-ETJ163-FIL-20260903. Requested continuation and adjudication with reserved cession; not a completed transfer.';ep='Existing control PD-DP748-ACT-004 / DP748-2026-20260716-AUTO. Provisional dismissal maintained; reopening was not ordered.'
        etj='2026-09-03_cuatrecasas_opposition_fulltext_en.md';dp='2026-09-01_order_16jul2026_fulltext_en.md';label='Existing public-safe full text';reg='Canonical specialist source control'
    else:
        a='18 de febrero de 2022 · correspondencia original de recobro';b='7 de marzo de 2022 · solicitud de información desglosada';c='3 de septiembre de 2026 · escrito de parte en ETJ 163/2020';e='16 de julio de 2026 · Auto en DP 748/2026'
        ap='Intervención de recobro comunicada y reclamaciones afirmadas; no acredita validez de la deuda, compra por RAUDA ni plan común oculto.';bp='Remisión a los profesionales del recobro; no acredita posterior entrega, retención o uso indebido de documentación.'
        cp='Control existente PD-ETJ163-FIL-20260903. Petición de continuación y adjudicación con reserva de cesión; no transmisión consumada.';ep='Control existente PD-DP748-ACT-004 / DP748-2026-20260716-AUTO. Se mantiene el sobreseimiento provisional; no se ordena reapertura.'
        etj='2026-09-03_cuatrecasas_impugnacion_reposicion_fulltext_source_safe.md';dp='2026-09-01_auto_16jul2026_fulltext_source_safe.md';label='Texto público seguro existente';reg='Control canónico de fuentes especializado'
    rows=[('PD-CR-COM-20220218',a,ap,''),('PD-CR-COM-20220307',b,bp,''),('PD-CR-SOURCE-ETJ163-20260903',c,cp,f'/por-derecho/docs/cuatrecasas/ETJ163/{etj}'),('PD-CR-SOURCE-DP748-20260716',e,ep,f'/por-derecho/docs/cuatrecasas/DP748/{dp}')]
    out=[]
    for ident,title,body,url in rows:
        link=f' <a href="{url}">{label}</a>.' if url else ''
        out.append(f'<div class="pd-cr-source" id="{ident}"><p><strong>{title}</strong> — {body}{link}</p></div>')
    out.append(f'<p><a href="/por-derecho/{CANON}">{reg}</a>.</p>')
    return '\n'.join(out)

def navigation(lang):
    labels={'discipline':('Deontología','Professional discipline'),'unitary':('Reconstrucción unitaria','Unitary reconstruction'),'civil':('Acción civil','Civil action'),'execution':('ETJ 163/2020','ETJ 163/2020'),'criminal':('DP 748/2026','DP 748/2026'),'debt':('Cambiario 1048/2019','Cambiario 1048/2019'),'mandate':('Mandato y continuidad RIC','Mandate and RIC continuity'),'property':('Título, remate y restitución','Title, remate and restitution'),'regulatory':('CNMV / RICPE','CNMV / RICPE'),'advisers':('Otros asesores: contraste específico','Other advisers: separate examination')}
    links=[]
    for es,en,kind in PAIRS[1:]:
        slug=es if lang=='es' else en;label=labels[kind][0 if lang=='es' else 1]
        if kind=='advisers':label=('PwC' if slug.startswith('pwc') else 'Uría Menéndez')+' — '+label
        links.append(f'<a href="/por-derecho/{lang}/{slug}/">{label}</a>')
    return '<nav class="pd-cr-links" aria-label="'+('Rutas relacionadas' if lang=='es' else 'Related routes')+'">'+' · '.join(links)+'</nav>'

def outputs():
    out,rid=identity_outputs();out[CANON]=canonical_output(rid)
    out[PRO_ROSTER]=original(PRO_ROSTER)
    out[CSS]='.pd-cr-review,.pd-cr-crosslink{overflow-wrap:anywhere;scroll-margin-top:7rem}.pd-cr-review .tablewrap{max-width:100%;overflow-x:auto}.pd-cr-review table{width:100%;border-collapse:collapse;table-layout:fixed}.pd-cr-review th,.pd-cr-review td{padding:.8rem;vertical-align:top;text-align:left;border-bottom:1px solid currentColor}.pd-cr-review .pd-cr-source{padding:.35rem 0;scroll-margin-top:7rem}.pd-cr-review .pd-cr-links{line-height:1.9}.pd-cr-jump{padding:.6rem 0}.pd-cr-review .record{max-width:100%}@media(max-width:600px){.pd-cr-review th{width:32%}.pd-cr-review td,.pd-cr-review th{padding:.5rem;font-size:.95rem}}\n'
    page_audit=[]
    for es,en,kind in PAIRS:
        for lang,slug in [('es',es),('en',en)]:
            path=f'{lang}/{slug}/index.html';base=original(path)
            assert base.lower().count('</main>')==1 and base.lower().count('</head>')==1,path
            if kind=='main':
                content=(ROOT/f'assets/content/cuatrecasas-rauda-20260905.{lang}.html').read_text()
                content=content.replace('<!-- PD-CR-SOURCE-ROWS -->',source_rows(lang))
                note=('RAUDA se registra como denominación presente en las fuentes; su entidad jurídica exacta sigue pendiente. El identificador no acredita mandato, control ni responsabilidad.' if lang=='es' else 'RAUDA is recorded as a source-literal label; its exact legal entity remains unresolved. The identifier establishes no mandate, control or liability.')
                content=content.replace('<!-- PD-CR-IDENTITY-NOTE -->',f'<p class="pd-cr-identity" data-caepr-id="{rid}" data-caret-state="CARET_PENDING"><small>{note} {rid}.</small></p>').replace('<!-- PD-CR-RELATED-LINKS -->',navigation(lang))
                assert '<!-- PD-CR-' not in content
                jump=('Revisión Cuatrecasas–RAUDA de 5 de septiembre: fuentes, vías y límites' if lang=='es' else '5 September Cuatrecasas–RAUDA review: sources, routes and limits')
                page=re.sub(r'(<h1\b[^>]*>.*?</h1>)',lambda m:m.group(1)+block('JUMP',f'<p class="pd-cr-jump"><a href="#{ANCHOR}">{jump}</a></p>'),base,count=1,flags=re.S|re.I)
            else:
                title=('Cuatrecasas–RAUDA: del mandato al recobro y al remate' if lang=='es' else 'Cuatrecasas–RAUDA: from mandate to recovery and remate')
                text=('Una investigación fáctica conectada, con pruebas penales, civiles, deontológicas y de recuperación separadas. Incluye las comunicaciones de recobro de 2022, el escrito de 3 de septiembre y el sobreseimiento provisional de julio; no presume cesión, culpabilidad ni suspensión.' if lang=='es' else 'One connected factual inquiry with distinct criminal, civil, professional-discipline and recovery tests. Includes the 2022 recovery correspondence, 3 September pleading and July provisional dismissal; no assignment, guilt or stay is presumed.')
                content=f'<section id="{ANCHOR}-crosslink" class="pd-cr-crosslink"><h2>{title}</h2><p>{text} <a href="/por-derecho/{lang}/cuatrecasas-sun-park/#{ANCHOR}">'+('Leer fuentes, contraste y prueba pendiente' if lang=='es' else 'Read the sources, countercase and outstanding evidence')+'</a>.</p></section>'
                page=base
            page=page.replace('</main>',block('BODY',content)+'</main>',1)
            page=page.replace('</head>',block('STYLE',f'<link rel="stylesheet" href="/por-derecho/{CSS}">')+'</head>',1)
            assert remove_managed(page)==base,'Existing content changed: '+path
            out[path]=page
            page_audit.append({'path':path,'role':kind,'baseline_sha256':sha(base),'output_sha256':sha(page),'blocks_sha256':[sha(b) for b in managed(page)]})
    institutional=json.loads(original(INSTITUTIONAL))
    assert len(institutional['events'])==333
    notes=f'''# Cuatrecasas–RAUDA publication continuity — 5 September 2026

Control: {CONTROL}. Source state: PREPARED_PENDING_MERGE. Actual PR, merge, Pages and live evidence belong in Issue #1428 and the release PR, not in a self-certifying source claim.

## Scope and authoritative records
The English and Spanish source fragments supply the public-safe substantive update. Existing page text, images, links, identities and procedural facts are preserved. The existing La Laguna specialist control now indexes the two original private-professional recovery communications as PD-CR-COM-20220218 and PD-CR-COM-20220307. It reuses PD-ETJ163-FIL-20260903, PD-DP748-ACT-004 and PD-DP748-NOT-001; it does not create duplicate judicial acts or recast email forwarding as filing. The 333-row institutional register remains byte-identical because private recovery correspondence is not an institutional notice. RAUDA is identity {rid}, source-literal only, exact legal entity pending; no caret upgrade. It belongs to the general organisation registry, not the closed roster of our former/current professional organisations, which remains byte-identical.

## Evidential and private boundaries
The 2022 collection role was disclosed. There is no newly proved advisory mandate for RAUDA, debt purchase, completed adjudication, cessionary, common plan, automatic stay or final liability. The July provisional dismissal and the opponent's substantive countercase remain visible. Fincas 8584/8588, companies, estates, clients, note makers and judgment debtors remain separate. Wider harm needs right-specific causation and valuation.

The full private handoff, raw court copies, original emails, provider locators, signature/verification identifiers, internal advice and the unclosed July/September knowledge/chronology hypothesis remain outside this public repository. Recover the private handoff from the originating conversation when authorised. Do not recreate missing primary facts from this public summary. Publication is not filing, service, notification, institutional endorsement or a deadline-preservation act.

## Finite work that remains
'''+''.join(f'- {key}: {value}\n' for key,value in GAPS)+'''
## Reuse and deployment
Refresh current main and PD-MTCP-20260904-01 before further work. Reuse the canonical controls above; preserve the public-safe summaries and underlying private custody distinction. The builder is deterministic and integration-only for writes. Read-only CI compares broader inherited failures with the immutable baseline, tests desktop/mobile/no-script and validates the exact changed blocks. Main automation only verifies. No unrelated worker branch, history rewrite, global gate change, email or legal filing is part of this release.
'''
    out[NOTE]=notes
    audit={'schema':'por-derecho.cuatrecasas-rauda-publication.v1','control_id':CONTROL,'source_state':'PREPARED_PENDING_MERGE','as_of':'2026-09-05','source_base':BASE,'branch':BRANCH,'public_private_boundary':'PUBLIC_SAFE_DERIVATIVE_ONLY','canonical_source_control':CANON,'rauda_identity_id':rid,'institutional_register_rows':333,'institutional_register_sha256':sha(original(INSTITUTIONAL)),'reused_court_controls':['PD-ETJ163-FIL-20260903','PD-DP748-ACT-004','PD-DP748-NOT-001'],'recovery_communication_controls':[m['control_id'] for m in MAIL],'pages':page_audit,'outputs':sorted(out),'verification_boundary':'This source manifest describes prepared deterministic outputs, not a completed merge, deployment or live verification.'}
    out[AUDIT]=dump(audit)
    return out

def verify(out):
    checks=0
    for path,text in out.items():
        actual=(ROOT/path).read_text(encoding='utf-8')
        assert actual==text,'Deterministic output drift: '+path;checks+=1
        if path.endswith('index.html'):
            base=original(path);assert remove_managed(actual)==base;checks+=1
            old=Parser(base);new=Parser(actual)
            assert old.images==new.images and old.scripts==new.scripts;checks+=1
            old_duplicates={k for k in old.ids if old.ids.count(k)>1}
            assert {k for k in new.ids if new.ids.count(k)>1}<=old_duplicates;checks+=1
            added='\n'.join(managed(actual));p=Parser(added)
            assert not re.search(r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}',added),'Contact leak'
            assert not re.search(r'(?:gmail_message_id|provider_id|PRIVATE_REVIEW_WORK_PRODUCT|BEGIN PRIVATE KEY|data:application)',added,re.I),'Private material'
            for href in p.hrefs:
                u=urlsplit(urljoin(SITE+path,href))
                if u.netloc!='sbu001monterecco.github.io':continue
                rel=unquote(u.path).removeprefix('/por-derecho/')
                if rel.endswith('/'):rel+='index.html'
                target=ROOT/rel
                assert target.is_file(),'Missing target '+rel
                if u.fragment and target.suffix=='.html':assert unquote(u.fragment) in Parser(target.read_text()).ids,'Missing anchor '+href
                checks+=1
    assert (ROOT/INSTITUTIONAL).read_text()==original(INSTITUTIONAL);checks+=1
    assert (ROOT/PRO_ROSTER).read_text()==original(PRO_ROSTER);checks+=1
    old=json.loads(original(CANON));new=json.loads(out[CANON])
    for key,value in old.items():assert new[key]==value,'Existing canonical field modified '+key;checks+=1
    old=json.loads(original(ORG));new=json.loads(out.get(ORG,original(ORG)))
    assert new['records'][:len(old['records'])]==old['records'];checks+=1
    for name in [IDENTITY,ORG,CANON]:json.loads((ROOT/name).read_text());checks+=1
    subprocess.run([sys.executable,'scripts/validate_legal_professional_register.py'],cwd=ROOT,check=True);checks+=1
    print(json.dumps({'result':'SCOPED_PASS','checks':checks,'managed_pages':len(PAIRS)*2,'institutional_events_preserved':333,'no_private_payload':True,'closed_professional_roster_preserved':True}))

def live(out):
    audit=json.loads(out[AUDIT]);pending={r['path']:r for r in audit['pages']};pending[AUDIT]=None;head=git('rev-parse','HEAD');deadline=time.monotonic()+600
    while pending and time.monotonic()<deadline:
        for path,row in list(pending.items()):
            route=path.removesuffix('index.html') if path.endswith('index.html') else path
            try:
                req=Request(SITE+route+'?pd-cr='+head,headers={'Cache-Control':'no-cache','User-Agent':'PorDerecho-Release-Verification'})
                with urlopen(req,timeout=25) as r:text=r.read().decode('utf-8')
                good=text==out[path] if row is None else [sha(b) for b in managed(text)]==row['blocks_sha256']
                if good:print('LIVE_MATCH',path,head);del pending[path]
            except Exception as exc:print('LIVE_PENDING',path,type(exc).__name__)
        if pending:time.sleep(15)
    assert not pending,'Public readback incomplete: '+','.join(pending)
    print(json.dumps({'result':'LIVE_VERIFIED','commit':head,'resources':len(audit['pages'])+1,'scope':'exact managed blocks and source release manifest; no merits finding'}))

def main():
    a=argparse.ArgumentParser();g=a.add_mutually_exclusive_group(required=True);g.add_argument('--write',action='store_true');g.add_argument('--check',action='store_true');g.add_argument('--live',action='store_true');args=a.parse_args()
    git('cat-file','-e',BASE+'^{commit}')
    out=outputs()
    if args.write:
        assert git('branch','--show-current')==BRANCH,'Writes are integration-only'
        assert git('rev-parse','origin/main')==BASE,'Main advanced: reconcile first'
        for path,text in out.items():
            p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8')
        verify(out)
        print('ALLOWED_GENERATED_PATHS',json.dumps(sorted(out)))
    elif args.check:verify(out)
    else:live(out)

if __name__=='__main__':main()
