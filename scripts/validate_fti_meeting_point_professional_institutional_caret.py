#!/usr/bin/env python3
"""Validate the finite FTI/Meeting Point professional-institutional caret census."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "assets/data/caepr-caret-fti-meeting-point-professional-institutional-v1.json"
CONTROL_ID = "PD-FTI-MP-PROF-INST-CARET-20260827-01"
EXPECTED_VERDICT = (
    "FINITE ROLE-SELECTED 13-SURFACE PROFESSIONAL-INSTITUTIONAL CENSUS COMPLETE; "
    "40/101 CARET_CONFIRMED; 61 CARET_PENDING; 0 CARET_SUSPENDED; "
    "PARTIAL — NOT ALL IS^"
)
EXPECTED_COUNTS = {
    "PERSON": (19, 8, 11),
    "ORGANISATION_OR_STRUCTURE": (40, 22, 18),
    "INSTITUTION_OR_SUBORGAN": (24, 7, 17),
    "PROCEEDING_OR_FILE": (18, 3, 15),
}
EXPECTED_SEPARATE = {
    "PD-FTI-MP-RICPE-CARET-20260827-01": 65,
    "PD-ALV-MP357-CARET-20260827-01": 32,
    "PD-ALV-MP357-FIRST-HOP-CARET-20260827-01": 130,
    "PD-UNITARY-REDIGEST-20260827-01": 24,
}
PAGE_RULES = {
    "S08": {
        "path": "es/fti-meeting-point-ricpe-alertador-continuidad/index.html",
        "required": (
            "31 ACCIONES CONTROLADAS · NINGUNA AUTORIZADA POR ESTA PÁGINA",
            "Censo finito de alcance seleccionado: 40 de 101 confirmados; 61 pendientes.",
            "trece superficies fuente controladas enumeradas en el censo",
            "No incluye el registro o la vista transaccional canónicos añadidos posteriormente",
            "ni pretende enumerar hotel por hotel, nuevos compradores, operadores, gestores, financiadores u otras contrapartes",
            "Los cuatro denominadores heredados y el quinto denominador ampliado de 101 objetos se mantienen separados",
            "Abrir los 101 registros — 40 confirmados / 61 pendientes →",
        ),
    },
    "S09": {
        "path": "en/fti-meeting-point-ricpe-whistleblower-continuity/index.html",
        "required": (
            "31 CONTROLLED ACTIONS · NONE AUTHORISED BY THIS PAGE",
            "Finite role-selected census: 40 of 101 confirmed; 61 pending.",
            "thirteen controlled source surfaces enumerated in the census",
            "It does not include the canonical transaction register or watch view added later",
            "it does not purport to enumerate hotel-by-hotel assets, new buyers, operators, managers, financiers or other counterparties",
            "The four legacy denominators and the fifth expanded 101-object denominator remain separate",
            "Open all 101 records — 40 confirmed / 61 pending →",
        ),
    },
    "S10": {
        "path": "de/fti-meeting-point-ricpe-hinweisgeber-kontinuitaet/index.html",
        "required": (
            "Endlicher, rollenbezogener Zensus: 40 von 101 bestätigt; 61 offen.",
            "dreizehn im Zensus aufgeführten kontrollierten Quellflächen",
            "Das später hinzugefügte kanonische Transaktionsregister und die Monitoringansicht sind nicht enthalten",
            "einzelne Hotels, neue Käufer, Betreiber, Manager, Finanzierer oder andere Gegenparteien vollständig aufzuführen",
            "Die vier bisherigen Nenner und der fünfte erweiterte Nenner mit 101 Objekten bleiben getrennt",
            "Alle 101 Datensätze öffnen — 40 bestätigt / 61 offen →",
        ),
    },
}
CENSUS_HREF = "../../assets/data/caepr-caret-fti-meeting-point-professional-institutional-v1.json"
PAGE_COUNT_MARKERS = ("<td>8/19</td>", "<td>22/40</td>", "<td>7/24</td>", "<td>3/18</td>")
REQUIRED_KEYS = {
    # Named people and office-holders in the German/Spanish chain.
    "MARK_SELLMANN",
    "AXEL_W_BIERBACH",
    "OLIVER_SCHARTL",
    "LARS_CREUTZMANN",
    "KARL_MARKGRAF",
    "SABINE_DORN",
    "GEORG_ABEGG",
    "PATRICIA_AYALA_JIMENEZ",
    "SINJA_BAUM",
    "ALBERTO_LOPEZ_VILLARRUBIA",
    "GUILLERMO_FERNANDEZ_GARCIA",
    # Exact legal persons, professional firms and controlled perimeters.
    "FTI_TOURISTIK_GMBH_EXACT",
    "FTI_GROUP_GOVERNANCE_COMPLIANCE",
    "MEETING_POINT_INTERNATIONAL_GMBH",
    "MP_HOTELMANAGEMENT_HOLDING_GMBH",
    "MP_HOTELMANAGEMENT_CANARIES",
    "MP_SPAIN",
    "MP_INVESTMENT",
    "FINKENHOF_EXACT",
    "MHBK_EXACT",
    "RODL_SPAIN_EXACT",
    "AUREN_REESTRUCTURACIONES",
    "PORTOBELLO_CAPITAL_SL",
    "GESTORA_BLUE_SEA_PARTNER",
    "BLUESEA_COMMERCIAL_PERIMETER",
    # Authorities and formal files.
    "AMTSGERICHT_MUNCHEN",
    "STAATSANWALTSCHAFT_MUNCHEN_I",
    "MUNICH_POLICE_K71",
    "FISCALIA_PROVINCIAL_LAS_PALMAS_EXACT",
    "CNMC",
    "CNMV",
    "AIPI_EXTERNAL_CHANNEL",
    "SEPI",
    "OLAF",
    "EPPO",
    "FTI_COMPLIANCE_2024_94",
    "FTI_INSOLVENCY_1500_IN_1758_24",
    "MP_INTERNATIONAL_INSOLVENCY_1500_IN_10126_24",
    "MP_HOLDING_INSOLVENCY_1500_IN_10107_24",
    "MEETING_POINT_357_2024",
    "CNMC_C_1549_25",
    "CGPJ_ALZADA_286_2026",
    "SEPI_FASEE_MEETING_POINT_OPERATION_FILE",
}
MANDATORY_COLLISION_FRAGMENTS = {
    "FTI Touristik controlled perimeter is not FTI Touristik GmbH",
    "Meeting Point Hotels commercial perimeter is not Meeting Point International GmbH",
    "FINKENHOF procedural counsel is not MHBK",
    "Axel W. Bierbach and Oliver Schartl are distinct people",
    "Generic Auren professional perimeter is not AUREN REESTRUCTURACIONES SLP",
    "SEPI is not FASEE",
    "BLUESEA commercial perimeter is not Gestora Blue Sea Partner, S.A.",
    "RIC statutory mechanism is not RIC Private Equity Investment Partners SCR, S.A.",
    "Ithikios/provider identity is not RICPE",
    "A registry attribution to Alberto López Villarrubia does not establish signature",
    "Registration, receipt and transmission are not opening",
}
UUID_RE = re.compile(
    r"(?<![0-9a-f])[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-"
    r"[89ab][0-9a-f]{3}-[0-9a-f]{12}(?![0-9a-f])",
    re.I,
)

errors: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def load_object(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"cannot load {path.relative_to(ROOT)}: {exc}")
        return {}
    check(isinstance(value, dict), f"{path.relative_to(ROOT)} root is not an object")
    return value if isinstance(value, dict) else {}


def registry_records() -> dict[str, dict]:
    master = load_object(ROOT / "assets/data/matter-identity-registry-v1.json")
    result: dict[str, dict] = {}
    for part in master.get("parts", []):
        part_path = ROOT / "assets/data" / str(part.get("path", ""))
        data = load_object(part_path)
        for record in data.get("records", []):
            rid = record.get("id")
            if isinstance(rid, str):
                check(rid not in result, f"duplicate canonical registry id: {rid}")
                result[rid] = record
    return result


def validate() -> None:
    data = load_object(PATH)
    check(data.get("control_id") == CONTROL_ID, "control id mismatch")
    check(data.get("verdict") == EXPECTED_VERDICT, "verdict mismatch")
    check("identity only" in str(data.get("scope_rule", "")).lower(), "identity-only rule missing")
    scope = str(data.get("scope", ""))
    check("finite role-selected snapshot" in scope.lower(), "finite role-selected scope missing")
    check("excludes the canonical asset-transaction register and watch view" in scope.lower(), "post-snapshot transaction exclusion missing")
    check("hotel-by-hotel assets" in scope.lower(), "hotel-by-hotel exclusion missing")
    check("does not follow links" in scope.lower(), "finite no-follow scope missing")

    surfaces = data.get("source_surfaces", [])
    check(isinstance(surfaces, list) and len(surfaces) == 13, "expected thirteen frozen source surfaces")
    surface_ids: set[str] = set()
    surface_by_id: dict[str, dict] = {}
    for surface in surfaces if isinstance(surfaces, list) else []:
        sid = surface.get("id")
        path = ROOT / str(surface.get("path", ""))
        digest = str(surface.get("sha256", ""))
        check(isinstance(sid, str) and sid not in surface_ids, f"bad or duplicate source id: {sid}")
        if isinstance(sid, str):
            surface_ids.add(sid)
            surface_by_id[sid] = surface
        check(path.is_file(), f"source surface does not exist: {surface.get('path')}")
        check(bool(re.fullmatch(r"[0-9a-f]{64}", digest)), f"bad source fingerprint: {sid}")

    # The three continuity pages are current integrated outputs as well as
    # enumerated source surfaces. Their public scope, denominator parity,
    # census link and exact bytes must remain synchronized with this asset.
    for sid, rules in PAGE_RULES.items():
        surface = surface_by_id.get(sid, {})
        expected_path = str(rules["path"])
        check(surface.get("path") == expected_path, f"{sid} continuity-page path mismatch")
        page_path = ROOT / expected_path
        if not page_path.is_file():
            continue
        page = page_path.read_text(encoding="utf-8")
        for marker in rules["required"]:
            check(marker in page, f"{sid} required public-scope marker missing: {marker}")
        for marker in PAGE_COUNT_MARKERS:
            check(marker in page, f"{sid} by-type 40/101 parity marker missing: {marker}")
        check(CENSUS_HREF in page, f"{sid} expanded-census JSON link missing")
        check("101/101" not in page, f"{sid} misleading 101/101 wording present")
        current_digest = hashlib.sha256(page_path.read_bytes()).hexdigest()
        check(
            surface.get("sha256") == current_digest,
            f"{sid} current page fingerprint mismatch: declared {surface.get('sha256')}, current {current_digest}",
        )

    records = data.get("records", [])
    check(isinstance(records, list), "records must be a list")
    if not isinstance(records, list):
        return
    check(len(records) == 101, f"denominator is {len(records)}, expected 101")
    check([r.get("ordinal") for r in records] == list(range(1, 102)), "ordinals are not exactly 1..101")
    keys = [r.get("object_key") for r in records]
    check(len(set(keys)) == 101, "object keys are not unique")
    labels = [r.get("label") for r in records]
    check(len(set(labels)) == 101, "labels are not unique")
    check(REQUIRED_KEYS <= set(keys), f"required objects missing: {sorted(REQUIRED_KEYS - set(keys))}")

    states = Counter(r.get("state") for r in records)
    check(states == Counter({"CARET_CONFIRMED": 40, "CARET_PENDING": 61}), f"state split wrong: {states}")
    declared = data.get("counts", {})
    check(declared.get("eligible") == 101, "declared eligible count mismatch")
    check(declared.get("confirmed") == 40, "declared confirmed count mismatch")
    check(declared.get("pending") == 61, "declared pending count mismatch")
    check(declared.get("suspended") == 0, "declared suspended count mismatch")
    check(declared.get("coverage_percent") == 39.6, "coverage percentage mismatch")

    registry = registry_records()
    allowed_registry_types = {
        "PERSON": {"PERSON"},
        "ORGANISATION_OR_STRUCTURE": {"ORGANISATION", "STRUCTURE"},
        "INSTITUTION_OR_SUBORGAN": {"INSTITUTION"},
        "PROCEEDING_OR_FILE": {"PROCEEDING"},
    }
    by_type = data.get("counts", {}).get("by_type", {})
    for record_type, (eligible, confirmed, pending) in EXPECTED_COUNTS.items():
        subset = [r for r in records if r.get("type") == record_type]
        subset_states = Counter(r.get("state") for r in subset)
        check(len(subset) == eligible, f"{record_type} eligible split wrong")
        check(subset_states == Counter({"CARET_CONFIRMED": confirmed, "CARET_PENDING": pending}), f"{record_type} state split wrong")
        check(
            by_type.get(record_type) == {
                "eligible": eligible,
                "confirmed": confirmed,
                "pending": pending,
                "suspended": 0,
            },
            f"declared {record_type} count object mismatch",
        )

    allowed_jurisdictions = {"GERMANY", "SPAIN", "SPAIN_GERMANY", "EUROPEAN_UNION", "CROSS_BORDER"}
    for record in records:
        key = record.get("object_key")
        record_type = record.get("type")
        check(record_type in EXPECTED_COUNTS, f"bad type for {key}")
        check(record.get("jurisdiction") in allowed_jurisdictions, f"bad jurisdiction for {key}")
        check(bool(record.get("role_class")), f"missing role class for {key}")
        refs = record.get("source_refs")
        check(isinstance(refs, list) and bool(refs), f"missing source refs for {key}")
        if isinstance(refs, list):
            check(set(refs) <= surface_ids, f"unknown source ref for {key}: {set(refs) - surface_ids}")
        if record.get("state") == "CARET_CONFIRMED":
            rid = record.get("caepr_id")
            check(isinstance(rid, str) and rid in registry, f"confirmed {key} lacks valid CAEPR id")
            if isinstance(rid, str) and rid in registry:
                check(
                    registry[rid].get("type") in allowed_registry_types.get(record_type, set()),
                    f"canonical type mismatch for {key}: {rid}",
                )
            check(bool(record.get("boundary")), f"confirmed {key} lacks identity boundary")
            check("next_source_needed" not in record, f"confirmed {key} carries pending source field")
        elif record.get("state") == "CARET_PENDING":
            check("caepr_id" not in record, f"pending {key} must not carry a CAEPR id")
            check(bool(record.get("next_source_needed")), f"pending {key} lacks finite next source")
            check(bool(record.get("finite_source_type")), f"pending {key} lacks finite source type")

    separation = {item.get("control_id"): item.get("denominator") for item in data.get("separate_from", [])}
    check(separation == EXPECTED_SEPARATE, f"separate-denominator control mismatch: {separation}")

    guard_text = "\n".join(str(item) for item in data.get("collision_guards", []))
    for fragment in MANDATORY_COLLISION_FRAGMENTS:
        check(fragment in guard_text, f"mandatory collision guard missing: {fragment}")

    # Exact object-state guards: official-looking sources do not create a caret
    # until the canonical registry contains the exact identity.
    state_by_key = {r.get("object_key"): r.get("state") for r in records}
    for key in {
        "FTI_TOURISTIK_GMBH_EXACT",
        "MEETING_POINT_INTERNATIONAL_GMBH",
        "MP_HOTELMANAGEMENT_HOLDING_GMBH",
        "FINKENHOF_EXACT",
        "MHBK_EXACT",
        "RODL_SPAIN_EXACT",
        "AXEL_W_BIERBACH",
        "OLIVER_SCHARTL",
        "AMTSGERICHT_MUNCHEN",
        "CNMC",
        "CNMV",
    }:
        check(state_by_key.get(key) == "CARET_PENDING", f"exact-object pending guard failed: {key}")

    # Public-safe census: never carry an exact whistleblowing-channel UUID.
    raw = PATH.read_text(encoding="utf-8")
    check(not UUID_RE.search(raw), "census exposes a UUID-like private channel identifier")


validate()

if errors:
    print("FTI / Meeting Point professional-institutional caret validation: FAIL", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print("FTI / Meeting Point professional-institutional caret validation: PASS")
print("- finite 101-object Germany/Spain/EU professional and authority census")
print("- 40 confirmed; 61 pending; 0 suspended; partial — not all is caret")
print("- exact-entity collision guards and identity-only boundary enforced")
print("- every pending object has a finite source need")
