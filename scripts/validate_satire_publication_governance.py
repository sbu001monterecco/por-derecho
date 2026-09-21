#!/usr/bin/env python3
"""Fail-closed validation for public satire/caricature/spoof surfaces.

The validator is intentionally specialist and path-gated in CI. It verifies the
machine governance contract, the finite public-surface register, disclosures,
name-display decisions, dated affiliations and opposing-counsel risk preflight.
It does not decide whether an allegation is true or provide legal clearance.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

DEFAULT_ROOT = Path(__file__).resolve().parents[1]
GOVERNANCE_PATH = Path("ops/SATIRE_CARICATURE_SPOOF_GOVERNANCE_V1.json")
HUMAN_STANDARD_PATH = Path(
    ".github/governance/SATIRE_CARICATURE_SPOOF_PUBLICATION_STANDARD_ES_EN.md"
)
COMPLIANCE_PATH = Path("data/satire-publication-compliance-v1.json")
DIGITAL_REGISTER_PATH = Path("data/digital-media-asset-register-v1.json")
PEOPLE_PATH = Path("assets/data/matter-identity-registry-v1.people.json")

DISCLOSURES = {
    "CARICATURA / REPRESENTACIÓN SATÍRICA — NO ES UN ANUNCIO REAL",
    "ANUNCIO SATÍRICO — PARODIA Y CARICATURA. NO ES PUBLICIDAD REAL",
    "ANUNCIO SATÍRICO — PARODIA Y CARICATURA. NO ES PUBLICIDAD REAL NI UNA COMUNICACIÓN DE LAS ENTIDADES REPRESENTADAS.",
    "SATIRICAL / CARICATURE REPRESENTATION — NOT A REAL ADVERTISEMENT",
    "SATIRICAL ADVERTISEMENT — PARODY AND CARICATURE. NOT REAL ADVERTISING AND NOT A COMMUNICATION FROM THE ENTITIES DEPICTED.",
}

DISCOVERY_MARKERS = (
    "CARICATURA / REPRESENTACIÓN SATÍRICA",
    "ANUNCIO SATÍRICO — PARODIA Y CARICATURA",
    "SATIRICAL / CARICATURE REPRESENTATION",
    "SATIRICAL ADVERTISEMENT — PARODY AND CARICATURE",
)

PUBLIC_ROOTS = ("es", "en", "de", "assets/media")
PUBLIC_SUFFIXES = {".html", ".svg"}
RISK_KEYS = {
    "HONOUR_REPUTATION_PROFESSIONAL_PRESTIGE",
    "FALSE_ENDORSEMENT_AUTHORSHIP_QUOTATION_MANDATE_OR_ROLE",
    "IMAGE_LIKENESS_PERSONALITY_RIGHTS",
    "IMPLIED_DISHONESTY_CONFLICT_CORRUPTION_ILLEGALITY_OR_CRIMINALITY",
    "LOGO_TRADE_DRESS_OR_REAL_ADVERTISING_CONFUSION",
    "PERSONAL_DATA_NECESSITY_AND_PROPORTIONALITY",
    "CORRECTION_REPLY_TAKEDOWN_AND_NARROW_REVERT_PATH",
}

FULL_FORMS = {
    "FULL_CANONICAL_CARET_CONFIRMED",
    "FULL_NAME_STRONGLY_VERIFIED_EXCEPTION",
}
PENDING_FORMS = {
    "EXACT_SOURCE_SHORT_FORM",
    "SURNAME_PLUS_SOURCED_ROLE",
    "ENTITY_PLUS_ROLE",
    "NEUTRAL_DESCRIPTOR",
    "WITHHOLD_IDENTITY",
}
AFFILIATION_STATES = {
    "HISTORICAL_DATED",
    "CURRENT_VERIFIED_ON_DATE",
    "SOURCE_LITERAL",
    "DISPUTED_OR_CONFLICTING",
    "OPEN",
    "NOT_APPLICABLE",
}


def load_json(root: Path, relative: Path) -> dict[str, Any]:
    path = root / relative
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ValueError(f"Missing required file: {relative.as_posix()}") from None
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {relative.as_posix()}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"Expected JSON object in {relative.as_posix()}")
    return value


def nonempty_strings(value: Any) -> bool:
    return isinstance(value, list) and bool(value) and all(
        isinstance(item, str) and item.strip() for item in value
    )


def validate_named_person(
    person: Any,
    canonical_people: dict[str, str],
    context: str,
) -> list[str]:
    errors: list[str] = []
    if not isinstance(person, dict):
        return [f"{context}: named-person entry must be an object."]

    display = person.get("display_name")
    naming_form = person.get("naming_form")
    identity_state = person.get("identity_state")
    caepr_id = person.get("caepr_id")
    source_refs = person.get("source_refs")
    factual_role = person.get("factual_role")
    affiliation = person.get("affiliation")
    satirical_function = person.get("satirical_function")

    if not isinstance(display, str) or not display.strip():
        errors.append(f"{context}: display_name is required.")
    if not nonempty_strings(source_refs):
        errors.append(f"{context}: source_refs must be a non-empty string list.")
    if not isinstance(factual_role, dict):
        errors.append(f"{context}: factual_role object is required.")
    else:
        if not isinstance(factual_role.get("label"), str) or not factual_role["label"].strip():
            errors.append(f"{context}: factual_role.label is required.")
        if not isinstance(factual_role.get("date_or_period"), str) or not factual_role[
            "date_or_period"
        ].strip():
            errors.append(f"{context}: factual_role.date_or_period is required.")
        if not nonempty_strings(factual_role.get("source_refs")):
            errors.append(f"{context}: factual_role.source_refs is required.")
    if not isinstance(satirical_function, dict) or satirical_function.get("state") not in {
        "NONE",
        "QUESTION",
        "QUOTED_SHORTHAND",
        "METAPHOR",
        "ANALYTICAL_LENS",
    }:
        errors.append(f"{context}: satirical_function must declare a controlled state.")

    if naming_form == "FULL_CANONICAL_CARET_CONFIRMED":
        if identity_state != "CARET_CONFIRMED":
            errors.append(f"{context}: full canonical name requires CARET_CONFIRMED.")
        if not isinstance(caepr_id, str) or canonical_people.get(caepr_id) != display:
            errors.append(
                f"{context}: full canonical name must exactly match its immutable CAEPR person ID."
            )
    elif naming_form == "FULL_NAME_STRONGLY_VERIFIED_EXCEPTION":
        if identity_state != "STRONGLY_VERIFIED_EXCEPTION":
            errors.append(f"{context}: strong full-name exception requires its matching state.")
        if caepr_id not in {None, ""}:
            errors.append(f"{context}: strong exception must not create or borrow a CAEPR ID.")
        if not nonempty_strings(person.get("direct_public_sources")):
            errors.append(f"{context}: strong exception requires direct_public_sources.")
        necessity = person.get("full_name_necessity")
        if not isinstance(necessity, str) or len(necessity.strip()) < 20:
            errors.append(f"{context}: strong exception requires a specific necessity rationale.")
        if person.get("no_resolved_caepr_record_available") is not True:
            errors.append(f"{context}: strong exception must confirm no resolved CAEPR record.")
    elif naming_form in PENDING_FORMS:
        if identity_state not in {"CARET_PENDING", "OPEN_OR_UNVERIFIED"}:
            errors.append(f"{context}: neutral/withheld form requires a pending or open state.")
        if caepr_id not in {None, ""}:
            errors.append(f"{context}: pending/open identity must not carry a CAEPR person ID.")
        if isinstance(display, str) and display in canonical_people.values():
            errors.append(
                f"{context}: a known full canonical name cannot be presented through a pending form."
            )
    else:
        errors.append(f"{context}: unsupported naming_form {naming_form!r}.")

    if not isinstance(affiliation, dict):
        errors.append(f"{context}: affiliation object is required.")
    else:
        affiliation_state = affiliation.get("state")
        if affiliation_state not in AFFILIATION_STATES:
            errors.append(f"{context}: unsupported affiliation state {affiliation_state!r}.")
        if affiliation_state == "CURRENT_VERIFIED_ON_DATE":
            if not isinstance(affiliation.get("verified_on"), str) or not affiliation[
                "verified_on"
            ].strip():
                errors.append(f"{context}: current affiliation requires verified_on.")
            if not nonempty_strings(affiliation.get("source_refs")):
                errors.append(f"{context}: current affiliation requires dated source_refs.")
        if affiliation_state == "HISTORICAL_DATED" and not isinstance(
            affiliation.get("date_or_period"), str
        ):
            errors.append(f"{context}: historical affiliation requires date_or_period.")

    return errors


def discover_public_satire_surfaces(root: Path) -> set[str]:
    discovered: set[str] = set()
    for public_root in PUBLIC_ROOTS:
        base = root / public_root
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in PUBLIC_SUFFIXES:
                continue
            try:
                content = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            if any(marker in content for marker in DISCOVERY_MARKERS):
                discovered.add(path.relative_to(root).as_posix())
    return discovered


def validate(root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        governance = load_json(root, GOVERNANCE_PATH)
        compliance = load_json(root, COMPLIANCE_PATH)
        digital = load_json(root, DIGITAL_REGISTER_PATH)
        people = load_json(root, PEOPLE_PATH)
    except ValueError as exc:
        return [str(exc)], warnings

    if governance.get("status") != "ACTIVE_REPOSITORY_GOVERNANCE":
        errors.append("Satire machine governance must be ACTIVE_REPOSITORY_GOVERNANCE.")
    enforcement = governance.get("machine_enforcement")
    if not isinstance(enforcement, dict) or enforcement.get("mode") != (
        "FAIL_CLOSED_FOR_REGISTERED_AND_NEW_PUBLIC_SATIRE_SURFACES"
    ):
        errors.append("Machine governance must declare the specialist fail-closed mode.")
    if set(governance.get("opposing_counsel_risk_preflight", [])) != RISK_KEYS:
        errors.append("Machine governance risk-preflight keys do not match the canonical set.")
    policy = governance.get("person_name_display_policy")
    if not isinstance(policy, dict) or set(policy.get("precedence", [])) != {
        "FULL_CANONICAL_CARET_CONFIRMED",
        "FULL_NAME_STRONGLY_VERIFIED_EXCEPTION",
        "SHORT_SOURCE_LITERAL_OR_NEUTRAL_ROLE",
        "WITHHOLD_IDENTITY",
    }:
        errors.append("Machine governance lacks the complete name-display precedence.")

    standard_path = root / HUMAN_STANDARD_PATH
    try:
        standard = standard_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        errors.append(f"Missing human standard: {HUMAN_STANDARD_PATH.as_posix()}")
        standard = ""
    for required in (
        "Mandatory name-display hierarchy",
        "Never complete a person's name from memory",
        "An image/portrait identity lock and a CAEPR name lock are separate controls",
        "Opposing-counsel publication-risk preflight",
        "Machine enforcement and repair path",
    ):
        if required not in standard:
            errors.append(f"Human standard is missing required control text: {required!r}.")

    canonical_people: dict[str, str] = {}
    for record in people.get("records", []):
        if isinstance(record, dict) and isinstance(record.get("id"), str) and isinstance(
            record.get("name"), str
        ):
            canonical_people[record["id"]] = record["name"]

    publications = compliance.get("publications")
    if not isinstance(publications, list) or not publications:
        errors.append("Compliance register requires a non-empty publications list.")
        publications = []
    publication_ids: set[str] = set()
    registered_surfaces: set[str] = set()
    logical_to_publication: dict[str, str] = {}

    for publication in publications:
        if not isinstance(publication, dict):
            errors.append("Compliance publication entry must be an object.")
            continue
        publication_id = publication.get("publication_id")
        if not isinstance(publication_id, str) or not publication_id:
            errors.append("Compliance publication_id is required.")
            continue
        if publication_id in publication_ids:
            errors.append(f"Duplicate compliance publication_id: {publication_id}.")
        publication_ids.add(publication_id)
        context = publication_id

        logical_assets = publication.get("logical_assets")
        if not nonempty_strings(logical_assets):
            errors.append(f"{context}: logical_assets must be a non-empty string list.")
        else:
            for logical_asset in logical_assets:
                previous = logical_to_publication.get(logical_asset)
                if previous and previous != publication_id:
                    errors.append(
                        f"{context}: logical asset {logical_asset} is also assigned to {previous}."
                    )
                logical_to_publication[logical_asset] = publication_id

        surfaces = publication.get("public_surfaces")
        if not isinstance(surfaces, list) or not surfaces:
            errors.append(f"{context}: public_surfaces must be non-empty.")
            surfaces = []
        surface_texts: list[tuple[str, str]] = []
        for surface in surfaces:
            if not isinstance(surface, dict):
                errors.append(f"{context}: surface entry must be an object.")
                continue
            path_value = surface.get("path")
            disclosure = surface.get("required_disclosure")
            if not isinstance(path_value, str) or not path_value:
                errors.append(f"{context}: surface path is required.")
                continue
            if path_value in registered_surfaces:
                errors.append(f"Surface is registered more than once: {path_value}.")
            registered_surfaces.add(path_value)
            if not isinstance(disclosure, str) or not disclosure:
                errors.append(f"{context}: {path_value} requires an exact disclosure.")
                continue
            if disclosure not in DISCLOSURES:
                errors.append(f"{context}: {path_value} uses a non-canonical disclosure.")
            full_path = root / path_value
            if not full_path.is_file():
                errors.append(f"{context}: registered public surface is missing: {path_value}.")
                continue
            content = full_path.read_text(encoding="utf-8")
            surface_texts.append((path_value, content))
            if disclosure not in content:
                errors.append(f"{context}: exact disclosure missing from {path_value}.")

        named_people = publication.get("named_people")
        if not isinstance(named_people, list):
            errors.append(f"{context}: named_people must be a list, including [] when none.")
            named_people = []
        declared_names: set[str] = set()
        for index, person in enumerate(named_people):
            errors.extend(
                validate_named_person(person, canonical_people, f"{context}.named_people[{index}]")
            )
            if isinstance(person, dict) and isinstance(person.get("display_name"), str):
                declared_names.add(person["display_name"])

        for path_value, content in surface_texts:
            for canonical_name in canonical_people.values():
                if canonical_name in content and canonical_name not in declared_names:
                    errors.append(
                        f"{context}: {path_value} contains known full canonical name "
                        f"{canonical_name!r} without a named_people decision."
                    )

        if publication.get("factual_role_and_satirical_function_separated") is not True:
            errors.append(f"{context}: factual/satirical role separation must be affirmed.")
        if not nonempty_strings(publication.get("source_refs")):
            errors.append(f"{context}: source_refs must be non-empty.")
        risk = publication.get("opposing_counsel_risk_review")
        if not isinstance(risk, dict) or set(risk) != RISK_KEYS:
            errors.append(f"{context}: opposing-counsel risk review is incomplete.")
        elif any(not isinstance(value, str) or not value.strip() for value in risk.values()):
            errors.append(f"{context}: every risk-review result must be explicit.")

    discovered = discover_public_satire_surfaces(root)
    for path_value in sorted(discovered - registered_surfaces):
        errors.append(f"Unregistered public satire surface: {path_value}.")
    for path_value in sorted(registered_surfaces - discovered):
        errors.append(
            f"Registered surface lacks a canonical satire discovery marker: {path_value}."
        )

    family_ids = {
        family.get("family_id")
        for family in digital.get("families", [])
        if isinstance(family, dict) and "satire" in str(family.get("scope", "")).lower()
    }
    file_entries = {
        entry.get("reference"): entry
        for entry in digital.get("files", [])
        if isinstance(entry, dict) and isinstance(entry.get("reference"), str)
    }
    for asset in digital.get("logical_assets", []):
        if not isinstance(asset, dict) or asset.get("family_id") not in family_ids:
            continue
        reference = asset.get("reference")
        compliance_id = asset.get("satire_compliance_id")
        if compliance_id not in publication_ids:
            errors.append(f"{reference}: missing or unknown satire_compliance_id.")
        elif logical_to_publication.get(reference) != compliance_id:
            errors.append(f"{reference}: compliance register linkage is inconsistent.")
        web_file = asset.get("web_file")
        file_entry = file_entries.get(web_file)
        if not isinstance(file_entry, dict):
            errors.append(f"{reference}: web_file {web_file!r} is absent from the PD-DMA files register.")
            continue
        repository_path = file_entry.get("repository_path")
        if repository_path not in registered_surfaces:
            errors.append(
                f"{reference}: registered web surface {repository_path!r} is absent from satire compliance."
            )

    return sorted(set(errors)), sorted(set(warnings))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument(
        "--advisory",
        action="store_true",
        help="Report would-be failures but return success for shadow evaluation.",
    )
    args = parser.parse_args()
    errors, warnings = validate(args.root.resolve())
    if warnings:
        print("WARNINGS:")
        for warning in warnings:
            print(f"  - {warning}")
    if errors:
        heading = "ADVISORY FINDINGS" if args.advisory else "ERRORS"
        print(f"{heading}:")
        for error in errors:
            print(f"  - {error}")
        if args.advisory:
            print(f"Advisory satire-governance scan found {len(errors)} issue(s); exit remains 0.")
            return 0
        print(f"Satire publication governance validation failed with {len(errors)} error(s).")
        return 1
    print(
        "Satire publication governance validation passed: machine policy, disclosures, "
        "surface census, name decisions, affiliations and risk preflight are consistent."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
