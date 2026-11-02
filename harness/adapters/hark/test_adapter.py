"""The standing check of HARK's adapter, with HARK at the adapter's pin (README.md):

    uv run --with "econ-ark @ git+https://github.com/llorracc/HARK.git@1185280590b21fe2ddac80cadcfea66476e45380" \
        --with sympy --with jsonschema --with pyyaml --with scipy --with referencing --with pytest pytest -q harness/adapters/hark

The Markov solution on the nonpersistent chain must give the same rule in both employment states and the standard
consumer's rule on the same nodes, the adapter's results file must validate and pass the checker's verification, a
member of a natural family must be solved under the stated laws' limit, and the method file must name only the family's
method targets, each once.
"""
import pathlib
import subprocess
import sys

import numpy as np
import pytest

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import adapter  # noqa: E402

BST = adapter.SCHEMAS / "bst"
MEMBER = {"library": BST / "natural" / "members" / "library.yaml",
          "toy-natural": BST / "other" / "natural-no-point-mass" / "members" / "toy-natural.yaml",
          "toy": BST / "artificial" / "members" / "toy.yaml",
          "toy-untruncated": BST / "other" / "zero-infima" / "members" / "toy-untruncated.yaml"}
SAME_AS_STANDARD = 1e-12      # the largest relative difference from the standard consumer's rule
LEVEL = adapter.LEVELS[1]


def _member(name):
    bst1, _ = adapter.load_checker(str(adapter.SCHEMAS))
    return bst1.load_member(MEMBER[name])


@pytest.mark.parametrize("name", ["toy", "library"])
def test_the_markov_rule_is_the_standard_consumers(name):
    member = _member(name)
    nodes, P, PSI, XI, _ = adapter.shocks(member, LEVEL["nodes"])
    for t in member.types:
        beta = float(t["beta"])
        markov = adapter.solve_type(member, beta, nodes, LEVEL)          # asserts the two states' rules coincide
        standard = adapter.solve_standard(member, beta, P, PSI, XI, LEVEL).solution[0]
        lo = markov.solution[0].mNrmMin
        assert lo == pytest.approx(float(standard.mNrmMin), abs=1e-12)
        m = lo + np.geomspace(1e-6, LEVEL["dist_top"] - lo, 2000)
        c_m, c_s = np.asarray(markov.solution[0].cFunc(m), float), np.asarray(standard.cFunc(m), float)
        assert np.max(np.abs(c_m - c_s) / c_s) < SAME_AS_STANDARD, beta


@pytest.mark.parametrize("name", ["toy", "library"])
def test_the_results_file_passes_the_checker(name, tmp_path):
    results = adapter.main([str(MEMBER[name]), "--out", str(tmp_path), "--level", "1"])
    check = subprocess.run([sys.executable, str(adapter.SCHEMAS / "checker" / "check.py"), str(MEMBER[name]),
                            "--verify-results", results], capture_output=True, text=True)
    assert check.returncode == 0, check.stdout + check.stderr


def test_a_natural_member_is_solved_under_the_stated_limit(tmp_path):
    # In a natural family HARK computes the natural limit from the infima the adapter records, so the constraint in force is
    # the stated laws' a_Nat, whatever the nodes; and the results file passes the checker.
    import json
    member_file = MEMBER["toy-natural"]
    member = adapter.load_checker(str(adapter.SCHEMAS))[0].load_member(member_file)
    a_nat = member.natural_borrowing_constraint()
    for n in (5, 9):                 # HARK's iteration stops a little above the limit; the nodes do not move it
        nodes, *_ = adapter.shocks(member, n)
        lo = adapter.solve_type(member, float(member.types[0]["beta"]), nodes, LEVEL).solution[0].mNrmMin
        assert -1e-9 < lo - a_nat < 1e-6, (n, lo, a_nat)
    results = adapter.main([str(member_file), "--out", str(tmp_path / "out"), "--level", "1"])
    check = subprocess.run([sys.executable, str(adapter.SCHEMAS / "checker" / "check.py"), str(member_file),
                            "--verify-results", results], capture_output=True, text=True)
    assert check.returncode == 0, check.stdout + check.stderr
    derived = json.load(open(results))["effective_member"]["derived"]
    assert derived["constraint_in_force"] == pytest.approx(member.natural_borrowing_constraint(), abs=1e-12)


def test_the_method_file_names_only_the_family_s_targets():
    import re
    text = (adapter.SCHEMAS / "bst" / "model.md").read_text(encoding="utf-8")
    section = text.split("## Method targets", 1)[1].split("\n## ", 1)[0]
    targets = {m.group(1) for line in section.splitlines() for m in [re.match(r"\| `([^`]+)`", line)] if m}
    named = [entry["on"] for entry in adapter.METHODS]
    assert set(named) <= targets and len(named) == len(set(named)), sorted(set(named) - targets)


def test_the_provenance_does_not_name_the_machine(tmp_path):
    import json
    import platform
    results = adapter.main([str(MEMBER["library"]), "--out", str(tmp_path), "--level", "1"])
    text = json.dumps(json.load(open(results))["provenance"])
    assert platform.node() not in text and platform.platform() not in text


def test_the_restrained_limit_suite_converges():
    # BST's experiment "The Liquidity Constrained Solution as a Limit" (bst/model.md, "The restrained-limit suite"): as the probability
    # of the zero-income event falls, the natural member's rule comes closer to the restrained consumer's, on a common
    # grid of m. At level 1 on 2026-11-01 the largest gaps were 0.138, 0.061 and 0.027.
    m = np.concatenate([np.linspace(1e-4, 1.0, 400), np.linspace(1.0, 10.0, 400)[1:]])
    lev = adapter.LEVELS[1]

    def rule(path):
        member = adapter.load_checker(str(adapter.SCHEMAS))[0].load_member(path)
        nodes = adapter.shocks(member, lev["nodes"])[0]
        return np.asarray(adapter.solve_type(member, member.types[0]["beta"], nodes, lev).solution[0].cFunc(m), float)

    restrained = rule(BST / "artificial" / "members" / "bst-restrained.yaml")
    gaps = [float(np.max(np.abs(rule(BST / "natural" / "members" / f"bst-p-zero-{wp}.yaml") - restrained)))
            for wp in ("0.005", "0.0005", "0.00005")]
    assert gaps[0] > gaps[1] > gaps[2] > 0, gaps
