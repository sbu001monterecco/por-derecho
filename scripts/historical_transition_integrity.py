#!/usr/bin/env python3
"""Verify dated release snapshots against their actual recorded Git origins.

Current files have current contracts, not obsolete historical byte locks. A
known pre-existing bot reconciliation is verified separately from the original
release; neither snapshot is rewritten or silently accepted at today's bytes.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import re
import subprocess

# This inherited mutation was found through Git history, not generated here.
# 7249c209 changed nine candidate hashes and the 43/63 coverage to 45/61.
# Retain and verify both observations; reject any further unrecorded mutation.
RECONCILED_SNAPSHOTS = {
    'publication-manifests/historic-proceedings-authority-reintegration-20260903.json': {
        'revision': '7249c209d496e044bf17259b9d82b0b45c2fcef1',
        'blob': 'be687d4b96bd722a98205fb746dab5b3c84ab32a',
        'original_revision': '687c0a32a217f1db32a3e7e3be5e8650b677570a',
        'original_blob': '02a9c30ea7979072a2948cc9d488290192ab9bbd',
    },
}


def historical_transition_bytes_match(root: Path, manifest_path: str, handoff_path: str) -> bool:
    try:
        for value in (manifest_path, handoff_path):
            if Path(value).is_absolute() or '..' in Path(value).parts:
                raise ValueError('Unsafe control path')
        current=(root/manifest_path).read_bytes()
        handoff=json.loads((root/handoff_path).read_bytes())
        release=handoff['production_release']
        original, merged=release['reviewed_head_sha'], release['merge_sha']
        if not all(isinstance(s,str) and re.fullmatch(r'[a-f0-9]{40}',s) for s in (original,merged)):
            raise ValueError('Missing exact historical source/merge SHA')
        def git(*args):
            return subprocess.run(['git',*args],cwd=root,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True).stdout
        git('merge-base','--is-ancestor',original,merged)
        git('merge-base','--is-ancestor',merged,'HEAD')
        original_bytes=git('show',original+':'+manifest_path)
        observations=[(original, original_bytes)]
        reconciliation=RECONCILED_SNAPSHOTS.get(manifest_path)
        if current != original_bytes:
            if reconciliation is None or original != reconciliation['original_revision']:
                raise ValueError('Unrecorded historical snapshot mutation')
            revision=reconciliation['revision']
            git('merge-base','--is-ancestor',merged,revision)
            git('merge-base','--is-ancestor',revision,'HEAD')
            for rev,key in ((original,'original_blob'),(revision,'blob')):
                actual=git('rev-parse',rev+':'+manifest_path).decode().strip()
                if actual != reconciliation[key]:
                    raise ValueError('Recorded historical snapshot blob mismatch')
            reconciled_bytes=git('show',revision+':'+manifest_path)
            if current != reconciled_bytes:
                raise ValueError('Snapshot differs from its documented bot-reconciliation origin')
            observations.append((revision,reconciled_bytes))
        checked=0
        for revision, raw in observations:
            snapshot=json.loads(raw)
            rows=snapshot['transitions'];seen=set()
            if len(rows)!=snapshot['candidate_delta_file_count']:
                raise ValueError('Historical transition row count mismatch')
            mismatches=[]
            for row in rows:
                path=row['resource'];expected=row['candidate_sha256']
                if not isinstance(path,str) or Path(path).is_absolute() or '..' in Path(path).parts or path in seen:
                    raise ValueError('Unsafe or duplicate transition path')
                seen.add(path)
                if expected is None:
                    result=subprocess.run(['git','cat-file','-e',revision+':'+path],cwd=root,capture_output=True)
                    if result.returncode==0:mismatches.append(path)
                    elif result.returncode not in (1,128):raise ValueError('Git object lookup failed')
                else:
                    if not isinstance(expected,str) or not re.fullmatch(r'[a-f0-9]{64}',expected):
                        raise ValueError('Invalid historical content hash')
                    if hashlib.sha256(git('show',revision+':'+path)).hexdigest()!=expected:mismatches.append(path)
            if mismatches:
                raise ValueError('Snapshot hashes disagree with '+revision+': '+', '.join(mismatches))
            checked+=len(rows)
            print(f'HISTORICAL TRANSITION: verified {len(rows)} hashes at {revision}')
        print(f'HISTORICAL TRANSITION: PASS — {checked} historical hashes; no current files or dated observations rewritten')
        return True
    except (OSError,ValueError,KeyError,TypeError,subprocess.CalledProcessError) as exc:
        print('HISTORICAL TRANSITION: FAIL —',str(exc))
        return False
