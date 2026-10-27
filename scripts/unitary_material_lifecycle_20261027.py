"""Fail-closed, source-qualified material lifecycle for the October 2026 live audit.

The September Cuatrecasas entry is *historical* pending-publication evidence;
the current pending cohort is the distinct Madrid/CTBG October 25 source. This
module never promotes a registered filing, released URL, or material status.
"""
from __future__ import annotations

HISTORICAL_ID = "PD-CUATRECASAS-ETJ-DP748-20260918-01"
HISTORICAL_SHA = "cf73bd7cffd65ad08f48d3cc850b692fc17aec23"
CURRENT_ID = "PD-MADRID-CTBG-REGISTERED-20261025"
CURRENT_INPUT = "assets/data/institutional-communications-20261025.json"
CURRENT_STATES = {
    "PREPARED_SOURCE_VERIFIED_NOT_DEPLOYED",
    "PREPARED_PENDING_MERGE",
    "MERGED_AWAITING_PAGES_READBACK",
}
HISTORICAL_ROUTES = {
    "/en/cuatrecasas-etj163-dp748-18-september-2026/",
    "/es/cuatrecasas-etj163-dp748-18-septiembre-2026/",
    "/en/updates/",
    "/es/actualizaciones/",
}
CURRENT_ROUTES = {
    "/es/incentivos-regionales-gc836-p06/",
    "/en/regional-incentives-gc836-p06/",
    "/es/actualizaciones/",
    "/en/updates/",
}


def valid_material_stage(material, expected_date, current_control,
                         source_material=None):
    """Return false on mismatched source/current/history or unproven promotion.

    source_material, when given, is the repository's authenticated candidate;
    'material' is the independently fetched public-state projection.
    """
    if not isinstance(material, dict) or not isinstance(current_control, dict):
        return False
    latest = material.get("repository_latest_material_date")
    live = material.get("last_live_verified_material_date")
    if (latest != expected_date or material.get("latest_material_date") != latest
            or not isinstance(live, str) or live > latest):
        return False
    parity = (f"{latest}_LIVE_VERIFIED" if live == latest
              else f"REPOSITORY_{latest}_PENDING_PUBLICATION_LAST_LIVE_VERIFIED_{live}")
    if material.get("public_parity") != parity:
        return False
    history = material.get("pending_publication_history")
    if not isinstance(history, list):
        return False
    matches = [v for v in history if isinstance(v, dict)
               and v.get("control_id") == HISTORICAL_ID]
    if len(matches) != 1:
        return False
    previous = matches[0]
    if (previous.get("state") != "MERGED_AWAITING_PAGES_READBACK"
            or previous.get("material_date") != "2026-09-18"
            or previous.get("merge_sha") != HISTORICAL_SHA
            or previous.get("merged_to") != "main"
            or previous.get("controlling_pr") != 1548
            or not HISTORICAL_ROUTES.issubset(set(previous.get("routes") or []))):
        return False
    if source_material is not None:
        if not isinstance(source_material, dict):
            return False
        if (history != source_material.get("pending_publication_history")
                or material.get("pending_publication")
                   != source_material.get("pending_publication")
                or live != source_material.get("last_live_verified_material_date")
                or parity != source_material.get("public_parity")):
            return False
    if live != latest:
        pending = material.get("pending_publication")
        if not isinstance(pending, dict) or pending.get("control_id") != CURRENT_ID:
            return False
        if (pending.get("material_date") != expected_date
                or pending.get("source_input") != CURRENT_INPUT
                or current_control.get("control_id") != CURRENT_ID
                or not CURRENT_ROUTES.issubset(set(pending.get("routes") or []))
                or pending.get("state") not in CURRENT_STATES):
            return False
        if pending["state"] == "MERGED_AWAITING_PAGES_READBACK":
            sha = pending.get("merge_sha")
            if (not isinstance(sha, str) or len(sha) != 40
                    or any(c not in "0123456789abcdef" for c in sha)
                    or pending.get("merged_to") != "main"):
                return False
        elif pending.get("merge_sha") or pending.get("merged_to"):
            return False
    return True
