# Pilot v1 — measured outcome

Four runs were planned: `requests_7309` and `rich_3471`, each under candidate A (thinking off) and
candidate B (thinking on), ordered A/B then B/A. **Two ran. Neither produced a graded result, and
two never started.** No candidate comparison is possible from this pilot.

## Runtime environment, observed rather than requested

The accelerator named in notebook metadata is a request. These values come from the run itself:

| observation | value |
|---|---|
| `torch.cuda.device_count()` | 4 |
| device names | `NVIDIA L4` x4 |
| vLLM tensor parallel | `tp=4`, ready in 6.3 min |
| model | `gemma-4-31b-it-qat-w4a16-ct` revision 2, config SHA-256 `b100d85e571c25b6…` |
| quantization | pack-quantized, 4-bit |
| harness | swegemma 0.2.7, adk-submission 0.2.11, google-adk 1.36.1, vLLM 0.19.1 |

Budgets were identical for both arms: 10 minutes, 100 tool calls, 60 turns, 300-second commands.
**GPU quota charged is unavailable**: no pre-dispatch reading was taken, and a single later figure
cannot establish the delta.

## The four planned rows

| # | run | status | outcome | attribution |
|---|---|---|---|---|
| 1 | requests_7309 / A | executed | not resolved | verification patch could not be applied; grading never ran (`test_exit_code -1`) |
| 2 | requests_7309 / B | executed | not resolved | empty patch after a context-window error |
| 3 | rich_3471 / B | **not run** | missing | dispatch guard stopped after run 2 |
| 4 | rich_3471 / A | **not run** | missing | dispatch guard stopped after run 2 |

## Row 1 — thinking off

Agent loop 108.2 s, grading phase 26.9 s, 23 tool calls, 8 edit calls, 2 repeated identical
commands, 5 tool errors, 177,719 prompt and 3,327 completion tokens. Finish reasons unavailable.

Import provenance was verified inside both the agent and grading sandboxes: each resolved the
package to the task checkout, not a released copy. The evaluation repair held under real conditions.

The agent produced a genuine source edit and also edited the verification test file. See
[LESSONS](LESSONS.md).

## Row 2 — thinking on

Agent loop 225.5 s, grading never started, 44 tool calls, 5 edit calls, 1 tool error, 646,691 prompt
tokens (3.6x row 1) and 7,085 completion tokens. Finish reasons unavailable.

The agent edited source before damaging the test file and making 25 identical reads.
The run ended with a context-window error before a patch was extracted. See [EXPERIMENTS](EXPERIMENTS.md).

## Contamination audit

Neither trace referenced task metadata files, stored solutions, verification patches or secret
paths. Every mention of an input path was the model directory recorded on each step. This is a
trace audit of observed calls, not a proof of filesystem isolation; the subprocess backend is not
a security boundary.

## What this establishes

Model serving and agent execution run on real four-L4 hardware with the real quantized model, the import
repair survives real agent and grading sandboxes, and phase timings, traces and artifacts are
usable. It establishes nothing about relative candidate quality: zero of four runs were graded.

## CPU replay correction (28 September)

The unpatched control failed the five target cases and the reference passed all 220 tests.
Both A's original saved patch and its source-only variant passed all 220 tests. The original
patch's four deleted test expectations were reset successfully before verification patching.
Thus the claim that A's test edits caused the pilot grading failure is withdrawn. That failure
did not reproduce; its mechanism remains an open issue. Replay is not a fresh agent run.
