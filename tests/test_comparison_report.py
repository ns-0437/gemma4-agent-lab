import copy
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from comparison_report import build_report


class ComparisonReportTests(unittest.TestCase):
    def setUp(self):
        self.plan = [dict(task=f"synthetic_{i}", candidate=c)
                     for i in range(4) for c in ("A", "B")]

    def test_early_stop_keeps_eight_rows(self):
        run = dict(self.plan[0], outcome="environment", resolved=None)
        rows = build_report(self.plan, [run], "sandbox failure")
        self.assertEqual(len(rows), 8)
        self.assertEqual(sum(r["attempted"] for r in rows), 1)
        for row in rows[1:]:
            self.assertIsNone(row["resolved"])
            self.assertIsNone(row["outcome"])
            self.assertEqual(row["stop_reason"], "sandbox failure")

    def test_duplicate_plan_rejected(self):
        with self.assertRaises(ValueError): build_report(self.plan * 2, [])

    def test_duplicate_result_rejected(self):
        with self.assertRaises(ValueError): build_report(self.plan, [self.plan[0]] * 2)

    def test_unplanned_result_rejected(self):
        with self.assertRaises(ValueError): build_report(self.plan, [dict(task="other", candidate="A")])

    def test_false_is_distinct_from_unknown(self):
        rows = build_report(self.plan, [dict(self.plan[0], resolved=False), self.plan[1]])
        self.assertIs(rows[0]["resolved"], False)
        self.assertIsNone(rows[1]["resolved"])
        self.assertTrue(rows[1]["attempted"])
        self.assertFalse(rows[2]["attempted"])

    def test_plan_order_not_result_order(self):
        rows = build_report(self.plan, list(reversed(self.plan)))
        self.assertEqual([(r["task"], r["candidate"]) for r in rows],
                         [(r["task"], r["candidate"]) for r in self.plan])

    def test_bad_identity_or_resolution_rejected(self):
        for bad in (dict(task="", candidate="A"), dict(task=1, candidate="A")):
            with self.assertRaises(ValueError): build_report([bad], [])
        with self.assertRaises(ValueError): build_report(self.plan, [dict(self.plan[0], resolved="false")])

    def test_inputs_unchanged(self):
        saved = copy.deepcopy(self.plan)
        build_report(self.plan, self.plan)
        self.assertEqual(self.plan, saved)
