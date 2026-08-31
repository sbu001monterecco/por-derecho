import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("community_builder", ROOT / "scripts/build_community_acta_authority_interconnectivity.py")
builder = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(builder)


class CommunityAuthorityBuilderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = builder.build()

    def test_finite_denominators(self):
        self.assertEqual(self.payload["coverage"]["public_acta_packages"], 20)
        self.assertEqual(self.payload["coverage"]["public_authority_files"], 49)
        self.assertEqual(self.payload["coverage"]["evidentiary_axes"], 7)

    def test_parallel_track_preserves_time_and_separation(self):
        parallel = self.payload["parallel_2022"]
        self.assertEqual(parallel["days_from_acta_to_deed"], 17)
        self.assertEqual(parallel["relationship_type"], "TEMPORAL_AND_SUBJECT_MATTER_COMPARISON_ONLY")
        self.assertIn("do not prove", parallel["boundary_en"])

    def test_named_authorities_are_present(self):
        ids = {record["master_id"] for record in self.payload["authority_files"]}
        for master_id in ("X-INT-004", "X-EU-003", "NAT-CNMV-001", "LZ-YAI-014", "LZ-CAB-019", "NAT-AID-001"):
            self.assertIn(master_id, ids)

    def test_every_authority_has_one_group_and_reciprocal_entry(self):
        groups = {group["id"] for group in self.payload["authority_groups"]}
        for record in self.payload["authority_files"]:
            self.assertIn(record["group_id"], groups)
            self.assertIn(record["master_id"], self.payload["by_master_id"])

    def test_allegation_is_not_a_finding(self):
        self.assertEqual(self.payload["attributed_allegation"]["status"], "SERIOUS_FALSIFIABLE_PARTY_ALLEGATION_NOT_ESTABLISHED")
        self.assertIn("not establish", self.payload["attributed_allegation"]["boundary_en"])


if __name__ == "__main__":
    unittest.main()
