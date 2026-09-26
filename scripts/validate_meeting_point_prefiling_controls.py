#!/usr/bin/env python3
"""Bounded technical checks, never a merits decision or filing certification.
Legacy: validator DOC1.txt DOC2.txt
Successor: validator DOC1.pdf DOC2.pdf --profile bounded-v13-v7 --manifest PRIVATE.json
The private manifest and court PDFs must not be committed to public Git.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path

CORE = {
    'historical_non_adoption': ['no constituye', 'reiteración automática'],
    'cexp_extinction_control': ['CEXP', 'extinción'],
    'capacity_specific': ['capacidad', 'procedimiento'],
    'historic_damages_control': ['cuantificaciones históricas', 'no constituyen'],
    'criminal_allegation_control': ['calificaciones penales históricas', 'hechos probados'],
    'historical_current_controller': ['posición actual', 'Documento 1'],
}
LEGACY = {
    'hava_vida_control': ['Hava Vida', 'titularidad registral'],
    'term_sheet_control': ['Hoja de Términos', 'exigibilidad'],
}
REQUIRED_DOC1 = {**CORE, **LEGACY}
FORBIDDEN_UNQUALIFIED = [
    'la cexp quedó extinguida', 'la cexp fue disuelta por',
    'todos los propietarios eran miembros de la cexp',
    'la cifra de 89.646.211,25 euros se reclama',
    'la hoja de términos prueba el desembolso',
]
ALLOWED_PUZZLE = {5, 6, 9, 10, 11, 18, 19, 20, 21, 22, 23, 24, 25, 27, 28, 29, 30}
PROFILE = 'bounded-v13-v7'
BINDINGS = {('prospectus', 1, 156), ('prospectus', 7, 157),
            ('ricpe_web', 2, 158), ('ricpe_web', 3, 159), ('ricpe_web', 4, 160),
            ('puzzle', 27, 163), ('puzzle', 28, 164), ('puzzle', 29, 165)}

def norm(s: str) -> str:
    return ' '.join(s.lower().split())

def check_text(doc1: str, doc2: str, profile: str = 'legacy') -> list[str]:
    if profile not in ('legacy', PROFILE):
        return ['Unknown profile']
    a, b = norm(doc1), norm(doc2)
    failures = []
    for gate, needles in (REQUIRED_DOC1 if profile == 'legacy' else CORE).items():
        if not all(norm(n) in a for n in needles):
            failures.append(f'{gate}: missing required markers')
    for phrase in FORBIDDEN_UNQUALIFIED:
        if norm(phrase) in a:
            failures.append(f'Forbidden unqualified phrase: {phrase}')
    if 'documento 2' not in a or 'históric' not in a:
        failures.append('Missing Document 1 controller for historical Document 2')
    if profile == PROFILE:
        if not all(x in b for x in ('no constituye', 'documento 1', 'históric')):
            failures.append('Missing Document 2 front-control markers')
        # This explicit successor excludes collateral, rather than silently waiving safeguards.
        # A deliberate future reintroduction requires a new reviewed profile.
        if re.search(r'\b(hava vida|ben oldman|mct|hoja de términos)\b', a + ' ' + b):
            failures.append('Excluded collateral reintroduced into bounded successor')
        for needle in ('38bis', '38ter', 'en estudio', 'newco', 'condiciones', 'sha-256'):
            if needle not in a:
                failures.append(f'Missing successor/source control: {needle}')
    return failures

def check_manifest_shape(m: dict) -> list[str]:
    if not isinstance(m, dict):
        return ['Manifest must be a JSON object']
    errors = []
    if m.get('schema') != 1 or m.get('profile') != PROFILE:
        errors.append('Unknown manifest schema/profile')
    if m.get('versions') != [13, 7]:
        errors.append('Version pair is not v13/v7')
    selected = m.get('puzzle_pages')
    if selected != [27, 28, 29] or not set(selected or []).issubset(ALLOWED_PUZZLE):
        errors.append('PUZZLE selection violates the closed successor selection')
    try:
        actual = {(x['source'], x['source_page'], x['output_page']) for x in m['bindings']}
        if actual != BINDINGS or len(m['bindings']) != len(BINDINGS):
            errors.append('Source-to-output page bindings differ from this profile')
        if {x['id'] for x in m['sources']} != {'prospectus', 'ricpe_web', 'puzzle'} or len(m['sources']) != 3:
            errors.append('Missing or duplicate source')
        if len(m['documents']) != 2:
            errors.append('Exactly two documents required')
    except (KeyError, TypeError):
        errors.append('Incomplete manifest')
    return errors

def digest(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def verify_package(paths: list[Path], manifest_path: Path) -> list[str]:
    import fitz  # Only the PDF profile needs PyMuPDF; legacy and unit tests use stdlib.
    m = json.loads(manifest_path.read_text(encoding='utf-8'))
    errors = check_manifest_shape(m)
    if errors:
        return errors
    docs, sources = [], {}
    try:
        for i, (path, expected) in enumerate(zip(paths, m['documents'])):
            if path.suffix.lower() != '.pdf':
                return ['The bounded profile requires the exact PDFs, not text surrogates']
            if digest(path) != expected['sha256']:
                errors.append(f'Document {i+1}: SHA-256 mismatch')
            if path.stat().st_size != expected['bytes'] or path.stat().st_size >= 10_000_000:
                errors.append(f'Document {i+1}: byte count/internal size target failure')
            d = fitz.open(path); docs.append(d)
            if len(d) != expected['pages'] or len(d) != (165 if i == 0 else 213):
                errors.append(f'Document {i+1}: page-count mismatch')
            front = norm(' '.join(p.get_text() for p in list(d)[:2]))
            version = 'v13' if i == 0 else 'v7'
            if version not in front or (i == 1 and 'v13' not in front):
                errors.append(f'Document {i+1}: front version/pair mismatch')
        if errors:
            return errors
        for src in m['sources']:
            p = manifest_path.parent / src['path']
            if digest(p) != src['sha256']:
                errors.append(f"Source {src['id']}: SHA-256 mismatch")
            s = fitz.open(p); sources[src['id']] = s
            if len(s) != src['pages']:
                errors.append(f"Source {src['id']}: page-count mismatch")
        if errors:
            return errors
        for item in m['bindings']:
            src = sources[item['source']][item['source_page']-1]
            out = docs[0][item['output_page']-1]
            text = norm(src.get_text())
            if text and text not in norm(out.get_text()):
                errors.append(f"Source text not preserved at output page {item['output_page']}")
            if item['source'] == 'puzzle':
                a = src.get_pixmap()
                b = out.get_pixmap(clip=fitz.Rect(0, 22, src.rect.width, src.rect.height+22))
                if (a.width, a.height, a.samples) != (b.width, b.height, b.samples):
                    errors.append(f"PUZZLE pixel mismatch at output page {item['output_page']}")
        errors += check_text('\n'.join(p.get_text() for p in docs[0]),
                             '\n'.join(p.get_text() for p in docs[1]), PROFILE)
        return errors
    finally:
        for d in docs + list(sources.values()):
            d.close()

def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('doc1', type=Path); p.add_argument('doc2', type=Path)
    p.add_argument('--profile', choices=['legacy', PROFILE], default='legacy')
    p.add_argument('--manifest', type=Path)
    args = p.parse_args(argv)
    try:
        if args.profile == PROFILE:
            if args.manifest is None:
                print('BLOCKED: bounded profile requires a private exact-file manifest')
                return 2
            errors = verify_package([args.doc1, args.doc2], args.manifest)
        else:
            errors = check_text(args.doc1.read_text(encoding='utf-8'), args.doc2.read_text(encoding='utf-8'))
        if errors:
            print('BLOCKED\n' + '\n'.join(' - ' + e for e in errors))
            return 1
        print('MACHINE_CONTROLS_PASS_HUMAN_REVIEW_REQUIRED')
        print('Not legal approval, signature clearance, remote CI, submission or receipt.')
        return 0
    except (OSError, ValueError, KeyError, TypeError, IndexError, ImportError) as exc:
        print(f'BLOCKED: {type(exc).__name__}: {exc}')
        return 2

if __name__ == '__main__':
    raise SystemExit(main())
