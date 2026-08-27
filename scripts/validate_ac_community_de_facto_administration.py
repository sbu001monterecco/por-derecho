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
    ('data-ac-community-shadow-control-page="20260824"', es, "Spanish 20260824 marker"),
    ('data-ac-community-shadow-control-page="20260824"', en, "English 20260824 marker"),
    ("Francisco Mario Matos Matas, Antonio Cogolludo Rojas, Shaila María Cogolludo Ramos, José Daniel Acosta Matos y Laura Patricia Acosta Matos", es, "Spanish five-actor perimeter"),
    ("Francisco Mario Matos Matas, Antonio Cogolludo Rojas, Shaila María Cogolludo Ramos, José Daniel Acosta Matos and Laura Patricia Acosta Matos", en, "English five-actor perimeter"),
    ("correos, reuniones, peticiones, autorizaciones, decisiones, implementación, adopción y ratificación", es, "Spanish affirmative Administrator conduct"),
    ("emails, meetings, requests, authorisations, decisions, implementation, adoption and ratification", en, "English affirmative Administrator conduct"),
    ("el Ilmo. Sr. D. Alberto López Villarrubia, Magistrado-Juez del entonces Juzgado de lo Mercantil n.º 1 de Las Palmas de Gran Canaria", es, "Spanish controlled historical judicial title"),
    ("el Ilmo. Sr. D. Alberto López Villarrubia, Magistrado-Juez del entonces Juzgado de lo Mercantil n.º 1 de Las Palmas de Gran Canaria", en, "English page preserves the controlled historical judicial title"),
    ("salida desarrollada y respaldada por financiación", es, "Spanish funded-exit allegation"),
    ("developed, finance-backed exit", en, "English funded-exit allegation"),
    ("NO DECLARACIÓN JUDICIAL", es, "Spanish non-finding boundary"),
    ("NOT A JUDICIAL FINDING", en, "English non-finding boundary"),
    ("718.663,24", es, "Spanish debt amount"),
    ("718,663.24", en, "English debt amount"),
    ("1.145.798,29", es, "Spanish bid amount"),
    ("1,145,798.29", en, "English bid amount"),
    ("data-ac-dfa-update", module, "base update marker"),
    ("data-ac-dfa-crosslink", module, "base crosslink marker"),
    ("Cinco administradores en la sombra alegados y una habilitación institucional activa", visibility, "Spanish attributed allegation headline"),
    ("Five alleged shadow administrators and active institutional enablement", visibility, "English attributed allegation headline"),
    ("Francisco Mario Matos Matas, Antonio Cogolludo Rojas, Shaila María Cogolludo Ramos", visibility, "visibility layer names the private perimeter"),
    ("Alberto López Villarrubia", visibility, "visibility layer names the judicial actor"),
    ("data-ac-dfa-allegation-visibility", visibility, "visibility marker"),
    ("data-ac-dfa-impact-chain", visibility, "impact-chain marker"),
    ("data-ac-dfa-route-relevance", visibility, "route-relevance marker"),
    ("data-ac-dfa-route-type", visibility, "route-type marker"),
    ("downstream", visibility, "downstream route boundary"),
    ("panel.dataset.acDfaUpdate", stability, "base update marker preservation"),
    ("panel.dataset.acDfaCrosslink", stability, "base crosslink marker preservation"),
    ("panels.slice(1).forEach(removePanel)", stability, "duplicate-panel removal"),
    ("data-ac-de-facto-knowing-facilitation-visibility-loader", site, "visibility loader marker"),
    ("ac-de-facto-knowing-facilitation-visibility-20260820.js?v=20260824a", site, "visibility loader and cache bump"),
    ("data-ac-de-facto-knowing-facilitation-stability-loader", site, "stability loader marker"),
    ("ac-de-facto-knowing-facilitation-stability-20260820.js?v=20260824a", site, "stability loader and cache bump"),
    ("ac-community-de-facto-administration-20260820.js?v=20260824a", site, "20260824 base module cache bump"),
    ("sitemap-ac-community-de-facto-administration.xml", robots, "robots sitemap"),
    ("/por-derecho/es/administracion-de-hecho-comunidad-ac/", sitemap, "Spanish sitemap route"),
    ("/por-derecho/en/de-facto-administration-community-ac/", sitemap, "English sitemap route"),
]
for marker, text, label in checks:
    if marker not in text:
        errors.append(f"missing {label}: {marker}")

parent = load("assets/data/ac-private-actor-de-facto-administration-v1.json")
if parent.get("schema_version") != "1.2":
    errors.append("parent dataset schema_version must be 1.2")
if parent.get("control_date") != "2026-08-24":
    errors.append("parent dataset control date must reflect the 20260824 substantive update")
update_marker = "five-actor-shadow-administration-ac-judicial-acts-omissions-funded-exit-20260824"
if parent.get("substantive_update_marker") != update_marker:
    errors.append("parent dataset 20260824 substantive-update marker mismatch")
expected_update_controls = {
    "FIVE_ACTOR_SHADOW_DE_FACTO_ADMINISTRATION_DIRECT_ALLEGATION_20260824",
    "AC_AFFIRMATIVE_COMMISSIONS_ENABLEMENT_AND_OMISSIONS_DIRECT_ALLEGATION_20260824",
    "JUDICIAL_AFFIRMATIVE_ACTS_OMISSIONS_FUNDED_EXIT_SABOTAGE_DIRECT_ALLEGATION_20260824",
    "AWESWELL_SPONSOR_PERFORMANCE_COLLATERAL_AND_INSTITUTIONAL_DEPENDENCIES_20260824",
}
if set(parent.get("update_controls", [])) != expected_update_controls:
    errors.append("parent dataset must contain the four exact 20260824 allegation and finance controls")
if parent.get("status") != "ACTIVE_FORENSIC_INVESTIGATION_NOT_A_FINDING":
    errors.append("parent dataset status boundary mismatch")
for key in ["criminal_guilt_established", "collusion_established", "full_shadow_administrator_status_established"]:
    if parent.get("public_boundary", {}).get(key) is not False:
        errors.append(f"parent dataset boundary mismatch: {key}")
for key in [
    "five_actor_collective_participation_in_every_step_established",
    "administrator_commission_or_omission_criminally_adjudicated",
    "judicial_acts_or_omissions_criminally_adjudicated",
    "funded_exit_sabotage_adjudicated",
]:
    if parent.get("public_boundary", {}).get(key) is not False:
        errors.append(f"parent dataset 20260824 non-adjudication boundary mismatch: {key}")
if parent.get("public_boundary", {}).get("five_actor_shadow_administration_allegation_attributed") is not True:
    errors.append("parent dataset must preserve Gil's attributed five-actor allegation")

central = parent.get("central_hypothesis", {})
if central.get("attributed_to") != "Gil Marer" or central.get("attributed") is not True:
    errors.append("central hypothesis must remain directly attributed to Gil Marer")
if central.get("criminal_finding") is not False or central.get("not_a_finding") is not True:
    errors.append("central hypothesis must preserve the allegation/not-finding distinction")
for phrase in (
    "administración de hecho y control material paralelo presuntamente ocultado",
    "de facto or shadow-administration architecture and allegedly concealed parallel material control",
    "actos afirmativos y omisiones",
    "affirmative acts and omissions",
):
    if phrase not in f"{central.get('es', '')}\n{central.get('en', '')}":
        errors.append(f"central hypothesis missing required 20260824 copy: {phrase}")

expected_private_actors = [
    ("ACT-FMMM", "Francisco Mario Matos Matas"),
    ("ACT-ACR", "Antonio Cogolludo Rojas"),
    ("ACT-SMCR", "Shaila María Cogolludo Ramos"),
    ("ACT-JDAM", "José Daniel Acosta Matos"),
    ("ACT-LPAM", "Laura Patricia Acosta Matos"),
]
private_perimeter = parent.get("canonical_private_actor_perimeter_20260824", {})
actual_private_actors = [
    (actor.get("id"), actor.get("name"))
    for actor in private_perimeter.get("actors", [])
    if isinstance(actor, dict)
]
if actual_private_actors != expected_private_actors:
    errors.append("parent dataset five-private-actor perimeter is missing, reordered or misnamed")
if private_perimeter.get("criminal_finding") is not False:
    errors.append("five-actor shadow-administration allegation must not be represented as a finding")
for key in ("collective_participation_in_every_step_established", "shared_criminal_intent_established"):
    if private_perimeter.get(key) is not False:
        errors.append(f"five-actor perimeter boundary mismatch: {key}")
if "directly alleges a five-actor shadow/de facto administration" not in private_perimeter.get("direct_allegation", ""):
    errors.append("five-actor perimeter must preserve Gil's direct shadow/de facto-administration copy")

institutional = parent.get("institutional_attributions_20260824", {})
administrator = institutional.get("insolvency_administrator", {})
judge = institutional.get("judge", {})
if administrator.get("actor") != "Francisco de Borja Rodríguez-Batllori Laffitte":
    errors.append("20260824 Administrator institutional actor mismatch")
if administrator.get("marker") != "AC_AFFIRMATIVE_COMMISSIONS_ENABLEMENT_AND_OMISSIONS_DIRECT_ALLEGATION_20260824":
    errors.append("20260824 Administrator allegation marker mismatch")
if administrator.get("attributed_to") != "Gil Marer" or administrator.get("direct_criminal_allegation") is not True:
    errors.append("Administrator commissions-and-omissions allegation must be directly attributed to Gil")
if administrator.get("criminal_finding") is not False:
    errors.append("Administrator allegation must not be represented as a criminal finding")
for key, minimum in (
    ("affirmative_commissions_and_enablement_alleged", 4),
    ("omissions_alleged", 4),
    ("documented_basis", 4),
    ("contrary_evidence", 3),
    ("unresolved_proof", 4),
):
    if len(administrator.get(key, [])) < minimum:
        errors.append(f"Administrator 20260824 control is too thin: {key}")
if "conditionally closable exit" not in administrator.get("funded_exit_sabotage_claim", "").lower():
    errors.append("Administrator 20260824 conditional finance-exit allegation is missing")

if judge.get("actor") != "Alberto López Villarrubia":
    errors.append("20260824 judge institutional actor mismatch")
if judge.get("marker") != "JUDICIAL_AFFIRMATIVE_ACTS_OMISSIONS_FUNDED_EXIT_SABOTAGE_DIRECT_ALLEGATION_20260824":
    errors.append("20260824 judicial allegation marker mismatch")
if judge.get("attributed_to") != "Gil Marer" or judge.get("direct_criminal_allegation") is not True:
    errors.append("judicial acts-and-omissions allegation must be directly attributed to Gil")
if judge.get("criminal_finding") is not False:
    errors.append("judicial allegation must not be represented as a criminal finding")
for key, minimum in (
    ("affirmative_acts_alleged", 3),
    ("omissions_alleged", 4),
    ("documented_basis", 3),
    ("contrary_evidence", 4),
    ("unresolved_proof", 4),
):
    if len(judge.get(key, [])) < minimum:
        errors.append(f"judicial 20260824 control is too thin: {key}")
funded_exit_claim = judge.get("funded_exit_sabotage_claim", "")
for phrase in ("direct enabling role", "affirmative acts and omissions", "Daniel Irigoyen", "conditionally closable exit"):
    if phrase not in funded_exit_claim:
        errors.append(f"judicial funded-exit allegation missing required copy: {phrase}")

finance_marker = "AWESWELL_SPONSOR_PERFORMANCE_COLLATERAL_AND_INSTITUTIONAL_DEPENDENCIES_20260824"
finance = parent.get("finance_condition_allocation_20260824", {})
if finance.get("marker") != finance_marker or finance.get("attributed_to") != "Gil Marer":
    errors.append("parent finance-condition control marker or attribution mismatch")
finance_direct = finance.get("direct_allegation", {})
if finance_direct.get("criminal_finding") is not False or finance_direct.get("causation_adjudicated") is not False:
    errors.append("parent finance-condition allegation must remain a non-finding")
for phrase in (
    "performed or could perform all sponsor-side",
    "staged security and collateral package",
    "Insolvency Administrator debt certificate",
    "lender-in-possession mechanism obstructing redemption and refinancing",
):
    if phrase not in finance_direct.get("en", ""):
        errors.append(f"parent finance-condition allegation missing copy: {phrase}")
condition_classes = finance.get("condition_classes", {})
for key in ("sponsor_borrower_or_counterparty_side", "court_administrator_and_collateral_dependencies", "lender_internal_or_third_party"):
    if len(condition_classes.get(key, {}).get("documented_conditions", [])) < 4:
        errors.append(f"parent finance-condition class is too thin: {key}")
routes = finance.get("route_source_status", {})
if set(routes) != {"ona_clubotel", "stoneweg_vso", "ben_oldman", "lagune_elaia"}:
    errors.append("parent finance-condition control must preserve the four exact route source-status records")
for route in routes.values():
    if not route.get("status") or not route.get("limits"):
        errors.append("parent finance route lacks status or limits")
if len(finance.get("publication_boundaries", [])) < 5 or len(finance.get("unresolved_evidence", [])) < 6:
    errors.append("parent finance-condition boundaries or unresolved-evidence ledger is too thin")

visibility_data = load("assets/data/ac-de-facto-knowing-facilitation-visibility-v1.json")
if visibility_data.get("schema_version") != "1.2":
    errors.append("visibility dataset schema_version must be 1.2")
if visibility_data.get("control_date") != "2026-08-24":
    errors.append("visibility dataset control date must reflect the 20260824 update")
if visibility_data.get("substantive_update_marker") != update_marker:
    errors.append("visibility dataset substantive-update marker mismatch")
if visibility_data.get("status") != "ATTRIBUTED_CROSS_CUTTING_ALLEGATION_ACTIVE_INVESTIGATION":
    errors.append("visibility dataset status mismatch")
public_allegation = visibility_data.get("public_allegation", {})
if public_allegation.get("attributed") is not True:
    errors.append("visibility allegation must be attributed")
if public_allegation.get("criminal_finding") is not False:
    errors.append("visibility allegation must not be a criminal finding")
if set(visibility_data.get("canonical_private_actor_perimeter", [])) != {name for _, name in expected_private_actors}:
    errors.append("visibility dataset must preserve the exact five-actor perimeter")
visibility_nodes = visibility_data.get("institutional_nodes", {})
if visibility_nodes.get("insolvency_administrator", {}).get("name") != "Francisco de Borja Rodríguez-Batllori Laffitte":
    errors.append("visibility dataset must preserve the full Administrator identity")
if visibility_nodes.get("judge", {}).get("name") != "Alberto López Villarrubia":
    errors.append("visibility dataset must preserve the judicial actor identity")
if visibility_data.get("publication_boundaries", {}).get("infer_downstream_knowledge") is not False:
    errors.append("downstream knowledge-transfer boundary mismatch")
if len(visibility_data.get("route_classes", [])) < 7:
    errors.append("visibility route coverage is unexpectedly narrow")
if len(visibility_data.get("alleged_effect_chain", [])) < 8:
    errors.append("alleged effect chain is unexpectedly short")
visibility_finance = visibility_data.get("finance_condition_allocation_20260824", {})
if visibility_finance.get("marker") != finance_marker or visibility_finance.get("attributed_to") != "Gil Marer":
    errors.append("visibility finance-condition marker or attribution mismatch")
visibility_finance_direct = visibility_finance.get("direct_allegation", {})
if visibility_finance_direct.get("criminal_finding") is not False or visibility_finance_direct.get("causation_adjudicated") is not False:
    errors.append("visibility finance-condition allegation must remain a non-finding")
if set(visibility_finance.get("route_source_status", {})) != {"ona_clubotel", "stoneweg_vso", "ben_oldman", "lagune_elaia"}:
    errors.append("visibility finance-condition control must preserve ONA, VSO, Ben Oldman and Elaia source status")
visibility_classes = visibility_finance.get("condition_allocation", {})
for key in ("sponsor_borrower_or_counterparty", "court_administrator_or_collateral_dependency", "lender_internal_or_third_party"):
    if len(visibility_classes.get(key, {}).get("examples", [])) < 4:
        errors.append(f"visibility finance-condition class is too thin: {key}")
for rel, text in (
    ("assets/data/ac-private-actor-de-facto-administration-v1.json", read("assets/data/ac-private-actor-de-facto-administration-v1.json")),
    ("assets/data/ac-de-facto-knowing-facilitation-visibility-v1.json", read("assets/data/ac-de-facto-knowing-facilitation-visibility-v1.json")),
):
    if "mafia" in text.lower():
        errors.append(f"non-institutional criminal epithet exposed in {rel}")

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
