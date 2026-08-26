#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ES = ROOT / "es/alberto-lopez-villarrubia-meeting-point-357-masa-activa/index.html"
EN = ROOT / "en/alberto-lopez-villarrubia-meeting-point-357-active-estate/index.html"

errors = []
for path in (ES, EN):
    if not path.exists():
        errors.append(f"missing {path.relative_to(ROOT)}")

if not errors:
    es = ES.read_text(encoding="utf-8")
    en = EN.read_text(encoding="utf-8")
    required = {
        "Spanish": (es, ["9/20", "NO TODO ES^", "atribuyen", "original firmado", "alegación", "SEPI", "Club Sei"]),
        "English": (en, ["9/20", "NOT ALL IS^", "attribute", "signed original", "allegation", "SEPI", "Club Sei"]),
    }
    for label, (text, needles) in required.items():
        for needle in needles:
            if needle not in text:
                errors.append(f"{label} page missing {needle!r}")
    forbidden = [
        "Alberto signed the 24 October",
        "Alberto firmó el 24 de octubre",
        "Meeting Point committed a crime",
        "Meeting Point cometió un delito",
        "concealed the conflict as established fact",
    ]
    for phrase in forbidden:
        if phrase in es or phrase in en:
            errors.append(f"forbidden overstatement: {phrase}")

old_error = "Aweswell won the 18 May"
for rel in ["archive/LPAM_MAGISTRADO_SOURCE_COMPLETION_16AUG2026.md", "assets/lpam-magistrado-source-control-20260816.js"]:
    if old_error in (ROOT / rel).read_text(encoding="utf-8"):
        errors.append(f"stale auction error in {rel}")

plan = (ROOT / "ops/ALBERTO_MEETING_POINT_357_AUTHORITY_SUBMISSION_PLAN_26AUG2026.md").read_text(encoding="utf-8")
if "HOLD" not in plan or "No email" not in plan:
    errors.append("authority plan must remain HOLD and prohibit email action")

for rel in ["sitemap.xml", "sitemap-meeting-point.xml", "sitemap-judicial-spine.xml"]:
    text = (ROOT / rel).read_text(encoding="utf-8")
    for slug in ["alberto-lopez-villarrubia-meeting-point-357-masa-activa", "alberto-lopez-villarrubia-meeting-point-357-active-estate"]:
        if slug not in text:
            errors.append(f"{rel} missing {slug}")

if errors:
    raise SystemExit("\n".join(errors))
print("Alberto / Meeting Point cross-proceeding validation passed")
