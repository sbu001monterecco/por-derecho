#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "assets" / "data"
CONTROL = DATA / "sun-park-owner-perimeter-classification-v1.json"
REGISTRY = DATA / "matter-identity-registry-v1.json"
PROTOCOL = ROOT / "archive" / "SUN_PARK_OWNER_PERIMETER_CLASSIFICATION_PROTOCOL_26AUG2026.md"
CSS = ROOT / "assets" / "owner-perimeter-tokens.css"
HEX = re.compile(r"^#[0-9A-Fa-f]{6}$")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    try:
        control = load(CONTROL)
        require(control.get("schema") == "por-derecho.sun-park-owner-perimeter-classification.v1", "unexpected schema")
        require(control.get("control_id") == "PD-SP-OWNER-PERIMETERS-001", "unexpected control id")

        index = load(REGISTRY)
        ids = set()
        for desc in index.get("parts", []):
            part = load(DATA / desc["path"])
            records = part.get("records", [])
            require(len(records) == desc.get("count"), f"registry part count drift: {desc['path']}")
            ids.update(r["id"] for r in records)
        require(len(ids) == index.get("counts", {}).get("total"), "registry total mismatch")

        legend = control.get("visual_legend", {})
        required_tokens = {
            "PD_PERIMETER_OUR_OWNER_CONTROL",
            "PD_PERIMETER_OUR_ADVISERS",
            "PD_PERIMETER_MM_DISSIDENT_CORE",
            "PD_PERIMETER_MM_WIDER",
            "PD_PERIMETER_OTHER_MINORITY",
            "PD_PERIMETER_LPB_TRANSFEREE_12",
            "PD_PERIMETER_LATER_CAM",
            "PD_PERIMETER_NEUTRAL_OPEN",
        }
        require(required_tokens <= set(legend), "visual legend incomplete")
        for token, meta in legend.items():
            require(HEX.fullmatch(meta.get("color", "")) is not None, f"invalid colour for {token}")
            require(meta.get("label_es") and meta.get("label_en"), f"missing bilingual label for {token}")

        perimeters = control.get("perimeters", [])
        by_class = {p.get("classification"): p for p in perimeters}
        required_classes = {
            "OUR_OWNER_CONTROL",
            "OUR_ADVISERS_AND_REPRESENTATIVES",
            "MONTELANZA_MOLINA_JUDICIAL_LITIGATION_CORE",
            "MONTELANZA_MOLINA_WIDER_DISSIDENT_REPRESENTED_PERIMETER",
            "MONTELANZA_MOLINA_REPRESENTATIVES_AND_COMMUNITY_OFFICEHOLDERS",
            "LPB_POST_ACQUISITION_TRANSFEREE_OWNER_COHORT",
            "OTHER_NON_LPB_MATKATOR_MINORITY_OWNERS",
            "LATER_CAM_ACOSTA_MATOS_PERIMETER",
        }
        require(required_classes <= set(by_class), "required perimeter classes missing")

        for p in perimeters:
            token = p.get("visual_token")
            require(token in legend, f"unknown visual token for {p.get('perimeter_id')}")
            for field in ("members", "owner_or_interest_ids", "representative_ids"):
                for rid in p.get(field, []):
                    require(rid in ids, f"unknown registry ID {rid} in {p.get('perimeter_id')}.{field}")
            for role in p.get("roles", []):
                rid = role.get("identity_id")
                require(rid in ids, f"unknown representative ID {rid}")
                require(role.get("role_code"), f"missing role code for {rid}")

        our = set(by_class["OUR_OWNER_CONTROL"].get("members", []))
        require({"PD-SP-O-0001", "PD-SP-O-0002", "PD-SP-O-0003"} <= our, "our owner/control perimeter incomplete")

        ap89 = by_class["MONTELANZA_MOLINA_JUDICIAL_LITIGATION_CORE"]
        require(len(ap89.get("members", [])) == 7, "AP89 claimant-owner core must contain exactly seven members")
        require(ap89.get("representative_ids") == ["PD-SP-P-0003"], "AP89 counsel edge drift")

        twelve = by_class["LPB_POST_ACQUISITION_TRANSFEREE_OWNER_COHORT"]
        require(twelve.get("reported_unit_count") == 12, "reported LPB-transferee denominator drift")
        require(twelve.get("owner_ids") == [], "twelve-unit cohort must not invent unidentified owners")
        require("REQUIRES_FINA_BY_FINA" in twelve.get("status", ""), "twelve-unit status must stay reconstruction-open")
        require("Do not encode an endpoint from recollection alone" in " ".join(twelve.get("open_questions", [])), "later-chain verification boundary missing")

        other = by_class["OTHER_NON_LPB_MATKATOR_MINORITY_OWNERS"]
        require("not yet supported" in other.get("rule", ""), "other-minority non-collapse rule missing")

        rules = " ".join(control.get("governing_rules", []))
        require("NON_LPB_MATKATOR_OWNER does not mean MONTELANZA_MOLINA_DISSIDENT" in rules, "central non-collapse rule missing")
        require("adverse/dissident" in rules, "attributed adverse-label boundary missing")

        overlap = control.get("overlap_model", {})
        require(overlap.get("type") == "MANY_TO_MANY_TEMPORAL", "overlap model must be temporal many-to-many")
        require("Colour follows the displayed edge/perimeter" in " ".join(overlap.get("rules", [])), "edge-colour rule missing")

        role_codes = control.get("role_codes", {})
        require("ALLEGED_ENABLEMENT" in role_codes, "alleged-enablement role missing")
        require("never inferred" in role_codes["ALLEGED_ENABLEMENT"], "enablement evidential boundary missing")

        require(PROTOCOL.is_file(), "classification protocol missing")
        protocol = PROTOCOL.read_text(encoding="utf-8")
        for marker in [
            "NON-LPB/MATKATOR OWNER ≠ MONTELANZA/MOLINA DISSIDENT",
            "reported twelve LPB transferee units",
            "Colour follows the **edge/perimeter being shown**",
        ]:
            require(marker in protocol, f"protocol marker missing: {marker}")

        require(CSS.is_file(), "owner perimeter CSS tokens missing")
        css = CSS.read_text(encoding="utf-8")
        for marker in [
            "--pd-perimeter-our-owner",
            "--pd-perimeter-mm-core",
            "--pd-perimeter-lpb-transferee-12",
            "--pd-perimeter-other-minority",
        ]:
            require(marker in css, f"CSS token missing: {marker}")

        print("OWNER PERIMETER CLASSIFICATION: PASS")
        print(" - ownership provenance kept separate from adverse/representational alignment")
        print(" - AP89 core: 7 claimant-owners + separate counsel edge")
        print(" - LPB transferee cohort: reported 12 units, owners intentionally unresolved")
        print(" - other minority owners remain non-adverse by default")
        print(" - temporal overlap and semantic colour tokens enforced")
        return 0
    except AssertionError as exc:
        print(f"OWNER PERIMETER CLASSIFICATION: FAIL\n - {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
