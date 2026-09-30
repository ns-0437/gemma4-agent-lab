"""Separate failed checks from a grading path that was never exercised."""


def instrument_state(checks, grading_ran, grading_provenance):
    if not isinstance(checks, dict) or not checks:
        raise ValueError('supply named required checks')
    failed = [name for name, value in checks.items() if value is False]
    unknown = [name for name, value in checks.items() if type(value) is not bool]
    if grading_provenance is False:
        failed.append('grading_provenance')
    if failed:
        state = 'demonstrated_failure'
    elif unknown or type(grading_ran) is not bool:
        state = 'incomplete_evidence'
    elif not grading_ran:
        state = 'grading_path_unobserved'
    elif grading_provenance is not True:
        state = 'incomplete_evidence'
    else:
        state = 'observed_checks_passed'
    return {'state': state, 'failed_checks': failed, 'unknown_checks': unknown,
            'graded_path_verified': state == 'observed_checks_passed'}
