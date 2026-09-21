#!/usr/bin/env python3
"""Reject stale DIP 80 blocked-publication state after the casebook was merged."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "publication-manifests" / "icalpa-dip80-open-kimono-20260818.json"

EXPECTED_PR = 525
EXPECTED_MERGE = "e81a3ec5e4791b978f69b932c786233e7cf552c4"
HISTORICAL_PR = 352
REQUIRED_EVENTS = {
    "CASEBOOK_SOURCE_MERGED",
    "SECOND_PAIR_FRAMEWORK_ADDED",
    "SECOND_PAIR_ACTIVATED_ON_DIP80",
    "PONENTE_VIEW_UPGRADED",
    "PUBLIC_EDGE_VERIFICATION_ADDED",
    "PUBLIC_EDGE_VERIFIED",
    "LIVE_STATUS_CLOSEOUT_RECORDED",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    try:
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
        require(data.get("publication_id") == "ICALPA-DIP80-OPEN-KIMONO-20260818", "unexpected publication ID")
        require(data.get("current_state") == "LIVE_VERIFIED", "current DIP 80 publication state must be LIVE_VERIFIED")
        require(data.get("controlling_pr") == EXPECTED_PR, "PR #525 must control current publication lineage")
        require(data.get("controlling_merge_sha") == EXPECTED_MERGE, "wrong DIP 80 controlling merge SHA")

        historical = data.get("historical_blocked_state") or {}
        require(historical.get("state") == "BLOCKED_RECOVERY", "historical blocked state must remain preserved")
        require(historical.get("controlling_pr") == HISTORICAL_PR, "historical PR #352 provenance missing")
        require((historical.get("superseded_by") or {}).get("pr") == EXPECTED_PR, "historical blocked state not superseded by PR #525")
        require((historical.get("superseded_by") or {}).get("merge_sha") == EXPECTED_MERGE, "historical supersession SHA mismatch")

        events = {item.get("event") for item in data.get("implementation_lineage", []) if isinstance(item, dict)}
        require(REQUIRED_EVENTS <= events, f"DIP 80 lineage events missing: {sorted(REQUIRED_EVENTS - events)}")

        route_count = 0
        for lang in ("es", "en"):
            routes = (data.get("current_routes") or {}).get(lang)
            require(isinstance(routes, list) and len(routes) >= 8, f"expected at least eight {lang} casebook routes")
            for rel in routes:
                path = ROOT / rel
                require(path.is_file(), f"missing DIP 80 route: {rel}")
                text = path.read_text(encoding="utf-8", errors="replace")
                require("noindex,follow,noarchive" in text, f"DIP 80 route lost noindex boundary: {rel}")
                route_count += 1

        for rel in data.get("current_source_files", []):
            require((ROOT / rel).is_file(), f"missing DIP 80 source file: {rel}")

        privacy = data.get("privacy_review") or {}
        require(privacy.get("state") == "OPEN_P0_LEGACY_REMEDIATION", "legacy privacy remediation must remain explicit")
        require("provider-specific" in str(privacy.get("next_action", "")), "provider-identifier remediation action missing")

        require("BLOCKED_RECOVERY" not in json.dumps({"current_state": data.get("current_state")}), "blocked state leaked into current publication state")

        print("DIP 80 PUBLICATION LINEAGE: PASS")
        print(f" - current controlling PR: #{EXPECTED_PR}")
        print(f" - historical blocked PR preserved: #{HISTORICAL_PR}")
        print(f" - current routes checked: {route_count}")
        print(" - noindex boundary: preserved")
        print(" - legacy privacy remediation: explicitly open")
        return 0
    except (AssertionError, json.JSONDecodeError) as exc:
        print(f"DIP 80 PUBLICATION LINEAGE: FAIL\n - {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
