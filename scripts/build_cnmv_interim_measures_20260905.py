#!/usr/bin/env python3
"""Deterministic, additive CNMV publication. No email, filing or external write.

--write: prepare only in an explicitly checked integration working tree.
--check: deterministic output, original-content, register and link assertions.
--live: read-only exact public-file / managed-block verification.
"""
from __future__ import annotations
import argparse, hashlib, html, json, re, subprocess, time
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote, urljoin
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
BASE = '66003743d2cb3a1807c1f3765c530bf639857da3'
CONTROL = 'PD-CNMV-INTERIM-20260905-01'
DATA = 'assets/data/cnmv-interim-measures-20260905.json'
AUDIT = 'ops/CNMV_INTERIM_PUBLICATION_AUDIT_20260905.json'
CSS = 'assets/cnmv-interim-measures-20260905.css'
JS = 'assets/cnmv-interim-measures-20260905.js'
PREFIX = '/por-derecho/'
HOST = 'https://sbu001monterecco.github.io/por-derecho/'
ROUTES = {'en':'en/authorities-duties-asset-recovery/index.html', 'es':'es/autoridades-deberes-recuperacion-activos/index.html'}
CNMV = {'en':'en/cnmv-ricpe-verification/index.html', 'es':'es/cnmv-ricpe-verificacion/index.html'}
INST = {'en':'en/institutional-records/', 'es':'es/registros-institucionales/'}
MARK = 'CNMV-INTERIM-20260905'
START, END = '<!-- '+MARK+':START -->', '<!-- '+MARK+':END -->'
HSTART, HEND = '<!-- '+MARK+':HEAD -->', '<!-- '+MARK+':HEAD-END -->'
JSTART, JEND = '<!-- '+MARK+':JUMP -->', '<!-- '+MARK+':JUMP-END -->'
D = json.loads((ROOT/DATA).read_text())
S = D['sources']

def esc(s): return html.escape(str(s), quote=True)
def jdump(x): return json.dumps(x, ensure_ascii=False, indent=2)+'\n'
def digest(b): return hashlib.sha256(b).hexdigest()
def link(path, label): return '<a href="'+esc(PREFIX+path.removesuffix('index.html'))+'">'+esc(label)+'</a>'
def src(keys):
    return '<p class="ca-sources">'+' · '.join('<a href="'+esc(S[k][1])+'" rel="external noopener">'+esc(S[k][0])+'</a>' for k in keys)+'</p>'
def p(s): return '<p>'+esc(s)+'</p>'
def title(s,n=2): return '<h'+str(n)+'>'+esc(s)+'</h'+str(n)+'>'
def sec(i,t,b): return '<section class="ca-section" id="'+i+'">'+title(t)+b+'</section>\n'
def select(l,en,es): return en if l=='en' else es

def original(path):
    r=subprocess.run(['git','show',BASE+':'+path],cwd=ROOT,capture_output=True)
    if r.returncode: raise RuntimeError('Required base file not available: '+path)
    return r.stdout.decode('utf-8')

def strip_owned(text):
    for a,b in [(START,END),(HSTART,HEND),(JSTART,JEND)]:
        text=re.sub(re.escape(a)+r'.*?'+re.escape(b),'',text,flags=re.S)
    return text

def event(l, ident, label): return link(INST[l]+'#communication-'+ident,label)

def action(l, standalone=False):
    aid = 'cnmv-action' if standalone else select(l,'interim-measures','medidas-provisionales')
    gt = link(ROUTES[l],select(l,'Full authority and asset-recovery guide','Guía completa de autoridades y recuperación'))
    cp = link(CNMV[l],select(l,'CNMV documentary landing page','Página documental CNMV'))
    status = select(l,'PUBLIC REQUEST · 5 SEPTEMBER 2026 · NOT AN OFFICIAL ORDER OR PROOF OF SERVICE','SOLICITUD PÚBLICA · 5 SEPTIEMBRE 2026 · NO ES RESOLUCIÓN NI ACREDITACIÓN DE NOTIFICACIÓN')
    heading=select(l,'CNMV: preserve the evidence, assess interim protection, explain what may lawfully be made public.','CNMV: preservar la prueba, valorar medidas provisionales y dar publicidad a lo legalmente procedente.')
    intro=select(l,'We invite the competent CNMV teams to use this landing page and the linked source record to connect the reported facts to a concrete, proportionate action. We request assessment and lawful action—not acceptance of a predetermined finding of criminality, a blanket seizure or closure of lawful businesses.','Invitamos a los equipos competentes de CNMV a utilizar esta página y las fuentes enlazadas para conectar los hechos comunicados con una actuación concreta y proporcionada. Solicitamos valoración y actuación legal, no adhesión a una conclusión penal predeterminada, embargo indiscriminado ni cierre de empresas lícitas.')
    b='<div class="ca-kicker">'+status+'</div>'+title(heading)+p(intro)
    b+='<div class="ca-banner"><strong>'+select(l,'Publication is not formal delivery.','Publicación no equivale a presentación formal.')+'</strong> '+select(l,'This release does not record a new email, REG-AGE submission, CNMV intervention, judicial freeze or preservation order as sent, filed or granted.','Esta entrega no registra como enviados, presentados o acordados un nuevo correo, escrito REG-AGE, intervención CNMV, embargo judicial o requerimiento de preservación.')+'</div>'
    b+='<div class="ca-links">'+gt+' · '+cp+'</div>'
    b+='<div class="ca-grid ca-three">'
    statuses=[
        (select(l,'A regulated starting point','Punto de partida regulado'),select(l,'The official register lists RIC PRIVATE EQUITY INVESTMENT PARTNERS, S.C.R., S.A., no.295, registered 25 October 2019. Registration does not establish misconduct, a listed-security nexus or the statutory intervention threshold.','El registro oficial identifica RIC PRIVATE EQUITY INVESTMENT PARTNERS, S.C.R., S.A., nº295, inscrita el 25 de octubre de 2019. La inscripción no acredita infracción, negociación de valores ni el umbral de intervención.'),src(['CNMVREG'])),
        (select(l,'6 May 2026: action was acknowledged','6 mayo 2026: actuación reconocida'),select(l,'CNMV stated that the reported facts had been taken into account in its supervisory activity and invoked supervisory secrecy. The question is the scope, adequacy and next legally justified step—not an unsupported assertion that CNMV did nothing.','CNMV comunicó que los hechos se habían tenido en cuenta en sus actuaciones supervisoras e invocó el secreto supervisor. La cuestión es su alcance, suficiencia y siguiente actuación legalmente justificada, no afirmar sin base que no hizo nada.'),link(l+'/ric-private-equity-sun-park/',select(l,'Existing RICPE source dossier','Dossier RICPE existente'))+src(['LMV'])),
        (select(l,'4 September: access timetable extended','4 septiembre: ampliación del plazo de acceso'),select(l,'Incoming 2026114903 / outgoing 2026149422: one additional month for the public-information decision because of volume and complexity. It is not a refusal, a merits decision or a decision to suspend all separate supervisory/preservation work.','Entrada 2026114903 / salida 2026149422: un mes adicional para resolver acceso por volumen y complejidad. No es denegación, resolución de fondo ni decisión de suspender toda función separada de supervisión o preservación.'),event(l,'PD-SP-EVT-0177','PD-SP-EVT-0177')+' · '+event(l,'PD-SP-EVT-0178',select(l,'Separate covering email','Correo de remisión separado')))
    ]
    for a,c,d in statuses:b+='<article class="ca-card">'+title(a,3)+p(c)+d+'</article>'
    b+='</div>'+title(select(l,'Six requests, six legally distinct decisions','Seis peticiones, seis decisiones jurídicamente distintas'),3)
    requests=[
        (['ECR'],('Link, route and reconcile','Associate the new material with the existing record; identify the competent functional team and a secure channel for source files. Keep supervisory reporting, investor complaints and SAIP distinct.'),('Vincular, repartir y conciliar','Incorporar el material al registro existente; identificar unidad funcional competente y canal seguro. Mantener separadas comunicación supervisora, reclamación inversora y SAIP.')),
        (['ECR','IIC'],('Preserve and obtain defined records','Preserve relevant CNMV-held versions and correspondence. Assess targeted requirements for investment approvals, title/conditions, source-and-use, conflicts, Series F/G and subsequent transfers under the applicable information/inspection powers.'),('Preservar y obtener documentos determinados','Conservar versiones y comunicaciones relevantes en poder de CNMV. Valorar requerimientos delimitados sobre aprobación, titularidad/condiciones, origen y destino de fondos, conflictos, Series F/G y transmisiones posteriores.')),
        (['ECR','IIC'],('Assess proportionate interim protection','Compare available supervisory requirements, intervention or replacement under art.102/arts.72–75, and judicial protection requested under art.86.1(d). Identify the entity, evidence, risk, legal threshold and less disruptive effective alternatives.'),('Valorar protección provisional proporcionada','Comparar requerimientos supervisores, intervención o sustitución de art.102/arts.72–75 y aseguramiento judicial solicitado al amparo de art.86.1(d). Identificar entidad, prueba, riesgo, umbral y alternativas eficaces menos lesivas.')),
        (['LECRIM','EOMF','LMV','EPPO'],('Refer and cooperate where the legal trigger is met','Place concrete criminal indications and a specified digital-preservation schedule before the competent prosecution/judicial-police authority. LECrim 588 octies is their power, not CNMV’s. EPPO requires a qualifying EU-financial-interest nexus.'),('Trasladar y cooperar cuando concurra el presupuesto legal','Poner indicios penales concretos y una ficha de preservación digital ante Fiscalía/Policía Judicial competente. El art.588 octies es potestad de estas, no de CNMV. Fiscalía Europea exige nexo cualificado con intereses financieros de la UE.')),
        (['CP','ORGA','IIC','LGS'],('Protect innocent stakeholders and operating value','Design any justified measure around employees, guests, lawful suppliers, creditors and good-faith investors. Test liquidity, contracts, grant advances, costs and review rights; do not transfer business control to the complainant.'),('Proteger a terceros inocentes y valor operativo','Diseñar cualquier medida justificada considerando empleados, huéspedes, proveedores lícitos, acreedores e inversores de buena fe. Evaluar liquidez, contratos, anticipos, costes y recursos; no transferir control al denunciante.')),
        (['IIC','LMV','SAIP'],('Apply lawful publicity and provide the available response','If intervention/replacement is adopted, apply BOE publication and Registro Mercantil registration under art.73.3. Assess protective disclosure within art.243’s actual scope, and communicate the procedural information legally available without exposing reserved investigations.'),('Aplicar publicidad legal y dar la respuesta procedente','Si se acuerda intervención/sustitución, cumplir publicación BOE e inscripción mercantil del art.73.3. Valorar información protectora dentro del ámbito real del art.243 y comunicar lo procedimental legalmente accesible sin revelar investigación reservada.'))
    ]
    b+='<ol class="ca-requests">'
    for laws,en,es in requests:
        a,c=en if l=='en' else es
        b+='<li>'+title(a,4)+p(c)+src(laws)+'</li>'
    b+='</ol>'
    b+=p(select(l,'This asks CNMV to assess action ex officio on supported information; it does not assert that Gil satisfies the specific shareholder/entity petition conditions of art.73.1. Any preferred rapid response interval is an operational request, not an invented statutory deadline.','Se pide valorar actuación de oficio a partir de información sustentada; no se afirma que Gil reúna las condiciones societarias del art.73.1. Cualquier plazo rápido propuesto sería operativo, no un plazo legal inventado.'))
    b+='<div class="ca-note">'+select(l,'The evidence chain is unitary; coercive powers and liabilities are not. Each authority must act within its own competence, thresholds and safeguards. A confidentiality limit is not proof of wrongdoing, but neither prevents every lawfully authorised inter-agency exchange.','La cadena probatoria es unitaria; las potestades coercitivas y responsabilidades no lo son. Cada órgano actúa con su competencia, presupuestos y garantías. La reserva no prueba irregularidad, pero tampoco impide toda comunicación interinstitucional legalmente autorizada.')+'</div>'
    return '<section class="ca-module" id="'+aid+'" data-cnmv-interim-control="'+CONTROL+'">'+b+'</section>'

def publicity(l):
    cards=[
      (select(l,'Our public request','Nuestra solicitud pública'),select(l,'The requested action and source map are public here. That does not prove delivery to CNMV, personal knowledge, an admitted proceeding or an official protective order. The formal email/registry stage must be recorded separately when it occurs.','Aquí son públicos la petición y el mapa documental. No acreditan entrega a CNMV, conocimiento personal, expediente admitido ni medida oficial. La fase de correo/registro debe documentarse separadamente cuando se produzca.'),[]),
      (select(l,'Official intervention: BOE + Mercantile Registry','Intervención oficial: BOE + Registro Mercantil'),select(l,'Article 73.3 of Ley35/2003, through Ley22/2014 art.102, requires publication and registration of an adopted intervention/replacement decision. Article74 entails broad approval consequences after BOE publication: this is not simply an informal monitor. The statutory factual and procedural conditions remain essential.','El art.73.3 Ley35/2003, por remisión del art.102 Ley22/2014, exige publicar e inscribir la intervención/sustitución acordada. El art.74 comporta amplios efectos de aprobación tras el BOE: no es simple seguimiento informal. Siguen siendo esenciales sus presupuestos y procedimiento.'),['ECR','IIC']),
      (select(l,'Protective market information—not investigation secrets','Información protectora de mercado, no secretos investigadores'),select(l,'Assess art.243 Ley6/2023 only after identifying the relevant issuer/entity, securities, trading and material-information nexus. Article233 protects reserved information while permitting specified lawful exchanges. SCR registration does not itself establish a listed issuer or a duty to reveal an ongoing investigation.','Valorar art.243 Ley6/2023 tras identificar emisor/entidad, valores, negociación y relevancia. El art.233 protege información reservada y permite comunicaciones legales tasadas. Inscripción SCR no acredita emisor cotizado ni deber de revelar una investigación en curso.'),['LMV'])
    ]
    out='<div class="ca-grid ca-three">'
    for a,b,c in cards:out+='<article class="ca-card">'+title(a,3)+p(b)+src(c)+'</article>'
    return out+'</div>'+p(select(l,'The request is for the official decision, statutory notices and any lawful protective communication—not public bank records, confidential identities, preservation tactics or material whose disclosure would compromise an investigation or third-party rights.','Se solicitan decisión oficial, anuncios legales e información protectora lícita, no cuentas bancarias, identidades confidenciales, tácticas de preservación o datos cuya difusión comprometa investigación o derechos de terceros.'))

def footer(l):
    text=(ROOT/'AUTHOR_REPORTING_PERSON_ALERTADOR_FOOTER_CONTROL_22AUG2026.md').read_text()
    part=text.split('## Exact '+('English' if l=='en' else 'Spanish')+' footer text',1)[1].split('### '+('Official links' if l=='en' else 'Enlaces oficiales'),1)[0]
    paragraphs=[]; active=[]
    for line in part.splitlines():
        if line.startswith('> '): active.append(line[2:])
        elif line.strip()=='>':
            if active: paragraphs.append(' '.join(active));active=[]
    if active:paragraphs.append(' '.join(active))
    assert len(paragraphs)==2, 'Required two-paragraph reporting-person footer'
    return '<footer class="ca-footer">'+title(select(l,'Author’s reporting-person position','Posición del autor como persona informante'),2)+''.join(p(x) for x in paragraphs)+src(['INFORMANT'])+'</footer>'

def smallcards(items,l,klass=''):
    return '<div class="ca-grid '+klass+'">'+''.join('<article class="ca-card">'+title(x[l][0],3)+p(x[l][1])+src(x.get('law',[]))+'</article>' for x in items)+'</div>'

PAIRS=[
 ('en/index.html','es/index.html'),
 ('en/ric-private-equity-sun-park/index.html','es/ric-private-equity-sun-park/index.html'),
 ('en/orion-rental-socimi/index.html','es/orion-rental-socimi/index.html'),
 ('en/institutional-records/index.html','es/registros-institucionales/index.html'),
 ('en/asset-recovery-intervention-confiscation/index.html','es/recuperacion-activos-intervencion-decomiso/index.html'),
 ('en/acosta-matos-perimeter/index.html','es/acosta-matos-perimetro/index.html'),
 ('en/public-authority-unitary-case-reconstruction/index.html','es/reconstruccion-unitaria-autoridades-publicas/index.html'),
 ('en/fti-touristik-meeting-point-insolvency-preinsolvency-bluesea/index.html','es/fti-touristik-meeting-point-insolvencia-preconcurso-bluesea/index.html')
]

def document(l):
    other='es' if l=='en' else 'en'
    page_title=select(l,'Authorities, interim protection and criminal asset recovery','Autoridades, protección provisional y recuperación penal de activos')
    desc=select(l,'A criminal-first guide to preservation, proportionate intervention, lawful publicity and cross-border recovery: Spanish, Canary, EU, German and UK routes.','Guía penal prioritaria de preservación, intervención proporcionada, publicidad legal y recuperación transfronteriza: España, Canarias, UE, Alemania y Reino Unido.')
    out='<!doctype html>\n<html lang="'+l+'"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
    out+='<title>'+esc(page_title)+' | Por Derecho</title><meta name="description" content="'+esc(desc)+'">'
    out+='<link rel="canonical" href="'+HOST+ROUTES[l].removesuffix('index.html')+'">'
    for lang in ['es','en']:
        out+='<link rel="alternate" hreflang="'+lang+'" href="'+HOST+ROUTES[lang].removesuffix('index.html')+'">'
    out+='<link rel="alternate" hreflang="x-default" href="'+HOST+ROUTES['es'].removesuffix('index.html')+'">'
    out+='<link rel="stylesheet" href="../../assets/styles.css"><link rel="stylesheet" href="../../'+CSS+'"><script src="../../assets/site.js" defer></script><script src="../../'+JS+'" defer></script></head>\n<body class="dossier-page ca-page">'
    out+='<a class="skip-link" href="#content">'+select(l,'Skip to content','Saltar al contenido')+'</a><header class="site-header"><div class="shell header-inner">'+link(l+'/', 'Por Derecho · Project Sun Rock')+'<nav class="main-nav" aria-label="'+select(l,'Authority guide','Guía de autoridades')+'">'+link(CNMV[l],'CNMV / RICPE')+' '+link(INST[l],select(l,'Institutional record','Registro institucional'))+' '+link(ROUTES[other],other.upper())+'</nav></div></header>'
    out+='<main id="content" class="ca-shell" data-cnmv-interim-control="'+CONTROL+'">'
    out+='<section class="ca-hero"><div class="ca-kicker">'+select(l,'CRIMINAL FIRST · CAREFUL INTERVENTION · PUBLIC ACCOUNTABILITY','PENAL PRIMERO · INTERVENCIÓN CUIDADOSA · RENDICIÓN DE CUENTAS')+'</div><h1>'+esc(page_title)+'</h1>'+p(desc)
    out+='<p class="ca-principle">'+select(l,'Protect the evidence. Trace the value. Keep lawful activity viable.','Proteger la prueba. Seguir el valor. Preservar la actividad lícita.')+'</p><div class="ca-metrics"><div><strong>35</strong><span>'+select(l,'distinct mechanisms','mecanismos distintos')+'</span></div><div><strong>78</strong><span>'+select(l,'authority / unit / custodian entries','entradas de órganos / unidades / custodios')+'</span></div><div><strong>8</strong><span>'+select(l,'separate rights routes','vías de derechos separadas')+'</span></div><div><strong>15</strong><span>'+select(l,'screening-only entries','entradas de examen preliminar')+'</span></div></div></section>'
    labels={'criminal-first':('Purpose','Finalidad'),'cnmv-action':('CNMV action','Actuación CNMV'),'tools':('35 tools','35 instrumentos'),'authorities':('Authorities','Autoridades'),'cross-border':('Cross-border','Transfronterizo'),'case':('Sun Park','Sun Park'),'preserve':('Preservation','Preservación'),'continuity':('Continuity','Continuidad'),'rights':('Rights','Derechos'),'publicity':('Publicity','Publicidad'),'sources':('Sources','Fuentes')}
    out+='<nav class="ca-toc" aria-label="'+select(l,'On this page','En esta página')+'">'+''.join('<a href="#'+i+'">'+x[0 if l=='en' else 1]+'</a>' for i,x in labels.items())+'</nav>'
    b=p(select(l,'A criminal investigation asks whether particular acts constitute an offence and whether evidence or recoverable value must be secured. It is not merely a civil claim for payment. Criminal confiscation, criminal-case civil liability, insolvency estate recovery, tax recovery and grant recovery can intersect without becoming the same remedy.','La investigación penal examina si actos concretos constituyen delito y si deben asegurarse prueba o valor recuperable. No es una mera demanda civil de pago. Decomiso, responsabilidad civil derivada del delito, recuperación concursal, tributaria y de subvenciones pueden conectarse sin ser el mismo remedio.'))+src(['CP','LECRIM'])
    b+=p(select(l,'The operational question is: which defined record or asset, held by whom, can which authority preserve or investigate, under which threshold, with which safeguards, and what lawful decision or response follows? Powers are not all mandatory duties; a duty to assess or refer is not a guarantee that every requested measure will be granted.','La pregunta operativa es: qué documento o activo determinado, en poder de quién, puede preservar o investigar qué autoridad, con qué umbral y garantías, y qué decisión o respuesta procede. No toda facultad es deber obligatorio; valorar o trasladar no garantiza acordar cada medida solicitada.'))+src(['EOMF','ECR','LPAC'])
    b+='<div class="ca-flow" aria-label="'+select(l,'Criminal recovery pathway','Secuencia de recuperación penal')+'">'+''.join('<span>'+x+'</span>' for x in select(l,['Identify','Trace','Preserve','Restrain','Manage','Decide','Recover / restore'],['Identificar','Localizar','Preservar','Asegurar','Gestionar','Resolver','Recuperar / restituir']))+'</div>'
    b+=p(select(l,'This is a functional guide with explicit open gates, not a directory of every office or a case-specific jurisdiction ruling. The 15 screening-only entries require further statutory and factual matching. Preserve adverse outcomes, limitation questions and innocent explanations.','Es una guía funcional con presupuestos abiertos, no directorio de toda oficina ni decisión de competencia en el caso. Las 15 entradas preliminares requieren correspondencia normativa y fáctica adicional. Conservar resultados adversos, prescripción y explicaciones inocentes.'))
    out+=sec('criminal-first',select(l,'From suspicion to a lawful protective decision','De la sospecha a una decisión protectora legal'),b)
    out+=action(l,True)
    b='<div class="ca-filter" data-ca-filter="tools"><label for="ca-tools-search">'+select(l,'Search a power, authority or legal article','Buscar facultad, autoridad o artículo')+'</label><input id="ca-tools-search" type="search" autocomplete="off"><output aria-live="polite"></output></div><div class="ca-grid" data-ca-items="tools">'
    for x in D['tools']:
        a,c,e=x[l]
        b+='<article class="ca-card ca-tool" id="tool-'+x['key']+'" data-ca-item><div class="ca-kicker">'+esc(x['key']+' · '+x['lane'])+'</div>'+title(a,3)+p(c)+'<p class="ca-limit"><strong>'+select(l,'Threshold / limit: ','Presupuesto / límite: ')+'</strong>'+esc(e)+'</p>'+src(x['law'])+'</article>'
    b+='</div>'
    out+=sec('tools',select(l,'The toolkit: who may do what, and on what conditions','Instrumentos: quién puede hacer qué y con qué condiciones'),b)
    b=p(select(l,'The list retains authorities, units, oversight bodies and private custodians as different roles. Group descriptions identify common functions; an individual office still needs a case-specific legal and territorial allocation.','La lista distingue autoridades, unidades, órganos de control y custodios privados. Cada descripción recoge funciones del grupo; la oficina concreta necesita atribución legal y territorial para el caso.'))
    b+='<div class="ca-filter" data-ca-filter="authorities"><label for="ca-authorities-search">'+select(l,'Find an authority or function','Localizar órgano o función')+'</label><input id="ca-authorities-search" type="search" autocomplete="off"><output aria-live="polite"></output></div><div data-ca-items="authorities">'
    statusnames={'core':('Core function reviewed','Función general examinada'),'allocation':('Exact allocation required','Requiere atribución concreta'),'screening':('SCREENING ONLY · mandate not established','SOLO EXAMEN PRELIMINAR · mandato no acreditado'),'custodian':('Evidence custodian · not a criminal decision-maker','Custodio probatorio · no órgano penal decisor')}
    for g in D['authority_groups']:
        b+='<article class="ca-authority-group" id="authority-group-'+g['key']+'"><h3>'+esc(g[l][0])+'</h3>'+p(g[l][1])+src(g['law'])+'<ul class="ca-authority-list">'
        for name,status in g['entries']:b+='<li data-ca-item data-status="'+status+'"><strong>'+esc(name)+'</strong><span>'+statusnames[status][0 if l=='en' else 1]+'</span></li>'
        b+='</ul></article>'
    b+='</div>'+p(select(l,'These navigation labels allocate no new canonical person or authority identity. The existing institutional and asset-recovery registers remain controlling; private custodians are not mislabelled public investigators.','Estas etiquetas de navegación no crean identidad canónica de persona u órgano. Siguen rigiendo los registros institucionales y de recuperación existentes; custodios privados no se presentan como investigadores públicos.'))
    out+=sec('authorities',select(l,'Authority map: 78 entries, not 78 identical powers','Mapa de órganos: 78 entradas, no 78 potestades iguales'),b)
    cb=[{'law':['EIO','FREEZE','DE'],'en':['Germany: evidence, estates and assets','The existing FTI/Meeting Point record identifies a planned Club Sei/Lava Verde connection, not proof that Sun Park caused the group insolvency. Keep FTI Touristik, BigXtra, Meeting Point International, MP Hotelmanagement Holding and Spanish Meeting Point debtors separate. Obtain executed contracts, costs, claims, impairments and records from the correct estate. COVID postponement remains contrary evidence to assumed operation.'],'es':['Alemania: prueba, masas y bienes','El registro FTI/Meeting Point recoge conexión proyectada Club Sei/Lava Verde, no prueba de que Sun Park causara la insolvencia del grupo. Separar FTI Touristik, BigXtra, Meeting Point International, MP Hotelmanagement Holding y deudores españoles. Obtener contratos ejecutados, costes, créditos, deterioros y registros de la masa correcta. El aplazamiento COVID contradice operación presumida.']},
        {'law':['UKMLA','CPS'],'en':['United Kingdom: Aweswell and specific records','The project identifies Aweswell Limited as the UK holding company/foreign investor, not a hotel located in Britain. Separate its direct rights and losses from those of Spanish companies. Identify any UK bank, contract, evidence or asset connection and the exact historical Youtravel counterparty. Use post-Brexit MLA/TCA routes, not a new EIO to the UK.'],'es':['Reino Unido: Aweswell y registros concretos','El proyecto identifica Aweswell Limited como matriz/inversor británico, no como hotel situado en Reino Unido. Separar derechos y daños propios de los de sociedades españolas. Identificar cuentas, contratos, pruebas o activos británicos y contraparte histórica exacta de Youtravel. Utilizar MLA/TCA posterior al Brexit, no nueva OEI al Reino Unido.']},
        {'law':['EPPO','EUFUNDS','LGS'],'en':['EU funds: prove the budget connection','RIC tax relief, national regional incentives, SEPI/FASEE and German WSF credit, and EU programme expenditure have different sources and rules. Identify beneficiary, instrument, programme, operation, payment and alleged offence before asserting EPPO competence. State-aid approval is not an EU disbursement.'],'es':['Fondos europeos: acreditar nexo presupuestario','RIC, incentivos regionales nacionales, crédito SEPI/FASEE y WSF alemán y gasto de programa UE tienen fuentes y reglas distintas. Identificar beneficiario, instrumento, programa, operación, pago y delito antes de atribuir competencia a Fiscalía Europea. Autorizar ayuda de Estado no es desembolsar presupuesto UE.']}]
    b=smallcards(cb,l,'ca-three')+'<p>'+link(PAIRS[-1][0 if l=='en' else 1],select(l,'FTI / Meeting Point source and contrary-record dossier','Dossier FTI / Meeting Point y prueba limitadora'))+' · '+link('en/about/',select(l,'Project identity / Aweswell','Identidad del proyecto / Aweswell (EN)'))+'</p>'
    b+=p(select(l,'Directive2024/1260 has a 23 November2026 transposition deadline. Complete Spanish transposition has not been established by this bounded review; do not treat every directive provision as an already available domestic coercive power.','La Directiva2024/1260 fija transposición para el 23 de noviembre de2026. Esta revisión delimitada no acredita transposición española completa; no convertir cada disposición en potestad coercitiva nacional ya disponible.'))+src(['DIRECTIVE'])
    out+=sec('cross-border',select(l,'Cross-border does not mean jurisdiction everywhere','Transfronterizo no significa competencia de todos'),b)
    b='<div class="ca-allegation"><strong>'+select(l,'ATTRIBUTED CRIMINAL ALLEGATION · Gil Marer','ALEGACIÓN PENAL ATRIBUIDA · Gil Marer')+'</strong>'+p(select(l,'Gil alleges an organised, coordinated and continuous criminal mechanism spanning Community authority and documents, debt/voting, proceedings inside and outside Concurso36/2012, disputed effective safeguards over LPB assets, title/credit transactions, RIC/RICPE funding and downstream businesses. He alleges that appropriated assets or income enabled investment in apparently separate assets, employment, financing and public incentives. This is his allegation, not an adjudicated finding against every associated entity or person.','Gil alega un mecanismo criminal organizado, coordinado y continuo que comprende autoridad y documentos comunitarios, deuda/voto, procedimientos dentro y fuera del Concurso36/2012, eficacia discutida de las salvaguardas sobre bienes LPB, titularidad/crédito, financiación RIC/RICPE y empresas posteriores. Alega que activos o ingresos apropiados permitieron invertir en bienes aparentemente separados, empleo, financiación e incentivos públicos. Es su alegación, no conclusión judicial contra cada entidad o persona relacionada.'))+'</div>'
    b+='<p>'+link(l+'/ric-private-equity-sun-park/',select(l,'RICPE evidence and competing explanations','Prueba RICPE y explicaciones alternativas'))+' · '+link(PAIRS[6][0 if l=='en' else 1],select(l,'Unitary public-authority reconstruction','Reconstrucción unitaria de autoridades'))+'</p>'
    stages=select(l,['Original right','Control / transfer','Financing / security','Works / operation','Income / distribution','Current holder / equivalent value'],['Derecho inicial','Control / transmisión','Financiación / garantía','Obras / explotación','Ingreso / distribución','Titular actual / equivalente'])
    b+='<div class="ca-flow">'+''.join('<span>'+x+'</span>' for x in stages)+'</div>'
    b+=p(select(l,'Every arrow is a question requiring evidence: asset identity, legal capacity, contract, bank movement, valuation, approval, recipient and date. Trace direct, transformed and equivalent value under the correct rule; association alone does not make all assets recoverable. Employment, investment or commercial success establishes neither culpability nor immunity.','Cada flecha exige prueba: identidad del bien, capacidad, contrato, movimiento bancario, valoración, aprobación, destinatario y fecha. Seguir valor directo, transformado o equivalente conforme a su regla; la asociación sola no hace recuperable todo patrimonio. Empleo, inversión o éxito comercial no acreditan culpabilidad ni inmunidad.'))+src(['CP'])
    b+='<div class="ca-grid ca-three"><article class="ca-card">'+title(select(l,'July2021 → later re-entry','Julio2021 → reentrada posterior'),3)+p(select(l,'The existing CNMV dossier records a conditional acquisition, an unsigned LOI and incomplete due diligence. The later operating outcome does not answer what changed, who approved it and what safeguards or contrary information were considered.','El dossier CNMV recoge adquisición condicionada, LOI sin firma y due diligence incompleta. La explotación posterior no responde qué cambió, quién lo aprobó ni qué salvaguardas o información contraria se consideraron.'))+link(CNMV[l],select(l,'Read the bounded documentary review','Leer revisión documental delimitada'))+'</article>'
    b+='<article class="ca-card">'+title(select(l,'Series F/G: do not normalise the difference','Series F/G: no normalizar la diferencia'),3)+p(select(l,'The dossier distinguishes €6,570,713.56 in the 20 September2023 prospectus from €6,573,703.10 in an accounts reconstruction. The €2,989.54 difference remains open. Neither amount is proof of criminal proceeds; obtain contract-to-bank-to-ledger reconciliation.','El dossier distingue 6.570.713,56€ del folleto de20 septiembre2023 y 6.573.703,10€ de una reconstrucción contable. La diferencia de2.989,54€ permanece abierta. Ningún importe prueba ganancias delictivas; conciliar contrato, banco y contabilidad.'))+link(CNMV[l],select(l,'Source-specific number control','Control de importes por fuente'))+'</article>'
    b+='<article class="ca-card">'+title(select(l,'HNT GC/836/P06: an award, not a payment finding','HNT GC/836/P06: concesión, no prueba de pago'),3)+'<dl class="ca-amounts"><dt>'+select(l,'Eligible investment','Inversión subvencionable')+'</dt><dd>€11,469,714</dd><dt>'+select(l,'Grant awarded','Subvención concedida')+'</dt><dd>€3,440,914.20</dd><dt>'+select(l,'Jobs to create','Empleos a crear')+'</dt><dd>60</dd></dl>'+p(select(l,'OrderHFP/521/2023. These conditions prove neither disbursement, actual jobs, compliance, fraud nor actual EU co-financing.','OrdenHFP/521/2023. Estas condiciones no prueban desembolso, empleo real, cumplimiento, fraude ni cofinanciación europea efectiva.'))+src(['HNT'])+'</article></div>'
    b+='<div class="ca-note"><strong>'+select(l,'Contrary and adverse material remains part of the case.','La prueba contraria y adversa forma parte del caso.')+'</strong>'+p(select(l,'Retain the 2018 provisional criminal dismissal and appeal outcome within their exact scope; disclosed conflicts, abstentions and control opinions; COVID postponement; lawful credit/title explanations; and the missing complete bank-to-proceeds bridge. Reopening, limitation and same-fact/party questions require the actual orders and qualified case-specific review.','Mantener archivo provisional penal y resultado de apelación de2018 en su ámbito exacto; conflictos, abstenciones y opiniones de control revelados; aplazamiento COVID; explicaciones lícitas de crédito/titularidad y falta de puente bancario íntegro hasta ganancias. Reapertura, prescripción e identidad de hechos/partes requieren resoluciones y examen cualificado del caso.'))+'</div>'
    b+='<p>'+link(l+'/ric-private-equity-sun-park/',select(l,'Case source record','Fuentes del caso'))+' · '+link(INST[l],select(l,'Existing communication register','Registro de comunicaciones existente'))+'</p>'
    out+=sec('case',select(l,'Apply the tools to Sun Park—without presuming the result','Aplicar los instrumentos a Sun Park sin presumir resultado'),b)
    rows=select(l,[['CNMV record','Submitted versions, correspondence and internal custody','Preserve under the applicable records/supervisory regime; retain dated originals'],['Regulated investment','Approvals, conditions, Series F/G, conflicts, valuations','Targeted CNMV information/inspection requirements; proper court route where needed'],['Money and rights','Loan contracts, bank movements, charges, distributions','Authorised financial investigation; source-to-use and recipient reconciliation'],['Specified digital evidence','Relevant stored records, version history and logs','Fiscalía/Judicial Police assess art.588 octies; judicial authorisation for disclosure'],['Hotel continuity','Payroll totals, guest obligations, cash needs and essential contracts','Scope-limited lawful production; minimise personal information'],['Cross-border / public funds','Exact debtor, contract, programme and payment record','EIO, MLA/TCA, programme-control or EPPO route only within its conditions']],
    [['Registro CNMV','Versiones aportadas, comunicaciones y custodia interna','Conservación conforme al régimen documental/supervisor; mantener originales fechados'],['Inversión regulada','Aprobaciones, condiciones, Series F/G, conflictos, valoraciones','Requerimientos CNMV delimitados; vía judicial cuando corresponda'],['Dinero y derechos','Contratos, movimientos, cargas, distribuciones','Investigación financiera autorizada; conciliar origen, destino y destinatario'],['Prueba digital concreta','Datos almacenados relevantes, versiones y trazas','Fiscalía/Policía Judicial valoran art.588 octies; autorización judicial para cesión'],['Continuidad hotelera','Totales de nóminas, huéspedes, caja y contratos esenciales','Producción legal delimitada; minimizar información personal'],['Transfronterizo / ayudas','Deudor, contrato, programa y pago exactos','OEI, MLA/TCA, control de programa o Fiscalía Europea con sus presupuestos']])
    b=p(select(l,'For each item identify custodian, system/document, dates, transaction, preservation risk, lawful route and responsible authority. This is a public category schedule, not a disclosure of confidential targets or a served preservation notice. No actual deletion, imminent disposal date or unidentified system is asserted.','Identificar por elemento custodio, sistema/documento, fechas, operación, riesgo, vía legal y órgano responsable. Es una ficha pública de categorías, no revelación de objetivos confidenciales ni requerimiento notificado. No se afirma borrado efectivo, fecha inminente de eliminación ni sistema no identificado.'))
    b+='<div class="ca-table-wrap" tabindex="0" role="region" aria-label="'+select(l,'Preservation schedule','Ficha de preservación')+'"><table><thead><tr>'+''.join('<th scope="col">'+x+'</th>' for x in select(l,['Object','Record sought','Decision / route'],['Objeto','Documento buscado','Decisión / cauce']))+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+esc(c)+'</td>' for c in row)+'</tr>' for row in rows)+'</tbody></table></div>'+src(['LECRIM','ECR','IIC','EIO','UKMLA'])
    b+=p(select(l,'Native records, available metadata and version history should be preserved proportionately, including exculpatory material. A hash identifies a file, not its truth or authorship. Privilege, protected identities and irrelevant guest/employee data remain protected.','Conservar proporcionalmente nativos, metadatos disponibles y versiones, incluida prueba exculpatoria. Una huella identifica un archivo, no su veracidad o autoría. Mantener protegidos secreto profesional, identidades y datos irrelevantes de huéspedes/empleados.'))
    out+=sec('preserve',select(l,'Preservation now: specified records, not an indiscriminate search','Preservar ahora: documentos concretos, no búsqueda indiscriminada'),b)
    b='<p class="ca-principle">'+select(l,'Economic importance is a reason to design intervention carefully—not a reason to abandon investigation.','La importancia económica exige diseñar cuidadosamente la intervención, no abandonar la investigación.')+'</p>'+p(select(l,'The terms below are proposals for legal review, not an order or a promise of rescue, job guarantees or additional public funds. A proportionate solution must not manufacture an avoidable collapse.','Las condiciones siguientes son propuestas para examen jurídico, no resolución ni promesa de rescate, empleo garantizado o fondos adicionales. La respuesta proporcionada no debe provocar un colapso evitable.'))+smallcards(D['continuity'],l)+src(['CP','LECRIM','ORGA','IIC','LGT','LGS','CPS'])
    out+=sec('continuity',select(l,'Preserve productive value and innocent interests','Preservar valor productivo e intereses inocentes'),b)
    out+=sec('rights',select(l,'Eight separate legal capacities and channels','Ocho capacidades y canales jurídicos separados'),smallcards(D['rights'],l))
    b=publicity(l)
    b+=title(select(l,'A handling record, not a presumption of criminal omission','Un registro de tramitación, no presunción de omisión delictiva'),3)
    b+='<div class="ca-flow">'+''.join('<span>'+x+'</span>' for x in select(l,['Sent','Received','Registered','Routed','Assessed','Decided','Notified','Reviewed'],['Enviado','Recibido','Registrado','Repartido','Examinado','Resuelto','Notificado','Revisado']))+'</div>'+p(select(l,'Each step needs its own evidence. Article408 CP requires intentional failure to promote prosecution in breach of a specific duty. A lawful archive, a disclosure limit or disagreement is not enough. The project disputes some institutional handling, including Fiscalía; this does not erase the actual competences or the need for actor-specific proof.','Cada paso exige prueba propia. El art.408 CP requiere omisión intencional de promover persecución incumpliendo deber específico. Archivo lícito, límite de información o discrepancia no bastan. El proyecto discute actuaciones institucionales, incluidas de Fiscalía; ello no elimina competencias reales ni necesidad de prueba individualizada.'))+src(['CP','EOMF','LMV'])
    b+='<p>'+event(l,'PD-SP-EVT-0171','20 Aug · PD-SP-EVT-0171')+' · '+event(l,'PD-SP-EVT-0175','27 Aug · PD-SP-EVT-0175')+' · '+event(l,'PD-SP-EVT-0177','4 Sep · PD-SP-EVT-0177')+' · '+link(INST[l],select(l,'Full canonical register','Registro canónico completo'))+'</p>'
    b+=p(select(l,'The 20 August native submission/annex reconciliation and the relationship between the separate 24 August REG-AGE event PD-SP-EVT-0152 and 25 August CNMV incoming reference remain source-controlled questions in the preceding release. This page does not close those gaps by inference.','La conciliación del nativo/anexos del20 agosto y la relación entre el evento REG-AGE separado del24 agosto PD-SP-EVT-0152 y la entrada CNMV del25 agosto siguen siendo cuestiones documentales en la entrega precedente. Esta página no cierra esas lagunas por inferencia.'))
    out+=sec('publicity',select(l,'What we ask to be public—and what must remain protected','Qué pedimos hacer público y qué debe quedar protegido'),b)
    b=p(select(l,'The closest verified match to the earlier “July25” reference is the OECD report of28 July2025 on confiscation in Kazakhstan. Together with its2025 tax-crime investigation manual, it supports comparative analysis of tracing and recovery. This identifies guidance, not Spanish statutory powers and not a conclusion about this case. The intended source identification remains an inference.','La coincidencia verificada más próxima a la referencia “July25” es el informe OCDE de28 julio2025 sobre decomiso en Kazajistán. Junto con su manual de investigación tributaria de2025, sirve para análisis comparado de localización y recuperación. Es orientación, no potestad española ni conclusión del caso. La identificación de la referencia pretendida sigue siendo inferencia.'))+src(['OECD','OECDMANUAL'])
    out+=sec('comparative',select(l,'OECD: comparative guidance, not a Spanish order','OCDE: orientación comparada, no mandato español'),b)
    b=p(select(l,'Targeted research reviewed5 September2026. Use the law in force for each act and procedure. The source register and scoped boundaries are not a certificate that all historic files, every authority mandate or complete Spanish transposition have been audited. The original canonical sources and known gaps remain controlling.','Investigación delimitada revisada5 septiembre2026. Aplicar normativa vigente a cada acto y procedimiento. Este índice no certifica auditoría de todo archivo histórico, mandato de cada órgano ni transposición española completa. Rigen fuentes canónicas y lagunas conocidas.'))
    b+='<ol class="ca-source-list">'+''.join('<li id="legal-source-'+k+'"><a href="'+esc(v[1])+'" rel="external noopener">'+esc(v[0])+'</a></li>' for k,v in S.items())+'</ol>'
    b+='<p>'+link(DATA,select(l,'Public research read model (JSON)','Modelo público de investigación (JSON)'))+' · '+link('ASSET_RECOVERY_AUTHORITY_MATRIX_21AUG2026.json',select(l,'Existing authority matrix and dated record','Matriz existente y registro fechado'))+' · '+link('assets/data/institutional-communications-register-v1.json',select(l,'Canonical communications register','Registro canónico de comunicaciones'))+'</p>'
    out+=sec('sources',select(l,'Official legal sources and source boundaries','Fuentes legales oficiales y límites documentales'),b)
    out+=footer(l)+'</main></body></html>\n'
    return out

CSS_TEXT='''/* Scope-isolated CNMV research and action components. */
.ca-shell{max-width:1180px;margin:auto;padding:0 22px 3rem;color:#152d35}.ca-page{background:#f5f3ed}.ca-page .site-header{background:#fff}.ca-module,.ca-section{max-width:1136px;margin:2rem auto;padding:clamp(1.15rem,3vw,2.25rem);background:#fff;border:1px solid #cdd9d9;border-radius:16px;box-sizing:border-box}.ca-module{border-top:7px solid #ba8a36}.ca-section h2,.ca-module h2{font-size:clamp(1.55rem,3vw,2.35rem);line-height:1.17;margin:.55rem 0 1.15rem}.ca-module p,.ca-section p,.ca-card p{line-height:1.62}.ca-hero{background:#102b35;color:#f9f7ef;border-radius:0 0 24px 24px;padding:clamp(2rem,5vw,4rem);margin-bottom:1.5rem}.ca-hero h1{font-size:clamp(2.05rem,5vw,4rem);line-height:1.04;max-width:23ch;color:inherit}.ca-hero p{font-size:1.1rem;line-height:1.6;max-width:75ch}.ca-kicker{font-size:.74rem;line-height:1.5;font-weight:800;letter-spacing:.055em;text-transform:uppercase}.ca-principle{font-size:clamp(1.15rem,2.1vw,1.65rem);font-weight:800;line-height:1.45;border-left:5px solid #b98730;padding-left:1rem}.ca-metrics{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:1rem;margin-top:2rem}.ca-metrics div{border-top:1px solid #66838d;padding-top:.65rem}.ca-metrics strong{display:block;font-size:2rem}.ca-metrics span{display:block;font-size:.85rem;margin-top:.3rem}.ca-toc,.ca-links{display:flex;flex-wrap:wrap;gap:.65rem;padding:.6rem 0}.ca-toc a,.ca-jump a,.ca-links a{display:inline-block;border:1px solid #afc3c4;padding:.55rem .8rem;border-radius:8px;background:#edf3f1;color:#163f49;font-weight:750}.ca-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1rem;margin:1.15rem 0}.ca-three{grid-template-columns:repeat(3,minmax(0,1fr))}.ca-card{padding:1.1rem;border:1px solid #cedad8;border-top:4px solid #4a786b;border-radius:12px;background:#fbfcfa;min-width:0}.ca-card h3{font-size:1.15rem;line-height:1.35;margin:.2rem 0 .6rem}.ca-card p{font-size:.94rem}.ca-card .ca-limit{background:#f2eee3;border-left:3px solid #a78037;padding:.7rem}.ca-sources{font-size:.77rem!important;overflow-wrap:anywhere}.ca-banner,.ca-note{border-left:5px solid #a67a2d;padding:1rem;background:#f5efdf;margin:1rem 0;line-height:1.6}.ca-note{background:#edf2f1;border-color:#436d72}.ca-allegation{background:#f6ede8;border-left:5px solid #934c38;padding:1rem}.ca-requests{padding-left:1.4rem}.ca-requests li{padding:.7rem .3rem;border-bottom:1px solid #d6dfdc}.ca-requests h4{font-size:1.08rem;margin:.2rem 0}.ca-flow{display:flex;flex-wrap:wrap;gap:.55rem;margin:1.2rem 0}.ca-flow span{padding:.65rem .85rem;background:#173d47;color:#fff;border-radius:8px;flex:1 1 110px;text-align:center;font-weight:750;font-size:.88rem;line-height:1.35}.ca-flow span:not(:last-child)::after{content:' →';color:#e5c27d}.ca-filter{padding:1rem;border:1px solid #b4c8c6;border-radius:9px;background:#edf3f0}.ca-filter label{display:block;font-weight:800}.ca-filter input{display:block;width:100%;max-width:620px;border:2px solid #5c7c80;border-radius:6px;padding:.75rem;margin:.5rem 0;background:white;color:#142d37;font-size:1rem;box-sizing:border-box}.ca-filter output{display:block;font-size:.86rem;min-height:1.35em}.ca-authority-group{padding:.9rem 0 1.3rem;border-bottom:1px solid #b9ccca}.ca-authority-list{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.6rem}.ca-authority-list li{padding:.8rem;border:1px solid #c7d3d2;border-radius:8px;min-width:0}.ca-authority-list span{display:block;font-size:.79rem;margin-top:.4rem}.ca-authority-list [data-status=screening]{border-left:5px solid #a46a37;background:#faf1e7}.ca-authority-list [data-status=custodian]{border-left:5px solid #657685}.ca-table-wrap{overflow:auto;border:1px solid #ccd8d5;border-radius:8px;margin:1rem 0}.ca-table-wrap table{border-collapse:collapse;width:100%;min-width:650px}.ca-table-wrap th,.ca-table-wrap td{padding:.8rem;vertical-align:top;text-align:left;border-bottom:1px solid #d4dfdb;line-height:1.5}.ca-table-wrap th{background:#183d46;color:#fff}.ca-amounts{margin:.7rem 0}.ca-amounts dt{font-size:.81rem;margin-top:.6rem}.ca-amounts dd{font-size:1.2rem;font-weight:800;margin:0}.ca-source-list li{margin:.65rem 0;overflow-wrap:anywhere}.ca-footer{padding:2rem 1.2rem;border-top:2px solid #adc1bf;font-size:.86rem;line-height:1.6}.ca-footer h2{font-size:1.1rem}.ca-jump{max-width:1136px;margin:.8rem auto;padding:.6rem 1rem;display:flex;flex-wrap:wrap;gap:.7rem;align-items:center;box-sizing:border-box}.ca-page a,.ca-module a,.ca-section a{overflow-wrap:anywhere}.ca-page :focus-visible,.ca-module :focus-visible{outline:3px solid #ac752c;outline-offset:3px}.ca-page [hidden],.ca-module [hidden]{display:none!important}@media(max-width:850px){.ca-three{grid-template-columns:1fr}.ca-metrics{grid-template-columns:1fr 1fr}}@media(max-width:600px){.ca-grid,.ca-authority-list{grid-template-columns:1fr}.ca-shell{padding:0 12px 2rem}.ca-module{margin:1rem 10px}.ca-section{padding:1rem}.ca-hero{padding:1.5rem}.ca-toc{gap:.35rem}.ca-toc a{font-size:.87rem}.ca-metrics{gap:.8rem}}@media print{.site-header,.ca-toc,.ca-filter,.ca-jump{display:none!important}.ca-page{background:white}.ca-shell{max-width:none;padding:0}.ca-section,.ca-module,.ca-card{box-shadow:none;break-inside:avoid}.ca-hero{background:white;color:black;border:1px solid #aaa}.ca-grid,.ca-three,.ca-authority-list{display:block}.ca-card,.ca-authority-list li{margin:.6rem 0}.ca-page [hidden]{display:block!important}.ca-table-wrap{overflow:visible}.ca-table-wrap table{min-width:0}}
'''
JS_TEXT='''/* Progressive enhancement only: all substantive records remain in static HTML. */
(()=>{'use strict';const language=document.documentElement.lang;const norm=s=>s.normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').toLowerCase();document.querySelectorAll('[data-ca-filter]').forEach(box=>{const name=box.dataset.caFilter;const root=document.querySelector('[data-ca-items="'+name+'"]');if(!root)return;const input=box.querySelector('input'),output=box.querySelector('output');const items=[...root.querySelectorAll('[data-ca-item]')];const update=()=>{const q=norm(input.value.trim());let visible=0;items.forEach(item=>{item.hidden=!!q&&!norm(item.textContent).includes(q);if(!item.hidden)visible++});output.textContent=visible+' / '+items.length+' '+(language==='es'?'entradas visibles':'entries visible');root.querySelectorAll('.ca-authority-group').forEach(group=>{group.hidden=![...group.querySelectorAll('[data-ca-item]')].some(x=>!x.hidden)})};input.addEventListener('input',update);update()})})();
'''

class Parser(HTMLParser):
    def __init__(self,text):
        super().__init__(convert_charrefs=True);self.ids=[];self.links=[];self.feed(text)
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if 'id' in d:self.ids.append(d['id'])
        for a in ['href','src']:
            if a in d:self.links.append(d[a])

def prepared():
    out={CSS:CSS_TEXT,JS:JS_TEXT}
    for l in ['en','es']:out[ROUTES[l]]=document(l)
    touched=[]
    for l in ['en','es']:
        path=CNMV[l];base=original(path);aid=select(l,'interim-measures','medidas-provisionales')
        block=START+action(l)+END
        match=re.search(r'<section class="cnmv-hero".*?</section>',base,re.S)
        if not match:raise RuntimeError('CNMV hero insertion point absent: '+path)
        new=base[:match.end()]+block+base[match.end():]
        head=HSTART+'<link rel="stylesheet" href="../../'+CSS+'">'+HEND
        new=new.replace('</head>',head+'</head>',1)
        jump=JSTART+'<aside class="ca-jump">'+link(path+'#'+aid,select(l,'NEW · Interim measures and lawful publicity','NUEVO · Medidas provisionales y publicidad legal'))+'</aside>'+JEND
        new=new.replace('<main id="content">','<main id="content">'+jump,1)
        out[path]=new;touched.append(path)
    for pair in PAIRS:
        for l,path in zip(['en','es'],pair):
            base=original(path)
            if '</main>' not in base:raise RuntimeError('No main closing tag in '+path)
            fragment=START+'<aside class="ca-jump" aria-label="'+select(l,'CNMV and criminal recovery action','Actuación CNMV y recuperación penal')+'"><strong>'+select(l,'Preservation · interim measures · lawful publicity','Preservación · medidas provisionales · publicidad legal')+'</strong>'+link(CNMV[l]+'#'+select(l,'interim-measures','medidas-provisionales'),'CNMV')+' '+link(ROUTES[l],select(l,'Authorities and recovery toolkit','Autoridades e instrumentos de recuperación'))+'</aside>'+END
            head=HSTART+'<link rel="stylesheet" href="'+PREFIX+CSS+'">'+HEND
            out[path]=base.replace('</main>',fragment+'</main>',1).replace('</head>',head+'</head>',1);touched.append(path)
    matrix=json.loads(original('ASSET_RECOVERY_AUTHORITY_MATRIX_21AUG2026.json'))
    matrix['public_research_extension_20260905']={'control_id':CONTROL,'read_model':DATA,'routes':ROUTES,'new_email_sent':False,'new_registry_filing':False,'official_intervention_order_identified':False,'historical_status_rule':'Original 21-August recent_status is retained as historical, not certified current. The new page links separate canonical events and preserves source gaps.'}
    out['ASSET_RECOVERY_AUTHORITY_MATRIX_21AUG2026.json']=jdump(matrix)
    manifest={'schema':'por-derecho.publication-manifest.v1','publication_id':CONTROL,'owner':'Por Derecho scoped CNMV integration','control_date':'2026-09-05','current_state':'PREPARED','title':'CNMV interim measures, lawful publicity and criminal asset-recovery guide','source_base_sha':BASE,'head_branch':'integration/cnmv-interim-measures-20260905','expected_routes':{l:[ROUTES[l],CNMV[l]] for l in ['en','es']},'expected_source_files':[DATA,CSS,JS,'scripts/build_cnmv_interim_measures_20260905.py'],'authorization':{'repository_and_website_publication':True,'external_contact_or_delivery':False,'email_action':'NOT_SENT','filing_or_portal_action':'NOT_FILED'},'lifecycle_note':'PREPARED is the reproducible pre-merge source state. Exact merge, Pages and live verification are independently recorded in Control Tower #1428; this manifest is not a pre-emptive deployment certificate.'}
    out['publication-manifests/cnmv-interim-measures-20260905.json']=jdump(manifest)
    audit={'control_id':CONTROL,'source_base_sha':BASE,'read_model':DATA,'read_model_sha256':digest((ROOT/DATA).read_bytes()),'tools':len(D['tools']),'authority_entries':sum(len(x['entries']) for x in D['authority_groups']),'screening_only_entries':sum(s=='screening' for g in D['authority_groups'] for _,s in g['entries']),'rights':len(D['rights']),'continuity_terms':len(D['continuity']),'official_source_entries':len(S),'canonical_register_unchanged':True,'canonical_register_sha256':digest((ROOT/D['canonical_register']).read_bytes()),'standalone_pages':list(ROUTES.values()),'managed_existing_pages':touched,'owned_files':[DATA,CSS,JS,*ROUTES.values(),'ASSET_RECOVERY_AUTHORITY_MATRIX_21AUG2026.json'],'outputs':sorted(out),'output_sha256':{k:digest(v.encode()) for k,v in out.items()},'limits':['No universal historical completeness or case-jurisdiction claim','15 screening-only authority entries retained','No raw private source, unsent email, signature, filing or authority contact published','Original 333-event communications register and preceding Orion notice blocks unchanged','Standalone original preparation bundle is source material, not represented as uploaded verbatim','No new communication or official measure represented as completed']}
    out[AUDIT]=jdump(audit)
    note='# CNMV interim measures — scoped release and source boundaries\n\nControl: `'+CONTROL+'`\n\nBase: `'+BASE+'`. Two new bilingual public guides, two expanded existing CNMV landing pages, additive reciprocal links, 35 legal mechanisms, 78 authority/unit/custodian entries (15 screening-only), eight rights routes and ten continuity terms. This is a public research read model, not a competing canonical register.\n\nThe 333-row institutional register and prior ORION-NOTICE-20260905 blocks are preserved. The 6-May supervisory confirmation is not recast as inaction. The 4-September SAIP extension is not a refusal. Registration295 is not misconduct; interim measures remain requested, not granted. The user authorises publication, not email or REG-AGE filing.\n\n## Reproducible checks\n\nRun `python scripts/build_cnmv_interim_measures_20260905.py --check`. It checks deterministic outputs, original-content preservation, source/status boundaries, immutable canonical register, counts and all added local links/fragments. `--live` performs read-only public-byte and managed-block checks with bounded retries. The workflow has no write job on main.\n\n## Broader baseline exceptions\n\nThe preceding release records unrelated global failures in `ops/ORION_NOTICE_RELEASE_EXCEPTIONS_20260905.md`. This release must compare base and head with origin/main actually available; a shallow-checkout missing-base error is not evidence of a substantive baseline defect. No branch protection or general validator is disabled. A successful scoped check is not a claim that all historical repository defects are fixed. Actual run IDs and any remaining differences are recorded in the PR and Control Tower.\n\n## Deployment and external-action boundary\n\nPREPARED manifest status is a source-stage label. Only the actual merge SHA, successful Pages deployment and exact live verifier support a live closeout, recorded in Control Tower1428. No mail, filing, signature, authority contact or private-source upload is part of this release. The public request is not proof of institutional receipt.\n'
    out['ops/CNMV_INTERIM_RELEASE_20260905.md']=note
    return out

def validate(outputs):
    checks=0
    def ck(condition,msg):
        nonlocal checks
        checks+=1
        if not condition:raise AssertionError(msg)
    ck(len(D['tools'])==35,'35 mechanisms')
    ck(sum(len(g['entries']) for g in D['authority_groups'])==78,'78 entries')
    ck(sum(s=='screening' for g in D['authority_groups'] for _,s in g['entries'])==15,'15 screening entries')
    ck(len(D['rights'])==8 and len(D['continuity'])==10,'rights/continuity count')
    ck(all(not D[x] for x in ['new_communication_sent','new_regage_filing','official_measure_identified_as_granted']),'No false completed action')
    reg=(ROOT/D['canonical_register']).read_text()
    ck(reg==original(D['canonical_register']),'Canonical register modified')
    ck(len(json.loads(reg)['events'])==333,'Canonical event count')
    for path,text in outputs.items():
        ck((ROOT/path).exists(),'Missing output '+path)
        ck((ROOT/path).read_text()==text,'Non-deterministic / stale output '+path)
        if path.endswith('.html'):
            parsed=Parser(text)
            if path in ROUTES.values():
                ck(len(parsed.ids)==len(set(parsed.ids)),'Duplicate new-page IDs '+path)
                ck('noindex' not in text,'New guide marked noindex')
                for l in ['en','es']:ck('hreflang="'+l+'"' in text,'Missing alternate')
                scoped=text
            else:
                ck(strip_owned(text)==original(path),'Existing content changed beyond managed additions '+path)
                scoped=''.join(m.group(0) for m in re.finditer(re.escape(START)+r'.*?'+re.escape(END),text,re.S))
                scoped+=''.join(m.group(0) for m in re.finditer(re.escape(HSTART)+r'.*?'+re.escape(HEND),text,re.S))
                scoped+=''.join(m.group(0) for m in re.finditer(re.escape(JSTART)+r'.*?'+re.escape(JEND),text,re.S))
            for bad in ['mail.google.com','sdmnt','ANGjd','Y2231410X','Calle Pozo Cabildo','sbu001@monterecco.com']:
                ck(bad not in scoped,'Private source material '+bad)
            for href in Parser(scoped).links:
                u=urlsplit(href)
                if u.scheme in ['http','https','mailto','data']:continue
                pathpart=unquote(u.path)
                if pathpart.startswith(PREFIX):target=pathpart[len(PREFIX):]
                elif pathpart.startswith('/'):raise AssertionError('Non-project absolute path '+href)
                elif pathpart:target=str((Path(path).parent/pathpart))
                else:target=path
                targetp=(ROOT/target).resolve()
                ck(targetp.is_relative_to(ROOT),'Escaped root '+href)
                if targetp.is_dir() or pathpart.endswith('/'):targetp=targetp/'index.html'
                ck(targetp.exists(),'Broken internal path '+path+' -> '+href)
                if u.fragment:
                    ck(unquote(u.fragment) in Parser(targetp.read_text()).ids,'Broken fragment '+path+' -> '+href)
    print(jdump({'result':'SCOPED_PASS','checks':checks,'tools':35,'authority_entries':78,'screening_only':15,'canonical_events':333,'managed_existing_pages':len(json.loads(outputs[AUDIT])['managed_existing_pages']),'new_pages':2}))
    return checks

def live():
    a=json.loads((ROOT/AUDIT).read_text());token=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()
    files=list(dict.fromkeys(a['owned_files']+[D['canonical_register'],AUDIT]))
    blocks=a['managed_existing_pages']
    targets=files+blocks
    cache={}
    def get(path):
        url=HOST+path+'?cnmv_verify='+token
        req=Request(url,headers={'Cache-Control':'no-cache','User-Agent':'Por-Derecho-scoped-live-verifier'})
        with urlopen(req,timeout=35) as r:
            if r.status!=200:raise AssertionError(str(r.status)+' '+path)
            return r.read()
    for attempt in range(1,25):
        try:
            for path in targets:
                b=get(path);local=(ROOT/path).read_bytes();cache[path]=b
                if path in files:
                    if b!=local:raise AssertionError('Live bytes differ '+path)
                else:
                    remote=b.decode();text=local.decode()
                    for x,y in [(START,END),(HSTART,HEND),(JSTART,JEND)]:
                        lm=re.search(re.escape(x)+r'.*?'+re.escape(y),text,re.S)
                        if lm:
                            rm=re.search(re.escape(x)+r'.*?'+re.escape(y),remote,re.S)
                            if not rm or rm.group()!=lm.group():raise AssertionError('Live managed block differs '+path)
            print(jdump({'result':'LIVE_VERIFIED','commit':token,'exact_files':files,'managed_pages':blocks,'source_register_sha256':digest(cache[D['canonical_register']]),'attempt':attempt,'no_external_write':True}));return
        except Exception as e:
            print('Live attempt',attempt,'not yet verified:',e,flush=True)
            if attempt==24:raise
            time.sleep(20)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--check',action='store_true');ap.add_argument('--live',action='store_true');args=ap.parse_args()
    if args.live:live()
    else:
        outputs=prepared()
        if args.write:
            branch=subprocess.check_output(['git','branch','--show-current'],cwd=ROOT).decode().strip()
            if branch!='integration/cnmv-interim-measures-20260905':raise SystemExit('Writes allowed only on the designated integration branch, never main')
            for path,text in outputs.items():
                q=ROOT/path;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(text)
            print('Generated',len(outputs),'scoped files')
        validate(outputs)
