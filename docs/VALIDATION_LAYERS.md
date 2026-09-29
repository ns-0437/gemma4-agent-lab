# What a validation result establishes

| Layer | Evidence | Does not establish |
|---|---|---|
| Static source check | A name or statement exists | That a branch executes |
| Unit test | Specified inputs produce expected outputs | Integration with a generated notebook |
| Executed generated-cell test | Actual shipped code runs with controlled dependencies | Real sandbox or model compatibility |
| CPU baseline/reference pair | Verification can distinguish the unfixed and reference checkout | Agent solving ability |
| Agent run | Observed patch, errors and task verification | Broad superiority or private leaderboard rank |

The private evaluation-set repair exposed why these distinctions matter: string searches passed
while the notebook referenced an undefined policy, retained a stale reporting lookup and contained
a broken string literal. Later tests executed embedded code and checked files actually written.

Before a model comparison, review candidate distribution, both splits' repository coverage,
failure relevance and the actual answer-key access boundary. Keep previously studied tasks out
of held-out. Preserve partial evidence on failure. A hash identifies bytes; it does not prove quality.

Public examples are synthetic and deliberately exclude raw task data and verification bodies.
The repository's Python runner discovers public tests; explorer presentation checks run with
`node tests/test_explorer.cjs`. Neither invokes Kaggle or consumes GPU quota.
