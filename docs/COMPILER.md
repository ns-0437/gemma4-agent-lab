# Two validation levels

`validate_and_zip.py` is a local approximation. It checks layout and builds deterministic
archives; it does not replace the official compiler.

`official_check.py` calls `adk_submission.validate_directory` and `compile_submission` with
competition limits and stub tool signatures. `effective_settings.py` prints the compiled
model arguments for both agents. Obtain official packages from the competition's supported
environment; no harness wheel or source is bundled in this public repository.

Local audit versions: adk_submission 0.2.11, google-adk 1.36.1, swegemma 0.2.7. The first
supports Python >=3.11; swegemma requires >=3.12. We use Python 3.12 for development.

Observed compiler mapping: include_thoughts controls enable_thinking. The numeric 4096
thinking budget was absent from the compiled additional model arguments. Do not describe it
as an enforced server-side reasoning cap without observing the outgoing request.
