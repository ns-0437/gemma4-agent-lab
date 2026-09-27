"""Check tracked files only: no competition payloads, secrets, oversized blobs or broken docs."""
from pathlib import Path
import re
import subprocess

ROOT=Path(__file__).resolve().parent.parent
MAX_BYTES=1_000_000
DENIED_ROOTS={'reference','data','competition_data','snapshots','graphs','embeddings','wheels','models','runs','artifacts','build','.venv','.kaggle'}
DENIED_SUFFIXES={'.ipynb','.jsonl','.safetensors','.bin','.pt','.pth','.whl','.zip','.tgz','.tar','.gz','.parquet','.pem','.key'}
SECRET_PATTERNS=[re.compile(r'gh[pousr]_[A-Za-z0-9]{24,}'),re.compile(r'AIza[A-Za-z0-9_-]{30,}'),
                 re.compile(r'-----BEGIN [A-Z ]*PRIVATE KEY-----')]


def tracked_files():
    result=subprocess.run(['git','ls-files','-z'],cwd=ROOT,capture_output=True,check=True)
    return [Path(p) for p in result.stdout.decode().split('\0') if p]


def violations(relative, data):
    path=Path(relative);issues=[]
    if path.parts[0] in DENIED_ROOTS or path.suffix.lower() in DENIED_SUFFIXES:
        issues.append('restricted payload path')
    if path.name in {'kaggle.json','access_token','.env'} or (path.name.startswith('.env.') and path.name!='.env.example'):
        issues.append('credential/environment path')
    if len(data)>MAX_BYTES: issues.append('file exceeds 1 MB code-only limit')
    text=data.decode('utf-8',errors='replace')
    if any(p.search(text) for p in SECRET_PATTERNS): issues.append('credential-shaped content')
    return issues


def missing_markdown_links(path):
    text=path.read_text(encoding='utf-8')
    missing=[]
    for raw in re.findall(r'\]\(([^)]+)\)',text):
        target=raw.strip('<>').split('#',1)[0]
        if not target or '://' in target or target.startswith('mailto:'): continue
        if not (path.parent/target).exists(): missing.append(target)
    return missing


def main():
    paths=tracked_files();errors=[];total=0
    for rel in paths:
        data=(ROOT/rel).read_bytes();total+=len(data)
        errors.extend(f'{rel}: {e}' for e in violations(rel,data))
        if rel.suffix=='.md':
            errors.extend(f'{rel}: missing link {x}' for x in missing_markdown_links(ROOT/rel))
    if errors: raise SystemExit('\n'.join(errors))
    print(f'Public boundary OK: {len(paths)} tracked files, {total:,} bytes; no restricted payload paths or detected credential patterns.')


if __name__=='__main__': main()
