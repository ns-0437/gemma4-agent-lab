"""Keep every planned run in denominators, including ungraded and missing runs."""
from collections import Counter


def summarize_pairs(rows, left, right):
    if left == right:
        raise ValueError('two different candidates are required')
    tasks = {}
    totals = {candidate: Counter(planned=0, not_attempted=0, ungraded=0, solved=0, unsolved=0)
              for candidate in (left, right)}
    for row in rows:
        candidate = row['candidate']
        if candidate not in totals:
            raise ValueError('unexpected candidate')
        pair = tasks.setdefault(row['task'], {})
        if candidate in pair:
            raise ValueError('duplicate task/candidate')
        if row.get('attempted') is not True:
            state = 'not_attempted'
        elif row.get('comparable') is not True:
            state = 'ungraded'
        elif type(row.get('resolved')) is not bool:
            raise ValueError('comparable outcome needs boolean resolution')
        else:
            state = 'solved' if row['resolved'] else 'unsolved'
        pair[candidate] = state
        totals[candidate]['planned'] += 1
        totals[candidate][state] += 1
    pairs = []
    for task, states in tasks.items():
        if set(states) != {left, right}:
            raise ValueError('plan must contain both candidates for every task')
        a, b = states[left], states[right]
        if a not in ('solved', 'unsolved') or b not in ('solved', 'unsolved'):
            verdict = 'undecided'
        elif a == b:
            verdict = 'tie'
        else:
            verdict = left if a == 'solved' else right
        pairs.append({'task': task, 'states': states, 'verdict': verdict})
    return {'candidates': {k: dict(v) for k, v in totals.items()}, 'pairs': pairs,
            'scope': 'Observed selected tasks only; no population or leaderboard projection.'}
