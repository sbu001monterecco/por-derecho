#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import json
import re

ROOT = Path('.')
REG = ROOT/'assets/data/matter-identity-registry-v1.json'
counts = json.loads(REG.read_text(encoding='utf-8'))['counts']
ordered = {k: counts[k] for k in ('total','PERSON','ORGANISATION','STRUCTURE','INSTITUTION','PROCEEDING')}

# Current unitary control contains a dated historical source base plus a separately
# labelled current canonical identity denominator. Update only the latter.
p = ROOT/'ops/CURRENT_UNITARY_STATE.json'
state = json.loads(p.read_text(encoding='utf-8'))
identity = state['identity_registry']
identity['counts'] = ordered.copy()
identity['total'] = counts['total']
identity['INSTITUTION'] = counts['INSTITUTION']
identity['PROCEEDING'] = counts['PROCEEDING']
p.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

# Validators intentionally preserve historical snapshot constants while deriving
# the current canonical registry denominator from this generated block. This
# replacement accepts both multiline and compact prior output, so rerunning the
# release workflow cannot fail merely because this sync already ran once.
def sync_python_block(path: Path) -> None:
    text = path.read_text(encoding='utf-8')
    block_lines = ['CURRENT_CANONICAL_IDENTITY_COUNTS = {']
    block_lines.extend(f'    {json.dumps(key)}: {ordered[key]},' for key in ('total','PERSON','ORGANISATION','STRUCTURE','INSTITUTION','PROCEEDING'))
    block_lines.append('}')
    block = '\n'.join(block_lines)
    pattern = re.compile(r'CURRENT_CANONICAL_IDENTITY_COUNTS\s*=\s*\{[^}]*\}', re.S)
    text2, n = pattern.subn(block, text, count=1)
    if n != 1:
        raise AssertionError(f'current canonical count block not found in {path}')
    path.write_text(text2, encoding='utf-8')

for rel in ('scripts/validate_operational_truth.py','scripts/validate_current_reverse_engineered_digest.py'):
    sync_python_block(ROOT/rel)

# Static registry self-check markers are generated from the current registry, not
# maintained as another independent denominator.
marker = '-'.join(str(counts[k]) for k in ('total','PERSON','ORGANISATION','STRUCTURE','INSTITUTION','PROCEEDING'))
for rel in ('es/registro-identidad-materia/index.html','en/matter-identity-registry/index.html'):
    path = ROOT/rel
    text = path.read_text(encoding='utf-8')
    text, n = re.subn(r'data-static-registry-counts="\d+-\d+-\d+-\d+-\d+-\d+"', f'data-static-registry-counts="{marker}"', text)
    if n == 0:
        raise AssertionError(f'static registry marker absent from {rel}')
    path.write_text(text, encoding='utf-8')

# Idempotence self-check: a second in-process application must make no further
# semantic change and must still locate the generated blocks.
first = {rel: (ROOT/rel).read_text(encoding='utf-8') for rel in ('scripts/validate_operational_truth.py','scripts/validate_current_reverse_engineered_digest.py')}
for rel in first:
    sync_python_block(ROOT/rel)
    assert (ROOT/rel).read_text(encoding='utf-8') == first[rel], f'non-idempotent count sync: {rel}'

print('CURRENT_CAEPR_COUNTS_SYNCED', ordered, marker, 'IDEMPOTENT')
