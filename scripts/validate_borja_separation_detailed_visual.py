#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
ES = ROOT / 'es/concurso-36-2012-separacion-administrador-concursal-rpl-3304-2025/index.html'
EN = ROOT / 'en/insolvency-36-2012-administrator-removal-rpl-3304-2025/index.html'
DATA = ROOT / 'assets/data/concurso36-ac-separation-rpl3304-convergence-v1.json'
RESCAN = ROOT / 'archive/BORJA_SEPARATION_DETAILED_VISUAL_RESCAN_02SEP2026.md'

errors: list[str] = []

def check(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)

for path in (ES, EN, DATA, RESCAN):
    check(path.is_file(), f'missing required file: {path.relative_to(ROOT)}')

es = ES.read_text(encoding='utf-8') if ES.is_file() else ''
en = EN.read_text(encoding='utf-8') if EN.is_file() else ''
data = json.loads(DATA.read_text(encoding='utf-8')) if DATA.is_file() else {}

required_es = [
    'Aweswell originó la demanda → Aweswell recurrió → LPB recurrió independientemente',
    'LIVE · CONSOLIDATED MASTER ROLL',
    'Solicitud de separación de 23 abril 2025 · 58 páginas',
    'SIETE BLOQUES ALEGADOS · RESUMEN DETALLADO',
    'Qué se alegó',
    'Por qué se presentó como causa de separación',
    'RPL 3319/2025',
    'RPL 3304/2025',
    'Decreto 222/2026',
]
required_en = [
    'Aweswell originated the application → Aweswell appealed → LPB independently appealed',
    'LIVE · CONSOLIDATED MASTER ROLL',
    'The 23 April 2025 application · 58 pages',
    'SEVEN PLEADED BLOCKS · DETAILED SUMMARY',
    'What was alleged',
    'Why it was advanced as a removal ground',
    'RPL 3319/2025',
    'RPL 3304/2025',
    'Decree 222/2026',
]
for marker in required_es:
    check(marker in es, f'Spanish page missing marker: {marker}')
for marker in required_en:
    check(marker in en, f'English page missing marker: {marker}')

for label, text in (('Spanish', es), ('English', en)):
    check(len(re.findall(r'class="metric"', text)) == 6, f'{label} visual summary must contain exactly 6 metric cards')
    check(len(re.findall(r'class="relief"', text)) == 6, f'{label} petitum must contain exactly 6 relief cards')
    check(len(re.findall(r'class="ground" id=', text)) == 7, f'{label} page must contain exactly 7 detailed ground cards')
    check(len(re.findall(r'class="link-card"', text)) == 6, f'{label} page must contain exactly 6 interlink groups')
    check('class="master"' in text, f'{label} page lacks consolidated master-roll panel')
    check('SHA-256' in text and '5665ec05ae42f18fc64b1209ed7984c39ece015933bdfc9dd8bcf1a8ece6bf26' in text, f'{label} page lacks controlled application hash')

expected_ground_ids = {
    'accounts', 'financial-risk-swap', 'credit-assignment', 'dacion',
    'hotel-unit', 'remuneration', 'opacity-conflicts'
}
details = data.get('originating_application', {}).get('pleaded_factual_blocks_detailed', [])
check(len(details) == 7, 'machine-readable control must contain 7 detailed factual blocks')
check({item.get('key') for item in details} == expected_ground_ids, 'machine-readable ground keys drift')
visual = data.get('originating_application', {}).get('visual_summary', {})
check(visual == {
    'pages': 58,
    'pleaded_factual_blocks': 7,
    'relief_or_communication_families': 6,
    'controlled_first_instance_decisions': 2,
    'independent_appeals': 2,
    'live_consolidated_rolls': 1,
}, 'machine-readable visual summary drift')
check(data.get('canonical_ids', {}).get('rpl_3304', {}).get('state') == 'LIVE_CONSOLIDATED_MASTER_ROLL', 'RPL 3304 canonical live state drift')
check(data.get('canonical_ids', {}).get('rpl_3319', {}).get('state') == 'HISTORICAL_ORIGINATING_APPEAL_ACCUMULATED_INTO_GC_APP_005', 'RPL 3319 accumulated state drift')

href_re = re.compile(r'href="([^"]+)"')
for label, path, text in (('Spanish', ES, es), ('English', EN, en)):
    for href in href_re.findall(text):
        parsed = urlsplit(href)
        if parsed.scheme or href.startswith('//') or href.startswith('#') or href.startswith('mailto:'):
            continue
        target = unquote(parsed.path)
        resolved = (path.parent / target).resolve()
        try:
            resolved.relative_to(ROOT.resolve())
        except ValueError:
            errors.append(f'{label} link escapes repository: {href}')
            continue
        if target.endswith('/') or not Path(target).suffix:
            candidate = resolved / 'index.html'
        else:
            candidate = resolved
        check(candidate.exists(), f'{label} internal link target missing: {href} -> {candidate.relative_to(ROOT) if candidate.is_relative_to(ROOT) else candidate}')

if errors:
    print('BORJA SEPARATION DETAILED VISUAL VALIDATION: FAIL')
    for error in errors:
        print(f'- {error}')
    raise SystemExit(1)

print('BORJA SEPARATION DETAILED VISUAL VALIDATION: PASS — bilingual 58-page summary, 7 detailed grounds, 6 relief cards, 6 interlink groups and canonical 3304/3319 state verified')
