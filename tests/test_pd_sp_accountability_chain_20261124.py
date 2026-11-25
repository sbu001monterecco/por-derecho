#!/usr/bin/env python3
"""Draft-only bilingual accountability validation. Does not publish or contact external systems."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
m=json.loads((ROOT/"ops/continuity/PD_SP_ACCOUNTABILITY_CHAIN_20261124_DRAFT.json").read_text(encoding="utf-8"))
c="PD-SP-ACCOUNTABILITY-CHAIN-20261124-DRAFT-01"
assert m["control"]==c and m["stage"]=="DRAFT_SOURCE_ONLY"
assert not any(m[k] for k in ("publishable","merge_authorized","deploy_authorized","external_contact_authorized","registry_request_authorized","filing_authorized"))
assert len(m["events"])==9 and len(m["existing_pages"])==10 and len(m["new_pages"])==2
assert len({e["id"] for e in m["events"]})==9
for p in m["existing_pages"]:
 text=(ROOT/p["path"]).read_text(encoding="utf-8")
 assert text.count("<!-- "+c+" START -->")==1 and text.count("<!-- "+c+" END -->")==1
 assert text.count("</main>")==1 and 'data-topic="'+p["topic"]+'"' in text
for route,lang in zip(m["new_pages"],("en","es")):
 text=(ROOT/route).read_text(encoding="utf-8")
 assert f'<html lang="{lang}">' in text and '<svg' in text
 assert 'data-publication="DRAFT_ONLY_NO_DEPLOY"' in text
 assert text.count('class="pdsp-event"')==9 and 'data-filter="official"' in text
 assert all(e["id"] in text for e in m["events"])
 assert "DP 1901" in text and "DP 1956" in text
 assert 'id="pdsp-criminal-attribution"' in text and 'data-legal-status="ALLEGED_NOT_ADJUDICATED"' in text
 assert "C36-E008" in text and "C36-E055" in text
 assert "252" in text and "253" in text and "446" in text
 assert "third-party bidder" in text if lang=="en" else "tercer oferente" in text
 assert ("third-party bidder" in text if lang=="en" else "tercer oferente" in text) and (('735,694.02' in text) or ('735.694,02' in text))
 assert (('erroneous' in text) or ('errónea' in text))
 assert 'id="pd-sp-ev-09"' in text and 'datetime="2026-07-21"' in text
 assert 'id="pd-sp-ev-08"' in text and 'datetime="2026-09-14"' in text
 assert not any(t in text.lower() for t in ("jsixto@", "mail.google.com", "sbu001@", "regage26e"))
print("PASS: 10 additive pages, 2 bilingual visual hubs, 9 events, distinct July/September dismissals, draft controls")
