#!/usr/bin/env python3
"""Regression coverage for the recovered CI rules; no network or writes to source."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import loader_graph as graph
import production_smoke_check_v2 as smoke
import reconcile_identity_registry_projections as projection
import validate_publication_integrity_v2 as publication


class LoaderTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root/'assets').mkdir()
        self.put('site.js', "load('bridge.js?v=1');")
        self.put('bridge.js', "load('target.js'); load('site.js');")
        self.put('target.js', "window.targetLoaded = true;")
    def put(self, name, text):
        (self.root/'assets'/name).write_text(text, encoding='utf-8')
    def test_delegation_and_cycle(self):
        self.assertEqual(graph.find_loader_path('assets/site.js','assets/target.js',root=self.root), ('assets/site.js','assets/bridge.js','assets/target.js'))
    def test_comment_is_not_dependency(self):
        self.put('site.js', "// load('bridge.js')\n/* 'target.js' */\nconst url='https://example.invalid/no.js';")
        self.assertIsNone(graph.find_loader_path('assets/site.js','assets/target.js',root=self.root))
    def test_missing_file_never_matches_itself(self):
        self.assertIsNone(graph.find_loader_path('assets/missing.js','assets/missing.js',root=self.root))
    def test_removed_bridge_fails(self):
        (self.root/'assets/bridge.js').unlink()
        with self.assertRaises(ValueError): smoke.loader_contract(self.root, ('assets/target.js',))
    def test_escaping_path_rejected(self):
        with self.assertRaises(ValueError): graph.find_loader_path('../secrets.js','assets/site.js',root=self.root)
    def test_dynamic_template_not_claimed_as_edge(self):
        self.put('site.js', 'load(`${prefix}target.js`);')
        self.assertEqual(graph.local_loader_references('assets/site.js',root=self.root), ())
    def test_hash_contract_good_bytes(self):
        expected=smoke.loader_contract(self.root, ('assets/target.js',))
        rows=[{'path':p, 'ok':True, **v} for p,v in expected.items()]
        self.assertTrue(smoke.verify_hashes(rows,expected)[0])
    def test_mutated_deployed_bytes_fail(self):
        expected=smoke.loader_contract(self.root, ('assets/target.js',))
        rows=[{'path':p, 'ok':True, **v} for p,v in expected.items()]
        rows[0]['sha256']='0'*64
        self.assertFalse(smoke.verify_hashes(rows,expected)[0])
    def test_omitted_dependency_fails(self):
        expected=smoke.loader_contract(self.root, ('assets/target.js',))
        self.assertFalse(smoke.verify_hashes([],expected)[0])
    def test_business_failure_stays_failed(self):
        expected=smoke.loader_contract(self.root, ('assets/target.js',))
        rows=[{'path':p, 'ok':True, **v} for p,v in expected.items()]
        rows.append({'path':'es/example/', 'ok':False})
        self.assertFalse(smoke.verify_hashes(rows,expected)[0])
    def test_actual_source_retains_all_business_assertions(self):
        before=[x for x in deepcopy(smoke.ORIGINAL_CHECKS) if x['kind']!='global_loader']
        with patch.object(smoke.legacy,'CHECKS',deepcopy(smoke.ORIGINAL_CHECKS)), patch.object(smoke.legacy,'one_pass',smoke.ORIGINAL_ONE_PASS):
            smoke.apply_current_loader_contract()
            after=[x for x in smoke.legacy.CHECKS if x['kind'] not in ('global_loader','loader_dependency')]
            self.assertEqual(before,after)


class ProjectionTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);(self.root/'assets/data').mkdir(parents=True)
        self.records=[{'id':'TEST-P-1','type':'PERSON'}]
        self.save()
    def save(self, count=1):
        (self.root/'assets/data/people.json').write_text(json.dumps({'records':self.records}))
        self.index={'parts':[{'path':'people.json','count':count}], 'counts':{'total':count, **{t:(count if t=='PERSON' else 0) for t in projection.TYPES}}, 'control_date':'2026-09-03'}
        (self.root/projection.INDEX).write_text(json.dumps(self.index))
    def test_source_derived_next_identity(self):
        self.records.append({'id':'TEST-P-2','type':'PERSON'});self.save(2)
        self.assertEqual(projection.canonical_snapshot(self.root)[0]['total'],2)
    def test_duplicate_identity_fails(self):
        self.records.append(dict(self.records[0]));self.save(2)
        with self.assertRaises(ValueError):projection.canonical_snapshot(self.root)
    def test_incorrect_part_count_fails(self):
        self.save(2)
        with self.assertRaises(ValueError):projection.canonical_snapshot(self.root)
    def test_invalid_date_fails(self):
        self.index['control_date']='not-a-date';(self.root/projection.INDEX).write_text(json.dumps(self.index))
        with self.assertRaises(ValueError):projection.canonical_snapshot(self.root)
    def test_actual_projection_is_idempotent(self):
        for path,text in projection.projection_outputs().items():
            self.assertEqual((projection.ROOT/path).read_text(encoding='utf-8'),text,path)
    def test_future_counts_are_not_frozen(self):
        counts, stamp=projection.canonical_snapshot()
        counts['total']+=1;counts['PERSON']+=1
        for lang,path in projection.PAGES.items():
            original=(projection.ROOT/path).read_text(encoding='utf-8')
            output=projection.project_page(original,counts,stamp,lang)
            self.assertIn('data-registry-stat="TOTAL">'+str(counts['total']),output)
            self.assertIn('data-registry-stat="PERSON">'+str(counts['PERSON']),output)
            self.assertEqual(projection.project_page(output,counts,stamp,lang),output)


class PublicationTests(unittest.TestCase):
    def test_changed_legacy_requires_schema(self):
        record={k:None for k in publication.LEGACY_REQUIRED_FIELDS}
        self.assertIsNotNone(publication.classify_document(record,changed=True)[1])
    def test_unchanged_complete_legacy_remains_readable(self):
        record={k:None for k in publication.LEGACY_REQUIRED_FIELDS}
        self.assertEqual(publication.classify_document(record,changed=False),('legacy',None))
    def test_new_unknown_schema_rejected(self):
        self.assertIsNotNone(publication.classify_document({'schema':'unsupported'},changed=True)[1])
    def test_publication_wrong_version_rejected(self):
        self.assertIsNotNone(publication.classify_document({'schema':publication.PUBLICATION_SCHEMA,'schema_version':'0'},changed=True)[1])
    def test_transition_has_its_own_contract(self):
        self.assertEqual(publication.classify_document({'schema':publication.TRANSITION_SCHEMA},changed=False),('transition',None))
    def test_machine_schema_matches_validator(self):
        errors=[];publication.validate_publication_contract(errors);self.assertEqual(errors,[])

if __name__=='__main__':unittest.main()
