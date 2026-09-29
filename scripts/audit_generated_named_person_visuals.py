#!/usr/bin/env python3
"""Audit composite sidecars for named-person rendering safety."""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
COMP=ROOT/"assets/composites"

def has_person_ref(value):
    if isinstance(value,str):
        return value.startswith("person.")
    if isinstance(value,dict):
        if any(has_person_ref(v) for v in value.values()): return True
        return bool(value.get("identity") and (value.get("source_asset") or value.get("identity_status")))
    if isinstance(value,list):
        return any(has_person_ref(v) for v in value)
    return False

def main():
    errors=[]; reviewed=0; quarantined=0; exact=0
    for path in sorted(COMP.glob("*.asset-map.json")):
        try: obj=json.loads(path.read_text(encoding="utf-8"))
        except Exception: continue
        named = has_person_ref(obj.get("slots")) or has_person_ref(obj.get("rendered_asset_ids"))
        if not named: continue
        reviewed += 1
        mode=str(obj.get("representation_mode",""))
        storage=str(obj.get("composite_storage_mode",""))
        render=str(obj.get("public_landing_visual",{}).get("render_mode",""))
        treatment=str(obj.get("portrait_treatment","")).lower()
        status=str(obj.get("publication_status",obj.get("status","")))
        creator=str(obj.get("creator_source","")).lower()

        stylised = "STYLIZATION" in mode
        exact_source = (
            "native-html-css" in storage.lower()
            or "html/css" in render.lower()
            or "source-portraits" in storage.lower()
            or ("not retouched" in treatment and "regenerated" in treatment)
        )
        if stylised:
            if "NOT_DOCUMENTARY_PORTRAIT_EVIDENCE" not in mode:
                errors.append(f"{path.relative_to(ROOT)}: named-person stylisation lacks explicit non-documentary boundary")
            else:
                quarantined += 1
            continue
        if exact_source:
            exact += 1
            continue
        if "openai" in creator or "image generation" in creator:
            errors.append(f"{path.relative_to(ROOT)}: generated named-person composite lacks deterministic public rendering")
            continue
        if status in {"READY","OWNER_AUTHORISED_LOCKED_EDITORIAL_VISUALS","OWNER_AUTHORIZED_EDITORIAL_RELEASE"}:
            errors.append(f"{path.relative_to(ROOT)}: active named-person composite lacks deterministic/source-pixel rendering declaration")

    if errors:
        print("GENERATED NAMED-PERSON COMPOSITE AUDIT: FAIL")
        for e in errors: print("- "+e)
        raise SystemExit(1)
    print(f"GENERATED NAMED-PERSON COMPOSITE AUDIT: PASS ({reviewed} named-person sidecars; {exact} exact-source; {quarantined} quarantined stylisations)")

if __name__=="__main__":
    main()
