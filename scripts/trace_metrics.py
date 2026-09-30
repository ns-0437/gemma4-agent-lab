"""Conservative counts from recorded tool events, not inferred repository changes."""
import json
from collections import Counter
from pathlib import PurePosixPath


def summarize_trace(trace):
    counts = Counter()
    calls = Counter()
    payloads = Counter()
    for step in trace.get('steps', []):
        tool_calls = step.get('tool_calls', [])
        counts['tool_calls'] += len(tool_calls)
        for call in tool_calls:
            calls[call.get('function_name', 'unknown')] += 1
            signature = json.dumps([call.get('function_name'), call.get('arguments')],
                                   sort_keys=True, ensure_ascii=False)
            payloads[signature] += 1
        if not tool_calls:
            continue
        content = step.get('observation', {}).get('content')
        try:
            response = json.loads(content) if isinstance(content, str) else content
        except (ValueError, TypeError):
            response = None
        if not isinstance(response, dict):
            counts['unknown_observations'] += 1
            continue
        rejected = bool(response.get('error')) or response.get('status') == 'error'
        counts['rejected_observations'] += int(rejected)
        if len(tool_calls) != 1:
            counts['unattributed_observations'] += 1
            continue
        call = tool_calls[0]
        if call.get('function_name') not in ('edit_file', 'write_file'):
            continue
        counts['file_edit_attempts'] += 1
        path = PurePosixPath(call.get('arguments', {}).get('filepath', ''))
        in_repo = (str(path) not in ('', '.') and '..' not in path.parts
                   and (not path.is_absolute() or str(path).startswith('/workspace/')))
        # An acknowledgement is still not proof of a changed source diff.
        if in_repo and response.get('status') == 'ok' and not rejected:
            counts['acknowledged_repo_edit_calls'] += 1
    counts['submit_patch_calls'] = calls['submit_patch']
    counts['distinct_payloads'] = len(payloads)
    counts['repeated_payload_calls'] = sum(n - 1 for n in payloads.values())
    counts['most_frequent_payload_calls'] = max(payloads.values(), default=0)
    return {'counts': dict(counts), 'tools': dict(calls),
            'successful_source_changes': None,
            'limitation': 'Repeated payloads may be justified after state changes. Source changes require a diff; shell commands alone are not edit evidence.'}
