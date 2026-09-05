#!/usr/bin/env python3
"""Replay only the existing CajaSiete delta on actual main; never publish main.

Preserve current-main records and page bytes, keep fixed canonical identities,
validate before a normal worker push, and stop if either remote ref has moved.
A separately authorised integrator must retire the writer and verify the release.
"""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

BRANCH = 'worker/cajasiete-board-visuals-20260905'
GENERATOR = 'scripts/prepare_cajasiete_board_visuals_20260905.py'
CHECKER = 'scripts/check_cajasiete_board_browser_20260905.py'
SELF = 'scripts/reconcile_cajasiete_documentary_review_20260905.py'
WORKFLOW = '.github/workflows/cajasiete-board-visuals-20260905.yml'
CROSS = 'ops/CAJASIETE_BOARD_VISUAL_CROSSWALK_20260905.json'
INPUT = 'ops/cajasiete-board-source-input-20260905.json'
REG = 'assets/data/institutional-communications-register-v1.json'
BUILDER = 'scripts/reconcile_institutional_communications.py'
REPORT = 'ops/CAJASIETE_REVIEW_RECONCILIATION_20260905.json'
CONTROL = 'PD-CAJASIETE-BOARD-VISUALS-20260905'

OVERRIDE = {
    'es': {
        'intro': 'La gestión del canal de información se examina por sus propios documentos. La consulta comercial genuina es independiente y debe valorarse por sus propios méritos; su resultado no determina la evaluación del canal.',
        'timeline': [
            ['10 DIC 2025', 'Independencia declarada', 'Se anunciaron medidas de inhibición y reasignación ante posibles conflictos para garantizar una evaluación objetiva.'],
            ['9 ABR 2026', 'Comunicación recibida', 'El canal confirmó la recepción. El acuse no acredita admisión, contenido completo ni examen sustantivo.'],
            ['28 ABR 2026', 'Inadmisión comunicada', 'El canal declaró un examen preliminar y anunció destruir la información conforme a la normativa aplicable.']
        ],
        'oriontitle': 'ORION: RAMA DISTINTA, INTERCONECTADA',
        'orion': 'Cajasiete ↔ Orion ↔ Grupo Patrimonial Acosta Matos. Relación societaria fechada: no acredita una transmisión de Sun Park a Orion ni coordinación ilícita.',
        'review': '<h3>Qué acredita cada documento</h3><p>La respuesta de independencia describe una garantía de procedimiento, no una promesa de admisión. El acuse acredita recepción. La decisión declara un examen preliminar: la pregunta es qué se examinó y qué sustentó cada motivo, no afirmar que no hubo examen alguno. Cada uno de estos tres hitos remite a su propio evento y fuente en los enlaces de esta sección.</p><p><strong>Extracto literal de la decisión de inadmisión:</strong> «Se procederá a destruir la información en cumplimiento de la normativa aplicable». <a href="/por-derecho/es/registros-institucionales/#source-PD-SP-SRC-0015">PD-SP-SRC-0015</a>. No acredita destrucción efectiva ni su ilicitud. Las figuras son síntesis editoriales de Por Derecho, no reproducciones de documentos oficiales.</p><p><strong>Título y financiación:</strong> deben distinguirse la fecha de la escritura, la inscripción y la expedición de la nota; titular registral, hipotecante y prestatario; responsabilidad hipotecaria, desembolso y valoración. Los extractos informativos parciales no se presentan como certificaciones completas. No se atribuye la reconstrucción agregada del proyecto a un préstamo de CajaSiete.</p><p><strong>Rama Orion:</strong> se conservan las conexiones societarias documentadas, sus fechas y las identidades de las distintas sociedades. Una participación histórica no se presenta como participación actual. Cualquier flujo concreto de activos, ingresos o garantías desde Sun Park requiere prueba propia.</p><p><strong>Respuesta y corrección:</strong> se invita a aportar explicación, prueba contraria y corrección documentada. El silencio no equivale a admisión. La preservación, transferencia, anonimización y supresión se examinan conforme a las reglas aplicables y con acceso restringido, no mediante publicación de datos protegidos.</p>'
    },
    'en': {
        'intro': 'Reporting-channel handling is examined on its own documents. The genuine commercial enquiry is independent and must be assessed on its own merits; its outcome does not determine the assessment of channel handling.',
        'timeline': [
            ['10 DEC 2025', 'Independence stated', 'Recusal and reassignment measures for potential conflicts were described to secure an objective assessment.'],
            ['9 APR 2026', 'Communication received', 'The channel confirmed receipt. The acknowledgement does not establish admission, complete contents or substantive review.'],
            ['28 APR 2026', 'Inadmission communicated', 'The channel stated a preliminary examination and announced destruction under the applicable rules.']
        ],
        'oriontitle': 'ORION: DISTINCT, INTERCONNECTED BRANCH',
        'orion': 'Cajasiete ↔ Orion ↔ Grupo Patrimonial Acosta Matos. A dated corporate relationship, not proof of a Sun Park transfer to Orion or unlawful coordination.',
        'review': '<h3>What each document establishes</h3><p>The independence response describes a procedural safeguard, not a promise of admission. The acknowledgement establishes receipt. The decision states that a preliminary examination occurred: the question is what was examined and what supported each ground, not an assertion that no examination occurred. Each of these three stages resolves to its own event and source through this section’s links.</p><p><strong>Original Spanish extract from the inadmission decision:</strong> «Se procederá a destruir la información en cumplimiento de la normativa aplicable». <a href="/por-derecho/en/institutional-records/#source-PD-SP-SRC-0015">PD-SP-SRC-0015</a>. Translation: the information will be destroyed in accordance with the applicable rules. This does not establish actual or unlawful destruction. The figures are Por Derecho editorial summaries, not reproductions of official documents.</p><p><strong>Title and financing:</strong> distinguish the deed date, registration and issue of the note; registered owner, mortgagor and borrower; mortgage liability, cash advanced and valuation. Partial informational extracts are not presented as complete certificates. The aggregate project reconstruction is not attributed to a CajaSiete loan.</p><p><strong>Orion branch:</strong> documented corporate connections, source dates and distinct legal persons are preserved. A historical shareholding is not presented as current ownership. Any specific flow of assets, income or guarantees from Sun Park requires its own evidence.</p><p><strong>Response and correction:</strong> explanations, contrary evidence and documented corrections are invited. Silence is not admission. Preservation, transfer, anonymisation and deletion are assessed under the applicable rules and restricted access, not by publishing protected data.</p>'
    }
}

def git(*args: str, cwd: Path | None = None) -> str:
    return subprocess.check_output(['git', *args], cwd=cwd, text=True).strip()

def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + '\n')

def patch_generator(path: Path) -> None:
    text = path.read_text()
    begin = '# DOCUMENTARY-REVIEW-20260905:START\n'
    end = '# DOCUMENTARY-REVIEW-20260905:END\n'
    patch = begin + 'for _language, _changes in ' + repr(OVERRIDE) + '.items():\n COPY[_language].update(_changes)\n' + end
    if begin in text:
        assert text.count(begin) == text.count(end) == 1
        text = text[:text.index(begin)] + patch + text[text.index(end) + len(end):]
    else:
        assert text.count('def vector(lang,n,logical,x):') == 1
        text = text.replace('def vector(lang,n,logical,x):', patch + 'def vector(lang,n,logical,x):', 1)
    old = '<h3>{c["sources"]}</h3><p>{source_links(lang,x)}</p>'
    new = old + '{c["review"]}'
    assert new in text or text.count(old) == 1
    if new not in text:
        text = text.replace(old, new, 1)
    # Current builder writes by default; --check remains read-only.
    text = text.replace("[sys.executable,BUILDER,'--write']", '[sys.executable,BUILDER]')
    compile(text, str(path), 'exec')
    path.write_text(text)

def adapt_current_builder(path: Path) -> None:
    """Use the actual canonical KEY_EVENTS reconciliation, not an obsolete loop."""
    text = path.read_text()
    if 'def load_cajasiete_board_events(' in text:
        raise ValueError('CajaSiete adapter already exists: inspect before replay')
    anchor = 'def reconcile_register(\n'
    call = '    key_events = deepcopy(KEY_EVENTS)\n'
    assert text.count(anchor) == text.count(call) == 1, 'Current canonical reconciliation architecture changed'
    adapter = ('def load_cajasiete_board_events(root: Path) -> list[dict]:\n'
               '    from prepare_cajasiete_board_visuals_20260905 import load_cajasiete_events\n'
               '    return load_cajasiete_events(root)\n\n\n')
    text = text.replace(anchor, adapter + anchor, 1)
    text = text.replace(call, call + '    key_events.extend(load_cajasiete_board_events(REPO_ROOT))\n', 1)
    compile(text, str(path), 'exec')
    path.write_text(text)

def main() -> None:
    root = Path(git('rev-parse', '--show-toplevel'))
    seed = os.environ['GITHUB_SHA']
    assert os.environ['GITHUB_REF_NAME'] == BRANCH
    assert git('rev-parse', 'HEAD') == seed
    subprocess.run(['git', 'fetch', '--quiet', 'origin', 'main'], check=True, cwd=root)
    base = git('rev-parse', 'origin/main', cwd=root)
    assert git('ls-remote', 'origin', 'refs/heads/' + BRANCH, cwd=root).split()[0] == seed
    work = Path(os.environ['RUNNER_TEMP']) / ('cajasiete-review-' + seed[:12])
    assert not work.exists()
    subprocess.run(['git', 'worktree', 'add', '--detach', str(work), base], check=True, cwd=root)
    artifacts = root / 'qa-cajasiete-review'
    artifacts.mkdir(exist_ok=True)
    write_json(artifacts / 'attempt.json', {'seed': seed, 'base': base, 'state': 'PREPARING_NOT_PUBLISHED'})
    cross = json.loads((root / CROSS).read_text())
    before = json.loads((work / REG).read_text())
    ids = {v['event_id'] for v in cross['events'].values()}
    assert not any(e['event_id'] in ids for e in before['events']), 'Already integrated or event collision'
    current_media = json.loads((work / 'data/digital-media-asset-register-v1.json').read_text())
    assert not set(cross['assets'].values()) & {a['reference'] for a in current_media['logical_assets']}, 'Media ID collision'
    unique = [GENERATOR, CHECKER, SELF, WORKFLOW, INPUT, CROSS]
    for name in unique:
        target = work / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(root / name, target)
    previous = cross['baseline_pages'].copy()
    cross.setdefault('baseline_reconciliation_history', []).append({'prior_page_hashes': previous, 'source_worker': seed, 'new_main': base, 'reason': 'Preserve every current-main page byte outside the existing CajaSiete owned block; no stale whole-file replay.'})
    for rel in cross['baseline_pages']:
        data = (work / rel).read_bytes()
        assert b'<!-- CAJASIETE-BOARD-VISUALS-20260905:START -->' not in data
        cross['baseline_pages'][rel] = hashlib.sha256(data).hexdigest()
    cross['review_base_sha'] = base
    write_json(work / CROSS, cross)
    patch_generator(work / GENERATOR)
    adapt_current_builder(work / BUILDER)
    commands = [
        [sys.executable, GENERATOR, 'apply'],
        [sys.executable, BUILDER, '--check'],
        [sys.executable, 'scripts/validate_institutional_communications.py'],
        [sys.executable, GENERATOR, 'check'],
        [sys.executable, CHECKER],
    ]
    for number, command in enumerate(commands, 1):
        result = subprocess.run(command, cwd=work, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        (artifacts / f'check-{number}.txt').write_text(result.stdout)
        print(result.stdout, flush=True)
        if result.returncode:
            if (work / 'qa-cajasiete').exists():
                shutil.copytree(work / 'qa-cajasiete', artifacts / 'screenshots', dirs_exist_ok=True)
            raise RuntimeError(f'Validation {number} failed with exit {result.returncode}; no push')
    after = json.loads((work / REG).read_text())
    amap = {e['event_id']: e for e in after['events']}
    assert all(amap.get(e['event_id']) == e for e in before['events']), 'Existing canonical record changed'
    br = json.loads((work / 'ops/CAJASIETE_BOARD_BROWSER_20260905.json').read_text())
    assert br['status'] == 'PASS' and br['case_count'] == br['passed'] == 24
    acceptance = json.loads((work / 'ops/CAJASIETE_BOARD_VISUAL_ACCEPTANCE_20260905.json').read_text())
    allowed = set(acceptance['paths']) | {GENERATOR, CHECKER, SELF, WORKFLOW, CROSS, INPUT, REPORT, 'ops/CAJASIETE_BOARD_VISUAL_ACCEPTANCE_20260905.json', 'ops/CAJASIETE_BOARD_BROWSER_20260905.json'}
    status = subprocess.check_output(['git', 'status', '--porcelain', '--untracked-files=all'], cwd=work, text=True)
    changed = [line[3:] for line in status.splitlines()]
    tracked_changes = [p for p in changed if not p.startswith(('qa-cajasiete/', '__pycache__/', 'scripts/__pycache__/'))]
    assert all(p in allowed for p in tracked_changes), ('Unexpected changed paths', tracked_changes)
    assert all(not line.startswith(' D') and not line.startswith('D ') for line in status.splitlines()), 'No deletion permitted'
    record = {'control_id': CONTROL, 'status': 'CURRENT_MAIN_RECONCILED_STATIC_AND_24_BROWSER_PASS_NOT_DEPLOYED', 'source_worker_sha': seed, 'base_sha': base, 'preserved_canonical_events': len(before['events']), 'candidate_event_count': len(after['events']), 'native_private_sources_published': False, 'source_crops_published': False, 'source_crop_status': 'WITHHELD_PENDING_CANONICAL_IDENTITY_AND_PUBLICATION_REVIEW', 'main_not_modified': True, 'changed_paths': sorted(set(tracked_changes) | {REPORT}), 'browser_report': 'ops/CAJASIETE_BOARD_BROWSER_20260905.json', 'open_gaps': acceptance.get('open_proof', []), 'writer_retirement_required': True, 'remaining_acceptance': ['Retire preparation writer', 'Exact-head release and publication checks', 'Active integrator/controller permit', 'Merge, exact Pages SHA and live readback']}
    write_json(work / REPORT, record)
    subprocess.run(['git', 'add', '--', *sorted(allowed)], cwd=work, check=True)
    tree = git('write-tree', cwd=work)
    commit = subprocess.check_output(['git','commit-tree',tree,'-p',seed,'-p',base,'-m','Reconcile CajaSiete documentary reader onto current main; preserve all sources and pass 24 browser cases'], cwd=work, text=True).strip()
    record['prepared_tree'] = tree
    record['candidate_sha'] = commit
    for path in sorted(allowed):
        src = work / path
        if src.is_file():
            dest = artifacts / path
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dest)
    shutil.copytree(work / 'qa-cajasiete', artifacts / 'screenshots', dirs_exist_ok=True)
    write_json(artifacts / 'preparation-receipt.json', record)
    assert git('ls-remote','origin','refs/heads/'+BRANCH,cwd=root).split()[0] == seed, 'Concurrent worker moved: no push'
    assert git('ls-remote','origin','refs/heads/main',cwd=root).split()[0] == base, 'Main moved: preserve artifact and reconcile again'
    subprocess.run(['git','push','origin',commit+':refs/heads/'+BRANCH],cwd=root,check=True)
    print(json.dumps({'status':'WORKER_UPDATED_NOT_PUBLISHED','candidate':commit,'base':base,'tree':tree},indent=2))

if __name__ == '__main__':
    main()
