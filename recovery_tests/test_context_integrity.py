"""Synthetic regression fixtures only; no case facts or actual reviewer signoff."""
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from legaltech.unitary_review import context_integrity as ci


def source(sid, text, root='DEMO'):
    return {'id': sid, 'text': text, 'text_sha256': ci.text_digest(text),
            'root_origin': root, 'kind': 'SYNTHETIC'}


def span(s, text=None):
    text = s['text'] if text is None else text
    start = s['text'].index(text)
    return {'source_id': s['id'], 'start': start, 'end': start + len(text),
            'quote': text, 'source_text_sha256': s['text_sha256']}


def fixture():
    s = source('S1', 'I said I felt fine because I feared another intervention.')
    u = source('S2', 'The words I felt fine prove there was no injury.')
    r = ci.blank_review('R1', {'document_id': 'SYNTHETIC'}, span(s, 'I felt fine'))
    return {'schema': ci.SCHEMA, 'synthetic': True, 'sources': [s, u], 'reviews': [r]}


def completed():
    p = fixture()
    r = p['reviews'][0]
    r.update(use_anchor=span(p['sources'][1]), context_anchors=[span(p['sources'][0])],
        selected_rules=['CI-005', 'CI-008'],
        inference_invited='The later argument treats the words as proof of no injury.',
        restored_context_conclusion='The fear explanation defeats that inference in this invented example; injury itself still needs evidence.',
        strongest_lawful_alternative='The later author may not have had the complete statement.',
        lineage_review='One invented story; two statements are not two independent origins.',
        cumulative_review='Read the utterance and the stated fear together.',
        legal_limits='Synthetic method test; no real offence, intent, reliance or duty determination.')
    r['scope_comparison'] = {a: {'status': 'MATCH', 'reason': 'Same synthetic scope.'} for a in ci.AXES}
    r['contrary_search'] = {'status': 'BOUNDED_NONE_LOCATED', 'scope': 'Two synthetic passages only.',
                           'result': 'No other material provided; not an exhaustive search.', 'anchors': []}
    r['assessment'] = {'kind': 'SYNTHETIC_EXPECTATION', 'reviewer': 'TEST_FIXTURE_NOT_A_PERSON',
        'at_utc': '2026-09-24T00:00:00Z', 'relation': 'MISLEADING_INFERENCE',
        'input_sha256': ci.review_fingerprint(r, p['sources'])}
    return p


class ContextIntegrityTests(unittest.TestCase):
    def test_01_open_is_not_false(self):
        row = ci.audit(fixture())['rows'][0]
        self.assertEqual(row['recorded_relation'], 'UNASSESSED')
        self.assertIsNone(row['truth_score'])
        self.assertIsNone(row['guilt_score'])

    def test_02_quote_true_does_not_certify_underlying_claim(self):
        row = ci.audit(fixture())['rows'][0]
        self.assertEqual(row['documented_fields'], 1)
        self.assertEqual(row['field_denominator'], 12)
        self.assertFalse(row['publication_authorized_by_tool'])

    def test_03_completed_synthetic_record_not_real_verdict(self):
        p = completed()
        before = ci.digest(p)
        row = ci.audit(p)['rows'][0]
        self.assertEqual(row['recorded_relation'], 'MISLEADING_INFERENCE')
        self.assertEqual(row['record_completeness_percent'], 100)
        self.assertFalse(row['reviewer_identity_authenticated'])
        self.assertEqual(ci.digest(p), before)

    def test_04_benign_use_is_admissible_review_outcome(self):
        p = completed()
        p['reviews'][0]['assessment']['relation'] = 'NO_MATERIAL_DISTORTION'
        self.assertEqual(ci.audit(p)['rows'][0]['recorded_relation'], 'NO_MATERIAL_DISTORTION')

    def test_05_context_change_stales_assessment(self):
        p = completed()
        p['reviews'][0]['restored_context_conclusion'] += ' Revised.'
        self.assertEqual(ci.audit(p)['rows'][0]['recorded_relation'], 'UNASSESSED')

    def test_06_quotation_mismatch_fails(self):
        p = fixture()
        p['reviews'][0]['source_anchor']['quote'] = 'I never felt fine'
        with self.assertRaises(ci.IntegrityError): ci.audit(p)

    def test_07_stale_hash_fails(self):
        p = fixture()
        p['reviews'][0]['source_anchor']['source_text_sha256'] = '0' * 64
        with self.assertRaises(ci.IntegrityError): ci.audit(p)

    def test_08_invalid_offsets_fail(self):
        for value in (-1, True, 1.5, '1'):
            p = fixture()
            p['reviews'][0]['source_anchor']['start'] = value
            with self.subTest(value=value), self.assertRaises(ci.IntegrityError): ci.audit(p)

    def test_09_duplicate_source_ids_fail(self):
        p = fixture(); p['sources'].append(p['sources'][0])
        with self.assertRaises(ci.IntegrityError): ci.audit(p)

    def test_10_duplicate_review_ids_fail(self):
        p = fixture(); p['reviews'].append(p['reviews'][0])
        with self.assertRaises(ci.IntegrityError): ci.audit(p)

    def test_11_changed_source_bytes_fail(self):
        p = fixture(); p['sources'][0]['text'] += '!'
        with self.assertRaises(ci.IntegrityError): ci.audit(p)

    def test_12_unknown_rule_fails(self):
        p = fixture(); p['reviews'][0]['selected_rules'] = ['CI-999']
        with self.assertRaises(ci.IntegrityError): ci.audit(p)

    def test_13_duplicate_rules_do_not_count_as_evidence(self):
        p = fixture(); p['reviews'][0]['selected_rules'] = ['CI-001', 'CI-001']
        with self.assertRaises(ci.IntegrityError): ci.audit(p)

    def test_14_synthetic_signoff_on_real_input_fails(self):
        p = completed(); p['synthetic'] = False
        with self.assertRaises(ci.IntegrityError): ci.audit(p)

    def test_15_automatic_assessment_fails(self):
        p = completed(); p['reviews'][0]['assessment']['kind'] = 'AI_AUTOMATIC'
        with self.assertRaises(ci.IntegrityError): ci.audit(p)

    def test_16_intent_cannot_be_inferred_from_context(self):
        p = completed(); p['reviews'][0]['knowledge_intent']['status'] = 'GUILTY'
        with self.assertRaises(ci.IntegrityError): ci.audit(p)

    def test_17_effect_review_requires_separate_sources(self):
        p = fixture(); p['reviews'][0]['actual_reliance_effect']['status'] = 'SOURCE_REVIEW_RECORDED'
        with self.assertRaises(ci.IntegrityError): ci.audit(p)

    def test_18_absent_alternative_keeps_record_open(self):
        p = completed(); p['reviews'][0]['strongest_lawful_alternative'] = ''
        p['reviews'][0]['assessment']['input_sha256'] = ci.review_fingerprint(p['reviews'][0], p['sources'])
        self.assertEqual(ci.audit(p)['rows'][0]['recorded_relation'], 'UNASSESSED')

    def test_19_contrary_located_requires_anchor(self):
        p = completed(); p['reviews'][0]['contrary_search']['status'] = 'LOCATED'
        p['reviews'][0]['assessment']['input_sha256'] = ci.review_fingerprint(p['reviews'][0], p['sources'])
        self.assertEqual(ci.audit(p)['rows'][0]['recorded_relation'], 'UNASSESSED')

    def test_20_scope_not_applicable_requires_reason(self):
        p = completed(); p['reviews'][0]['scope_comparison']['time'] = {'status': 'NOT_APPLICABLE', 'reason': ''}
        self.assertFalse(ci.audit(p)['rows'][0]['checks']['eight_scope_axes_recorded'])

    def test_21_unknown_origins_not_independent(self):
        s = [source('S1', 'a', ''), source('S2', 'b', '')]
        out = ci.independence(s)
        self.assertEqual(len(out['unresolved_origin_ids']), 2)
        self.assertFalse(out['independent_corroboration_established_by_tool'])

    def test_22_host_copies_are_duplicates(self):
        s = [source('GH', 'same', 'R33'), source('GL', 'same', 'R33')]
        out = ci.independence(s)
        self.assertEqual(out['exact_text_duplicate_groups'], [['GH', 'GL']])
        self.assertEqual(len(out['declared_origin_groups']), 1)

    def test_23_lexical_cues_are_candidates_only(self):
        cues = ci.candidate_cues('All may be final ... 77%')
        self.assertTrue(cues)
        self.assertTrue(all(c['status'] == 'LEXICAL_CANDIDATE_ONLY' for c in cues))
        self.assertTrue(all('score' not in c for c in cues))

    def test_24_no_cues_is_not_true(self):
        self.assertEqual(ci.candidate_cues('An ordinary sentence.'), [])
        self.assertEqual(ci.audit(fixture())['rows'][0]['recorded_relation'], 'UNASSESSED')

    def test_25_reopening_traverses_cycles_preserves_records(self):
        records = [{'id': 'A', 'assessment': 'old'}, {'id': 'B', 'assessment': 'old'}]
        before = copy.deepcopy(records)
        out = ci.reopen_queue(records, ['S'], [{'from': 'S', 'to': 'A'}, {'from': 'A', 'to': 'B'}, {'from': 'B', 'to': 'A'}])
        self.assertEqual([r['review_id'] for r in out], ['A', 'B'])
        self.assertEqual(records, before)
        self.assertEqual(ci.reopen_queue(records, ['X'], []), [])

    def test_26_unknown_dependency_target_fails(self):
        with self.assertRaises(ci.IntegrityError):
            ci.reopen_queue([{'id': 'A'}], ['S'], [{'from': 'S', 'to': 'missing'}])

    def test_27_forensic_adapter_preserves_ids_and_unicode(self):
        text = 'Sí: se recibió, pero no fue examinado.'
        c = {'schema': 'pd.forensic.v1', 'document': {'id': 'DOC', 'sha256': '0' * 64},
             'blocks': [{'id': 'B1', 'page': 1, 'text': text}],
             'annotations': [{'id': 'A1', 'block': 'B1', 'start': 0, 'end': len(text), 'quote': text}]}
        before = ci.digest(c)
        p = ci.from_forensic(c)
        self.assertEqual(p['reviews'][0]['target']['annotation_id'], 'A1')
        self.assertEqual(ci.digest(c), before)
        self.assertEqual(ci.audit(p)['complete_supplied_records'], 0)
        c['annotations'].append(c['annotations'][0])
        with self.assertRaises(ci.IntegrityError): ci.from_forensic(c)

    def test_28_catalogue_stable_and_complete(self):
        self.assertEqual(len(ci.RULES), 40)
        self.assertEqual(ci.RULES['CI-008'], 'true_premise_false_implication')
        self.assertEqual(len(set(ci.RULES.values())), 40)

    def test_29_empty_denominator_no_truth_percentage(self):
        result = ci.audit({'schema': ci.SCHEMA, 'sources': [], 'reviews': []})
        self.assertEqual(result['review_records'], 0)
        self.assertNotIn('overall_score', result)

    def test_30_cli_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            source_file, output = Path(d) / 'in.json', Path(d) / 'out.json'
            source_file.write_text(json.dumps(fixture()), encoding='utf-8')
            args = [sys.executable, '-m', 'legaltech.unitary_review.context_integrity', str(source_file), '--out', str(output)]
            self.assertEqual(subprocess.run(args, capture_output=True).returncode, 0)
            before = output.read_bytes()
            self.assertNotEqual(subprocess.run(args, capture_output=True).returncode, 0)
            self.assertEqual(output.read_bytes(), before)

    def test_31_numeric_truth_scores_rejected(self):
        for key in ('truth_score', 'guilt_score', 'lie_probability', 'credibility_score'):
            p = completed(); p['reviews'][0][key] = 75
            with self.subTest(key=key), self.assertRaises(ci.IntegrityError): ci.audit(p)

    def test_32_document_catalogue_matches_code(self):
        root = Path(__file__).resolve().parents[1]
        doc = (root / 'governance/CONTEXT_INTEGRITY_TRUTH_INVERSION_24SEP2026.md').read_text(encoding='utf-8')
        for rid in ci.RULES:
            self.assertEqual(doc.count('| ' + rid + ' |'), 1)

if __name__ == '__main__':
    unittest.main()
