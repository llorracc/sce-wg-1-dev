"""Tests for the checker's verification of a results file's Jacobians block (jacobians.py), on synthetic matrices that
satisfy every identity exactly, and on breaks of each one."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import numpy as np
import pytest

import jacobians
from bst1 import validate_results

T = 60
R, SURVIVAL = 1.01, 0.99375
RHO = R * SURVIVAL
LAMBDA = 0.8          # the decay of the synthetic consumption responses


def synthetic(types=2):
    """Matrices for C, A and Y_hh of the three inputs that satisfy the flow budget exactly, a transfer's consumption
    columns with present value one, and a steady state with its own budget closed."""
    c0 = 1 - LAMBDA / RHO
    out = {}
    for k in range(types):
        a_ss, y_ss = 6.0 + k, 1.000115
        c_ss = y_ss + a_ss * (RHO - 1)
        cols = {}
        for name in ("return", "income_scale", "transfer"):
            jc = np.zeros((T, T))
            for s in range(T):
                for t in range(s, T):
                    jc[t, s] = c0 * LAMBDA ** (t - s) * {"return": 0.3, "income_scale": y_ss, "transfer": 1.0}[name]
            jy = {"return": 0 * np.eye(T), "income_scale": y_ss * np.eye(T), "transfer": np.eye(T)}[name]
            cash = SURVIVAL * a_ss * np.eye(T) if name == "return" else 0 * np.eye(T)
            ja = np.zeros((T, T))
            for t in range(T):
                prev = ja[t - 1] if t > 0 else 0.0
                ja[t] = RHO * prev + jy[t] + cash[t] - jc[t]
            cols[name] = {"C": jc, "A": ja, "Y_hh": jy}
        ss = {"C": c_ss, "A": a_ss, "Y_hh": y_ss, "R": R, "survival": SURVIVAL, "rho": RHO, "mass_at_constraint": 0.03,
              "mpc_mean_population": 0.25, "mpc_mean_income": c0}
        out[k] = (cols, ss)
    return out


def write_block(tmp_path: Path, data, weights) -> dict:
    matrices = []
    agg = {i: {o: sum(w * data[k][0][i][o] for k, w in enumerate(weights)) for o in ("C", "A", "Y_hh")}
           for i in ("return", "income_scale", "transfer")}
    agg_ss = {key: sum(w * data[k][1][key] for k, w in enumerate(weights)) for key in data[0][1]}
    agg_ss.update(R=R, survival=SURVIVAL, rho=RHO)
    for i in agg:
        for o in agg[i]:
            for t, m in [(k, data[k][0][i][o]) for k in data] + [("aggregate", agg[i][o])]:
                path = tmp_path / f"{o}_{i}_{t}.npy"
                with path.open("wb") as f:
                    np.lib.format.write_array(f, np.ascontiguousarray(m, dtype="<f8"), version=(1, 0))
                matrices.append({"output": o, "input": i, "type": t, "path": path.name,
                                 "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
    return {
        "T": T, "inputs": ["return", "income_scale", "transfer"], "outputs": ["C", "A", "Y_hh"],
        "conventions": {"dating": {"return": "the gross return paid at the start of s on assets carried from s - 1",
                                   "income_scale": "all non-capital income received in s, the benefit included",
                                   "transfer": "x times permanent income, received in s by every household alive"},
                        "units": "per capita, per unit of the steady state's aggregate permanent income",
                        "measure": "income-weighted",
                        "newborns": {"assets": 0.0, "first_period": "the employed branch of xi; psi drawn",
                                     "receive_transfer": True},
                        "assets_of_the_dead": "vanish"},
        "grid": {"N": 1000, "a_max": 500.0, "exponent": 3, "nodes_sha256": jacobians.grid_sha256(1000, 500.0),
                 "mass_above_a_max": {"by_type": [0.0] * len(weights), "aggregate": 0.0}},
        "method": {"name": "fake-news", "step": 1e-4, "scheme": "forward", "baseline": "steady-state"},
        "steady_state": {"tolerance": 1e-10, "backward_step_residual": 1e-12,
                         "by_type": [data[k][1] for k in data], "aggregate": agg_ss},
        "weights": weights, "matrices": matrices,
    }


@pytest.fixture
def good(tmp_path):
    return write_block(tmp_path, synthetic(), [0.4, 0.6]), tmp_path


def test_the_grid_s_hash_is_the_design_s():
    assert jacobians.grid_sha256(1000, 500.0) == "e88176020da3a4ad8dc6299b9ee06c719b6c9dea93d321e299112a3976944e06"


def test_a_consistent_block_passes(good):
    block, base = good
    assert jacobians.verify(block, base) == []


def test_the_block_validates_in_a_results_file(good):
    import test_results_schema
    data = test_results_schema.sample()
    data["jacobians"] = good[0]
    assert validate_results(data) == []
    data["jacobians"]["steady_state"]["tolerance"] = 1e-6
    assert any("tolerance" in p for p in validate_results(data))


def test_a_return_dated_one_row_late_is_caught(tmp_path):
    data = synthetic()
    for k in data:
        cols, ss = data[k]
        cash = SURVIVAL * ss["A"] * np.eye(T, k=-1)            # the return's term one row late
        ja = np.zeros((T, T))
        for t in range(T):
            ja[t] = RHO * (ja[t - 1] if t > 0 else 0.0) + cash[t] - cols["return"]["C"][t]
        cols["return"]["A"] = ja
    problems = jacobians.verify(write_block(tmp_path, data, [0.4, 0.6]), tmp_path)
    assert any(p.startswith("flow budget/return") for p in problems)


def test_a_transfer_that_misses_newborns_is_caught(tmp_path):
    data = synthetic()
    for k in data:
        data[k][0]["transfer"]["Y_hh"] = SURVIVAL * np.eye(T)
    problems = jacobians.verify(write_block(tmp_path, data, [0.4, 0.6]), tmp_path)
    assert any("Y_hh/transfer" in p for p in problems)


@pytest.mark.parametrize("break_it, problem", [
    (lambda b, base: b["matrices"][0].update(sha256="0" * 64), "SHA-256"),
    (lambda b, base: b["grid"].update(a_max=400.0), "nodes_sha256"),
    (lambda b, base: b.update(weights=[0.5, 0.6]), "weights"),
    (lambda b, base: b["steady_state"]["aggregate"].update(mpc_mean_income=0.5), "mean MPC"),
    (lambda b, base: b["matrices"].pop(), "missing"),
    (lambda b, base: np.save(base / b["matrices"][0]["path"], np.zeros((T, T)).T), "SHA-256"),
])
def test_each_break_is_caught(good, break_it, problem):
    block, base = good
    block = copy.deepcopy(block)
    break_it(block, base)
    assert any(problem in p for p in jacobians.verify(block, base)), jacobians.verify(block, base)
