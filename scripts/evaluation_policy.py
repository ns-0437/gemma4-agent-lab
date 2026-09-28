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
