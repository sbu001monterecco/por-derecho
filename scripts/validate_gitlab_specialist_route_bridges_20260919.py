#!/usr/bin/env python3
"""Validate specialist public GitLab route continuity bridges."""
from __future__ import annotations

import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
CONTROL = ROOT / "ops" / "continuity" / "GITLAB_SPECIALIST_ROUTE_BRIDGES_20260919.json"

EXPECTED_SLUGS = {
    "orion-transparency-memorandum",
    "portfolio-international-nexus",
    "portfolio-board-open-letter",
    "canary-presidency-records-coordination",
    "media-travel-asset-recovery",
    "new-horizons-source-images",
    "actua-to-title-documentary-journey",
    "sun-park-history",
}
BOUNDARY = "does not reproduce or reconstruct unavailable GitLab source"
BASE = "https://sbu001monterecco.github.io/por-derecho/"


def validate() -> list[str]:
    failures: list[str] = []
    data = json.loads(CONTROL.read_text(encoding="utf-8"))

    if data.get("schema") != "por-derecho.gitlab-specialist-route-bridges.v1":
        failures.append("schema_mismatch")
    if data.get("status") != "FUNCTIONAL_GITHUB_BRIDGES_EXACT_GITLAB_SOURCE_PENDING":
        failures.append("status_mismatch")
    if data.get("authenticated_gitlab_restoration_verified") is not False:
        failures.append("authenticated_gitlab_restoration_must_remain_false")

    items = data.get("items") or []
    slugs = {item.get("slug") for item in items}
    if slugs != EXPECTED_SLUGS:
        failures.append("slug_set_mismatch")

    for item in items:
        slug = item.get("slug", "")
        if item.get("status") != "FUNCTIONAL_GITHUB_EQUIVALENT":
            failures.append(f"status_not_functional:{slug}")
        en_target = item.get("canonical_en", "")
        es_target = item.get("canonical_es", "")
        for lang, target in (("en", en_target), ("es", es_target)):
            if not target.startswith(f"{lang}/") or not target.endswith("/"):
                failures.append(f"target_shape_invalid:{slug}:{lang}")
                continue
            target_file = ROOT / target / "index.html"
            if not target_file.is_file():
                failures.append(f"target_missing:{slug}:{target}")

        bridge = ROOT / "en" / slug / "index.html"
        if not bridge.is_file():
            failures.append(f"bridge_missing:{slug}")
            continue
        text = bridge.read_text(encoding="utf-8")
        if 'meta name="robots" content="noindex,follow"' not in text:
            failures.append(f"bridge_not_noindex:{slug}")
        expected_canonical = BASE + en_target
        match = re.search(r'<link rel="canonical" href="([^"]+)">', text)
        if not match or match.group(1) != expected_canonical:
            failures.append(f"bridge_canonical_mismatch:{slug}")
        if BOUNDARY.lower() not in text.lower():
            failures.append(f"bridge_boundary_missing:{slug}")
        if "exact GitLab source recovery" in text and "does not" not in text.lower():
            failures.append(f"bridge_exact_recovery_claim:{slug}")

    for path in (
        ROOT / "en" / "gitlab-public-gap-map" / "index.html",
        ROOT / "es" / "mapa-brechas-publicas-gitlab" / "index.html",
    ):
        if not path.is_file():
            failures.append(f"gap_map_missing:{path.relative_to(ROOT)}")

    rules = " ".join(data.get("rules", [])).lower()
    for token in (
        "not exact gitlab source recovery",
        "noindex",
        "rendered gitlab html",
        "current github source-controlled facts supersede",
        "authenticated restoration",
    ):
        if token not in rules:
            failures.append(f"rule_missing:{token}")

    return failures


def main() -> int:
    failures = validate()
    print(json.dumps({
        "schema": "por-derecho.gitlab-specialist-route-bridges-validation.v1",
        "status": "PASS" if not failures else "FAIL",
        "control": str(CONTROL.relative_to(ROOT)),
        "failures": failures,
    }, indent=2, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
