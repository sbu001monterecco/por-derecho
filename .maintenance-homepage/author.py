#!/usr/bin/env python3
"""One-shot bounded homepage authoring. Stages an unreferenced tree, never a release."""
from pathlib import Path
from collections import Counter
from html.parser import HTMLParser
import hashlib,json,os,re,subprocess,sys,urllib.request
ROOT=Path(sys.argv[1]).resolve();OUT=Path(sys.argv[2]).resolve();OUT.mkdir(parents=True,exist_ok=True)
BASE=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
CSS_PATH='assets/homepage-reading-20260925.css';MANIFEST='publication-manifests/homepage-reading-and-scope-20260925.json'
STYLE=r'''/* Homepage only. Existing text, anchors, images and other routes remain. */
body.pd-home-refined{font-size:17px;line-height:1.65;--pd-home-reading:72ch}
.pd-home-refined .hero{min-height:0}
.pd-home-refined .hero-grid{gap:clamp(1.5rem,4vw,3.5rem);padding-block:clamp(2.3rem,5vw,4rem);grid-template-columns:minmax(0,1.2fr) minmax(0,.8fr)}
.pd-home-refined .hero h1{max-width:18ch;font-size:clamp(2.6rem,4.9vw,4.6rem);line-height:1.06}
.pd-home-refined .hero .lead{font-size:1.075rem;line-height:1.6;margin-top:1.25rem;max-width:60ch}
.pd-home-refined .hero .actions{margin-top:1.25rem}
.pd-home-refined .hero .actions .button:first-child{background:#f0dfc4;color:#13252d;border-color:#f0dfc4}
.pd-home-refined .hero-photo{align-self:center}
.pd-home-refined .hero-photo figcaption{font-size:.9rem;line-height:1.5}
.pd-home-refined .header-inner{gap:1rem;max-width:80rem;min-height:4.5rem}
.pd-home-refined .brand{flex-shrink:0}
.pd-home-refined .main-nav{gap:.15rem;align-items:center;flex-wrap:wrap}
.pd-home-refined .main-nav>a{font-size:.91rem;padding:.6rem .55rem;min-height:44px;display:inline-flex;align-items:center}
.pd-home-refined .pd-home-more{position:relative;align-self:center;font-size:.91rem}
.pd-home-refined .pd-home-more>summary{cursor:pointer;padding:.6rem .65rem;min-height:44px;border-radius:.4rem;color:#dce4e5}
.pd-home-refined .pd-home-more[open]>summary{background:#24434a;color:#fff}
.pd-home-refined .pd-home-more-links{position:absolute;right:0;top:100%;width:min(25rem,90vw);padding:.7rem;display:grid;grid-template-columns:1fr 1fr;gap:.25rem;background:#13252d;border:1px solid #7d9295;border-radius:.6rem;box-shadow:0 14px 32px #10202833;z-index:60}
.pd-home-refined .pd-home-more-links a{font-size:.95rem;white-space:normal;min-height:44px}
.pd-home-refined .pd-home-orientation{margin-top:1.2rem;border-left:3px solid #c58a39;padding:.3rem 0 .3rem 1rem;max-width:62ch}
.pd-home-refined .pd-home-orientation p{margin:.2rem 0;color:#f3eee4;font-size:1rem;line-height:1.6}
.pd-home-refined .pd-home-orientation strong{color:#fff}
.pd-home-refined .pd-home-orientation a{color:#f0dfc4;text-decoration:underline;text-underline-offset:.2em}
.pd-home-refined .pd-home-scope{width:min(calc(100% - 2rem),76rem);margin:3rem auto;padding:clamp(1.25rem,3vw,2.5rem);background:#fffdf8;border:1px solid #d9d3c8;border-top:4px solid #146a70;border-radius:1rem;scroll-margin-top:6rem}
.pd-home-refined .pd-home-scope h2{font-size:clamp(2rem,3.3vw,3.2rem);max-width:30ch;margin:.4rem 0 1rem}
.pd-home-refined .pd-home-scope>p{max-width:var(--pd-home-reading)}
.pd-home-refined .pd-home-scope .pd-home-scope-status{color:#43585b;font-size:.9rem;font-weight:700;letter-spacing:.02em}
.pd-home-refined .pd-home-scope-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1.1rem;margin:1.5rem 0}
.pd-home-refined .pd-home-scope-grid article{padding:1.3rem;background:#f3f6f5;border:1px solid #cbdad7;border-radius:.7rem}
.pd-home-refined .pd-home-scope-grid h3{font-size:1.35rem;line-height:1.2;margin:.15rem 0 .8rem}
.pd-home-refined .pd-home-scope-grid p{font-size:1rem;line-height:1.65;margin:0}
.pd-home-refined .pd-home-proof-boundary{padding:1rem 1.25rem;background:#f4eee3;border-left:4px solid #9a6a20;font-size:1rem;line-height:1.65}
.pd-home-refined .pd-home-source-link{font-size:.95rem}
.pd-home-refined .pd-five-ac{border-width:2px;box-shadow:0 .8rem 2rem #10202812;margin-block:2rem 3rem}
.pd-home-refined .pd-five-ac__head{padding:clamp(1.25rem,3vw,2.1rem)}
.pd-home-refined .pd-five-ac__head h2{font-size:clamp(2rem,3.5vw,3.15rem);line-height:1.12;max-width:32ch}
.pd-home-refined .pd-five-ac__head p{font-size:1.05rem;line-height:1.7;max-width:72ch}
.pd-home-refined .pd-five-ac__criminal{padding:1.25rem 1.5rem;border-bottom-width:3px}
.pd-home-refined .pd-five-ac__criminal p{font-size:1rem;line-height:1.65}
.pd-home-refined .pd-five-ac__criminal strong{font-size:clamp(1.15rem,2.2vw,1.6rem);line-height:1.3}
.pd-home-refined .pd-five-ac__private,.pd-home-refined .pd-five-ac__institutional,.pd-home-refined .pd-five-ac__linkage{padding:clamp(1rem,2vw,1.6rem)}
.pd-home-refined .pd-five-ac__eyebrow,.pd-home-refined .pd-five-ac__criminal small,.pd-home-refined .pd-five-ac__institution-role{font-size:.875rem;line-height:1.5;font-weight:800;letter-spacing:.04em}
.pd-home-refined .pd-five-ac__context,.pd-home-refined .pd-five-ac__legend span{font-size:.875rem;line-height:1.5}
.pd-home-refined .pd-five-ac__private-head p,.pd-home-refined .pd-five-ac__institutional-head p,.pd-home-refined .pd-five-ac__linkage-head p{font-size:1rem;line-height:1.65;max-width:72ch}
.pd-home-refined .pd-five-ac__card{padding:1.1rem;min-height:0;border-top-width:3px;background:#fffdf8;overflow:visible}
.pd-home-refined .pd-five-ac__card::after{content:none}
.pd-home-refined .pd-five-ac__name{font-size:1.25rem;line-height:1.25;overflow-wrap:anywhere}
.pd-home-refined .pd-five-ac__copy,.pd-home-refined .pd-five-ac__institution-copy{font-size:1rem;line-height:1.65}
.pd-home-refined .pd-five-ac__stage{font-size:.875rem;line-height:1.5;min-height:0;font-weight:800}
.pd-home-refined .pd-five-ac__rel{font-size:.9rem;line-height:1.5;font-weight:700}
.pd-home-refined .pd-five-ac__cluster-figure figcaption,.pd-home-refined .pd-five-ac__portrait-note,.pd-home-refined .pd-five-ac__evidence-visuals figcaption{font-size:.9rem;line-height:1.6}
.pd-home-refined .pd-five-ac__image-boundary{font-weight:600}
.pd-home-refined .pd-five-ac__institution-name{font-size:1.4rem;line-height:1.25}
.pd-home-refined .pd-five-ac__accountability-columns{grid-template-columns:1fr;gap:.8rem}
.pd-home-refined .pd-five-ac__accountability-column strong{font-size:.9rem;line-height:1.5}
.pd-home-refined .pd-five-ac__accountability-column ul{font-size:1rem;line-height:1.65}
.pd-home-refined .pd-five-ac__institution-allegation,.pd-home-refined .pd-five-ac__institution-boundary,.pd-home-refined .pd-five-ac__lock,.pd-home-refined .pd-five-ac__linkage-boundary{font-size:1rem;line-height:1.65;font-weight:600}
.pd-home-refined .pd-five-ac__linkage-cell{font-size:.95rem;line-height:1.6;overflow-wrap:anywhere}
.pd-home-refined .pd-five-ac__linkage-actor{font-size:1rem;line-height:1.5}
.pd-home-refined .pd-five-ac__steps strong,.pd-home-refined .pd-five-ac__steps span{font-size:.95rem;line-height:1.55}
.pd-home-refined .pd-five-ac__steps{grid-template-columns:repeat(4,minmax(0,1fr))}
.pd-home-refined .pd-five-ac__notice p,.pd-home-refined .pd-five-ac__hinge p{font-size:1rem;line-height:1.65}
.pd-home-refined .pd-five-ac__links a{font-size:.95rem;min-height:44px;align-items:center}
.pd-home-refined .pd-five-ac__correction{font-size:.95rem;line-height:1.65}
.pd-home-refined .section-head p{line-height:1.7}
.pd-home-refined p,.pd-home-refined li{overflow-wrap:break-word}
.pd-home-refined :is(a,button,summary):focus-visible{outline:3px solid #c58a39;outline-offset:4px}
@media(max-width:1200px){.pd-home-refined .header-inner{flex-wrap:wrap;padding-block:.7rem}.pd-home-refined .main-nav{width:100%;justify-content:flex-start}.pd-home-refined .pd-five-ac__cards{grid-template-columns:1fr}.pd-home-refined .pd-five-ac__institution-person{grid-template-columns:7rem minmax(0,1fr)}.pd-home-refined .pd-five-ac__institution-portrait{width:7rem;height:8.3rem}}
@media(max-width:800px){.pd-home-refined .site-header{position:relative}.pd-home-refined .hero-grid{grid-template-columns:1fr}.pd-home-refined .hero-photo{max-width:40rem}.pd-home-refined .pd-home-scope-grid{grid-template-columns:1fr}.pd-home-refined .pd-five-ac__cards,.pd-home-refined .pd-five-ac__cluster-cards--trio,.pd-home-refined .pd-five-ac__cluster-cards--pair,.pd-home-refined .pd-five-ac__institutional-grid{grid-template-columns:1fr}.pd-home-refined .pd-five-ac__steps{grid-template-columns:1fr}.pd-home-refined .pd-five-ac__steps li{min-height:0}.pd-home-refined .pd-five-ac__institution-person{grid-template-columns:6.5rem minmax(0,1fr)}.pd-home-refined .pd-five-ac__institution-portrait{width:6.5rem;height:7.8rem}.pd-home-refined .pd-home-more-links{position:static;width:100%;box-shadow:none}.pd-home-refined .pd-home-more[open]{flex-basis:100%}.pd-home-refined .pd-home-more-links{grid-template-columns:1fr 1fr}.pd-home-refined .pd-five-ac__linkage-cell{grid-template-columns:1fr}.pd-home-refined .pd-five-ac__linkage-cell::before{font-size:.875rem}}
/* Native navigation remains available when JavaScript is disabled. */
.pd-home-refined .nav-toggle{display:none}
.pd-home-refined #main-nav{display:flex!important;position:static;transform:none;max-height:none;height:auto;opacity:1;visibility:visible;overflow:visible}
@media(max-width:480px){.pd-home-refined .main-nav>a{font-size:.9rem;padding:.5rem}.pd-home-refined .pd-five-ac__institution-person{grid-template-columns:1fr}.pd-home-refined .pd-five-ac__institution-portrait{width:8rem;height:auto;max-height:none}.pd-home-refined .pd-home-more-links{grid-template-columns:1fr}}
@media(prefers-reduced-motion:reduce){.pd-home-refined{scroll-behavior:auto}.pd-home-refined *{scroll-behavior:auto;animation:none!important;transition:none!important}}
@media print{.pd-home-refined .pd-home-more-links{position:static}.pd-home-refined .pd-home-scope,.pd-home-refined .pd-five-ac{box-shadow:none}}
'''
COPY={
'en':{'orientation':'<div class="pd-home-orientation" data-homepage-scope="20260925"><p><strong>Sun Park is a principal evidential entry point, not the limit of the allegation.</strong> Gil Marer alleges a wider Acosta Matos asset-acquisition and accumulation programme built on the reported unlawful conduct, its economic benefits and financing capacity. <a href="#economic-scope-20260925">Whole-portfolio allegation; asset-by-asset substantiation.</a></p></div>','people':'People & accountability','more':'More routes','selected':['#recovery','#record','updates/','future/'],'section':'''<section class="pd-home-scope" id="economic-scope-20260925" aria-labelledby="economic-scope-title-20260925" data-scope-status="attributed-allegation-not-adjudicated"><p class="pd-home-scope-status">Position stated by Gil Marer · 25 September 2026 · Not an adjudicated finding</p><h2 id="economic-scope-title-20260925">The whole acquired portfolio is the allegation’s perimeter.</h2><p>Gil Marer alleges that the whole asset portfolio acquired within the relevant Acosta Matos perimeter during the approximately six-to-eight-year acquisition cycle described in his 25 September 2026 statement was built on the reported unlawful conduct and the resulting control of assets, economic benefits and financing capacity. The allegation is not confined to one hotel, the capital raised through RICPE or one public subsidy.</p><p><strong>Whole-portfolio allegation; asset-by-asset substantiation.</strong> Requiring proof of each connection does not reduce the allegation to the transactions already quantified.</p><div class="pd-home-scope-grid" aria-label="Three distinct connections to investigate"><article><h3>Proceeds and reinvestment</h3><p>Did money, property or substitute value derived from the alleged conduct enter another company, acquisition or investment? Follow ownership and dated transfers; do not infer a transfer from association.</p></article><article><h3>Assets, income and financing</h3><p>Were assets, rights or operating income used as collateral, guarantees, refinancing support or released equity for later acquisitions? The initial funding amount is not necessarily the limit of the inquiry.</p></article><article><h3>Commercial-platform contribution</h3><p>Did the project, its apparent ownership, operation or approvals help attract investors, lenders or partners? Commercial enablement and traceable criminal proceeds remain separate questions.</p></article></div><p class="pd-home-proof-boundary"><strong>What must still be established:</strong> ownership, acquisition funding, the relevant causal connection, independent lawful resources and third-party interests for each asset. RICPE is examined as a separate financing and documentary channel, not automatically as an Acosta Matos group company. RIC-related arrangements and public support do not establish that tax incentives and grants are the same funds. No consolidated attributable euro value, collective liability or unlawful origin of every asset is established here. The economic allegation does not establish who caused any digital incident.</p><p>Gross acquired asset value, actual economic interests, allegedly attributable value, and income or onward transfers must be measured separately, without counting the same value repeatedly. The pre-existing business and lawful funding baseline remains part of the test.</p><p class="pd-home-source-link"><a href="#record">Examine the source record</a> · <a href="ric-private-equity-sun-park/">RICPE source analysis</a> · <a href="public-authority-unitary-case-reconstruction/">Institutional reconstruction</a> · <a href="../publication-manifests/homepage-reading-and-scope-20260925.json">Statement scope and publication provenance</a></p></section>'''},
'es':{'orientation':'<div class="pd-home-orientation" data-homepage-scope="20260925"><p><strong>Sun Park es una entrada probatoria principal, no el límite de la acusación.</strong> Gil Marer alega un proceso más amplio de adquisición y acumulación de activos del perímetro Acosta Matos construido sobre las conductas ilícitas denunciadas, sus beneficios económicos y su capacidad de financiación. <a href="#economic-scope-20260925">Alegación sobre el conjunto de la cartera; prueba activo por activo.</a></p></div>','people':'Personas y responsabilidades','more':'Más rutas','selected':['#recuperacion','#registro','actualizaciones/','futuro/'],'section':'''<section class="pd-home-scope" id="economic-scope-20260925" aria-labelledby="economic-scope-title-20260925" data-scope-status="attributed-allegation-not-adjudicated"><p class="pd-home-scope-status">Posición expresada por Gil Marer · 25 de septiembre de 2026 · No es una conclusión judicial</p><h2 id="economic-scope-title-20260925">La alegación abarca toda la cartera adquirida.</h2><p>Gil Marer alega que el conjunto de la cartera de activos adquirida dentro del perímetro Acosta Matos relevante durante el ciclo de adquisiciones de aproximadamente seis a ocho años descrito en su declaración de 25 de septiembre de 2026 se construyó sobre las conductas ilícitas denunciadas y el consiguiente control de activos, beneficios económicos y capacidad de financiación. La alegación no se limita a un hotel, al capital captado mediante RICPE ni a una subvención pública.</p><p><strong>Alegación sobre el conjunto de la cartera; prueba activo por activo.</strong> Exigir prueba de cada conexión no reduce la alegación a las operaciones ya cuantificadas.</p><div class="pd-home-scope-grid" aria-label="Tres conexiones distintas que investigar"><article><h3>Beneficios y reinversión</h3><p>¿Entraron dinero, bienes o valor sustitutivo derivados de las conductas alegadas en otra sociedad, adquisición o inversión? Deben seguirse la titularidad y las transferencias fechadas, sin inferir una transferencia por asociación.</p></article><article><h3>Activos, ingresos y financiación</h3><p>¿Se utilizaron activos, derechos o ingresos operativos como garantía, aval, respaldo de refinanciación o liberación de capital para adquisiciones posteriores? El importe inicial no limita necesariamente la investigación.</p></article><article><h3>Contribución de la plataforma comercial</h3><p>¿Ayudaron el proyecto, su aparente titularidad, su explotación o sus autorizaciones a atraer inversores, financiadores o socios? La contribución comercial y los beneficios delictivos trazables son cuestiones distintas.</p></article></div><p class="pd-home-proof-boundary"><strong>Qué debe acreditarse:</strong> la titularidad, la financiación de la adquisición, la conexión causal relevante, los recursos lícitos independientes y los derechos de terceros respecto de cada activo. RICPE se examina como un canal separado de financiación y documentación, no automáticamente como una sociedad del grupo Acosta Matos. Los instrumentos vinculados a la RIC y las ayudas públicas no acreditan que los incentivos fiscales y las subvenciones sean los mismos fondos. Aquí no se establece una cifra consolidada de valor atribuible, responsabilidad colectiva ni el origen ilícito de todos los activos. La alegación económica no identifica al causante de ningún incidente digital.</p><p>El valor bruto de los activos adquiridos, los intereses económicos reales, el valor presuntamente atribuible y los ingresos o transferencias posteriores deben medirse por separado, sin contar reiteradamente el mismo valor. La actividad preexistente y la financiación lícita de partida siguen formando parte del contraste.</p><p class="pd-home-source-link"><a href="#registro">Examinar las fuentes</a> · <a href="ric-private-equity-sun-park/">Análisis documental de RICPE</a> · <a href="reconstruccion-unitaria-autoridades-publicas/">Reconstrucción institucional</a> · <a href="../publication-manifests/homepage-reading-and-scope-20260925.json">Alcance y procedencia de la publicación</a></p></section>'''}}
class Census(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.links=[];self.images=[];self.words=[];self.skip=0
 def handle_starttag(self,t,a):
  d=dict(a)
  if t in ('script','style'):self.skip+=1
  if d.get('id'):self.ids.append(d['id'])
  if t=='a' and d.get('href'):self.links.append(d['href'])
  if t=='img' and d.get('src'):self.images.append(d['src'])
 def handle_endtag(self,t):
  if t in ('script','style'):self.skip=max(0,self.skip-1)
 def handle_data(self,d):
  if not self.skip:self.words.extend(d.split())
def census(t):
 p=Census();p.feed(t);return p
def section_end(t,start):
 depth=0
 for m in re.finditer(r'<(/?)section\b[^>]*>',t[start:],re.I):
  depth+=-1 if m.group(1) else 1
  if depth==0:return start+m.end()
 raise RuntimeError('Unbalanced protected section')
def run(cmd,name):
 p=subprocess.run(cmd,cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=240)
 (OUT/(name+'.log')).write_text(p.stdout,encoding='utf8');print(name,'EXIT',p.returncode,p.stdout[-1800:],flush=True)
 return {'name':name,'exit_code':p.returncode}
commands=[['python3','scripts/validate_repository_preservation.py'],['python3','scripts/validate_publication_integrity.py'],['python3','scripts/validate_audience_experience.py']]
baseline=[run(c,'baseline-'+str(i)) for i,c in enumerate(commands)]
receipts={};changed=[]
for lang,c in COPY.items():
 path=ROOT/lang/'index.html';old=path.read_text();new=old
 assert 'pd-home-refined' not in old,'Already applied: review successor rather than duplicate it'
 new=re.sub(r'<body([^>]*)>',lambda m:'<body'+m[1]+' class="pd-home-refined">' if 'class=' not in m[1] else '<body'+re.sub(r'class="([^"]*)"',r'class="\1 pd-home-refined"',m[1])+'>',new,count=1)
 assert new!=old
 new=new.replace('</head>',f'<link rel="stylesheet" href="../{CSS_PATH}" data-homepage-reading="20260925">\n</head>',1)
 lead=re.search(r'<p class="lead">.*?</p>',new,re.S);assert lead
 new=new[:lead.end()]+c['orientation']+new[lead.end():]
 nav=re.search(r'(<nav\b[^>]*\bid="main-nav"[^>]*>)(.*?)(</nav>)',new,re.S);assert nav
 anchors=re.findall(r'<a\b.*?</a>',nav[2],re.S);assert len(anchors)>=12
 primary=[];secondary=[];language=[]
 for a in anchors:
  if 'class="language-link"' in a:language.append(a)
  elif any('href="'+h+'"' in a for h in c['selected']):primary.append(a)
  else:secondary.append(a)
 assert len(language)==1 and len(primary)==4
 content='\n<a href="#pd-five-ac-title" class="pd-home-people">'+c['people']+'</a>\n'+'\n'.join(primary)+'\n<details class="pd-home-more"><summary>'+c['more']+'</summary><div class="pd-home-more-links">'+'\n'.join(secondary)+'</div></details>\n'+language[0]+'\n'
 new=new[:nav.start()]+nav[1]+content+nav[3]+new[nav.end():]
 start=new.index('<section class="pd-five-ac"');end=section_end(new,start);protected=new[start:end]
 new=new[:end]+'\n'+c['section']+'\n'+new[end:]
 before=census(old);after=census(new)
 assert not (Counter(before.ids)-Counter(after.ids)),'Removed anchor'
 assert not (Counter(before.links)-Counter(after.links)),'Removed link'
 assert not (Counter(before.images)-Counter(after.images)),'Removed image'
 assert not (Counter(before.words)-Counter(after.words)),'Removed original text'
 assert len(after.ids)==len(set(after.ids)),'Duplicate IDs'
 old_start=old.index('<section class="pd-five-ac"');old_protected=old[old_start:section_end(old,old_start)]
 assert protected==old_protected,'Protected seven-person block changed'
 path.write_text(new,encoding='utf8');changed.append(lang+'/index.html')
 receipts[lang]={'old_sha256':hashlib.sha256(old.encode()).hexdigest(),'new_sha256':hashlib.sha256(new.encode()).hexdigest(),'protected_block_sha256':hashlib.sha256(protected.encode()).hexdigest(),'all_original_text_links_images_and_ids_retained':True}
(ROOT/CSS_PATH).write_text(STYLE,encoding='utf8');changed.append(CSS_PATH)
post=[run(c,'candidate-'+str(i)) for i,c in enumerate(commands)]
manifest={'schema':'por-derecho.homepage-reading-scope.v1','control_date':'2026-09-25','state':'CANDIDATE_REQUIRES_PR_CHECKS_AND_LIVE_READBACK','base_sha':BASE,'existing_pr':1893,'prior_candidate_head':'d83f48d1f14f5f0b16eb1be344f9c245b7a826e5','authority':'Owner instruction in the homepage-refinement conversation, 25 September 2026. Retain the seven substantive front-page presentations and relevant appearances elsewhere; use the owner-supplied whole-portfolio framing.','scope_source':'PD-OWNER-PORTFOLIO-SCOPE-20260925; owner-adopted allegation, not an independent report or adjudicated finding','source_limit':'Unresolved embedded references in the supplied statement are not promoted as verified report citations. No new quantified AUM, guilt finding, third-party transfer or digital-incident attribution.','statement_period':'The approximately six-to-eight-year acquisition cycle described as of 25 September 2026; not a moving window or a uniform start date for every asset.','paths':changed+[MANIFEST],'preservation':receipts,'baseline_checks':baseline,'candidate_checks':post,'seven_person_record':'Protected block retained byte-for-byte. No actor or institutional node hidden or moved off the homepage.','other_routes':'Untouched; repeated relevant appearances remain.','private_boundary':'No mailbox originals, provider message IDs, identity-document material, private financial ledgers or legal advice published.','gitlab_state':'NOT_UPDATED_BY_THIS_PACKAGE','live_state':'NOT_VERIFIED_BY_AUTHORING_HELPER'}
(ROOT/MANIFEST).parent.mkdir(exist_ok=True);(ROOT/MANIFEST).write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');changed.append(MANIFEST)
(OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
for rel in changed:
 dest=OUT/'candidate'/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes((ROOT/rel).read_bytes())
status=subprocess.check_output(['git','diff','--name-only'],cwd=ROOT,text=True).splitlines();assert set(status)<=set(changed),status
repo=os.environ['GITHUB_REPOSITORY'];token=os.environ['GH_TOKEN']
def api(method,path,payload=None):
 data=None if payload is None else json.dumps(payload).encode()
 req=urllib.request.Request('https://api.github.com/repos/'+repo+path,data=data,method=method,headers={'Authorization':'Bearer '+token,'Accept':'application/vnd.github+json','Content-Type':'application/json','X-GitHub-Api-Version':'2022-11-28'})
 with urllib.request.urlopen(req,timeout=90) as r:return json.load(r)
base_tree=subprocess.check_output(['git','rev-parse','HEAD^{tree}'],cwd=ROOT,text=True).strip()
tree=api('POST','/git/trees',{'base_tree':base_tree,'tree':[{'path':p,'mode':'100644','type':'blob','content':(ROOT/p).read_text()} for p in changed]})
result={'base_sha':BASE,'base_tree':base_tree,'tree_sha':tree['sha'],'changed_paths':changed,'baseline_checks':baseline,'candidate_checks':post}
(OUT/'candidate-tree.json').write_text(json.dumps(result,indent=2));print('PD_CANDIDATE_TREE='+json.dumps(result),flush=True)
