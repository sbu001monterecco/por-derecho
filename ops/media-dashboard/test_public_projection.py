import copy
import json
import unittest
from public_projection import build_projection, RESOURCES


class ProjectionTests(unittest.TestCase):
    def setUp(self):
        self.cfg = dict(language='es', as_of='2026-09-05', resource_ids=list(RESOURCES),
                        release_approved=False, approval_record='')

    def test_preview_has_no_private_data_or_actions(self):
        out = build_projection(self.cfg, preview=True)
        self.assertEqual(out['mode'], 'preview_not_deployed')
        self.assertFalse(out['has_correspondence_data'])
        self.assertFalse(out['has_forms'])
        self.assertFalse(out['can_send_email'])
        self.assertNotIn('approval_record', out)

    def test_release_blocked_by_default(self):
        with self.assertRaises(ValueError): build_projection(self.cfg)

    def test_release_requires_record(self):
        self.cfg['release_approved'] = True
        with self.assertRaises(ValueError): build_projection(self.cfg)

    def test_release_assertion_is_not_deployment_proof(self):
        self.cfg.update(release_approved=True, approval_record='synthetic-approval')
        self.assertEqual(build_projection(self.cfg)['mode'], 'approved_projection_not_deployment_proof')

    def test_private_fields_rejected(self):
        for field in ('email', 'contacts', 'gmail_id', 'body', 'response', 'recipient_hash', 'campaign_metrics'):
            with self.subTest(field=field):
                cfg = copy.deepcopy(self.cfg); cfg[field] = 'editor@example.invalid'
                with self.assertRaises(ValueError): build_projection(cfg, preview=True)

    def test_external_private_url_rejected(self):
        self.cfg['resource_ids'].append('https://mail.google.com/mail/#all/synthetic')
        with self.assertRaises(ValueError): build_projection(self.cfg, preview=True)

    def test_unknown_source_rejected(self):
        self.cfg['resource_ids'].append('not_reviewed')
        with self.assertRaises(ValueError): build_projection(self.cfg, preview=True)

    def test_no_duplicate_sources(self):
        self.cfg['resource_ids'].append('website_es')
        with self.assertRaises(ValueError): build_projection(self.cfg, preview=True)

    def test_required_body_entry_resources(self):
        for field in ('website_es', 'sunpark_ricpe', 'court_authority_context', 'institutional_records'):
            with self.subTest(field=field):
                cfg = copy.deepcopy(self.cfg); cfg['resource_ids'].remove(field)
                with self.assertRaises(ValueError): build_projection(cfg, preview=True)

    def test_invalid_date(self):
        self.cfg['as_of'] = '2026-02-30'
        with self.assertRaises(ValueError): build_projection(self.cfg, preview=True)

    def test_invalid_language(self):
        self.cfg['language'] = 'xx'
        with self.assertRaises(ValueError): build_projection(self.cfg, preview=True)

    def test_string_approval_is_not_boolean(self):
        self.cfg['release_approved'] = 'true'
        with self.assertRaises(ValueError): build_projection(self.cfg, preview=True)

    def test_english_preserves_spanish_source_language(self):
        self.cfg['language'] = 'en'
        out = build_projection(self.cfg, preview=True)
        self.assertEqual(next(r for r in out['resources'] if r['id']=='sunpark_ricpe')['source_language'],'es')

    def test_approval_record_not_exported(self):
        self.cfg.update(release_approved=True, approval_record='private-review-reference')
        self.assertNotIn('private-review-reference', json.dumps(build_projection(self.cfg)))

    def test_input_not_mutated(self):
        original = copy.deepcopy(self.cfg)
        build_projection(self.cfg, preview=True)
        self.assertEqual(original, self.cfg)


if __name__ == '__main__': unittest.main()
