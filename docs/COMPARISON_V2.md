# Repaired prompt comparison: 30 September checkpoint

This is a sanitized summary of privately downloaded Kaggle version-2 artifacts. No task text,
reference patches, model weights or raw traces are published here.

## Identity and outcome

- Notebook SHA-256: `97873af2210b0f26276efce30c14d1b4c0491320f008e983c20c174328bfdbbc`.
- A: submitted v3, archive `b8da59c1c3a0671bb9b11b2fe4238a252ff792a63abf7ea4b5d555ceab57b24b`.
- B: shorter prompt, archive `33a5ec57db0dd482fd4f807206f2cbda45cdc5f14a28c836c88417305c6e3909`.
- Both use thinking off. These are not the earlier pilot's thinking-off/thinking-on pair.
- Eight control arms passed, including expected baseline failures and reference passes.
- Runtime reported four NVIDIA L4 devices and tensor parallelism 4; model startup took 9.6 minutes.
- Two of eight agent runs executed; neither reached grading. Six were not attempted.

| Run | Observation | Agent-loop time |
|---|---|---:|
| First task / A | Repeated reproduction commands; exhausted 60 turns; no submitted patch | 377.5 s |
| First task / B | 42 rejected edit calls missing a required parameter; no submit_patch | 244.0 s |
| Remaining six | Controller stopped dispatch | Unavailable |

The controller called missing submission an unclassified environment failure. The trace shows
failed tool use and absent submission, not an independently observed environment fault. Neither
candidate is a winner. Notebook COMPLETE means execution ended, not that the agent solved tasks.

## What the repair established

The earlier control failure was reproduced with a real patch file: its writer omitted a final
newline and Git rejected it as corrupt. Normalizing that newline fixed patch transport. The public
regression uses an invented one-line patch and real Git, with separate original/applied hashes.

## Remaining work

Inspect model-response versus parser evidence before attributing malformed arguments to one
component. Preserve unknowns when raw responses are missing. Correct the stop classification and
use one bounded intervention at a time. Public helpers and synthetic tests do not prove that the
private workflow has been repaired or that a candidate improves leaderboard performance.

Four tasks from one repository cannot establish broad generalization. Trace audits do not prove
filesystem isolation. Quota charged was not established from this artifact packet.
