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

## Pilot v1: repetition before context overflow

B had already edited source. After test edits caused collection errors, it read the same range
25 consecutive times. The final request required at least 24,577 input plus 8,192 reserved output
tokens, exceeding 32,768. Cumulative prompt usage of 646,691 is not a single context size.

This does not demonstrate an inherent incompatibility between thinking and the output cap.
Lowering output allowance alone would not prevent a tool loop. Evaluate loop behavior and context
headroom explicitly, and isolate reasoning-setting comparisons from other candidate changes.
