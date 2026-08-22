from html.parser import HTMLParser
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class StrictHTMLParser(HTMLParser):
    """Parse each controlled public page and fail on malformed entity references."""


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


required = {
    "AGENTS.md": [
        "ND-COM-CRIM-001",
        "mandatory non-derogation rule",
        "Do not publish the guilt",
        "5 January 2022",
    ],
    "CHATGPT_START_HERE.md": [
        "ND-COM-CRIM-001",
        "criminal instrumentalisation",
        "5 January 2022",
    ],
    "archive/SUN_PARK_COMMUNITY_CRIMINAL_INSTRUMENTALISATION_NON_DEROGATION_CONTROL_21AUG2026.md": [
        "Controlling thesis",
        "later adoption and culmination",
        "20.993%",
        "28 January 2022",
        "29 March 2022",
        "31 March 2022",
        "self-ratify",
        "Article 262 Criminal Code",
        "Article 262 LECrim",
    ],
    "COMMUNITY_ACTAS_TWO_TRACK_AUDIT.md": [
        "Criminal non-derogation",
        "later adoption/culmination",
        "20.993%",
    ],
    "TWO_COMPETING_GOVERNANCE_RECORDS_2008_2022.md": [
        "Express criminal attribution",
        "attribution of that criminal case thesis to Por Derecho",
        "conclusion**. Whether the mechanism occurred as alleged",
        "later adoption/culmination and documentary-conversion phase",
    ],
    "THREAD_DELETION_AUDIT_2026-08-19_COMMUNITY_ACTAS.md": [
        "later adoption/culmination and documentary-conversion phase",
        "criminal-instrumentalisation attribution as a mandatory repository proposition",
        "ND-COM-CRIM-001",
    ],
    "archive/CORRECTION_REGISTER_COMMUNITY_ACTAS_ADDENDUM_17AUG2026.md": [
        "CR-COM-008",
        "CR-COM-013",
        "CP art. 262",
    ],
    "archive/MISSING_EVIDENCE_REGISTER_COMMUNITY_ACTAS_ADDENDUM_17AUG2026.md": [
        "ME-COM-013",
        "ME-COM-014",
        "ME-COM-015",
    ],
    "archive/CONTINUOUS_MAINTENANCE_MATRIX.md": [
        "Sun Park Community / ACTA criminal instrumentalisation",
        "No 5-Jan JDAM project signature is asserted",
    ],
    "es/comunidad-instrumentalizacion/index.html": [
        "Atribución penal expresa de Por Derecho",
        "instrumentalización penal",
    ],
    "en/community-instrumentalisation/index.html": [
        "Por Derecho's express criminal attribution",
        "criminal instrumentalisation",
    ],
    "es/comunidad-instrumentalizacion/actas-2011-2022/index.html": [
        "Copia escaneada localizada",
        "20,993%",
        "28 enero",
        "29 marzo",
        "31 marzo",
    ],
    "en/community-instrumentalisation/minutes-2011-2022/index.html": [
        "Located scanned copy",
        "20.993%",
        "28 January",
        "29 March",
        "31 March",
    ],
    "es/comunidad-instrumentalizacion/dos-registros-gobernanza-competidores/index.html": [
        "instrumentalización penal",
        "<h2>Adopción y culminación</h2>",
        "20,993%",
    ],
    "en/community-instrumentalisation/two-competing-governance-records/index.html": [
        "criminal instrumentalisation",
        "<h2>Adoption and culmination</h2>",
        "20.993%",
    ],
    "es/arquitectura-nodo-documental-jdam/index.html": [
        "nodo de conversión penal",
        "20,993%",
        "No se afirmará que JDAM firmó el proyecto el 5 enero de 2022",
    ],
    "en/architecture-documentary-node-jdam/index.html": [
        "criminal conversion node",
        "20.993%",
        "will not state that JDAM signed the project on 5 January 2022",
    ],
}

for rel, needles in required.items():
    content = read(rel)
    for needle in needles:
        assert needle in content, f"{needle!r} missing from {rel}"


html_files = [rel for rel in required if rel.endswith(".html")]
for rel in html_files:
    StrictHTMLParser(convert_charrefs=False).feed(read(rel))


legacy_ui_markers = [
    "<h2>Fase sucesora</h2>",
    "<h2>Successor phase</h2>",
    "<span>2022+ · nueva etapa</span>",
    "<span>2022+ · separate epoch</span>",
]
for rel in [
    rel
    for rel in html_files
    if "architecture-documentary-node" not in rel
    and "arquitectura-nodo-documental" not in rel
]:
    content = read(rel)
    for marker in legacy_ui_markers:
        assert marker not in content, f"legacy neutral-period marker {marker!r} remains in {rel}"


unsafe_public_claims = [
    "JDAM firmó el proyecto el 5 de enero de 2022",
    "JDAM signed the project on 5 January 2022",
]
for rel in [
    rel
    for rel in html_files
    if "architecture-documentary-node" not in rel
    and "arquitectura-nodo-documental" not in rel
]:
    content = read(rel)
    for claim in unsafe_public_claims:
        assert claim not in content, f"unsupported project-signature claim remains in {rel}"


with (ROOT / "assets/data/community-criminal-instrumentalisation-v1.json").open(
    encoding="utf-8"
) as handle:
    control = json.load(handle)

assert control["control_id"] == "ND-COM-CRIM-001"
assert control["thesis"]["attribution_is_absolute"] is True
assert control["thesis"]["adjudicated_guilt"] is False
assert control["thesis"]["actor_specific_proof_required"] is True
assert control["acta_2022_copy"]["attendance_stated_percent"] == 20.993
assert control["acta_2022_copy"]["budget_annex"]["date_stated"] == "2022-01-28"
assert control["acta_2022_copy"]["budget_annex"]["signature_identity_authenticated"] is False
assert control["project_control"]["self_ratification_rejected"] is True
assert control["article_262_control"]["must_not_conflate"] is True
assert control["follow_up"]["broad_repeat_email_recommended"] is False
assert control["follow_up"]["focused_evidence_supplement_recommended"] is True


with (ROOT / "assets/data/jdam-architecture-documentary-node-v1.json").open(
    encoding="utf-8"
) as handle:
    jdam = json.load(handle)

assert jdam["public_boundary"]["not_a_finding"] is True
assert jdam["control_date"] == "2026-08-21"
assert jdam["public_boundary"]["criminal_thesis_must_not_be_neutralised"] is True
assert jdam["community_acta_2022_copy"]["attendance_stated_percent"] == 20.993
assert "do not state a 5 January 2022" in jdam["community_acta_2022_copy"][
    "date_control"
]

print("Community criminal-instrumentalisation non-derogation validation passed")
