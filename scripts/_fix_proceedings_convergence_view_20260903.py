#!/usr/bin/env python3
"""Keep the current convergence-view wording aligned with the audited corridor contract.

This fixer runs after the current-state reintegration manifest is generated. Because it
lawfully changes the schema candidate byte, it also refreshes only that schema entry in
the current reintegration transition. Historical publication manifests remain immutable.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INTERLINK = ROOT / "assets/data/proceedings-interlinkability-v1.json"
SCHEMA = ROOT / "assets/data/proceedings-interconnectivity-schema-v1.json"
REINTEGRATION_MANIFEST = ROOT / "publication-manifests/historic-proceedings-authority-reintegration-20260903.json"

inter = json.loads(INTERLINK.read_text(encoding="utf-8"))
coverage = inter.get("coverage") or {}
clusters = int(coverage.get("context_cluster_count", 0))
if clusters <= 0:
    raise SystemExit("missing positive context_cluster_count")

schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
views = schema.setdefault("implemented_public_views", {})
views["CONVERGENCE_CLUSTER"] = (
    f"{clusters} source-controlled material clusters and 1 source-controlled corridor: "
    "recorded Connection groups, the bounded source-controlled corridor and Case Prism propositions; "
    "Stream and Geography remain taxonomy only"
)
SCHEMA.write_text(json.dumps(schema, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

manifest = json.loads(REINTEGRATION_MANIFEST.read_text(encoding="utf-8"))
schema_rel = str(SCHEMA.relative_to(ROOT))
rows = [
    row for row in manifest.get("transitions", [])
    if isinstance(row, dict) and row.get("resource") == schema_rel
]
if len(rows) != 1:
    raise SystemExit("reintegration manifest lacks one controlled schema transition row")
rows[0]["candidate_sha256"] = hashlib.sha256(SCHEMA.read_bytes()).hexdigest()
REINTEGRATION_MANIFEST.write_text(
    json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print("CONVERGENCE_VIEW_OK", clusters, 1, "TRANSITION_HASH_REFRESHED")
