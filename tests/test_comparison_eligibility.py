import unittest
from scripts.comparison_report import comparison_eligible, build_report


class EligibilityTests(unittest.TestCase):
    def record(self):
        return dict(task='invented', candidate='A', test_exit_code=0, grading_ran=True,
                    cleanup_ok=True, provenance_ok=True, resolved=True)

    def test_each_gate_independently_rejects(self):
        cases = [('test_exit_code', v) for v in (-1,2,3,4,5,True,None)] + [
            ('grading_ran',False), ('cleanup_ok',None), ('provenance_ok',False),
            ('failure_class','environment'), ('failure_class','unknown'),
            ('resolved',None), ('resolved',False)]
        for field,value in cases:
            with self.subTest(field=field,value=value):
                self.assertFalse(comparison_eligible(self.record() | {field:value})[0])

    def test_pass_and_fail_and_table_use_same_gate(self):
        for code in (0,1):
            row=self.record() | dict(test_exit_code=code,resolved=code==0)
            self.assertTrue(comparison_eligible(row)[0])
            self.assertTrue(build_report([row],[row])[0]['comparable'])
        row=self.record() | dict(test_exit_code=-1,resolved=False)
        result=build_report([row],[row])[0]
        self.assertFalse(result['comparable'])
        self.assertFalse(result['resolved'])  # Preserve raw flag, don't score it.
