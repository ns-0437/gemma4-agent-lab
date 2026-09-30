# Stage 1 and the concise-prompt comparison

Checkpoint: September 30, 2026. This is a summary of saved local evidence and the
owner's launch record, not a new Kaggle status check. Public scores remain 0.06 for
v1, v2 and v3. No later candidate has a measured public score.

## Recovery candidate R: one task, no graded result

The private Stage-1 review records one planned and attempted run. Both control
arms agreed with saved expectations, agent provenance passed and cleanup passed.
The agent exhausted 60 turns without producing a source patch. There were zero
rejected calls; the rejection-recovery ladder was not exercised. The trace
contained 59 run_command calls and one read_file call, with a dominant probe
issued 56 times. submit_patch was observed zero times.

Grading never ran (exit sentinel -1), so grading provenance is unobserved rather
than a demonstrated infrastructure failure. The absence of a submit_patch call
is not independently disqualifying: the harness may extract a working-tree diff.
Here the preserved patch size was zero. Stage 1 did not pass.

An acknowledged write is not proof that bytes changed. A read following a rejected
edit cannot establish recovery. Neither a final changed path nor its basename
alone attributes a change to a particular operation.

## Candidate S: hypothesis and frozen launch

S derives from scored v3/A and changes only the coder prompt: 1,247 to 413 words.
The shorter workflow is a prompt-package hypothesis, not a finding that prompt
length caused repetition. Model, sampling, tools and analyzer remain unchanged.

| Artifact | SHA-256 |
| --- | --- |
| Submitted v3/A archive | `b8da59c1c3a0671bb9b11b2fe4238a252ff792a63abf7ea4b5d555ceab57b24b` |
| R coder prompt | `74a12c7d241371f7e8a26aad9b061780bac2a5c8c5b8fd4fd9ed80f5eedea8c3` |
| S archive | `8bf9f72c5d7ac4747e10c53637393bd7b18a6b66aae1879ddf4a62f4e4a6dc07` |
| A/S launched notebook | `86d1c83bb203a1000c205d8913df59abcf83f86c584e66eb2ceba1e3e5a5a649` |

The owner reports one version pushed at 15:07 UTC on September 30. This checkpoint
does not establish its current scheduler state. Four selected Rich development
tasks are paired A/S, S/A, A/S, S/A. All protected held-out tasks remain excluded.
The initial cross-repository proposal was withdrawn because those validated
FastAPI/Requests tasks belonged to the protected hold-out.

All eight planned rows must remain visible, including missing and ungraded runs.
Reliability (patch and grading completion), performance (paired solves and
regressions), and mechanism (repetition and edit evidence) are separate measures.
More incorrect graded patches is not a solve improvement. Four selected tasks
cannot establish general Rich performance or a competition score prediction.

The runtime estimate is about 130 minutes, not a bound. The 300-minute session
admission setting prevents new dispatch after its threshold; it is not a hard
kill timer. GPU quota readings are account-wide and do not directly attribute
charges to a particular run.

## Feedback audit limits

Recorded token growth and source inspection are consistent with retained history.
Outgoing request bodies were not captured. No feedback-path defect was found,
but neither correct message ordering nor retention of each instruction was
directly established from request bodies.

No raw task data, reference patches, verification tests, model weights or traces
are published here. Public checks use invented fixtures.
