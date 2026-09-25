#!/usr/bin/env python3
from pathlib import Path
import json, sys

ROOT=Path(__file__).resolve().parents[1]
CONTRACT=ROOT/"ops/publication/HOMEPAGE_PUBLICATION_CONTRACT_20260925.json"
errors=[]

try:
    cfg=json.loads(CONTRACT.read_text(encoding="utf-8"))
except Exception as e:
    raise SystemExit(f"cannot read homepage contract: {e}")

for rel in cfg["required_routes"]:
    p=ROOT/rel
    if not p.is_file():
        errors.append(f"missing required homepage destination: {rel}")

def check_home(lang):
    rel=cfg["homepage_files"][lang]
    p=ROOT/rel
    if not p.is_file():
        errors.append(f"missing homepage: {rel}")
        return
    raw=p.read_bytes()
    text=raw.decode("utf-8")
    if len(raw) > cfg["byte_budget"][lang]:
        errors.append(f"{rel} exceeds byte budget: {len(raw)} > {cfg['byte_budget'][lang]}")
    for token in cfg[f"required_{lang}"]:
        if token not in text:
            errors.append(f"{rel} missing contract token: {token}")
    for token in cfg[f"forbidden_{lang}"]:
        if token in text:
            errors.append(f"{rel} contains forbidden homepage token: {token}")
    if lang=="en" and 'href="future/"' not in text:
        errors.append("EN Future route missing")
    if lang=="es" and 'href="futuro/"' not in text:
        errors.append("ES Futuro route missing")

check_home("en"); check_home("es")

if errors:
    print("HOMEPAGE PUBLICATION CONTRACT: FAIL")
    for e in errors: print("-",e)
    sys.exit(1)
print("HOMEPAGE PUBLICATION CONTRACT: PASS")
