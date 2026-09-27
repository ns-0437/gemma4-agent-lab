# Agent architecture

The coder searches the repository, forms a hypothesis, makes a focused source edit,
verifies relevant behavior and calls `submit_patch`. A read-only analyzer can inspect
callers and code graphs when localization remains unclear. Both use the same base model.

`submission/` is the evolving working candidate, NOT a scored artifact. Frozen sources live
in `releases/`. v1 and submitted v2 are the only artifacts with reported public scores.

The working prompt covers checkout import provenance, scratch files through shell commands,
exit-status preservation, bounded searches, exact issue/API semantics and untracked changes.
These are engineering hypotheses, not independently proven score improvements.
