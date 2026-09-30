import unittest
from scripts.paired_summary import summarize_pairs


def row(task, candidate, **changes):
    return dict(dict(task=task, candidate=candidate, attempted=True, comparable=True, resolved=True), **changes)


class PairTests(unittest.TestCase):
    def test_missing_grade_never_becomes_opponents_win(self):
        rows = [row('one', 'A'), row('one', 'S', comparable=False, resolved=False),
                row('two', 'A', attempted=False), row('two', 'S', attempted=False)]
        result = summarize_pairs(rows, 'A', 'S')
        self.assertEqual([p['verdict'] for p in result['pairs']], ['undecided', 'undecided'])
        self.assertEqual(result['candidates']['A']['planned'], 2)
        self.assertEqual(result['candidates']['A']['solved'], 1)
        self.assertEqual(result['candidates']['S']['ungraded'], 1)
        self.assertEqual(result['candidates']['S']['not_attempted'], 1)

    def test_win_and_failed_tie_stay_distinct(self):
        rows = [row('one', 'A', resolved=False), row('one', 'S'),
                row('two', 'A', resolved=False), row('two', 'S', resolved=False)]
        self.assertEqual([p['verdict'] for p in summarize_pairs(rows, 'A', 'S')['pairs']], ['S', 'tie'])

    def test_incomplete_or_duplicate_plan_rejected(self):
        for rows in ([row('one', 'A')], [row('one', 'A'), row('one', 'A')]):
            with self.assertRaises(ValueError):
                summarize_pairs(rows, 'A', 'S')
