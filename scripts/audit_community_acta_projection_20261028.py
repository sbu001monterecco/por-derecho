#!/usr/bin/env python3
"""Read-only CI audit of a deterministic public ACTA derived graph.

Source of truth = existing builder plus current checked-out source files.
Never hand-edit target, publish or alter the source history.
"""
from __future__ import annotations

import argparse
import base64
import difflib
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = Path("assets/data/community-acta-authority-interconnectivity-v1.json")
OUTDIR = Path("artifacts/community-acta-projection-20261028")


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def run(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(args, cwd=ROOT, check=check, capture_output=True, text=True)


def walk(before, after, path=""):
    if before == after:
        return []
    if isinstance(before, dict) and isinstance(after, dict):
        results = []
        for key in sorted(set(before) | set(after)):
            where = path + "/" + str(key)
            if key not in before:
                results.append({"path": where, "kind": "ADDED_KEY"})
            elif key not in after:
                results.append({"path": where, "kind": "REMOVED_KEY"})
            else:
                results.extend(walk(before[key], after[key], where))
        return results
    if isinstance(before, list) and isinstance(after, list):
        output = []
        if len(before) != len(after):
            output.append({"path": path, "kind": "LIST_LENGTH_CHANGED",
                           "old": len(before), "new": len(after)})
        for i, (a, b) in enumerate(zip(before, after)):
            output.extend(walk(a, b, path + "/" + str(i)))
        return output
    return [{"path": path, "kind": "CONTENT_CHANGED",
             "old_repr": repr(before)[:200], "new_repr": repr(after)[:200]}]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--emit-base64", action="store_true")
    args = ap.parse_args()
    OUTDIR.mkdir(parents=True, exist_ok=True)
    previous = (ROOT / TARGET).read_bytes()
    old = json.loads(previous)
    original_head = run("git", "rev-parse", "HEAD").stdout.strip()
    original_tree = run("git", "status", "--porcelain").stdout.strip()
    if original_tree:
        raise SystemExit("Must run on clean exact repository checkout; no mutations authorised")

    generate = run(sys.executable,
                   "scripts/build_community_acta_authority_interconnectivity.py")
    print(generate.stdout.strip())
    revised = (ROOT / TARGET).read_bytes()
    new = json.loads(revised)
    validation = run(sys.executable,
                     "scripts/validate_community_acta_authority_interconnectivity.py")
    print(validation.stdout.strip())
    unittest = run(sys.executable, "-m", "unittest", "-v",
                   "scripts/test_build_community_acta_authority_interconnectivity.py")
    print(unittest.stderr.strip()[-1300:])

    modified = [p for p in run("git", "diff", "--name-only").stdout.splitlines() if p]
    if modified != [str(TARGET)]:
        raise SystemExit("Builder mutated unexpected tracked files: " + repr(modified))
    deltas = walk(old, new)
    coverage = new.get("coverage", {})
    assert coverage.get("public_acta_packages") == 20
    assert coverage.get("public_authority_files") == 49
    assert coverage.get("evidentiary_axes") == 7
    assert coverage.get("public_authority_communication_events") == 19
    assert old["schema_version"] == new["schema_version"]
    report = {
        "audit": "PD-COMMUNITY-ACTA-DETERMINISTIC-REBUILD-20261028-01",
        "state": "READ_ONLY_REGENERATED_AND_VALIDATED_NOT_PUBLISHED",
        "source_commit": original_head,
        "before_sha256": digest(previous), "after_sha256": digest(revised),
        "before_bytes": len(previous), "after_bytes": len(revised),
        "modified_tracked_files": modified,
        "schema_version": new["schema_version"],
        "old_coverage": old.get("coverage"), "new_coverage": coverage,
        "change_count": len(deltas), "change_samples": deltas[:150],
        "no_merge_or_publication": True,
    }
    (OUTDIR / "audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (OUTDIR / "regenerated.json").write_bytes(revised)
    patch = run("git", "diff", "--", str(TARGET)).stdout
    (OUTDIR / "source-diff.patch").write_text(patch, encoding="utf-8")
    print("ACTA_PROJECTION_AUDIT " + json.dumps({
        "before_sha256": report["before_sha256"],
        "after_sha256": report["after_sha256"],
        "changes": len(deltas),
        "before_bytes": len(previous), "after_bytes": len(revised),
        "denominators": coverage,
        "status": "DIAGNOSTIC_ONLY_SOURCE_VALIDATED",
    }, separators=(",", ":")))
    if args.emit_base64:
        if len(revised) > 1_000_000:
            raise SystemExit("Refusing to emit unexpectedly large generated payload")
        encoded = base64.b64encode(revised).decode("ascii")
        width = 4000
        chunks = [encoded[i:i+width] for i in range(0, len(encoded), width)]
        print(f"ACTA_OUTPUT_BEGIN sha256={digest(revised)} bytes={len(revised)} parts={len(chunks)}")
        for index, chunk in enumerate(chunks, start=1):
            print(f"ACTA_OUTPUT_B64_PART {index}/{len(chunks)}:{chunk}")
        print("ACTA_OUTPUT_END")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
