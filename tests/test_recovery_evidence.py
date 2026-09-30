import unittest
from scripts.recovery_evidence import assess_recovery


class RecoveryTests(unittest.TestCase):
    def operation(self, **changes):
        return dict(dict(tool='write_file', accepted=True, reported_path='/workspace/src/a.py',
                         before_sha256='a'*64, after_sha256='b'*64), **changes)

    def test_read_and_same_basename_do_not_establish_recovery(self):
        for operation in (self.operation(tool='read_file'), self.operation(reported_path='other/a.py')):
            self.assertTrue(assess_recovery(True, operation, ['src/a.py']).startswith('unproven'))

    def test_acknowledgment_and_noop_are_not_changes(self):
        op = self.operation(before_sha256=None, after_sha256=None, size=100)
        self.assertIn('byte change unproven', assess_recovery(True, op, ['src/a.py']))
        self.assertIn('did not change', assess_recovery(True, self.operation(after_sha256='a'*64), ['src/a.py']))

    def test_shell_with_operation_level_evidence_can_qualify(self):
        self.assertIn('observed byte change', assess_recovery(True, self.operation(tool='run_command'), ['src/a.py']))

    def test_rejection_acceptance_and_safe_path_are_required(self):
        self.assertIn('no observed rejection', assess_recovery(False, self.operation(), ['src/a.py']))
        self.assertIn('not acknowledged', assess_recovery(True, self.operation(accepted=False), ['src/a.py']))
        self.assertIn('not established', assess_recovery(True, self.operation(reported_path='../src/a.py'), ['../src/a.py']))
