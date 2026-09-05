#!/usr/bin/env python3
"""Check/write the existing identity projections; never edit canonical identities.

Resumes the projection work from PRs #1412/#1437 without their frozen 351-ID
Valencia-only assumption. Dates and counts come from the same canonical index.
"""
from __future__ import annotations
import argparse
from collections import Counter
from copy import deepcopy
from datetime import date
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
INDEX = 'assets/data/matter-identity-registry-v1.json'
STATE = 'ops/CURRENT_UNITARY_STATE.json'
PAGES = {'en': 'en/matter-identity-registry/index.html', 'es': 'es/registro-identidad-materia/index.html'}
TYPES = ('PERSON', 'ORGANISATION', 'STRUCTURE', 'INSTITUTION', 'PROCEEDING')
MONTHS = {'en': 'JANUARY FEBRUARY MARCH APRIL MAY JUNE JULY AUGUST SEPTEMBER OCTOBER NOVEMBER DECEMBER'.split(), 'es': 'ENERO FEBRERO MARZO ABRIL MAYO JUNIO JULIO AGOSTO SEPTIEMBRE OCTUBRE NOVIEMBRE DICIEMBRE'.split()}
WORDS = {'en': ('people', 'organisations', 'structures', 'institutions', 'proceedings'), 'es': ('personas', 'organizaciones', 'estructuras', 'instituciones', 'procedimientos')}


def read_json(root: Path, rel: str) -> dict:
    data = json.loads((root / rel).read_text(encoding='utf-8'))
    if not isinstance(data, dict):
        raise ValueError(f'{rel}: expected JSON object')
    return data


def canonical_snapshot(root: Path = ROOT) -> tuple[dict, str]:
    index = read_json(root, INDEX)
    actual: Counter = Counter()
    seen: set[str] = set()
    for part in index['parts']:
        rel = Path(INDEX).parent / part['path']
        path = (root / rel).resolve()
        if not path.is_relative_to(root.resolve()) or path.suffix != '.json':
            raise ValueError(f'Unsafe registry part: {rel}')
        records = read_json(root, str(rel))['records']
        if len(records) != part['count']:
            raise ValueError(f'Part count mismatch: {rel}')
        for row in records:
            rid, kind = row['id'], row['type']
            if not isinstance(rid, str) or not rid or rid in seen or kind not in TYPES:
                raise ValueError(f'Duplicate/invalid identity: {rid!r} / {kind!r}')
            seen.add(rid)
            actual[kind] += 1
    counts = {'total': len(seen), **{key: actual[key] for key in TYPES}}
    if counts != index['counts']:
        raise ValueError('Canonical index counts disagree with its identity shards')
    stamp = index['control_date']
    if not isinstance(stamp, str) or date.fromisoformat(stamp).isoformat() != stamp:
        raise ValueError('Canonical control date must be ISO YYYY-MM-DD')
    return counts, stamp


def once(text: str, pattern: str, replacement, label: str) -> str:
    matches = list(re.finditer(pattern, text, flags=re.DOTALL))
    if len(matches) != 1:
        raise ValueError(f'{label}: expected one projection field, found {len(matches)}')
    return re.sub(pattern, replacement, text, count=1, flags=re.DOTALL)


def project_page(text: str, counts: dict, stamp: str, lang: str) -> str:
    text = once(text, r'data-static-registry-counts="[0-9-]+"', 'data-static-registry-counts="' + '-'.join(str(counts[k]) for k in ('total', *TYPES)) + '"', lang+' static counts')
    for key in ('total', *TYPES):
        stat = key.upper()
        text = once(text, rf'(<strong data-registry-stat="{stat}">)\d+(</strong>)', lambda m: m[1]+str(counts[key])+m[2], lang+' '+stat)
    # Numeric prose projections only: preserve every qualifying/evidential sentence.
    for kind, word in zip(TYPES, WORDS[lang]):
        text = re.sub(r'\b\d+ (?='+word+r'\b)', str(counts[kind])+' ', text)
    if lang == 'en':
        patterns = (r'(?<=register of )\d+(?= immutable IDs)', r'\b\d+(?= canonical identities)', r'(?<=register of )\d+(?= identities)', r'\b\d+(?= IDs</strong>)', r'(?<=static canonical denominator is )\d+')
    else:
        patterns = (r'(?<=Registro operativo de )\d+(?= IDs)', r'\b\d+(?= identidades canónicas)', r'(?<=Registro canónico de )\d+(?= identidades)', r'\b\d+(?= IDs</strong>)', r'(?<=denominador canónico estático es )\d+', r'(?<=capa estática canónica es )\d+')
    for pattern in patterns:
        text = re.sub(pattern, str(counts['total']), text)
    day = date.fromisoformat(stamp)
    human = f'{day.day} {MONTHS[lang][day.month-1]} {day.year}'
    text = once(text, r'(PD-SP-IDENTITY-REGISTRY-001 · PD-SP-IDENTITY-OPS-001 · )[^<]+', lambda m:m[1]+human, lang+' displayed date')
    def dataset(match):
        data = json.loads(match[2])
        if data.get('identifier') != 'PD-SP-IDENTITY-REGISTRY-001':
            return match[0]
        data['dateModified'] = stamp
        measured = data['variableMeasured']
        labels = ('Total', *('People Organisations Structures Institutions Proceedings'.split() if lang == 'en' else 'Personas Organizaciones Estructuras Instituciones Procedimientos'.split()))
        mapping = dict(zip(labels, ('total', *TYPES)))
        if {v['name'] for v in measured} != set(labels):
            raise ValueError(lang+' Dataset count labels differ from canonical classes')
        for value in measured:
            value['value'] = counts[mapping[value['name']]]
        return match[1]+json.dumps(data,ensure_ascii=False,separators=(',',':'))+match[3]
    text = once(text, r'(<script type="application/ld\+json">)(\{.*?"identifier":"PD-SP-IDENTITY-REGISTRY-001".*?\})(</script>)', dataset, lang+' Dataset')
    return text


def projection_outputs(root: Path = ROOT) -> dict[str, str]:
    counts, stamp = canonical_snapshot(root)
    outputs = {rel:project_page((root/rel).read_text(encoding='utf-8'),counts,stamp,lang) for lang,rel in PAGES.items()}
    state = deepcopy(read_json(root,STATE))
    section = state['identity_registry']
    section['counts'] = counts
    section['control_date'] = stamp
    for key in ('total', *TYPES):
        if key in section:
            section[key] = counts[key]
    outputs[STATE] = json.dumps(state,ensure_ascii=False,indent=2)+'\n'
    return outputs


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    mode=parser.add_mutually_exclusive_group()
    mode.add_argument('--write',action='store_true')
    mode.add_argument('--check',action='store_true')
    args=parser.parse_args()
    try:
        outputs=projection_outputs()
        drift=[p for p,t in outputs.items() if (ROOT/p).read_text(encoding='utf-8') != t]
        if args.write:
            for path in drift:
                (ROOT/path).write_text(outputs[path],encoding='utf-8')
            print('IDENTITY PROJECTIONS: WROTE',json.dumps(drift))
            return 0
        if drift:
            raise ValueError('Stale derived projections: '+', '.join(drift)+'; run with --write before merge')
        print('IDENTITY PROJECTIONS: PASS',json.dumps(canonical_snapshot()[0]))
        return 0
    except (ValueError,KeyError,TypeError,OSError) as exc:
        print('IDENTITY PROJECTIONS: FAIL —',exc)
        return 1

if __name__ == '__main__':
    raise SystemExit(main())
