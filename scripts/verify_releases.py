"""Rebuild frozen archive bytes in memory and compare with the public release manifest."""
from pathlib import Path
import hashlib
import io
import json
import zipfile

ROOT = Path(__file__).resolve().parent.parent


def archive_bytes(root):
    root = Path(root).resolve()
    if not (root / 'agent.yaml').is_file():
        raise ValueError(f'Missing root agent: {root}')
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as z:
        for p in sorted(root.rglob('*'), key=lambda p: p.relative_to(root).as_posix()):
            if p.is_symlink():
                raise ValueError('Symlinks are not allowed in a frozen release')
            if not p.is_file():
                continue
            if p.suffix not in {'.yaml', '.yml', '.md', '.txt', '.py', '.json'}:
                raise ValueError(f'Unexpected file type: {p.suffix}')
            entry = zipfile.ZipInfo(p.relative_to(root).as_posix(), (1980, 1, 1, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.external_attr = 0o644 << 16
            z.writestr(entry, p.read_bytes())
    return buffer.getvalue()


def main():
    records = json.loads((ROOT / 'releases/manifest.json').read_text())['releases']
    for record in records:
        digest = hashlib.sha256(archive_bytes(ROOT / record['directory'])).hexdigest()
        if digest != record['sha256']:
            raise SystemExit(f"Hash mismatch: {record['id']} {digest}")
        print(f"OK {record['id']} {digest}")


if __name__ == '__main__':
    main()
