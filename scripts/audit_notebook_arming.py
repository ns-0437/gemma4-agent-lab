"""Verify an explicit False -> True launch-flag change without executing a notebook."""
import argparse
import ast
import copy
import hashlib
import json
from pathlib import Path


def source_text(cell):
    source = cell.get("source", "")
    if isinstance(source, list) and all(isinstance(line, str) for line in source):
        return "".join(source)
    if isinstance(source, str):
        return source
    raise ValueError("cell source must be text or a list of strings")


def flag_location(notebook):
    hits = []
    for index, cell in enumerate(notebook.get("cells", [])):
        if cell.get("cell_type") != "code":
            continue
        tree = ast.parse(source_text(cell))
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and node.id == "DISPATCH_CONFIRM" and isinstance(node.ctx, ast.Store):
                hits.append((index, node))
        assignments = [node for node in tree.body if isinstance(node, ast.Assign)
                       and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name)
                       and node.targets[0].id == "DISPATCH_CONFIRM"]
        for node in assignments:
            if isinstance(node.value, ast.Constant) and type(node.value.value) is bool:
                for hit in hits:
                    if hit[0] == index and hit[1] is node.targets[0]:
                        hit[1].launch_value = node.value
    if len(hits) != 1 or not hasattr(hits[0][1], "launch_value"):
        raise ValueError("require exactly one top-level boolean DISPATCH_CONFIRM assignment")
    index, target = hits[0]
    return index, target.launch_value


def audit(disabled, armed):
    before_cell, before = flag_location(disabled)
    after_cell, after = flag_location(armed)
    if before.value is not False or after.value is not True or before_cell != after_cell:
        raise ValueError("expected False -> True in the same cell")
    normalized = copy.deepcopy(armed)
    lines = source_text(normalized["cells"][after_cell]).splitlines(keepends=True)
    # AST offsets count UTF-8 bytes, not Unicode characters.
    line = lines[after.lineno - 1].encode("utf-8")
    lines[after.lineno - 1] = (line[:after.col_offset] + b"False" + line[after.end_col_offset:]).decode("utf-8")
    normalized["cells"][after_cell]["source"] = "".join(lines)
    baseline = copy.deepcopy(disabled)
    # Jupyter permits either string or list representation of cell sources.
    for document in (baseline, normalized):
        for cell in document.get("cells", []):
            cell["source"] = source_text(cell)
    if baseline != normalized:
        raise ValueError("notebook changes extend beyond the launch flag")
    return {"flag_cell_index": after_cell, "only_launch_flag_changed": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("disabled", type=Path)
    parser.add_argument("armed", type=Path)
    args = parser.parse_args()
    before, after = args.disabled.read_bytes(), args.armed.read_bytes()
    result = audit(json.loads(before), json.loads(after))
    result.update(disabled_sha256=hashlib.sha256(before).hexdigest(),
                  armed_sha256=hashlib.sha256(after).hexdigest())
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
