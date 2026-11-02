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
sys.path.insert(0, str(HERE))
from experiment import ANCHORS, EXPERIMENTS, SCHEMA, SCHEMAS, load, problems  # noqa: E402


def test_the_validator_is_a_json_schema():
    jsonschema.Draft202012Validator.check_schema(SCHEMA)


def test_there_is_an_experiment():
    assert [p.parent.name for p in EXPERIMENTS] == ["restrained-limit"]


@pytest.mark.parametrize("path", EXPERIMENTS, ids=lambda p: p.parent.name)
def test_each_experiment_is_sound(path):
    assert problems(load(path), path.parent) == []


def test_the_restrained_limit_members_share_their_points():
    # Its first check compares rules member against member, so their request files must ask for the same points.
    path = SCHEMAS / "bst" / "experiments" / "restrained-limit" / "experiment.yaml"
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
    path = SCHEMAS / "bst" / "experiments" / "restrained-limit" / "experiment.yaml"
    if name == "an anchor BST does not have" and not ANCHORS.is_file():
        pytest.skip("the ontology's list of BST's anchors is not on this branch")
    experiment = load(path)
    BREAKS[name](experiment)
    assert problems(experiment, path.parent) != []
