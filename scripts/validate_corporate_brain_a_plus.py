#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "ops" / "corporate-brain" / "A_PLUS_DEPLOYMENT_STATUS_20260929.json"
EVALS = ROOT / "data" / "corporate-brain-evals-v1.json"

ALLOWED = {"GREEN", "YELLOW", "ORANGE", "RED"}
REQUIRED = {f"CB-{i:02d}" for i in range(1, 15)}

def main():
    status = json.loads(STATUS.read_text(encoding="utf-8"))
    gates = status.get("gates", [])
    ids = {g.get("id") for g in gates}
    assert ids == REQUIRED, f"gate IDs mismatch: {sorted(ids ^ REQUIRED)}"
    assert all(g.get("status") in ALLOWED for g in gates)
    assert all(g.get("name") and g.get("note") for g in gates)
    assert status.get("privacy_boundary")
    assert status.get("authority_boundary")

    evals = json.loads(EVALS.read_text(encoding="utf-8"))
    categories = evals.get("categories", [])
    assert len(categories) >= 5
    assert all(c.get("id") and c.get("questions") for c in categories)
    questions = [q for c in categories for q in c["questions"]]
    assert len(questions) >= 10
    assert evals.get("release_rule")

    print("CORPORATE_BRAIN_A_PLUS_CONTROL_VALID")

if __name__ == "__main__":
    main()
