#!/usr/bin/env python3
"""Resolve repository-local JavaScript dependencies without freezing loader depth.

This is a literal-reference source contract, not a JavaScript execution engine.
Browser checks separately prove execution. Comments never create dependencies;
missing files, escaping paths and dynamic template expressions are not edges.
"""
from __future__ import annotations
from collections import deque
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
_JS_REFERENCE = re.compile(r"(?P<quote>['\"`])(?P<value>(?!https?:|//)[^'\"`\n]*?\.js(?:\?[^'\"`\n]*)?)(?P=quote)")
_TOKENS = re.compile(r"'(?:\\.|[^'\\])*'|\"(?:\\.|[^\"\\])*\"|`(?:\\.|[^`\\])*`|//[^\n]*|/\*.*?\*/", re.DOTALL)


def source_without_comments(text: str) -> str:
    return _TOKENS.sub(lambda m: '\n' * m[0].count('\n') if m[0].startswith(('//', '/*')) else m[0], text)


def _repo_path(value: str | Path) -> str:
    path = Path(value)
    if path.is_absolute() or '..' in path.parts:
        raise ValueError(f'Expected a safe repository-relative path: {value!r}')
    return path.as_posix()


def _source_path(value: str | Path, root: Path) -> Path | None:
    path = (root / _repo_path(value)).resolve()
    if not path.is_relative_to(root.resolve()) or not path.is_file():
        return None
    return path


def local_loader_references(source: str | Path, *, root: Path = ROOT) -> tuple[str, ...]:
    source_path = _source_path(source, root)
    if source_path is None:
        return ()
    body = source_without_comments(source_path.read_text(encoding='utf-8'))
    references: set[str] = set()
    for match in _JS_REFERENCE.finditer(body):
        clean = match['value'].split('#', 1)[0].split('?', 1)[0]
        if not clean or '${' in clean:
            continue
        candidate = ((root.resolve() / clean.lstrip('/')) if clean.startswith('/') else source_path.parent / clean).resolve()
        if not candidate.is_relative_to(root.resolve()) or candidate.suffix != '.js' or not candidate.is_file():
            continue
        references.add(candidate.relative_to(root.resolve()).as_posix())
    return tuple(sorted(references))


def find_loader_path(source: str | Path, target: str | Path, *, root: Path = ROOT) -> tuple[str, ...] | None:
    source_rel, target_rel = _repo_path(source), _repo_path(target)
    if _source_path(source_rel, root) is None or _source_path(target_rel, root) is None:
        return None
    queue = deque([(source_rel, (source_rel,))])
    visited = {source_rel}
    while queue:
        node, path = queue.popleft()
        if node == target_rel:
            return path
        for child in local_loader_references(node, root=root):
            if child not in visited:
                visited.add(child)
                queue.append((child, (*path, child)))
    return None


def reachable_loader_text(source: str | Path = 'assets/site.js', *, root: Path = ROOT) -> str:
    """Actual reachable source for legacy marker assertions; not a directory scan."""
    start = _repo_path(source)
    if _source_path(start, root) is None:
        raise ValueError(f'Missing source loader: {start}')
    queue = deque([start]); visited: set[str] = set(); parts: list[str] = []
    while queue:
        node = queue.popleft()
        if node in visited:
            continue
        visited.add(node)
        parts.append(source_without_comments((root/node).read_text(encoding='utf-8')))
        queue.extend(local_loader_references(node, root=root))
    return '\n'.join(parts)


def require_loader_path(errors: list[str], source: str | Path, target: str | Path, message: str, *, root: Path = ROOT) -> tuple[str, ...] | None:
    path = find_loader_path(source, target, root=root)
    if path is None:
        errors.append(message)
    return path


def format_loader_path(path: tuple[str, ...] | None) -> str:
    return ' -> '.join(path or ())
