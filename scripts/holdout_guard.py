"""Reject development plans that consume protected evaluation tasks."""


def validate_development_tasks(selected, freeze):
    protected = freeze.get('protected_holdout')
    if not isinstance(protected, list) or not all(isinstance(t, str) and t.strip() for t in protected):
        raise ValueError('protected_holdout must be an explicit list of task IDs')
    if not selected or not all(isinstance(t, str) and t.strip() for t in selected):
        raise ValueError('select nonempty task IDs')
    if len(selected) != len(set(selected)):
        raise ValueError('duplicate selected task')
    if len(protected) != len(set(protected)):
        raise ValueError('duplicate protected task')
    overlap = sorted(set(selected) & set(protected))
    if overlap:
        raise ValueError('protected hold-out overlap: ' + ', '.join(overlap))
    return {'selected': list(selected), 'protected_count': len(protected), 'disjoint': True}
