# Offline evidence review

Run `python scripts/review_run_records.py input.json` to emit a review to stdout.
The input is not modified and no model or network request is made. The patch
inspector invokes local Git in a temporary directory with `apply --numstat`; it
does not apply the patch. Passing syntax does not establish applicability.

The required top-level fields are `plan` and `runs`. Optional additions:

| Field | Meaning |
| --- | --- |
| `freeze.protected_holdout` | Explicit protected task-ID list; overlap rejects review |
| `pair_candidates` | Two candidate names; requires both in every planned pair |
| run `instrument_checks` | Named booleans for required observed checks |
| run `grading_provenance_ok` | True, false or unknown, separate from grading occurrence |
| run `patch_text` | Preserved text patch, checked when supplied |
| run `agent_patch_size` | Integer character count, not UTF-8 byte count |

The existing run fields `grading_ran`, `test_exit_code`, `cleanup_ok`,
`provenance_ok`, `resolved` and error fields still govern comparison eligibility.
Additional failed checks may disqualify a run; they cannot upgrade an ineligible
run. Missing evidence is not invented. Legacy inputs remain supported, so callers
requiring patch inspection must supply patch_text, including an empty string for
an observed empty patch.

Paired summaries retain all planned runs in denominators. A missing/ungraded side
produces an undecided pair, not an opponent win. Solved, unsolved, ungraded and
not-attempted counts are reported separately.

`scripts/recovery_evidence.py` accepts operation-level before/after SHA-256 values
and an exact reported path. Those hashes must come from measurements around that
operation; callers must not substitute final-artifact hashes or invented values.
Without such evidence an acknowledged write stays unproven. A byte change still
does not establish correctness or that the recovery instruction caused it.

Run `python scripts/run_checks.py` for public checks. No GPU is required.
