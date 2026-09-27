# Release and experiment operations

## Ordinary code changes

1. Create a focused branch. Keep candidate behavior, evaluation fixes and presentation changes separate.
2. Run `python scripts/run_checks.py` and inspect the Git diff.
3. Open a PR with validation evidence and limitations. Let both CI platforms pass before merging.
4. Never backdate commits or portray an AI-assisted import as historical independent human reviews.

## Notebook generation

Set `KAGGLE_KERNEL_OWNER` explicitly in your shell. An unset owner produces the deliberate
`YOUR_KAGGLE_USERNAME` placeholder. No script stores credentials or performs `kaggle kernels push`.
Use the Kaggle CLI's supported authentication separately; do not add its files to this repository.

The pilot defaults to `DISPATCH_CONFIRM=False`. This prevents vLLM startup, not GPU allocation:
a notebook requested on GPU hardware may consume quota during CPU setup. Authorization is a
separate human decision. An admission deadline does not forcibly stop an in-flight process.

## Authorized four-run pilot

Enable the generator deliberately, regenerate once, rerun tests, and separately inspect the saved
shipping flag. Tests override flags in synthetic namespaces, so passing tests alone cannot prove
the shipping notebook is enabled. Record its full hash and the returned Kaggle kernel/version.

Push once. On ambiguous response inspect status before retrying. Stop further dispatch on setup,
provenance or server failure. Preserve ordinary wrong answers as results. Do not expand the run or
restart polling without authorization. Download artifacts locally; repair reports offline first.

## Competition submission

Freeze a newly named candidate, validate and officially compile it, then generate from that frozen
directory with `--source`. After an authorized notebook run, download the actual output archive
and match its full hash before a separately authorized competition submission. Keep the best known
scored release intact. This repository and CI do not submit anything automatically.

## Public documentation deployment

GitHub Pages publishes only docs/ and the release manifest. It never deploys ignored data, scripts,
credentials or generated notebooks. The explorer reads the versioned result ledger and hash manifest.
Change those records only when new evidence exists; null means unmeasured, never zero performance.
