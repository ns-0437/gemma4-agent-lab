# What belongs in Git

Include our agent YAML/prompts, scripts, synthetic tests, documentation and small aggregate
results with their evidence labels. Frozen agent sources are included byte-for-byte.

Exclude competition tasks and reference patches, snapshots, graph/embedding files, model
weights, adapter binaries, wheel packages, downloaded harness source, downloaded public
notebooks, generated notebooks, raw run traces and private machine notes. Small size alone
does not make a competition file suitable for redistribution.

Participants must obtain competition files directly from Kaggle under the applicable rules.
Keep them under ignored `reference/` or `data/`. Nothing here grants rights to those files.
Do not add Kaggle tokens, API keys, private paths or environment exports to Git.

The public test suite uses invented task contents. A synthetic pass proves test behavior,
not performance on a real coding task. Official compiler and real-model runs require local
dependencies/data not distributed here.

The 22 GB competition bundle is not uploaded, including through Git LFS. Generated notebooks
can embed experimental context, so create them locally and inspect before any authorized use.
