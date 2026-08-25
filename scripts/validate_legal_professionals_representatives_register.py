#!/usr/bin/env python3
"""Validate the controlled legal-professionals and representatives master census."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "assets" / "data"

INDEX = DATA / "legal-professionals-representatives-register-v1.json"
PEOPLE = DATA / "legal-professionals-representatives-register-v1.people.json"
ORGS = DATA / "legal-professionals-representatives-register-v1.organisations.json"
MATTER_PEOPLE = DATA / "matter-identity-registry-v1.people.json"
MATTER_ORGS = DATA / "matter-identity-registry-v1.organisations.json"
CENSUS_MD = ROOT / "archive" / "LEGAL_PROFESSIONALS_REPRESENTATIVES_MASTER_CENSUS_25AUG2026.md"
AUTHORITY_MD = ROOT / ".github" / "governance" / "records" / "FULLEST_LEGAL_PROFESSIONAL_LIST_AUTHORITY_20260825.md"
START_GATE = ROOT / "PERSON_PERIMETER_START_HERE.md"

REGISTER_SCHEMA = "por-derecho.legal-professionals-representatives-master-register.v1"
PART_SCHEMA = "por-derecho.legal-professionals-representatives-master-register.part.v1"
REGISTER_ID = "PD-SP-PROF-REG-001"
AUTHORITY_ID = "GIL-DIRECT-20260825-FULLEST-PROFESSIONAL-LIST"

PERSON_ID = re.compile(r"^PD-SP-PROF-P-\d{4}$")
ORG_ID = re.compile(r"^PD-SP-PROF-O-\d{4}$")
MATTER_PERSON_ID = re.compile(r"^PD-SP-P-\d{4}$")
MATTER_ORG_ID = re.compile(r"^PD-SP-O-\d{4}$")

ALLOWED_KINDS = {
    "LAWYER",
    "PROCURADOR",
    "FIRM_CONTACT",
    "LEGAL_PROFESSIONAL_CANDIDATE",
    "LEGAL_PROFESSIONAL_OR_CONTACT",
    "PROPOSAL_CONTACT",
}
ALLOWED_RELATIONSHIPS = {
    "OUR_CURRENT_PROFESSIONAL",
    "OUR_FORMER_PROFESSIONAL",
    "ADVERSE_PARTY_PROFESSIONAL",
    "UNRESOLVED_PRIVATE_CANDIDATE",
}
PROHIBITED_RELATIONSHIPS = {
    "OUR_CORE",
    "OUR_REPRESENTED_INTEREST",
    "ADVERSE_FORMAL_PARTY",
    "ADVERSE_PRIVATE_FUNCTIONAL_ACTOR",
}
ALLOWED_CENSUS_STATES = {
    "INCLUDED_CONFIRMED",
    "INCLUDED_CONFIRMED_CORRECTION",
    "INCLUDED_WITH_LIMITS",
    "PRIVATE_REVIEW_CANDIDATE",
    "INCLUDED_ROLE_LIMITED",
    "INCLUDED_PROPOSAL_ONLY",
}
ALLOWED_PROFILE_STATES = {
    "PENDING_PERSON_SPECIFIC_AUTHORIZATION",
    "LEGACY_PUBLIC_ENTRY_UNDER_AUTHORIZATION_REVIEW",
    "NOT_AUTHORIZED_FOR_PUBLIC_PROFILE",
}
PUBLICATION_STATE = "AUTHORIZED_FOR_MASTER_CENSUS_ONLY"

REQUIRED_PEOPLE = {
    "Javier Sixto-Seijas",
    "Estefanía Sixto Seijas",
    "Carlos Llamas Sanz",
    "Adriana Hernández Díaz",
    "María Díaz Vecino",
    "María del Pilar García Coello",
    "Miguel Méndez Itarte",
    "José María Martínez de Artola",
    "Víctor de la Torre García",
    "Zulay Carmen Rodríguez Cabrera",
    "Pedro Campaña Ávila",
    "Mónica Lasquibar Rodríguez",
    "Rosa Gual Tomás",
    "Iñigo Jorge de Luisa Maiz",
    "Adriana González García",
    "Pablo Villaseca Rico",
    "Luis Álvarez de la Vega Gaztelu",
    "Cristóbal Cotta",
    "Cristo Ayose Suárez Pimentel",
    "Juan Tomás Parrilla Suárez",
    "Armando Betancor Álamo",
    "José María Betancor Álamo",
    "Davinia Sánchez de la Cruz",
    "Joaquín Ruiz de Infante Abella",
    "Daniel Jiménez García",
    "Almudena Santafé Blecua",
    "Luis Miguel López Gómez",
    "Manuel Gallego Águeda",
    "Bernardino “Bernard” Afonso",
    "Jordi Albiol",
    "Tania Alejandra Domínguez Limiñana",
    "Manuela Cabrera de la Cruz",
    "Francisco Javier Pérez Almeida",
}
REQUIRED_PROCURADORES = {
    "Adriana Hernández Díaz",
    "María Díaz Vecino",
    "María del Pilar García Coello",
    "Tania Alejandra Domínguez Limiñana",
    "Manuela Cabrera de la Cruz",
    "Francisco Javier Pérez Almeida",
}
REQUIRED_ORGS = {
    "Sixto Abogados",
    "J&A Garrigues, S.L.P.",
    "Cuatrecasas, Gonçalves Pereira, S.L.P.",
    "Pimentel Servicios Legales",
    "Alas Legal Advisors, S.L.",
    "Devina — later professional continuity candidate",
    "Bufete Ruiz de Infante",
    "SLJ Abogados",
    "López Castelo Abogados",
    "Gallego Abogados",
    "DWF-RCD / Rousaud Costas Duran professional perimeter",
    "Tenerife Procuradores",
    "Cases & Lacambra",
    "ONTIER",
    "APM Law",
}

CONTACT_PATTERNS = [
    re.compile(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}"),
    re.compile(r"https?://(?:mail\.google|drive\.google|outlook|dropbox)", re.I),
    re.compile(r"\b(?:message-id|thread-id|gmail-id|native locator)\b", re.I),
]
PHONE_CANDIDATE = re.compile(r"(?<![\w])\+?\d[\d .()/-]{7,}\d(?![\w])")


def load(path: Path) -> dict[str, Any]:
    try:
        obj = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise AssertionError(f"cannot parse {path.relative_to(ROOT)}: {exc}") from exc
    require(isinstance(obj, dict), f"{path.relative_to(ROOT)} root must be object")
    return obj


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def no_private_locator(value: Any, context: str) -> None:
    text = json.dumps(value, ensure_ascii=False)
    for pattern in CONTACT_PATTERNS:
        require(not pattern.search(text), f"private/contact locator pattern in {context}: {pattern.pattern}")
    for match in PHONE_CANDIDATE.finditer(text):
        candidate = match.group()
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", candidate):
            continue
        if len(re.sub(r"\D", "", candidate)) >= 10:
            raise AssertionError(f"possible telephone number in {context}")


def main() -> int:
    try:
        index = load(INDEX)
        people_part = load(PEOPLE)
        org_part = load(ORGS)
        matter_people = load(MATTER_PEOPLE)
        matter_orgs = load(MATTER_ORGS)

        require(index.get("schema") == REGISTER_SCHEMA, "unexpected register schema")
        require(index.get("register_id") == REGISTER_ID, "unexpected register ID")
        require(index.get("control_date") == "2026-08-25", "unexpected control date")
        require(index.get("authority_reference") == AUTHORITY_ID, "authority reference missing")
        require(re.fullmatch(r"[0-9a-f]{40}", str(index.get("source_main_sha", ""))) is not None, "source main SHA invalid")
        require(index.get("governance", {}).get("perimeter_policy_id") == "PD-PERIMETER-GOV-001", "perimeter policy link missing")
        require(index.get("governance", {}).get("public_profile_decisions") == "PENDING_PERSON_SPECIFIC_AUTHORIZATION", "public-profile gate missing")
        no_private_locator(index, "index")

        for part, kind, path in [
            (people_part, "PERSON", PEOPLE),
            (org_part, "ORGANISATION", ORGS),
        ]:
            require(part.get("schema") == PART_SCHEMA, f"unexpected part schema: {path.name}")
            require(part.get("register_id") == REGISTER_ID, f"register ID mismatch: {path.name}")
            require(part.get("type") == kind, f"part type mismatch: {path.name}")
            require(isinstance(part.get("records"), list), f"records not array: {path.name}")

        descriptors = index.get("parts")
        require(isinstance(descriptors, list) and len(descriptors) == 2, "index must declare two parts")
        descriptor_by_type = {item.get("type"): item for item in descriptors if isinstance(item, dict)}
        require(descriptor_by_type["PERSON"].get("count") == len(people_part["records"]), "person part count mismatch")
        require(descriptor_by_type["ORGANISATION"].get("count") == len(org_part["records"]), "organisation part count mismatch")

        matter_person_ids = {item.get("id") for item in matter_people.get("records", [])}
        matter_org_ids = {item.get("id") for item in matter_orgs.get("records", [])}

        people_ids: set[str] = set()
        people_names: set[str] = set()
        procuradores: set[str] = set()
        org_refs: set[str] = set()

        for record in people_part["records"]:
            require(isinstance(record, dict), "person record must be object")
            pid = record.get("professional_record_id")
            name = record.get("name")
            require(isinstance(pid, str) and PERSON_ID.fullmatch(pid), f"invalid professional person ID: {pid!r}")
            require(pid not in people_ids, f"duplicate professional person ID: {pid}")
            people_ids.add(pid)
            require(isinstance(name, str) and name.strip(), f"missing person name: {pid}")
            require(name not in people_names, f"duplicate professional person name: {name}")
            people_names.add(name)

            require(record.get("professional_kind") in ALLOWED_KINDS, f"invalid professional kind: {pid}")
            relationship = record.get("relationship_classification")
            require(relationship in ALLOWED_RELATIONSHIPS, f"invalid relationship classification: {pid}")
            require(relationship not in PROHIBITED_RELATIONSHIPS, f"principal-perimeter classification forbidden: {pid}")
            require(record.get("census_inclusion_status") in ALLOWED_CENSUS_STATES, f"invalid census status: {pid}")
            require(record.get("public_profile_status") in ALLOWED_PROFILE_STATES, f"invalid profile status: {pid}")
            require(record.get("census_name_publication_status") == PUBLICATION_STATE, f"census authority missing: {pid}")

            aliases = record.get("name_variants")
            require(isinstance(aliases, list) and all(isinstance(item, str) and item.strip() for item in aliases), f"invalid variants: {pid}")
            firms = record.get("firm_ids")
            require(isinstance(firms, list) and all(isinstance(item, str) and ORG_ID.fullmatch(item) for item in firms), f"invalid firm refs: {pid}")
            org_refs.update(firms)

            registry_id = record.get("registry_id")
            if registry_id is not None:
                require(isinstance(registry_id, str) and MATTER_PERSON_ID.fullmatch(registry_id), f"invalid matter person ID: {pid}")
                require(registry_id in matter_person_ids, f"unknown matter person ID: {pid} -> {registry_id}")

            if record.get("professional_kind") == "PROCURADOR":
                procuradores.add(name)

            if record.get("track") in {"PROPOSAL_OR_CONSULTATION_ONLY", "ROLE_LIMITED_FIRM_CONTACT", "REVIEW_CANDIDATE", "PROFESSIONAL_ADVISER_REVIEW"}:
                require(record.get("evidence_status") not in {"CONFIRMED_SUBSTANTIVE", "CONFIRMED_CURRENT"}, f"limited/candidate record overstated: {pid}")

            require(isinstance(record.get("limits"), str) and record["limits"].strip(), f"missing limits: {pid}")
            require(isinstance(record.get("source_basis_public_safe"), str) and record["source_basis_public_safe"].strip(), f"missing source basis: {pid}")
            no_private_locator(record, pid)

        org_ids: set[str] = set()
        org_names: set[str] = set()
        for record in org_part["records"]:
            require(isinstance(record, dict), "organisation record must be object")
            oid = record.get("professional_organisation_id")
            name = record.get("name")
            require(isinstance(oid, str) and ORG_ID.fullmatch(oid), f"invalid professional organisation ID: {oid!r}")
            require(oid not in org_ids, f"duplicate professional organisation ID: {oid}")
            org_ids.add(oid)
            require(isinstance(name, str) and name.strip(), f"missing organisation name: {oid}")
            require(name not in org_names, f"duplicate professional organisation name: {name}")
            org_names.add(name)
            registry_id = record.get("registry_id")
            if registry_id is not None:
                require(isinstance(registry_id, str) and MATTER_ORG_ID.fullmatch(registry_id), f"invalid matter organisation ID: {oid}")
                require(registry_id in matter_org_ids, f"unknown matter organisation ID: {oid} -> {registry_id}")
            require(record.get("census_name_publication_status") == PUBLICATION_STATE, f"census authority missing: {oid}")
            require(isinstance(record.get("limits"), str) and record["limits"].strip(), f"missing organisation limits: {oid}")
            no_private_locator(record, oid)

        require(org_refs <= org_ids, f"unknown firm references: {sorted(org_refs - org_ids)}")
        require(REQUIRED_PEOPLE <= people_names, f"required professional people missing: {sorted(REQUIRED_PEOPLE - people_names)}")
        require(REQUIRED_PROCURADORES == procuradores, f"procurador set mismatch: expected {sorted(REQUIRED_PROCURADORES)}, got {sorted(procuradores)}")
        require(REQUIRED_ORGS <= org_names, f"required firms/practices missing: {sorted(REQUIRED_ORGS - org_names)}")

        adriana = next(item for item in people_part["records"] if item["name"] == "Adriana Hernández Díaz")
        require(adriana["professional_kind"] == "PROCURADOR", "Adriana Hernández Díaz must be procuradora")
        require("called her counsel" in adriana["limits"].lower() or "correction" in adriana["census_inclusion_status"].lower(), "Adriana correction limit missing")

        maria = next(item for item in people_part["records"] if item["name"] == "María Díaz Vecino")
        require({"María Luisa Díaz Vecino", "María Vecino Díaz"} <= set(maria["name_variants"]), "María Díaz Vecino variants incomplete")
        require("not yet personada" in maria["limits"], "María Díaz Vecino personation limit missing")

        perez = next(item for item in people_part["records"] if item["name"] == "Francisco Javier Pérez Almeida")
        require(perez.get("registry_id") == "PD-SP-P-0056", "Francisco Javier Pérez matter ID not preserved")
        require("Francisco Javier Pérez Alemán-Almeida" in perez.get("name_variants", []), "Francisco Javier Pérez source variant missing")

        counts = index.get("counts", {})
        require(counts.get("people_total") == len(people_ids), "index people_total mismatch")
        require(counts.get("organisations_total") == len(org_ids), "index organisations_total mismatch")
        require(counts.get("procuradores_total") == len(procuradores), "index procurador count mismatch")
        require(counts.get("people_with_matter_registry_id") == sum(bool(item.get("registry_id")) for item in people_part["records"]), "person registry-link count mismatch")
        require(counts.get("organisations_with_matter_registry_id") == sum(bool(item.get("registry_id")) for item in org_part["records"]), "organisation registry-link count mismatch")

        for path, markers in {
            CENSUS_MD: [REGISTER_ID, AUTHORITY_ID, "Adriana Hernández Díaz", "María Díaz Vecino", "Francisco Javier Pérez Almeida"],
            AUTHORITY_MD: [AUTHORITY_ID, REGISTER_ID, "update the fullest list"],
            START_GATE: [REGISTER_ID, "legal-professionals-representatives-register-v1.people.json", "Professional completeness gate"],
        }.items():
            require(path.is_file(), f"missing controlled file: {path.relative_to(ROOT)}")
            text = path.read_text(encoding="utf-8")
            for marker in markers:
                require(marker in text, f"missing marker {marker!r} in {path.relative_to(ROOT)}")
            no_private_locator(text, str(path.relative_to(ROOT)))

    except AssertionError as exc:
        print(f"LEGAL PROFESSIONALS REGISTER: FAIL\n - {exc}", file=sys.stderr)
        return 1

    print("LEGAL PROFESSIONALS REGISTER: PASS")
    print(f" - people: {len(people_ids)}")
    print(f" - organisations: {len(org_ids)}")
    print(f" - procuradores/as: {len(procuradores)}")
    print(f" - matter-person links: {sum(bool(item.get('registry_id')) for item in people_part['records'])}")
    print(f" - matter-organisation links: {sum(bool(item.get('registry_id')) for item in org_part['records'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
