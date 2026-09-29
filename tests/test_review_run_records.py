import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from scripts.review_run_records import review


class ReviewIntegrationTests(unittest.TestCase):
    def payload(self):
        plan=[dict(task=f'invented_{i}',candidate=c) for i in range(4) for c in 'AB']
        run=plan[0] | dict(harness_error='Agent completed execution without calling submit_patch.',
                          test_exit_code=-1,grading_ran=False,cleanup_ok=True,provenance_ok=True,
                          resolved=False)
        return dict(plan=plan,runs=[run])

    def test_missing_submission_keeps_plan_without_inventing_grade(self):
        rows=review(self.payload())['rows']
        self.assertEqual(len(rows),8)
        self.assertFalse(rows[0]['termination']['stop'])
        self.assertFalse(rows[0]['comparable'])
        self.assertEqual(sum(r['attempted'] for r in rows),1)
        self.assertIsNone(rows[1]['resolved'])

    def test_independent_environment_evidence_disqualifies(self):
        p=self.payload()
        p['runs'][0].update(test_exit_code=0,grading_ran=True,resolved=True,environment_error=True)
        row=review(p)['rows'][0]
        self.assertTrue(row['termination']['stop'])
        self.assertFalse(row['comparable'])

    def test_cli_does_not_modify_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'fixture.json'
            path.write_text(json.dumps(self.payload()),encoding='utf-8')
            before=hashlib.sha256(path.read_bytes()).hexdigest()
            script=Path(__file__).resolve().parents[1]/'scripts/review_run_records.py'
            result=subprocess.run([sys.executable,str(script),str(path)],capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertEqual(len(json.loads(result.stdout)['rows']),8)
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),before)
