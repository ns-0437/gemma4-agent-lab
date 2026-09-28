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

## Dispatch record: pilot v1 (2026-09-27)

The four-run A/B pilot was dispatched after explicit owner authorization. A forwarded template
containing authorization text was not treated as authorization; the hold was lifted in conversation.

| item | value |
|---|---|
| kernel | `gemma4-swe-agent-pilot` version 1, private, pushed once |
| dispatch-enabled notebook | `1321f80539a68bb8e7c35629a8b0960d26045fb7acd77d0959b8fe161019c322` |
| dispatch-disabled notebook (pre-flip) | `30b500e01d762bee70ec406f47bbe7d690a8e5cdbe40a3aa430cf0b0d3147d24` |
| candidate A | `f6392b8207a91a521c2434e1b5ce9f3f8d68d881298615725230d678bf04b3e3` |
| candidate B | `194b420a487c48f475267bf2a35b33a813c13bd2e2410e23d0ea405835bf913d` |

Enabling changed exactly one line in one cell (`DISPATCH_CONFIRM False -> True`); a whole-notebook
diff confirmed nothing else moved, and the saved shipping flag was read directly rather than inferred
from the test suite, which overrides that flag in its simulated namespaces. Candidate hashes were
recomputed after regeneration and were unchanged.

The notebook sat queued for roughly nineteen hours before starting. No account-level blocker was
found: no warning on the version page, no competing session, and ample accelerator quota. Other
entrants reported multi-hour four-L4 queues in the same window. The cause remains unconfirmed.

## Two claims corrected after review

**Accelerator metadata is a request, not an allocation.** The notebook version page showing
`GPU L4 x4` states what was asked for. Only runtime values establish what was granted: device count,
device names, and the tensor-parallel size the server actually starts with. The pilot's own record
shows four devices and `tp=4`; earlier wording that treated the settings label as proof was wrong.

**A single quota reading cannot establish what a run was charged.** Observing 39 minutes used out of
30 hours shows headroom, nothing more. Attributing consumption to one run needs a before-and-after
delta, and no pre-dispatch reading was taken, so the pilot's charge is unavailable. Take the reading
before dispatch in future runs.

An earlier note also gave a "conservative maximum of about 1.5 hours" for the four runs. That figure
was unsupported and is withdrawn. The session setting admits new runs; it does not cap wall-clock
time, terminate a run in progress, or end the Kaggle session, and CPU setup inside a GPU notebook
consumes quota as well.

## When the guard stopped the run

After run 2 the log recorded `Stopping further dispatch after infrastructure/provenance failure`
and rows 3 and 4 never started. The guard fired because the failed run produced only one setup
observation: grading never began, so the grading-phase import probe never ran and
`both_setup_imports_verified` stayed false.

The guard behaved as designed and preserved every artifact already written. Whether it should have
fired is a separate question. A context-window error is a candidate configuration failure, not a
broken sandbox, and treating the two alike cost both remaining runs on an unaffected task.

The distinction to encode next time is between provenance or setup failures, which invalidate later
runs, and per-candidate request failures, which do not. Widening the guard is only safe once that
separation exists; until then stopping early remains the conservative default.

## Competition submission

Freeze a newly named candidate, validate and officially compile it, then generate from that frozen
directory with `--source`. After an authorized notebook run, download the actual output archive
and match its full hash before a separately authorized competition submission. Keep the best known
scored release intact. This repository and CI do not submit anything automatically.

## Public documentation deployment

GitHub Pages publishes only docs/ and the release manifest. It never deploys ignored data, scripts,
credentials or generated notebooks. The explorer reads the versioned result ledger and hash manifest.
Change those records only when new evidence exists; null means unmeasured, never zero performance.
