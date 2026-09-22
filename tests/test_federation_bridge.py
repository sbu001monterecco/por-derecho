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

    def test_blind_mirroring_cannot_be_enabled(self):
        root=Path(__file__).resolve().parents[1]
        original=MODULE.load
        def altered(path):
            obj=original(path)
            if path.name=="PD_FEDERATION_V1.json":
                obj=json.loads(json.dumps(obj))
                obj["authority_boundary"]["blind_bidirectional_mirroring"]=True
            return obj
        with mock.patch.object(MODULE,"load",side_effect=altered):
            with self.assertRaisesRegex(ValueError,"blind bidirectional"):
                MODULE.validate(root)

    def test_recursion_cannot_be_unbounded(self):
        root=Path(__file__).resolve().parents[1]
        original=MODULE.load
        def altered(path):
            obj=original(path)
            if path.name=="PD_FEDERATION_V1.json":
                obj=json.loads(json.dumps(obj))
                obj["recursive_engine"]["max_hops"]=999
            return obj
        with mock.patch.object(MODULE,"load",side_effect=altered):
            with self.assertRaisesRegex(ValueError,"bounded"):
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
