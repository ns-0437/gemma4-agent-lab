# Next decisions

## Immediate

- Obtain an explicitly authorized four-run pilot with valid imports and complete artifacts.
- Audit every trace for answer leakage and actual edits; separate environment failure from wrong fixes.
- Choose one failure mode to improve, rather than expanding the prompt on speculation.

## If the pilot works

Develop a broader validated task set across repositories. Predeclare exclusions and a holdout
before candidate outcomes. Report paired candidate-only wins, baseline-only wins, shared passes
and shared failures, along with agent time and runtime tails. Two tasks are not a quality estimate.

## Hypotheses worth testing

- If source is found but never changed: reduce repeated investigation after a supported diagnosis.
- If edits are rejected: improve exact snippet and indentation handling.
- If patches are plausible but wrong: derive precise acceptance checks from issue semantics.
- If thinking truncates useful output: test output allowance separately from other configuration.
- If localization is genuinely failing: compare a focused navigation skill against ordinary search.

Each hypothesis needs its own measurable outcome. A clever architecture name, longer prompt or
passing compiler is not evidence of a better agent. LoRA remains a later option after support,
activation, data permissions and held-out evaluation are verified.

The public leaderboard can guide attention, but it is not the development test set or a guaranteed
private-score forecast. The 0.06 result remains the published measured result until a new submitted
artifact produces evidence that warrants an update.

## Next measurement

Validate a repository-stratified development and held-out pool using CPU baseline/reference
controls. Keep mechanically eligible tasks provisional until failure relevance is reviewed.
After that, compare frozen candidates under equal model budgets on development tasks. Reserve
held-out agent outcomes for a preselected candidate. Report missing runs and infrastructure errors.

v3 is an exploratory submission, not a proven improvement. Do not infer leaderboard outcomes
from replay success, synthetic test counts, or prompt length.
