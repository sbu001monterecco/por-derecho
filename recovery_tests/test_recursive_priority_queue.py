import json,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from legaltech.unitary_review import recursive_priority_queue as q

class RecursiveQueueTests(unittest.TestCase):
    def test_github_queue_is_ordered_and_bound(self):
        r=q.run(ROOT/"assets/data/truth-machine-priority-queue-v1.json","github")
        self.assertFalse(r["hard_integrity_problem"])
        self.assertEqual([x["rank"] for x in r["candidates"]],list(range(len(r["candidates"]))))
        self.assertTrue(all(not x["automatic_merits_promotion"] for x in r["candidates"]))
    def test_r33_then_an2023(self):
        d=json.loads((ROOT/"assets/data/truth-machine-priority-queue-v1.json").read_text())
        self.assertEqual(d["candidates"][0]["id"],"C36-SPECIALIST-R33")
        self.assertEqual(d["candidates"][1]["id"],"AN2023-QUERELLA-21SEP")
    def test_changed_github_pin_fails_closed(self):
        d=json.loads((ROOT/"assets/data/truth-machine-priority-queue-v1.json").read_text())
        d["candidates"][1]["sources"][0]["github_blob_sha"]="0"*40
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"q.json";p.write_text(json.dumps(d))
            r=q.run(p,"github");self.assertTrue(r["hard_integrity_problem"])
            self.assertEqual(r["candidates"][1]["queue_state"],"REVIEW_REQUIRED_SOURCE_CHANGED")
    def test_declared_host_gap_is_not_fabricated_parity(self):
        d=json.loads((ROOT/"assets/data/truth-machine-priority-queue-v1.json").read_text())
        dp=next(x for x in d["candidates"] if x["id"]=="DP1901-AUTO-14SEP2026")
        self.assertIsNone(dp["sources"][0]["gitlab_blob_sha"])
    def test_no_truth_score_field(self):
        raw=json.dumps(q.run(ROOT/"assets/data/truth-machine-priority-queue-v1.json","github")).lower()
        self.assertNotIn('"truth_score"',raw);self.assertNotIn('"guilt_score"',raw)
if __name__=="__main__": unittest.main()
