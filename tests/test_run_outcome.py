import unittest
from scripts.run_outcome import classify_run


class OutcomeTests(unittest.TestCase):
    def classify(self, **kw):
        return classify_run(**(dict(provenance_ok=True, cleanup_ok=True) | kw))

    def test_missing_submission_continues(self):
        r = self.classify(errors=['Agent completed execution without calling submit_patch.'])
        self.assertEqual(r, dict(kind='candidate', stop=False, reason='missing_submission'))

    def test_candidate_does_not_hide_independent_failure(self):
        for field in ('environment_error', 'provenance_ok', 'cleanup_ok'):
            r = self.classify(errors=['Agent completed execution without calling submit_patch.'],
                              **{field: field == 'environment_error'})
            self.assertEqual(r['kind'], 'environment')
            self.assertTrue(r['stop'])

    def test_unknown_is_not_claimed_as_environment(self):
        r = self.classify(errors=['Agent exceeded turns budget (60 turns)', 'unrecognized failure'])
        self.assertEqual(r['kind'], 'unknown')
        self.assertTrue(r['stop'])

    def test_unconfirmed_state_stops(self):
        for field in ('cleanup_ok', 'provenance_ok'):
            self.assertTrue(self.classify(**{field: None})['stop'])

    def test_context_wrapper_and_clean_completion(self):
        r = self.classify(errors=['Unexpected worker error: ContextWindowExceededError'])
        self.assertEqual(r['reason'], 'context_limit')
        self.assertFalse(r['stop'])
        self.assertEqual(self.classify()['kind'], 'completed')
