#!/usr/bin/env python3
"""Verify immutable release snapshots against their recorded Git revision.

Current content is validated by current contracts. It must not be forced back to
old byte hashes to satisfy a historical attestation. This check never mutates a
snapshot and fails when its recorded history or ancestry cannot be verified.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import re
import subprocess


def historical_transition_bytes_match(root: Path, manifest_path: str, handoff_path: str) -> bool:
    try:
        for value in (manifest_path, handoff_path):
            if Path(value).is_absolute() or '..' in Path(value).parts:
                raise ValueError('Unsafe control path')
        raw=(root/manifest_path).read_bytes()
        snapshot=json.loads(raw)
        handoff=json.loads((root/handoff_path).read_bytes())
        release=handoff['production_release']
        revision, merged=release['reviewed_head_sha'], release['merge_sha']
        if not all(isinstance(s,str) and re.fullmatch(r'[a-f0-9]{40}',s) for s in (revision,merged)):
            raise ValueError('Missing exact historical source/merge SHA')
        def git(*args):
            return subprocess.run(['git',*args],cwd=root,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True).stdout
        git('merge-base','--is-ancestor',revision,merged)
        git('merge-base','--is-ancestor',merged,'HEAD')
        if git('show',revision+':'+manifest_path) != raw:
            raise ValueError('Immutable historical snapshot has changed since its reviewed release')
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
            raise ValueError('Historical snapshot hashes disagree with recorded revision: '+', '.join(mismatches))
        print(f'HISTORICAL TRANSITION: PASS — {len(rows)} hashes at {revision}; current files are not overwritten')
        return True
    except (OSError,ValueError,KeyError,TypeError,subprocess.CalledProcessError) as exc:
        print('HISTORICAL TRANSITION: FAIL —',str(exc))
        return False
