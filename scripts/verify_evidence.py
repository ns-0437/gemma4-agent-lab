"""Read-only verification of an arm.json artifact manifest."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath


def verify_arm(directory):
    directory = Path(directory).resolve()
    record = json.loads((directory/'arm.json').read_text(encoding='utf-8'))
    hashes = record.get('artifact_sha256')
    if not isinstance(hashes, dict) or not hashes:
        raise ValueError('nonempty artifact_sha256 manifest required')
    errors = []
    for name, expected in hashes.items():
        parts = PurePosixPath(name)
        if parts.is_absolute() or '..' in parts.parts or '\\' in name or ':' in name:
            raise ValueError('unsafe artifact path')
        path = (directory/name).resolve()
        if not path.is_relative_to(directory):
            raise ValueError('artifact escapes evidence directory')
        if not path.is_file():
            errors.append(f'{name}: missing')
        elif hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            errors.append(f'{name}: hash mismatch')
    return errors


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    args = parser.parse_args()
    errors = verify_arm(args.directory)
    print('\n'.join(errors) if errors else 'All declared artifacts match; grading validity is a separate check.')
    raise SystemExit(bool(errors))
