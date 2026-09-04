#!/usr/bin/env python3
"""Production smoke v2: preserve route checks while testing the current loader contract.

The legacy smoke suite remains the source of route/marker coverage.  This wrapper
replaces only the historical global-loader assertion, which previously required
an August Treasury loader to be referenced directly from assets/site.js even
after the root loader became a delegated chain.
"""
from __future__ import annotations

import production_smoke_check as legacy


def apply_current_loader_contract() -> None:
    for check in legacy.CHECKS:
        if check.get("kind") != "global_loader":
            continue
        check["kind"] = "global_loader_delegated_contract"
        check["markers"] = [
            "const load =",
            "document.head.appendChild",
            "loadMatkator8584Release",
            "loadControl2224Release",
        ]
        check["min_bytes"] = 700
        return
    raise RuntimeError("legacy production smoke suite no longer exposes global_loader")


if __name__ == "__main__":
    apply_current_loader_contract()
    raise SystemExit(legacy.main())
