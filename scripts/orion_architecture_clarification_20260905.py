#!/usr/bin/env python3
"""Scoped, deterministic Orion framing correction; never auto-repairs main.

--apply is integration preparation only. --check and --live are read-only.
Existing evidence, allegations, counter-records and source identifiers survive.
"""
from __future__ import annotations
import argparse
import collections
import hashlib
import json
import re
import subprocess
import sys
import time
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTROL = 'PD-ORION-ARCH-20260905-01'
MARKER = 'orion-architecture-clarification-20260905'
BASE = 'e482e29325091bcc32af3fd2b2624335c6699e19'
RECORD = '.github/evidence-intelligence/records/PD-SP-EI-20260905-02-ORION-RENTAL-SOCIMI-GOVERNANCE.md'
GRAPH = 'assets/data/orion-rental-socimi-governance-20260905.json'
ROUTES = {
    'en': ('en/orion-ricpe-platform-continuity/index.html', 'en/orion-rental-socimi/index.html'),
    'es': ('es/orion-ricpe-continuidad/index.html', 'es/orion-rental-socimi/index.html'),
}
COPY = {
'en': {
    'title_old': 'Orion Rental SOCIMI · RICPE branch and FMMM trajectory',
    'title': 'Orion Rental SOCIMI · distinct but interconnected branches',
    'desc_old': 'RICPE→Orion corporate and finance facts; separation from the Sun Park/MYND funding chain and a limited analysis of FMMM’s professional trajectory from the Community.',
    'desc': 'Distinct but interconnected Sun Park/MYND and Orion branches: documented RICPE, AGM, Pamalexsha and Acosta Matos connections; separate proof of asset flows and actor-specific responsibility.',
    'brand_old': 'RICPE → Orion · separate branch',
    'brand': 'Sun Park / Orion · connected branches',
    'eyebrow_old': 'RICPE → ORION / AGM · NO SUN PARK → ORION WITHOUT A SPECIFIC BRIDGE',
    'eyebrow': 'DISTINCT BRANCHES · DOCUMENTED CONNECTIONS · NO AUTOMATIC ASSET FLOW OR LIABILITY',
    'h1_old': 'Orion is a later branch of the RICPE platform, not Sun Park’s automatic next financial life.',
    'h1': 'Sun Park/MYND and Orion: distinct but interconnected branches.',
    'lead_old': 'The RICPE→Orion corporate and finance facts are documented. For Sun Park, the analysis is presently limited to FMMM’s trajectory and any specific patrimonial bridge that may later be proved.',
    'lead': 'The analysis preserves distinct legal persons, assets and transactions within one connected inquiry. RICPE, AGM, Pamalexsha and Acosta Matos links are documented; any transfer of Sun Park/MYND/LPB/Matkator assets or value into Orion must be traced separately. FMMM’s trajectory is one important inquiry, not the exclusive connection.',
    'notice_old': '<div class="correction"><strong>ARCHITECTURE CORRECTION</strong><p>The broad line “Sun Park/Pamalexsha/CAM → RICPE → AGM → Orion” is replaced by two branches: a Sun Park/MYND branch of title, finance, support and operation; and an independent Orion branch of founder, capital, finance, management and market admission.</p></div>',
    'notice': '<strong>ARCHITECTURE CLARIFICATION — DISTINCT BRANCHES, DOCUMENTED CONNECTIONS</strong><p>The analysis distinguishes two interconnected branches: the <strong>Sun Park/MYND asset, title, financing, public-support and operating branch</strong>, and the <strong>later Orion formation, capital, financing, management, related-party and market-admission branch</strong>.</p><p>They concern distinct legal persons, assets and transactions. They must not be presented as unconnected: the record documents RICPE’s founding and financing relationship with Orion, AGM’s management role, and ownership and governance connections involving Pamalexsha and the Acosta Matos perimeter.</p><p>These connections belong within the unitary analysis. They do not, without further evidence, establish that Sun Park assets, income, financing or public support flowed into Orion. Any such transfer, guarantee, collateral use or other economic benefit must be traced specifically.</p><p>Orion’s incorporation in June 2023 prevents attributing earlier Sun Park acts to Orion itself. It does not erase the earlier roles of individuals or entities subsequently connected to it. Any allegation concerning concealment, conflicts, misleading disclosure or enabling conduct must be tested against each actor’s knowledge, duties, decisions and conduct, not inferred automatically from association.</p>',
    'fmmm_old': 'The only Sun Park question to develop here: FMMM',
    'fmmm': 'Actor-specific inquiry: FMMM within the connected branches',
    'intro_old': 'The inquiry should not construct a general Orion theory from personal association. It must reconstruct the specific professional trajectory:',
    'intro': 'FMMM’s professional trajectory remains a specific inquiry within the broader documented RICPE, AGM, Pamalexsha and Acosta Matos connections. Each actor’s mandate, knowledge, duties and conduct must be reconstructed separately; personal association alone does not prove coordination or liability:',
    'bridge_title': 'Documented connections, with a separate test for asset or value flows',
    'bridge': '<div class="grid"><article class="card"><h3>Pamalexsha / AGM</h3><p>The controlled audited related-party record documents FMMM’s and the Cogolludo interests in Pamalexsha and Pamalexsha’s interest in AGM. These are ownership connections, not proof of a direct Orion office for every participant or of shared intent.</p></article><article class="card"><h3>Acosta Matos / AGM / Orion</h3><p>The same record documents JDAM’s AGM interest, Grupo Patrimonial Acosta Matos’s Orion holding and disclosed Acosta-related construction and service transactions. These economic and governance links are not findings of misconduct.</p></article><article class="card"><h3>RICPE / Orion / AGM</h3><p>RICPE’s founding and financing relationship with Orion and AGM’s management role are documented. Each connection must be labelled by its function and date, rather than presented as a single ownership or money-flow chain.</p></article></div><p><strong>Two different proof questions:</strong> documented corporate and economic connections do not, by themselves, trace identifiable Sun Park assets, proceeds, fees, guarantees, collateral or other value into Orion. The latter remains an open, transaction-specific inquiry. Disclosure, conflicts and any alleged enabling conduct also require actor-specific evidence.</p>',
    'dossier_link': 'Open the audited Orion governance and related-party dossier',
    'backlink': 'Read the clarified two-branch architecture',
    'panel': 'Sun Park/MYND and Orion are distinct but interconnected branches. The documented RICPE, AGM, Pamalexsha and Acosta Matos links remain within one analysis; neither a Sun Park-to-Orion asset flow nor any actor’s knowledge or liability follows automatically. The FMMM inquiry is preserved but is not the exclusive connection.',
    'reply': 'Corrections, contrary evidence and exculpatory records remain welcome. Silence is not admission.',
},
'es': {
    'title_old': 'Orion Rental SOCIMI · rama RICPE y trayectoria de FMMM',
    'title': 'Orion Rental SOCIMI · ramas distintas pero interconectadas',
    'desc_old': 'Hechos corporativos y financieros RICPE→Orion; separación de la cadena Sun Park/MYND y análisis limitado de la trayectoria profesional de FMMM desde la Comunidad.',
    'desc': 'Ramas Sun Park/MYND y Orion distintas pero interconectadas: vínculos documentados RICPE, AGM, Pamalexsha y Acosta Matos; prueba separada de flujos patrimoniales y responsabilidad individual.',
    'brand_old': 'RICPE → Orion · rama separada',
    'brand': 'Sun Park / Orion · ramas interconectadas',
    'eyebrow_old': 'RICPE → ORION / AGM · NO SUN PARK → ORION SIN PUENTE ESPECÍFICO',
    'eyebrow': 'RAMAS DISTINTAS · VÍNCULOS DOCUMENTADOS · SIN FLUJO PATRIMONIAL NI RESPONSABILIDAD AUTOMÁTICOS',
    'h1_old': 'Orion es una rama posterior de la plataforma RICPE, no la siguiente vida financiera automática de Sun Park.',
    'h1': 'Sun Park/MYND y Orion: ramas distintas pero interconectadas.',
    'lead_old': 'Los hechos corporativos y financieros RICPE→Orion están documentados. Para Sun Park, el análisis se limita actualmente a la trayectoria de FMMM y a cualquier puente patrimonial específico que llegue a probarse.',
    'lead': 'El análisis mantiene separadas las personas jurídicas, los activos y las operaciones dentro de una investigación conectada. Los vínculos RICPE, AGM, Pamalexsha y Acosta Matos están documentados; cualquier transferencia de activos o valor Sun Park/MYND/LPB/Matkator hacia Orion debe rastrearse por separado. La trayectoria de FMMM es una cuestión importante, no el vínculo exclusivo.',
    'notice_old': '<div class="correction"><strong>CORRECCIÓN DE ARQUITECTURA</strong><p>Se sustituye la línea amplia “Sun Park/Pamalexsha/CAM → RICPE → AGM → Orion” por dos ramas: una rama Sun Park/MYND de título, financiación, ayuda y explotación; y una rama Orion independiente de fundador, capital, financiación, gestión y admisión de mercado.</p></div>',
    'notice': '<strong>ACLARACIÓN DE ARQUITECTURA — RAMAS DISTINTAS, VÍNCULOS DOCUMENTADOS</strong><p>El análisis distingue dos ramas interconectadas: la <strong>rama Sun Park/MYND de activos, titularidad, financiación, apoyo público y explotación</strong>, y la <strong>rama posterior Orion de constitución, capital, financiación, gestión, operaciones vinculadas y admisión a mercado</strong>.</p><p>Se refieren a personas jurídicas, activos y operaciones distintos. No deben presentarse como desconectadas: el expediente documenta la relación fundacional y financiera de RICPE con Orion, la función gestora de AGM y los vínculos de propiedad y gobierno relacionados con Pamalexsha y el perímetro Acosta Matos.</p><p>Estos vínculos forman parte del análisis unitario. Sin prueba adicional, no acreditan que activos, ingresos, financiación o apoyo público de Sun Park fluyeran hacia Orion. Cualquier transferencia, garantía, uso de activos como garantía u otro beneficio económico debe rastrearse específicamente.</p><p>La constitución de Orion en junio de 2023 impide atribuir a la propia Orion actos anteriores de Sun Park. No borra las funciones anteriores de las personas o entidades posteriormente vinculadas a ella. Toda alegación de ocultación, conflictos, información engañosa o conducta facilitadora debe contrastarse con el conocimiento, los deberes, las decisiones y la conducta de cada actor, sin inferirse automáticamente por asociación.</p>',
    'fmmm_old': 'La única cuestión Sun Park que debe desarrollarse aquí: FMMM',
    'fmmm': 'Investigación individual: FMMM dentro de las ramas interconectadas',
    'intro_old': 'La investigación no debe construir una teoría general de Orion a partir de una asociación personal. Debe reconstruir la trayectoria profesional concreta:',
    'intro': 'La trayectoria profesional de FMMM sigue siendo una cuestión específica dentro de los vínculos más amplios documentados RICPE, AGM, Pamalexsha y Acosta Matos. Deben reconstruirse por separado el mandato, el conocimiento, los deberes y la conducta de cada actor; la asociación personal no prueba por sí sola coordinación ni responsabilidad:',
    'bridge_title': 'Vínculos documentados, con prueba separada de flujos de activos o valor',
    'bridge': '<div class="grid"><article class="card"><h3>Pamalexsha / AGM</h3><p>El registro controlado de partes vinculadas auditadas documenta las participaciones de FMMM y de los intereses Cogolludo en Pamalexsha, y la participación de Pamalexsha en AGM. Son vínculos de propiedad, no prueba de cargo directo en Orion para cada participante ni de intención compartida.</p></article><article class="card"><h3>Acosta Matos / AGM / Orion</h3><p>El mismo registro documenta la participación de JDAM en AGM, la participación de Grupo Patrimonial Acosta Matos en Orion y las operaciones declaradas de construcción y servicios vinculadas a Acosta. Estos vínculos económicos y de gobierno no constituyen hallazgos de irregularidad.</p></article><article class="card"><h3>RICPE / Orion / AGM</h3><p>La relación fundacional y financiera de RICPE con Orion y la función gestora de AGM están documentadas. Cada vínculo debe identificarse por su función y fecha, no presentarse como una única cadena de propiedad o flujo monetario.</p></article></div><p><strong>Dos cuestiones probatorias diferentes:</strong> los vínculos societarios y económicos documentados no rastrean por sí solos activos, ingresos, honorarios, garantías u otro valor identificable de Sun Park hacia Orion. Esta última cuestión sigue abierta y exige prueba operación por operación. La divulgación, los conflictos y cualquier conducta facilitadora alegada también requieren prueba individualizada.</p>',
    'dossier_link': 'Abrir el dossier auditado de gobierno y partes vinculadas de Orion',
    'backlink': 'Leer la arquitectura aclarada de las dos ramas',
    'panel': 'Sun Park/MYND y Orion son ramas distintas pero interconectadas. Los vínculos documentados RICPE, AGM, Pamalexsha y Acosta Matos permanecen dentro de un análisis conjunto; no se deduce automáticamente un flujo de activos Sun Park→Orion ni el conocimiento o la responsabilidad de ningún actor. La investigación de FMMM se conserva, pero no es el vínculo exclusivo.',
    'reply': 'Se mantienen abiertos el derecho de rectificación y la aportación de prueba contraria o exculpatoria. El silencio no implica admisión.',
}}

NOTE = '''\n## Architecture clarification — 5 September 2026\n\nControl: `PD-ORION-ARCH-20260905-01`. The existing bilingual platform-continuity routes are corrected to **distinct but interconnected branches**, not an independent/unconnected Orion branch and not an FMMM-only inquiry. Sections 2–8 below remain controlling and unchanged. The audited ownership, management, related-party and RICPE formation/financing links are preserved within the unitary analysis. Every edge retains its own role, date and evidential status.\n\nDocumented corporate/economic connections are distinct from proof that identifiable Sun Park/MYND/LPB/Matkator assets, income, fees, guarantees, collateral or other value entered or supported Orion. The latter remains open and requires transaction-specific evidence. The June-2023 temporal limit prevents attribution of earlier acts to Orion itself; it does not erase earlier roles of subsequently connected individuals/entities. Knowledge, duty, conduct, disclosure, reliance, benefit and responsibility remain actor-specific. FMMM's existing professional inquiry, all attributed allegations, adverse/contrary records, lawful alternatives and the right of reply are preserved.\n\nCorrected routes: `/en/orion-ricpe-platform-continuity/` and `/es/orion-ricpe-continuidad/`; reciprocal explanatory links connect both to the existing Orion Rental SOCIMI dossiers. No new identity, event, financing figure, asset-flow finding or criminal finding is created. This clarification alone proves neither deployment nor formal service.\n'''
ARCH = {
    'control_id': CONTROL,
    'framing_en': 'Distinct but interconnected branches',
    'framing_es': 'Ramas distintas pero interconectadas',
    'correction_scope': 'Remove independent/unconnected-branch and FMMM-only framing; preserve all existing documented edges and individual proof limits.',
    'documented_connections': 'Existing dated RICPE/Orion founding and financing, AGM management, Pamalexsha and Acosta ownership/governance/related-party records remain controlling.',
    'asset_value_flow': 'OPEN — a specific Sun Park/MYND/LPB/Matkator to Orion transfer, guarantee, collateral use or economic benefit requires separate transaction-level proof.',
    'temporal_limit': 'Orion was constituted in June 2023; earlier Sun Park acts are not attributed to Orion itself. Earlier roles of later-connected people/entities are not erased.',
    'individual_test': 'Knowledge, duties, conduct, disclosure, reliance, benefit and responsibility require actor-specific evidence; no transfer through association.',
    'routes': ['/' + p.removesuffix('index.html') for pair in ROUTES.values() for p in pair],
    'source_record': RECORD,
}

class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.links = collections.Counter(); self.ids = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        for key in ('href', 'src'):
            if key in a: self.links[(tag, key, a[key])] += 1
        if 'id' in a: self.ids.append(a['id'])

def replace_once(text: str, old: str, new: str) -> str:
    if old not in text:
        if new in text: return text
        raise ValueError('Unrecognised source; refusing broad replacement: ' + old[:100])
    if text.count(old) != 1: raise ValueError('Ambiguous replacement: ' + old[:100])
    return text.replace(old, new, 1)

def blocks(lang: str):
    c = COPY[lang]
    legacy, dossier = ROUTES[lang]
    link = '../orion-rental-socimi/'
    intro = f'<div class="correction" id="{MARKER}" data-control="{CONTROL}">{c["notice"]}<p><a href="{link}">{c["dossier_link"]} →</a></p></div>'
    bridge = f'<section class="section alt" id="documented-connections"><div class="shell record"><h2>{c["bridge_title"]}</h2>{c["bridge"]}<p><a href="{link}">{c["dossier_link"]} →</a> · <a href="https://www.boe.es/diario_borme/txt.php?id=BORME-A-2023-137-35">BORME 2023</a> · <a href="https://www.orionsocimi.com/inversores">Orion investor documents</a></p><p>{c["reply"]}</p></div></section>'
    back = '../' + legacy.split('/')[1] + '/#' + MARKER
    panel = f'<section class="section alt" id="{MARKER}" data-control="{CONTROL}"><div class="shell"><h2>{c["h1"]}</h2><p>{c["panel"]}</p><p><a href="{back}">{c["backlink"]} →</a></p></div></section>'
    return intro, bridge, panel

def transformed(path: str, text: str) -> str:
    for lang, pair in ROUTES.items():
        c = COPY[lang]; intro, bridge, panel = blocks(lang)
        if path == pair[0]:
            for key in ('title', 'desc', 'brand', 'eyebrow', 'h1', 'lead', 'fmmm', 'intro'):
                text = replace_once(text, c[key + '_old'], c[key])
            text = replace_once(text, c['notice_old'], intro)
            if 'id="documented-connections"' not in text:
                anchor = '<section class="section"><div class="shell record"><h2>' + c['fmmm']
                text = replace_once(text, anchor, bridge + '\n\n' + anchor)
            return text
        if path == pair[1]:
            if f'id="{MARKER}"' not in text:
                text = replace_once(text, '</main>', panel + '\n</main>')
            return text
    if path == RECORD:
        if CONTROL not in text:
            text = replace_once(text, '\n## 2. Primary corporate chronology\n', NOTE + '\n## 2. Primary corporate chronology\n')
        return text
    if path == GRAPH:
        d = json.loads(text)
        assert d['entity']['id'] == 'PD-SP-O-0027'
        if 'architecture_clarification' in d and d['architecture_clarification'] != ARCH:
            raise ValueError('Existing architecture clarification differs; semantic review required')
        d['architecture_clarification'] = ARCH
        return json.dumps(d, ensure_ascii=False, indent=2) + '\n'
    raise ValueError(path)

PATHS = [p for pair in ROUTES.values() for p in pair] + [RECORD, GRAPH]

def apply():
    ref = subprocess.check_output(['git', 'branch', '--show-current'], cwd=ROOT, text=True).strip()
    if ref in ('main', 'master', ''): raise RuntimeError('Preparation requires an explicit non-main branch')
    changes = {}
    for p in PATHS:
        before = (ROOT / p).read_text()
        after = transformed(p, before)
        if before != after: changes[p] = after
    for p, after in changes.items(): (ROOT / p).write_text(after)
    print(json.dumps({'control': CONTROL, 'prepared_files': list(changes)}, indent=2))

def git_text(base: str, path: str) -> str:
    return subprocess.check_output(['git', 'show', base + ':' + path], cwd=ROOT, text=True)

def check(base: str):
    checks = 0
    for p in PATHS:
        actual = (ROOT / p).read_text()
        expected = transformed(p, git_text(base, p))
        assert actual == expected, 'Unapproved source delta or missing correction: ' + p
        assert transformed(p, actual) == actual, 'Non-deterministic: ' + p
        checks += 2
        if p.endswith('.html'):
            old, new = Links(), Links(); old.feed(git_text(base, p)); new.feed(actual)
            assert not (old.links - new.links), 'Lost existing link or asset: ' + p
            assert len(new.ids) == len(set(new.ids)), 'Duplicate ID: ' + p
            assert MARKER in new.ids, 'Missing static correction: ' + p
            checks += 3
            for tag, key, target in new.links:
                if not target or target.startswith(('http:', 'https:', 'mailto:', '#', 'tel:', 'data:', 'javascript:')): continue
                clean = target.split('#')[0].split('?')[0]
                dest = ROOT / clean.removeprefix('/por-derecho/').lstrip('/') if clean.startswith('/') else (ROOT / p).parent / clean
                assert dest.exists(), 'Broken local resource: ' + p + ' -> ' + target
                checks += 1
    for lang, pair in ROUTES.items():
        text = (ROOT / pair[0]).read_text()
        for key in ('title', 'desc', 'brand', 'eyebrow', 'h1', 'lead', 'fmmm', 'intro'):
            assert COPY[lang][key] in text
            assert COPY[lang][key + '_old'] not in text
            checks += 2
        assert COPY[lang]['notice_old'] not in text
        assert '42/19/17/22' in text and '42/21/17/20' in text
        assert '2024136159' in text and '2024174266' in text
        checks += 3
    # Informative finite scan; historic quoted corrections are not automatically rewritten.
    hits = []
    for prefix in ('en', 'es', 'assets'):
        for p in (ROOT / prefix).rglob('*'):
            if p.suffix not in ('.html', '.js', '.json', '.md') or not p.is_file(): continue
            text = p.read_text(errors='replace')
            for term in ('independent Orion branch', 'rama Orion independiente', 'The only Sun Park question', 'La única cuestión Sun Park'):
                if term in text: hits.append({'path': str(p.relative_to(ROOT)), 'term': term})
    print(json.dumps({'control': CONTROL, 'base': base, 'checks_passed': checks, 'other_exact_legacy_hits': hits}, ensure_ascii=False, indent=2))
    # These exact incorrect phrases must not remain in reader-facing source or runtime data.
    assert not hits, 'Additional live-source framing contradiction requires reconciliation'

def live():
    root = 'https://sbu001monterecco.github.io/por-derecho/'
    sha = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    pending = set(PATHS[:4] + [GRAPH])
    for attempt in range(24):
        for p in sorted(pending.copy()):
            route = p.removesuffix('index.html')
            req = urllib.request.Request(root + route + '?orion-arch=' + sha, headers={'Cache-Control': 'no-cache', 'User-Agent': 'Por-Derecho-release-verification'})
            try:
                with urllib.request.urlopen(req, timeout=25) as response:
                    body = response.read()
                expected = (ROOT / p).read_bytes()
                if body == expected:
                    print('LIVE_BYTE_MATCH', p, hashlib.sha256(body).hexdigest(), flush=True); pending.remove(p)
            except Exception as exc: print('READBACK_RETRY', p, type(exc).__name__, flush=True)
        if not pending: return
        time.sleep(10)
    raise RuntimeError('Not live-verified: ' + ', '.join(sorted(pending)))

if __name__ == '__main__':
    a = argparse.ArgumentParser(); a.add_argument('--apply', action='store_true'); a.add_argument('--check', action='store_true'); a.add_argument('--live', action='store_true'); a.add_argument('--base', default=BASE)
    args = a.parse_args()
    if args.apply: apply()
    if args.check: check(args.base)
    if args.live: live()
    if not (args.apply or args.check or args.live): a.error('Choose --apply, --check or --live')
