#!/usr/bin/env python3
"""Fail-closed cross-validator for PD-C212224-001 and its three-track reader layer."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "assets/data/control-21-22-24-continuity-v1.json"
READER = ROOT / "data/three-track-full-digitisation-20260904.json"
CORPUS = ROOT / "data/control-21-22-24-source-corpus-20260921.json"


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
    corpus = load(CORPUS)

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
    if controls["CONTROL-21"].get("evidential_state") != "DOCUMENTED":
        fail("canonical stamped Control 21 filing must remain documented")
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
    if c24_track.get("supplement", {}).get("pages") != 13:
        fail("reader layer Control 24 dependent supplement must remain 13 pages")
    if tracks["DP1901-C21"].get("base_filing", {}).get("pages") != 86:
        fail("reader layer private-actor base source must remain 86 pages")
    if tracks["DP1901-C21"].get("immediate_amplification", {}).get("pages") != 26:
        fail("reader layer immediate private-actor amplification must remain 26 pages")
    if tracks["DP1901-C21"].get("expansion", {}).get("pages") != 19:
        fail("reader layer 9-Jul private-actor amplification must remain 19 pages")
    if tracks["DP1956-C22"].get("base_filing", {}).get("pages") != 55:
        fail("reader layer Control 22 base complaint must remain 55 pages")
    if tracks["C24-JUDGE"].get("base_filing", {}).get("pages") != 79:
        fail("reader layer Control 24 signed package must remain 79 pages")
    if tracks["C24-JUDGE"].get("base_filing", {}).get("text_layer_processed") != "79/79 pages":
        fail("reader layer Control 24 signed package must remain processed 79/79")
    if tracks["C24-JUDGE"].get("supplement", {}).get("text_layer_processed") != "13/13 pages":
        fail("reader layer Control 24 supplement must remain processed 13/13")

    expected_sources = {
        "C21-BASE-20260625": (86, "3f4bd2bbbc963605e4cc94bc73d116157e2bf4a2266e2285b013f38de9e90736", "86/86 pages"),
        "C21-AMP-20260626": (26, "a7f057fd99d0bdf1a891cf4610f69ed19788d2e40f9f23a6ff66fc6255d97846", "26/26 pages"),
        "C21-EXP-20260709": (19, "0d42dcbe30679331c557f4c3750e478e592a9a449c6b5ecb84e32f6fa56ad16f", "19/19 pages"),
        "C22-BASE-20260618": (55, "b11f10e7410f922a8cd1796ea462ea7ea20d555b7308e4481f2cb23732b1002b", "55/55 pages"),
        "C24-BASE-20260618": (79, "1cae1912a20202c5f5779db07e77c7e1d3f0ae514676e07d3ace4dd56f6f76a0", "79/79 pages"),
        "C24-SUPP-20260625": (13, "04051e33000f830c32ba06e31996ba4e6812c7d54c199ee03696b85e68589679", "13/13 pages"),
    }
    if corpus.get("control_id") != "PD-C212224-SOURCE-CORPUS-20260921-01":
        fail("unexpected six-source corpus control_id")
    if corpus.get("totals") != {"documents": 6, "source_pages": 278, "controls": 3}:
        fail("six-source corpus totals drifted")
    docs = {item.get("id"): item for item in corpus.get("documents", [])}
    if set(docs) != set(expected_sources):
        fail("six-source corpus document set drifted")
    for doc_id, (pages, digest, processed) in expected_sources.items():
        doc = docs[doc_id]
        if doc.get("pages") != pages or doc.get("sha256") != digest or doc.get("text_layer_processed") != processed:
            fail(f"source corpus identity/coverage drift for {doc_id}")
        if doc.get("digitisation_in_git") is not True:
            fail(f"source corpus digitisation-in-git flag missing for {doc_id}")

    dossier_paths = [
        ROOT / "es/control-21-denuncia-actores-privados-25-junio-2026/index.html",
        ROOT / "es/control-22-denuncia-administrador-concursal/index.html",
        ROOT / "es/control-24-denuncia-juez-concurso-36-2012/index.html",
        ROOT / "en/control-21-private-actors-complaint-25-june-2026/index.html",
        ROOT / "en/control-22-insolvency-administrator-complaint/index.html",
        ROOT / "en/control-24-insolvency-judge-complaint-36-2012/index.html",
    ]
    for path in dossier_paths:
        if not path.is_file():
            fail(f"missing interlinked dossier: {path.relative_to(ROOT)}")
        body = path.read_text(encoding="utf-8")
        if "control-21-22-24-source-corpus-20260921.json" not in body:
            fail(f"source-corpus manifest link missing from {path.relative_to(ROOT)}")
        if "86/86 + 26/26 + 19/19" not in body or "55/55" not in body or "79/79 + 13/13" not in body:
            fail(f"six-document coverage summary missing from {path.relative_to(ROOT)}")


    frozen_expectations = {
        "C21-BASE-20260625": ("evidence/control-21/source-text/frozen/2026-06-25-ref21-base-86p.md", 86),
        "C21-AMP-20260626": ("evidence/control-21/source-text/frozen/2026-06-26-ref21-immediate-amplification-26p.md", 26),
        "C21-EXP-20260709": ("evidence/control-21/source-text/frozen/2026-07-09-ref21-expansion-19p.md", 19),
        "C22-BASE-20260618": ("evidence/control-22/source-text/frozen/2026-06-18-ref22-ac-complaint-55p.md", 55),
        "C24-BASE-20260618": ("evidence/control-24/source-text/frozen/2026-06-18-ref24-signed-package-79p.md", 79),
        "C24-SUPP-20260625": ("evidence/control-24/source-text/frozen/2026-06-25-ref24-supplement-13p.md", 13),
    }
    current_expectations = {
        "CONTROL-21": ("evidence/control-21/source-text/current/control-21-current-enhanced.md", 131),
        "CONTROL-22": ("evidence/control-22/source-text/current/control-22-current-enhanced.md", 55),
        "CONTROL-24": ("evidence/control-24/source-text/current/control-24-current-enhanced.md", 92),
    }
    for doc_id, (rel, pages) in frozen_expectations.items():
        path = ROOT / rel
        if not path.is_file():
            fail(f"missing frozen source text: {rel}")
        body = path.read_text(encoding="utf-8")
        if body.count("## Source page ") != pages:
            fail(f"frozen page-marker coverage drift for {doc_id}")
        doc = docs[doc_id]
        if doc.get("github_frozen_text") != rel or doc.get("source_text_stored_in_git") is not True:
            fail(f"frozen corpus binding missing for {doc_id}")
        if "IMMUTABLE FROZEN LAYER" not in body:
            fail(f"frozen immutability marker missing for {doc_id}")
    for control, (rel, pages) in current_expectations.items():
        path = ROOT / rel
        if not path.is_file():
            fail(f"missing living current text: {rel}")
        body = path.read_text(encoding="utf-8")
        if body.count("## Source page ") != pages:
            fail(f"living full-text page-marker coverage drift for {control}")
        if "LIVING LAYER" not in body:
            fail(f"living-layer marker missing for {control}")

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

    print("PASS: canonical continuity, three-track reader and six-source 278-page corpus are mutually bound; all six dossiers are reciprocally interlinked while procedural bridges remain source-controlled")


if __name__ == "__main__":
    main()
