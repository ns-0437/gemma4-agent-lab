"""Inspect text-patch syntax with Git; never apply it or claim applicability."""
import subprocess
import tempfile
from pathlib import PurePosixPath


def inspect_patch(text, recorded_chars):
    result = {'size_matches': type(recorded_chars) is int and recorded_chars == len(text),
              'chars': len(text), 'bytes': len(text.encode('utf-8')),
              'syntax_valid': False, 'changed_paths': [], 'application_verified': None,
              'reason': None}
    if not result['size_matches']:
        result['reason'] = 'missing, invalid or mismatched character count'
        return result
    if not text.strip():
        result['reason'] = 'empty patch'
        return result
    with tempfile.TemporaryDirectory(prefix='patch-inspect-') as directory:
        checked = subprocess.run(['git', 'apply', '--numstat', '-z', '-'],
                                 input=text.encode('utf-8'), cwd=directory,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if checked.returncode:
        result['reason'] = checked.stderr.decode('utf-8', errors='replace').strip()
        return result
    for row in checked.stdout.decode('utf-8').split('\0'):
        if not row:
            continue
        fields = row.split('\t', 2)
        if len(fields) != 3 or not all(n.isdecimal() for n in fields[:2]):
            result['reason'] = 'only ordinary text-file diffs are supported'
            return result
        added, removed, path = fields
        parts = PurePosixPath(path)
        if parts.is_absolute() or '..' in parts.parts or '\\' in path or ':' in path:
            result['reason'] = 'unsafe or unsupported path'
            return result
        if int(added) + int(removed):
            result['changed_paths'].append(path)
    result['syntax_valid'] = bool(result['changed_paths'])
    result['reason'] = 'syntax only; applicability unverified' if result['syntax_valid'] else 'no changed lines'
    return result
