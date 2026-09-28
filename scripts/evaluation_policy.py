"""Data-free evaluation selection. Callers supply task metadata, never answer keys."""
from collections import defaultdict, deque
from hashlib import sha256

def screening_order(rows, cap):
    """Interleave repository/size strata without depending on input ordering."""
    if cap < 0:
        raise ValueError('cap must be nonnegative')
    groups = defaultdict(list)
    seen = set()
    for row in rows:
        if row['id'] in seen:
            raise ValueError('duplicate task id')
        seen.add(row['id'])
        groups[(row['repo'], row['size'])].append(row)
    queues = [deque(sorted(groups[k], key=lambda r: (sha256(r['id'].encode()).hexdigest(), r['id'])))
              for k in sorted(groups)]
    result = []
    while any(queues) and len(result) < cap:
        for queue in queues:
            if queue and len(result) < cap:
                result.append(queue.popleft())
    return result


def classify_controls(baseline, reference):
    """Mechanical eligibility only; a reviewer must establish failure relevance."""
    reasons=[]
    for name, arm, expected_exit in [('baseline',baseline,1),('reference',reference,0)]:
        if arm.get('exception'): reasons.append(f'{name}: exception')
        if arm.get('import_in_checkout') is not True: reasons.append(f'{name}: checkout unverified')
        for field in ['patch_rc','test_patch_rc']:
            if arm.get(field) != 0: reasons.append(f'{name}: {field} missing or nonzero')
        if arm.get('pytest_exit') != expected_exit: reasons.append(f'{name}: unexpected pytest exit')
        nodes=arm.get('nodes') or {}
        if not nodes: reasons.append(f'{name}: no nodes')
        if any(v not in {'passed','failed','skipped'} for v in nodes.values()):
            reasons.append(f'{name}: errored or unknown node')
        if name=='reference' and 'failed' in nodes.values(): reasons.append('reference: failed node')
        if arm.get('collection_error'): reasons.append(f'{name}: collection error')
    targets=sorted(n for n,v in (baseline.get('nodes') or {}).items()
                   if v=='failed' and (reference.get('nodes') or {}).get(n)=='passed')
    if not targets: reasons.append('no failure-to-pass nodes')
    return {'mechanically_eligible':not reasons,'reasons':reasons,'target_nodes':targets,
            'failure_relevance':'review_required'}
