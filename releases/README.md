# Frozen source releases

`v1` and `v2` are submitted artifacts, each reported at public score 0.06.
`v2_reviewed` and `pilot_A` contain the same unsubmitted reviewed source.
`pilot_B` differs from A only in `include_thoughts: true`.

SHA-256 refers to the deterministic ZIP of each source directory, not a hash of this folder.
`.gitattributes` disables newline conversion here to preserve the original artifact bytes.
No weights or ZIP binaries are stored in Git. `manifest.json` records expected archive hashes.

The v1 upload predates deterministic ZIP metadata. Its original uploaded archive hash is retained
separately as submitted_archive_sha256. The rebuilt v1 ZIP has a different hash; every source
entry was compared byte-for-byte against the historical ZIP before publication. Other releases
already used normalized ZIP metadata. This distinction is intentional, not a refrozen candidate.
