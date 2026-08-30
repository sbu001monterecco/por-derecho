#!/usr/bin/env python3
"""Validate the post-7-June-2018 / 4-February-2022 unitary control package."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "assets/data/sun-park-post-7june-2018-2022-continuing-harm-v1.json"
REGISTRY = ROOT / "assets/data/matter-identity-registry-v1.json"
PEOPLE = ROOT / "assets/data/matter-identity-registry-v1.people.json"
ORGANISATIONS = ROOT / "assets/data/matter-identity-registry-v1.organisations.json"
IMAGE = ROOT / "assets/acosta-matos-family-hotel-plans.jpg"
PROMPT = ROOT / "archive/prompts/SUN_PARK_POST7JUNE_2018_TO_2022_DELIBERATE_EXCLUSION_UNITARY_CRIMINAL_REVERSE_ENGINEERING_PROMPT_28AUG2026.md"
REPORT = ROOT / "archive/SUN_PARK_POST_7JUNE_2018_TO_4FEB2022_CONTINUING_HARM_CRIMINAL_FIRST_REVERSE_ENGINEERING_28AUG2026.md"
DECLARATION = ROOT / "archive/declarations/017_GIL_THOMPSON_POST_MEETING_ACTA_FORWARDING_AND_CONCEALED_MEETINGS_20260828.md"
PROVENANCE = ROOT / "evidence/community/actas/2022-02-04/provenance.md"
MANIFEST = ROOT / "evidence/community/actas/2022-02-04/manifest.json"
THOMPSON_AUDIT = ROOT / "docs/deletion-audits/2026-08-28-thompson-post-meeting-acta-forwarding-continuity.md"
OMNI_AUDIT = ROOT / "docs/deletion-audits/2026-08-28-2022-acta-omnidirectional-enablement-visual-continuity.md"
OMNI_CSS = ROOT / "assets/post7-2022-omnidirectional-map-20260828.css"
OMNI_MANIFEST = ROOT / "publication-manifests/post7june-2022-omnidirectional-enablement-20260828.json"
INTERLINK_MANIFEST = ROOT / "publication-manifests/post7june-2022-reciprocal-route-interlink-20260828.json"
ALBERTO_LIVE_WORKFLOW = ROOT / ".github/workflows/alberto-meeting-point-cross-proceeding.yml"
INTERLINK_BUILDER = ROOT / "scripts/build_post7june_route_interlinks.py"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_markers(path: Path, markers: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    for marker in markers:
        require(marker in text, f"{path.relative_to(ROOT)} missing marker: {marker}")


def attributed_links(text: str, attribute: str) -> dict[str, str]:
    links: dict[str, str] = {}
    for tag in re.findall(r"<a\b[^>]*>", text):
        key = re.search(rf'{re.escape(attribute)}="([^"]+)"', tag)
        href = re.search(r'href="([^"]+)"', tag)
        if key and href:
            links[key.group(1)] = href.group(1)
    return links


def require_local_destination(source: Path, href: str, expected: Path) -> None:
    route, _, fragment = href.partition("#")
    if route.startswith("/"):
        resolved = ROOT / route.lstrip("/")
    elif route:
        resolved = (source.parent / route).resolve()
    else:
        resolved = source.resolve()
    if route.endswith("/"):
        resolved /= "index.html"
    require(resolved == expected.resolve(), f"{source.relative_to(ROOT)} misroutes {href} to {resolved.relative_to(ROOT)}")
    require(expected.is_file(), f"missing reciprocal destination: {expected.relative_to(ROOT)}")
    if fragment:
        require(f'id="{fragment}"' in expected.read_text(encoding="utf-8"), f"{source.relative_to(ROOT)} missing destination fragment: {href}")


def main() -> int:
    case = load_json(DATA)
    registry = load_json(REGISTRY)
    people = load_json(PEOPLE)["records"]
    organisations = load_json(ORGANISATIONS)["records"]

    require(case["control_id"] == "PD-SP-POST7J-20260828-01", "case control ID mismatch")
    require(case["execution_prompt"] == str(PROMPT.relative_to(ROOT)), "execution prompt not routed")

    scope = case["caepr_scope_audit"]
    require((scope["denominator"], scope["confirmed"], scope["coverage_percent"]) == (6, 6, 100), "combined caret scope is not 6/6")
    expected_scope_ids = {
        "PD-SP-P-0011",
        "PD-SP-P-0012",
        "PD-SP-P-0093",
        "PD-SP-P-0094",
        "PD-SP-O-0074",
        "PD-SP-O-0005",
    }
    require({item["caepr_id"] for item in scope["objects"]} == expected_scope_ids, "combined caret object set mismatch")
    require(
        [(item["denominator"], item["confirmed"]) for item in scope["subscopes"]] == [(3, 3), (4, 4)],
        "meeting/image subscopes are not 3/3 and 4/4",
    )

    proof = case["meeting_2022_02_04"]["deliberate_exclusion_proof_model"]
    require(len(proof["unitary_sequence"]) == 7, "unitary call-to-later-use sequence is incomplete")
    require(len(proof["capable_of_proving_intent_when_convergent"]) >= 7, "intent proof package is incomplete")
    require("can be guaranteed" in proof["criminal_boundary"], "future-proof guarantee boundary missing")
    require("native invitation" in " ".join(proof["does_not_now"]).lower(), "native invitation gap missing")
    require("ownership_cost_fork" in case["meeting_2022_02_04"], "ownership/cost fork missing")

    omni = case["omnidirectional_enablement_map"]
    require(len(omni["incoming_tracks"]) == 4, "omnidirectional map must retain four incoming tracks")
    require(len(omni["hub_sequence"]) == 6, "omnidirectional map must retain six process stages")
    require(len(omni["outgoing_tracks"]) == 4, "omnidirectional map must retain four outgoing tracks")
    require("does not establish agreement" in omni["connector_rule"], "connector non-finding rule missing")
    require("protection architecture" in omni["judicial_safeguards_language"], "judicial-safeguards wording missing")
    require("not an autonomous criminal offence" in omni["hotel_mobbing_boundary"], "hotel-mobbing boundary missing")
    require("stable autonomous management" in omni["de_facto_administrator_boundary"], "de facto administrator test missing")
    require("Valid common or necessary works" in omni["lawful_alternative"], "lawful works allocation alternative missing")

    junction = omni["reciprocal_route_junction"]
    require(junction["id"] == "POST7J-ROUTE-JUNCTION-01", "reciprocal junction ID drift")
    require(junction["control_id"] == case["control_id"], "reciprocal junction control ID drift")
    require("separate legal persons" in junction["rule"], "reciprocal junction separation rule missing")
    require(junction["link_contract"] == {
        "core_route_destinations": 12,
        "satellite_routes": 9,
        "bilingual_satellite_pages": 18,
        "every_core_page_links_to_every_satellite": True,
        "every_satellite_page_links_to_both_core_routes": True,
    }, "reciprocal junction contract drift")
    expected_route_ids = {
        "takeover", "meeting", "community", "acosta", "ona", "estate",
        "de-facto", "club-sei", "deed", "funding", "financial-lives", "data",
    }
    core_paths = [
        ROOT / junction["core_routes"][core][locale]
        for locale in ("en", "es")
        for core in ("takeover", "meeting")
    ]
    for path in core_paths:
        text = path.read_text(encoding="utf-8")
        require(text.count(f'data-post7-evidence-junction="{case["control_id"]}"') == 1, f"{path.relative_to(ROOT)} junction denominator drift")
        links = attributed_links(text, "data-post7-route")
        require(set(links) == expected_route_ids, f"{path.relative_to(ROOT)} route set drift")
        locale = path.relative_to(ROOT).parts[0]
        expected_destinations = {
            core: ROOT / junction["core_routes"][core][locale]
            for core in ("takeover", "meeting")
        }
        expected_destinations.update({item["id"]: ROOT / item[locale] for item in junction["satellite_routes"]})
        expected_destinations["data"] = ROOT / junction["structured_model"]
        for route_id, expected in expected_destinations.items():
            require_local_destination(path, links[route_id], expected)

    satellites = junction["satellite_routes"]
    require(len(satellites) == 9, "reciprocal satellite-route denominator drift")
    require({item["id"] for item in satellites} == expected_route_ids - {"takeover", "meeting", "data"}, "reciprocal satellite-route IDs drift")
    for item in satellites:
        for locale in ("en", "es"):
            path = ROOT / item[locale]
            markers = [
                f'data-post7-evidence-backlink="{case["control_id"]}"',
                f'data-post7-route-id="{item["id"]}"',
                'data-post7-core="takeover"',
                'data-post7-core="meeting"',
            ]
            require_markers(path, markers)
            links = attributed_links(path.read_text(encoding="utf-8"), "data-post7-core")
            require(set(links) == {"takeover", "meeting"}, f"{path.relative_to(ROOT)} core backlink set drift")
            for core in ("takeover", "meeting"):
                require_local_destination(path, links[core], ROOT / junction["core_routes"][core][locale])
    require_markers(INTERLINK_BUILDER, ["POST7J-EVIDENCE-JUNCTION:BEGIN", "BUILT {changed} PAGES"])

    receipt = case["meeting_2022_02_04"]["post_meeting_indirect_receipt"]
    require(receipt["after_meeting"]["acta_obtained"] is True, "corrected ACTA receipt state missing")
    require(receipt["after_meeting"]["direct_community_communication_received"] is False, "direct Community receipt boundary missing")
    require(receipt["after_meeting"]["route"] == "indirect forwarding by the Thompson family", "Thompson relay route mismatch")
    require(receipt["after_meeting"]["native_message_status"] == "OPEN", "native Thompson message must remain open")
    require("26-April-2016" in receipt["pattern_since_2016"]["mandatory_limiting_evidence"], "2016 known-meeting counterexample missing")
    require(receipt["thompson_context"]["unit_lead"] == "bungalow 708 / registered property 8,557", "Thompson unit lead drift")
    event_matrix = receipt["pattern_since_2016"]["preliminary_event_matrix"]
    require(len(event_matrix) == 8, "2016-2022 preliminary event matrix must contain eight controlled events")
    require(event_matrix[0]["classification"] == "KNOWN_OR_PARTICIPATED_COUNTEREXAMPLE", "2016 counterexample classification drift")
    require(event_matrix[-1]["classification"] == "DIRECT_ATTRIBUTED_NO_PREKNOWLEDGE_INDIRECT_POST_MEETING_RECEIPT", "2022 receipt classification drift")

    acta_manifest = load_json(MANIFEST)
    acquisition = acta_manifest["acquisition_provenance"]
    require("Thompson family" in acquisition["route"], "ACTA manifest lacks Thompson acquisition route")
    require(acquisition["attachment_to_controlled_copy_hash_bridge"] == "OPEN", "ACTA attachment hash bridge overstated")

    image = case["four_sibling_image"]
    expected_hash = "aad5ebaffddf8211be21468f5936b6b1a0066c631919a43a06e9886a9061cd37"
    require(hashlib.sha256(IMAGE.read_bytes()).hexdigest() == expected_hash, "plans image SHA-256 mismatch")
    require(image["sha256"] == expected_hash, "structured image SHA-256 mismatch")
    require(
        [item["caepr_id"] for item in image["left_to_right"]]
        == ["PD-SP-P-0093", "PD-SP-P-0012", "PD-SP-P-0011", "PD-SP-P-0094"],
        "Gil-attributed left-to-right image order mismatch",
    )
    require(len(image["does_not_prove"]) >= 5, "image evidentiary ceiling incomplete")

    actors = {item.get("caepr_id"): item for item in case["actors"] if item.get("caepr_id")}
    require("PD-SP-P-0093" in actors and "PD-SP-P-0094" in actors, "Javier/Gerardo actor rows missing")

    require(registry["counts"] == {
        "total": 228,
        "PERSON": 95,
        "ORGANISATION": 79,
        "STRUCTURE": 11,
        "INSTITUTION": 23,
        "PROCEEDING": 20,
    }, "master registry counts mismatch")
    by_id = {item["id"]: item for item in people}
    expected_people = {
        "PD-SP-P-0088": "Fernando Aguiar Acosta",
        "PD-SP-P-0089": "Laura Hernando",
        "PD-SP-P-0090": "Miguel Vázquez",
        "PD-SP-P-0091": "Fernando Banderas Monis",
        "PD-SP-P-0092": "Juan José Vera Díaz",
        "PD-SP-P-0093": "Javier Acosta Matos",
        "PD-SP-P-0094": "Gerardo Zacarías Acosta Matos",
    }
    require(
        all(by_id[item_id]["name"] == name for item_id, name in expected_people.items()),
        "merge-time person identity reconciliation drift",
    )
    by_org_id = {item["id"]: item for item in organisations}
    expected_organisations = {
        "PD-SP-O-0072": "IREA Corporate Finance, S.L.",
        "PD-SP-O-0073": "Colliers International Spain, S.L.",
        "PD-SP-O-0074": "Construcciones Acos-Matos, S.L.",
    }
    require(
        all(by_org_id[item_id]["name"] == name for item_id, name in expected_organisations.items()),
        "merge-time organisation identity reconciliation drift",
    )
    require("PD-SP-P-0091" in by_id["PD-SP-P-0088"].get("not_same_as", []), "two-Fernando non-equivalence missing")
    require("PD-SP-P-0088" in by_id["PD-SP-P-0091"].get("not_same_as", []), "two-Fernando reverse non-equivalence missing")
    require("PD-SP-P-0094" in by_id["PD-SP-P-0013"].get("not_same_as", []), "father/son non-equivalence missing")
    require("PD-SP-P-0013" in by_id["PD-SP-P-0094"].get("not_same_as", []), "son/father non-equivalence missing")

    require_markers(PROMPT, [
        "What does the located ACTA already prove?",
        "What does the corrected receipt account add?",
        "26-April-2016 Owners' Community meeting is mandatory limiting evidence",
        "native 4-February invitation/convocation",
        "This is a title, control, benefit and cost-allocation inquiry—not arithmetic.",
        "Javier Acosta Matos^ (younger person at far left)",
        "Gerardo Zacarías Acosta Matos^ (bearded person at far right)",
    ])
    require_markers(REPORT, [
        "### 5.4.1 Omnidirectional 4-February bridge — inputs, transformation and outputs",
        "LPB assets formally subject to insolvency-administration and judicial-supervision safeguards",
        "“Hotel mobbing”",
        "De facto administrator / shadow director does not mean influence",
        "### 5.7 What can, what does and what could establish deliberate exclusion",
        "### 5.8 The alleged wider sequence — call, meeting, ACTA and later use",
        "#### 5.9.1 Thompson relay and the alleged pattern from at least 2016",
        "### 5.10 The ownership-and-cost fork inside the same ACTA",
        "### 5.11 The Acosta Matos plans image — significance and boundary",
    ])
    require_markers(DECLARATION, [
        "D017-P02",
        "after the meeting had taken place, the Thompson family forwarded the ACTA",
        "26-April-2016 Owners' Community meeting was known",
        "bungalow 708 / property 8,557",
    ])
    require_markers(PROVENANCE, [
        "Ruta de adquisición atribuida",
        "familia Thompson",
        "comparación hash",
    ])
    require_markers(THOMPSON_AUDIT, [
        "no invitation / no pre-meeting knowledge",
        "indirect Thompson forwarding after the meeting",
        "26-April-2016 meeting was known and attended",
    ])
    require_markers(OMNI_AUDIT, [
        "omnidirectional enabling-episode theory",
        "formal protection architecture",
        "not a standalone offence",
        "de facto administrator",
        "LIVE_VERIFIED",
        "PR #1146",
        "#1217",
    ])
    require_markers(OMNI_CSS, [
        ".omni-acta-map",
        ".omni-map-board",
        ".omni-map-hub",
        ".omni-process",
        "content: \"⇄\"",
        "@media (max-width: 620px)",
    ])
    require_markers(ALBERTO_LIVE_WORKFLOW, [
        "'total': 214",
        "'PERSON': 94",
        "'ORGANISATION': 74",
        "data-static-registry-counts=\"214-94-74-10-18-18\"",
        "identity_registry_parity'] == 204",
        "'identity_source_current': 214",
        "'specialist_historical_identity_snapshot': 204",
    ])
    omni_manifest = load_json(OMNI_MANIFEST)
    require(
        omni_manifest["state"]
        in {
            "LOCAL_PREPARED_NOT_PUBLISHED",
            "AUTHORIZED_FOR_PUSH_PR_MERGE_PAGES",
            "LIVE_VERIFIED",
        },
        "omnidirectional publication state unrecognised",
    )
    require(len(omni_manifest["routes"]) == 4, "omnidirectional manifest route denominator mismatch")
    require(omni_manifest["visual_model"]["incoming_tracks"] == 4, "manifest incoming-track count mismatch")
    require(omni_manifest["visual_model"]["hub_stages"] == 6, "manifest hub-stage count mismatch")
    require(omni_manifest["visual_model"]["outgoing_tracks"] == 4, "manifest outgoing-track count mismatch")
    require(omni_manifest["current_state"] == "LIVE_VERIFIED", "omnidirectional closeout is not live verified")
    require(omni_manifest["merge_sha"] == "faea6677f3a4df30eeefa92916d77a09826a0bab", "publication merge SHA drift")
    require(omni_manifest["validation"]["pull_request_checks"] == "PASS_36_OF_36", "PR check denominator drift")
    require(omni_manifest["validation"]["acta_workflow_run_id"] == 33168858619, "ACTA workflow evidence drift")
    require(omni_manifest["deployment_evidence"]["workflow_run_id"] == 33169202514, "Pages run evidence drift")
    require(len(omni_manifest["live_urls"]) == 8, "live URL denominator must remain eight")
    readback = omni_manifest["publication_result"]["live_readback"]["results"]
    require(len(readback) == 8, "exact live-readback denominator must remain eight")
    require(all(item["status"] == 200 and item["parity"] == "EXACT" for item in readback), "live-readback parity drift")
    governance = omni_manifest["governance_closeout"]
    require(governance["pull_request"].endswith("/1147"), "governance closeout PR drift")
    require(governance["merge_sha"] == "4f807502fc52f46fc80f369ba58decd4c25af733", "governance closeout merge SHA drift")
    require(governance["pages_workflow_run_id"] == 33170196929, "governance closeout Pages run drift")
    require(governance["public_edge_readback"]["status"] == "PASS_15_OF_15_HTTP_200_EXACT_REPOSITORY_BYTES", "governance public-edge result drift")
    followup = governance["post_merge_workflow_followup"]
    require(followup["failed_run_id"] == 33170197823, "push-only workflow failure run drift")
    require("current 214/94/74/10/18/18 registry" in followup["remediation_rule"], "current-registry remediation missing")
    require("historical identity_registry_parity value of 204" in followup["remediation_rule"], "historical specialist snapshot boundary missing")
    require(followup["verbatim_readback_reproduction"].startswith("PASS_41_EXACT_BYTE_SURFACES"), "corrected live-verifier reproduction missing")
    require(all(omni_manifest["external_actions"][key] is True for key in ("push", "pull_request", "merge", "deployment", "live_readback")), "publication action closeout incomplete")
    require(omni_manifest["external_actions"]["filing_or_contact"] is False, "filing/contact boundary drift")

    interlink_manifest = load_json(INTERLINK_MANIFEST)
    require(interlink_manifest["parent_control_id"] == case["control_id"], "interlink parent control drift")
    require(interlink_manifest["state"] == "LIVE_VERIFIED", "interlink publication state drift")
    require(interlink_manifest["current_state"] == "LIVE_VERIFIED", "interlink closeout is not live verified")
    require(interlink_manifest["junction_contract"]["destinations_per_core_page"] == 12, "interlink manifest core denominator drift")
    require(interlink_manifest["junction_contract"]["bilingual_satellite_pages"] == 18, "interlink manifest satellite denominator drift")
    require(interlink_manifest["validation"]["pull_request_checks"] == "PASS_27_OF_27", "interlink PR check denominator drift")
    require(interlink_manifest["validation"]["browser_execution"] == "PASS_30_ROUTE_VIEWPORT_CHECKS", "interlink browser evidence drift")
    interlink_result = interlink_manifest["publication_result"]
    require(interlink_result["pull_request"].endswith("/1149"), "interlink publication PR drift")
    require(interlink_result["merge_sha"] == "5aaa0b6f1b343789a2d8618c6ba5ac0bedaf9a9e", "interlink merge SHA drift")
    require(interlink_result["pages_workflow_run_id"] == 33176302160, "interlink Pages run drift")
    interlink_readback = interlink_result["live_readback"]
    require(interlink_readback["status"] == "PASS_26_OF_26_HTTP_200_EXACT_REPOSITORY_BYTES", "interlink live-readback result drift")
    require(len(interlink_readback["sha256"]) == 26, "interlink exact-byte denominator must remain 26")
    require("both featured evidence images" in interlink_result["post_merge_monitor_followup"]["hardening"], "image-ready monitor hardening missing")
    require("current 214/94/74/10/18/18" in interlink_result["unitary_control_plane_followup"]["hardening"], "current registry monitor hardening missing")
    require("last_live_verified_counts" in interlink_result["unitary_control_plane_followup"]["hardening"], "historical registry boundary missing")
    final_monitor = interlink_result["final_closeout_monitor_followup"]
    require(final_monitor["pull_request_conclusion"] == "success", "final monitor PR evidence drift")
    require("immediately after its selected" in final_monitor["monitor_separation"], "source-funds anchor boundary missing")
    require("dedicated five-actor workflow alone" in final_monitor["monitor_separation"], "five-actor monitor separation missing")
    governance = interlink_manifest["governance_closeout"]
    require(governance["pull_request"].endswith("/1150"), "interlink governance PR drift")
    require(governance["pull_request_checks"] == "PASS_18_OF_18", "interlink governance check denominator drift")
    require(governance["merge_sha"] == "b533dbfd6c4883885957b8dedee8fe8a1e1feb4e", "interlink governance merge SHA drift")
    require(governance["pages_workflow_run_id"] == 33177638207, "interlink governance Pages run drift")
    require(governance["public_edge_readback"]["status"] == "PASS_29_OF_29_HTTP_200_EXACT_REPOSITORY_BYTES", "interlink governance readback drift")
    require(all(interlink_manifest["external_actions"][key] is True for key in ("push", "pull_request", "merge", "deployment", "live_readback")), "interlink publication action closeout incomplete")
    require(interlink_manifest["external_actions"]["filing_or_contact"] is False, "interlink filing/contact boundary drift")

    bilingual_pages = {
        ROOT / "es/toma-control-sun-park-7-junio-2018/index.html": [
            "post7-2022-omnidirectional-map-20260828.css",
            "mapa-omnidireccional-4feb2022",
            "¿Activos «protegidos por el juzgado»?",
            "«Mobbing hotelero»",
            "prueba-exclusion-deliberada",
            "reenvio-acta-thompson",
            "imagen-cuatro-hermanos-acosta-matos",
            "Gerardo Zacarías Acosta Matos</strong><br><small><code>PD-SP-P-0094</code> · identidad confirmada en CAEPR",
            "Prompt forense reproducible",
        ],
        ROOT / "en/sun-park-takeover-7-june-2018/index.html": [
            "post7-2022-omnidirectional-map-20260828.css",
            "omnidirectional-4feb2022-map",
            "Were the assets “court-protected”?",
            "“Hotel mobbing”",
            "deliberate-exclusion-proof",
            "thompson-acta-relay",
            "acosta-matos-four-sibling-image",
            "Gerardo Zacarías Acosta Matos</strong><br><small><code>PD-SP-P-0094</code> · CAEPR-confirmed identity",
            "Reproducible forensic prompt",
        ],
        ROOT / "es/comunidad-instrumentalizacion/sala-documental-actas/2022-02-04/index.html": [
            "post7-2022-omnidirectional-map-20260828.css",
            "mapa-omnidireccional-4feb2022",
            "¿Activos «protegidos por el juzgado»?",
            "Lo que el ACTA sí demuestra",
            "Ruta de conocimiento corregida",
            "Paquete capaz de demostrar intención",
            "Gerardo Zacarías Acosta Matos^",
        ],
        ROOT / "en/community-instrumentalisation/acta-document-room/2022-02-04/index.html": [
            "post7-2022-omnidirectional-map-20260828.css",
            "omnidirectional-4feb2022-map",
            "Were the assets “court-protected”?",
            "What the ACTA does prove",
            "Corrected knowledge route",
            "Package capable of proving intent",
            "Gerardo Zacarías Acosta Matos^",
        ],
    }
    for path, markers in bilingual_pages.items():
        require_markers(path, markers)

    require_markers(ROOT / "es/index.html", ["Javier Acosta Matos (joven del extremo izquierdo)", "Gerardo Zacarías Acosta Matos (hombre barbado del extremo derecho)"])
    require_markers(ROOT / "en/index.html", ["Javier Acosta Matos (the younger person at far left)", "Gerardo Zacarías Acosta Matos (the bearded person at far right)"])
    require_markers(ROOT / "en/sun-park-owner-register/index.html", ["Gil separately identifies Thompson 708 / property 8,557 as a further attributed lead"])
    require_markers(ROOT / "es/registro-propietarios-sun-park/index.html", ["Gil identifica separadamente Thompson 708 / finca 8.557 como otra pista atribuida"])

    print("POST-7-JUNE / 4-FEB-2022 DELIBERATE-EXCLUSION CONTROL: PASS")
    print(" - unitary proof sequence: 7 stages")
    print(" - combined CAEPR scope: 6/6; meeting 3/3; image siblings 4/4")
    print(" - additive identity control: upstream P-0088–P-0091 preserved; Vera P-0092 / Javier P-0093 / Gerardo P-0094")
    print(" - image SHA-256 and attributed left-to-right order verified")
    print(" - bilingual takeover and ACTA surfaces verified")
    print(" - corrected Thompson post-meeting relay and 2016 event-specific pattern control verified")
    print(" - omnidirectional 4-in / 6-stage / 4-out visual and terminology controls verified")
    print(" - reciprocal route junction: 4 core pages × 12 destinations; 18 satellite pages × 2 core backlinks")
    print(" - preliminary 2016-2022 notice/knowledge matrix: 8 controlled events")
    print(" - native invitation/service/forwarding, complete attendance and actor-specific intent remain open")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
