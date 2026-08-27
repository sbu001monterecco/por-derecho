#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def require(path, needles):
    text = (ROOT / path).read_text(encoding="utf-8")
    for needle in needles:
        assert needle in text, f"{path}: missing {needle!r}"

require("es/lava-verde-club-sei-meeting-point/index.html", ["id=\"fti-recuperacion\"", "casi 980 M EUR", "Auditoría ^", "Deutsch"])
require("en/lava-verde-club-sei-meeting-point/index.html", ["id=\"fti-recovery\"", "almost EUR 980m", "^ audit", "Deutsch"])
require("de/lava-verde-club-sei-meeting-point/index.html", ["fast 980 Mio. EUR", "Großhandel", "Criminal-first", "Keine E-Mail"])
require("archive/CORRECTION_REGISTER.md", ["| CR-115 |", "| CR-116 |", "| CR-117 |", "| CR-118 |"])
require("archive/MISSING_EVIDENCE_REGISTER.md", ["| ME-097 |", "| ME-098 |"])

recovery = json.loads((ROOT / "assets/data/fti-touristik-club-sei-creditor-recovery-v1.json").read_text())
assert recovery["authority"]["publication_authorized"] is True
assert recovery["authority"]["email_authorized"] is False
assert recovery["authority"]["filing_authorized"] is False

caret = json.loads((ROOT / "assets/data/caepr-caret-fti-touristik-club-sei-recovery-v1.json").read_text())
assert caret["counts"] == {"eligible": 44, "confirmed": 11, "pending": 33, "suspended": 0, "coverage_percent": 25.0}

actions = json.loads((ROOT / "ops/FTI_TOURISTIK_CLUB_SEI_RECOVERY_ACTION_ADDENDUM_27AUG2026.json").read_text())
assert actions["email_authorized"] is False and actions["filing_authorized"] is False
assert all("AUTHORI" in item["state"] or item["state"] == "REPOSITORY_MONITOR_ONLY_NO_EXTERNAL_ACTION" for item in actions["actions"])

print("FTI CLUB SEI RECOVERY CLOSEOUT: PASS")
print("- ES/EN/DE routes and machine evidence present")
print("- 44/11/33/0 caret denominator controlled")
print("- publication authority separated from email/filing authority")
