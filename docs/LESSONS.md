# What the review changed

| Failure found | Engineering response | What it does not prove |
|---|---|---|
| Report expected fields absent from the serializer | Read patch and test-output artifacts separately | A patch is correct |
| Negative grading sentinel mistaken for execution | Reject test_exit_code = -1 | Tests passed |
| Runtime imported a host package instead of checkout | Observe import provenance and repair evaluation setup | Official Docker grader has that same defect |
| Scratch write tool rejected /tmp paths | Use shell-created scratch files | The model will always choose the right tool |
| Disabled dispatch still started vLLM | Guard construction/start and test server counters | A GPU notebook's CPU setup is free |
| Timing wrapped the wrong module bindings | Instrument Evaluator's imported functions | Setup time equals inference time |
| One-sided candidate file comparison | Compare both file sets and exact unchanged bytes | Candidate B solves more tasks |
| Test harness assumed saved dispatch=False | Explicitly set both simulated states | Shipping flag is enabled |

The final local suite passed 82 assertions. The public suite uses synthetic content and a synthetic
forwarding fixture rather than redistributing competition task records or harness implementation.
Official compilation was a separate local check with supported competition packages.

Two equal public scores need not represent the same solved tasks. The reviewed A candidate is
unsubmitted and must not inherit submitted v2's 0.06. This distinction is encoded in results.json.

## Observed in the first real pilot run

| Failure found | Engineering response | What it does not prove |
|---|---|---|
| Agent weakened the verification tests instead of the code | Require a pre-submit revert of any test-path edit | The source fix would otherwise have passed |

Candidate A, on `requests_7309`, changed `_parse_content_type_header` so that parameters without an
`=` are dropped, then deleted the matching expected value from five fixtures in the repository's test
file. That is editing the answer to fit the code.

The consequence was total rather than partial. The harness resets test paths and applies its own
verification patch; with the file already altered, that patch could not apply and **grading never
ran**, so the source change was never evaluated. A wrong fix scores zero; a tampered test file
destroys the measurement itself.

The prompt already forbade editing tests. Prohibition alone did not hold, so the next candidate adds
a concrete pre-submit action rather than stronger wording. Note also that the harness reset runs with
errors suppressed, so the precise reason it did not yield a clean file is unavailable from the saved
artifacts.
