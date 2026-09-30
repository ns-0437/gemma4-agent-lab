import unittest
from scripts.patch_evidence import inspect_patch

PATCH = 'diff --git a/demo.py b/demo.py\n--- a/demo.py\n+++ b/demo.py\n@@ -1 +1 @@\n-old\n+new\n'


class PatchTests(unittest.TestCase):
    def test_valid_syntax_does_not_claim_application(self):
        result = inspect_patch(PATCH, len(PATCH))
        self.assertTrue(result['syntax_valid'])
        self.assertEqual(result['changed_paths'], ['demo.py'])
        self.assertIsNone(result['application_verified'])

    def test_sizes_are_characters_not_bytes(self):
        patch = PATCH.replace('+new', '+café')
        self.assertTrue(inspect_patch(patch, len(patch))['syntax_valid'])
        self.assertFalse(inspect_patch(patch, len(patch.encode('utf-8')))['size_matches'])

    def test_missing_bool_and_wrong_size(self):
        for size in (None, True, 1):
            self.assertFalse(inspect_patch(PATCH, size)['syntax_valid'])

    def test_header_only_empty_and_corrupt_counts(self):
        for patch in ('', PATCH.split('@@')[0], PATCH.replace('@@ -1 +1 @@', '@@ -1,8 +1,8 @@')):
            with self.subTest(patch=patch):
                self.assertFalse(inspect_patch(patch, len(patch))['syntax_valid'])
