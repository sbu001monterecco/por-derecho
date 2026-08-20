#!/usr/bin/env python3
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
errors = []


def read(rel):
    path = ROOT / rel
    if not path.exists():
        errors.append(f"missing: {rel}")
        return ""
    return path.read_text(encoding="utf-8")


def load(rel):
    try:
        return json.loads(read(rel))
    except Exception as exc:
        errors.append(f"invalid json {rel}: {exc}")
        return {}

required = [
    "archive/AC_PRIVATE_ACTOR_DE_FACTO_ADMINISTRATION_COMMUNITY_DEBT_TEXTOS_FORENSIC_CONTROL_20AUG2026.md",
    "archive/AC_PRIVATE_ACTOR_DE_FACTO_ADMINISTRATION_RETRIEVAL_GATE_20AUG2026.md",
    "assets/data/ac-private-actor-de-facto-administration-v1.json",
    "assets/ac-community-de-facto-administration-20260820.js",
    "es/administracion-de-hecho-comunidad-ac/index.html",
    "en/de-facto-administration-community-ac/index.html",
    "operations/AC_COMMUNITY_DE_FACTO_ADMINISTRATION_ACTIVATION_2026-08-20.md",
    "publication-manifests/ac-community-de-facto-administration-2026-08-20.json",
    "sitemap-ac-community-de-facto-administration.xml",
    "scripts/render_ac_community_de_facto_administration.mjs",
    ".github/workflows/validate-ac-community-de-facto-administration.yml",
    ".github/workflows/verify-ac-community-de-facto-administration-live.yml",
]
for rel in required:
    read(rel)

es = read("es/administracion-de-hecho-comunidad-ac/index.html")
en = read("en/de-facto-administration-community-ac/index.html")
module = read("assets/ac-community-de-facto-administration-20260820.js")
site = read("assets/site.js")
robots = read("robots.txt")
sitemap = read("sitemap-ac-community-de-facto-administration.xml")

checks = [
    ('data-ac-community-shadow-control-page="20260820"', es, "Spanish marker"),
    ('data-ac-community-shadow-control-page="20260820"', en, "English marker"),
    ("718.663,24", es, "Spanish debt amount"),
    ("718,663.24", en, "English debt amount"),
    ("1.145.798,29", es, "Spanish bid amount"),
    ("1,145,798.29", en, "English bid amount"),
    ("data-ac-dfa-update", module, "update marker"),
    ("data-ac-dfa-crosslink", module, "crosslink marker"),
    ("ac-community-de-facto-administration-20260820.js", site, "site loader"),
    ("sitemap-ac-community-de-facto-administration.xml", robots, "robots sitemap"),
    ("/por-derecho/es/administracion-de-hecho-comunidad-ac/", sitemap, "Spanish sitemap route"),
    ("/por-derecho/en/de-facto-administration-community-ac/", sitemap, "English sitemap route"),
]
for marker, text, label in checks:
    if marker not in text:
        errors.append(f"missing {label}: {marker}")

data = load("assets/data/ac-private-actor-de-facto-administration-v1.json")
if data.get("status") != "ACTIVE_FORENSIC_INVESTIGATION_NOT_A_FINDING":
    errors.append("dataset status boundary mismatch")
for key in ["criminal_guilt_established", "collusion_established", "full_shadow_administrator_status_established"]:
    if data.get("public_boundary", {}).get(key) is not False:
        errors.append(f"dataset boundary mismatch: {key}")

manifest = load("publication-manifests/ac-community-de-facto-administration-2026-08-20.json")
if manifest.get("publication_id") != "AC-COMMUNITY-DE-FACTO-ADMINISTRATION-20260820":
    errors.append("manifest id mismatch")

if errors:
    print("validation: FAIL", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print("validation: PASS")
