"""Run CPU-only public checks; never installs packages, contacts Kaggle or starts a model."""
import os
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parent.parent


def run(args, env=None):
    print('RUN', ' '.join(args), flush=True)
    subprocess.run([sys.executable,*args],cwd=ROOT,env=env,check=True)


def main():
    run(['scripts/check_public_repo.py'])
    run(['scripts/verify_releases.py'])
    run(['-m','unittest','discover','-s','tests','-v'])
    for enabled in ('0','1'):
        env=dict(os.environ,PILOT_TEST_NOTEBOOK_ENABLED=enabled)
        output=ROOT/'build'/f'pilot-synthetic-{enabled}.log'
        output.parent.mkdir(exist_ok=True)
        with output.open('w',encoding='utf-8') as handle:
            result=subprocess.run([sys.executable,'scripts/test_pilot_notebook.py'],cwd=ROOT,env=env,
                                  stdout=handle,stderr=subprocess.STDOUT)
        tail=output.read_text(encoding='utf-8').splitlines()[-3:]
        print(f'Synthetic artifact enabled={enabled}:', '\n'.join(tail), flush=True)
        if result.returncode:
            raise SystemExit(f'Failure; inspect {output}')
    print('All public checks passed. No real-model evaluation performed.')


if __name__=='__main__': main()
