#!/usr/bin/env python3
"""Read-only deletion-safety and publication-integrity audit for the Laborý/CATRUDE workstream."""
from __future__ import annotations
import argparse, csv, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "ops/LABORY_CATRUDE_RECOVERY_STATUS.json"
ARCHIVES = ROOT / "evidence/sun-park/labory-catrude/archive-register.csv"
CANDIDATES = ROOT / "evidence/sun-park/labory-catrude/candidate-report-register.csv"
PAGES = [
    ROOT / "es/labory-catrude-antecedente-tecnico-historico/index.html",
    ROOT / "en/labory-catrude-historical-technical-antecedent/index.html",
]
WORKFLOW = ROOT / ".github/workflows/labory-catrude-thread-deletion-audit.yml"
PUBLIC_PREFIXES = [
    ROOT / "evidence/sun-park/labory-catrude",
    ROOT / "ops/LABORY_CATRUDE_RECOVERY_STATUS.json",
    ROOT / "ops/LABORY_CATRUDE_RECOVERY_BACKLOG.md",
    ROOT / "archive/LABORY_CATRUDE_RECOVERY_CONTINUITY_24AUG2026.md",
    *PAGES,
]
ALLOWED_CLASSIFICATIONS = {"POSSIBLE TARGET", "PROBABLE TARGET", "CONFIRMED TARGET", "RELATED BUT DIFFERENT REPORT", "EXCLUDED", "UNREADABLE / ACCESS PENDING"}
RECOVERED_INSPECTION_STATES = {
    "opened_safely_extracted_inventory",
    "opened_safely_extracted_recursive_inventory",
}
FORBIDDEN_PUBLIC_PATTERNS = {
    "gmail_message_id": re.compile(r"\b(?:14|15|16|17|18|19)[0-9a-f]{14}\b", re.I),
    "email_address": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
    "private_share_locator": re.compile(r"share\.google/", re.I),
    "gmail_attachment_token": re.compile(r"ANGjdJ[-_A-Za-z0-9]+"),
}


def load_json(path: Path, errors: list[str]) -> dict:
    try: return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{path.relative_to(ROOT)}: invalid or missing JSON: {exc}"); return {}


def public_files() -> list[Path]:
    files=[]
    for p in PUBLIC_PREFIXES:
        if p.is_dir(): files.extend(x for x in p.rglob('*') if x.is_file())
        elif p.is_file(): files.append(p)
    return sorted(set(files))


def main() -> int:
    parser=argparse.ArgumentParser()
    parser.add_argument('--output-dir', default='artifacts/labory-catrude-deletion-audit')
    args=parser.parse_args()
    errors=[]; warnings=[]
    status=load_json(STATUS, errors)
    if status.get('target_status') != 'NOT_IDENTIFIED': errors.append('target_status must remain NOT_IDENTIFIED unless the registers and primary evidence are updated together')
    if status.get('deletion_state') != 'not eligible': errors.append('workstream deletion_state must be not eligible')
    try:
        rows=list(csv.DictReader(ARCHIVES.open(encoding='utf-8')))
    except Exception as exc:
        errors.append(f'cannot read archive register: {exc}'); rows=[]
    if len(rows) != 18: errors.append(f'archive register contains {len(rows)} rows; expected 18')
    expected=[f'GMAIL-ZIP-{i:03d}' for i in range(1,19)]
    if [r.get('archive_id') for r in rows] != expected: errors.append('archive aliases must be complete and ordered GMAIL-ZIP-001 through GMAIL-ZIP-018')
    recovered=[]; pending=[]
    for r in rows:
        inspection=r.get('inspection_status')
        byte_access=r.get('byte_access_status')
        if inspection == 'metadata_only_not_opened':
            pending.append(r)
            if byte_access != 'not_accessible': errors.append(f"{r.get('archive_id')}: unopened row must remain not_accessible")
        elif inspection in RECOVERED_INSPECTION_STATES:
            recovered.append(r)
            if byte_access != 'recovered_and_sha256_verified': errors.append(f"{r.get('archive_id')}: opened row must be recovered_and_sha256_verified")
            if r.get('priority') != 'completed': errors.append(f"{r.get('archive_id')}: opened row must be marked completed")
            if not re.search(r'\bSHA-256 [0-9a-f]{64}\b', r.get('next_action','')): errors.append(f"{r.get('archive_id')}: opened row lacks a public SHA-256 custody reference")
        else:
            errors.append(f"{r.get('archive_id')}: unsupported inspection status {inspection!r}")
        if r.get('deletion_state') != 'not eligible': errors.append(f"{r.get('archive_id')}: deletion state is not protected")
        for key in ('archive_name','source_date','size_bytes','relevance','next_action'):
            if not r.get(key): errors.append(f"{r.get('archive_id')}: missing {key}")
    try:
        candidates=list(csv.DictReader(CANDIDATES.open(encoding='utf-8')))
    except Exception as exc:
        errors.append(f'cannot read candidate register: {exc}'); candidates=[]
    for c in candidates:
        if c.get('classification') not in ALLOWED_CLASSIFICATIONS: errors.append(f"{c.get('candidate_id')}: invalid classification")
    if not candidates or candidates[0].get('classification') != 'POSSIBLE TARGET': errors.append('target candidate must remain POSSIBLE TARGET')
    if not any(c.get('document') == 'Unidentified historical Laborý/CATRUDE report' for c in candidates): errors.append('target candidate is missing')
    for page in PAGES:
        if not page.is_file(): errors.append(f'missing page: {page.relative_to(ROOT)}'); continue
        text=page.read_text(encoding='utf-8')
        required=['NOT IDENTIFIED' if '/en/' in str(page) else 'NO IDENTIFICADO','FACT:' if '/en/' in str(page) else 'HECHO:','DOCUMENT:' if '/en/' in str(page) else 'DOCUMENTO:','OPEN QUESTION:' if '/en/' in str(page) else 'PREGUNTA ABIERTA:','Right of response' if '/en/' in str(page) else 'Derecho de respuesta','site.js?v=20260824e']
        for marker in required:
            if marker not in text: errors.append(f'{page.relative_to(ROOT)}: missing marker {marker}')
    if not WORKFLOW.is_file(): errors.append('scheduled workflow missing')
    else:
        workflow=WORKFLOW.read_text(encoding='utf-8')
        for marker in ('schedule:', "cron: '17 */6 * * *'", 'contents: read', 'workflow_dispatch:'):
            if marker not in workflow: errors.append(f'workflow missing {marker}')
        for forbidden in ('contents: write','git push','delete'):
            if forbidden in workflow.lower(): errors.append(f'workflow must be read-only; found {forbidden}')
    for path in public_files():
        if path.suffix.lower() not in {'.md','.csv','.json','.html','.yml','.yaml','.xml','.txt','.py'}: continue
        text=path.read_text(encoding='utf-8',errors='replace')
        for name, pattern in FORBIDDEN_PUBLIC_PATTERNS.items():
            if pattern.search(text): errors.append(f'{path.relative_to(ROOT)}: forbidden public {name}')
    result={
        'schema':'por-derecho.labory-catrude-deletion-audit.v1',
        'status':'FAIL' if errors else 'PASS',
        'target_status':status.get('target_status'),
        'deletion_state':status.get('deletion_state'),
        'archive_rows':len(rows),
        'archive_rows_recovered':len(recovered),
        'archive_rows_pending':len(pending),
        'candidate_rows':len(candidates),
        'errors':errors,
        'warnings':warnings,
        'operational_note':'Read-only audit. It does not delete, commit, push, merge or rewrite history.'
    }
    out=(ROOT/args.output_dir).resolve(); out.mkdir(parents=True,exist_ok=True)
    (out/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    md=['# Laborý / CATRUDE thread-deletion audit','',f"**Result:** {result['status']}",f"**Target:** {result['target_status']}",f"**Deletion state:** {result['deletion_state']}",f"**Archive rows:** {len(rows)}",'',result['operational_note']]
    if errors: md += ['', '## Errors', *[f'- {e}' for e in errors]]
    else: md += ['', '## Determination', '', f"This workstream remains **not eligible** for deletion because the target report is unidentified. {len(pending)} ranked archives remain uninspected at byte level; {len(recovered)} recovered archives are hash-controlled and also remain protected from deletion."]
    (out/'summary.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 1 if errors else 0

if __name__=='__main__': sys.exit(main())
