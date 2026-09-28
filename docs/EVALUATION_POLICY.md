# Portable evaluation selection

`scripts/evaluation_policy.py` accepts caller-provided metadata. It contains no competition tasks,
answer keys, Kaggle client, model calls or sandbox implementation. Tests use invented tasks.

1. Define repository quotas, size bands, screening cap and previously studied IDs before outcomes.
2. `screening_order` interleaves strata deterministically. A cap smaller than the number of strata
   cannot represent all strata; inspect the candidate distribution before dispatch.
3. `classify_controls` requires explicit successful patch return codes, checkout provenance,
   baseline exit 1, reference exit 0, no errored nodes and failure-to-pass cases. Its result is
   **mechanical eligibility**, not proof that an assertion failed for the issue's target behavior.
4. Inspect saved failure evidence before accepting eligible tasks. Preserve exclusions and reasons.
5. `allocate` enforces combined repository caps and reserves held-out slots for unstudied tasks.
   It reports shortages instead of silently filling them from a different repository. Review each
   split's composition: combined quotas do not guarantee repository coverage in both splits.

Run `python -m unittest discover -s tests -p test_evaluation_policy.py -v`.
The normal public check runner discovers these tests automatically. They do not execute a real
grading sandbox. These helpers are not automatically installed into the private Kaggle workflow.
