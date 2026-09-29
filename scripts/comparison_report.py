"""Build complete planned-run reports without inventing missing outcomes."""
import argparse
import json
from pathlib import Path


def key(record):
    pair = tuple(record.get(field) for field in ("task", "candidate"))
    if not all(isinstance(value, str) and value.strip() for value in pair):
        raise ValueError("task and candidate must be nonempty strings")
    return pair


def build_report(plan, runs, stop_reason=None):
    planned = [key(record) for record in plan]
    if len(planned) != len(set(planned)):
        raise ValueError("duplicate planned run")
    indexed = {}
    for record in runs:
        pair = key(record)
        if pair not in planned:
            raise ValueError("run outside the plan")
        if pair in indexed:
            raise ValueError("duplicate run result")
        indexed[pair] = record
    rows = []
    for task, candidate in planned:
        record = indexed.get((task, candidate))
        if record is None:
            rows.append(dict(task=task, candidate=candidate, attempted=False,
                             outcome=None, resolved=None,
                             stop_reason=stop_reason or "no run record available"))
        else:
            # Missing resolution stays unknown; false is a measured failure, not absence.
            resolved = record.get("resolved")
            if resolved is not None and type(resolved) is not bool:
                raise ValueError("resolved must be boolean or null")
            rows.append(dict(task=task, candidate=candidate, attempted=True,
                             outcome=record.get("outcome"), resolved=resolved,
                             stop_reason=None))
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="JSON with plan, runs and optional stop_reason")
    args = parser.parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    print(json.dumps(build_report(payload["plan"], payload["runs"],
                                  payload.get("stop_reason")), indent=2))


if __name__ == "__main__":
    main()
