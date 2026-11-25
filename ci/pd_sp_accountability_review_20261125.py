#!/usr/bin/env python3
"""Source-preserving independent review of the PD-SP accountability candidate.

Never merges, deploys, manipulates CI identities or handles privileged records.
Historic Lanzarote validators remain unchanged and must be separately admitted.
"""
from __future__ import annotations
import argparse
import hashlib
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
RELEASE_MANIFEST = "publication-manifests/PD_SP_ACCOUNTABILITY_GITHUB_20261125_RELEASE.json"
RELEASE_CONTROL = "PD-SP-ACCOUNTABILITY-CHAIN-20261125-GITHUB-01"
DRAFT_PREDECESSOR = "cf2a7b366824d55eebd78460fc548beae4a7a993"
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

# Same protected-bidder token digest used by the existing public name-only gate.
# Retains every bid amount and procedural fact while preventing public identification.
PROTECTED_BIDDER_TOKEN_DIGESTS = {
    "33c594e4e36529842cb1344043ec59e9f4d026466fd7ba0112a635fbe30baf3e"
}
def has_protected_bidder(text):
    tokens = re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ0-9_-]+", text, re.UNICODE)
    return any(hashlib.sha256(token.casefold().encode("utf-8")).hexdigest()
               in PROTECTED_BIDDER_TOKEN_DIGESTS for token in tokens)

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

def release_profile(host, manifest):
    """A GitHub-only successor; the historical source-only record stays immutable.

    This source check never issues a publication permit. The unchanged controller
    and protected checks must independently accept the exact head before merge.
    GitLab retains its original draft-only path and predecessor admission.
    """
    release_path = ROOT / RELEASE_MANIFEST
    if not release_path.exists():
        return None
    require(host == "github", "GitHub successor cannot admit GitLab publication")
    release = json.loads(release_path.read_text(encoding="utf-8"))
    require(release.get("publication_id") == RELEASE_CONTROL
            and release.get("host") == "github" and release.get("pr") == 2159,
            "release identity/host/PR")
    require(release.get("draft_predecessor") == DRAFT_PREDECESSOR
            and release.get("source_baseline") == GH_BASE, "release lineage")
    require(subprocess.run(["git", "merge-base", "--is-ancestor", DRAFT_PREDECESSOR,
                            "HEAD"], cwd=ROOT).returncode == 0, "draft lineage lost")
    original = baseline(DRAFT_PREDECESSOR, MANIFEST)
    require((ROOT / MANIFEST).read_bytes() == original
            and hashlib.sha256(original).hexdigest() == release.get("historical_draft_manifest_sha256"),
            "historical draft/source review was rewritten")
    auth = release.get("authorization", {})
    require(auth.get("received") is True and auth.get("date") == "2026-11-25"
            and auth.get("owner_instruction") == "Authorize GitHub-first live publication"
            and auth.get("existing_required_gates_preserved") is True,
            "owner GitHub-first scope missing")
    for key in ("external_contact", "filing", "registry_request",
                "independent_professional_opinion_claimed", "signed_final_copy_attestation_claimed"):
        require(auth.get(key) is False, "unauthorized action or invented attestation: " + key)
    gl = release.get("gitlab", {})
    require(gl.get("state") == "HOLD_SOURCE_ONLY_UNMERGED"
            and gl.get("mutations") is False and gl.get("parity_claim") is False
            and gl.get("protected_controls_unchanged") is True, "GitLab hold changed")
    routes = {x["path"] for x in manifest["existing_pages"]} | set(manifest["new_pages"])
    expected = release.get("expected_routes", {})
    require(set(expected) == {"en", "es"}
            and all(len(expected[k]) == 6 for k in expected)
            and set(expected["en"] + expected["es"]) == routes,
            "release route denominator changed")
    files = release.get("source_files", [])
    require(len(files) == len(routes) and {x["path"] for x in files} == routes,
            "release fingerprint denominator changed")
    for item in files:
        raw = (ROOT / item["path"]).read_bytes()
        require(len(raw) == item["bytes"] and hashlib.sha256(raw).hexdigest() == item["sha256"],
                "release bytes differ: " + item["path"])
    for path in (".gitlab-ci.yml", ".github/workflows/publication-controller.yml",
                 ".github/workflows/release-acceptance.yml",
                 ".github/workflows/publication-integrity-gate.yml",
                 "scripts/pd_release_controller.py", "scripts/check_release_acceptance.py"):
        existed = subprocess.run(["git", "cat-file", "-e", GH_BASE + ":" + path],
                                 cwd=ROOT, stdout=subprocess.DEVNULL,
                                 stderr=subprocess.DEVNULL).returncode == 0
        if existed:
            require((ROOT / path).read_bytes() == baseline(GH_BASE, path),
                    "existing publication control changed: " + path)
        else:
            require(not (ROOT / path).exists(), "new cross-host control introduced: " + path)
    return release

def check_hub(path, locale, manifest, origin, release=None):
    raw = (ROOT / path).read_text(encoding="utf-8")
    require(raw.startswith("<!doctype html>") and '<html lang="' + locale + '">' in raw, path + ": locale")
    marker = "PUBLIC_RELEASE" if release else "DRAFT_ONLY_NO_DEPLOY"
    require('data-publication="' + marker + '"' in raw and CONTROL in raw, path + ": publication state")
    if release:
        require('data-release="' + RELEASE_CONTROL + '"' in raw
                and 'DRAFT ONLY:' not in raw and 'BORRADOR:' not in raw,
                path + ": released reader still claims draft-only")
        require('class="pdsp-law-version"' in raw and 'AC-CLM-005' in raw
                and ('corrections-version-control/' in raw or 'correcciones-control-versiones/' in raw),
                path + ": legal-version, canonical-claim or correction link absent")
    require('<svg' in raw and 'role="img"' in raw, path + ": visual")
    for v in ("all", "official", "party", "documented"):
        require('data-filter="' + v + '"' in raw, path + ": filter " + v)
    require(raw.count('class="pdsp-event"') == 9, path + ": exact event count")
    require('id="pdsp-criminal-attribution"' in raw and 'data-legal-status="ALLEGED_NOT_ADJUDICATED"' in raw, path + ": attributed legal status")
    require(raw.count('class="pdsp-crime"') == 3, path + ": exactly three actor-specific offence tests")
    require(all(('C36-E%03d' % n) in raw for n in (8,14,19,22,29,44,55)), path + ": canonical evidence crosswalk")
    require(all(('art. %s' % n) in raw or ('%s CP' % n) in raw for n in (252,253,446)), path + ": offence elements")

    require('id="pd-sp-ev-09"' in raw and 'datetime="2026-07-21"' in raw, path + ": 1956 notice")
    require('id="pd-sp-ev-08"' in raw and 'datetime="2026-09-14"' in raw, path + ": 1901 order")
    require(all(e["id"].lower() in raw for e in manifest["events"]), path + ": event crosswalk")
    require(not PRIVATE.search(raw), path + ": private identifier")
    require(not has_protected_bidder(raw), path + ": protected bidder name")
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
            target = urlsplit(v)
            resolved = posixpath.normpath(posixpath.join(base_dir, target.path))
            if target.path.endswith("/"):
                resolved += "/index.html"
            require(not resolved.startswith("../") and (ROOT / resolved).is_file(),
                    path + ": missing local target " + resolved)
            if target.fragment:
                target_ids = Links()
                target_ids.feed((ROOT / resolved).read_text(encoding="utf-8"))
                require(target.fragment in target_ids.ids, path + ": missing target fragment " + v)
        else:
            require(v[1:] in parsed.ids, path + ": missing local fragment " + v)

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
    require(candidate[a:b].count(b'data-evidence-state="ATTRIBUTED_SUSPICION"') == 1,
            path + ": clearly attributed criminal allegation required in every updated reader")

    require(not has_protected_bidder(candidate[a:b].decode("utf-8")), path + ": new section reveals protected bidder")

def check(host, local=False):
    if local:
        require(host == "github" and not os.getenv("GITHUB_ACTIONS")
                and not os.getenv("CI_PIPELINE_SOURCE"), "local mode cannot represent native CI")
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
    elif not local:
        require(os.getenv("GITHUB_EVENT_NAME") == "pull_request", "PR event")
        event_path = os.getenv("GITHUB_EVENT_PATH")
        require(bool(event_path), "native PR event payload missing")
        event = json.loads(Path(event_path).read_text(encoding="utf-8"))
        pr = event.get("pull_request", {})
        require(pr.get("head", {}).get("sha") == current
                and pr.get("head", {}).get("ref") == BRANCH
                and pr.get("base", {}).get("ref") == "main"
                and event.get("number") == 2159, "native PR head/branch/number mismatch")
    manifest = json.loads((ROOT / MANIFEST).read_text(encoding="utf-8"))
    release = release_profile(host, manifest)
    require(manifest["control"] == CONTROL and manifest["stage"] == "DRAFT_SOURCE_ONLY"
            and manifest["publishable"] is False and manifest["merge_authorized"] is False
            and manifest["deploy_authorized"] is False, "no-publication state")
    require(manifest["base_commit"] == base, "manifest predecessor")
    auth = manifest.get("owner_conditional_release_authorization_20261125", {})
    require(auth.get("control") == "PD-SP-CRIMINAL-ATTRIBUTION-RELEASE-20261125-01"
            and auth.get("received") is True and auth.get("specific_final_page_attestation") is False,
            "conditional owner authorization or final-copy boundary changed")
    matrix = manifest.get("criminal_attribution_matrix_20261125", {})
    require(len(matrix.get("entries", [])) == 4
            and matrix.get("review_state") == "ACTOR_SPECIFIC_SUSPECTED_OFFENCES_UNADJUDICATED",
            "criminal attribution matrix incomplete")
    successor = manifest.get("release_successor_admission_20261125", {})
    require(successor.get("status") == "REQUIRED_GATES_UNFULFILLED_NO_DEPLOY"
            and successor.get("r865_source_only_preserved") is True
            and successor.get("prior_gitlab_jobs_not_relabelled_as_passed") is True,
            "successor admission must fail closed")

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
        if release:
            expected[RELEASE_MANIFEST] = "A"
    require(changed == expected, "candidate path inventory differs: " + str({k:v for k,v in changed.items() if expected.get(k) != v}))
    for path in existing:
        original_insertion_preservation(path, host, base)
    for path in manifest["new_pages"]:
        check_hub(path, "en" if path.startswith("en/") else "es", manifest, PUBLIC_ORIGINS[host], release)
    for old in ALLOWED_PREDECESSOR_SOURCE:
        if (ROOT / old).exists():
            require((ROOT / old).read_bytes() == baseline(base, old), "protected predecessor modified: " + old)
    if host == "gitlab":
        previous = baseline(base, ".gitlab-ci.yml")
        current_ci = (ROOT / ".gitlab-ci.yml").read_bytes()
        require(current_ci.startswith(previous), "existing CI jobs or publisher guards changed")
        require(current_ci[len(previous):].count(b"verify-sp-accountability-draft-20261125:") == 1,
                "exact additive verification job missing")
    print(json.dumps({"status":"PASS_GITHUB_RELEASE_SOURCE" if release else "PASS_DRAFT_ONLY", "head":current,"base":base,
                      "host":host,"changed_paths":len(changed),"events":9,
                      "old_source_preserved":len(existing),"new_visuals":2,
                      "historic_lanzarote_verifier_unchanged":True,
                      "execution_context": "LOCAL_SOURCE_REVIEW" if local else "NATIVE_CI",
                      "owner_github_release_authorized": bool(release),
                      "controller_permit_issued_by_this_test":False},sort_keys=True))

def render(browser_executable=None):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as e:
        raise RuntimeError("Playwright browser dependency missing") from e
    report = ROOT / "recovery-audit"
    report.mkdir(exist_ok=True)
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True, executable_path=browser_executable)
        print("Browser version:", browser.version)
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
                if (ROOT / RELEASE_MANIFEST).exists():
                    require(page.locator('body[data-publication="PUBLIC_RELEASE"]').count() == 1,
                            path + ": rendered release marker")
                    if mode == "mobile":
                        cards = page.locator('.pdsp-crime').evaluate_all(
                            "xs => xs.map(x => ({x:x.getBoundingClientRect().x,y:x.getBoundingClientRect().y}))")
                        require(len(cards) == 3 and max(x['x'] for x in cards) - min(x['x'] for x in cards) < 2
                                and cards[0]['y'] < cards[1]['y'] < cards[2]['y'],
                                path + ": mobile attribution cards must stack")
                page.screenshot(path=str(report / ("pdsp-%s-%s.png" % (locale,mode))),
                                full_page=True)
                page.close()
        manifest = json.loads((ROOT / MANIFEST).read_text(encoding="utf-8"))
        for item in manifest['existing_pages']:
            path = item['path']
            for mode, width, height in (("desktop", 1440, 900), ("mobile", 390, 844)):
                page = browser.new_page(viewport={"width":width,"height":height})
                page.goto((ROOT/path).resolve().as_uri(), wait_until="domcontentloaded", timeout=30000)
                block = page.locator('#pdsp-accountability-20261124')
                require(block.count() == 1 and block.is_visible(), path + ": added section not visible")
                require(block.locator('[data-evidence-state="ATTRIBUTED_SUSPICION"]').count() == 1,
                        path + ": allegation qualification missing in browser")
                if (ROOT / RELEASE_MANIFEST).exists():
                    require(block.get_attribute('data-release') == RELEASE_CONTROL, path + ": release section")
                block.screenshot(path=str(report / ('pdsp-%s-%s-%s.png' % (item['language'],item['topic'],mode))))
                page.close()
        browser.close()
    print("PASS_RENDERED_TWELVE_ROUTES_EN_ES_DESKTOP_MOBILE")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", choices=["github","gitlab"], required=True)
    parser.add_argument("--render", action="store_true")
    parser.add_argument("--local", action="store_true", help="Local GitHub source review; never a native CI attestation")
    parser.add_argument("--browser-executable", help="Optional installed Chromium for local review only")
    args = parser.parse_args()
    require(not args.browser_executable or args.local, "native CI uses its pinned browser")
    check(args.host, args.local)
    if args.render:
        render(args.browser_executable)
