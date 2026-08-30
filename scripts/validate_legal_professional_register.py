#!/usr/bin/env python3
"""Validate the authorised Por Derecho lawyers/procuradores register."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "assets" / "data"
INDEX = DATA / "matter-identity-registry-v1.json"
REGISTER = DATA / "legal-professionals-register-v1.json"
AUTHORIZATION = ROOT / ".github" / "governance" / "records" / "LEGAL_PROFESSIONAL_REGISTER_AUTHORIZATION_20260825.md"

ALAS_REQUIRED = {
    "PD-SP-P-0041",  # Juan Tomás Parrilla
    "PD-SP-P-0042",  # Armando Betancor
    "PD-SP-P-0043",  # José María Betancor
    "PD-SP-P-0044",  # Davinia Sánchez
    "PD-SP-P-0045",  # Joaquín Ruiz de Infante
    "PD-SP-P-0055",  # Cristo Ayose
    "PD-SP-P-0073",  # Ruth Pérez Castilla
    "PD-SP-P-0074",  # Luis A. Barber Marrero
}
PROCURADOR_REQUIRED = {
    "PD-SP-P-0056",  # Francisco Javier Pérez Almeida
    "PD-SP-P-0067",  # Adriana Hernández Díaz
    "PD-SP-P-0083",  # María del Pilar García Coello
    "PD-SP-P-0084",  # Tania Domínguez Limiñana
    "PD-SP-P-0085",  # Manuela Cabrera de la Cruz
    "PD-SP-P-0086",  # María Díaz Vecino
}
NEW_PROFESSIONAL_REQUIRED = {f"PD-SP-P-{n:04d}" for n in range(67, 83)}
PROHIBITED_ROSTER_NAMES = {
    "Guillermo Suárez Lacone",
    "Elisa Prieto",
    "Mª Natividad Heredia Marcos",
    "Yanira Alvarez",
}
REQUIRED_ORGANISATIONS = {
    "Sixto Abogados",
    "Carlos Llamas Legal Compliance",
    "Gallego Abogados",
    "DWF-RCD / Rousaud Costas Duran professional perimeter",
    "Del Rosal, Adame & Segrelles",
    "DPM Abogados",
}
ALLOWED_CLASSIFICATIONS = {"OUR_CURRENT_PROFESSIONAL", "OUR_FORMER_PROFESSIONAL"}
ALLOWED_TRACKS = {
    "CURRENT_COUNSEL", "FORMER_COUNSEL", "FORMER_COUNSEL_COLLABORATOR",
    "FORMER_COUNSEL_ROLE_REVIEW", "PROCURADOR_CURRENT", "PROCURADOR_FORMER",
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def fail(message: str):
    raise AssertionError(message)


def require(condition: bool, message: str):
    if not condition:
        fail(message)


def main() -> int:
    try:
        index = load(INDEX)
        reg = load(REGISTER)
        if reg.get("schema") != "por-derecho.legal-professionals-register.v1":
            fail("unexpected professional-register schema")
        if reg.get("register_id") != "PD-SP-LEGAL-PROF-001":
            fail("unexpected professional-register ID")
        if reg.get("authorization_reference") != "USER-2026-08-25-FULLEST-LEGAL-PROFESSIONAL-LIST":
            fail("missing controlling authorization reference")

        parts = []
        for descriptor in index.get("parts", []):
            path = DATA / descriptor["path"]
            if not path.is_file():
                fail(f"missing identity part {descriptor['path']}")
            payload = load(path)
            records = payload.get("records", [])
            if len(records) != descriptor.get("count"):
                fail(f"part count mismatch: {descriptor['path']}")
            parts.extend(records)

        identities = {r["id"]: r for r in parts}
        if len(identities) != len(parts):
            fail("duplicate immutable identity ID")
        counts = index.get("counts", {})
        if counts.get("total") != 229 or counts.get("PERSON") != 95 or counts.get("ORGANISATION") != 79:
            fail("canonical registry counts do not reflect professional extension")
        if len(parts) != 229:
            fail("canonical registry part total is not 229")

        records = reg.get("records", [])
        if len(records) != 40:
            fail(f"professional register must contain 40 records, found {len(records)}")
        ids = [r.get("identity_id") for r in records]
        id_set = set(ids)
        if len(ids) != len(id_set):
            fail("duplicate person in professional register")
        if not (ALAS_REQUIRED <= id_set):
            fail(f"missing Alas working professionals: {sorted(ALAS_REQUIRED - id_set)}")
        if not (PROCURADOR_REQUIRED <= id_set):
            fail(f"missing procuradores: {sorted(PROCURADOR_REQUIRED - id_set)}")
        if not (NEW_PROFESSIONAL_REQUIRED <= id_set):
            fail(f"missing newly admitted professional IDs: {sorted(NEW_PROFESSIONAL_REQUIRED - id_set)}")

        rendered_names = {r.get("public_name") for r in records}
        prohibited = rendered_names & PROHIBITED_ROSTER_NAMES
        if prohibited:
            fail(f"prohibited/non-professional names in roster: {sorted(prohibited)}")

        for record in records:
            pid = record.get("identity_id")
            if pid not in identities or identities[pid].get("type") != "PERSON":
                fail(f"unknown/non-person professional ID: {pid}")
            if record.get("classification") not in ALLOWED_CLASSIFICATIONS:
                fail(f"invalid professional classification for {pid}")
            if record.get("track") not in ALLOWED_TRACKS:
                fail(f"invalid professional track for {pid}: {record.get('track')}")
            if not record.get("evidence_status") or not record.get("matter_scope"):
                fail(f"missing status/scope for {pid}")
            if record.get("track") in {"PROCURADOR_CURRENT", "PROCURADOR_FORMER"}:
                require("Procurador" in str(record.get("role", "")), f"procurador track has non-procurador role: {pid}")
            if record.get("track") == "CURRENT_COUNSEL":
                require(record.get("role") == "Lawyer", f"current-counsel track has non-lawyer role: {pid}")
            for oid in record.get("firm_ids", []):
                if oid not in identities or identities[oid].get("type") != "ORGANISATION":
                    fail(f"unknown/non-organisation firm ID {oid} for {pid}")

        organisations = {r.get("name") for r in parts if r.get("type") == "ORGANISATION"}
        if not REQUIRED_ORGANISATIONS <= organisations:
            fail(f"missing professional organisations: {sorted(REQUIRED_ORGANISATIONS - organisations)}")

        computed = {
            "total": len(records),
            "current_counsel": sum(r["track"] == "CURRENT_COUNSEL" for r in records),
            "former_or_review_counsel": sum(r["track"] not in {"CURRENT_COUNSEL", "PROCURADOR_CURRENT", "PROCURADOR_FORMER"} for r in records),
            "current_procuradores": sum(r["track"] == "PROCURADOR_CURRENT" for r in records),
            "former_procuradores": sum(r["track"] == "PROCURADOR_FORMER" for r in records),
        }
        if reg.get("counts") != computed:
            fail(f"professional count drift: declared {reg.get('counts')}, computed {computed}")
        require(computed == {
            "total": 40,
            "current_counsel": 3,
            "former_or_review_counsel": 31,
            "current_procuradores": 2,
            "former_procuradores": 4,
        }, f"unexpected corrected professional totals: {computed}")

        by_id = {record["identity_id"]: record for record in records}
        adriana = by_id["PD-SP-P-0067"]
        require(adriana.get("role") == "Procuradora", "Adriana Hernández Díaz must be classified as procuradora")
        require(adriana.get("track") == "PROCURADOR_CURRENT", "Adriana Hernández Díaz has wrong track")
        require(adriana.get("evidence_status") == "COURT_RECORD_VERIFIED", "Adriana Hernández Díaz lacks court-record status")
        require("ETJ 163/2020" in adriana.get("matter_scope", ""), "Adriana Hernández Díaz scope must identify ETJ 163/2020")
        require("DP 748/2026" in adriana.get("matter_scope", ""), "Adriana Hernández Díaz scope must identify DP 748/2026")

        maria = by_id["PD-SP-P-0086"]
        require(maria.get("evidence_status") == "VERIFIED_CAPACITY_SCOPE_OPEN", "María Díaz Vecino must retain open scope status")
        require("proceeding-specific" in maria.get("matter_scope", ""), "María Díaz Vecino proceeding-specific limit missing")
        require("had not yet appeared" in maria.get("matter_scope", ""), "María Díaz Vecino non-personation limit missing")

        maria_aliases = set(identities["PD-SP-P-0086"].get("aliases", []))
        require({"María Luisa Díaz Vecino", "María Vecino Díaz"} <= maria_aliases, "María Díaz Vecino source-name variants missing")
        tania_aliases = set(identities["PD-SP-P-0084"].get("aliases", []))
        require("Tania Alejandra Domínguez Limiñana" in tania_aliases, "Tania Domínguez Limiñana fuller source-name variant missing")

        public_blob = REGISTER.read_text(encoding="utf-8")
        private_markers = ["mail.google.com", "gmail:", "@alaslegal.com", "@dras-abogados.com"]
        if any(marker in public_blob for marker in private_markers):
            fail("private-source locator leaked into public professional register")
        if re.search(r"\b[0-9a-f]{16}\b", public_blob, re.I):
            fail("probable private Gmail/source identifier leaked into public register")

        for path, markers in {
            ROOT / "es" / "profesionales-representantes" / "index.html": [
                "PD-SP-LEGAL-PROF-001", "Profesionales y representantes", "legal-professionals-register-v1.json",
                'data-prof-stat="CURRENT_COUNSEL">3', 'data-prof-stat="PROCURADOR_CURRENT">2', "Procuradoras actuales",
            ],
            ROOT / "en" / "professionals-representatives" / "index.html": [
                "PD-SP-LEGAL-PROF-001", "Professionals and representatives", "legal-professionals-register-v1.json",
                'data-prof-stat="CURRENT_COUNSEL">3', 'data-prof-stat="PROCURADOR_CURRENT">2', "Current procuradoras",
            ],
            ROOT / "assets" / "legal-professionals-register.js": [
                "CURRENT_COUNSEL", "PROCURADOR_FORMER", "REVIEW|OPEN", "Procuradoras actuales", "Current procuradoras",
            ],
            AUTHORIZATION: [
                "Post-merge factual correction", "Adriana Hernández Díaz as Procuradora de los Tribunales",
                "three current lawyers", "two current procuradoras",
            ],
        }.items():
            if not path.is_file():
                fail(f"missing public professional surface: {path.relative_to(ROOT)}")
            text = path.read_text(encoding="utf-8")
            for marker in markers:
                if marker not in text:
                    fail(f"missing marker {marker!r} in {path.relative_to(ROOT)}")

        extension_blob = (DATA / "matter-identity-registry-v1.professional-people.json").read_text(encoding="utf-8")
        if "Guillermo Suárez Lacone" in extension_blob:
            fail("explicitly excluded person appears in professional identity extension")

        print("LEGAL PROFESSIONAL REGISTER: PASS")
        print(" - canonical identities: 229 (95 people; 79 organisations)")
        print(" - professional roster: 40")
        print(" - current lawyers: 3; former/review lawyers: 31")
        print(" - procuradores/as: 2 current + 4 former")
        print(" - Adriana Hernández Díaz: court-record-verified procuradora")
        print(" - source-name variants: preserved")
        print(" - Alas working-professional set: complete")
        print(" - explicit exclusion: enforced")
        return 0
    except AssertionError as exc:
        print(f"LEGAL PROFESSIONAL REGISTER: FAIL\n - {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
