import unittest
from scripts.instrument_state import instrument_state


class InstrumentTests(unittest.TestCase):
    def test_unexercised_grading_is_not_broken(self):
        result = instrument_state({'controls': True, 'cleanup': True}, False, None)
        self.assertEqual(result['state'], 'grading_path_unobserved')
        self.assertFalse(result['graded_path_verified'])

    def test_observed_failure_wins_over_unobserved_grading(self):
        self.assertEqual(instrument_state({'cleanup': False}, False, None)['state'],
                         'demonstrated_failure')

    def test_grading_needs_provenance(self):
        self.assertEqual(instrument_state({'controls': True}, True, None)['state'], 'incomplete_evidence')
        self.assertTrue(instrument_state({'controls': True}, True, True)['graded_path_verified'])

    def test_truthy_unknown_is_not_pass(self):
        self.assertEqual(instrument_state({'controls': 1}, True, True)['state'], 'incomplete_evidence')
        with self.assertRaises(ValueError):
            instrument_state({}, False, None)
