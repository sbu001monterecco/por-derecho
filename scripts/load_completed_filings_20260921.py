#!/usr/bin/env python3
"""Load reviewed filing descriptors into the canonical event generator.

The input fixes identities after a repository-wide reservation search. It is
not a second event register and contains no native receipt or private locator.
"""
from copy import deepcopy
import hashlib
import json
from pathlib import Path

INPUT = 'ops/dp1901-eg745-registration-input-20260921.json'
CAJASIETE_INPUT = 'ops/cajasiete-accountability-register-input-20260918.json'
CONTROL = 'PD-DP1901-EG745-REGISTERED-20260921'


def load_existing_cajasiete_events(root: Path) -> list[dict]:
    """Reproduce the two existing rows exactly; no new Cajasiete assertion."""
    data = json.loads((root / CAJASIETE_INPUT).read_text())
    rows = data['canonical_event_rows']
    if [row['event_id'] for row in rows] != ['PD-SP-EVT-0179', 'PD-SP-EVT-0180']:
        raise ValueError('Existing Cajasiete identity preservation drift')
    return deepcopy(rows)


def load_completed_filing_events(root: Path, receipt_boundary: dict) -> list[dict]:
    raw = (root / INPUT).read_bytes()
    data = json.loads(raw)
    items = data['items']
    if len(items) != 24 or len({i['event_id'] for i in items}) != 24 or len({i['reference'] for i in items}) != 24:
        raise ValueError('Completed-filing cohort requires 24 distinct registration events')
    if sum(i['key'].startswith('DP1901-') for i in items) != 14 or sum(i['key'].startswith('EG745-') for i in items) != 10:
        raise ValueError('DP1901 / EG745 denominator mismatch')
    if any(191 <= int(i['event_id'][-4:]) <= 198 for i in items):
        raise ValueError('Orion/Martin event identities are reserved')
    rows = []
    for i in items:
        is_eg = i['key'].startswith('EG745-')
        en = f"Registered {i['reference']}: {i['purpose_en']}"
        es = f"Registrado {i['reference']}: {i['purpose_es']}"
        e = {
            'event_id': i['event_id'], 'cohort': 'CURATED_SOURCE_PROVED_EVENT',
            'layer': 'FORMAL_REGISTRATION', 'source_key': f"REGISTERED-20260921:{i['reference']}",
            'record_type': 'REGISTRATION_RECEIPT', 'event_date': i['date'],
            'direction': 'OUTBOUND_TO_INSTITUTION', 'channel': i['channel'],
            'office': i['office'], 'official_reference': i['reference'],
            'presented_local': i['presented_literal'],
            'source_timezone': 'NOT_STATED; receipt time preserved literally without conversion',
            'matter_references': i['matter_references'], 'source_batch_id': CONTROL,
            'source_integrity': {
                'status': 'RECEIPT_VERIFIED_PUBLIC_SAFE_DERIVATIVE',
                'repository_anchor': i['source_anchor'],
                'reviewed_input': INPUT, 'reviewed_input_sha256': hashlib.sha256(raw).hexdigest(),
            },
            'evidence_state': deepcopy(receipt_boundary),
            'public_summary': en, 'public_summary_es': es,
            'proves': [en, 'The receipt records presentation to the stated registry destination.'],
            'proves_es': [es, 'El justificante registra la presentación al destino registral indicado.'],
            'does_not_prove': [i['limit_en'], 'Registration does not establish downstream delivery, admission, incorporation, substantive examination, criminal responsibility or the merits of allegations.'],
            'does_not_prove_es': [i['limit_es'], 'El registro no acredita entrega ulterior, admisión, incorporación, examen sustantivo, responsabilidad penal ni el fondo de las alegaciones.'],
            'canonical_anchor_en': f"en/institutional-records/#communication-{i['event_id']}",
            'canonical_anchor_es': f"es/registros-institucionales/#communication-{i['event_id']}",
            'related_route_en': 'en/public-prosecution-inspection-exp-gub-745-2026/#filing-completion-20260921' if is_eg else 'en/dp-1901-2026/',
            'related_route_es': 'es/fiscalia-inspeccion-exp-gub-745-2026/#filing-completion-20260921' if is_eg else 'es/dp-1901-2026/',
            'attribution_state': 'NO_PERSON_ATTRIBUTED_IN_PUBLIC_REGISTER',
            'linked_transport_event_ids': [],
            'transport_link_state': 'REGISTRATION_RECEIPT_SEPARATE_FROM_ANY_EMAIL_TRANSPORT',
            'proof_level': 'REGISTRATION_RECEIPT_VERIFIED',
            'criminal_responsibility_transfer': False,
            'public_derivative_state': 'PUBLIC_SAFE_MINIMISED_DERIVATIVE',
        }
        for source, target in [('dir3', 'recipient_dir3'), ('registered_literal', 'registration_datetime_literal'), ('attachment_count', 'annex_count'), ('attachment_pages', 'attachment_pages'), ('linked_principal_registration', 'linked_principal_registration'), ('prior_rejected_reference', 'prior_rejected_reference'), ('submission_number', 'submission_number')]:
            if source in i:
                e[target] = i[source]
        if i.get('receipt_sha256'):
            e['source_integrity']['controlling_source_pdf_sha256'] = i['receipt_sha256']
        if i.get('attachment_hashes_verified'):
            e['proves'].append('The listed attachment fingerprints match the retained submitted files.')
            e['proves_es'].append('Las huellas de los anexos indicados coinciden con los archivos presentados conservados.')
            e['proof_level'] = 'REGISTRATION_RECEIPT_AND_ATTACHMENT_HASHES_VERIFIED'
        rows.append(e)
    return rows
