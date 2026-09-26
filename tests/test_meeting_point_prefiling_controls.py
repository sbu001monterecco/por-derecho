"""Synthetic fixtures only: no private court content or source files."""
import io
from contextlib import redirect_stdout
import importlib.util
from pathlib import Path
import unittest
PATH=Path(__file__).resolve().parents[1]/'scripts'/'validate_meeting_point_prefiling_controls.py'
if not PATH.exists(): PATH=Path(__file__).with_name('validate_meeting_point_prefiling_controls.py')
spec=importlib.util.spec_from_file_location('controls',PATH)
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
if __name__=='__main__':unittest.main()
