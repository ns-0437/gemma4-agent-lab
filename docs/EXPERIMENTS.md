# Experiment protocol

The publication checkpoint has two submitted scores (0.06 each) and zero measured pilot runs.
The current proposal is requests_7309 and rich_3471, each evaluated with frozen A and B, ordered
A/B then B/A. Alternation reduces ordering bias; it does not eliminate shared-server effects.

## Gates

1. Validate artifacts and compare frozen hashes. Keep real task/control data local and ignored.
2. Require target-relevant baseline failures and explicit gold passes of the same nodes. Check
   runtime provenance in both control sandboxes and reject infrastructure failures.
3. Confirm task fingerprints, model/runtime metadata and four actual L4 devices before serving.
4. Verify fresh setup imports inside every real agent and grading sandbox. Persist failures.
5. Start only after explicit GPU authorization. Dispatch defaults to False. CPU work in a GPU
   notebook consumes quota; the 150-minute admission deadline is not a hard session cap.
6. Save JSONL, patches, grading output, traces and setup observations locally. Audit answer-key access.
7. Inspect individual failures before changing prompts. Report missing data as unavailable.

Both agents share the same base model and generation settings within an arm. B changes thinking
on for coder and analyzer; the pilot is not an architecture ablation or v1/v2 comparison.

## Beyond the pilot

Select the next isolated change from demonstrated failures. Expand to a predeclared development
set across repositories, preserve untouched holdout tasks, and report matched wins/losses with
runtime. Do not silently drop difficult valid tasks. Repeat unstable outcomes under a fixed rule.
Promote a candidate only with evidence appropriate to the claim. Never promise leaderboard rank.

## Pilot v1 result: the thinking arm never reached a patch

Candidate B failed with a context-window error rather than a poor answer:

```
maximum context length is 32768 tokens. However, you requested 8192 output tokens
and your prompt contains at least 24577 input tokens, for a total of at least 32769
```

24,577 + 8,192 = 32,769, one token beyond the 32,768 limit. B had consumed 646,691 prompt tokens
across the run, 3.6 times candidate A on the same task, and produced no patch at all.

This is a configuration incompatibility between enabled thinking and `max_output_tokens: 8192`,
not evidence about the value of thinking. A run censored before it can edit says nothing about
solution quality. Raising the turn cap would not help either, because the failure is per-request.

The output allowance must therefore be tested as its own experiment, with `max_output_tokens`
reduced so that prompt plus output fits inside the window, before any thinking comparison is
attempted again. Do not read row 2 as a verdict on candidate B.
