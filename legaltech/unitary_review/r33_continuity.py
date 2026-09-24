"""Source-preserving R33 continuity adjunct; no automatic evidential promotion.

All populated inputs/outputs are PRIVATE. This module neither contacts providers
nor writes repositories. It complements, and does not replace, truth_machine.py.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from collections import Counter, deque
from pathlib import Path
from typing import Any

KINDS = {'SOURCE_RECOVERY', 'EVIDENCE_REVIEW', 'SEGMENTATION', 'TRANSLATION',
         'PRESENTATION', 'PRESERVATION', 'TOOLING', 'NO_CHANGE', 'INTEGRITY_REVIEW'}
TEXT = {'.md', '.txt', '.html', '.json', '.jsonl', '.csv', '.py', '.js', '.yml', '.yaml'}
HOSTS = {'gitlab', 'github'}

class ContinuityError(ValueError):
    """An input or state transition failed a source/continuity check."""

def require(ok: bool, message: str) -> None:
    if not ok:
        raise ContinuityError(message)

def digest(value: Any) -> str:
    raw = value if isinstance(value, bytes) else json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
    return hashlib.sha256(raw).hexdigest()

def normal(text: str) -> str:
    return ' '.join(text.split())

def source_hash(data: dict) -> str:
    value = data.get('document', {}).get('sha256', '')
    require(bool(re.fullmatch(r'[a-f0-9]{64}', value)), 'native source hash required')
    return value

def span(text: str, start: int, end: int, encoding: str) -> str:
    require(type(start) is int and type(end) is int and 0 <= start < end,
            'invalid nonempty span')
    if encoding == 'utf16':
        raw = text.encode('utf-16-le')
        require(end * 2 <= len(raw), 'UTF-16 span outside block')
        try:
            return raw[start * 2:end * 2].decode('utf-16-le')
        except UnicodeError as exc:
            raise ContinuityError('split UTF-16 surrogate') from exc
    require(encoding == 'codepoint' and end <= len(text), 'span outside block')
    return text[start:end]

def units(case: dict, encoding: str = 'codepoint') -> list[dict]:
    """Validate every quote and retain each original annotation as an opaque row.

    occurrence_id is version-specific; text_key is a nonunique retrieval key.
    Neither is an assertion that equal wording expresses the same proposition.
    """
    sha = source_hash(case)
    version = digest(case)
    schema = case.get('schema')
    require(schema in {'pd.forensic.v1', 'pd.truth-machine.v2'}, 'unsupported schema')
    blocks = case.get('blocks', [])
    require(isinstance(blocks, list), 'blocks must be a list')
    require(all(isinstance(b, dict) and isinstance(b.get('id'), str)
                and isinstance(b.get('text'), str) for b in blocks), 'invalid block')
    by_id = {b['id']: b for b in blocks}
    require(len(by_id) == len(blocks), 'duplicate block id')
    annotations = case.get('annotations') if schema == 'pd.forensic.v1' else case.get('propositions')
    require(isinstance(annotations, list), 'annotation/proposition list required')
    seen, output = set(), []
    for row in annotations:
        require(isinstance(row, dict) and isinstance(row.get('id'), str), 'invalid row')
        require(row['id'] not in seen, 'duplicate review id')
        seen.add(row['id'])
        quote = row.get('quote')
        require(isinstance(quote, str) and bool(quote), 'empty quote')
        block_id = row.get('block', row.get('block_id'))
        block = by_id.get(block_id)
        if schema == 'pd.forensic.v1':
            require(block is not None, 'unresolved block')
            require(span(block['text'], row.get('start'), row.get('end'), encoding) == quote,
                    'quotation differs from source span')
            page, last = block.get('page'), block.get('pageEnd', block.get('page'))
            source_kind = block.get('sourceKind', 'text_or_selected_excerpt')
        else:
            require(digest(quote.encode()) == row.get('quote_sha256'), 'quote hash differs')
            page, last, source_kind = row.get('page'), row.get('page'), 'segmentation_proposal'
        require(type(page) is int and type(last) is int and 1 <= page <= last,
                'invalid page range')
        output.append({
            'id': row['id'], 'occurrence_id': digest([version, row['id']]),
            'native_sha256': sha, 'input_object_sha256': version,
            'text_key': digest([sha, normal(quote)]), 'quote_sha256': digest(quote.encode()),
            'span_key': digest([sha, page, last, digest(block['text'].encode()) if block else None,
                                row.get('start'), row.get('end'), encoding, digest(quote.encode())]),
            'block_id': block_id, 'page': page, 'page_end': last,
            'start': row.get('start'), 'end': row.get('end'), 'offset_encoding': encoding,
            'source_kind': source_kind, 'quote': quote, 'original_row': row,
            'anchor_check': 'STORED_BLOCK_EXACT' if block else 'SELF_HASH_ONLY',
            'assessment_transfer': False})
    return output


def bind_successor(proposal: dict, original: dict, encoding: str = 'codepoint') -> list[dict]:
    """Bind a segmentation file to the actual preserved source-block package."""
    require(source_hash(proposal) == source_hash(original), 'source identity differs')
    validated = units(proposal)
    units(original, encoding)
    blocks = {b['id']: b for b in original['blocks']}
    for row in validated:
        block = blocks.get(row['block_id'])
        require(block is not None and block['page'] == row['page'], 'source block/page differs')
        require(span(block['text'], row['start'], row['end'], encoding) == row['quote'],
                'successor quote differs from preserved source block')
        row['anchor_check'] = 'PRESERVED_PARENT_BLOCK_EXACT'
        row['parent_object_sha256'] = digest(original)
    return validated



def crosswalk(old: list[dict], new: list[dict]) -> dict:
    """Return complete, many-to-many TEXT candidates; never copy assessments.

    Page-overlap plus exact/whitespace-normalised quotation is not semantic
    equivalence. Split/merge suggestions need separate source/human review.
    """
    require(len({r['id'] for r in old}) == len(old), 'duplicate old ids')
    require(len({r['id'] for r in new}) == len(new), 'duplicate new ids')
    hashes = {r['native_sha256'] for r in old + new}
    require(len(hashes) <= 1, 'different native documents need explicit source review')
    rows, used = [], set()
    for left in old:
        q = normal(left['quote'])
        eligible = [r for r in new if left['page'] <= r['page_end']
                    and r['page'] <= left['page_end']]
        exact = [r['id'] for r in eligible if left['quote'] == r['quote']]
        normed = [r['id'] for r in eligible if q == normal(r['quote'])]
        contained = [r['id'] for r in eligible if min(len(q), len(normal(r['quote']))) >= 35
                     and (q in normal(r['quote']) or normal(r['quote']) in q)]
        targets = exact or normed or contained
        if exact:
            status = 'EXACT_TEXT_CANDIDATE' if len(exact) == 1 else 'AMBIGUOUS_EXACT_TEXT'
        elif normed:
            status = 'WHITESPACE_CANDIDATE' if len(normed) == 1 else 'AMBIGUOUS_WHITESPACE'
        elif contained:
            status = 'SPLIT_MERGE_OR_SCOPE_CANDIDATE'
        else:
            status = 'NO_TEXT_COUNTERPART_LOCATED'
        used.update(targets)
        rows.append({'old_id': left['id'], 'old_occurrence_id': left['occurrence_id'],
                     'status': status, 'candidate_ids': targets,
                     'assessment_transfer': False, 'review': 'SOURCE_REVIEW_REQUIRED'})
    return {'old_count': len(old), 'new_count': len(new), 'rows': rows,
            'status_counts': dict(Counter(r['status'] for r in rows)),
            'new_without_candidate': [r['id'] for r in new if r['id'] not in used],
            'old_rows_preserved': len(old), 'new_rows_preserved': len(new),
            'boundary': 'Text matching is not independent corroboration or semantic adoption.'}

def snapshot(host: str, root: Path, revision: str, scope: str,
             max_bytes: int = 3_000_000) -> dict:
    """Inventory the supplied bounded tree, including explicit exclusions.

    revision is a recorded caller assertion, not authentication of a remote
    tree. Content hashes reproduce precisely the supplied local corpus.
    """
    require(host in HOSTS, 'host must be gitlab or github')
    require(root.is_dir() and not root.is_symlink(), 'regular corpus directory required')
    require(bool(re.fullmatch('[a-f0-9]{40}', revision)), '40-character revision required')
    require(bool(scope.strip()) and max_bytes > 0, 'scope and positive size limit required')
    entries, docs = [], {}
    for path in sorted(root.rglob('*')):
        rel = path.relative_to(root).as_posix()
        if path.is_symlink():
            entries.append({'path': rel, 'state': 'EXCLUDED_SYMLINK'}); continue
        if path.is_dir():
            continue
        if any(x in {'.git', 'node_modules', '.venv', 'venv'} for x in path.parts):
            entries.append({'path': rel, 'state': 'EXCLUDED_SUPPORT_TREE'}); continue
        try:
            size = path.stat().st_size
            if size > max_bytes:
                entries.append({'path': rel, 'state': 'EXCLUDED_SIZE', 'bytes': size}); continue
            raw = path.read_bytes()
            entry = {'path': rel, 'bytes': len(raw), 'sha256': digest(raw)}
            if path.suffix.lower() not in TEXT:
                entry['state'] = 'EXCLUDED_TYPE'
            else:
                try:
                    body = raw.decode('utf-8')
                    if '\x00' in body:
                        entry['state'] = 'EXCLUDED_BINARY'
                    elif not body.strip():
                        entry['state'] = 'EMPTY'
                    else:
                        entry['state'] = 'INDEXED'; docs[rel] = body
                except UnicodeDecodeError:
                    entry['state'] = 'UNREADABLE_UTF8'
            entries.append(entry)
        except OSError as exc:
            entries.append({'path': rel, 'state': 'READ_ERROR', 'error_type': type(exc).__name__})
    return {'host': host, 'revision': revision, 'revision_authentication': 'CALLER_DECLARED',
            'scope': scope, 'inventory': entries, 'inventory_sha256': digest(entries),
            'counts': dict(Counter(e['state'] for e in entries)), 'documents': docs,
            'complete_remote_repository': False}


def source_delta(before: dict, after: dict) -> dict:
    """Compute inventory changes; disappearance is not proof of suppression."""
    require(before['host'] == after['host'], 'cannot compare different hosts as versions')
    old = {r['path']: r for r in before['inventory']}
    new = {r['path']: r for r in after['inventory']}
    return {'host': after['host'], 'before': before['inventory_sha256'],
            'after': after['inventory_sha256'], 'added': sorted(new.keys() - old.keys()),
            'removed': sorted(old.keys() - new.keys()),
            'changed': sorted(k for k in old.keys() & new.keys() if old[k] != new[k]),
            'merits_assessment_changed': False}



def retrieve(corpora: list[dict], terms: list[str], offset: int = 0, limit: int = 8) -> dict:
    require(type(offset) is int and offset >= 0 and type(limit) is int and limit > 0,
            'invalid pagination')
    names = [c['host'] for c in corpora]
    require(set(names) <= HOSTS and len(names) == len(set(names)), 'invalid/duplicate hosts')
    require(terms and all(isinstance(t, str) and t.strip() for t in terms), 'terms required')
    output = {'searched_hosts': sorted(names), 'unsearched_hosts': sorted(HOSTS - set(names)),
              'host_search_coverage_percent': None, 'exhaustive_source_review': False,
              'state': 'SEARCHED_BOUNDED_CORPORA' if corpora else 'NO_CORPORA_SUPPLIED',
              'terms': terms, 'hosts': {}}
    for corpus in corpora:
        hits = []
        for path, body in corpus['documents'].items():
            score = sum(body.casefold().count(t.casefold()) for t in terms)
            if score:
                lines = [i for i, line in enumerate(body.splitlines(), 1)
                         if any(t.casefold() in line.casefold() for t in terms)]
                hits.append({'path': path, 'sha256': digest(body.encode()),
                             'matching_lines': lines, 'lexical_count': score,
                             'relation': 'CANDIDATE_ONLY', 'independent_corroboration': False})
        hits.sort(key=lambda h: (-h['lexical_count'], h['path']))
        end = offset + limit
        output['hosts'][corpus['host']] = {
            'revision': corpus['revision'], 'inventory_sha256': corpus['inventory_sha256'],
            'scope': corpus['scope'], 'total_candidates': len(hits),
            'offset': offset, 'limit': limit, 'hits': hits[offset:end],
            'truncated': end < len(hits), 'next_offset': end if end < len(hits) else None,
            'state': 'CANDIDATES' if hits else 'NO_CANDIDATE_IN_DECLARED_CORPUS'}
    return output

def invalidated(changed: list[str], edges: list[dict]) -> list[dict]:
    """Traverse declared dependencies, cycle-safely. Invalidated != disproved."""
    graph: dict[str, list[str]] = {}
    for edge in edges:
        require(all(isinstance(edge.get(k), str) and edge[k] for k in ('from', 'to', 'basis')),
                'dependency requires source, target and declared basis')
        graph.setdefault(edge['from'], []).append(edge['to'])
    seen, queue, found = set(changed), deque(changed), []
    while queue:
        source = queue.popleft()
        for target in sorted(graph.get(source, [])):
            if target not in seen:
                seen.add(target); queue.append(target)
                found.append({'id': target, 'triggered_by': source,
                              'state': 'REVIEW_REQUIRED', 'assessment_changed': False})
    return found

def decision_gate(decision: dict) -> dict:
    required = ['reviewer', 'left_pinpoint', 'right_pinpoint', 'actor_capacity_time_scope',
                'contrary_material', 'lawful_alternative', 'source_lineage', 'rationale']
    missing = [k for k in required if not isinstance(decision.get(k), str) or not decision[k].strip()]
    if decision.get('reviewer_type') != 'HUMAN':
        missing.append('human_review')
    if decision.get('relation') not in {'SUPPORTS', 'CONTRADICTS', 'NARROWS', 'QUALIFIES',
                                        'EXCULPATES', 'UNRESOLVED', 'NO_CONNECTION'}:
        missing.append('allowed_relation')
    for k in ('left_source_sha256', 'right_source_sha256'):
        if not isinstance(decision.get(k), str) or not re.fullmatch('[a-f0-9]{64}', decision[k]):
            missing.append(k)
    return {'state': 'ELIGIBLE_FOR_SEPARATE_REVIEW' if not missing else 'BLOCKED',
            'missing': missing, 'automatically_promoted': False,
            'boundary': 'Field completeness does not authenticate sources or prove intent.'}

def verify_ledger(events: list[dict]) -> None:
    previous, seen = None, set()
    for event in events:
        require(event.get('id') not in seen, 'duplicate event id'); seen.add(event.get('id'))
        require(event.get('previous_sha256') == previous, 'broken ledger chain')
        payload = {k: v for k, v in event.items() if k != 'sha256'}
        require(event.get('sha256') == digest(payload), 'changed ledger event')
        previous = event['sha256']

def append_event(events: list[dict], event: dict, expected_tip: str | None) -> list[dict]:
    """Pure append with optimistic concurrency; caller must persist atomically.

    Rewritten entire chains remain possible without an independently pinned tip.
    """
    verify_ledger(events)
    tip = events[-1]['sha256'] if events else None
    require(tip == expected_tip, 'stale expected tip')
    require(event.get('kind') in KINDS, 'unknown event kind')
    required = ['id', 'recorded_at', 'execution_state', 'input_versions', 'sources_examined',
                'propositions', 'before', 'after', 'contrary_evidence', 'dependencies',
                'integration', 'publication', 'reason']
    require(all(k in event for k in required), 'incomplete processing event')
    require(isinstance(event['id'], str) and event['id'].strip(), 'event id required')
    require(event['id'] not in {e['id'] for e in events}, 'event id already exists')
    require('sha256' not in event and 'previous_sha256' not in event, 'reserved chain fields')
    require(event['execution_state'] in {'EXECUTED', 'HISTORICAL_REPORTED', 'BLOCKED', 'NO_CHANGE'},
            'invalid execution state')
    if event['kind'] == 'NO_CHANGE' or event['execution_state'] == 'NO_CHANGE':
        require(event['before'] == event['after'], 'no-change event changes an assessment')
    payload = dict(event, previous_sha256=tip)
    return events + [dict(payload, sha256=digest(payload))]

def inspect_cases(paths: list[Path], output: Path) -> dict:
    require(len(paths) >= 1, 'at least one input required')
    require(not output.exists(), 'output already exists; use a new version directory')
    cases, provenance, anchors = [], [], []
    for path in paths:
        raw = path.read_bytes(); case = json.loads(raw)
        parsed = units(case)
        cases.append(case); anchors.append(parsed)
        provenance.append({'filename': path.name, 'bytes': len(raw), 'sha256': digest(raw),
                           'native_sha256': source_hash(case), 'units': len(parsed),
                           'blocks': len(case.get('blocks', [])), 'original_rows_retained': True})
    require(len({source_hash(c) for c in cases}) == 1, 'native-source mismatch')
    walks = [crosswalk(anchors[i], anchors[i + 1]) for i in range(len(anchors) - 1)]
    result = {'schema': 'pd.r33-continuity.v1', 'private': True, 'inputs': provenance,
              'crosswalks': walks, 'case_objects_unchanged': cases,
              'units': anchors, 'substantive_findings_added': 0, 'automatic_promotions': 0,
              'pdf_visual_validation': 'NOT_PERFORMED_BY_THIS_TOOL',
              'boundary': 'Structural recovery and text mapping, not a new merits decision.'}
    output.mkdir(parents=True)
    (output / 'continuity.private.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    return {'inputs': provenance, 'crosswalk_counts': [w['status_counts'] for w in walks],
            'automatic_promotions': 0}

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case', action='append', required=True, type=Path)
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    try:
        result = inspect_cases(args.case, args.out)
    except (OSError, json.JSONDecodeError, ContinuityError) as exc:
        parser.exit(2, f'Continuity check failed: {exc}\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
