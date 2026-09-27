# Frozen source releases

`v1` and `v2` are submitted artifacts, each reported at public score 0.06.
`v2_reviewed` and `pilot_A` contain the same unsubmitted reviewed source.
`pilot_B` differs from A only in `include_thoughts: true`.

SHA-256 refers to the deterministic ZIP of each source directory, not a hash of this folder.
`.gitattributes` disables newline conversion here to preserve the original artifact bytes.
No weights or ZIP binaries are stored in Git. `manifest.json` records expected archive hashes.
