#!/usr/bin/env python3
"""Keep the current convergence-view wording aligned with the audited corridor contract."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INTERLINK = ROOT / "assets/data/proceedings-interlinkability-v1.json"
SCHEMA = ROOT / "assets/data/proceedings-interconnectivity-schema-v1.json"

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
print("CONVERGENCE_VIEW_OK", clusters, 1)
