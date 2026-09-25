import copy
import hashlib
import json
import unittest
from legaltech.unitary_review import method_stack as ms

def case():
    text1="El pago de 400.000 € fue autorizado el 6 de julio de 2020."
    text2="Presumiblemente todos abandonaron el procedimiento."
    return {
      "schema":"pd.forensic.v1",
      "document":{"id":"DOC","title":"synthetic","sha256":"0"*64},
      "blocks":[{"id":"P01-B1","page":1,"text":text1},{"id":"P02-B1","page":2,"text":text2}],
      "annotations":[
        {"id":"X-P01-S1","block":"P01-B1","quote":text1,"origin":"LIAR_LIAR_FULL_V3_STATEMENT",
         "truth":{"status":"PARTIAL","decision":"PROPOSED","knowledge":"NOT_ASSESSED","causation":"UNSUPPORTED_INFERENCE"},
         "evidence":[{"relation":"RELATED","source":"S1"},{"relation":"CONTRADICTS","source":"S2","locator":"counter"}]},
        {"id":"X-P02-S1","block":"P02-B1","quote":text2,"origin":"LIAR_LIAR_FULL_V3_STATEMENT",
         "truth":{"status":"UNRESOLVED","decision":"PROPOSED","knowledge":"INFERRED_ONLY","causation":"NOT_ASSESSED"},
         "evidence":[{"relation":"RELATED","source":"S3"}]},
        {"id":"X-P01-PARA","block":"P01-B1","quote":text1,"origin":"LIAR_LIAR_FULL_V3_PARAGRAPH","truth":{"status":"PARTIAL"},"evidence":[]}
      ]
    }

class MethodStackTests(unittest.TestCase):
    def test_all_statement_records_processed(self):
        p,a=ms.analyse_case(case()); self.assertEqual(len(p["records"]),2); self.assertEqual(a["validation"]["statement_records_processed"],2)
    def test_source_not_mutated(self):
        c=case(); before=ms.digest(c); ms.analyse_case(c); self.assertEqual(before,ms.digest(c))
    def test_contradiction_is_candidate_not_lie(self):
        p,a=ms.analyse_case(case()); r=p["records"][0]["falsehood_register"]; self.assertEqual(r["state"],"CONTRADICTION_REVIEW_CANDIDATE"); self.assertFalse(r["knowingly_false"])
    def test_knowledge_inferred_only_not_promoted(self):
        p,_=ms.analyse_case(case()); self.assertFalse(p["records"][1]["falsehood_register"]["knowledge_evidence_established"])
    def test_verifiability_and_financial_control_cues(self):
        _,a=ms.analyse_case(case()); self.assertEqual(a["method_coverage"]["VERIFIABILITY"]["candidate_statements"],1); self.assertEqual(a["method_coverage"]["FATF_FINANCIAL"]["candidate_statements"],1); self.assertEqual(a["method_coverage"]["FCA_CONTROLS"]["candidate_statements"],1)
    def test_linguistic_probe_is_not_deception_finding(self):
        _,a=ms.analyse_case(case()); self.assertEqual(a["method_coverage"]["FBI_LINGUISTIC_PROBE"]["candidate_statements"],1); self.assertEqual(a["method_coverage"]["FBI_LINGUISTIC_PROBE"]["deception_findings"],0)
    def test_ach_has_no_probabilities(self):
        p,_=ms.analyse_case(case()); self.assertFalse(p["records"][0]["ach"]["probabilities_assigned"])
    def test_sue_does_not_simulate_interview(self):
        p,_=ms.analyse_case(case()); self.assertFalse(p["records"][0]["sue_statement_evidence"]["interview_strategy_simulated"])
    def test_forbidden_scores_absent(self):
        p,a=ms.analyse_case(case()); raw=json.dumps([p,a]); 
        for k in ms.FORBIDDEN_SCORES: self.assertNotIn('"'+k+'":',raw)
    def test_bad_schema_fails(self):
        c=case(); c["schema"]="x"
        with self.assertRaises(ms.MethodStackError): ms.analyse_case(c)
    def test_duplicate_statement_id_fails(self):
        c=case(); c["annotations"][1]["id"]=c["annotations"][0]["id"]
        with self.assertRaises(ms.MethodStackError): ms.analyse_case(c)
    def test_nonbinary_state_preserved(self):
        c=case(); c["annotations"][1]["truth"]["status"]="RHETORICAL_OR_LEGAL"
        p,_=ms.analyse_case(c); self.assertEqual(p["records"][1]["falsehood_register"]["state"],"NON_BINARY_RHETORIC_OR_LEGAL")

if __name__=="__main__": unittest.main()