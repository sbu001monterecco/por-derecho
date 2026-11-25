#!/usr/bin/env python3
"""Source-preserving independent review of the PD-SP accountability candidate.

Never merges, deploys, manipulates CI identities or handles privileged records.
Historic Lanzarote validators remain unchanged and must be separately admitted.
"""
from __future__ import annotations
import argparse
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import posixpath
import re
import subprocess
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
CONTROL = "PD-SP-ACCOUNTABILITY-CHAIN-20261124-DRAFT-01"
MANIFEST = "ops/continuity/PD_SP_ACCOUNTABILITY_CHAIN_20261124_DRAFT.json"
TEST = "tests/test_pd_sp_accountability_chain_20261124.py"
SCRIPT = "ci/pd_sp_accountability_review_20261125.py"
GH_BASE = "7aed9eea4085b53c4c62aa5a57a3520b1ec29cda"
GL_BASE = "f1ef99bd821b97d94eff2d6db512a44e69c7a236"
BRANCH = "draft/pd-sp-accountability-chain-20261124"
PUBLIC_ORIGINS = {
    "github": "https://sbu001monterecco.github.io/por-derecho",
    "gitlab": "https://por-derecho.gitlab.io/por-derecho-setup-or-gitlab-setup",
}
ALLOWED_PREDECESSOR_SOURCE = [
    "ci/pd_lanzarote_source_only_20261123.py",
    "ops/continuity/R865_SOURCE_ONLY_GITLAB_20261123.json",
    "ops/continuity/LANZAROTE_SOURCE_ONLY_GITLAB_20261123.json",
    "PUBLIC_RELEASE_SPEC.json",
    "publication-manifests/PD_AM_RICPE_INTERLINK_20261123_RELEASE.json",
]
PRIVATE = re.compile(
    r"(?i)(?:\bREGAGE\d{2}e\d+\b|"
    r"(?:[a-z0-9._%+-]+@(?:[a-z0-9.-]+\.[a-z]{2,}))|"
    r"(?:mail\.google\.com|(?:docs|drive)\.google\.com)|"
    r"-----BEGIN (?:RSA |OPENSSH )?PRIVATE KEY-----)"
)

def require(test, reason):
    if not test:
        raise AssertionError("PD_SP_ACCOUNTABILITY_REVIEW: " + reason)

def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, timeout=120)

def baseline(base, path):
    return git("show", base + ":" + path)

class Links(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = []
        self.links = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.append(a["id"])
        if tag in ("a", "link", "script") and ("href" in a or "src" in a):
            self.links.append(a.get("href", a.get("src")))

def check_hub(path, locale, manifest, origin):
    raw = (ROOT / path).read_text(encoding="utf-8")
    require(raw.startswith("<!doctype html>") and '<html lang="' + locale + '">' in raw, path + ": locale")
    require('data-publication="DRAFT_ONLY_NO_DEPLOY"' in raw and CONTROL in raw, path + ": draft gate")
    require('<svg' in raw and 'role="img"' in raw, path + ": visual")
    for v in ("all", "official", "party", "documented"):
        require('data-filter="' + v + '"' in raw, path + ": filter " + v)
    require(raw.count('class="pdsp-event"') == 9, path + ": exact event count")
    require('id="pd-sp-ev-09"' in raw and 'datetime="2026-07-21"' in raw, path + ": 1956 notice")
    require('id="pd-sp-ev-08"' in raw and 'datetime="2026-09-14"' in raw, path + ": 1901 order")
    require(all(e["id"].lower() in raw for e in manifest["events"]), path + ": event crosswalk")
    require(not PRIVATE.search(raw), path + ": private identifier")
    require('href="' + origin + "/" + path.replace("index.html", "") + '"' in raw, path + ": canonical")
    parsed = Links()
    parsed.feed(raw)
    require(len(parsed.ids) == len(set(parsed.ids)), path + ": duplicate IDs")
    for v in parsed.links:
        if v.startswith("mailto:") or v.startswith("javascript:"):
            require(False, path + ": unsafe link scheme")
        if v.startswith("https://"):
            require(v.startswith(origin + "/") or v.startswith("https://www.boe.es/"),
                    path + ": unapproved external source " + v[:90])
        elif not v.startswith("#"):
            base_dir = posixpath.dirname(path)
            resolved = posixpath.normpath(posixpath.join(base_dir, urlsplit(v).path))
            if v.endswith("/"):
                resolved += "/index.html"
            require(not resolved.startswith("../") and (ROOT / resolved).is_file(),
                    path + ": missing local target " + resolved)

def original_insertion_preservation(path, host, base):
    candidate = (ROOT / path).read_bytes()
    old = baseline(base, path)
    start = ("<!-- " + CONTROL + " START -->").encode()
    end = ("<!-- " + CONTROL + " END -->").encode()
    require(candidate.count(start) == 1 and candidate.count(end) == 1, path + ": exact insertion marker")
    a = candidate.index(start)
    b = candidate.index(end) + len(end)
    if host == "github":
        restored = candidate[:a].removesuffix(b"\n") + candidate[b:].removeprefix(b"\n\n")
    else:
        restored = candidate[:a] + candidate[b:].removeprefix(b"\n")
    require(restored == old, path + ": historical bytes modified")

def check(host):
    base = GH_BASE if host == "github" else GL_BASE
    require(git("rev-parse", "HEAD").decode().strip() == os.getenv("GITHUB_SHA", "").strip()
            if host == "github" and os.getenv("GITHUB_SHA") and os.getenv("GITHUB_EVENT_NAME") != "pull_request"
            else True, "unexpected checkout")
    current = git("rev-parse", "HEAD").decode().strip()
    require(subprocess.run(["git", "merge-base", "--is-ancestor", base, current], cwd=ROOT).returncode == 0,
            "source predecessor is not an ancestor")
    if host == "gitlab":
        require(os.getenv("CI_PROJECT_ID") == "86151898", "project ID")
        require(os.getenv("CI_PIPELINE_SOURCE") == "merge_request_event", "MR pipeline source")
        require(os.getenv("CI_MERGE_REQUEST_SOURCE_BRANCH_NAME") == BRANCH
                and os.getenv("CI_MERGE_REQUEST_TARGET_BRANCH_NAME") == "main", "branch identity")
        require(os.getenv("CI_COMMIT_SHA") == current, "current CI head")
    else:
        require(os.getenv("GITHUB_EVENT_NAME") == "pull_request", "PR event")
    manifest = json.loads((ROOT / MANIFEST).read_text(encoding="utf-8"))
    require(manifest["control"] == CONTROL and manifest["stage"] == "DRAFT_SOURCE_ONLY"
            and manifest["publishable"] is False and manifest["merge_authorized"] is False
            and manifest["deploy_authorized"] is False, "no-publication state")
    require(manifest["base_commit"] == base, "manifest predecessor")
    events = manifest["events"]
    require(len(events) == 9 and len({e["id"] for e in events}) == 9, "nine unique events")
    ev = {e["id"]: e for e in events}
    require(ev["PD-SP-EV-08"]["date"] == "2026-09-14" and ev["PD-SP-EV-09"]["date"] == "2026-07-21",
            "two independent dates")
    require(any(c.get("correction_id") == "PD-SP-CORR-01" for c in manifest.get("corrections", [])),
            "no documented correction provenance")
    require(len(manifest["existing_pages"]) == 10 and len(manifest["new_pages"]) == 2,
            "inventory consistency")
    changed = {}
    fields = git("diff", "--no-renames", "--name-status", "-z", base, current).split(b"\0")
    for action, path in zip(fields[::2], fields[1::2]):
        if not action and not path:
            continue
        path = path.decode()
        require(action in (b"A", b"M") and path not in changed, "unexpected deletion/rename/duplicate: " + path)
        changed[path] = action.decode()
    existing = {x["path"] for x in manifest["existing_pages"]}
    gh_existing = existing
    if host == "gitlab":
        existing = {x["path"] for x in manifest["existing_pages"] if x["topic"] != "obrem"}
    expected = {**{p:"M" for p in existing},
                **{p:"A" for p in manifest["new_pages"]},
                MANIFEST:"A", TEST:"A", SCRIPT:"A"}
    if host == "gitlab":
        expected.update({p:"A" for p in (gh_existing - existing)})
        expected[".gitlab-ci.yml"] = "M"
    else:
        expected[".github/workflows/pd-sp-accountability-review-20261125.yml"] = "A"
    require(changed == expected, "candidate path inventory differs: " + str({k:v for k,v in changed.items() if expected.get(k) != v}))
    for path in existing:
        original_insertion_preservation(path, host, base)
    for path in manifest["new_pages"]:
        check_hub(path, "en" if path.startswith("en/") else "es", manifest, PUBLIC_ORIGINS[host])
    for old in ALLOWED_PREDECESSOR_SOURCE:
        if (ROOT / old).exists():
            require((ROOT / old).read_bytes() == baseline(base, old), "protected predecessor modified: " + old)
    if host == "gitlab":
        previous = baseline(base, ".gitlab-ci.yml")
        current_ci = (ROOT / ".gitlab-ci.yml").read_bytes()
        require(current_ci.startswith(previous), "existing CI jobs or publisher guards changed")
        require(current_ci[len(previous):].count(b"verify-sp-accountability-draft-20261125:") == 1,
                "exact additive verification job missing")
    print(json.dumps({"status":"PASS_DRAFT_ONLY", "head":current,"base":base,
                      "host":host,"changed_paths":len(changed),"events":9,
                      "old_source_preserved":len(existing),"new_visuals":2,
                      "historic_lanzarote_verifier_unchanged":True,
                      "publication_authorized":False},sort_keys=True))

def render():
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as e:
        raise RuntimeError("Playwright browser dependency missing") from e
    report = ROOT / "recovery-audit"
    report.mkdir(exist_ok=True)
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        for locale, path in (("en", "en/accountability-chain-2018-2022/index.html"),
                             ("es", "es/cadena-responsabilidad-2018-2022/index.html")):
            for mode, width, height in (("desktop", 1440, 900),("mobile", 390, 844)):
                page = browser.new_page(viewport={"width":width,"height":height}, device_scale_factor=1)
                errors=[]
                page.on("pageerror", lambda e: errors.append(str(e)))
                page.goto((ROOT/path).resolve().as_uri(), wait_until="domcontentloaded", timeout=30000)
                require(page.locator(".pdsp-event").count() == 9, path + ": browser evidence rows")
                page.locator('button[data-filter="official"]').click()
                require(page.locator(".pdsp-event:visible").count() == 5, path + ": official filter")
                page.locator('button[data-filter="all"]').click()
                require(page.locator(".pdsp-event:visible").count() == 9, path + ": restored filter")
                require(page.evaluate("document.documentElement.scrollWidth <= innerWidth + 2"),
                        path + ": viewport overflow")
                require(not errors, path + ": JS errors " + repr(errors))
                page.screenshot(path=str(report / ("pdsp-%s-%s.png" % (locale,mode))),
                                full_page=True)
                page.close()
        browser.close()
    print("PASS_RENDERED_EN_ES_DESKTOP_MOBILE")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", choices=["github","gitlab"], required=True)
    parser.add_argument("--render", action="store_true")
    args = parser.parse_args()
    check(args.host)
    if args.render:
        render()
