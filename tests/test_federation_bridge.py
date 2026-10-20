import importlib.util
import json
import unittest
from pathlib import Path
from unittest import mock

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate_federation_bridge.py"
SPEC = importlib.util.spec_from_file_location("fed_validator", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)

class FederationBridgeTests(unittest.TestCase):
    def test_current_contract_passes(self):
        stats = MODULE.validate(Path(__file__).resolve().parents[1])
        self.assertEqual(stats["max_hops"], 32)
        self.assertEqual(stats["roles"], 6)
        self.assertEqual(stats["authority_fields"], 7)

    def _mutated_loader(self, filename, mutate):
        root=Path(__file__).resolve().parents[1]
        original=MODULE.load
        def altered(path):
            obj=original(path)
            if path.name==filename:
                obj=json.loads(json.dumps(obj))
                mutate(obj)
            return obj
        return root, altered

    def test_blind_mirroring_cannot_be_enabled(self):
        root, altered=self._mutated_loader(
            "PD_FEDERATION_V1.json",
            lambda obj: obj["authority_boundary"].__setitem__("blind_bidirectional_mirroring", True),
        )
        with mock.patch.object(MODULE,"load",side_effect=altered):
            with self.assertRaisesRegex(ValueError,r"class=AUTHORITY_DRIFT path=authority_boundary.blind_bidirectional_mirroring"):
                MODULE.validate(root)

    def test_authority_role_strings_fail_closed(self):
        root, altered=self._mutated_loader(
            "PD_FEDERATION_V1.json",
            lambda obj: obj["authority_boundary"].__setitem__("gitlab_role", "MUTATED_ROLE"),
        )
        with mock.patch.object(MODULE,"load",side_effect=altered):
            with self.assertRaisesRegex(ValueError,r"class=AUTHORITY_DRIFT path=authority_boundary.gitlab_role"):
                MODULE.validate(root)

    def test_recursion_cannot_be_unbounded(self):
        root, altered=self._mutated_loader(
            "PD_FEDERATION_V1.json",
            lambda obj: obj["recursive_engine"].__setitem__("max_hops", 999),
        )
        with mock.patch.object(MODULE,"load",side_effect=altered):
            with self.assertRaisesRegex(ValueError,r"class=RECURSION_POLICY_DRIFT path=recursive_engine.max_hops"):
                MODULE.validate(root)

    def test_non_genesis_requires_predecessor(self):
        root=Path(__file__).resolve().parents[1]
        schema=MODULE.load(root/"schemas/por-derecho-federation-envelope-v1.schema.json")
        example=MODULE.load(root/"ops/federation/EXAMPLE_STATE_ENVELOPE.json")
        example["iteration"]=1
        example["predecessor"]=None
        errors=list(MODULE.Draft202012Validator(schema).iter_errors(example))
        self.assertTrue(errors)

if __name__=="__main__":
    unittest.main()
