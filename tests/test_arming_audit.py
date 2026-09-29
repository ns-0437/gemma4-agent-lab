import copy
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from audit_notebook_arming import audit


def notebook(flag=False):
    return {"cells": [{"cell_type": "code", "source": f"DISPATCH_CONFIRM = {flag} # launch\n", "outputs": []}], "metadata": {}}


class ArmingAuditTests(unittest.TestCase):
    def test_only_flag_change(self):
        self.assertTrue(audit(notebook(), notebook(True))["only_launch_flag_changed"])

    def test_other_code_change_rejected(self):
        armed = notebook(True)
        armed["cells"][0]["source"] += "budget = 100\n"
        with self.assertRaises(ValueError): audit(notebook(), armed)

    def test_metadata_outputs_and_markdown_changes_rejected(self):
        for key in ("metadata", "outputs", "markdown"):
            with self.subTest(key=key):
                armed = notebook(True)
                if key == "metadata": armed["metadata"]["gpu"] = "different"
                elif key == "outputs": armed["cells"][0]["outputs"] = ["changed"]
                else: armed["cells"].append({"cell_type": "markdown", "source": "changed"})
                with self.assertRaises(ValueError): audit(notebook(), armed)

    def test_duplicate_or_nested_assignment_rejected(self):
        for code in ("DISPATCH_CONFIRM = False\nDISPATCH_CONFIRM = False\n",
                     "if True:\n    DISPATCH_CONFIRM = False\n",
                     "DISPATCH_CONFIRM = bool(0)\n"):
            before = notebook(); before["cells"][0]["source"] = code
            with self.assertRaises(ValueError): audit(before, notebook(True))

    def test_wrong_direction_rejected(self):
        with self.assertRaises(ValueError): audit(notebook(True), notebook())

    def test_source_list_supported(self):
        before = notebook(); before["cells"][0]["source"] = [before["cells"][0]["source"]]
        self.assertTrue(audit(before, notebook(True))["only_launch_flag_changed"])

    def test_unicode_byte_offsets(self):
        before, after = notebook(), notebook(True)
        for item in (before, after): item["cells"][0]["source"] = 'label = "🚀"; ' + item["cells"][0]["source"]
        self.assertTrue(audit(before, after)["only_launch_flag_changed"])

    def test_input_not_mutated(self):
        before, after = notebook(), notebook(True)
        saved = copy.deepcopy(after)
        audit(before, after)
        self.assertEqual(after, saved)
