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
    "archive/MASTER_EXECUTION_PROMPT_DE_FACTO_MANAGEMENT_KNOWING_FACILITATION_VISIBILITY_20AUG2026.md",
    "archive/AC_DE_FACTO_MANAGEMENT_KNOWING_FACILITATION_VISIBILITY_CONTROL_20AUG2026.md",
    "archive/THREAD_DELETION_AUDIT_AC_DE_FACTO_KNOWING_FACILITATION_VISIBILITY_20AUG2026.md",
    "assets/data/ac-private-actor-de-facto-administration-v1.json",
    "assets/data/ac-de-facto-knowing-facilitation-visibility-v1.json",
    "assets/ac-community-de-facto-administration-20260820.js",
    "assets/ac-de-facto-knowing-facilitation-visibility-20260820.js",
    "assets/ac-de-facto-knowing-facilitation-stability-20260820.js",
    "es/administracion-de-hecho-comunidad-ac/index.html",
    "en/de-facto-administration-community-ac/index.html",
    "operations/AC_COMMUNITY_DE_FACTO_ADMINISTRATION_ACTIVATION_2026-08-20.md",
    "operations/AC_DE_FACTO_MANAGEMENT_KNOWING_FACILITATION_VISIBILITY_ACTIVATION_2026-08-20.md",
    "publication-manifests/ac-community-de-facto-administration-2026-08-20.json",
    "publication-manifests/ac-de-facto-knowing-facilitation-visibility-2026-08-20.json",
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
visibility = read("assets/ac-de-facto-knowing-facilitation-visibility-20260820.js")
stability = read("assets/ac-de-facto-knowing-facilitation-stability-20260820.js")
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
    ("data-ac-dfa-update", module, "base update marker"),
    ("data-ac-dfa-crosslink", module, "base crosslink marker"),
    ("Alegación transversal: administración de hecho y facilitación consciente", visibility, "Spanish attributed allegation headline"),
    ("Cross-cutting allegation: de facto management and knowing facilitation", visibility, "English attributed allegation headline"),
    ("data-ac-dfa-allegation-visibility", visibility, "visibility marker"),
    ("data-ac-dfa-impact-chain", visibility, "impact-chain marker"),
    ("data-ac-dfa-route-relevance", visibility, "route-relevance marker"),
    ("data-ac-dfa-route-type", visibility, "route-type marker"),
    ("downstream", visibility, "downstream route boundary"),
    ("panel.dataset.acDfaUpdate", stability, "base update marker preservation"),
    ("panel.dataset.acDfaCrosslink", stability, "base crosslink marker preservation"),
    ("panels.slice(1).forEach(removePanel)", stability, "duplicate-panel removal"),
    ("data-ac-de-facto-knowing-facilitation-visibility-loader", site, "visibility loader marker"),
    ("ac-de-facto-knowing-facilitation-visibility-20260820.js?v=20260820b", site, "visibility loader and cache bump"),
    ("data-ac-de-facto-knowing-facilitation-stability-loader", site, "stability loader marker"),
    ("ac-de-facto-knowing-facilitation-stability-20260820.js?v=20260820b", site, "stability loader and cache bump"),
    ("ac-community-de-facto-administration-20260820.js?v=20260820b", site, "base module cache bump"),
    ("sitemap-ac-community-de-facto-administration.xml", robots, "robots sitemap"),
    ("/por-derecho/es/administracion-de-hecho-comunidad-ac/", sitemap, "Spanish sitemap route"),
    ("/por-derecho/en/de-facto-administration-community-ac/", sitemap, "English sitemap route"),
]
for marker, text, label in checks:
    if marker not in text:
        errors.append(f"missing {label}: {marker}")

parent = load("assets/data/ac-private-actor-de-facto-administration-v1.json")
if parent.get("status") != "ACTIVE_FORENSIC_INVESTIGATION_NOT_A_FINDING":
    errors.append("parent dataset status boundary mismatch")
for key in ["criminal_guilt_established", "collusion_established", "full_shadow_administrator_status_established"]:
    if parent.get("public_boundary", {}).get(key) is not False:
        errors.append(f"parent dataset boundary mismatch: {key}")

visibility_data = load("assets/data/ac-de-facto-knowing-facilitation-visibility-v1.json")
if visibility_data.get("status") != "ATTRIBUTED_CROSS_CUTTING_ALLEGATION_ACTIVE_INVESTIGATION":
    errors.append("visibility dataset status mismatch")
public_allegation = visibility_data.get("public_allegation", {})
if public_allegation.get("attributed") is not True:
    errors.append("visibility allegation must be attributed")
if public_allegation.get("criminal_finding") is not False:
    errors.append("visibility allegation must not be a criminal finding")
if visibility_data.get("publication_boundaries", {}).get("infer_downstream_knowledge") is not False:
    errors.append("downstream knowledge-transfer boundary mismatch")
if len(visibility_data.get("route_classes", [])) < 7:
    errors.append("visibility route coverage is unexpectedly narrow")
if len(visibility_data.get("alleged_effect_chain", [])) < 8:
    errors.append("alleged effect chain is unexpectedly short")

manifest = load("publication-manifests/ac-community-de-facto-administration-2026-08-20.json")
if manifest.get("publication_id") != "AC-COMMUNITY-DE-FACTO-ADMINISTRATION-20260820":
    errors.append("parent manifest id mismatch")
visibility_manifest = load("publication-manifests/ac-de-facto-knowing-facilitation-visibility-2026-08-20.json")
if visibility_manifest.get("publication_id") != "AC-DE-FACTO-KNOWING-FACILITATION-VISIBILITY-20260820":
    errors.append("visibility manifest id mismatch")
if visibility_manifest.get("parent_publication_id") != "AC-COMMUNITY-DE-FACTO-ADMINISTRATION-20260820":
    errors.append("visibility manifest parent mismatch")
if "assets/ac-de-facto-knowing-facilitation-stability-20260820.js" not in visibility_manifest.get("expected_source_files", []):
    errors.append("visibility manifest does not track stability guard")

# Public/privacy safety: no raw private source indicators or personal IDs in the public modules/data.
for rel, text in [
    ("assets/ac-de-facto-knowing-facilitation-visibility-20260820.js", visibility),
    ("assets/ac-de-facto-knowing-facilitation-stability-20260820.js", stability),
    ("assets/data/ac-de-facto-knowing-facilitation-visibility-v1.json", read("assets/data/ac-de-facto-knowing-facilitation-visibility-v1.json")),
]:
    for forbidden in ["44700629Z", "message_id", "gmail", "privileged advice text"]:
        if forbidden.lower() in text.lower():
            errors.append(f"private/public boundary violation in {rel}: {forbidden}")

if errors:
    print("validation: FAIL", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print("validation: PASS")
