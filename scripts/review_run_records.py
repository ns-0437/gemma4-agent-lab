"""Review caller-supplied run records offline; write JSON to stdout, never mutate inputs."""
import argparse
import json
from pathlib import Path

try:
    from .comparison_report import build_report, key
    from .run_outcome import classify_run
    from .trace_metrics import summarize_trace
except ImportError:  # Direct script invocation.
    from comparison_report import build_report, key
    from run_outcome import classify_run
    from trace_metrics import summarize_trace


def review(payload):
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
    return {'rows':rows, 'note':'A COMPLETE notebook is not evidence of a graded solve. No dispatch is performed.'}


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',type=Path)
    args=parser.parse_args()
    print(json.dumps(review(json.loads(args.input.read_text(encoding='utf-8'))),indent=2))
