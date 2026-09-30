import unittest
from scripts.holdout_guard import validate_development_tasks


class HoldoutTests(unittest.TestCase):
    def test_accepts_development_without_mutating_freeze(self):
        freeze = {'protected_holdout': ['reserved']}
        self.assertTrue(validate_development_tasks(['dev'], freeze)['disjoint'])
        self.assertEqual(freeze, {'protected_holdout': ['reserved']})

    def test_rejects_overlap_instead_of_moving_task(self):
        with self.assertRaisesRegex(ValueError, 'reserved'):
            validate_development_tasks(['dev', 'reserved'], {'protected_holdout': ['reserved']})

    def test_missing_freeze_and_duplicate_inputs_fail_closed(self):
        for selected, freeze in [(['dev'], {}), ([], {'protected_holdout': []}),
                                (['x', 'x'], {'protected_holdout': []}),
                                (['x'], {'protected_holdout': ['y', 'y']})]:
            with self.subTest(selected=selected, freeze=freeze), self.assertRaises(ValueError):
                validate_development_tasks(selected, freeze)
