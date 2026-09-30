"""Review caller-supplied run records offline; write JSON to stdout, never mutate inputs."""
import argparse
import json
from pathlib import Path

try:
    from .comparison_report import build_report, key
    from .run_outcome import classify_run
    from .trace_metrics import summarize_trace
    from .holdout_guard import validate_development_tasks
    from .instrument_state import instrument_state
    from .patch_evidence import inspect_patch
    from .paired_summary import summarize_pairs
except ImportError:  # Direct script invocation.
    from comparison_report import build_report, key
    from run_outcome import classify_run
    from trace_metrics import summarize_trace
    from holdout_guard import validate_development_tasks
    from instrument_state import instrument_state
    from patch_evidence import inspect_patch
    from paired_summary import summarize_pairs


def review(payload):
    holdout = None
    if 'freeze' in payload:
        holdout = validate_development_tasks(list(dict.fromkeys(r['task'] for r in payload['plan'])),
                                             payload['freeze'])
    rows = build_report(payload['plan'], payload['runs'], payload.get('stop_reason'))
    records = {key(r):r for r in payload['runs']}
    for row in rows:
        record = records.get(key(row))
        if record is None:
            continue
        row['termination'] = classify_run(
            errors=[record.get('harness_error'), record.get('run_error')],
            environment_error=record.get('environment_error',False),
            provenance_ok=record.get('provenance_ok'), cleanup_ok=record.get('cleanup_ok'))
        # Independent infrastructure evidence must also disqualify pairing.
        if row['termination']['stop']:
            row['comparable'] = False
            row['comparison_reason'] = row['termination']['reason']
        row['trace_metrics'] = (summarize_trace(record['trace'])
                                if isinstance(record.get('trace'), dict) else None)
        if 'instrument_checks' in record:
            row['instrument'] = instrument_state(record['instrument_checks'], record.get('grading_ran'),
                                                 record.get('grading_provenance_ok'))
            if row['instrument']['state'] != 'observed_checks_passed':
                row['comparable'] = False
                row['comparison_reason'] = row['instrument']['state']
        if 'patch_text' in record:
            row['patch_evidence'] = inspect_patch(record['patch_text'], record.get('agent_patch_size'))
            if not row['patch_evidence']['syntax_valid']:
                row['comparable'] = False
                row['comparison_reason'] = 'patch integrity unconfirmed'
    output = {'rows':rows, 'holdout_check': holdout,
              'note':'A COMPLETE notebook is not evidence of a graded solve. No dispatch is performed.'}
    if 'pair_candidates' in payload:
        candidates = payload['pair_candidates']
        if not isinstance(candidates, list) or len(candidates) != 2:
            raise ValueError('pair_candidates must contain two candidate names')
        output['paired_summary'] = summarize_pairs(rows, *candidates)
    return output


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',type=Path)
    args=parser.parse_args()
    print(json.dumps(review(json.loads(args.input.read_text(encoding='utf-8'))),indent=2))
