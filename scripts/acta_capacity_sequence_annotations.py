#!/usr/bin/env python3
"""Deterministic event-level capacity and attributed-sequence annotations.

The annotations in this module are intentionally narrower than an actor
biography.  They record only the capacity proved for Patricia Isabel
Domínguez Montelongo in each controlled ACTA/meeting family and the place of
that family, if any, in Gil Marer's attributed adverse-perimeter sequence.

Running this module without ``--write`` checks the controlled continuity JSON.
``--write`` applies the annotations deterministically.  The helper never
changes document/source IDs or any source-copy metadata.
"""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
DEFAULT_CONTINUITY = REPO / "evidence/community/actas/event-family-continuity-v1.json"

PATRICIA_PERSON = {
    "canonical_register_id": "P002",
    "actor_code": "PATRICIA_ISABEL_DOMINGUEZ_MONTELONGO",
    "canonical_name": "Patricia Isabel Domínguez Montelongo",
    "identity_status": "controlled-canonical-person",
}

PATRICIA_IDENTITY_CONTROL = {
    "distinct_from_canonical_register_id": "P028",
    "distinct_from_actor_code": "LAURA_PATRICIA_ACOSTA_MATOS",
    "distinct_from_canonical_name": "Laura Patricia Acosta Matos",
    "es": (
        "Patricia Isabel Domínguez Montelongo y Laura Patricia Acosta Matos "
        "son personas distintas; nunca se usa 'Patricia' para fusionarlas."
    ),
    "en": (
        "Patricia Isabel Domínguez Montelongo and Laura Patricia Acosta Matos "
        "are different people; 'Patricia' is never used to merge them."
    ),
}

CAPACITY_INFERENCE_BOUNDARY = {
    "es": (
        "Una función en Pink Canary Services, una participación personal o una "
        "declaración posterior no se transforma en representación de la Comunidad, "
        "CEXP, LPB, Aweswell ni otra entidad para este evento."
    ),
    "en": (
        "A Pink Canary Services role, personal participation or a later statement "
        "does not become representation of the Community, CEXP, LPB, Aweswell or "
        "another entity for this event."
    ),
}


ADVERSE_SEQUENCE_MODEL = {
    "theory_code": "GIL_ATTRIBUTED_ADVERSE_PERIMETER_SEQUENCE",
    "classification_status": "party-attributed-theory-and-project-documentary-classification",
    "sequence_node_codes": [
        "AAS",
        "FMMM_COGOLLUDO_PAMANIL",
        "ACOSTA_MATOS_CAM",
    ],
    "sequence_display": {
        "es": "AAS -> FMMM/Cogolludo/Pamanil -> Acosta Matos/CAM",
        "en": "AAS -> FMMM/Cogolludo/Pamanil -> Acosta Matos/CAM",
    },
    "actors": [
        {
            "actor_code": "AAS",
            "canonical_name": "Asunción Aizpurúa Sánchez",
            "actor_type": "natural-person",
            "sequence_node_code": "AAS",
        },
        {
            "actor_code": "FMMM",
            "canonical_name": "Francisco Mario Matos Matas",
            "actor_type": "natural-person",
            "sequence_node_code": "FMMM_COGOLLUDO_PAMANIL",
        },
        {
            "actor_code": "ANTONIO_COGOLLUDO_ROJAS",
            "canonical_name": "Antonio Cogolludo Rojas",
            "actor_type": "natural-person",
            "sequence_node_code": "FMMM_COGOLLUDO_PAMANIL",
        },
        {
            "actor_code": "SHAILA_MARIA_COGOLLUDO_RAMOS",
            "canonical_name": "Shaila María Cogolludo Ramos",
            "actor_type": "natural-person",
            "sequence_node_code": "FMMM_COGOLLUDO_PAMANIL",
        },
        {
            "actor_code": "PAMANIL",
            "canonical_name": "Pamanil, S.L.",
            "actor_type": "legal-person",
            "sequence_node_code": "FMMM_COGOLLUDO_PAMANIL",
        },
        {
            "actor_code": "JOSE_DANIEL_ACOSTA_MATOS",
            "canonical_name": "José Daniel Acosta Matos",
            "actor_type": "natural-person",
            "sequence_node_code": "ACOSTA_MATOS_CAM",
        },
        {
            "actor_code": "LAURA_PATRICIA_ACOSTA_MATOS",
            "canonical_name": "Laura Patricia Acosta Matos",
            "actor_type": "natural-person",
            "sequence_node_code": "ACOSTA_MATOS_CAM",
        },
        {
            "actor_code": "JAVIER_ACOSTA_MATOS",
            "canonical_name": "Javier Acosta Matos",
            "actor_type": "natural-person",
            "sequence_node_code": "ACOSTA_MATOS_CAM",
        },
        {
            "actor_code": "GERARDO_ZACARIAS_ACOSTA_MATOS",
            "canonical_name": "Gerardo Zacarías Acosta Matos",
            "actor_type": "natural-person",
            "sequence_node_code": "ACOSTA_MATOS_CAM",
        },
        {
            "actor_code": "CAM",
            "canonical_name": "Construcciones Acosta Matos, S.A.",
            "actor_type": "legal-person",
            "sequence_node_code": "ACOSTA_MATOS_CAM",
        },
    ],
    "boundary": {
        "es": (
            "Secuencia atribuida por Gil Marer y clasificación documental del proyecto. "
            "Cada persona, sociedad, cargo, representación y acto se mantiene separado y "
            "debe probarse fuente por fuente. No es un hallazgo judicial de conspiracion, "
            "fraude, finalidad criminal, responsabilidad o culpabilidad."
        ),
        "en": (
            "Sequence attributed by Gil Marer and the project's documentary classification. "
            "Every person, company, office, representation and act remains separate and must "
            "be proved source by source. It is not an adjudicated finding of conspiracy, "
            "fraud, criminal purpose, liability or guilt."
        ),
    },
}


def _capacity_none(event_family_id: str, source_note_es: str | None = None,
                   source_note_en: str | None = None) -> dict:
    """Return an explicit no-event-specific-capacity record."""
    return {
        "event_family_id": event_family_id,
        "person": copy.deepcopy(PATRICIA_PERSON),
        "status_code": "no-event-specific-capacity-documented",
        "documented_roles": [],
        "summary": {
            "es": (
                "No se documenta para Patricia Isabel Domínguez Montelongo una capacidad "
                "específica en este evento."
            ),
            "en": (
                "No event-specific capacity is documented for Patricia Isabel Domínguez "
                "Montelongo in this event."
            ),
        },
        "source_basis": {
            "es": source_note_es or "Las fuentes controladas de esta familia no prueban una capacidad propia del evento.",
            "en": source_note_en or "The controlled sources for this family do not prove an event-specific capacity.",
        },
        "identity_control": copy.deepcopy(PATRICIA_IDENTITY_CONTROL),
        "inference_boundary": copy.deepcopy(CAPACITY_INFERENCE_BOUNDARY),
    }


def _capacity_2012(event_family_id: str) -> dict:
    return {
        "event_family_id": event_family_id,
        "person": copy.deepcopy(PATRICIA_PERSON),
        "status_code": "documented-spanish-statement-reader-only",
        "documented_roles": [
            {
                "role_code": "spanish-language-reader-of-presidents-prepared-statement",
                "principal_actor_code": None,
                "es": "Lectura en español de la versión de una declaración previamente redactada del presidente.",
                "en": "Read the Spanish version of the chair's previously prepared statement.",
            }
        ],
        "summary": {
            "es": (
                "El ACTA sólo documenta que leyó en español la versión de una declaración "
                "previamente redactada del presidente e incorporada al ACTA."
            ),
            "en": (
                "The minutes document only that she read the Spanish version of the chair's "
                "previously prepared statement, which was incorporated into the minutes."
            ),
        },
        "source_basis": {
            "es": "ACTA de 10-Aug-2012, página fuente 3 de 4; declaración separada localizada.",
            "en": "10-Aug-2012 minutes, source page 3 of 4; separate statement located.",
        },
        "identity_control": copy.deepcopy(PATRICIA_IDENTITY_CONTROL),
        "inference_boundary": {
            "es": (
                "La lectura no prueba por sí sola representación de LPB, CEXP, la Comunidad, "
                "Aweswell o Pink Canary Services, ni autoría o aprobación del contenido."
            ),
            "en": (
                "Reading the statement does not by itself prove representation of LPB, CEXP, "
                "the Community, Aweswell or Pink Canary Services, or authorship or adoption of "
                "its content."
            ),
        },
    }


def _capacity_2016_04_26(event_family_id: str) -> dict:
    return {
        "event_family_id": event_family_id,
        "person": copy.deepcopy(PATRICIA_PERSON),
        "status_code": "documented-lpb-representative",
        "documented_roles": [
            {
                "role_code": "representative-of-legal-person",
                "principal_actor_code": "LPB",
                "principal_canonical_name": "Luchy Playa Blanca, S.L.U.",
                "es": "Representante de Luchy Playa Blanca, S.L.U. (LPB).",
                "en": "Representative of Luchy Playa Blanca, S.L.U. (LPB).",
            },
            {
                "role_code": "representative-of-owner",
                "principal_actor_code": "MARIANO_PALACIOS_FERNANDEZ",
                "principal_canonical_name": "Mariano Palacios Fernandez",
                "es": "La lista de representación controlada también la vincula a Mariano Palacios Fernández.",
                "en": "The controlled representation list also links her to Mariano Palacios Fernandez.",
            },
        ],
        "summary": {
            "es": (
                "El ACTA la identifica expresamente como representante de LPB; el mapa de "
                "asistencia controlado también registra la representación de Mariano Palacios "
                "Fernández."
            ),
            "en": (
                "The minutes expressly identify her as LPB's representative; the controlled "
                "attendance map also records representation of Mariano Palacios Fernandez."
            ),
        },
        "source_basis": {
            "es": "ACTA de 26-Apr-2016 y lista/mapa de asistencia y representación de su paquete de 77 páginas.",
            "en": "26-Apr-2016 minutes and the attendance/representation list and map in its 77-page package.",
        },
        "identity_control": copy.deepcopy(PATRICIA_IDENTITY_CONTROL),
        "inference_boundary": {
            "es": (
                "Estas representaciones son específicas de este evento; no prueban que actuara "
                "por la Comunidad, CEXP, Aweswell o Pink Canary Services ni se trasladan a otra "
                "reunión."
            ),
            "en": (
                "These representations are specific to this event; they do not prove that she "
                "acted for the Community, CEXP, Aweswell or Pink Canary Services and do not carry "
                "over to another meeting."
            ),
        },
    }


def _stage(event_family_id: str, stage_code: str, applicability_code: str,
           sequence_node_codes: list[str], event_actor_codes: list[str],
           summary_es: str, summary_en: str) -> dict:
    return {
        "event_family_id": event_family_id,
        "theory_code": ADVERSE_SEQUENCE_MODEL["theory_code"],
        "stage_code": stage_code,
        "applicability_code": applicability_code,
        "sequence_node_codes": sequence_node_codes,
        "event_actor_codes": event_actor_codes,
        "summary": {"es": summary_es, "en": summary_en},
        "boundary": copy.deepcopy(ADVERSE_SEQUENCE_MODEL["boundary"]),
    }


EVENT_IDS = (
    "SP-ACTA-2008-04-29",
    "SP-ACTA-2008-07-15",
    "SP-ACTA-2008-07-15-CEXP",
    "SP-ACTA-2008-07-25",
    "SP-ACTA-2008-12-17",
    "SP-ACTA-2009-05-28",
    "SP-ACTA-2011-02-02",
    "SP-ACTA-2011-06-22",
    "SP-ACTA-2012-08-10",
    "SP-ACTA-2014-04-10",
    "SP-ACTA-2014-08-28-CP",
    "SP-ACTA-2014-08-28-CEXP",
    "SP-ACTA-2015-11-19",
    "SP-ACTA-2016-04-26",
    "SP-MEETING-2016-06-10",
    "SP-ACTA-2017-04-07-CEXP",
    "SP-ACTA-2017-06-12",
    "SP-ACTA-2018-05-18",
    "SP-ACTA-2018-07-05",
    "SP-RECITAL-2018-11-20",
    "SP-RECITAL-2021-12-29-RICPE",
    "SP-ACTA-2022-02-04",
    "SP-MEETING-2022-03-11-RICPE",
)


_STAGE_ROWS = {
    "SP-ACTA-2008-04-29": (
        "pre-sequence-pre-sale", "not-applicable", [], [],
        "Evento anterior a la secuencia adversa atribuida; carril A de preventa.",
        "Event predating the attributed adverse sequence; pre-sale lane A.",
    ),
    "SP-ACTA-2008-07-15": (
        "post-sale-transition-unresolved", "transition-unresolved", [], [],
        "Transición de 2008 sin base segura para asignarla a un nodo de la secuencia adversa.",
        "2008 transition with no safe basis for assignment to an adverse-sequence node.",
    ),
    "SP-ACTA-2008-07-15-CEXP": (
        "post-sale-transition-unresolved", "transition-unresolved", [], [],
        "Reunión CEXP de transición con participación cruzada; no se fuerza un nodo adverso.",
        "Transitional CEXP meeting with cross-lane participation; no adverse node is forced.",
    ),
    "SP-ACTA-2008-07-25": (
        "project-lane-no-adverse-stage", "not-applicable", [], [],
        "Evento del carril del proyecto; no se le asigna etapa adversa.",
        "Project-lane event; no adverse stage is assigned.",
    ),
    "SP-ACTA-2008-12-17": (
        "unresolved-no-safe-stage", "unresolved", [], [],
        "La atribución del evento no permite fijar una etapa adversa.",
        "The event attribution does not permit an adverse stage to be fixed.",
    ),
    "SP-ACTA-2009-05-28": (
        "project-lane-no-adverse-stage", "not-applicable", [], [],
        "Evento del carril del proyecto; no se le asigna etapa adversa.",
        "Project-lane event; no adverse stage is assigned.",
    ),
    "SP-ACTA-2011-02-02": (
        "aas-stage", "attributed-primary", ["AAS"], ["AAS"],
        "Primer nodo AAS en la secuencia atribuida; los cambios de cargos se documentan, su finalidad no.",
        "AAS node in the attributed sequence; office changes are documented, their purpose is not.",
    ),
    "SP-ACTA-2011-06-22": (
        "aas-to-fmmm-cogolludo-pamanil-transition", "attributed-transition-overlap",
        ["AAS", "FMMM_COGOLLUDO_PAMANIL"], ["AAS", "FMMM", "PAMANIL"],
        "Transicion/solapamiento documentado entre AAS y el nodo FMMM/Pamanil; Cogolludo permanece actor separado.",
        "Documented transition/overlap between AAS and the FMMM/Pamanil node; Cogolludo remains a separate actor.",
    ),
    "SP-ACTA-2012-08-10": (
        "fmmm-cogolludo-pamanil-counterparty-overlap", "cross-lane-context",
        ["FMMM_COGOLLUDO_PAMANIL"], [],
        "Reunión del carril B con objeción/contraposición del nodo C1; esa presencia no cambia quién convocó.",
        "Lane-B meeting with objection/counter-position from the C1 node; that presence does not change who called it.",
    ),
    "SP-ACTA-2014-04-10": (
        "fmmm-cogolludo-pamanil-counterparty-overlap", "cross-lane-context",
        ["FMMM_COGOLLUDO_PAMANIL"], ["ANTONIO_COGOLLUDO_ROJAS", "PAMANIL"],
        "Junta competidora del carril B frente al nodo FMMM/Cogolludo/Pamanil; participación u objeción no equivale a control.",
        "Competing lane-B meeting opposite the FMMM/Cogolludo/Pamanil node; participation or objection is not control.",
    ),
    "SP-ACTA-2014-08-28-CP": (
        "fmmm-cogolludo-pamanil-counterparty-overlap", "cross-lane-context",
        ["FMMM_COGOLLUDO_PAMANIL"], ["PAMANIL"],
        "Registro del carril B que discute la autoridad Pamanil; contexto cruzado, no reasignacion del evento.",
        "Lane-B record addressing Pamanil authority; cross-lane context, not event reassignment.",
    ),
    "SP-ACTA-2014-08-28-CEXP": (
        "project-lane-no-adverse-stage", "not-applicable", [], [],
        "ACTA CEXP del carril del proyecto; no se le asigna etapa adversa.",
        "Project-lane CEXP minutes; no adverse stage is assigned.",
    ),
    "SP-ACTA-2015-11-19": (
        "aas-fmmm-cogolludo-pamanil-overlap", "attributed-primary-overlap",
        ["AAS", "FMMM_COGOLLUDO_PAMANIL"], ["AAS", "FMMM", "PAMANIL"],
        "Solapamiento AAS con la fase FMMM/Cogolludo/Pamanil atribuida por Gil; cargos y actos se prueban por separado.",
        "AAS overlap with the FMMM/Cogolludo/Pamanil phase attributed by Gil; offices and acts are proved separately.",
    ),
    "SP-ACTA-2016-04-26": (
        "aas-fmmm-cogolludo-pamanil-overlap", "attributed-primary-overlap",
        ["AAS", "FMMM_COGOLLUDO_PAMANIL"], ["AAS", "FMMM", "PAMANIL"],
        "Solapamiento AAS con la fase FMMM/Cogolludo/Pamanil; la asistencia LPB no convierte la junta en evento del carril B.",
        "AAS overlap with the FMMM/Cogolludo/Pamanil phase; LPB attendance does not turn the meeting into a lane-B event.",
    ),
    "SP-MEETING-2016-06-10": (
        "fmmm-pamanil-professional-overlap", "mixed-cross-lane-context",
        ["FMMM_COGOLLUDO_PAMANIL"], [],
        "Reunion profesional mixta que cruza los trabajos LPB/asesores y Comunidad/FMMM; capacidades y control siguen abiertos.",
        "Mixed professional meeting crossing LPB/adviser and Community/FMMM workstreams; capacities and control remain open.",
    ),
    "SP-ACTA-2017-04-07-CEXP": (
        "project-lane-no-adverse-stage", "not-applicable", [], [],
        "ACTA CEXP del carril del proyecto; no se le asigna etapa adversa.",
        "Project-lane CEXP minutes; no adverse stage is assigned.",
    ),
    "SP-ACTA-2017-06-12": (
        "fmmm-cogolludo-pamanil-late-stage", "attributed-primary",
        ["FMMM_COGOLLUDO_PAMANIL"], ["PAMANIL"],
        "Continuidad tardía del nodo FMMM/Cogolludo/Pamanil antes de la transición documentada hacia CAM.",
        "Late continuity of the FMMM/Cogolludo/Pamanil node before the documented transition towards CAM.",
    ),
    "SP-ACTA-2018-05-18": (
        "fmmm-cogolludo-pamanil-to-acosta-matos-cam-transition", "attributed-transition-overlap",
        ["FMMM_COGOLLUDO_PAMANIL", "ACOSTA_MATOS_CAM"],
        ["ANTONIO_COGOLLUDO_ROJAS", "SHAILA_MARIA_COGOLLUDO_RAMOS", "CAM"],
        "Transicion/solapamiento entre el nodo Cogolludo/Pamanil y Acosta Matos/CAM; no prueba una toma total.",
        "Transition/overlap between the Cogolludo/Pamanil and Acosta Matos/CAM nodes; it does not prove a total takeover.",
    ),
    "SP-ACTA-2018-07-05": (
        "acosta-matos-cam-stage", "attributed-primary", ["ACOSTA_MATOS_CAM"],
        ["SHAILA_MARIA_COGOLLUDO_RAMOS", "JOSE_DANIEL_ACOSTA_MATOS", "CAM"],
        "Fase Acosta Matos/CAM atribuida por Gil; las funciones concretas de CAM, José Daniel y Shaila se leen fuente por fuente.",
        "Acosta Matos/CAM phase attributed by Gil; the specific roles of CAM, José Daniel and Shaila are read source by source.",
    ),
    "SP-RECITAL-2018-11-20": (
        "acosta-matos-era-recital-unresolved", "unresolved", ["ACOSTA_MATOS_CAM"], [],
        "Mención posterior de la época Acosta Matos/CAM; sin original no se atribuyen convocante, asistentes o control.",
        "Later recital from the Acosta Matos/CAM period; without the original, convener, attendees and control are not assigned.",
    ),
    "SP-RECITAL-2021-12-29-RICPE": (
        "ricpe-corporate-recital-no-adverse-stage", "not-applicable-independent-corporate-body", [], [],
        "Mención posterior de una junta societaria RICPE; RICPE permanece separada de la Comunidad, CAM y los nodos adversos atribuidos, y la mención no prueba la reunión o el acuerdo.",
        "Later recital of a RICPE corporate shareholders' meeting; RICPE remains separate from the Community, CAM and the attributed adverse nodes, and the recital does not prove the meeting or resolution.",
    ),
    "SP-ACTA-2022-02-04": (
        "acosta-matos-cam-stage", "attributed-primary", ["ACOSTA_MATOS_CAM"],
        ["JAVIER_ACOSTA_MATOS", "LAURA_PATRICIA_ACOSTA_MATOS", "JOSE_DANIEL_ACOSTA_MATOS", "CAM"],
        "Fase Acosta Matos/CAM atribuida por Gil; Javier, Laura Patricia, José Daniel y CAM conservan identidades y capacidades separadas.",
        "Acosta Matos/CAM phase attributed by Gil; Javier, Laura Patricia, José Daniel and CAM retain separate identities and capacities.",
    ),
    "SP-MEETING-2022-03-11-RICPE": (
        "ricpe-corporate-notice-no-adverse-stage", "not-applicable-independent-corporate-body", [], [],
        "Convocatoria societaria RICPE fuera de la secuencia adversa atribuida; la clasificación mixta evita fusionar RICPE con la Comunidad, CAM o sus personas relacionadas.",
        "RICPE corporate notice outside the attributed adverse sequence; the mixed classification prevents RICPE from being merged with the Community, CAM or their related persons.",
    ),
}


EVENT_ANNOTATIONS: dict[str, dict] = {}
for _event_id in EVENT_IDS:
    if _event_id == "SP-ACTA-2012-08-10":
        _capacity = _capacity_2012(_event_id)
    elif _event_id == "SP-ACTA-2016-04-26":
        _capacity = _capacity_2016_04_26(_event_id)
    elif _event_id == "SP-MEETING-2016-06-10":
        _capacity = _capacity_none(
            _event_id,
            "El mapa de hablantes/asistentes y sus capacidades permanece abierto; no se importa una capacidad de otra reunión.",
            "The speaker/attendee and capacity map remains open; no capacity is imported from another meeting.",
        )
    else:
        _capacity = _capacity_none(_event_id)
    EVENT_ANNOTATIONS[_event_id] = {
        "patricia_dominguez_capacity": _capacity,
        "adverse_sequence_stage": _stage(_event_id, *_STAGE_ROWS[_event_id]),
    }


def validate_controlled_event_ids(event_ids: list[str] | tuple[str, ...] | set[str]) -> None:
    actual = set(event_ids)
    expected = set(EVENT_IDS)
    if actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        raise ValueError(f"capacity/sequence event universe mismatch; missing={missing}; extra={extra}")


def annotation_for_event(event_family_id: str) -> dict:
    """Return a defensive copy of one controlled annotation pair."""
    try:
        return copy.deepcopy(EVENT_ANNOTATIONS[event_family_id])
    except KeyError as exc:
        raise KeyError(f"No capacity/sequence annotation for {event_family_id}") from exc


def apply_annotations(payload: dict) -> dict:
    """Apply annotations to every family without altering document records."""
    result = copy.deepcopy(payload)
    families = result.get("event_families", [])
    validate_controlled_event_ids([family.get("stable_id", "") for family in families])
    for family in families:
        family.update(annotation_for_event(family["stable_id"]))
    result["adverse_sequence_model"] = copy.deepcopy(ADVERSE_SEQUENCE_MODEL)
    result["capacity_sequence_annotation_control"] = {
        "schema_version": "1.0",
        "controlled_event_family_count": len(EVENT_IDS),
        "annotation_source": "scripts/acta_capacity_sequence_annotations.py",
        "fields": ["patricia_dominguez_capacity", "adverse_sequence_stage"],
    }
    return result


def check_annotations(payload: dict) -> list[str]:
    errors: list[str] = []
    families = payload.get("event_families", [])
    try:
        validate_controlled_event_ids([family.get("stable_id", "") for family in families])
    except ValueError as exc:
        errors.append(str(exc))
        return errors
    for family in families:
        event_id = family["stable_id"]
        expected = EVENT_ANNOTATIONS[event_id]
        for field, expected_value in expected.items():
            if family.get(field) != expected_value:
                errors.append(f"{event_id}: {field} differs from deterministic control")
    if payload.get("adverse_sequence_model") != ADVERSE_SEQUENCE_MODEL:
        errors.append("root adverse_sequence_model differs from deterministic control")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--continuity", type=Path, default=DEFAULT_CONTINUITY)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    path = args.continuity.resolve()
    payload = json.loads(path.read_text(encoding="utf-8"))
    if args.write:
        updated = apply_annotations(payload)
        path.write_text(json.dumps(updated, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Annotated {len(EVENT_IDS)} ACTA/meeting event families in {path.relative_to(REPO)}")
        return
    errors = check_annotations(payload)
    if errors:
        raise SystemExit("\n".join(f"ERROR: {error}" for error in errors))
    print(f"Capacity/sequence annotations verified for {len(EVENT_IDS)} event families")


if __name__ == "__main__":
    main()
