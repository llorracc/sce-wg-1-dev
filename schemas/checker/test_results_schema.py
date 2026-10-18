"""The results validator accepts a file in the shape of results.md and rejects the common mistakes."""

from __future__ import annotations

import copy
import json
from pathlib import Path

import jsonschema
import pytest

SCHEMA = json.loads((Path(__file__).resolve().parent.parent / "bst-1" / "results.schema.json").read_text())
PROBS = ["0.01", "0.05", "0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9", "0.95", "0.99", "0.999", "1"]


def gl_map(scale=1.0, undefined=()):
    return {p: (None if p in undefined else scale * float(p)) for p in PROBS}


def distribution(undefined=()):
    block = {"gl": gl_map(undefined=undefined)}
    if undefined:
        block["undefined"] = list(undefined)
    return block


def population():
    return {
        "m": distribution(), "a": distribution(), "c": distribution(),
        "mean_c": {"status": "value", "value": 1.0},
        "mass_at_constraint": 0.15, "fraction_a_nonpositive": 0.15, "mean_mpc": 0.4,
        "mpc_by_a_quartile": [0.8, 0.4, 0.25, 0.15],
    }


def sample():
    h = "0" * 64
    points = [0.25, 0.5, 1.0, 2.0, 5.0]
    one_type = {
        "beta": 0.96, "share": 1.0, "comparison_points": points,
        "rule": {"c": [0.25, 0.5, 0.93, 1.3, 1.9], "mpc": [1.0, 1.0, 0.5, 0.29, 0.18]},
        "exported_rule": {"m": [0.1, 1.0, 50.0], "c": [0.1, 0.93, 7.6], "range": [0.01, 500.0]},
        "kink": {"status": "undefined"},
        "target": {"status": "value", "m": 1.39, "c": 1.01, "mpc": 0.07},
        "pseudo_target": {"status": "value", "m": 1.21, "c": 0.99, "mpc": 0.09},
        "population": population(),
        "income_measure": {"status": "value", "m": distribution(), "a": distribution(), "mass_at_constraint": 0.1,
                           "mean_a": {"status": "value", "value": 0.6}, "mean_mpc": 0.3},
        "welfare": {"status": "value", "mean_value": -31.2, "mean_felicity": -1.03},
        "marginal_welfare": {"status": "undefined", "by_a_quartile": [None, 1.1, 0.7, 0.4], "at_constraint": None,
                             "undefined": ["mean", "by_a_quartile[0]", "at_constraint"]},
        "euler_residuals": {"r": [0.0, 0.0, 1e-6, -2e-6, 1e-7], "max_abs": 2e-6,
                            "expectation_method": "bst_bench:gauss-legendre-log-support"},
        "stationarity_residual": {"population": 3e-5, "income": 4e-5},
    }
    return {
        "family": "bst/1", "parameter_file_sha256": h, "method_file_sha256": h, "settings_sha256": h,
        "request_file_sha256": h,
        "toolkit": {"name": "bst_bench", "version": "0.3"},
        "provenance": {"hardware": "jhu-dell", "threads": 1, "wall_seconds": 12.5},
        "types": [one_type],
        "pooled": {"population": population(),
                   "income_measure": {"status": "undefined"},
                   "welfare": {"status": "value", "mean_value": -31.2, "mean_felicity": -1.03},
                   "marginal_welfare": {"status": "undefined", "by_a_quartile": [None, 1.1, 0.7, 0.4],
                                        "at_constraint": None, "undefined": ["mean", "by_a_quartile[0]", "at_constraint"]}},
    }


def test_sample_validates():
    jsonschema.Draft202012Validator(SCHEMA).validate(sample())


@pytest.mark.parametrize("change", [
    lambda d: d["types"][0]["welfare"].pop("mean_value"),
    lambda d: d["types"][0]["population"]["m"]["gl"].pop("0.5"),
    lambda d: d["types"][0]["population"]["m"]["gl"].update({"0.33": 0.1}),
    lambda d: d["types"][0]["target"].update(status="maybe"),
    lambda d: d["types"][0]["population"].update(mean_c=1.0),
    lambda d: d.update(parameter_file_sha256="abc"),
    lambda d: d["types"][0].update(extra=1),
    lambda d: d["types"][0]["marginal_welfare"].update(status="value"),
])
def test_rejections(change):
    data = copy.deepcopy(sample())
    change(data)
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.Draft202012Validator(SCHEMA).validate(data)
