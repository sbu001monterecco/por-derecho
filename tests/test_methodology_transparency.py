import importlib.util, json, unittest
from pathlib import Path
from unittest import mock

SCRIPT=Path(__file__).resolve().parents[1]/"scripts"/"validate_methodology_transparency.py"
SPEC=importlib.util.spec_from_file_location("method_validator",SCRIPT)
M=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(M)

class MethodologyTransparencyTests(unittest.TestCase):
    def test_current_candidate_passes_semantic_projection(self):
        result=M.validate(Path(__file__).resolve().parents[1])
        self.assertEqual(result["stages"],11); self.assertEqual(result["publication_state"],"PR_OPEN")

    def test_stage_removal_fails_closed(self):
        root=Path(__file__).resolve().parents[1]; original=M.load
        def altered(path):
            obj=original(path)
            if path.name=="methodology-transparency-v1.json": obj=json.loads(json.dumps(obj)); obj["recursive_sequence"]=obj["recursive_sequence"][:-1]
            return obj
        with mock.patch.object(M,"load",side_effect=altered):
            with self.assertRaisesRegex(ValueError,"STAGE_ORDER_DRIFT"): M.validate(root)

    def test_live_status_cannot_self_promote(self):
        root=Path(__file__).resolve().parents[1]; original=M.load
        def altered(path):
            obj=original(path)
            if path.name=="methodology-transparency-20260922.json": obj=json.loads(json.dumps(obj)); obj["current_state"]="LIVE_VERIFIED"; obj["live_verified"]=True
            return obj
        with mock.patch.object(M,"load",side_effect=altered):
            with self.assertRaisesRegex(ValueError,"FALSE_RELEASE_PROMOTION"): M.validate(root)

    def test_architecture_history_cannot_hide_draft_status(self):
        root=Path(__file__).resolve().parents[1]; original=M.load
        def altered(path):
            obj=original(path)
            if path.name=="methodology-transparency-v1.json": obj=json.loads(json.dumps(obj)); obj["architecture_history"][-1]["status"]="CONTROLLING_ACCEPTED"
            return obj
        with mock.patch.object(M,"load",side_effect=altered):
            with self.assertRaisesRegex(ValueError,"ARCHITECTURE_HISTORY_DRIFT"): M.validate(root)

    def test_host_origin_map_is_explicit(self):
        self.assertIn("github",M.ORIGINS); self.assertIn("gitlab",M.ORIGINS); self.assertNotEqual(M.ORIGINS["github"],M.ORIGINS["gitlab"])

if __name__=="__main__": unittest.main()
