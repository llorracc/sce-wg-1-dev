"""The experiment validator (../experiment.schema.json, ../experiments.md) and the experiments written to it.

    uv run --with jsonschema --with pyyaml --with referencing --with pytest python -m pytest -q schemas/checker/test_experiment.py

What these tests establish: the validator is a valid JSON Schema; every experiment file is strict YAML and validates;
its members' and request files exist and hash as it says; each request file names its member's family and parameter
hash; its checks name declared members; every quantity it names exists in the results schema; and BST's anchors are
the published page's. Each break below is caught. They solve nothing, and say nothing about whether a toolkit passes.
"""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import jsonschema
import pytest

HERE = Path(__file__).resolve().parent
SCHEMAS = HERE.parent
sys.path.insert(0, str(HERE))
import canonical  # noqa: E402

SCHEMA = json.loads((SCHEMAS / "experiment.schema.json").read_text(encoding="utf-8"))
RESULTS = json.loads((SCHEMAS / "bst" / "results.schema.json").read_text(encoding="utf-8"))
EXPERIMENTS = sorted((SCHEMAS / "bst" / "suites").glob("*/experiment.yaml"))
ANCHORS = SCHEMAS.parent / "ontologies" / "buffer-stock-models" / "bst-anchors.txt"


def load(path: Path) -> dict:
    return canonical.load_strict(path.read_text(encoding="utf-8"))


def _deref(node: dict) -> dict:
    while "$ref" in node:
        node = RESULTS["$defs"][node["$ref"].split("/")[-1]]
    return node


def _branches(node: dict):
    node = _deref(node)
    yield node
    for key in ("allOf", "anyOf", "oneOf"):
        for sub in node.get(key, []):
            yield from _branches(sub)


def resolves(path: str) -> bool:
    """Whether a quantity's path names something the results schema defines."""
    nodes = [RESULTS]
    for segment in path.split("."):
        key, every = (segment[:-2], True) if segment.endswith("[]") else (segment, False)
        found = []
        for node in nodes:
            for branch in _branches(node):
                prop = branch.get("properties", {}).get(key)
                if prop is None:
                    continue
                if every:
                    found += [b["items"] for b in _branches(prop) if "items" in b]
                else:
                    found.append(prop)
        if not found:
            return False
        nodes = found
    return True


def problems(experiment: dict, folder: Path) -> list[str]:
    """What the validator cannot say about an experiment: its files, hashes, names and quantities."""
    out = [f"{'/'.join(map(str, e.path))}: {e.message}" for e in jsonschema.Draft202012Validator(SCHEMA).iter_errors(experiment)]
    if out:
        return out
    ids = [m["id"] for m in experiment["members"]]
    if len(set(ids)) != len(ids):
        out.append("a member's id is repeated")
    for m in experiment["members"]:
        p, r = folder / m["parameter_file"], folder / m["request_file"]
        if p.stem != m["id"]:
            out.append(f"{m['id']}: the id is not its parameter file's name")
        if not p.is_file() or not r.is_file():
            out.append(f"{m['id']}: a file is missing")
            continue
        member, request = load(p), load(r)
        if canonical.model_hash(member) != m["parameter_file_sha256"]:
            out.append(f"{m['id']}: the parameter file's hash differs")
        if canonical.model_hash(request) != m["request_file_sha256"]:
            out.append(f"{m['id']}: the request file's hash differs")
        if request.get("family") != member.get("family") or request.get("parameter_file_sha256") != m["parameter_file_sha256"]:
            out.append(f"{m['id']}: the request file is for another member")
    check_ids = [c["id"] for c in experiment["checks"]]
    if len(set(check_ids)) != len(check_ids):
        out.append("a check's id is repeated")
    for c in experiment["checks"]:
        named = [i for pair in c.get("pairs", []) for i in pair] + c.get("members", [])
        out += [f"{c['id']}: no member {i}" for i in named if i not in ids]
    for q in experiment["reports"] + [c["quantity"] for c in experiment["checks"]]:
        if not resolves(q):
            out.append(f"the results schema has no {q}")
    for s in experiment.get("report_scripts", []):
        if not (folder / s["path"]).is_file():
            out.append(f"no report script {s['path']}")
    if ANCHORS.is_file():
        anchors = {line.strip() for line in ANCHORS.read_text(encoding="utf-8").splitlines() if line.strip() and not line.startswith("#")}
        out += [f"BST has no anchor {a}" for a in experiment.get("sources", {}).get("bst", []) if a not in anchors]
    return out


def test_the_validator_is_a_json_schema():
    jsonschema.Draft202012Validator.check_schema(SCHEMA)


def test_there_is_an_experiment():
    assert [p.parent.name for p in EXPERIMENTS] == ["restrained-limit"]


@pytest.mark.parametrize("path", EXPERIMENTS, ids=lambda p: p.parent.name)
def test_each_experiment_is_sound(path):
    assert problems(load(path), path.parent) == []


def test_the_restrained_limit_members_share_their_points():
    # Its first check compares rules member against member, so their request files must ask for the same points.
    path = SCHEMAS / "bst" / "suites" / "restrained-limit" / "experiment.yaml"
    points = {m["id"]: load(path.parent / m["request_file"])["types"][0]["points"] for m in load(path)["members"]}
    assert len({tuple(p) for p in points.values()}) == 1


BREAKS = {
    "a wrong parameter hash": lambda e: e["members"][0].update(parameter_file_sha256="0" * 64),
    "a wrong request hash": lambda e: e["members"][1].update(request_file_sha256="f" * 64),
    "a request file for another member": lambda e: e["members"][0].update(
        request_file=e["members"][1]["request_file"], request_file_sha256=e["members"][1]["request_file_sha256"]),
    "an unknown member in a pair": lambda e: e["checks"][0]["pairs"].append(["bst-p-zero-0.5", "bst-restrained"]),
    "an unknown quantity": lambda e: e["reports"].append("types[].rule.consumption"),
    "an array taken as a key": lambda e: e["reports"].append("types.rule.c"),
    "pairs on a comparison of toolkits": lambda e: e["checks"][2].update(pairs=[["bst-restrained", "bst-restrained"]]),
    "decreasing across toolkits": lambda e: e["checks"][2].update(expect="decreasing"),
    "falls_with_level between members": lambda e: e["checks"][0].update(expect="falls_with_level"),
    "a level numerics.md does not name": lambda e: e["levels"].append("highest"),
    "a toolkit's setting": lambda e: e.update(grid_points=300),
    "an anchor BST does not have": lambda e: e["sources"].update(bst=["the-restrained-limit"]),
    "a repeated check": lambda e: e["checks"].append(copy.deepcopy(e["checks"][0])),
}


@pytest.mark.parametrize("name", BREAKS)
def test_each_break_is_caught(name):
    path = SCHEMAS / "bst" / "suites" / "restrained-limit" / "experiment.yaml"
    if name == "an anchor BST does not have" and not ANCHORS.is_file():
        pytest.skip("the ontology's list of BST's anchors is not on this branch")
    experiment = load(path)
    BREAKS[name](experiment)
    assert problems(experiment, path.parent) != []
