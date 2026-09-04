#!/usr/bin/env python3
"""Validate the current shared JavaScript loader graph semantically."""
from __future__ import annotations

import sys

from loader_graph import find_loader_path, format_loader_path, local_loader_references


REQUIRED_PATHS = (
    (
        "assets/site.js",
        "assets/site-pre-matkator-8584-20260903.js",
        "current root loader does not preserve the immediate pre-Matkator predecessor",
    ),
    (
        "assets/site.js",
        "assets/site-pre-treasury-154-hq-20260828.js",
        "current root loader cannot reach the preserved pre-Treasury predecessor",
    ),
    (
        "assets/site.js",
        "assets/calificacion-criminal-misuse-thesis-20260824.js",
        "current root loader cannot reach the Calificación criminal-misuse module",
    ),
    (
        "assets/site.js",
        "assets/asset-recovery-preservation-20260821.js",
        "current root loader cannot reach the protected asset-recovery module",
    ),
    (
        "assets/site.js",
        "assets/cam-favourable-pattern-20260819.js",
        "current root loader cannot reach the protected CAM pattern module",
    ),
)


def main() -> int:
    errors: list[str] = []
    paths: list[tuple[str, ...]] = []

    direct = local_loader_references("assets/site.js")
    if "assets/site-pre-matkator-8584-20260903.js" not in direct:
        errors.append("assets/site.js does not directly preserve site-pre-matkator-8584-20260903.js")

    for source, target, message in REQUIRED_PATHS:
        path = find_loader_path(source, target)
        if path is None:
            errors.append(message)
        else:
            paths.append(path)

    if errors:
        print("SHARED LOADER GRAPH: FAIL")
        for error in errors:
            print(f" - {error}")
        return 1

    print("SHARED LOADER GRAPH: PASS")
    for path in paths:
        print(f" - {format_loader_path(path)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
