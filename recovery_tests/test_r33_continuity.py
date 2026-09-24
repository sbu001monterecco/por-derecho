import copy
import json
import tempfile
import unittest
from pathlib import Path
from legaltech.unitary_review.r33_continuity import (
    ContinuityError, append_event, crosswalk, decision_gate, digest,
    inspect_cases, invalidated, retrieve, snapshot, span, units, verify_ledger, bind_successor, source_delta)

SHA = 'a' * 64

def case(text='A sufficiently long exact source statement for an auditable review.', identifier='A'):
    return {'schema': 'pd.forensic.v1', 'document': {'sha256': SHA},
            'blocks': [{'id': 'B', 'page': 1, 'text': text}],
            'annotations': [{'id': identifier, 'block': 'B', 'start': 0, 'end': len(text),
                             'quote': text, 'review': 'PROVISIONAL', 'note': 'Retain me'}]}

def event(identifier='E1', kind='INTEGRITY_REVIEW'):
    return dict(id=identifier, kind=kind, recorded_at='2026-09-24T00:00:00Z',
                execution_state='EXECUTED', input_versions=['v3'], sources_examined=['source'],
                propositions=['A'], before='OPEN', after='ANCHOR_VERIFIED',
                contrary_evidence=['not a merits review'], dependencies=['sidecar'],
                integration='LOCAL', publication='NOT_DEPLOYED', reason='Exact source validation')

class Anchors(unittest.TestCase):
    def test_valid(self):
        original=case(); parsed=units(original)
        self.assertEqual(parsed[0]['original_row'], original['annotations'][0])
        self.assertFalse(parsed[0]['assessment_transfer'])
    def test_bad_quote(self):
        d=case();d['annotations'][0]['quote']='wrong'
        with self.assertRaises(ContinuityError): units(d)
    def test_out_of_range(self):
        d=case();d['annotations'][0]['end']=9999
        with self.assertRaises(ContinuityError): units(d)
    def test_missing_block(self):
        d=case();d['annotations'][0]['block']='missing'
        with self.assertRaises(ContinuityError): units(d)
    def test_duplicate_annotation(self):
        d=case();d['annotations']*=2
        with self.assertRaises(ContinuityError): units(d)
    def test_duplicate_block(self):
        d=case();d['blocks']*=2
        with self.assertRaises(ContinuityError): units(d)
    def test_utf16(self):
        self.assertEqual(span('A😀B',1,3,'utf16'),'😀')
        with self.assertRaises(ContinuityError): span('A😀B',1,2,'utf16')
    def test_negative_span(self):
        with self.assertRaises(ContinuityError): span('abc',-1,2,'codepoint')
    def test_unknown_schema(self):
        d=case();d['schema']='other'
        with self.assertRaises(ContinuityError): units(d)
    def test_bad_native_hash(self):
        d=case();d['document']['sha256']=''
        with self.assertRaises(ContinuityError): units(d)
    def test_stable_span_across_note_change(self):
        a=case();b=copy.deepcopy(a);b['annotations'][0]['note']='changed analysis'
        x,y=units(a)[0],units(b)[0]
        self.assertEqual(x['span_key'],y['span_key'])
        self.assertNotEqual(x['occurrence_id'],y['occurrence_id'])
    def test_successor_self_hash_not_source_check(self):
        d={'schema':'pd.truth-machine.v2','document':{'sha256':SHA},'propositions':[
            {'id':'S','page':1,'block_id':'B','start':0,'end':3,'quote':'abc',
             'quote_sha256':digest(b'abc')}]}
        self.assertEqual(units(d)[0]['anchor_check'],'SELF_HASH_ONLY')
        d['propositions'][0]['quote']='def'
        with self.assertRaises(ContinuityError): units(d)

class Successor(unittest.TestCase):
    def proposal(self):
        d=case()
        return {'schema':'pd.truth-machine.v2','document':d['document'], 'propositions':[
            dict(id='T',page=1,block_id='B',start=0,end=len(d['blocks'][0]['text']),
                 quote=d['blocks'][0]['text'],quote_sha256=digest(d['blocks'][0]['text'].encode()))]}
    def test_parent_binding(self):
        self.assertEqual(bind_successor(self.proposal(),case())[0]['anchor_check'],
                         'PRESERVED_PARENT_BLOCK_EXACT')
    def test_parent_mismatch(self):
        with self.assertRaises(ContinuityError):bind_successor(self.proposal(),case('changed'))
    def test_source_delta(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);(p/'a.txt').write_text('before')
            a=snapshot('gitlab',p,'a'*40,'selected');(p/'a.txt').write_text('after')
            (p/'b.txt').write_text('new');b=snapshot('gitlab',p,'b'*40,'selected')
            r=source_delta(a,b)
            self.assertEqual(r['changed'],['a.txt']);self.assertEqual(r['added'],['b.txt'])
            self.assertFalse(r['merits_assessment_changed'])

class Crosswalk(unittest.TestCase):
    def test_exact_new_id(self):
        a,b=units(case()),units(case(identifier='renumbered'))
        result=crosswalk(a,b)
        self.assertEqual(result['rows'][0]['status'],'EXACT_TEXT_CANDIDATE')
        self.assertFalse(result['rows'][0]['assessment_transfer'])
    def test_duplicate_text_remains_ambiguous(self):
        d=case();r=copy.deepcopy(d['annotations'][0]);r['id']='A2';d['annotations'].append(r)
        self.assertEqual(crosswalk(units(case()),units(d))['rows'][0]['status'],'AMBIGUOUS_EXACT_TEXT')
    def test_whitespace(self):
        self.assertEqual(crosswalk(units(case('one two')),units(case('one  two')))[
            'rows'][0]['status'],'WHITESPACE_CANDIDATE')
    def test_contains(self):
        a=units(case());b=units(case('Introduction. '+a[0]['quote']+' More context.'))
        self.assertEqual(crosswalk(a,b)['rows'][0]['status'],'SPLIT_MERGE_OR_SCOPE_CANDIDATE')
    def test_unmatched_is_retained(self):
        out=crosswalk(units(case('alpha')),units(case('beta')))
        self.assertEqual(out['old_rows_preserved'],1)
        self.assertEqual(out['rows'][0]['status'],'NO_TEXT_COUNTERPART_LOCATED')
    def test_page_separation(self):
        d=case();d['blocks'][0]['page']=2
        self.assertEqual(crosswalk(units(case()),units(d))['rows'][0]['status'],
                         'NO_TEXT_COUNTERPART_LOCATED')
    def test_source_separation(self):
        d=case();d['document']['sha256']='b'*64
        with self.assertRaises(ContinuityError):crosswalk(units(case()),units(d))

class Coverage(unittest.TestCase):
    def test_no_corpora_is_not_no_hit(self):
        out=retrieve([],['term'])
        self.assertEqual(out['state'],'NO_CORPORA_SUPPLIED')
        self.assertIsNone(out['host_search_coverage_percent'])
    def test_missing_root(self):
        with self.assertRaises(ContinuityError): snapshot('github',Path('/does-not-exist'), 'f'*40,'bounded')
    def test_scope_and_host(self):
        with tempfile.TemporaryDirectory() as tmp:
            for host,scope in [('other','bounded'),('github','')]:
                with self.assertRaises(ContinuityError):snapshot(host,Path(tmp),'f'*40,scope)
    def test_exclusions(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)
            for n,b in [('a.md',b'term'),('b.pdf',b'pdf'),('c.txt',b'\xff'),
                        ('d.txt',b' '*5),('e.txt',b'\0'),('f.txt',b'x'*30)]: (p/n).write_bytes(b)
            (p/'link.txt').symlink_to(p/'a.md')
            s=snapshot('github',p,'f'*40,'selected test files',20)
            self.assertEqual(s['counts'],dict(INDEXED=1,EXCLUDED_TYPE=1,UNREADABLE_UTF8=1,
                EMPTY=1,EXCLUDED_BINARY=1,EXCLUDED_SIZE=1,EXCLUDED_SYMLINK=1))
            self.assertFalse(s['complete_remote_repository'])
    def test_pagination_and_duplicates(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)
            for i in range(12):(p/f'{i}.txt').write_text('term')
            s=snapshot('github',p,'f'*40,'selected')
            a=retrieve([s],['term'],limit=8)['hosts']['github']
            b=retrieve([s],['term'],offset=a['next_offset'],limit=8)['hosts']['github']
            self.assertEqual(a['total_candidates'],12)
            self.assertTrue(a['truncated']);self.assertFalse(b['truncated'])
            self.assertEqual(len(a['hits'])+len(b['hits']),12)
            with self.assertRaises(ContinuityError): retrieve([s,s],['term'])
    def test_no_hits_and_invalid_query(self):
        with tempfile.TemporaryDirectory() as tmp:
            s=snapshot('gitlab',Path(tmp),'f'*40,'empty selected corpus')
            self.assertEqual(retrieve([s],['none'])['hosts']['gitlab']['state'],
                             'NO_CANDIDATE_IN_DECLARED_CORPUS')
            with self.assertRaises(ContinuityError):retrieve([s],[])
            with self.assertRaises(ContinuityError):retrieve([s],['x'],offset=-1)

class Dependence(unittest.TestCase):
    def test_transitive_cycle(self):
        edges=[{'from':a,'to':b,'basis':'declared'} for a,b in [('S','A'),('A','B'),('B','A')]]
        result=invalidated(['S'],edges)
        self.assertEqual([r['id'] for r in result],['A','B'])
        self.assertTrue(all(not r['assessment_changed'] for r in result))
    def test_missing_basis(self):
        with self.assertRaises(ContinuityError):invalidated(['S'],[{'from':'S','to':'A'}])
    def test_no_change(self):self.assertEqual(invalidated([],[]),[])
    def test_no_human_promotion(self):
        out=decision_gate({'relation':'CONTRADICTS','reviewer_type':'AI'})
        self.assertEqual(out['state'],'BLOCKED');self.assertIn('human_review',out['missing'])
    def test_complete_record_still_not_auto_promoted(self):
        d={k:'reviewed explanation' for k in ['reviewer','left_pinpoint','right_pinpoint',
            'actor_capacity_time_scope','contrary_material','lawful_alternative','source_lineage','rationale']}
        d.update(relation='NARROWS',reviewer_type='HUMAN',left_source_sha256=SHA,right_source_sha256=SHA)
        result=decision_gate(d)
        self.assertEqual(result['state'],'ELIGIBLE_FOR_SEPARATE_REVIEW')
        self.assertFalse(result['automatically_promoted'])

class Ledger(unittest.TestCase):
    def test_append(self):
        rows=append_event([],event(),None)
        newer=append_event(rows,event('E2'),rows[-1]['sha256']);verify_ledger(newer)
        self.assertEqual(len(rows),1);self.assertEqual(len(newer),2)
    def test_stale(self):
        rows=append_event([],event(),None)
        with self.assertRaises(ContinuityError):append_event(rows,event('E2'),None)
    def test_duplicate(self):
        rows=append_event([],event(),None)
        with self.assertRaises(ContinuityError):append_event(rows,event(),rows[-1]['sha256'])
    def test_tamper(self):
        rows=append_event([],event(),None);rows[0]['after']='changed'
        with self.assertRaises(ContinuityError):verify_ledger(rows)
    def test_no_change_and_kind(self):
        d=event(kind='NO_CHANGE')
        with self.assertRaises(ContinuityError):append_event([],d,None)
        d['after']=d['before'];self.assertEqual(len(append_event([],d,None)),1)
        with self.assertRaises(ContinuityError):append_event([],event(kind='GUILT_SCORE'),None)
    def test_input_integrity_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);f=p/'input.json';raw=json.dumps(case()).encode();f.write_bytes(raw)
            result=inspect_cases([f],p/'out')
            self.assertEqual(f.read_bytes(),raw);self.assertEqual(result['automatic_promotions'],0)
            with self.assertRaises(ContinuityError):inspect_cases([f],p/'out')

if __name__=='__main__':unittest.main()
