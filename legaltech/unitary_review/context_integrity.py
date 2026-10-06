"""Context/inference audit adjunct; no automatic truth, intent or guilt findings.

The caller supplies lawful source-text derivatives and review records. Hashes
bind those derivatives, not native-document authenticity or reviewer identity.
No network, source mutation, public export, or background execution is performed.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
import re
from collections import defaultdict, deque
from datetime import datetime
from pathlib import Path
from typing import Any

SCHEMA = 'pd.context-inference-review.v1'
CONTROL = 'PD-CONTEXT-INTEGRITY-20260924-01'
RULE_NAMES = (
    'selective_quotation', 'negation_or_qualifier_deletion',
    'question_answer_detachment', 'modal_or_conditional_flattening',
    'speech_act_or_pressure_erasure', 'translation_or_transcription_shift',
    'misleading_recontextualisation', 'true_premise_false_implication',
    'allegation_to_fact', 'presupposition_or_loaded_question',
    'equivocation_or_definition_switch', 'some_to_all_generalisation',
    'chronology_truncation', 'retrospective_knowledge',
    'cause_effect_reversal', 'correlation_or_benefit_as_causation',
    'absence_of_hit_as_nonexistence', 'silence_as_admission',
    'character_attack_instead_of_answer', 'judgment_scope_migration',
    'procedural_status_or_finality_inflation', 'approval_as_implementation',
    'party_recital_as_judicial_finding', 'institutional_as_personal_knowledge',
    'entity_or_capacity_substitution', 'narrow_denial_as_complete_answer',
    'strawman_or_false_binary', 'burden_shift_or_impossible_proof',
    'fragmentation_of_cumulative_evidence', 'circular_or_duplicate_corroboration',
    'association_or_motive_as_elements', 'financial_category_or_payer_conflation',
    'denominator_or_sample_selection', 'unsupported_numeric_precision',
    'visual_implication_or_crop', 'witness_variation_or_incentive_omission',
    'source_custody_as_substantive_verification', 'pipeline_state_as_completion',
    'double_counted_statement_and_composite', 'own_output_confirmation_loop',
)
RULES = {f'CI-{i:03d}': name for i, name in enumerate(RULE_NAMES, 1)}
AXES = ('actor', 'capacity', 'time', 'asset_or_object', 'proceeding',
        'issue', 'quantifier', 'procedural_posture')
RELATIONS = {'ACCURATE_LIMITED_USE', 'MATERIAL_CONTEXT_OMISSION',
             'MISLEADING_INFERENCE', 'SCOPE_MISMATCH', 'DIRECT_CONTRADICTION',
             'NARROWS', 'INCONCLUSIVE', 'NO_MATERIAL_DISTORTION'}

class IntegrityError(ValueError):
    """Malformed or unbound input; never an accusation about a person."""

def digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
        separators=(',', ':'), allow_nan=False).encode('utf-8')).hexdigest()

def text_digest(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())

def source_index(sources: list[dict]) -> dict[str, dict]:
    out = {}
    if not isinstance(sources, list):
        raise IntegrityError('sources must be a list')
    for source in sources:
        if not isinstance(source, dict) or not nonempty(source.get('id')):
            raise IntegrityError('source needs an ID')
        if source['id'] in out:
            raise IntegrityError('duplicate source ID')
        if not isinstance(source.get('text'), str):
            raise IntegrityError('source needs text derivative')
        if source.get('text_sha256') != text_digest(source['text']):
            raise IntegrityError('source text fingerprint mismatch')
        out[source['id']] = source
    return out

def anchor(index: dict[str, dict], ref: dict) -> bool:
    if not isinstance(ref, dict) or ref.get('source_id') not in index:
        raise IntegrityError('unknown source anchor')
    source = index[ref['source_id']]
    start, end = ref.get('start'), ref.get('end')
    if type(start) is not int or type(end) is not int:
        raise IntegrityError('offsets must be integer Unicode code-point offsets')
    if not 0 <= start < end <= len(source['text']):
        raise IntegrityError('invalid anchor interval')
    if ref.get('quote') != source['text'][start:end]:
        raise IntegrityError('quotation mismatch')
    if ref.get('source_text_sha256') != source['text_sha256']:
        raise IntegrityError('stale source anchor')
    return True

def review_fingerprint(review: dict, sources: list[dict]) -> str:
    """Review attestation binds the entire bounded source universe and record."""
    record = {k: v for k, v in review.items() if k != 'assessment'}
    return digest({'review': record, 'sources': sources})

def blank_review(review_id: str, target: dict, source_anchor: dict) -> dict:
    if not nonempty(review_id):
        raise IntegrityError('review ID required')
    return {'id': review_id, 'target': copy.deepcopy(target),
        'source_anchor': copy.deepcopy(source_anchor), 'use_anchor': None,
        'context_anchors': [], 'selected_rules': [],
        'inference_invited': '', 'restored_context_conclusion': '',
        'scope_comparison': {a: {'status': 'OPEN', 'reason': ''} for a in AXES},
        'strongest_lawful_alternative': '',
        'contrary_search': {'status': 'NOT_REVIEWED', 'scope': '',
                           'result': '', 'anchors': []},
        'lineage_review': '', 'cumulative_review': '',
        'knowledge_intent': {'status': 'OPEN', 'anchors': []},
        'actual_reliance_effect': {'status': 'OPEN', 'anchors': []},
        'legal_limits': '', 'assessment': None,
        'publication_authorized': False}

def from_forensic(case: dict) -> dict:
    """Create OPEN envelopes; retain IDs; never migrate an earlier verdict."""
    if not isinstance(case, dict) or case.get('schema') != 'pd.forensic.v1':
        raise IntegrityError('pd.forensic.v1 input required')
    document = case.get('document', {})
    if not nonempty(document.get('id')) or not re.fullmatch(
            r'[0-9a-fA-F]{64}', str(document.get('sha256', ''))):
        raise IntegrityError('document identity and recorded native SHA required')
    sources, blocks, reviews, seen = [], {}, [], set()
    for block in case.get('blocks', []):
        if not isinstance(block, dict) or not nonempty(block.get('id')):
            raise IntegrityError('block ID required')
        if block['id'] in blocks or type(block.get('page')) is not int or block['page'] < 1:
            raise IntegrityError('duplicate block or invalid page')
        if not isinstance(block.get('text'), str):
            raise IntegrityError('block text required')
        source = {'id': document['id'] + '::' + block['id'],
            'text': block['text'], 'text_sha256': text_digest(block['text']),
            'kind': 'PRESERVED_TEXT_DERIVATIVE',
            'recorded_native_sha256': document['sha256'],
            'root_origin': document['id'], 'page': block['page']}
        blocks[block['id']] = source
        sources.append(source)
    annotations = case.get('annotations')
    if not isinstance(annotations, list) or not blocks:
        raise IntegrityError('nonempty blocks and annotation list required')
    index = source_index(sources)
    for ann in annotations:
        if not isinstance(ann, dict) or not nonempty(ann.get('id')) or ann['id'] in seen:
            raise IntegrityError('invalid or duplicate annotation ID')
        seen.add(ann['id'])
        if ann.get('block') not in blocks:
            raise IntegrityError('annotation block absent')
        source = blocks[ann['block']]
        ref = {'source_id': source['id'], 'start': ann.get('start'),
               'end': ann.get('end'), 'quote': ann.get('quote'),
               'source_text_sha256': source['text_sha256']}
        anchor(index, ref)
        reviews.append(blank_review('CI:' + document['id'] + ':' + ann['id'],
            {'document_id': document['id'], 'annotation_id': ann['id'],
             'block_id': ann['block'], 'page': source['page'],
             'unit_level': 'LEGACY_LEVEL_REQUIRES_RECONCILIATION'}, ref))
    return {'schema': SCHEMA, 'control': CONTROL, 'sources': sources,
            'reviews': reviews, 'input_sha256': digest(case),
            'source_inputs_modified': False, 'automatic_assessment_promotion': False,
            'private_working_output': True}

def audit(package: dict) -> dict:
    if package.get('schema') != SCHEMA or not isinstance(package.get('reviews'), list):
        raise IntegrityError('context review package required')
    index = source_index(package['sources'])
    rows, seen = [], set()
    for review in package['reviews']:
        rid = review.get('id')
        if not nonempty(rid) or rid in seen:
            raise IntegrityError('duplicate or missing review ID')
        seen.add(rid)
        for forbidden in ('truth_score', 'guilt_score', 'lie_probability', 'credibility_score'):
            if review.get(forbidden) is not None:
                raise IntegrityError('unsupported truth, guilt or credibility score')
        anchor(index, review.get('source_anchor'))
        if review.get('use_anchor') is not None:
            anchor(index, review['use_anchor'])
        for field in ('context_anchors',):
            if not isinstance(review.get(field), list):
                raise IntegrityError('anchor collection required')
            for ref in review[field]:
                anchor(index, ref)
        contrary = review.get('contrary_search', {})
        for ref in contrary.get('anchors', []):
            anchor(index, ref)
        for field in ('knowledge_intent', 'actual_reliance_effect'):
            value = review.get(field, {})
            if value.get('status') not in {'OPEN', 'NOT_ASSESSED', 'SOURCE_REVIEW_RECORDED'}:
                raise IntegrityError('no automatic intent or effect findings')
            for ref in value.get('anchors', []):
                anchor(index, ref)
            if value.get('status') == 'SOURCE_REVIEW_RECORDED' and not value.get('anchors'):
                raise IntegrityError('separate intent/effect review needs source anchors')
        chosen = review.get('selected_rules', [])
        if not isinstance(chosen, list) or any(x not in RULES for x in chosen):
            raise IntegrityError('unknown rule ID')
        if len(chosen) != len(set(chosen)):
            raise IntegrityError('duplicate rule IDs do not increase evidence')
        scope = review.get('scope_comparison', {})
        checks = {
            'literal_text_anchor': True,
            'later_use_anchor': review.get('use_anchor') is not None,
            'material_context_bound': bool(review['context_anchors']),
            'invited_inference_identified': nonempty(review.get('inference_invited')),
            'restoration_test_recorded': nonempty(review.get('restored_context_conclusion')),
            'eight_scope_axes_recorded': all(scope.get(a, {}).get('status') in
                {'MATCH', 'DIFFERS', 'NOT_APPLICABLE'} and
                nonempty(scope[a].get('reason')) for a in AXES),
            'lawful_alternative_recorded': nonempty(review.get('strongest_lawful_alternative')),
            'contrary_search_recorded': contrary.get('status') in {'LOCATED', 'BOUNDED_NONE_LOCATED'}
                and nonempty(contrary.get('scope')) and nonempty(contrary.get('result'))
                and (contrary.get('status') != 'LOCATED' or bool(contrary.get('anchors'))),
            'lineage_review_recorded': nonempty(review.get('lineage_review')),
            'cumulative_review_recorded': nonempty(review.get('cumulative_review')),
            'legal_limits_recorded': nonempty(review.get('legal_limits')),
        }
        assessment = review.get('assessment')
        bound = False
        if assessment is not None:
            if not isinstance(assessment, dict) or assessment.get('relation') not in RELATIONS:
                raise IntegrityError('invalid supplied assessment')
            if assessment.get('kind') not in {'HUMAN_SOURCE_REVIEW', 'SYNTHETIC_EXPECTATION'}:
                raise IntegrityError('automatic merits promotion prohibited')
            if assessment.get('kind') == 'SYNTHETIC_EXPECTATION' and package.get('synthetic') is not True:
                raise IntegrityError('synthetic signoff cannot certify real input')
            try:
                stamp = datetime.fromisoformat(assessment['at_utc'].replace('Z', '+00:00'))
            except (KeyError, TypeError, ValueError, AttributeError) as exc:
                raise IntegrityError('review timestamp required') from exc
            if stamp.tzinfo is None or not nonempty(assessment.get('reviewer')):
                raise IntegrityError('attributed review and timezone required')
            bound = assessment.get('input_sha256') == review_fingerprint(review, package['sources'])
        checks['assessment_bound_to_inputs'] = bound
        ready = all(checks.values())
        rows.append({'review_id': rid, 'checks': checks,
            'documented_fields': sum(checks.values()), 'field_denominator': len(checks),
            'record_completeness_percent': round(100 * sum(checks.values()) / len(checks), 1),
            'record_state': 'COMPLETE_SUPPLIED_REVIEW_RECORD' if ready else 'OPEN_OR_STALE_REVIEW_RECORD',
            'recorded_relation': assessment['relation'] if ready else 'UNASSESSED',
            'reviewer_identity_authenticated': False,
            'truth_score': None, 'guilt_score': None,
            'publication_authorized_by_tool': False})
    return {'schema': SCHEMA + '.audit', 'control': CONTROL, 'rows': rows,
        'review_records': len(rows), 'complete_supplied_records': sum(
            r['record_state'] == 'COMPLETE_SUPPLIED_REVIEW_RECORD' for r in rows),
        'metric_boundary': 'Input-record completeness only; not evidential truth, human authenticity, corpus completeness, intent, guilt, or publication approval.',
        'package_sha256': digest(package), 'private_working_output': True}

def candidate_cues(text: str) -> list[dict]:
    """Bounded lexical hints only; no asserted detection of deception."""
    cues = {'CI-002': r'\.{3}|…', 'CI-004': r'\b(may|might|could|podr[ií]a|siempre que)\b',
            'CI-012': r'\b(all|every|never|always|todos|nunca|siempre)\b',
            'CI-019': r'\b(delirante|obsesivo|ret[oó]rica vac[ií]a)\b',
            'CI-021': r'\b(final|firme|archivado|dismissed)\b',
            'CI-034': r'\b\d+(?:\.\d+)?\s*%'}
    return [{'rule_id': rid, 'status': 'LEXICAL_CANDIDATE_ONLY',
             'start': m.start(), 'end': m.end(), 'matched_text': m.group()}
            for rid, pattern in cues.items() for m in re.finditer(pattern, text, re.I)]

def independence(sources: list[dict]) -> dict:
    source_index(sources)
    hashes, roots, unknown = defaultdict(list), defaultdict(list), []
    for source in sources:
        hashes[source['text_sha256']].append(source['id'])
        if nonempty(source.get('root_origin')):
            roots[source['root_origin']].append(source['id'])
        else:
            unknown.append(source['id'])
    return {'exact_text_duplicate_groups': [x for x in hashes.values() if len(x) > 1],
            'declared_origin_groups': dict(roots), 'unresolved_origin_ids': unknown,
            'independent_corroboration_established_by_tool': False}

def reopen_queue(records: list[dict], changed_ids: list[str], edges: list[dict]) -> list[dict]:
    """Edges run source/review -> dependent review. Return queue, not new verdicts."""
    ids = [r['id'] for r in records]
    if len(ids) != len(set(ids)):
        raise IntegrityError('duplicate review ID')
    graph = defaultdict(set)
    for edge in edges:
        if not nonempty(edge.get('from')) or edge.get('to') not in ids:
            raise IntegrityError('invalid dependency target')
        graph[edge['from']].add(edge['to'])
    visited, queue = set(), deque(changed_ids)
    while queue:
        item = queue.popleft()
        if item in visited:
            continue
        visited.add(item)
        queue.extend(sorted(graph[item] - visited))
    return [{'review_id': rid, 'action': 'REVIEW_REQUIRED_SOURCE_OR_DEPENDENCY_CHANGED',
             'prior_assessment_preserved': True} for rid in sorted(set(ids) & visited)]

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--from-forensic', action='store_true')
    ns = parser.parse_args()
    try:
        data = json.loads(ns.input.read_text(encoding='utf-8'))
        result = from_forensic(data) if ns.from_forensic else audit(data)
        # Exclusive creation prevents accidental overwrite of a prior review.
        with ns.out.open('x', encoding='utf-8') as handle:
            json.dump(result, handle, ensure_ascii=False, indent=2, allow_nan=False)
            handle.write('\n')
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(2, f'Context audit stopped: {exc}\n')

if __name__ == '__main__':
    main()
