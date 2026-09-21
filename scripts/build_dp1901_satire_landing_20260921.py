#!/usr/bin/env python3
"""Build the authorized bilingual editorial landing pages without replacing the dossier.

Network-free builder. The two already hash-controlled image renditions must be
provided at ASSET paths. No publication, social posting or filing is performed.
"""
from __future__ import annotations
import hashlib
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = '/por-derecho/'
HOST = 'https://sbu001monterecco.github.io'
PID = 'PD-SAT-DP1901-SHAME-20260921'
FAMILY = 'PD-DMA-FAM-DP1901-SHAME-001'
ASSET = 'assets/visuals/dp1901-shame-20260921/'
CSS_PATH = 'assets/dp1901-satire-landing-20260921.css'
JS_PATH = 'assets/dp1901-satire-copy-20260921.js'
ROUTES = {
 'en': 'en/dp-1901-2026/shame-has-left-the-building/',
 'es': 'es/dp-1901-2026/la-verguenza-no-se-fue/'
}
SOURCES = {
 'identity': 'evidence/judicial/dp-1901-2026/PROCEDURAL_IDENTITY_SOURCE_CLOSURE_18SEP2026.md',
 'order': 'evidence/judicial/dp-1901-2026/full-text/auto-14sep2026-public-transcription.md',
 'complaints': 'data/three-track-full-digitisation-20260904.json',
 'control24': 'evidence/judicial-governance/decanato-reference-24/README.md'
}
POSTS = {
'en': '''SHAME HAS LEFT THE BUILDING.
It didn’t leave. It was thrown out.

SATIRE / SÁTIRA — EDITORIAL METAPHOR

In this image, Shame is expelled through the courthouse entrance while the shadows behind the building bury Justice, effective judicial protection and the rule of law.

The scene is fictional. The questions behind it are not.

In June 2026, I presented separate complaints in Las Palmas: Ref. 24 concerned judicial conduct; Ref. 21 concerned five private actors. Contemporary July records show private-actor material submitted under DP 1901/2026. The certified electronic history explaining the subsequent treatment of those separate matters remains outstanding in the record available to me.

On 14 September 2026, an order described DP 1901 as a judicial-prevarication matter, recorded a 29 July prosecution request for dismissal, and ordered sobreseimiento libre and archive. The court considered the allegations insufficiently supported. I dispute that assessment.

But this is not simply disagreement with an adverse decision.

The underlying complaints address alleged fabrication and use of community authority, minutes and debt; access to and control of Sun Park; and the subsequent route through liquidation, title, hotel operation, financing and income. Those are allegations requiring examination—not findings of guilt, but not merely bookkeeping disagreements either.

What happened to the private-actor complaint? What evidence reached Fiscalía? What was actually examined before dismissal?

The signed prosecution report, its authorship and complete documentary basis have not been located in the controlled record available to me. That absence does not prove destruction or improper coordination. It identifies precisely what needs to be produced and explained.

I am asking for the records to be preserved, the report to be produced, and the handling of each complaint to be reconstructed—without allowing separate allegations to disappear inside an unexplained procedural history.

Judicial independence must coexist with accountability. So must prosecutorial legality and impartiality.

I write as a directly and indirectly affected party and as an alertador invoking Spain’s Law 2/2023, seeking verification, preservation and effective protection—not a predetermined verdict.

The image depicts generic institutional figures, not identifiable officials committing a literal act.

A file can be closed. Accountability should not be buried with it.

#RuleOfLaw #JudicialAccountability #Whistleblowing #ProjectSunRock''',
'es': '''LA VERGÜENZA HA SALIDO DEL EDIFICIO.
No se fue. La echaron.

SÁTIRA — METÁFORA EDITORIAL

En esta imagen, expulsan a la Vergüenza por la entrada del juzgado mientras las sombras, detrás del edificio, entierran la Justicia, la tutela judicial efectiva y el Estado de Derecho.

La escena es ficticia. Las preguntas que plantea no lo son.

En junio de 2026 presenté denuncias separadas en Las Palmas: la Ref. 24 se refería a actuaciones judiciales; la Ref. 21, a cinco actores privados. Documentos contemporáneos de julio muestran la presentación de material de la vía privada bajo DP 1901/2026. Sigue pendiente, en la documentación a mi disposición, la historia electrónica certificada que explique el tratamiento posterior de ambos asuntos.

El Auto de 14 de septiembre de 2026 describió DP 1901 como un asunto de presunta prevaricación judicial, recogió una solicitud fiscal de archivo de 29 de julio y acordó el sobreseimiento libre y el archivo. El juzgado consideró insuficientemente sustentadas las alegaciones. Discrepo de esa valoración.

Pero no se trata simplemente de discrepar de una resolución adversa.

Las denuncias abordan la presunta fabricación y utilización de autoridad comunitaria, actas y deuda; el acceso y control de Sun Park; y la secuencia posterior de liquidación, titularidad, explotación hotelera, financiación e ingresos. Son alegaciones que requieren examen: no declaraciones de culpabilidad, pero tampoco meras discrepancias contables.

¿Qué ocurrió con la denuncia contra los actores privados? ¿Qué documentación recibió Fiscalía? ¿Qué se examinó realmente antes del archivo?

No se han localizado, en el corpus controlado a mi disposición, el informe fiscal firmado, su autoría ni su base documental completa. Esa ausencia no demuestra destrucción ni coordinación indebida. Delimita lo que debe aportarse y explicarse.

Pido preservar los registros, aportar el informe y reconstruir la tramitación de cada denuncia, sin que alegaciones autónomas desaparezcan dentro de una historia procesal sin explicar.

La independencia judicial debe coexistir con la rendición de cuentas. También la legalidad y la imparcialidad del Ministerio Fiscal.

Escribo como parte directa e indirectamente afectada y como alertador que invoca la Ley 2/2023, solicitando verificación, preservación y protección efectiva, no un resultado predeterminado.

La imagen representa figuras institucionales genéricas, no funcionarios identificables cometiendo un acto real.

Un expediente puede archivarse. La rendición de cuentas no debería enterrarse con él.

#EstadoDeDerecho #RendiciónDeCuentas #Alertadores #ProjectSunRock'''
}
TEXT = {
'en': {
 'title': 'Shame has left the building', 'headline': 'Shame has left<br>the building.',
 'subtitle': 'It didn’t leave. It was thrown out.', 'label': 'SATIRE · EDITORIAL METAPHOR',
 'disclosure': 'SATIRICAL / CARICATURE REPRESENTATION — NOT A REAL ADVERTISEMENT',
 'deck': 'Two complaints. Two identities. What else is being buried?',
 'intro': 'An editorial response to the disputed handling of DP 1901/2026. The illustration is fictional; the documented questions, the adverse order and the limits of the available record are linked below.',
 'dossier': 'Read the DP 1901 dossier', 'post': 'English LinkedIn post',
 'other': 'Español', 'sources': 'The record behind the metaphor',
 'source_intro': 'Read the source documents alongside the criticism. An allegation, a procedural act and an unresolved question are not interchangeable.',
 'alt': 'AI-generated editorial satire: generic judge and prosecutor expel a ghost labelled Shame; their shadows bury allegorical Justice beside separate Ref. 21 and Ref. 24 folders. Not a photograph or a factual depiction.',
 'caption': 'AI-generated illustration. The institutional figures, physical scene, architectural details and wall inscriptions are fictional or symbolic, not authenticated portraits, a courthouse photograph or official statements. No official endorsement is implied.',
 'image_note': 'The original English-title artwork is preserved without changing its composition. This page serves compressed web renditions; the illustration is not primary evidence.',
 'full_image': 'Open the full illustration', 'manual': 'Prepared for manual publication · English first',
 'post_intro': 'First-person editorial copy prepared for the complainant’s manual LinkedIn publication. It has not been posted or scheduled by this page. The source links below preserve the supporting record and its qualifications.',
 'copy': 'Copy post + link', 'download': 'Download plain text', 'copied': 'Copied. Nothing has been posted.',
 'copyfail': 'Automatic copy is unavailable. Use the plain-text download or select the post text.',
 'chars': 'characters, including the landing-page link',
 'boundary_title': 'What this publication does—and does not—say',
 'boundary': 'The burial and expulsion are editorial metaphors. They do not establish destruction of documents, improper coordination, intent or personal criminal responsibility. The signed prosecution report and the certified electronic history remain production questions in the reviewed record. The court’s contrary assessment is expressly retained. Publication is not a court filing, service, admission, appeal or determination of rights.',
 'correction': 'Corrections and responses',
 'correction_text': 'A correction or reply should identify the specific statement or image element and the supporting source. Use the contact and reply channels in the main DP 1901 dossier. New official records may change the analysis.',
 'footer': 'Por Derecho / Project Sun Rock · Editorial page prepared 21 September 2026 · Manual social publication only',
 'cards': [
  ('DOCUMENTED PRESENTATIONS', 'Two separate complaints', 'The June stamped covers and contemporaneous July record distinguish Ref. 24, the judge-related filing, from Ref. 21, the five-private-actor complaint. The 25 June supplement belongs to Ref. 24. Private-actor material was physically tendered under DP 1901 on 9 July; a certified electronic history remains outstanding.', 'identity', 'Read the June–July source record'),
  ('OFFICIAL OUTCOME · CONTRARY ASSESSMENT', 'The 14 September order', 'The controlled transcription records the court’s assessment that the allegations were insufficiently supported, the 29 July prosecution request for dismissal, and the order for sobreseimiento libre and archive. The complainant disputes that assessment. The transcription is not the native court file or proof of finality.', 'order', 'Read the complete order transcription'),
  ('ATTRIBUTED ALLEGATIONS · OPEN PROOF', 'More than a dispute over labels', 'The June pleadings address alleged manufacture and use of community authority, minutes and debt; access, control, liquidation and economic effects. The administrator, judge and five private actors remain separate. Shared documents do not transfer knowledge, intent or liability.', 'complaints', 'Read the three-track source inventory')
 ]
},
'es': {
 'title': 'La vergüenza no se fue. La echaron.', 'headline': 'La vergüenza<br>no se fue.',
 'subtitle': 'La echaron.', 'label': 'SÁTIRA · METÁFORA EDITORIAL',
 'disclosure': 'CARICATURA / REPRESENTACIÓN SATÍRICA — NO ES UN ANUNCIO REAL',
 'deck': 'Dos denuncias. Dos identidades. ¿Qué más se está enterrando?',
 'intro': 'Una respuesta editorial al tratamiento controvertido de DP 1901/2026. La ilustración es ficticia; las cuestiones documentadas, la resolución adversa y los límites del corpus disponible se enlazan a continuación.',
 'dossier': 'Leer el expediente DP 1901', 'post': 'Publicación en español para LinkedIn',
 'other': 'English', 'sources': 'La documentación detrás de la metáfora',
 'source_intro': 'Las fuentes deben leerse junto con la crítica. Una alegación, una actuación procesal y una cuestión no resuelta no son intercambiables.',
 'alt': 'Sátira editorial generada con IA: un juez y una fiscal genéricos expulsan a un fantasma llamado Shame; sus sombras entierran a la Justicia alegórica junto a carpetas separadas Ref. 21 y Ref. 24. No es una fotografía ni una representación factual.',
 'caption': 'Ilustración generada con IA. Las figuras institucionales, la escena física, los detalles arquitectónicos y las inscripciones son ficticios o simbólicos, no retratos autenticados, una fotografía del juzgado ni declaraciones oficiales. No se implica respaldo institucional.',
 'image_note': 'Se conserva la ilustración original con el titular en inglés, sin alterar su composición. Su traducción es: «La vergüenza ha salido del edificio. No se fue. La echaron». Esta página utiliza versiones comprimidas; la imagen no es prueba primaria.',
 'full_image': 'Abrir la ilustración completa', 'manual': 'Preparado para publicación manual · Después de la versión inglesa',
 'post_intro': 'Texto editorial en primera persona preparado para que el denunciante lo publique manualmente en LinkedIn. Esta página no lo ha publicado ni programado. Las fuentes conservan el respaldo documental y sus límites.',
 'copy': 'Copiar texto y enlace', 'download': 'Descargar texto', 'copied': 'Copiado. No se ha publicado nada.',
 'copyfail': 'No se puede copiar automáticamente. Descargue el texto o selecciónelo en la página.',
 'chars': 'caracteres, incluido el enlace a esta página',
 'boundary_title': 'Qué afirma esta publicación y qué no',
 'boundary': 'El entierro y la expulsión son metáforas editoriales. No acreditan destrucción documental, coordinación indebida, intención ni responsabilidad penal personal. El informe fiscal firmado y la historia electrónica certificada siguen siendo extremos cuya aportación se solicita en el corpus revisado. Se conserva expresamente la valoración contraria del juzgado. La publicación no equivale a presentación judicial, notificación, admisión, recurso ni determinación de derechos.',
 'correction': 'Correcciones y respuestas',
 'correction_text': 'Una corrección o réplica debe identificar la afirmación o elemento visual concreto y su fuente. Utilice los canales de contacto y respuesta del expediente principal DP 1901. La incorporación de documentos oficiales nuevos puede modificar el análisis.',
 'footer': 'Por Derecho / Project Sun Rock · Página editorial preparada el 21 de septiembre de 2026 · Publicación social exclusivamente manual',
 'cards': [
  ('PRESENTACIONES DOCUMENTADAS', 'Dos denuncias separadas', 'Las portadas selladas de junio y los documentos contemporáneos de julio distinguen la Ref. 24, relativa a actuaciones judiciales, de la Ref. 21, contra cinco actores privados. La ampliación de 25 de junio pertenece a la Ref. 24. El 9 de julio se presentó material de la vía privada bajo DP 1901; sigue pendiente la historia electrónica certificada.', 'identity', 'Leer el cierre de fuentes de junio y julio'),
  ('RESOLUCIÓN OFICIAL · VALORACIÓN CONTRARIA', 'El Auto de 14 de septiembre', 'La transcripción controlada recoge la valoración judicial de insuficiente sustento de las alegaciones, la solicitud fiscal de archivo de 29 de julio y el sobreseimiento libre y archivo. El denunciante discrepa de esa valoración. La transcripción no es el expediente judicial nativo ni prueba de firmeza.', 'order', 'Leer la transcripción íntegra del Auto'),
  ('ALEGACIONES ATRIBUIDAS · PRUEBA PENDIENTE', 'Más que una disputa de etiquetas', 'Los escritos de junio abordan la presunta fabricación y utilización de autoridad comunitaria, actas y deuda; el acceso, control, liquidación y efectos económicos. El administrador, el juez y los cinco privados permanecen separados. Compartir documentación no transfiere conocimiento, intención ni responsabilidad.', 'complaints', 'Leer el inventario de las tres vías')
 ]
}}
CSS = '''*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#f5f2eb;color:#17252b;font-family:Arial,Helvetica,sans-serif;line-height:1.65}a{color:#8f241f;text-underline-offset:.2em}a:hover{text-decoration-thickness:2px}a:focus-visible,button:focus-visible{outline:3px solid #efb64e;outline-offset:5px}button{font:inherit;cursor:pointer}.wrap{width:min(1180px,calc(100% - 48px));margin:auto}.skip{position:absolute;top:-90px;padding:12px;background:white;z-index:10}.skip:focus{top:8px}.top{border-bottom:1px solid #d6d0c4;background:#fffdf8}.top .wrap{display:flex;align-items:center;justify-content:space-between;gap:20px;padding-block:18px}.brand{text-decoration:none;color:#14242c;font-weight:800;letter-spacing:.03em}.brand small{display:block;font-size:.73rem;letter-spacing:.13em;font-weight:500}.top nav{display:flex;gap:20px;flex-wrap:wrap;font-size:.87rem}.hero{background:#12242c;color:#fbf7ef;padding:46px 0 54px}.hero-grid{display:grid;grid-template-columns:.95fr 1.05fr;gap:48px;align-items:center}.kicker{font-size:.74rem;font-weight:800;letter-spacing:.16em;text-transform:uppercase;margin:0 0 18px}.badge{display:inline-block;border:1px solid #efb5a6;color:#ffd1c5;border-radius:4px;padding:6px 10px;font-size:.7rem;letter-spacing:.09em;font-weight:800}.hero h1{font-size:clamp(2.65rem,4.4vw,4.65rem);line-height:1.02;letter-spacing:-.045em;margin:22px 0 12px;max-width:12ch}.subhead{color:#ffb8a7;font-family:Georgia,serif;font-size:clamp(1.5rem,2.5vw,2.1rem);line-height:1.2;margin:0 0 27px}.deck{font-size:1.27rem;font-weight:700;line-height:1.45;max-width:32ch}.intro{color:#e1e3dc;font-size:.98rem;max-width:47ch}.actions{display:flex;gap:12px;flex-wrap:wrap;margin:24px 0}.button{display:inline-flex;align-items:center;justify-content:center;min-height:46px;background:#a93127;color:#fff;padding:10px 17px;border-radius:4px;font-weight:700;text-decoration:none;border:1px solid #a93127;font-size:.9rem}.button.secondary{background:transparent;border-color:#87999e;color:inherit}.hero figure{margin:0}.hero picture{display:block;max-width:490px;margin:auto}.hero img{width:100%;height:auto;display:block;border-radius:3px;box-shadow:0 15px 40px #0005}.hero figcaption{max-width:490px;font-size:.75rem;line-height:1.5;color:#d5ddd9;margin:16px auto 0}.disclosure{font-size:.64rem;font-weight:700;line-height:1.5;margin-top:20px;color:#d2d9d5}.hero figcaption a{color:#ffd1c5}.section{padding:60px 0}.section h2{font-family:Georgia,serif;font-weight:500;letter-spacing:-.02em;font-size:clamp(1.9rem,3vw,2.75rem);line-height:1.2;margin:0 0 16px}.section-lead{max-width:74ch;color:#4b585b;margin:0 0 28px}.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}.card{background:#fffdf8;border:1px solid #d9d2c7;border-top:4px solid #a93127;padding:23px;border-radius:5px}.card .kicker{font-size:.62rem;letter-spacing:.1em;line-height:1.5;color:#774037;margin-bottom:12px}.card h3{font-size:1.25rem;line-height:1.25;margin:0 0 16px}.card p{font-size:.91rem}.card a{font-size:.9rem;font-weight:700}.post-section{background:#fffdf8;border-block:1px solid #d9d2c7}.post-layout{display:grid;grid-template-columns:260px 1fr;gap:60px}.post-aside{position:sticky;top:24px;align-self:start}.post-aside p{font-size:.85rem;color:#546167}.post-aside .button{width:100%;margin:0 0 10px}.post-aside .secondary{color:#17252b;border-color:#a8aca7}.status{font-size:.7rem;font-weight:700;line-height:1.5;letter-spacing:.05em;color:#75342b;border-left:3px solid #a93127;padding-left:12px}.post-text{font-size:1.04rem;max-width:72ch;overflow-wrap:anywhere}.post-text p{margin:0 0 1.25em;white-space:pre-line}.post-text p:first-child{font-size:1.4rem;font-weight:800;line-height:1.25}.post-text p:nth-child(2){font-size:.77rem;font-weight:800;letter-spacing:.06em;color:#80352d}.post-link{font-size:.86rem;overflow-wrap:anywhere}.boundary{border-left:5px solid #a93127;padding:25px 30px;background:#ebe5d9;max-width:970px}.boundary h2{font-size:1.65rem}.boundary p{font-size:.9rem}.foot{padding:30px 0;background:#12242c;color:#d2ddd8;font-size:.76rem}.foot .wrap{display:flex;flex-wrap:wrap;gap:16px;justify-content:space-between}.foot a{color:#ffd1c5}#copy-status{font-size:.8rem;min-height:1.4em}@media(max-width:850px){.hero-grid{grid-template-columns:1fr;gap:28px}.hero h1{max-width:none;font-size:3.4rem}.hero .intro{max-width:70ch}.hero picture,.hero figcaption{max-width:540px}.cards{grid-template-columns:1fr}.post-layout{grid-template-columns:1fr;gap:26px}.post-aside{position:static}.post-aside .actions{max-width:500px}.post-aside .button{width:auto}.section{padding:42px 0}}@media(max-width:480px){.wrap{width:calc(100% - 32px)}.top .wrap{align-items:flex-start;gap:12px}.top nav{font-size:.78rem;gap:10px;justify-content:flex-end}.brand{font-size:.87rem}.hero{padding-top:30px}.hero h1{font-size:2.85rem}.hero h1 br{display:none}.hero-grid{gap:22px}.badge{font-size:.64rem}.deck{font-size:1.13rem}.post-text{font-size:1rem}.boundary{padding:20px}.disclosure{font-size:.62rem}.button{font-size:.84rem}}
'''
JS = '''document.addEventListener('DOMContentLoaded',()=>{const b=document.querySelector('[data-copy-url]');if(!b)return;b.addEventListener('click',async()=>{const s=document.getElementById('copy-status');try{const r=await fetch(b.dataset.copyUrl,{cache:'no-cache'});if(!r.ok)throw new Error('fetch');const t=await r.text();await navigator.clipboard.writeText(t.trimEnd());s.textContent=b.dataset.copied;}catch(e){s.textContent=b.dataset.copyfail;}});});\n'''

def sha(data: bytes) -> str:
 return hashlib.sha256(data).hexdigest()
def write(path: str, content: str) -> None:
 target=ROOT/path; target.parent.mkdir(parents=True,exist_ok=True); target.write_text(content,encoding='utf-8')
def jwrite(path: str, value: dict) -> None:
 write(path,json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def url(path: str) -> str:
 return BASE+path

def build_page(lang: str) -> str:
 t=TEXT[lang]; other='es' if lang=='en' else 'en'; route=ROUTES[lang]
 plain=POSTS[lang]+'\n\n'+HOST+url(route)+'\n'
 txt=route+'linkedin-'+lang+'.txt'; write(txt,plain)
 assert len(plain.strip())<3000, (lang,len(plain.strip()))
 paras='\n'.join('<p>'+html.escape(p)+'</p>' for p in POSTS[lang].split('\n\n'))
 cards='\n'.join('<article class="card"><p class="kicker">'+html.escape(k)+'</p><h3>'+html.escape(h)+'</h3><p>'+html.escape(body)+'</p><a href="'+url(SOURCES[src])+'">'+html.escape(link)+' →</a></article>' for k,h,body,src,link in t['cards'])
 return f'''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(t['title'])} · DP 1901/2026 · Por Derecho</title>
<meta name="description" content="{html.escape(t['intro'],quote=True)}">
<link rel="canonical" href="{HOST}{url(route)}">
<link rel="alternate" hreflang="en" href="{HOST}{url(ROUTES['en'])}"><link rel="alternate" hreflang="es" href="{HOST}{url(ROUTES['es'])}">
<meta property="og:type" content="article"><meta property="og:title" content="{html.escape(t['title'],quote=True)}"><meta property="og:description" content="{html.escape(t['label']+' — '+t['deck'],quote=True)}"><meta property="og:url" content="{HOST}{url(route)}"><meta property="og:image" content="{HOST}{url(ASSET+'shame-exits-the-courthouse.jpg')}"><meta property="og:image:width" content="1055"><meta property="og:image:height" content="1491"><meta property="og:image:alt" content="{html.escape(t['alt'],quote=True)}"><meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="{url(CSS_PATH)}"><script src="{url(JS_PATH)}" defer></script>
</head><body class="dp1901-editorial-landing"><a class="skip" href="#content">{'Skip to content' if lang=='en' else 'Saltar al contenido'}</a>
<header class="top"><div class="wrap"><a class="brand" href="{url(lang+'/')}">POR DERECHO<small>PROJECT SUN ROCK</small></a><nav aria-label="{'Page navigation' if lang=='en' else 'Navegación'}"><a href="{url(lang+'/dp-1901-2026/')}">DP 1901/2026</a><a href="{url(ROUTES[other])}" lang="{other}">{t['other']}</a></nav></div></header>
<main id="content"><section class="hero"><div class="wrap hero-grid"><div><p class="kicker">DP 1901/2026 · LAS PALMAS</p><span class="badge">{t['label']}</span><h1>{t['headline']}</h1><p class="subhead">{t['subtitle']}</p><p class="deck">{t['deck']}</p><p class="intro">{t['intro']}</p><div class="actions"><a class="button" href="{url(lang+'/dp-1901-2026/')}">{t['dossier']} →</a><a class="button secondary" href="#linkedin-post">{t['post']}</a></div><p class="disclosure">{t['disclosure']}</p></div>
<figure><a href="{url(ASSET+'shame-exits-the-courthouse.jpg')}" aria-label="{t['full_image']}"><picture><source type="image/avif" srcset="{url(ASSET+'shame-exits-the-courthouse.avif')}"><img src="{url(ASSET+'shame-exits-the-courthouse.jpg')}" width="1055" height="1491" fetchpriority="high" alt="{html.escape(t['alt'],quote=True)}"></picture></a><figcaption>{t['caption']}<br><br>{t['image_note']}</figcaption></figure></div></section>
<section class="section" id="source-record"><div class="wrap"><p class="kicker">{'SOURCE RECORD / EVIDENCE BOUNDARIES' if lang=='en' else 'FUENTES / LÍMITES PROBATORIOS'}</p><h2>{t['sources']}</h2><p class="section-lead">{t['source_intro']}</p><div class="cards">{cards}</div></div></section>
<section class="section post-section" id="linkedin-post"><div class="wrap post-layout"><aside class="post-aside"><p class="status">{t['manual']}</p><h2>{t['post']}</h2><p>{t['post_intro']}</p><div class="actions"><button type="button" class="button" data-copy-url="{url(txt)}" data-copied="{html.escape(t['copied'],quote=True)}" data-copyfail="{html.escape(t['copyfail'],quote=True)}">{t['copy']}</button><a class="button secondary" href="{url(txt)}" download>{t['download']}</a></div><p>{len(plain.strip())} {t['chars']}.</p><p id="copy-status" role="status" aria-live="polite"></p></aside><article class="post-text" aria-label="{t['post']}">{paras}<p class="post-link"><a href="{HOST}{url(route)}">{HOST}{url(route)}</a></p></article></div></section>
<section class="section" id="publication-boundary"><div class="wrap"><div class="boundary"><h2>{t['boundary_title']}</h2><p>{t['boundary']}</p><h3>{t['correction']}</h3><p>{t['correction_text']}</p><a href="{url(lang+'/dp-1901-2026/')}">{t['dossier']} →</a></div></div></section></main>
<footer class="foot"><div class="wrap"><span>{t['footer']}</span><a href="{url(ROUTES[other])}" lang="{other}">{t['other']}</a></div></footer></body></html>
'''

def main() -> None:
 image_specs=[('avif','24d6993e0d546903248c83d5da273d26a91817663c6ea3329d1dd332919f4997',59248),('jpg','839e2353c14fe3f7cef9fbd663b9f73acf6ece2e8f98a10993c66ce6c8e02b55',431615)]
 for ext,digest,size in image_specs:
  data=(ROOT/(ASSET+'shame-exits-the-courthouse.'+ext)).read_bytes()
  assert len(data)==size and sha(data)==digest, ext
 for path in SOURCES.values(): assert (ROOT/path).is_file(),path
 write(CSS_PATH,CSS); write(JS_PATH,JS)
 for lang in ('en','es'): write(ROUTES[lang]+'index.html',build_page(lang))
 preservation=[]
 for lang in ('en','es'):
  path=lang+'/dp-1901-2026/index.html'; original=(ROOT/path).read_text(encoding='utf-8')
  begin='<!-- dp1901-editorial-entry-20260921:start -->'; end='<!-- dp1901-editorial-entry-20260921:end -->'
  clean=re.sub(re.escape(begin)+r'.*?'+re.escape(end)+'\n?', '', original, flags=re.S)
  t=TEXT[lang]
  label='Satire / editorial commentary' if lang=='en' else 'Sátira / comentario editorial'
  boundary='Symbolic illustration, not a factual depiction. The full documentary dossier remains below.' if lang=='en' else 'Ilustración simbólica, no representación factual. El expediente documental íntegro continúa a continuación.'
  block=f'''{begin}
<section id="shame-has-left-the-building" aria-label="{label}" style="margin:24px auto;padding:22px;max-width:1120px;border:1px solid #d8c9b6;border-left:6px solid #a93127;border-radius:8px;background:#fff8ee;color:#17252b;display:flex;gap:24px;align-items:center;flex-wrap:wrap"><a href="{url(ROUTES[lang])}"><img src="{url(ASSET+'shame-exits-the-courthouse.jpg')}" width="155" height="219" loading="lazy" alt="{html.escape(t['alt'],quote=True)}" style="width:155px;height:auto;display:block"></a><div style="flex:1;min-width:220px"><p style="font-size:.75rem;font-weight:bold;letter-spacing:.1em">{label.upper()}</p><h2 style="margin:.25rem 0;font-size:1.7rem">{t['title']}</h2><p>{t['deck']}</p><p style="font-size:.9rem">{boundary}</p><a href="{url(ROUTES[lang])}" style="font-weight:bold">{'Open the illustration, post and sources' if lang=='en' else 'Abrir la ilustración, el texto y las fuentes'} →</a></div></section>
{end}
'''
  m=re.search(r'<main\b[^>]*>',clean); assert m,path
  result=clean[:m.end()]+'\n'+block+clean[m.end():]
  # Compare after removing precisely the newly inserted block and extra newline.
  assert result.replace('\n'+block,'',1)==clean
  write(path,result)
  preservation.append({'path':path,'previous_sha256':sha(clean.encode()),'method':'one additive entry block after main opener; original text retained exactly','result':'PASS'})
 digital_path='data/digital-media-asset-register-v1.json'; dp=ROOT/digital_path
 digital=json.loads(dp.read_text(encoding='utf-8'))
 existing=[a for a in digital['logical_assets'] if a.get('satire_compliance_id')==PID]
 if existing:
  ids={a['language']:a['reference'] for a in existing}
 else:
  nums=[int(m.group(1)) for a in digital['logical_assets'] if (m:=re.fullmatch(r'PD-DMA-(\d+)',a.get('reference','')))]
  n=max(nums)+1; ids={'en':f'PD-DMA-{n:04d}','es':f'PD-DMA-{n+1:04d}'}
 digital['logical_assets']=[a for a in digital['logical_assets'] if a.get('satire_compliance_id')!=PID]
 digital['families']=[f for f in digital['families'] if f.get('family_id')!=FAMILY]
 digital['files']=[f for f in digital['files'] if f.get('logical_asset') not in ids.values()]
 source_id='SRC-DP1901-SHAME-USER-APPROVED-20260921'
 digital['source_claims']=[s for s in digital['source_claims'] if s.get('id')!=source_id]
 digital['source_claims'].append({'id':source_id,'source_type':'USER_AUTHORIZED_AI_GENERATED_EDITORIAL_ILLUSTRATION','claim':'User requested public use of the generated Shame/Justice metaphor with English and Spanish landing text; not a photograph, official endorsement or evidence of literal conduct.','control':'publication-manifests/dp1901-shame-landing-20260921.json'})
 digital['families'].append({'family_id':FAMILY,'title':'DP1901: Shame expelled / Justice buried','scope':'Editorial satire with bilingual landing pages; generic figures, fictional setting and inscriptions. English-title raster shared between both language pages.','current_primary_en':ids['en'],'current_primary_es':ids['es'],'mandatory_boundary':'No physical burial, documentary destruction, official authorship, actual likeness, criminal finding or coordination is established by this metaphor.'})
 for lang in ('en','es'):
  ref=ids[lang]; path=ROUTES[lang]+'index.html'; data=(ROOT/path).read_bytes()
  digital['logical_assets'].append({'reference':ref,'family_id':FAMILY,'title':TEXT[lang]['title'],'language':lang,'edition':'ENGLISH_FIRST_MANUAL_SOCIAL' if lang=='en' else 'SPANISH_LANDING_AND_LATER_MANUAL_SOCIAL','publication_status':'PREPARED_PUBLICATION_CANDIDATE','satire_compliance_id':PID,'web_file':ref+'-PAGE^','sources':[source_id]})
  digital['files'].append({'reference':ref+'-PAGE^','logical_asset':ref,'role':'PUBLIC_WEB_PRESENTATION','repository_path':path,'public_url':'/'+ROUTES[lang],'mime':'text/html','bytes':len(data),'sha256':sha(data),'repository_mirror':True,'publication_status':'PREPARED_PUBLICATION_CANDIDATE'})
 for ext,digest,size in image_specs:
  digital['files'].append({'reference':ids['en']+'-'+ext.upper()+'^','logical_asset':ids['en'],'role':'COMPRESSED_WEB_RENDITION','repository_path':ASSET+'shame-exits-the-courthouse.'+ext,'public_url':'/'+ASSET+'shame-exits-the-courthouse.'+ext,'mime':'image/avif' if ext=='avif' else 'image/jpeg','width_px':1055,'height_px':1491,'bytes':size,'sha256':digest,'repository_mirror':True,'publication_status':'PREPARED_PUBLICATION_CANDIDATE','source_original_sha256':'ca301b92c670abcaa691bbd5b569dfb971034595c300238369e265f861fe947d','boundary':'Compression derivative; not original PNG byte identity; no crop, resize or new composition.'})
 jwrite(digital_path,digital)
 compliance_path='data/satire-publication-compliance-v1.json'; compliance=json.loads((ROOT/compliance_path).read_text(encoding='utf-8'))
 compliance['publications']=[p for p in compliance['publications'] if p.get('publication_id')!=PID]
 risk={
 'HONOUR_REPUTATION_PROFESSIONAL_PRESTIGE':'Public-interest criticism addresses disputed procedure; adverse outcome and open evidence remain visible. No finding of guilt or guarantee of zero legal risk.',
 'FALSE_ENDORSEMENT_AUTHORSHIP_QUOTATION_MANDATE_OR_ROLE':'Visible disclosure identifies fictional institutional figures and invented wall inscriptions. No official quotation, endorsement or authorship claimed.',
 'IMAGE_LIKENESS_PERSONALITY_RIGHTS':'Generic generated judge/prosecutor archetypes, not identified portraits; no real person identified from the image.',
 'IMPLIED_DISHONESTY_CONFLICT_CORRUPTION_ILLEGALITY_OR_CRIMINALITY':'Burial is an attributed editorial metaphor, not proof of physical destruction, knowledge, improper coordination or criminal responsibility; source record and contrary ruling linked.',
 'LOGO_TRADE_DRESS_OR_REAL_ADVERTISING_CONFUSION':'Generated building emblems and inscriptions are expressly fictional/contextual, not a court communication, photograph or advertisement.',
 'PERSONAL_DATA_NECESSITY_AND_PROPORTIONALITY':'No private correspondence, signatures, addresses, personal identifiers or native private pleadings published.',
 'CORRECTION_REPLY_TAKEDOWN_AND_NARROW_REVERT_PATH':'Visible correction/reply route through existing dossier; preserve source and correction history; use narrow ordinary corrective/revert PR if needed.'}
 compliance['publications'].append({'publication_id':PID,'family_id':FAMILY,'title':'DP1901 Shame/Justice editorial landing pages','logical_assets':[ids['en'],ids['es']],'public_surfaces':[{'path':ROUTES[l]+'index.html','language':l,'required_disclosure':TEXT[l]['disclosure']} for l in ('en','es')],'entry_points':[l+'/dp-1901-2026/index.html#shame-has-left-the-building' for l in ('en','es')],'entry_point_scope':'Navigation preview with visible symbolic-image notice; full editorial disclosure and record on the registered linked landing page. Existing dossier names and content remain unchanged.','named_people':[],'factual_role_and_satirical_function_separated':True,'source_refs':list(SOURCES.values())+[source_id],'evidence_states_present':['DOCUMENTED_FACT','OFFICIAL_OUTCOME','ATTRIBUTED_ALLEGATION','RHETORICAL_METAPHOR_OR_DOUBLE_MEANING','CONTRARY_RECORD_OR_LAWFUL_ALTERNATIVE','OPEN_OR_UNVERIFIED'],'opposing_counsel_risk_review':risk,'manual_social_only':True,'posting_order':['en','es'],'social_posted':False,'social_scheduled':False,'spanish_raster_translation':False})
 jwrite(compliance_path,compliance)
 paths=[ROUTES[l]+f for l in ('en','es') for f in ('index.html','linkedin-'+l+'.txt')]+[CSS_PATH,JS_PATH]+[ASSET+'shame-exits-the-courthouse.'+x[0] for x in image_specs]+[l+'/dp-1901-2026/index.html' for l in ('en','es')]+[digital_path,compliance_path]
 manifest={'schema':'por-derecho.publication-state.v1','publication_id':'PD-DP1901-SHAME-LANDING-20260921','control_date':'2026-09-21','current_state':'PREPARED','status':'CANDIDATE_NOT_DEPLOYMENT_ATTESTATION','owner':'DP1901 bilingual editorial landing worker','expected_routes':[url(ROUTES[l]) for l in ('en','es')]+[url(l+'/dp-1901-2026/') for l in ('en','es')],'source_refs':list(SOURCES.values()),'logical_assets':ids,'manual_social':{'posting_order':['en','es'],'posted':False,'scheduled':False,'cambiante_used':False,'publication_on_website_is_not_social_posting':True},'native_png_sha256':'ca301b92c670abcaa691bbd5b569dfb971034595c300238369e265f861fe947d','native_png_in_repository':False,'web_image_versions':['avif','jpeg'],'spanish_page_uses_original_english_title_image_with_visible_translation_note':True,'dossier_preservation':preservation,'validation':{'source_review':'source-limited editorial text; allegation, adverse order and production limits retained','browser_and_repository_tests':'See exact candidate PR/Actions results; not inferred by this manifest'},'files':[{'path':p,'bytes':len((ROOT/p).read_bytes()),'sha256':sha((ROOT/p).read_bytes())} for p in paths],'boundaries':['No literal burial or destruction claim','No named official portrait attribution','No private original publication','No filing, service, legal signature or social publication','No scratch transfer workflow or temporary signed URL included']}
 jwrite('publication-manifests/dp1901-shame-landing-20260921.json',manifest)
 print(json.dumps({'status':'BUILT','logical_assets':ids,'files':paths+['publication-manifests/dp1901-shame-landing-20260921.json'],'post_characters':{l:len((POSTS[l]+'\n\n'+HOST+url(ROUTES[l])).strip()) for l in POSTS},'dossier_preservation':'PASS'},ensure_ascii=False))

if __name__=='__main__': main()
