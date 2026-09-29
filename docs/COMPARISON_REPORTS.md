# Complete comparison reports

Use `python scripts/comparison_report.py input.json` to print one row per planned task/candidate
pair. The input has `plan` and `runs` arrays, each with `task` and `candidate` strings, plus an
optional `stop_reason`. Results may carry `outcome` and a boolean or null `resolved` field.

Rows follow the plan, even if results arrive out of order. Duplicate planned pairs, duplicate
results and results outside the plan are rejected. Missing results get `attempted: false` with
null outcome and resolution; the utility never turns missing evidence into a failed solve.
A present record means attempted according to the caller, not independently verified execution.

For example, an eight-run plan stopped after its first environment error still produces eight
rows: one attempted and seven unavailable. A measured `resolved: false` remains distinct from
an unknown result. The accompanying tests use synthetic task names and include early-stop,
duplicate, unplanned-result and ordering cases.

Keep raw evidence separately. This small utility is a presentation contract, not a grading
engine: it does not inspect traces, prove provenance, identify failure causes, compute a solve
rate, or establish why a run is missing. It is not integrated into the private Kaggle notebook.
No competition data, reference patches or private traces belong in this repository.

## Grading eligibility and integrated offline review

Rows now include `comparable` and `comparison_reason`. Eligibility requires explicit
`grading_ran`, `cleanup_ok`, `provenance_ok`, an integer `test_exit_code` of 0 or 1, and a
consistent boolean `resolved`. A raw false flag on an ungraded run is preserved but excluded.

`python scripts/review_run_records.py input.json` additionally classifies `harness_error` and
`run_error`, and summarizes an optional inline `trace` object. It accepts the same plan/runs
envelope. Explicit `environment_error` overrides candidate termination evidence. Unknown errors
stop the suggested dispatch decision without being labelled as proven environment failures.
It only prints a report: it never starts or stops runs. The tests execute the CLI and verify that
input bytes remain unchanged.

`python scripts/verify_evidence.py /path/to/arm` checks the `artifact_sha256` entries created by
`control_evidence.write_arm`. Hash integrity is separate from grading validity. Missing files,
changed bytes and unsafe paths are rejected. These public utilities are not automatically wired
into the private competition notebook.
