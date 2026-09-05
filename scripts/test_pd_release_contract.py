#!/usr/bin/env python3
from copy import deepcopy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import pd_release_contract as c
import pd_release_controller as controller


def result(exit=0, stdout='', stderr=''):
    return {'check':'fixture', 'exit':exit, 'stdout':stdout, 'stderr':stderr, 'completed':True, 'status':'PASS' if exit==0 else 'FAIL'}


class AcceptanceTests(unittest.TestCase):
    def test_pass(self): self.assertTrue(c.acceptance([result()],['fixture'])['accepted'])
    def test_failure(self): self.assertFalse(c.acceptance([result(1)],['fixture'])['accepted'])
    def test_missing(self): self.assertFalse(c.acceptance([],['fixture'])['accepted'])
    def test_duplicate(self): self.assertFalse(c.acceptance([result(),result()],['fixture'])['accepted'])
    def test_skipped_not_success(self):
        r=result();r['status']='SKIPPED';self.assertFalse(c.acceptance([r],['fixture'])['accepted'])
    def test_incomplete_not_success(self):
        r=result();r['completed']=False;self.assertFalse(c.acceptance([r],['fixture'])['accepted'])
    def test_boolean_zero_rejected(self):
        r=result();r['exit']=False;self.assertFalse(c.acceptance([r],['fixture'])['accepted'])
    def test_unknown_status(self):
        r=result();r['status']='neutral';self.assertFalse(c.acceptance([r],['fixture'])['accepted'])
    def test_empty_required(self):
        with self.assertRaises(ValueError):c.acceptance([],[])
    def test_real_child_failure_aggregated(self):
        with tempfile.TemporaryDirectory() as td:
            r=c.run_check('fixture',[sys.executable,'-c','raise SystemExit(7)'],Path(td))
        self.assertFalse(c.acceptance([r],['fixture'])['accepted'])
    def test_timeout_aggregated(self):
        with tempfile.TemporaryDirectory() as td:
            r=c.run_check('fixture',[sys.executable,'-c','import time;time.sleep(2)'],Path(td),1)
        self.assertEqual(r['status'],'TIMEOUT');self.assertFalse(c.acceptance([r],['fixture'])['accepted'])


class FindingTests(unittest.TestCase):
    def test_inventory_growth_not_failure(self):
        a=result(1,json.dumps({'public_html_files_scanned':1054,'strict_errors':['missing A','missing B']}))
        b=result(1,json.dumps({'public_html_files_scanned':1056,'strict_errors':['missing A','missing B']}))
        self.assertEqual(c.compare_results(a,b)['status'],'INHERITED_FINDINGS_UNCHANGED')
    def test_added_defect_blocks(self):
        self.assertFalse(c.compare_results(result(1,stderr='ERROR: A'),result(1,stderr='ERROR: A\nERROR: B'))['no_new_failure'])
    def test_increased_multiplicity_blocks(self):
        self.assertFalse(c.compare_results(result(1,stderr='ERROR: A'),result(1,stderr='ERROR: A\nERROR: A'))['no_new_failure'])
    def test_numeric_defect_not_normalized_away(self):
        self.assertFalse(c.compare_results(result(1,stderr='ERROR: 3 missing'),result(1,stderr='ERROR: 4 missing'))['no_new_failure'])
    def test_unknown_identical_failure_blocks(self):
        self.assertFalse(c.compare_results(result(1,'opaque'),result(1,'opaque'))['no_new_failure'])
    def test_resolved_is_success(self):
        self.assertEqual(c.compare_results(result(1,'opaque'),result())['status'],'RESOLVED')
    def test_improved_not_false_green(self):
        answer=c.compare_results(result(1,stderr='ERROR: A\nERROR: B'),result(1,stderr='ERROR: A'))
        self.assertTrue(answer['no_new_failure']);self.assertFalse(answer['candidate_passed'])
    def test_systemexit_error_bullets(self):
        r=result(1,stderr='- exact defect\n- second defect');self.assertTrue(c.findings(r)[1])
    def test_success_console_bullets_ignored(self):
        self.assertEqual(c.findings(result(0,'PASS\n - 22 sources'))[0],[])
    def test_nonzero_with_empty_errors_fails(self):
        self.assertFalse(c.compare_results(result(),result(1,'{"strict_errors":[]}'))['no_new_failure'])
    def test_zero_with_explicit_errors_fails(self):
        self.assertFalse(c.compare_results(result(),result(0,'{"errors":["A"]}'))['no_new_failure'])


class LegacyErrorAdapterTests(unittest.TestCase):
    def assertion(self, expression='assert registry["counts"] == EXPECTED', line=161, source='<ROOT>/scripts/counts.py'):
        return result(1, stderr='Traceback (most recent call last):\n  File "'+source+'", line '+str(line)+', in <module>\n    '+expression+'\nAssertionError\n')
    def test_explicit_fail_prefix_is_a_defect(self):
        r=result(1,stderr='FAIL: node A missing edges [1, 2]')
        self.assertTrue(c.compare_results(r,r)['no_new_failure'])
        self.assertFalse(c.compare_results(r,result(1,stderr='FAIL: node A missing edges [1, 2, 3]'))['no_new_failure'])
    def test_bare_assertion_line_number_is_not_defect(self):
        self.assertTrue(c.compare_results(self.assertion(),self.assertion(line=190))['no_new_failure'])
    def test_bare_assertion_changed_predicate_blocks(self):
        self.assertFalse(c.compare_results(self.assertion(),self.assertion('assert other == EXPECTED'))['no_new_failure'])
    def test_bare_assertion_changed_source_blocks(self):
        self.assertFalse(c.compare_results(self.assertion(),self.assertion(source='<ROOT>/scripts/other.py'))['no_new_failure'])
    def test_unlocated_assertion_is_unknown(self):
        r=result(1,stderr='AssertionError')
        self.assertFalse(c.compare_results(r,r)['no_new_failure'])

class ScopedOwnershipTests(unittest.TestCase):
    def test_independent_event_addition(self): c.require_prefix_records([{'id':'A','v':1}],[{'id':'A','v':1},{'id':'B','v':2}])
    def test_changed_event_fails(self):
        with self.assertRaises(ValueError):c.require_prefix_records([{'id':'A','v':1}],[{'id':'A','v':2}])
    def test_deleted_event_fails(self):
        with self.assertRaises(ValueError):c.require_prefix_records([{'id':'A'}],[])
    def test_duplicate_event_fails(self):
        with self.assertRaises(ValueError):c.require_prefix_records([{'id':'A'}],[{'id':'A'},{'id':'A'}])
    def test_unowned_page_addition(self):self.assertEqual(c.owned_blocks('old <a>x</a>','new <a>x</a> extra',[('<a>','</a>')]),['<a>x</a>'])
    def test_changed_owned_block_fails(self):
        with self.assertRaises(ValueError):c.owned_blocks('<a>x</a>','<a>y</a>',[('<a>','</a>')])
    def test_duplicate_owned_block_fails(self):
        with self.assertRaises(ValueError):c.owned_blocks('<a>x</a>','<a>x</a><a>x</a>',[('<a>','</a>')])
    def test_missing_owned_block_fails(self):
        with self.assertRaises(ValueError):c.owned_blocks('<a>x</a>','other',[('<a>','</a>')])


class IdentityTests(unittest.TestCase):
    def old(self):return {'PD-SP-O-0084':{'id':'PD-SP-O-0084','type':'ORGANISATION','name':'RAUDA'}}
    def test_collision_rejected(self):
        new=self.old();new['PD-SP-O-0084']['name']='URÍA MENÉNDEZ ABOGADOS, S.L.P.'
        self.assertTrue(c.identity_collisions(self.old(),new))
    def test_alias_alone_cannot_reassign(self):
        new=self.old();new['PD-SP-O-0084'].update(name='Different',aliases=['RAUDA'])
        self.assertTrue(c.identity_collisions(self.old(),new))
    def test_source_linked_prior_history(self):
        old=self.old();new=deepcopy(old);new['PD-SP-O-0084'].update(name='RAUDA ALSP S.L.P.',identity_resolution_history=[{'prior_record':old['PD-SP-O-0084'],'source_refs':['BORME-fixture'],'superseded_only':'identity'}])
        self.assertEqual(c.identity_collisions(old,new),[])
    def test_new_unused_id(self):
        old=self.old();new=deepcopy(old);new['X']={'id':'X','type':'ORGANISATION','name':'Different'}
        self.assertEqual(c.identity_collisions(old,new),[])
    def test_missing_identity_rejected(self):self.assertTrue(c.identity_collisions(self.old(),{}))
    def test_traversal_rejected(self):
        with self.assertRaises(ValueError):c.safe_path('../secret')


class ControllerTests(unittest.TestCase):
    def state(self):return {'phase':'ACCEPTED','owner':'1:'+('a'*40),'fence':3,'checkpoints':[]}
    def test_stale_fence_blocked(self):
        with self.assertRaises(ValueError):c.advance(self.state(),'MERGE_PENDING',self.state()['owner'],2)
    def test_wrong_owner_blocked(self):
        with self.assertRaises(ValueError):c.advance(self.state(),'MERGE_PENDING','other',3)
    def test_no_skip_merge_to_live(self):
        with self.assertRaises(ValueError):c.advance(self.state(),'VERIFIED_FOR_SCOPE',self.state()['owner'],3,{'exact_matches':[1],'pending':[]})
    def test_interrupted_merge_retained(self):
        s=c.advance(self.state(),'MERGE_PENDING',self.state()['owner'],3)
        s=c.advance(s,'RECOVERY_REQUIRED',s['owner'],3)
        self.assertNotIn(s['phase'],c.TERMINAL)
    def test_merge_requires_evidence(self):
        s=c.advance(self.state(),'MERGE_PENDING',self.state()['owner'],3)
        with self.assertRaises(ValueError):c.advance(s,'MERGED',s['owner'],3)
    def test_pending_public_files_cannot_close(self):
        s=self.state();s['phase']='DEPLOYED'
        with self.assertRaises(ValueError):c.advance(s,'VERIFIED_FOR_SCOPE',s['owner'],3,{'exact_matches':[1],'pending':['missing']})
    def event(self):return {'repository':{'full_name':controller.REPO},'issue':{'number':1428},'comment':{'user':{'login':controller.OWNER},'author_association':'OWNER','body':'/pd-release claim 1 '+'a'*40}}
    def test_exact_owner_command(self):self.assertEqual(controller.command(self.event()),('claim',1,'a'*40))
    def test_nonowner_command_rejected(self):
        e=self.event();e['comment']['user']['login']='someone'
        with self.assertRaises(ValueError):controller.command(e)
    def test_injected_argument_rejected(self):
        e=self.event();e['comment']['body']+='; dangerous'
        with self.assertRaises(ValueError):controller.command(e)
    def test_wrong_issue_rejected(self):
        e=self.event();e['issue']['number']=1
        with self.assertRaises(ValueError):controller.command(e)
    def test_conflicting_cas_cannot_overwrite(self):
        api=controller.GitHub.__new__(controller.GitHub);api.token='fixture';storage={'sha':'v1'}
        def request(path,data=None,method=None):
            if data['sha']!=storage['sha']:raise ValueError('conflicting blob SHA')
            storage['sha']='v2';return {'content':{'sha':'v2'}}
        api.request=request
        self.assertEqual(api.save(self.state(),'v1'),'v2')
        with self.assertRaises(ValueError):api.save(self.state(),'v1')

class WriteConfinementTests(unittest.TestCase):
    def api(self):
        from pd_release_controller import GitHub
        with patch.dict('os.environ', {'GH_TOKEN':'test-not-a-real-token'}):
            return GitHub()
    def test_main_update_is_rejected_before_network(self):
        with self.assertRaises(ValueError):self.api().request('git/refs/heads/main',{'sha':'0'*40},'PATCH')
    def test_merge_is_rejected_before_network(self):
        with self.assertRaises(ValueError):self.api().request('pulls/1/merge',{'sha':'0'*40},'PUT')
    def test_state_file_cannot_target_main(self):
        with self.assertRaises(ValueError):self.api().request('contents/state.json',{'branch':'main'},'PUT')
    def test_ref_initialization_cannot_target_main(self):
        with self.assertRaises(ValueError):self.api().request('git/refs',{'ref':'refs/heads/main'},'POST')

if __name__=='__main__':unittest.main()
