"""The standing check of HARK's adapter, with HARK at the adapter's pin (README.md):

    uv run --with "econ-ark @ git+https://github.com/llorracc/HARK.git@03a2c7a11ebd430e0c54eaa2da7f0eb5ab3d7483" \
        --with sympy --with jsonschema --with pyyaml --with scipy --with referencing --with pytest pytest -q schemas/adapters/hark

The Markov solution on the nonpersistent chain must give the same rule in both employment states and the standard consumer's
rule on the same nodes, the adapter's results file must validate and pass the checker's verification, and its method file
must name only the family's method targets, each once.
"""
import pathlib
import subprocess
import sys

import numpy as np
import pytest

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import adapter  # noqa: E402

MEMBERS = adapter.SCHEMAS / "bst-1" / "members"
SAME_AS_STANDARD = 1e-12      # the largest relative difference from the standard consumer's rule
LEVEL = adapter.LEVELS[1]


def _member(name):
    bst1, _ = adapter.load_checker(str(adapter.SCHEMAS))
    return bst1.load_member(MEMBERS / f"{name}.yaml")


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
    results = adapter.main([str(MEMBERS / f"{name}.yaml"), "--out", str(tmp_path), "--level", "1"])
    check = subprocess.run([sys.executable, str(adapter.SCHEMAS / "checker" / "check.py"), str(MEMBERS / f"{name}.yaml"),
                            "--verify-results", results], capture_output=True, text=True)
    assert check.returncode == 0, check.stdout + check.stderr


def test_the_method_file_names_only_the_family_s_targets():
    import re
    text = (adapter.SCHEMAS / "bst-1" / "model.md").read_text(encoding="utf-8")
    section = text.split("## Method targets", 1)[1].split("\n## ", 1)[0]
    targets = {m.group(1) for line in section.splitlines() for m in [re.match(r"\| `([^`]+)`", line)] if m}
    named = [entry["on"] for entry in adapter.METHODS]
    assert set(named) <= targets and len(named) == len(set(named)), sorted(set(named) - targets)


def test_the_provenance_does_not_name_the_machine(tmp_path):
    import json
    import platform
    results = adapter.main([str(MEMBERS / "library.yaml"), "--out", str(tmp_path), "--level", "1"])
    text = json.dumps(json.load(open(results))["provenance"])
    assert platform.node() not in text and platform.platform() not in text
