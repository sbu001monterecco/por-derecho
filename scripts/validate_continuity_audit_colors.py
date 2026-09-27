#!/usr/bin/env python3
import re
import sys
from pathlib import Path

STATUS = ("🟢 GREEN", "🟠 AMBER", "🔴 RED")
THREAD = ("🟢 THREAD", "🟠 THREAD", "🔴 THREAD")

def validate(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    lower = text.lower()
    if not any(k in lower for k in ("continuity", "preservation", "deletion-safety", "readiness audit")):
        return []
    errors = []
    first = text[:3500]
    if "Overall operational/readiness:" not in first:
        errors.append("missing overall operational/readiness marker near start")
    if not any(s in first for s in STATUS):
        errors.append("missing traffic-light cue near start")
    if "Component statuses" not in first:
        errors.append("missing component-status block near start")
    if not any(t in text[-1600:] for t in THREAD):
        errors.append("missing separate THREAD deletion-safety cue near end")
    return errors

def main() -> int:
    if len(sys.argv) < 2:
        print("usage: validate_continuity_audit_colors.py <audit.md> [...]", file=sys.stderr)
        return 2
    failed = False
    for raw in sys.argv[1:]:
        path = Path(raw)
        errs = validate(path)
        if errs:
            failed = True
            for e in errs:
                print(f"{path}: {e}", file=sys.stderr)
        else:
            print(f"{path}: continuity-audit colour presentation OK")
    return 1 if failed else 0

if __name__ == "__main__":
    raise SystemExit(main())
