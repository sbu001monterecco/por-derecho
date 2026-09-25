#!/usr/bin/env python3
"""Validate the canonical Calificación position, objectives, status and proof controls."""
from __future__ import annotations

import json
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class StructureParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.position_layers = 0
        self.objective_depth = 0
        self.objective_items = 0
        self.closure_depth = 0
        self.closure_rows = 0
        self.rpl_status_sections = 0

    @staticmethod
    def attrs_dict(attrs: list[tuple[str, str | None]]) -> dict[str, str]:
        return {key: value or "" for key, value in attrs}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = self.attrs_dict(attrs)
        classes = set(values.get("class", "").split())
        if "data-calificacion-position-objectives" in values:
            self.position_layers += 1
        if values.get("id") in {"posicion-objetivos", "position-objectives"}:
            self.objective_depth = 1
        elif self.objective_depth:
            self.objective_depth += 1
        if self.objective_depth and tag == "li":
            self.objective_items += 1
        if "cm-closure-table" in classes:
            self.closure_depth = 1
        elif self.closure_depth:
            self.closure_depth += 1
        if self.closure_depth and tag == "tr":
            self.closure_rows += 1
        if values.get("id") in {"estado-rpl-2523-2025", "rpl-2523-2025-status"}:
            self.rpl_status_sections += 1

    def handle_endtag(self, tag: str) -> None:
        if self.objective_depth:
            self.objective_depth -= 1
        if self.closure_depth:
            self.closure_depth -= 1


def require(errors: list[str], condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    errors: list[str] = []
    canonical = {
        "es/tesis-uso-criminal-procedimiento-calificacion/index.html": [
            "Nuestra posición no es que toda resolución adversa sea delictiva",
            "La cuestión es si se invirtió la responsabilidad y se desvió el escrutinio",
            "Corrección, recuperación y responsabilidad proporcional",
            "TRANSFERENCIA DE VALOR + INVERSIÓN DE RESPONSABILIDAD + DESVIACIÓN DEL ESCRUTINIO",
            "Verificado hasta 24 ago 2026",
            "No se ha localizado una sentencia de fondo posterior",
            "No pedimos a ninguna autoridad que acepte esa conclusión de antemano",
            "El defecto textual puede ser un error y debe esclarecerse",
        ],
        "en/insolvency-classification-criminal-misuse-thesis/index.html": [
            "Our position is not that every adverse decision is criminal",
            "The question is whether responsibility was inverted and scrutiny diverted",
            "Correction, recovery and proportionate accountability",
            "TRANSFER OF VALUE + INVERSION OF RESPONSIBILITY + DIVERSION OF SCRUTINY",
            "Verified through 24 Aug 2026",
            "No later merits judgment, service record or finality record has been located",
            "We ask no institution to accept that conclusion in advance",
            "The textual defect may be an error and must be clarified",
        ],
    }
    for path, markers in canonical.items():
        body = read(path)
        parser = StructureParser()
        parser.feed(body)
        for marker in markers:
            require(errors, marker in body, f"{path}: missing {marker!r}")
        require(errors, parser.position_layers == 1, f"{path}: expected one canonical Position/Objectives layer, found {parser.position_layers}")
        require(errors, parser.objective_items == 7, f"{path}: expected seven objectives, found {parser.objective_items}")
        require(errors, parser.closure_rows == 6, f"{path}: expected five closure rows plus header, found {parser.closure_rows}")
        require(errors, parser.rpl_status_sections == 1, f"{path}: expected one RPL status section")

    appeals = {
        "es/concurso-36-2012-ap-seccion-4/index.html": [
            "ACTUALIZADO · 24 AGOSTO 2026",
            "A 24 de agosto de 2026",
            "La expectativa legítima es estrecha y exigente",
            "La independencia institucional incluye la capacidad de corregir el error de primera instancia",
            "cualquier otra acción corresponde a su foro propio",
        ],
        "en/insolvency-36-2012-ap-section-4/index.html": [
            "UPDATED · 24 AUGUST 2026",
            "As at 24 August 2026",
            "The legitimate expectation is narrow and exacting",
            "Institutional independence includes the capacity to correct first-instance error",
            "every other action belongs in its proper forum",
        ],
    }
    for path, markers in appeals.items():
        body = read(path)
        parser = StructureParser()
        parser.feed(body)
        for marker in markers:
            require(errors, marker in body, f"{path}: missing {marker!r}")
        require(errors, parser.position_layers == 1, f"{path}: expected one appeal Position/Objectives layer, found {parser.position_layers}")
        require(errors, "23 August 2026" not in body and "23 de agosto de 2026" not in body, f"{path}: stale 23-Aug status remains")

    ledger = json.loads(read("assets/data/calificacion-criminal-misuse-thesis-v1.json"))
    position = ledger.get("position_and_objectives", {})
    require(errors, len(position.get("es", {}).get("objectives", [])) == 7, "machine ledger: Spanish objectives must contain seven items")
    require(errors, len(position.get("en", {}).get("objectives", [])) == 7, "machine ledger: English objectives must contain seven items")
    require(errors, position.get("controlling_hypothesis") == "TRANSFER_OF_VALUE_PLUS_INVERSION_OF_RESPONSIBILITY_PLUS_DIVERSION_OF_SCRUTINY", "machine ledger: controlling hypothesis missing")
    status = ledger.get("appeal_status", {})
    require(errors, status.get("roll") == "RPL 2523/2025", "machine ledger: appeal roll mismatch")
    require(errors, status.get("corpus_cutoff") == "2026-08-24", "machine ledger: corpus cutoff mismatch")
    require(errors, status.get("later_merits_ruling_located") is False, "machine ledger: later ruling state must remain false/not located")
    require(errors, status.get("inference_limit") == "NOT_LOCATED_DOES_NOT_MEAN_NONEXISTENT", "machine ledger: nonexistence inference limit missing")
    require(errors, len(ledger.get("pillars", [])) == 5, "machine ledger: expected five pillars")
    require(errors, all(item.get("evidence_state") for item in ledger.get("pillars", [])), "machine ledger: every pillar needs an evidence state")

    loader = read("assets/calificacion-criminal-misuse-thesis-20260824.js")
    root_site = read("assets/site.js")
    site = read("assets/site-pre-treasury-154-hq-20260828.js")
    css = read("assets/styles.css")
    render = read("scripts/render_calificacion_criminal_misuse_thesis.mjs")
    workflow = read(".github/workflows/validate-calificacion-criminal-misuse-thesis.yml")
    for marker in ["addPositionStrip", "calificacionPositionObjectives", "Our position", "Nuestra posición", "Appeal boundary", "Límite de apelación", "persistent-20260824d"]:
        require(errors, marker in loader, f"scoped loader: missing {marker!r}")
    require(errors, "site-pre-treasury-154-hq-20260828.js?v=20260828a" in root_site, "root site loader: delegated pre-Treasury release missing")
    require(errors, "calificacion-criminal-misuse-thesis-20260824.js?v=20260824d" in site, "delegated site loader: revision 20260824d missing")
    for marker in ["CALIFICACION-POSITION-OBJECTIVES-20260824", ".cm-position-objectives", ".cm-rpl-status", ".cm-closure-table", ".cm-evidence-state--open"]:
        require(errors, marker in css, f"styles: missing {marker!r}")
    for marker in ["positionCount", "positionVisible", "closureTests", "rplStatusVisible", "20260824d"]:
        require(errors, marker in render, f"render gate: missing {marker!r}")
    require(errors, "validate_calificacion_position_objectives.py" in workflow, "workflow: Position/Objectives validator is not registered")

    control = read("archive/CALIFICACION_POSITION_OBJECTIVES_STATUS_PROOF_CONTROL_24AUG2026.md")
    for marker in ["Canonical position", "Canonical objectives", "RPL 2523/2025 controlled status", "Appeal firewall", "Five finite proof demands", "Publication exclusions"]:
        require(errors, marker in control, f"canonical control: missing {marker!r}")
    register = read("archive/MISSING_EVIDENCE_REGISTER.md")
    require(errors, "ME-013" in register and "no later signed merits decision" in register, "ME-013: updated 24-Aug status not recorded")

    manifest = json.loads(read("publication-manifests/calificacion-position-objectives-20260824.json"))
    safety = manifest.get("publication_safety", {})
    require(errors, safety.get("criminal_guilt_stated_as_adjudicated") is False, "manifest: non-adjudication safety missing")
    require(errors, safety.get("appeal_pressure_or_threat_language_used") is False, "manifest: appeal pressure safety missing")
    require(errors, safety.get("appeal_independence_preserved") is True, "manifest: appeal independence must be preserved")

    public_bodies = "\n".join(read(path) for path in [*canonical, *appeals])
    prohibited = [
        "this will cost them",
        "les costará",
        "capture is proved",
        "captura está probada",
        "the Fiscal confessed",
        "el Fiscal confesó",
        "silence proves guilt",
        "el silencio prueba culpabilidad",
    ]
    lowered = public_bodies.lower()
    for phrase in prohibited:
        require(errors, phrase.lower() not in lowered, f"public pages: prohibited formulation remains {phrase!r}")

    if errors:
        print("CALIFICACION POSITION / OBJECTIVES / STATUS / PROOF: FAIL")
        for error in errors:
            print(f" - {error}")
        return 1
    print("CALIFICACION POSITION / OBJECTIVES / STATUS / PROOF: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
