#!/usr/bin/env python3
"""Release acceptance primitives. Discovery, execution, acceptance and live proof differ."""
from __future__ import annotations
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import unicodedata

SCHEMA = 'por-derecho.release-acceptance.v1'
TERMINAL = {'VERIFIED_FOR_SCOPE', 'ABORTED_BEFORE_MERGE'}
TRANSITIONS = {
    'CLAIMED': {'ACCEPTED', 'BLOCKED', 'ABORTED_BEFORE_MERGE'},
    'ACCEPTED': {'MERGE_PENDING', 'BLOCKED', 'ABORTED_BEFORE_MERGE'},
    'MERGE_PENDING': {'MERGED', 'RECOVERY_REQUIRED'},
    'MERGED': {'DEPLOYED', 'RECOVERY_REQUIRED'},
    'DEPLOYED': {'VERIFIED_FOR_SCOPE', 'RECOVERY_REQUIRED'},
    'BLOCKED': {'CLAIMED', 'ABORTED_BEFORE_MERGE'},
    'RECOVERY_REQUIRED': {'MERGED', 'DEPLOYED', 'VERIFIED_FOR_SCOPE', 'ABORTED_BEFORE_MERGE'},
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_path(path: str) -> str:
    if not isinstance(path, str) or not path or Path(path).is_absolute() or '..' in Path(path).parts or '\\' in path:
        raise ValueError('Unsafe repository-relative path')
    return path


def acceptance(results: list[dict], required: list[str]) -> dict:
    """Missing, duplicate, skipped, timed-out and unknown required checks all fail."""
    if not required or len(set(required)) != len(required):
        raise ValueError('Required checks must be a nonempty unique list')
    names = [r.get('check') for r in results]
    errors = []
    for name in required:
        matches = [r for r in results if r.get('check') == name]
        if len(matches) != 1:
            errors.append({'rule': 'CHECK_CARDINALITY', 'check': name, 'count': len(matches)})
        elif (matches[0].get('status') != 'PASS' or type(matches[0].get('exit')) is not int
              or matches[0]['exit'] != 0 or matches[0].get('completed') is not True):
            errors.append({'rule': 'CHECK_NOT_PASSED', 'check': name})
    if len(names) != len(set(names)):
        errors.append({'rule': 'DUPLICATE_RESULT'})
    return {'schema': SCHEMA, 'required': required, 'results': results,
            'errors': errors, 'accepted': not errors,
            'state': 'ACCEPTED' if not errors else 'BLOCKED'}


def run_check(name: str, command: list[str], cwd: Path, timeout: int = 180, env: dict | None = None) -> dict:
    try:
        process = subprocess.run(command, cwd=cwd, env=env, capture_output=True, text=True, timeout=timeout)
        return {'check': name, 'completed': True, 'exit': process.returncode,
                'status': 'PASS' if process.returncode == 0 else 'FAIL',
                'stdout': process.stdout, 'stderr': process.stderr}
    except subprocess.TimeoutExpired as exc:
        return {'check': name, 'completed': False, 'exit': 124, 'status': 'TIMEOUT',
                'stdout': str(exc.stdout or ''), 'stderr': 'Bounded check timed out'}
    except OSError as exc:
        return {'check': name, 'completed': False, 'exit': 127, 'status': 'ERROR',
                'stdout': '', 'stderr': type(exc).__name__}


def _objects(text: str):
    decoder = json.JSONDecoder()
    for match in re.finditer(r'(?m)^\s*\{', text):
        try:
            value, _ = decoder.raw_decode(text[match.start():].lstrip())
            if isinstance(value, dict):
                yield value
        except ValueError:
            continue


def findings(result: dict) -> tuple[list[dict], bool]:
    """Read explicit defect fields or known error lines, never inventory/progress text.

    Unrecognised failures remain fail-closed, even when their logs happen to match.
    Multiplicity and numeric facts inside defect messages are preserved.
    """
    text = result.get('stdout', '') + '\n' + result.get('stderr', '')
    messages = None
    for obj in _objects(text):
        for key in ('strict_errors', 'errors', 'failures'):
            if key in obj and isinstance(obj[key], list):
                messages = obj[key]
                break
        if messages is not None:
            break
    if messages is None:
        lines = text.splitlines()
        messages = [m.group(1) for line in lines
                    if (m := re.match(r'^\s*(?:ERROR:|FAIL:|AssertionError:|ValueError:|RuntimeError:)\s*(.+)', line))]
        if not messages:
            marker = next((i for i, line in enumerate(lines)
                           if re.fullmatch(r'.*(?:VALIDATION FAILED|AUDIT: FAIL(?:ED)?|STRICT FAILURES:).*', line)), None)
            if marker is not None:
                messages = [m.group(1) for line in lines[marker+1:]
                            if (m := re.match(r'^\s*-\s+(.+)', line))]
    if not messages and result.get('exit') != 0:
        error_lines = [line.strip() for line in result.get('stderr', '').splitlines() if line.strip()]
        if error_lines and all(line.startswith('- ') for line in error_lines):
            messages = [line[2:] for line in error_lines]
    if not messages and re.search(r'(?m)^AssertionError\s*$', text) and 'Traceback (most recent call last):' in text:
        # A message-free assertion still identifies its source predicate. Keep
        # file/function/expression, not irrelevant frame line numbers or arrows.
        frames = list(re.finditer(r'(?m)^\s*File "([^"\n]+)", line \d+, in ([^\n]+)\n\s+(assert [^\n]+)', text))
        if frames:
            frame = frames[-1]
            messages = [{'error_type': 'AssertionError', 'source': frame[1],
                         'function': frame[2].strip(), 'predicate': frame[3].strip()}]
    records = []
    for message in messages:
        if isinstance(message, dict):
            encoded = json.dumps(message, sort_keys=True, ensure_ascii=False)
        elif isinstance(message, str) and message.strip():
            encoded = re.sub(r'\x1b\[[0-9;]*m', '', message).strip()
        else:
            return [], False
        records.append({'rule': result.get('check', 'legacy-validator'), 'severity': 'ERROR', 'detail': encoded})
    parsed = bool(records) if result.get('exit') != 0 else not records
    return records, parsed


def compare_results(base: dict, candidate: dict) -> dict:
    before, bp = findings(base)
    after, cp = findings(candidate)
    key = lambda row: json.dumps(row, sort_keys=True, ensure_ascii=False)
    b, c = Counter(map(key, before)), Counter(map(key, after))
    added, resolved = c-b, b-c
    unknown = candidate.get('completed', True) is not True or not cp
    if candidate.get('exit') == 0 and cp:
        state, allowed = ('RESOLVED' if base.get('exit') else 'PASS'), True
    elif bp and cp and not added and not unknown:
        state, allowed = ('IMPROVED_WITH_OPEN_FINDINGS' if resolved else 'INHERITED_FINDINGS_UNCHANGED'), True
    else:
        state, allowed = 'NEW_OR_UNPARSED_FAILURE', False
    return {'status': state, 'no_new_failure': allowed,
            'new': [json.loads(k) for k in added.elements()],
            'resolved': [json.loads(k) for k in resolved.elements()],
            'remaining': after, 'candidate_passed': candidate.get('exit') == 0 and cp}


def require_prefix_records(original: list[dict], current: list[dict], key: str = 'id') -> None:
    """Allow independently authorised additions, never silently lose/change old rows."""
    def index(rows):
        out = {}
        for row in rows:
            ident = row.get(key)
            if not isinstance(ident, str) or not ident or ident in out:
                raise ValueError('Missing or duplicate canonical record ID')
            out[ident] = row
        return out
    a, b = index(original), index(current)
    for ident, row in a.items():
        if b.get(ident) != row:
            raise ValueError('Previously registered event changed or disappeared: '+ident)


def owned_blocks(expected: str, actual: str, markers: list[tuple[str, str]]) -> list[str]:
    blocks = []
    for start, end in markers:
        count = expected.count(start)
        if not count:
            if start in actual or end in actual:
                raise ValueError('Unexpected owned block marker')
            continue
        if count != 1 or expected.count(end) != 1 or actual.count(start) != 1 or actual.count(end) != 1:
            raise ValueError('Missing or duplicate managed block')
        pattern = re.escape(start) + r'.*?' + re.escape(end)
        want, have = re.search(pattern, expected, re.S), re.search(pattern, actual, re.S)
        if not want or not have or want[0] != have[0]:
            raise ValueError('Managed block differs from its source model')
        blocks.append(have[0])
    if not blocks:
        raise ValueError('Shared page has no owned blocks')
    return blocks


def identity_records(root: Path, revision: str | None = None) -> dict[str, dict]:
    index_path = 'assets/data/matter-identity-registry-v1.json'
    def load(path):
        safe_path(path)
        content = subprocess.check_output(['git', 'show', revision+':'+path], cwd=root) if revision else (root/path).read_bytes()
        return json.loads(content)
    index = load(index_path)
    result, parts, counts = {}, set(), Counter()
    for part in index['parts']:
        rel = 'assets/data/'+safe_path(part['path'])
        if rel in parts:
            raise ValueError('Duplicate identity part')
        parts.add(rel)
        rows = load(rel)['records']
        if len(rows) != part['count']:
            raise ValueError('Identity part count drift')
        for row in rows:
            ident, kind = row['id'], row['type']
            if ident in result or kind != part['type']:
                raise ValueError('Duplicate identity or wrong part type: '+ident)
            result[ident] = row
            counts[kind] += 1
    if {'total': len(result), **dict(counts)} != index['counts']:
        raise ValueError('Canonical identity count drift')
    return result


def identity_collisions(before: dict[str, dict], after: dict[str, dict]) -> list[str]:
    errors = []
    normalize = lambda s: ''.join(c for c in unicodedata.normalize('NFKD', s.casefold()) if not unicodedata.combining(c)).strip()
    for ident, old in before.items():
        new = after.get(ident)
        if new is None:
            errors.append(ident+': existing identity disappeared')
            continue
        if old['type'] != new['type']:
            errors.append(ident+': identity type changed')
        if normalize(old['name']) == normalize(new['name']):
            continue
        # No unreviewed reassignment. A source-supported correction retains exact
        # prior identity, a correction record and source references in its history.
        history = new.get('identity_resolution_history', [])
        valid_history = any(r.get('prior_record') == old and r.get('source_refs') and r.get('superseded_only') for r in history)
        if not valid_history:
            errors.append(ident+': changed canonical name without source-linked prior-record history')
    return errors


def advance(state: dict, phase: str, owner: str, fence: int, evidence: dict | None = None) -> dict:
    if state.get('owner') != owner or state.get('fence') != fence:
        raise ValueError('Stale publication owner/fence')
    if phase not in TRANSITIONS.get(state['phase'], set()):
        raise ValueError('Invalid publication transition')
    if phase == 'MERGED' and not (evidence or {}).get('merge_sha'):
        raise ValueError('Merge evidence required')
    if phase == 'DEPLOYED' and not (evidence or {}).get('pages_run_id'):
        raise ValueError('Successful exact-SHA Pages evidence required')
    if phase == 'VERIFIED_FOR_SCOPE' and not ((evidence or {}).get('exact_matches') and (evidence or {}).get('pending') == []):
        raise ValueError('Complete live scope evidence required')
    result = deepcopy(state)
    result['phase'] = phase
    result['updated_at'] = utc_now()
    result.setdefault('checkpoints', []).append({'phase': phase, 'at': result['updated_at'], 'evidence': evidence or {}})
    return result
