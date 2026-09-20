#!/usr/bin/env python3
"""Build the authorized bilingual addition before merge; never writes a remote ref."""
from pathlib import Path
import json, hashlib, html, re
ROOT = Path.cwd()
PUB = 'PD-SAT-DP1901-SHAME-20260921'
IMG = 'assets/visuals/dp1901-shame-20260921/shame-exits-the-courthouse.png'
DATA = 'assets/data/dp1901-shame-linkedin-20260921.json'
CSS = 'assets/dp1901-shame-linkedin-20260921.css'
SOURCE = 'SRC-DP1901-SHAME-GENERATED-20260920'
BASE = 'https://sbu001monterecco.github.io/por-derecho/'
EVID = ['evidence/judicial/dp-1901-2026/PROCEDURAL_IDENTITY_SOURCE_CLOSURE_18SEP2026.md', 'evidence/judicial/dp-1901-2026/full-text/auto-14sep2026-public-transcription.md', 'data/three-track-full-digitisation-20260904.json']
D = json.loads((ROOT / DATA).read_text())
raw = (ROOT / IMG).read_bytes()
assert len(raw) == D['image']['bytes']
assert hashlib.sha256(raw).hexdigest() == D['image']['sha256']
paths = []
for lang in ('en', 'es'):
    p = ROOT / f'{lang}/dp-1901-2026/index.html'
    old = p.read_text()
    assert 'id="shame-has-left-the-building"' not in old, 'Refuse to duplicate or overwrite an existing landing section.'
    es = lang == 'es'
    other = 'en' if es else 'es'
    text = D['posts'][lang]
    parts = text.split('\n\n')
    lines = parts[0].splitlines()
    disclosure = ('CARICATURA / REPRESENTACIÓN SATÍRICA — NO ES UN ANUNCIO REAL' if es else 'SATIRICAL / CARICATURE REPRESENTATION — NOT A REAL ADVERTISEMENT')
    caption = ('Imagen original generada con IA. Sátira: figuras, arquitectura e inscripciones son una representación artística, no una fotografía ni una reconstrucción de hechos observados. Las figuras son genéricas; no identifican a un juez o fiscal concreto. No acredita destrucción documental, intención, coordinación ni responsabilidad penal. Se conserva la imagen original con su titular en inglés; el texto completo en español figura al lado.' if es else 'Original AI-generated image. Satire: the figures, architecture and inscriptions are artistic representations, not a photograph or reconstruction of observed events. The figures are generic, not portraits identifying a particular judge or prosecutor. It establishes no destruction of records, intent, coordination or criminal responsibility.')
    alt = ('Sátira: un juez y una fiscal genéricos expulsan a la figura de la Vergüenza; sus sombras entierran a la Justicia, las carpetas Ref. 21 y Ref. 24 y principios jurídicos. No representa hechos físicos.' if es else 'Satire: a generic judge and prosecutor expel the personification of Shame; their shadows bury Justice, the separate Ref. 21 and Ref. 24 folders, and legal principles. Not a depiction of physical events.')
    paras = []
    for x in parts[2:]:
        cls = 'pd-shame-question' if x.startswith(('What happened', '¿Qué ocurrió')) else ('pd-shame-closing' if x.startswith(('A file can', 'Un expediente puede')) else '')
        paras.append('<p' + (f' class="{cls}"' if cls else '') + '>' + html.escape(x).replace('\n', '<br>') + '</p>')
    links = [(BASE + EVID[0], 'Identidad y trazabilidad de junio/julio' if es else 'June/July identity and routing record'), (BASE + EVID[1], 'Texto de la resolución adversa de 14 de septiembre' if es else 'Text of the adverse 14 September order'), (BASE + f'{lang}/' + ('dp-1901-plataforma-recuperacion/' if es else 'dp-1901-platform-recovery/'), 'Contenido de las denuncias y recuperación' if es else 'Complaint substance and recovery'), (BASE + EVID[2], 'Fuentes de los tres carriles' if es else 'Three-track source inventory')]
    citations = ''.join(f'<a href="{u}"><span>{i:02d}</span>{t} →</a>' for i, (u, t) in enumerate(links, 1))
    section = f'''
<!-- dp1901-shame-landing-20260921:start -->
<section class="pd-shame-landing" id="shame-has-left-the-building" aria-labelledby="pd-shame-title" data-satire-publication="{PUB}">
<div class="pd-shame-shell">
<p class="pd-shame-kicker">POR DERECHO / PROJECT SUN ROCK · DP 1901/2026</p>
<div class="pd-shame-heading"><div><p class="pd-shame-label">{'SÁTIRA · METÁFORA EDITORIAL' if es else 'SATIRE · EDITORIAL METAPHOR'}</p><h2 id="pd-shame-title">{html.escape(lines[0])}</h2><p class="pd-shame-subtitle">{html.escape(lines[1])}</p></div><a class="pd-shame-language" lang="{other}" hreflang="{other}" href="../../{other}/dp-1901-2026/#shame-has-left-the-building">{'English version' if es else 'Versión española'} ↗</a></div>
<p class="pd-shame-disclosure">{disclosure}</p>
<p class="pd-shame-context">{'Texto de Gil Marer preparado el 20 de septiembre de 2026. Opinión atribuida; las resoluciones adversas y las cuestiones pendientes permanecen visibles en las fuentes y en el expediente que sigue.' if es else 'Text by Gil Marer prepared on 20 September 2026. Attributed opinion; adverse decisions and open questions remain visible in the sources and the documentary dossier below.'}</p>
<div class="pd-shame-layout"><figure><a href="../../{IMG}" aria-label="{'Abrir la imagen completa' if es else 'Open the full image'}"><img src="../../{IMG}" width="1055" height="1491" alt="{html.escape(alt, quote=True)}" fetchpriority="high" decoding="async"></a><figcaption>{caption}</figcaption></figure>
<article class="pd-shame-post" aria-label="{'Texto íntegro de la publicación para LinkedIn' if es else 'Full LinkedIn post text'}">{''.join(paras)}</article></div>
<div class="pd-shame-evidence" id="shame-evidence"><h3>{'Fuentes detrás de la metáfora' if es else 'The record behind the metaphor'}</h3><p>{'La sátira no es prueba primaria. La resolución judicial se cita como resultado adverso, no como aceptación de las alegaciones. La Ref. 22 / DP 1956 mantiene su tramitación separada; no se representa como archivada por el mismo Auto de DP 1901.' if es else 'The satire is not primary evidence. The court order is cited as an adverse outcome, not acceptance of the allegations. Ref. 22 / DP 1956 remains a separate track; it is not depicted as dismissed by the same DP 1901 order.'}</p><nav aria-label="{'Fuentes de la publicación' if es else 'Post sources'}">{citations}</nav></div>
<p class="pd-shame-jump"><a href="#pd-shame-existing-dossier">{'Continuar al expediente documental completo ↓' if es else 'Continue to the complete documentary dossier ↓'}</a></p>
</div></section><div id="pd-shame-existing-dossier"></div>
<!-- dp1901-shame-landing-20260921:end -->
'''
    match = re.search(r'<main\b[^>]*>', old)
    assert match
    new = old[:match.end()] + section + old[match.end():]
    # Source preservation: removing exactly this addition reproduces the original body.
    assert new.replace(section, '', 1) == old
    head = f'\n<link rel="stylesheet" href="../../{CSS}">\n<meta property="og:image" content="{BASE + IMG}">\n<meta property="og:image:width" content="1055">\n<meta property="og:image:height" content="1491">\n<meta property="og:image:alt" content="{html.escape(alt, quote=True)}">\n<meta name="twitter:card" content="summary_large_image">\n<meta name="twitter:image" content="{BASE + IMG}">\n'
    # No earlier social-image tag is silently overwritten. An existing tag needs explicit reconciliation.
    assert not re.search(r'<meta\b[^>]*(?:property|name)=["\'](?:og:image|twitter:image)["\']', old, re.I)
    new = new.replace('</head>', head + '</head>', 1)
    p.write_text(new)
    paths.append(str(p.relative_to(ROOT)))
    q = ROOT / f'assets/social/dp1901-shame-{lang}-20260921.txt'
    q.parent.mkdir(parents=True, exist_ok=True)
    q.write_text(text + '\n\n' + BASE + f'{lang}/dp-1901-2026/#shame-has-left-the-building\n')

comp = ROOT / 'data/satire-publication-compliance-v1.json'
reg = json.loads(comp.read_text())
assert all(p['publication_id'] != PUB for p in reg['publications'])
people = json.loads((ROOT / 'assets/data/matter-identity-registry-v1.people.json').read_text())
alltext = '\n'.join((ROOT / p).read_text() for p in paths)
named = []
for rec in people.get('records', []):
    name, ident = rec.get('name'), rec.get('id')
    if name and ident and name in alltext:
        named.append({'display_name': name, 'naming_form': 'FULL_CANONICAL_CARET_CONFIRMED', 'identity_state': 'CARET_CONFIRMED', 'caepr_id': ident, 'source_refs': paths, 'factual_role': {'label': 'Named author or person in the pre-existing source-led dossier. Not identified as a figure in this image. No existing factual role is changed.', 'date_or_period': 'Dated source material in the unchanged documentary dossier; editorial addition prepared 20 September 2026', 'source_refs': paths}, 'affiliation': {'state': 'NOT_APPLICABLE'}, 'satirical_function': {'state': 'NONE', 'label': 'No person-specific likeness or satirical attribution is added.'}})
risk = {'HONOUR_REPUTATION_PROFESSIONAL_PRESTIGE': 'Institutional satire with generic figures; actual adverse outcome retained and criticism expressly attributed to the complainant. No guilt finding.', 'FALSE_ENDORSEMENT_AUTHORSHIP_QUOTATION_MANDATE_OR_ROLE': 'No fabricated official quotation. Inscription and architecture are identified as artistic, not real features or institutional endorsements.', 'IMAGE_LIKENESS_PERSONALITY_RIGHTS': 'User-generated symbolic figures; no purported identification of a real judge or prosecutor.', 'IMPLIED_DISHONESTY_CONFLICT_CORRUPTION_ILLEGALITY_OR_CRIMINALITY': 'Literal destruction, coordinated misconduct and culpability are not asserted. The full post retains open evidence and contrary judicial assessment.', 'LOGO_TRADE_DRESS_OR_REAL_ADVERTISING_CONFUSION': 'Image includes stylised institutional symbols. Visible canonical non-advertisement disclosure and no-official-endorsement clarification.', 'PERSONAL_DATA_NECESSITY_AND_PROPORTIONALITY': 'Only the user-approved image, public post and existing public evidence links. No private source records or new private personal data.', 'CORRECTION_REPLY_TAKEDOWN_AND_NARROW_REVERT_PATH': 'Additive changes and exact asset can be corrected by normal PR without removing the previous dossier. No assurance of zero legal risk.'}
# Allocate the next free logical media identity from the actual branch register, not chat memory.
digital_path = ROOT / 'data/digital-media-asset-register-v1.json'
digital = json.loads(digital_path.read_text())
nums = [int(x['reference'].split('-')[-1]) for x in digital.get('logical_assets', []) if re.fullmatch(r'PD-DMA-\d+', x.get('reference', ''))]
logical = f'PD-DMA-{max(nums, default=0) + 1:04d}'
family = 'PD-DMA-FAM-DP1901-SHAME-001'
assert not any(x.get('family_id') == family for x in digital.get('families', []))
digital['source_claims'].append({'id': SOURCE, 'source_type': 'USER_APPROVED_AI_GENERATED_EDITORIAL_SATIRE', 'claim': 'Exact image generated and approved for the bilingual DP1901 public landing. It does not depict observed physical acts or identify real officials.', 'control': DATA})
digital['families'].append({'family_id': family, 'title': 'Shame expelled / Justice buried — DP1901 editorial satire', 'scope': 'Original editorial satire and bilingual source-linked public post; no finding of culpability.', 'current_primary_en': logical, 'current_primary_es': logical})
digital['logical_assets'].append({'reference': logical, 'family_id': family, 'title': 'Shame has left the building', 'language': 'en', 'edition': 'EXACT_ORIGINAL_WITH_BILINGUAL_PAGE_CONTEXT', 'publication_status': 'PREPARED_FOR_PUBLICATION', 'satire_compliance_id': PUB, 'web_file': logical + '-EN-PAGE^', 'image_file': logical + '-PNG^', 'sources': [SOURCE]})
for lang, path in zip(('en', 'es'), paths):
    b = (ROOT / path).read_bytes()
    digital['files'].append({'reference': logical + '-' + lang.upper() + '-PAGE^', 'logical_asset': logical, 'role': 'PUBLIC_CONTEXT_PAGE', 'repository_path': path, 'public_url': BASE + path.removesuffix('index.html'), 'mime': 'text/html', 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest(), 'repository_mirror': True, 'publication_status': 'PREPARED_FOR_PUBLICATION'})
digital['files'].append({'reference': logical + '-PNG^', 'logical_asset': logical, 'role': 'FULL_RESOLUTION_EDITORIAL_ORIGINAL', 'repository_path': IMG, 'public_url': BASE + IMG, 'mime': 'image/png', 'width_px': 1055, 'height_px': 1491, 'bytes': len(raw), 'sha256': D['image']['sha256'], 'repository_mirror': True, 'publication_status': 'PREPARED_FOR_PUBLICATION', 'intended_channels': ['LinkedIn', 'bilingual landing page']})
digital_path.write_text(json.dumps(digital, ensure_ascii=False, indent=2) + '\n')
reg['publications'].append({'publication_id': PUB, 'family_id': family, 'title': 'Shame has left the building / La vergüenza ha salido del edificio', 'logical_assets': [logical], 'public_surfaces': [{'path': p, 'language': p[:2], 'required_disclosure': ('CARICATURA / REPRESENTACIÓN SATÍRICA — NO ES UN ANUNCIO REAL' if p.startswith('es') else 'SATIRICAL / CARICATURE REPRESENTATION — NOT A REAL ADVERTISEMENT')} for p in paths], 'named_people': named, 'factual_role_and_satirical_function_separated': True, 'source_refs': EVID + [DATA], 'opposing_counsel_risk_review': risk})
comp.write_text(json.dumps(reg, ensure_ascii=False, indent=2) + '\n')
record = ROOT / 'archive/DP1901_LINKEDIN_LANDING_EN_ES_20260921.md'
record.write_text('''# DP1901 bilingual image and full LinkedIn post landing

Authorized scope: add the exact generated image, complete English post and faithful Spanish translation at `#shame-has-left-the-building` on the existing EN/ES DP1901 pages. Previous body content is preserved byte-for-byte around the addition. The original bitmap is not cropped, redrawn or translated; Spanish heading, full post, caption, alternative text and disclosures are translated. No procedural filing status is changed by this addition.

Exact PNG:1055x1491,2590908bytes,SHA256 `ca301b92c670abcaa691bbd5b569dfb971034595c300238369e265f861fe947d`. The image is satire, not a real building photograph or a reconstruction of observed conduct. Building inscriptions are artistic; generic figures do not identify actual officials. Allegations, contrary judicial assessment and missing-source limitations are retained in the complete post and source links.

Both Cambiante drafts contain the image and remain pending approval, without scheduling or LinkedIn publication. Website publication is separate. Native private legal files are not part of this release.

The isolated preparation job copies a public asset and materializes deterministic page changes before review. It neither writes main nor deploys. No production validator or deployment setting is altered. The preparation workflow must be excluded from the publication tree; the public source-data/CSS/image/builder, two pages and controls remain.

This record is not a merge or live-deployment certificate. The PR, exact head/merge SHA, deployment and affected-route readback determine completion.

## Español

Se incorpora la imagen original, el texto inglés completo y su traducción fiel al español, conservando el expediente anterior. Se mantienen visibles las alegaciones, la resolución adversa y los extremos documentales pendientes. La imagen original lleva titular en inglés; no se afirma haber traducido el bitmap. La publicación web no equivale a publicación en LinkedIn, presentación judicial ni declaración de culpabilidad.
''')
print(json.dumps({'updated_routes': paths, 'logical_asset': logical, 'declared_existing_names': len(named), 'image_sha256': D['image']['sha256'], 'post_lengths': {k: len(v) for k, v in D['posts'].items()}}, indent=2))
