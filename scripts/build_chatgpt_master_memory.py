#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "assets/data/chatgpt-master-memory-v1.json"
OUT = ROOT / "governance/chatgpt-memory/MASTER_MEMORY_COMPACT.txt"

data = json.loads(SRC.read_text(encoding="utf-8"))
text = "\n\n".join(data["compact_sections"]).strip() + "\n"
if "--write" in __import__("sys").argv:
    OUT.write_text(text, encoding="utf-8")
else:
    current = OUT.read_text(encoding="utf-8")
    if current != text:
        raise SystemExit("PD-MEM-001 compact projection drift")
print("PD-MEM-001 compact projection OK")
