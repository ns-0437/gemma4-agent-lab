# Auditing a notebook launch

The standalone `scripts/audit_notebook_arming.py` command compares a saved disabled notebook
with an armed copy without importing or executing any cell:

```powershell
python scripts/audit_notebook_arming.py path/to/disabled.ipynb path/to/armed.ipynb
```

It accepts exactly one top-level `DISPATCH_CONFIRM = False` to `True` transition in the
same code cell. Other cell content, outputs and metadata must remain equal. Jupyter's string
and list-of-lines source representations are normalized; each input's raw file SHA-256 is
also printed. JSON whitespace can differ without changing the parsed notebook.

The audit rejects duplicate assignments, computed flags, nested assignments, changed code,
changed metadata and a reversed transition. Unicode before the flag is handled using AST
byte offsets. The tests use synthetic notebooks only.

A passing audit is a structural check, not authorization to spend quota. It cannot prove
that unrelated code honors the flag, that code is safe to execute, that a model will solve a
task, or that uploaded bytes equal the local file. Review the disabled baseline first, obtain
the owner's authorization separately, and compare the uploaded artifact's hash where available.
Do not upload private notebook bundles to this public repository.

This utility is not wired into the private Kaggle comparison generator. It does not start a
session, push a notebook, submit a competition entry or poll Kaggle.
