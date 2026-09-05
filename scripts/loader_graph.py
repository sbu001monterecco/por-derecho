#!/usr/bin/env python3
"""Resolve local JavaScript loader reachability from repository source.

Por Derecho's shared site loader is intentionally layered: each release preserves
its predecessor and adds new scoped modules. Validators must therefore prove that
a required loader remains reachable through the current graph, not require that a
historic predecessor continue to be named directly by ``assets/site.js``.
"""
from __future__ import annotations

import re
from collections import deque
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

# Local loader references are expressed as quoted strings in ``new URL(...)``
# calls and in the shared ``load('file.js', ...)`` helper. Comments in the
# repository name files without quotes, so they do not create false graph edges.
_JS_REFERENCE = re.compile(
    r"(?P<quote>['\"`])(?P<value>(?!https?:|//)[^'\"`\n]*?\.js(?:\?[^'\"`\n]*)?)(?P=quote)"
)


def _repo_path(value: str | Path) -> str:
    return Path(value).as_posix().lstrip("./")


def local_loader_references(source: str | Path, *, root: Path = ROOT) -> tuple[str, ...]:
    """Return existing repository-local JavaScript files referenced by ``source``."""
    source_rel = _repo_path(source)
    source_path = (root / source_rel).resolve()
    root_resolved = root.resolve()
    if not source_path.is_file():
        return ()

    try:
        body = source_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return ()

    references: set[str] = set()
    for match in _JS_REFERENCE.finditer(body):
        raw = match.group("value")
        clean = raw.split("#", 1)[0].split("?", 1)[0]
        if not clean or "${" in clean:
            continue
        if clean.startswith("/"):
            candidate = (root_resolved / clean.lstrip("/")).resolve()
        else:
            candidate = (source_path.parent / clean).resolve()
        try:
            candidate.relative_to(root_resolved)
        except ValueError:
            continue
        if candidate.suffix != ".js" or not candidate.is_file():
            continue
        references.add(candidate.relative_to(root_resolved).as_posix())
    return tuple(sorted(references))


def find_loader_path(
    source: str | Path,
    target: str | Path,
    *,
    root: Path = ROOT,
) -> tuple[str, ...] | None:
    """Return one shortest local-loader path from ``source`` to ``target``."""
    source_rel = _repo_path(source)
    target_rel = _repo_path(target)
    if source_rel == target_rel:
        return (source_rel,)
    if not (root / source_rel).is_file() or not (root / target_rel).is_file():
        return None

    queue: deque[tuple[str, tuple[str, ...]]] = deque([(source_rel, (source_rel,))])
    visited = {source_rel}
    while queue:
        node, path = queue.popleft()
        for child in local_loader_references(node, root=root):
            if child == target_rel:
                return (*path, child)
            if child in visited:
                continue
            visited.add(child)
            queue.append((child, (*path, child)))
    return None


def require_loader_path(
    errors: list[str],
    source: str | Path,
    target: str | Path,
    message: str,
    *,
    root: Path = ROOT,
) -> tuple[str, ...] | None:
    """Append ``message`` when the target is not transitively reachable."""
    path = find_loader_path(source, target, root=root)
    if path is None:
        errors.append(message)
    return path


def format_loader_path(path: tuple[str, ...] | None) -> str:
    return " -> ".join(path or ())
