#!/usr/bin/env python3
"""Command-line entry point for the Por Derecho LegalTech Uría release gate."""
from __future__ import annotations

import sys

from legaltech_uria_search_graph_validation import run


def main() -> int:
    errors, metrics = run()
    if errors:
        print("LEGALTECH URÍA SEARCH/GRAPH GATE: FAIL")
        for error in errors:
            print(f" - {error}")
        return 1
    print(
        "LEGALTECH URÍA SEARCH/GRAPH GATE: PASS "
        f"({metrics['canonical_objects']} canonical objects; {metrics['graph_nodes']} graph nodes; "
        f"{metrics['events']} events; {metrics['review_candidates']} review candidates; "
        f"{metrics['evidence_selections']} evidence selections; {metrics['matrix_rows']} matrix rows)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
