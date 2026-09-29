# Control evidence contract

The public `scripts/control_evidence.py` helpers are standalone. They do not patch the competition
harness or start Kaggle jobs. All tests use invented XML and temporary directories.

Use a fresh evidence directory per task, arm and attempt. Capture setup and patch command output
as commands complete. In the caller's `finally` block, invoke `write_arm` with available metadata,
stdout, stderr, traceback and retrieved XML, then clean up the sandbox in a nested `finally`.
Do not catch persistence failures and report success: missing evidence is an audit failure.

`reached_pytest` must be explicit. A setup exception produces `NO_PYTEST_RUN.txt`; a started pytest
process with no retrievable XML produces `MISSING_JUNIT.txt`. Neither fabricates test outcomes.
Every text artifact has a SHA-256 in `arm.json`, which is written last. Existing directories are
rejected to prevent a previous attempt's XML from masquerading as current evidence.

JUnit failures, errors and skips remain distinct. Duplicate test identities cause an explicit error
instead of overwriting a result. Failed-to-passed nodes still need review for relevance to the issue.
Keep raw evidence private: it may contain reference tests, repository content or sensitive output.
Public summaries should contain aggregate outcomes and limitations, not raw task artifacts.

Run `python -m unittest discover -s tests -p test_control_evidence.py -v`.
