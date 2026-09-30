"""Conservative operation-level recovery evidence, independent of final solve status."""
import re
from pathlib import PurePosixPath


def normalized_path(value):
    if not isinstance(value, str) or not value or '\\' in value:
        return None
    path = PurePosixPath(value)
    if '..' in path.parts:
        return None
    if path.is_absolute():
        try:
            path = path.relative_to('/workspace')
        except ValueError:
            return None
    return str(path) if str(path) != '.' else None


def assess_recovery(rejection_observed, operation, changed_source_paths):
    """Input hashes must be captured around this operation, not final artifact hashes."""
    if rejection_observed is not True:
        return 'unproven: no observed rejection'
    if operation.get('tool') not in ('edit_file', 'write_file', 'run_command'):
        return 'unproven: not a modifying tool'
    if operation.get('accepted') is not True:
        return 'unproven: operation not acknowledged'
    target = normalized_path(operation.get('reported_path'))
    paths = {normalized_path(p) for p in changed_source_paths}
    if target is None or target not in paths:
        return 'unproven: exact source path not established'
    before, after = operation.get('before_sha256'), operation.get('after_sha256')
    valid = lambda value: isinstance(value, str) and re.fullmatch(r'[0-9a-f]{64}', value)
    if not valid(before) or not valid(after):
        return 'consistent with recovery; byte change unproven'
    if before == after:
        return 'unproven: operation did not change bytes'
    return 'observed byte change after rejection; correctness unproven'
