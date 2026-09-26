"""Synthetic fixtures only: no private court content or source files."""
import io
from contextlib import redirect_stdout
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch
PATH=Path(__file__).resolve().parents[1]/'scripts'/'validate_meeting_point_prefiling_controls.py'
# The private audit bundle colocates scripts; repository execution uses scripts/.
if not PATH.is_file():
    PATH=Path(__file__).with_name('validate_meeting_point_prefiling_controls.py')
if not PATH.is_file():
    raise FileNotFoundError(f'Meeting Point validator script not found: {PATH}')
spec=importlib.util.spec_from_file_location('controls',PATH)
if spec is None or spec.loader is None:
    raise ImportError(f'Cannot load Meeting Point validator script: {PATH}')
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class ControlTests(unittest.TestCase):
    def setUp(self):
        self.a=' '.join(x for row in v.CORE.values() for x in row)+' Documento 2 histórico 38bis 38ter en estudio NewCo condiciones SHA-256'
        self.b='Documento 1 histórico no constituye'
        self.m={'schema':1,'profile':v.PROFILE,'versions':[13,7],'puzzle_pages':[27,28,29],
                'sources':[{'id':x} for x in ['prospectus','ricpe_web','puzzle']], 'documents':[{},{}],
                'bindings':[{'source':a,'source_page':b,'output_page':c} for a,b,c in sorted(v.BINDINGS)]}
    def test_legacy_still_requires_collateral_controls(self):
        self.assertTrue(v.check_text(self.a,self.b))
    def test_legacy_full_controls_pass(self):
        a=self.a+' '+' '.join(x for r in v.LEGACY.values() for x in r)
        self.assertEqual(v.check_text(a,self.b),[])
    def test_explicit_bounded_profile(self):
        self.assertEqual(v.check_text(self.a,self.b,v.PROFILE),[])
    def test_unknown_profile_fails(self):
        self.assertTrue(v.check_text(self.a,self.b,'other'))
    def test_missing_core_fails(self):
        self.assertTrue(v.check_text(self.a.replace('extinción',''),self.b,v.PROFILE))
    def test_collateral_reintroduction_fails(self):
        for item in ['Hava Vida','Ben Oldman','MCT','Hoja de Términos']:
            with self.subTest(item=item):self.assertTrue(v.check_text(self.a+' '+item,self.b,v.PROFILE))
    def test_missing_second_control_fails(self):
        self.assertTrue(v.check_text(self.a,'',v.PROFILE))
    def test_forbidden_phrase_fails(self):
        for phrase in v.FORBIDDEN_UNQUALIFIED:
            with self.subTest(phrase=phrase):self.assertTrue(v.check_text(self.a+' '+phrase,self.b,v.PROFILE))
    def test_manifest_valid_shape(self):
        self.assertEqual(v.check_manifest_shape(self.m),[])
    def test_wrong_pair_fails(self):
        self.m['versions']=[12,7];self.assertTrue(v.check_manifest_shape(self.m))
    def test_unlisted_puzzle_page_fails(self):
        self.m['puzzle_pages']=[26,27,28,29];self.assertTrue(v.check_manifest_shape(self.m))
    def test_extra_allowed_page_requires_new_profile(self):
        self.m['puzzle_pages']=[24,27,28,29];self.assertTrue(v.check_manifest_shape(self.m))
    def test_wrong_binding_fails(self):
        self.m['bindings'][0]['output_page']=1;self.assertTrue(v.check_manifest_shape(self.m))
    def test_missing_source_fails(self):
        self.m['sources'].pop();self.assertTrue(v.check_manifest_shape(self.m))
    def test_missing_manifest_blocks_cli(self):
        with redirect_stdout(io.StringIO()):
            self.assertEqual(v.main(['missing.pdf','also_missing.pdf','--profile',v.PROFILE]),2)
    def test_non_object_manifest_fails(self):
        self.assertTrue(v.check_manifest_shape([]))
    def test_malformed_manifest_fails(self):
        self.assertTrue(v.check_manifest_shape({}))
    def test_front_declarations_match_actual_document_roles(self):
        self.assertEqual(v.check_front_versions('Documento 1 v13',1),[])
        self.assertEqual(v.check_front_versions('Documento 2 v7 controller v13',2),[])
    def test_each_declared_version_is_required(self):
        for front,number in [('Documento 1',1),('v7 only',2),('v13 only',2)]:
            with self.subTest(front=front):self.assertTrue(v.check_front_versions(front,number))
    def test_version_substrings_do_not_pass(self):
        self.assertTrue(v.check_front_versions('v130',1))
        self.assertTrue(v.check_front_versions('v70 v13',2))
    def test_size_mismatch_and_threshold_are_separate(self):
        errors=v.check_size(20,21,1)
        self.assertEqual(len(errors),1)
        self.assertIn('byte-count mismatch',errors[0])
        errors=v.check_size(10_000_000,10_000_000,1)
        self.assertEqual(len(errors),1)
        self.assertIn('internal size target exceeded',errors[0])
        self.assertEqual(len(v.check_size(10_000_000,9,1)),2)
    def test_dependency_failure_is_not_content_failure(self):
        output=io.StringIO()
        with patch.object(v,'verify_package',side_effect=ImportError('No module named fitz')):
            with redirect_stdout(output):
                result=v.main(['a.pdf','b.pdf','--profile',v.PROFILE,'--manifest','m.json'])
        self.assertEqual(result,2)
        self.assertIn('BLOCKED_ENVIRONMENT',output.getvalue())
        self.assertIn('No content-integrity conclusion',output.getvalue())
if __name__=='__main__':unittest.main()
