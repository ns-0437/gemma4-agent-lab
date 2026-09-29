import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from scripts.control_evidence import write_arm
from scripts.verify_evidence import verify_arm


class EvidenceVerificationTests(unittest.TestCase):
    def test_read_only_and_detects_tampering_or_missing_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'arm'
            write_arm(path, {'reached_pytest':False}, stdout='example')
            before={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in path.iterdir()}
            self.assertEqual(verify_arm(path), [])
            self.assertEqual(before, {f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in path.iterdir()})
            (path/'stdout.txt').write_text('changed')
            self.assertIn('stdout.txt: hash mismatch', verify_arm(path))
            (path/'stderr.txt').unlink()
            self.assertIn('stderr.txt: missing', verify_arm(path))

    def test_refuses_escape_and_empty_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)
            for name in ('../secret','/absolute','C:/file','..\\secret'):
                (path/'arm.json').write_text(json.dumps({'artifact_sha256':{name:'x'}}))
                with self.assertRaises(ValueError): verify_arm(path)
            (path/'arm.json').write_text('{"artifact_sha256":{}}')
            with self.assertRaises(ValueError): verify_arm(path)
