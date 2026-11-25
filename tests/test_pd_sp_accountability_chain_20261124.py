#!/usr/bin/env python3
"""Bilingual accountability/source-state validation; never issues release permits."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
m=json.loads((ROOT/"ops/continuity/PD_SP_ACCOUNTABILITY_CHAIN_20261124_DRAFT.json").read_text(encoding="utf-8"))
c="PD-SP-ACCOUNTABILITY-CHAIN-20261124-DRAFT-01"
release_path=ROOT/"publication-manifests/PD_SP_ACCOUNTABILITY_GITHUB_20261125_RELEASE.json"
release=json.loads(release_path.read_text(encoding="utf-8")) if release_path.exists() else None
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
 assert ('data-publication="PUBLIC_RELEASE"' if release else 'data-publication="DRAFT_ONLY_NO_DEPLOY"') in text
 if release:
  assert 'data-release="'+release['publication_id']+'"' in text
  assert 'DRAFT ONLY:' not in text and 'BORRADOR:' not in text
  assert 'AC-CLM-005' in text and 'class="pdsp-law-version"' in text
 assert text.count('class="pdsp-event"')==9 and 'data-filter="official"' in text
 assert all(e["id"] in text for e in m["events"])
 assert "DP 1901" in text and "DP 1956" in text
 assert "GC-CRI-008" in text and "GC-CRI-009" in text
 assert 'id="pdsp-criminal-attribution"' in text and 'data-legal-status="ALLEGED_NOT_ADJUDICATED"' in text
 assert "C36-E008" in text and "C36-E055" in text
 assert "252" in text and "253" in text and "446" in text
 assert "third-party bidder" in text if lang=="en" else "tercer oferente" in text
 assert ("third-party bidder" in text if lang=="en" else "tercer oferente" in text) and (('735,694.02' in text) or ('735.694,02' in text))
 assert (('erroneous' in text) or ('errónea' in text))
 assert 'id="pd-sp-ev-09"' in text and 'datetime="2026-07-21"' in text
 assert 'id="pd-sp-ev-08"' in text and 'datetime="2026-09-14"' in text
 assert not any(t in text.lower() for t in ("jsixto@", "mail.google.com", "sbu001@", "regage26e"))
if release:
 # A GitHub successor must never admit a GitLab deployment or rewrite the
 # historical source-only manifest. Check these rejection paths explicitly.
 import importlib.util
 from tempfile import TemporaryDirectory
 from unittest.mock import patch
 spec=importlib.util.spec_from_file_location('pdsp_review',ROOT/'ci/pd_sp_accountability_review_20261125.py')
 review=importlib.util.module_from_spec(spec); spec.loader.exec_module(review)
 try:
  review.release_profile('gitlab',m)
 except AssertionError as error:
  assert 'cannot admit GitLab' in str(error)
 else:
  raise AssertionError('GitHub release incorrectly admitted GitLab')
 with TemporaryDirectory() as temp:
  root=Path(temp)
  (root/review.RELEASE_MANIFEST).parent.mkdir(parents=True)
  (root/review.RELEASE_MANIFEST).write_text(json.dumps(release))
  (root/review.MANIFEST).parent.mkdir(parents=True)
  (root/review.MANIFEST).write_bytes((ROOT/review.MANIFEST).read_bytes()+b' ')
  with patch.object(review,'ROOT',root), patch.object(review.subprocess,'run') as run, patch.object(review,'baseline',return_value=(ROOT/review.MANIFEST).read_bytes()):
   run.return_value.returncode=0
   try:
    review.release_profile('github',m)
   except AssertionError as error:
    assert 'historical draft/source review was rewritten' in str(error)
   else:
    raise AssertionError('rewritten historical source control accepted')
print("PASS: 10 preserved pages, 2 bilingual hubs, 9 events, separate dismissals, historic draft controls and host-specific release boundary")
