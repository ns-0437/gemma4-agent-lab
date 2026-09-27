"""Invented control/task evidence for CPU-only public regression tests.

Names mirror the pilot's selected IDs to exercise its routing. Contents, node names,
paths and results below are synthetic, not copied competition task rows or gold patches.
Never use this evidence to generate or authorize a real Kaggle evaluation.
"""
import hashlib
import json
from pathlib import Path
import make_pilot_notebook as generator

ROOT = Path(__file__).resolve().parent.parent


def notebook_fixture():
    tasks=[]
    for tid,repo in [('requests_7309','psf/requests'),('rich_3471','Textualize/rich')]:
        tasks.append(dict(instance_id=tid,repo=repo,base_commit='deadbeef',
            problem_statement='Synthetic fixture: normalize a widget value.',hints_text='',
            patch='--- a/pkg/widget.py\n+++ b/pkg/widget.py\n+        value = normalize(value)\n',
            test_patch='--- a/tests/test_widget.py\n+++ b/tests/test_widget.py\n+def test_widget():\n+    assert True\n'))
    evidence={}
    for t in tasks:
        base={'workspace_real':'/tmp/synthetic/workspace','agent_pkg_file':'/tmp/synthetic/workspace/pkg/__init__.py',
              'pytest_pkg_file':'/tmp/synthetic/workspace/pkg/__init__.py','n_cases':1,'errored':[]}
        evidence[t['instance_id']]={
            'negative':dict(base,pytest_exit=1,failed_nodes=['synthetic::test_widget'],passed_nodes=[],failed=['test_widget']),
            'positive':dict(base,pytest_exit=0,failed_nodes=[],passed_nodes=['synthetic::test_widget'],failed=[])}
    hashes={t['instance_id']:hashlib.sha256(json.dumps({k:t[k] for k in
        ('repo','base_commit','problem_statement','hints_text','patch','test_patch')},sort_keys=True).encode()).hexdigest() for t in tasks}
    bundles={}
    for name in ('A','B'):
        b64,sha=generator.bundle(ROOT/f'releases/pilot_{name}')
        bundles[name]={'b64':b64,'sha256':sha}
    selected=generator.TASKS.replace('__TASKS__',json.dumps([t['instance_id'] for t in tasks]))
    selected=selected.replace('__EVIDENCE__',json.dumps(evidence)).replace('__TASK_HASHES__',json.dumps(hashes))
    cells=[generator.CFG,generator.INSTALL,generator.VERIFY,generator.COMMON,selected,generator.LEAK,
           generator.CANDS.replace('__BUNDLES__',json.dumps(bundles)),generator.REPAIR,generator.PRECOND,
           generator.SERVER,generator.RUN,generator.REPORT]
    return {'cells':[{'cell_type':'code','source':c.splitlines(keepends=True)} for c in cells]}
