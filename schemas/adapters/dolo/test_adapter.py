"""Tests for dolo's adapter, in the environment of dolo's release (README.md):

    uv run --python 3.11 --with dolo==0.4.9.20 --with jsonschema --with pyyaml --with referencing --with pytest \\
        python -m pytest -q schemas/adapters/dolo/test_adapter.py

The restrained member is checked against HARK's committed results file, so that the two toolkits agree; the toy and the
library are solved and verified by the checker; and the restrained-limit suite converges as BST's proposition says.
"""

from __future__ import annotations

import json
import pathlib
import sys

import numpy as np
import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import adapter  # noqa: E402

SCHEMAS = adapter.SCHEMAS
BST = SCHEMAS / "bst"
SUITE = BST / "suites" / "restrained-limit"
HARK_RUN = SCHEMAS / "records" / "findings" / "2026-11-01_restrained-limit-suite-hark" / "results"


def _run(member, out, level=1, request=None):
    argv = [str(member), "--out", str(out), "--level", str(level)]
    if request:
        argv += ["--request", str(request)]
    return json.loads(pathlib.Path(adapter.main(argv)).read_text())


def _verify(member, results):
    bst1, _ = adapter.load_checker(str(SCHEMAS))
    assert bst1.validate_results(results) == []
    assert bst1.load_member(member).verify_results(results) == []


def test_the_restrained_member_agrees_with_hark(tmp_path):
    member = BST / "artificial" / "members" / "bst-restrained.yaml"
    mine = _run(member, tmp_path, request=SUITE / "bst-restrained.request.yaml")
    _verify(member, mine)
    theirs = json.loads((HARK_RUN / "bst-restrained" / "level-1" / "results.json").read_text())
    d, h = mine["types"][0], theirs["types"][0]
    assert d["comparison_points"] == h["comparison_points"]
    pts = np.array(d["comparison_points"])
    gap = np.abs(np.array(d["rule"]["c"]) - np.array(h["rule"]["c"]))[pts <= 20]
    assert gap.max() < 5e-4, gap.max()
    assert abs(d["kink"]["m"] - h["kink"]["m"]) < 1e-4
    assert d["kink"]["slope_below"] == pytest.approx(1.0) and abs(d["kink"]["slope_above"] - h["kink"]["slope_above"]) < 0.01
    assert abs(d["population"]["mass_at_constraint"] - h["population"]["mass_at_constraint"]) < 1e-3
    assert d["welfare"]["status"] == "not computed"


@pytest.mark.parametrize("name, scenario", [("toy", "artificial"), ("library", "natural")])
def test_a_member_is_solved_and_verified(tmp_path, name, scenario):
    member = BST / scenario / "members" / f"{name}.yaml"
    results = _run(member, tmp_path)
    _verify(member, results)
    assert results["toolkit"]["name"] == "dolo"


def test_the_restrained_limit_suite_converges(tmp_path):
    # BST's experiment (bst/model.md, "The restrained-limit suite"): each rung's largest gap to the restrained rule, at the
    # suite's common points, is smaller than the rung before.
    def rule(name, scenario):
        out = tmp_path / name
        res = _run(BST / scenario / "members" / f"{name}.yaml", out, request=SUITE / f"{name}.request.yaml")
        return np.array(res["types"][0]["rule"]["c"])
    restrained = rule("bst-restrained", "artificial")
    gaps = [float(np.max(np.abs(rule(f"bst-p-zero-{p}", "natural") - restrained))) for p in ("0.005", "0.0005", "0.00005")]
    assert gaps[0] > gaps[1] > gaps[2] > 0, gaps
