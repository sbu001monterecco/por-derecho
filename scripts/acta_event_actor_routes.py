#!/usr/bin/env python3
"""Controlled event-specific actor/entity routes for ACTA lineage pages."""

from __future__ import annotations

import copy


ACTOR_ROUTE_CATALOG = {
    "MONTELANZA": {
        "canonical_name": "Montelanza / Monte Lanza, S.L.",
        "label": {"es": "Montelanza / Monte Lanza", "en": "Montelanza / Monte Lanza"},
        "routes": {
            "es": "es/montelanza-monte-lanza-sl/",
            "en": "en/montelanza-monte-lanza-sl/",
        },
    },
    "AWESWELL": {
        "canonical_name": "Aweswell Limited",
        "label": {"es": "Aweswell Limited", "en": "Aweswell Limited"},
        "routes": {"es": "es/aweswell-limited/", "en": "en/aweswell-limited/"},
    },
    "LPB": {
        "canonical_name": "Lanzarote Business Park, S.L. (LPB)",
        "label": {
            "es": "Lanzarote Business Park, S.L. (LPB)",
            "en": "Lanzarote Business Park, S.L. (LPB)",
        },
        "routes": {"es": "es/insolvencia-lpb/", "en": "en/lpb-insolvency/"},
    },
    "GIL_MARER": {
        "canonical_name": "Gil Marer",
        "label": {"es": "Gil Marer", "en": "Gil Marer"},
        "routes": {
            "es": "es/actores-partes-abogados-representantes/",
            "en": "en/actors-parties-lawyers-representatives/",
        },
    },
    "PATRICIA_DOMINGUEZ": {
        "canonical_name": "Patricia Isabel Domínguez Montelongo",
        "label": {
            "es": "Patricia Isabel Domínguez Montelongo",
            "en": "Patricia Isabel Domínguez Montelongo",
        },
        "routes": {
            "es": "es/actores-partes-abogados-representantes/",
            "en": "en/actors-parties-lawyers-representatives/",
        },
    },
    "URI_OMID": {
        "canonical_name": "Uri Omid",
        "label": {"es": "Uri Omid", "en": "Uri Omid"},
        "routes": {
            "es": "es/actores-partes-abogados-representantes/",
            "en": "en/actors-parties-lawyers-representatives/",
        },
    },
    "AAS": {
        "canonical_name": "Asunción Aizpurúa Sánchez",
        "label": {"es": "Asunción Aizpurúa Sánchez", "en": "Asunción Aizpurúa Sánchez"},
        "routes": {
            "es": "es/asuncion-aizpurua-sanchez/",
            "en": "en/asuncion-aizpurua-sanchez/",
        },
    },
    "FMMM": {
        "canonical_name": "Francisco Mario Matos Matas",
        "label": {"es": "Francisco Mario Matos Matas", "en": "Francisco Mario Matos Matas"},
        "routes": {
            "es": "es/francisco-mario-matos-matas/",
            "en": "en/francisco-mario-matos-matas/",
        },
    },
    "ANTONIO_COGOLLUDO_ROJAS": {
        "canonical_name": "Antonio Cogolludo Rojas",
        "label": {"es": "Antonio Cogolludo Rojas", "en": "Antonio Cogolludo Rojas"},
        "routes": {
            "es": "es/antonio-cogolludo-rojas/",
            "en": "en/antonio-cogolludo-rojas/",
        },
    },
    "SHAILA_MARIA_COGOLLUDO_RAMOS": {
        "canonical_name": "Shaila María Cogolludo Ramos",
        "label": {"es": "Shaila María Cogolludo Ramos", "en": "Shaila María Cogolludo Ramos"},
        "routes": {
            "es": "es/shaila-maria-cogolludo-ramos/",
            "en": "en/shaila-maria-cogolludo-ramos/",
        },
    },
    "PAMANIL": {
        "canonical_name": "Pamanil, S.L.",
        "label": {"es": "Pamanil, S.L.", "en": "Pamanil, S.L."},
        "routes": {"es": "es/pamanil-sl/", "en": "en/pamanil-sl/"},
    },
    "ACOSTA_MATOS_PERIMETER": {
        "canonical_name": "Acosta Matos / CAM documentary perimeter",
        "label": {"es": "Perímetro Acosta Matos / CAM", "en": "Acosta Matos / CAM perimeter"},
        "routes": {
            "es": "es/acosta-matos-perimetro/",
            "en": "en/acosta-matos-perimeter/",
        },
    },
    "PAMALEXSHA": {
        "canonical_name": "Pamalexsha Servicios Integrales, S.L.",
        "label": {"es": "Pamalexsha Servicios Integrales, S.L.", "en": "Pamalexsha Servicios Integrales, S.L."},
        "routes": {
            "es": "es/pamalexsha-servicios-integrales-sl/",
            "en": "en/pamalexsha-servicios-integrales-sl/",
        },
    },
    "JOSE_DANIEL_ACOSTA_MATOS": {
        "canonical_name": "José Daniel Acosta Matos",
        "label": {"es": "José Daniel Acosta Matos", "en": "José Daniel Acosta Matos"},
        "routes": {
            "es": "es/actores-partes-abogados-representantes/",
            "en": "en/actors-parties-lawyers-representatives/",
        },
    },
    "OWNERS_COMMUNITY": {
        "canonical_name": "Comunidad de Propietarios Sun Park",
        "label": {
            "es": "Comunidad de Propietarios Sun Park",
            "en": "Sun Park Owners' Community",
        },
        "routes": {
            "es": "es/comunidad-instrumentalizacion/",
            "en": "en/community-instrumentalisation/",
        },
    },
    "RICPE": {
        "canonical_name": "RIC Private Equity Investment Partners S.C.R., S.A. (RICPE)",
        "label": {
            "es": "RIC Private Equity Investment Partners S.C.R., S.A. (RICPE)",
            "en": "RIC Private Equity Investment Partners S.C.R., S.A. (RICPE)",
        },
        "routes": {
            "es": "es/ric-private-equity-sun-park/",
            "en": "en/ric-private-equity-sun-park/",
        },
    },
}


# Values are (actor/entity key, event-specific relationship status). A route
# records a documented participant/office/entity or a clearly labelled project
# succession/context page; it never supplies a mandate by inference.
EVENT_ACTOR_ROUTE_ROWS = {
    "SP-ACTA-2008-04-29": [("MONTELANZA", "documented-pre-sale-entity-context")],
    "SP-ACTA-2008-07-15": [],
    "SP-ACTA-2008-07-15-CEXP": [
        ("MONTELANZA", "documented-participating-entity"),
        ("LPB", "documented-participating-entity"),
        ("URI_OMID", "documented-elected-chair"),
        ("AWESWELL", "later-project-succession-context"),
    ],
    "SP-ACTA-2008-07-25": [
        ("LPB", "documented-participating-entity"),
        ("AWESWELL", "later-project-succession-context"),
    ],
    "SP-ACTA-2008-12-17": [],
    "SP-ACTA-2009-05-28": [
        ("LPB", "documented-chair-entity"),
        ("AWESWELL", "later-project-succession-context"),
    ],
    "SP-ACTA-2011-02-02": [("AAS", "documented-officeholder-election")],
    "SP-ACTA-2011-06-22": [
        ("AAS", "documented-chair"),
        ("FMMM", "documented-administrator"),
        ("PAMANIL", "documented-proposal-or-service-context"),
    ],
    "SP-ACTA-2012-08-10": [
        ("LPB", "documented-signatory-or-chair-entity"),
        ("GIL_MARER", "documented-signatory-or-chair-representative"),
        ("PATRICIA_DOMINGUEZ", "documented-Spanish-statement-reader-only"),
        ("AWESWELL", "project-succession-context"),
        ("AAS", "documented-objecting-participant"),
    ],
    "SP-ACTA-2014-04-10": [
        ("LPB", "documented-convener-entity"),
        ("GIL_MARER", "documented-LPB-representative"),
        ("AWESWELL", "project-succession-context"),
        ("ANTONIO_COGOLLUDO_ROJAS", "documented-participant-or-representative"),
        ("PAMANIL", "documented-competing-governance-context"),
    ],
    "SP-ACTA-2014-08-28-CP": [
        ("LPB", "documented-chair-entity"),
        ("GIL_MARER", "documented-LPB-representative"),
        ("AWESWELL", "project-succession-context"),
        ("PAMANIL", "documented-competing-authority-context"),
    ],
    "SP-ACTA-2014-08-28-CEXP": [
        ("LPB", "documented-project-entity-context"),
        ("AWESWELL", "project-succession-context"),
    ],
    "SP-ACTA-2015-11-19": [
        ("AAS", "documented-chair"),
        ("FMMM", "documented-administrator"),
        ("PAMANIL", "documented-community-service-context"),
    ],
    "SP-ACTA-2016-04-26": [
        ("LPB", "documented-represented-owner-entity"),
        ("PATRICIA_DOMINGUEZ", "documented-LPB-representative"),
        ("AAS", "documented-chair"),
        ("FMMM", "documented-administrator"),
        ("PAMANIL", "documented-community-service-context"),
    ],
    "SP-MEETING-2016-06-10": [("FMMM", "recorded-or-referenced-capacity-open")],
    "SP-ACTA-2017-04-07-CEXP": [
        ("LPB", "documented-project-entity-context"),
        ("AWESWELL", "project-succession-context"),
    ],
    "SP-ACTA-2017-06-12": [
        ("FMMM", "documented-officeholder-continuity-context"),
        ("PAMANIL", "documented-community-service-context"),
    ],
    "SP-ACTA-2018-05-18": [
        ("ANTONIO_COGOLLUDO_ROJAS", "documented-officeholder-or-participant"),
        ("SHAILA_MARIA_COGOLLUDO_RAMOS", "documented-officeholder-or-participant"),
        ("PAMANIL", "documented-officeholder-continuity-context"),
        ("ACOSTA_MATOS_PERIMETER", "documented-CAM-transition-context"),
    ],
    "SP-ACTA-2018-07-05": [
        ("SHAILA_MARIA_COGOLLUDO_RAMOS", "documented-officeholder-or-participant"),
        ("ACOSTA_MATOS_PERIMETER", "documented-CAM-and-Acosta-Matos-context"),
    ],
    "SP-RECITAL-2018-11-20": [
        ("ACOSTA_MATOS_PERIMETER", "later-recital-context-only")
    ],
    "SP-RECITAL-2021-12-29-RICPE": [
        ("RICPE", "later-recital-of-corporate-event-only")
    ],
    "SP-ACTA-2022-02-04": [
        ("OWNERS_COMMUNITY", "documented-meeting-body"),
        ("JOSE_DANIEL_ACOSTA_MATOS", "documented-intervening-person"),
        ("ACOSTA_MATOS_PERIMETER", "documented-CAM-and-Acosta-Matos-context"),
        ("PAMALEXSHA", "documented-administration-context"),
    ],
    "SP-MEETING-2022-03-11-RICPE": [
        ("RICPE", "documented-notice-issuer-and-scheduled-meeting-body")
    ],
}


EVENT_ACTOR_ROUTE_GAP_ROWS = {
    "SP-ACTA-2008-07-15": [{
        "subject_code": "REDACTED_OFFICEHOLDERS",
        "reason": {
            "es": "La edición pública reserva los nombres de presidencia accidental y secretaría-administración; no se inventa una ruta individual.",
            "en": "The public edition withholds the acting chair and secretary-administrator names; no individual route is invented.",
        },
    }],
    "SP-ACTA-2008-07-25": [{
        "subject_code": "MULTIMATRIX",
        "reason": {
            "es": "Multimatrix consta en la fase documental, pero no existe una página bilingüe individual controlada; el registro del evento conserva el contexto sin inventar una ruta.",
            "en": "Multimatrix is recorded in the documentary phase, but no controlled individual bilingual page exists; the event record preserves the context without inventing a route.",
        },
    }],
    "SP-ACTA-2008-12-17": [{
        "subject_code": "REDACTED_OFFICEHOLDERS",
        "reason": {
            "es": "La copia pública expurga los nombres de presidencia y secretaría accidental y no se ha unido la convocatoria; no se inventa una ruta individual.",
            "en": "The public copy redacts the chair and acting secretary names and the notice remains unjoined; no individual route is invented.",
        },
    }],
    "SP-ACTA-2009-05-28": [{
        "subject_code": "MULTIMATRIX",
        "reason": {
            "es": "Multimatrix forma parte de la fase documental, pero no existe una página bilingüe individual controlada; se enlaza LPB y se conserva esta carencia expresamente.",
            "en": "Multimatrix forms part of the documentary phase, but no controlled individual bilingual page exists; LPB is linked and this route gap is preserved expressly.",
        },
    }],
}


ROUTE_INFERENCE_BOUNDARY = {
    "es": (
        "El enlace indica una relación documental específica del evento o una sucesión/contexto "
        "expresamente rotulado. No prueba por sí solo mandato, convocatoria, control, actuación "
        "conjunta, validez o culpabilidad."
    ),
    "en": (
        "The link identifies an event-specific documentary relationship or an expressly labelled "
        "succession/context route. It does not by itself prove mandate, convocation, control, joint "
        "conduct, validity or guilt."
    ),
}


def actor_routes_for_event(event_family_id: str) -> list[dict]:
    try:
        rows = EVENT_ACTOR_ROUTE_ROWS[event_family_id]
    except KeyError as exc:
        raise KeyError(f"No actor/entity route control for {event_family_id}") from exc
    result = []
    for actor_key, status in rows:
        item = copy.deepcopy(ACTOR_ROUTE_CATALOG[actor_key])
        item["actor_key"] = actor_key
        item["relationship_status_code"] = status
        item["inference_boundary"] = copy.deepcopy(ROUTE_INFERENCE_BOUNDARY)
        result.append(item)
    return result


def actor_route_gaps_for_event(event_family_id: str) -> list[dict]:
    if event_family_id not in EVENT_ACTOR_ROUTE_ROWS:
        raise KeyError(f"No actor/entity route control for {event_family_id}")
    return copy.deepcopy(EVENT_ACTOR_ROUTE_GAP_ROWS.get(event_family_id, []))
