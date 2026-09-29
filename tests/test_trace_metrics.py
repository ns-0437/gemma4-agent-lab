import unittest
from scripts.trace_metrics import summarize_trace


def event(name='edit_file', path='src/demo.py', response=None):
    return dict(tool_calls=[dict(function_name=name, arguments=dict(filepath=path))],
                observation=dict(content=response))


class TraceMetricsTests(unittest.TestCase):
    def test_plain_error_rejections_not_successful_edits(self):
        step = event(response='{"error":"mandatory parameter old_string missing"}')
        r = summarize_trace(dict(steps=[step] * 42))
        self.assertEqual(r['counts']['rejected_observations'], 42)
        self.assertEqual(r['counts']['file_edit_attempts'], 42)
        self.assertEqual(r['counts'].get('acknowledged_repo_edit_calls', 0), 0)
        self.assertIsNone(r['successful_source_changes'])

    def test_scratch_and_shell_not_repository_edits(self):
        steps = [event(path='/tmp/repro.py', response={'status':'ok'}),
                 event(name='run_command', response={'status':'ok'}),
                 event(path='../outside.py', response={'status':'ok'}),
                 event(path='/workspace/src/x.py', response={'status':'ok'})]
        self.assertEqual(summarize_trace(dict(steps=steps))['counts']['acknowledged_repo_edit_calls'], 1)

    def test_unknown_and_multi_call_are_not_attributed(self):
        step = event(response={'status':'ok'})
        step['tool_calls'] *= 2
        r = summarize_trace(dict(steps=[step, event(response='broken json')]))['counts']
        self.assertEqual(r['unknown_observations'], 1)
        self.assertEqual(r['unattributed_observations'], 1)
        self.assertNotIn('acknowledged_repo_edit_calls', r)
