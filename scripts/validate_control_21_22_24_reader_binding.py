#!/usr/bin/env python3
"""Fail-closed cross-validator for PD-C212224-001 and its three-track reader layer."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "assets/data/control-21-22-24-continuity-v1.json"
READER = ROOT / "data/three-track-full-digitisation-20260904.json"


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def load(path: Path):
    if not path.is_file():
        fail(f"missing required file: {path.relative_to(ROOT)}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"invalid JSON in {path.relative_to(ROOT)}: {exc}")


def route(path: str) -> str:
    prefix = "/por-derecho"
    return path[len(prefix):] if path.startswith(prefix) else path


def main() -> None:
    canonical = load(CANONICAL)
    reader = load(READER)

    if canonical.get("control_id") != "PD-C212224-001":
        fail("unexpected canonical control_id")
    if reader.get("control_id") != "PD-THREE-TRACK-DIGITISATION-20260904-01":
        fail("unexpected reader-layer control_id")

    controls = {item.get("id"): item for item in canonical.get("controls", [])}
    for control_id in ("CONTROL-21", "CONTROL-22", "CONTROL-24"):
        if control_id not in controls:
            fail(f"canonical control missing: {control_id}")

    if controls["CONTROL-21"].get("bridge_status") != "UNVERIFIED_CANDIDATE_BRIDGE":
        fail("canonical Control 21 -> DP 1901 bridge was upgraded")
    if controls["CONTROL-22"].get("bridge_status") != "UNVERIFIED_CANDIDATE_BRIDGE":
        fail("canonical Control 22 -> DP 1956 bridge was upgraded")

    c24 = controls["CONTROL-24"]
    if c24.get("formal_destination_status") != "UNKNOWN":
        fail("canonical Control 24 formal destination was upgraded")
    if c24.get("supplement_status") != "DEPENDENT_SAME_RECORD":
        fail("canonical Control 24 supplement no longer remains within one Reg. No. 24 record")
    presumed = c24.get("expected_or_presumed_route", "")
    if "TSJ Canarias / TSJC" not in presumed or "not verified" not in presumed:
        fail("canonical Control 24 TSJC route is not preserved as presumed/unverified")
    if c24.get("trace_status") != "ACTIVE_TRACE_REQUESTED":
        fail("canonical Control 24 active trace state drifted")

    continuity = reader.get("continuity_governance", {})
    if continuity.get("control_id") != "PD-C212224-001":
        fail("reader layer is not bound to PD-C212224-001")
    if continuity.get("canonical_state") != "assets/data/control-21-22-24-continuity-v1.json":
        fail("reader layer points to the wrong canonical state")

    bindings = continuity.get("track_bindings", {})
    if bindings.get("DP1901-C21", {}).get("bridge_status") != "UNVERIFIED_CANDIDATE_BRIDGE":
        fail("reader layer upgraded Control 21 -> DP 1901")
    if bindings.get("DP1956-C22", {}).get("bridge_status") != "UNVERIFIED_CANDIDATE_BRIDGE":
        fail("reader layer upgraded Control 22 -> DP 1956")
    c24_binding = bindings.get("C24-JUDGE", {})
    if c24_binding.get("formal_destination_status") != "UNKNOWN":
        fail("reader layer upgraded Control 24 formal destination")
    if c24_binding.get("bridge_status") != "UNVERIFIED_CANDIDATE_BRIDGE":
        fail("reader layer changed Control 24 bridge state")

    same_date = continuity.get("same_date_safeguard", {})
    if same_date.get("control_21_object") != "CONTROL-21-OBJECT-20260625":
        fail("reader-layer Control 21 25 June object id drifted")
    if same_date.get("control_24_amplification") != "CONTROL-24-AMPLIACION-20260625":
        fail("reader-layer Control 24 25 June supplement id drifted")
    if same_date.get("control_21_object") == same_date.get("control_24_amplification"):
        fail("Control 21 and Control 24 25 June document objects collapsed")
    if same_date.get("bridge_status") != "NO_BRIDGE":
        fail("NO_BRIDGE safeguard between the two 25 June document objects was removed")

    layers = canonical.get("reader_layers", [])
    if len(layers) != 1:
        fail("canonical graph must contain exactly one bound three-track reader layer")
    layer = layers[0]
    if layer.get("control_id") != "PD-THREE-TRACK-DIGITISATION-20260904-01":
        fail("canonical reader-layer control id drifted")
    if layer.get("path") != "data/three-track-full-digitisation-20260904.json":
        fail("canonical reader-layer path drifted")
    if layer.get("relationship") != "BOUND_READER_LAYER":
        fail("canonical reader layer is not explicitly bound")

    tracks = {item.get("track_id"): item for item in reader.get("tracks", [])}
    if set(tracks) != {"DP1901-C21", "DP1956-C22", "C24-JUDGE"}:
        fail("reader layer must preserve exactly the three controlled tracks")

    c24_track = tracks["C24-JUDGE"]
    status = c24_track.get("status_control", {})
    if status.get("official_case_number") is not None or status.get("nig") is not None or status.get("assigned_court") is not None:
        fail("reader layer assigned an unverified official Control 24 destination")
    if "formal allocation unknown" not in c24_track.get("procedure", "").casefold():
        fail("reader layer no longer states that Control 24 formal allocation is unknown")
    if "dependent supplement" not in c24_track.get("supplement", {}).get("relationship", "").casefold():
        fail("reader layer no longer treats the 25 June Control 24 document as dependent")

    aliases = set(canonical.get("aliases", []))
    for alias in ("DP1901-C21", "DP1956-C22", "C24-JUDGE", "PD-THREE-TRACK-DIGITISATION-20260904-01"):
        if alias not in aliases:
            fail(f"canonical reader-layer alias missing: {alias}")

    routes = canonical.get("public_routes", {})
    expected = {
        "READER_DP-1901_EN": route(tracks["DP1901-C21"].get("public_route_en", "")),
        "READER_DP-1901_ES": route(tracks["DP1901-C21"].get("public_route_es", "")),
        "READER_DP-1956_EN": route(tracks["DP1956-C22"].get("public_route_en", "")),
        "READER_DP-1956_ES": route(tracks["DP1956-C22"].get("public_route_es", "")),
        "READER_CONTROL-24_EN": route(c24_track.get("public_route_en", "")),
        "READER_CONTROL-24_ES": route(c24_track.get("public_route_es", "")),
    }
    for key, value in expected.items():
        if routes.get(key) != value:
            fail(f"canonical/reader route drift for {key}: {routes.get(key)!r} != {value!r}")

    print("PASS: PD-C212224-001 and PD-THREE-TRACK-DIGITISATION-20260904-01 are mutually bound while Reg. No. 24 remains filed-but-untraced, TSJC presumed/unverified, and Control 21/22 bridges remain unverified")


if __name__ == "__main__":
    main()
