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
