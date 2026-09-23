#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEM = json.loads((ROOT / "assets/data/chatgpt-master-memory-v1.json").read_text(encoding="utf-8"))
REQ = json.loads((ROOT / "assets/data/chatgpt-master-memory-required-controls-v1.json").read_text(encoding="utf-8"))
COMPACT = (ROOT / "governance/chatgpt-memory/MASTER_MEMORY_COMPACT.txt").read_text(encoding="utf-8")
PUBLIC = (ROOT / "governance/chatgpt-memory/MASTER_MEMORY_PUBLIC.md").read_text(encoding="utf-8")

ids = {x["id"] for x in MEM["controls"]}
missing = [x for x in REQ["required_p0"] if x not in ids]
if missing:
    raise SystemExit("Missing P0 controls: " + ", ".join(missing))

checks = {
    "ANTI_FRAGMENTATION":"ANTI-FRAGMENTATION",
    "NO_TOO_NARROW_ANALYSIS":"technically correct narrow answer",
    "SOURCE_BRIDGE_LINEAGE":"thematic overlap",
    "LIVE_REPOSITORY_REVALIDATION":"live repository",
    "AWESWELL_IDENTITY_LOCK":"AWESWELL LIMITED",
    "SEVEN_JUNE_2018_PIVOT":"7-Jun-2018",
    "EXTERNAL_ACTION_REQUIRES_AUTHORITY":"≠authority",
}
for cid, needle in checks.items():
    if needle not in COMPACT and needle not in PUBLIC:
        raise SystemExit(f"P0 projection missing {cid}: {needle}")

print(f"PD-MEM-001 OK — {len(REQ['required_p0'])}/{len(REQ['required_p0'])} P0 controls present")
