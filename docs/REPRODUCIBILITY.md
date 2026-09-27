# Reproduce the checks, not an invented score

## Public CPU path

Use Python 3.12+, install requirements-dev.txt, then run `python scripts/run_checks.py`.
It requires no competition account, data or GPU. The suite checks frozen artifacts, packaging,
repository boundaries and synthetic pilot cell behavior in both saved dispatch states.

The public fixture generator constructs invented issues, patches and test outcomes in memory.
Task identifiers are routing labels only. It does not read competition task rows or downloaded
harness source. This differs from the historical private test, which also exercised the actual
Evaluator forwarding method. Neither test serves Gemma or establishes a solved-task count.

## Real local compiler path

Obtain supported competition packages through Kaggle. The recorded audit used adk_submission
0.2.11 and google-adk 1.36.1. Use `scripts/official_check.py` and `scripts/effective_settings.py`.
Do not infer official-compiler acceptance solely from the local approximate validator.

## Real evaluation path

Acquire the competition data yourself after accepting the applicable rules. Store tasks.jsonl,
snapshots, wheels and local evidence outside tracked paths. The pilot generator expects
`reference/tasks.jsonl` and `reference/provenance_run_2026-09-27_repaired/controls_full.json`.
Those controls are NOT shipped: generate and review valid controls in your own environment first.
Do not substitute the public synthetic fixtures as real control evidence.

Review generated code, owner, hardware/model sources, expected task hashes and dispatch defaults.
Real execution requires explicit authorization and GPU quota. Current software versions, competition
rules and model availability must be checked when reproducing later; this is a dated research record.

## Artifact identity across operating systems

Source bytes are preserved under releases/ by .gitattributes. ZIP builders fix entry order,
timestamps, permissions and creator-system metadata. Linux CI exposed the last field's OS-dependent
default; builders now pin it to match the historical Windows archives. Verify the actual final
archive hash rather than assuming every Python/zlib implementation emits identical compressed bytes.

The v1 historical archive had earlier metadata. The public manifest records its original upload
hash separately from the deterministic rebuild. Source entries were verified identical locally.
