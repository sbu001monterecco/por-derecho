#!/usr/bin/env python3
"""Render the bilingual public methodology transparency projection.

This builder is deliberately deterministic and public-safe. It consumes only the
public methodology model; it never reads private evidence or source locators.
"""
import argparse, html, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MODEL=ROOT/"assets/data/methodology-transparency-v1.json"
EXPECTED_STAGE_IDS=["observe","manifest","compare","classify","traverse","adversarial","reconcile","verify","deploy","readback","envelope"]

def load_model():
    return json.loads(MODEL.read_text(encoding="utf-8"))

def validate_model(m):
    ids=[x["id"] for x in m["recursive_sequence"]]
    if ids!=EXPECTED_STAGE_IDS:
        raise ValueError(f"method stage order drift: observed={ids} expected={EXPECTED_STAGE_IDS}")
    if m.get("public_release_approved") is not False or m.get("live_verified") is not False:
        raise ValueError("candidate builder cannot claim publication approval or live verification")
    if m["constitutional"].get("safeguards_self_modify") is not False:
        raise ValueError("constitutional safeguards cannot self-modify")
    if m["constitutional"].get("no_numeric_truth_score") is not True:
        raise ValueError("numeric truth-score prohibition missing")
    return m

def semantic_projection(lang):
    m=validate_model(load_model())
    return {
        "control_id":m["control_id"],
        "lang":lang,
        "stage_ids":[x["id"] for x in m["recursive_sequence"]],
        "source_controls":m["source_controls"],
        "architecture_history":[{"date":x["date"],"status":x["status"],"control":x["control"]} for x in m["architecture_history"]],
        "publication_status":m["publication_status"],
        "public_release_approved":m["public_release_approved"],
        "live_verified":m["live_verified"],
    }

def check_rendered(lang):
    m=validate_model(load_model())
    path=ROOT/m["routes"][lang]
    text=path.read_text(encoding="utf-8")
    last=-1
    for order,stage_id in enumerate(EXPECTED_STAGE_IDS,1):
        token=f'data-method-stage="{stage_id}" data-method-order="{order}"'
        pos=text.find(token)
        if pos<0 or pos<=last:
            raise ValueError(f"rendered stage missing/out of order: {stage_id}")
        last=pos
    required=[
        f'data-methodology-control="{m["control_id"]}"',
        'data-publication-status="PUBLIC_SAFE_CANDIDATE"',
        'data-private-boundary="true"',
        'data-live-verified="false"',
    ]
    for token in required:
        if token not in text:
            raise ValueError(f"rendered methodology marker missing: {token}")
    return path

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--check",action="store_true")
    p.add_argument("--host",choices=["github","gitlab"],default="github")
    args=p.parse_args()
    m=validate_model(load_model())
    if args.check:
        for lang in ("en","es"): check_rendered(lang)
        print(json.dumps({"status":"PASS","control_id":m["control_id"],"host":args.host,"languages":["en","es"],"stages":len(EXPECTED_STAGE_IDS)},sort_keys=True))
        return
    raise SystemExit("Initial candidate is already rendered. Use --check; future successors may extend this builder to emit bytes after review.")

if __name__=="__main__": main()
