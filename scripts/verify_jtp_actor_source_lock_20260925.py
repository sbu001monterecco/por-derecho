#!/usr/bin/env python3
"""Static fail-closed audit of the JTP exact-actor source lock."""
from pathlib import Path
import hashlib, json
ROOT=Path(__file__).resolve().parents[1]
LOCK=ROOT/"ops/jtp/JTP_ACTOR_IMAGE_SOURCE_LOCK_20260925.json"
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
lock=json.loads(LOCK.read_text())
for key,row in lock["actors"].items():
    p=ROOT/row["path"]
    if not p.is_file() or p.is_symlink(): raise SystemExit("missing/unsafe actor asset: "+key)
    if sha(p)!=row["sha256"]: raise SystemExit("actor hash mismatch: "+key)
if set(lock["actors"])!={"jtp","borja","jdam","lpam","alberto"}: raise SystemExit("actor set changed")
if lock["validated_working_output"]["changed_pixels_outside_authorised_boxes"]!=0: raise SystemExit("invalid working-output boundary")
if lock["validated_working_output"]["jtp_region_unchanged"] is not True: raise SystemExit("JTP preservation lock lost")
print("JTP_EXACT_ACTOR_SOURCE_LOCK_PASS")
