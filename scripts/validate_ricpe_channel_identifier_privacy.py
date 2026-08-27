#!/usr/bin/env python3
"""Fail if the private RICPE communication code reappears in the current tree."""

from __future__ import annotations

import hashlib
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_FINGERPRINT = "e53bda34973e530520bde39648768a1e32a358d8984294b21258789faebe6a24"
UUID_RE = re.compile(r"(?<![0-9a-f])[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}(?![0-9a-f])", re.I)
REQUIRED = [
    ROOT / "evidence/ricpe-cnmv/2026-08-27/resolution.txt",
    ROOT / "CURRENT_HANDOVER_RICPE_HNT_GC836_TREASURY_21AUG2026.md",
    ROOT / "archive/THREAD_DELETION_AUDIT_CRITICAL_STATUS_UPDATE_21AUG2026.md",
]

errors: list[str] = []

for path in REQUIRED:
    text = path.read_text(encoding="utf-8")
    if PUBLIC_FINGERPRINT not in text:
        errors.append(f"approved public fingerprint absent from {path.relative_to(ROOT)}")

output = subprocess.check_output(
    ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
    cwd=ROOT,
    text=True,
)
for relative in output.splitlines():
    path = ROOT / relative
    try:
        if path.stat().st_size > 8_000_000:
            continue
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        continue
    for candidate in UUID_RE.findall(text):
        if hashlib.sha256(candidate.encode("utf-8")).hexdigest() == PUBLIC_FINGERPRINT:
            errors.append(f"private RICPE communication code exposed in {relative}")

resolution = REQUIRED[0].read_text(encoding="utf-8")
if "Correlación pública (SHA-256 del código privado)" not in resolution:
    errors.append("public resolution lacks the privacy-safe correlation label")
if "Código de comunicación:" in resolution:
    errors.append("public resolution contains the prohibited exact-code label")

if errors:
    print("RICPE CHANNEL IDENTIFIER PRIVACY: FAIL", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print("RICPE CHANNEL IDENTIFIER PRIVACY: PASS")
print("- approved one-way fingerprint present in all three controlled files")
print("- no current-tree UUID resolves to the private communication-code fingerprint")
