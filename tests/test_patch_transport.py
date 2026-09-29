import hashlib
import subprocess
import tempfile
import unittest
from pathlib import Path
from scripts.patch_transport import prepare_patch


class PatchTransportTests(unittest.TestCase):
    def test_empty_and_normalized_are_unchanged(self):
        for text in ('', 'already\n'):
            data, record = prepare_patch(text)
            self.assertEqual(data, text.encode())
            self.assertFalse(record['added_final_newline'])

    def test_unicode_counts_bytes_and_preserves_original_identity(self):
        data, record = prepare_patch('rocket 🚀')
        self.assertEqual(record['applied_bytes'], len(data))
        self.assertEqual(record['original_sha256'], hashlib.sha256('rocket 🚀'.encode()).hexdigest())
        self.assertEqual(record['applied_sha256'], hashlib.sha256(data).hexdigest())

    def test_real_git_rejects_raw_and_applies_normalized_patch(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)
            def git(*args):
                return subprocess.run(['git', *args], cwd=path, capture_output=True)
            self.assertEqual(git('init', '-q').returncode, 0)
            self.assertEqual(git('config', 'core.autocrlf', 'false').returncode, 0)
            source = path/'demo.txt'
            source.write_bytes(b'before\n')
            patch = '--- a/demo.txt\n+++ b/demo.txt\n@@ -1 +1 @@\n-before\n+after'
            file = path/'change.patch'
            file.write_bytes(patch.encode())
            self.assertNotEqual(git('apply', str(file)).returncode, 0)
            self.assertEqual(source.read_bytes(), b'before\n')
            file.write_bytes(prepare_patch(patch)[0])
            result = git('apply', str(file))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(source.read_bytes(), b'after\n')
