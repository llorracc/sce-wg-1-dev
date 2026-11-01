"""The checker's verification of a results file's Jacobians block (../jacobians.md, "What the checker can verify without
solving"). It reads the matrices the block lists, beside the results file, and checks what needs no solution:

- each matrix file: present, its SHA-256 the one listed, a .npy of version 1.0, little-endian float64 in C order, T x T;
- the block's completeness: every output and input for every type and the aggregate, and weights summing to one;
- the shared grid: its nodes, x = j/(N - 1) and a_j = a_max ((x x) x) in IEEE double precision, hashing to the stated
  SHA-256;
- the households' income responses, which are known exactly: zero for the return, the steady state's mean income
  times the identity for the income scale, the identity for a transfer that reaches every household;
- the flow budget, column by column: dC + dA - rho L dA - dY_hh = cash, with cash = survival A_ss on row s for the return;
- the steady state's own budget, C + A - rho A - Y_hh = 0;
- the present value of the transfer's consumption columns, sum_t rho^-(t-s) J^{C,transfer}[t, s] = 1, for columns far
  enough from the horizon;
- the first-period response to a transfer, J^{C,transfer}[0, 0], against the mean MPC under the income measure;
- the aggregate as the weighted sum of the types.

Tolerances are the design's: a grid's flow budget closes to about 1e-6, the first-period MPC to about 1e-3.
"""

from __future__ import annotations

import hashlib
import struct
from pathlib import Path

import numpy as np

FLOW_TOLERANCE = 1e-6
STEADY_TOLERANCE = 1e-8
MPC_TOLERANCE = 1e-3
PRESENT_VALUE_TOLERANCE = 1e-3
INCOME_TOLERANCE = 1e-9
AGGREGATE_TOLERANCE = 1e-9


def grid_nodes(n: int, a_max: float) -> list[float]:
    """The shared grid's nodes, by correctly rounded operations only, so that every language computes the same doubles."""
    nodes = []
    for j in range(n):
        x = j / float(n - 1)
        nodes.append(a_max * ((x * x) * x))
    return nodes


def grid_sha256(n: int, a_max: float) -> str:
    return hashlib.sha256(struct.pack(f"<{n}d", *grid_nodes(n, a_max))).hexdigest()


def _load_npy(path: Path, sha256: str, shape: tuple[int, ...], problems: list[str], label: str):
    if not path.is_file():
        problems.append(f"{label}: {path.name} is missing")
        return None
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != sha256:
        problems.append(f"{label}: {path.name}'s SHA-256 is not the one listed")
    with path.open("rb") as f:
        try:
            version = np.lib.format.read_magic(f)
            if version != (1, 0):
                problems.append(f"{label}: .npy version {version}, not 1.0")
                return None
            read_shape, fortran, dtype = np.lib.format.read_array_header_1_0(f)
        except ValueError as error:
            problems.append(f"{label}: not a .npy file ({error})")
            return None
    if fortran or dtype != np.dtype("<f8"):
        problems.append(f"{label}: must be little-endian float64 in C order, not {dtype} with fortran_order {fortran}")
    if tuple(read_shape) != shape:
        problems.append(f"{label}: shape {tuple(read_shape)}, not {shape}")
        return None
    return np.load(path, allow_pickle=False)


def verify(block: dict, base: Path) -> list[str]:
    """The problems with a Jacobians block whose matrices lie relative to `base`, the results file's folder; empty when
    every check passes. The block is assumed to have passed the results schema."""
    problems: list[str] = []
    T, inputs, outputs = block["T"], block["inputs"], block["outputs"]
    weights = block["weights"]
    n_types = len(weights)
    if abs(sum(weights) - 1.0) > 1e-12:
        problems.append(f"weights: they sum to {sum(weights)!r}, not 1")
    if len(block["steady_state"]["by_type"]) != n_types:
        problems.append("steady_state/by_type: one entry per type is required, as many as the weights")
    grid = block["grid"]
    if grid_sha256(grid["N"], grid["a_max"]) != grid["nodes_sha256"]:
        problems.append("grid/nodes_sha256: not the hash of the nodes a_j = a_max ((x x) x), x = j/(N - 1)")

    # the matrices
    J: dict[tuple, np.ndarray] = {}
    for entry in block["matrices"]:
        key = (entry["output"], entry["input"], entry["type"])
        if key in J:
            problems.append(f"matrices: {key} is listed twice")
            continue
        label = f"matrices/{entry['output']}/{entry['input']}/{entry['type']}"
        m = _load_npy(base / entry["path"], entry["sha256"], (T, T), problems, label)
        if m is not None:
            J[key] = m
    who = list(range(n_types)) + ["aggregate"]
    missing = [(o, i, t) for o in outputs for i in inputs for t in who if (o, i, t) not in J]
    if missing:
        problems.append(f"matrices: {len(missing)} missing, the first {missing[0]}")
    if problems:
        return problems

    eye = np.eye(T)
    lag = np.eye(T, k=-1)
    receives = block["conventions"]["newborns"]["receive_transfer"]
    for t in who:
        ss = block["steady_state"]["aggregate"] if t == "aggregate" else block["steady_state"]["by_type"][t]
        rho, survival = ss["rho"], ss["survival"]
        if abs(rho - ss["R"] * survival) > 1e-12 * max(1.0, rho):
            problems.append(f"steady_state/{t}: rho {rho!r} is not R times survival")
        gap = ss["C"] + ss["A"] - rho * ss["A"] - ss["Y_hh"]
        if abs(gap) > STEADY_TOLERANCE * max(1.0, abs(ss["Y_hh"])):
            problems.append(f"steady_state/{t}: C + A - rho A - Y_hh is {gap:.3e}, not 0")
        for i in inputs:
            if "Y_hh" in outputs:
                known = {"return": 0.0 * eye, "income_scale": ss["Y_hh"] * eye,
                         "transfer": eye if receives else None}[i]
                if known is not None and np.max(np.abs(J["Y_hh", i, t] - known)) > INCOME_TOLERANCE:
                    problems.append(f"Y_hh/{i}/{t}: the households' income response is not the known one")
            if {"C", "A", "Y_hh"} <= set(outputs):
                cash = survival * ss["A"] * eye if i == "return" else 0.0 * eye
                residual = J["C", i, t] + J["A", i, t] - rho * lag @ J["A", i, t] - J["Y_hh", i, t] - cash
                worst = float(np.max(np.abs(residual)))
                if worst > FLOW_TOLERANCE:
                    r, s = np.unravel_index(np.argmax(np.abs(residual)), residual.shape)
                    problems.append(f"flow budget/{i}/{t}: off by {worst:.3e} at row {r}, column {s}; a dating, unit or "
                                    "newborn convention differs from the design's")
        if "transfer" in inputs and "C" in outputs and receives:
            jc = J["C", "transfer", t]
            first = float(jc[0, 0])
            if abs(first - ss["mpc_mean_income"]) > MPC_TOLERANCE:
                problems.append(f"C/transfer/{t}: J[0, 0] = {first:.6f}, not the income measure's mean MPC "
                                f"{ss['mpc_mean_income']:.6f}")
            for s in sorted({0, T // 10, T // 4}):
                pv = float(sum(rho ** -(k - s) * jc[k, s] for k in range(T)))
                if abs(pv - 1.0) > PRESENT_VALUE_TOLERANCE:
                    problems.append(f"C/transfer/{t}: column {s}'s present value is {pv:.6f}, not 1; T may be too short")
    for o in outputs:
        for i in inputs:
            combined = sum(w * J[o, i, k] for k, w in enumerate(weights))
            if np.max(np.abs(combined - J[o, i, "aggregate"])) > AGGREGATE_TOLERANCE * max(1.0, np.max(np.abs(combined))):
                problems.append(f"{o}/{i}/aggregate: not the weighted sum of the types")
    return problems
