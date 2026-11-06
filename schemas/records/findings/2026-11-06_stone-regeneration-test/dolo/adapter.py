"""dolo's adapter for the buffer-stock families: a member in, a results file out, with HARK's adapter's command line.

    <python of dolo's environment> harness/adapters/dolo/adapter.py <member.yaml> --out <dir> --level <n> [--request <file>]

Written from dolo's Rosetta Stone, rosetta/dolo.md with rosetta/dolo.cards.yaml, and the hub, schemas/. What is here is
dolo's part alone, the Toolkit of common.py's protocol; the nodes, the effective member, the population, the statistics,
the diagnostics and the results file are the code the adapters share.
  - encode: a member's type and the level's settings become the recast model file of the stone (one file per type, its
    exogenous block a placeholder), the joint nodes of (psi, xi) as a FiniteDistribution, the savings grid, and the
    uniform grid of m;
  - the call: dolo.algos.egm.egm, iterated to convergence, with standard output silenced; an error if it does not
    converge;
  - decode: the rule read linearly through the values of egm's rule at the nodes of the uniform grid, with the kink's
    point added from the Euler equation at a = a_min for an artificial member; the MPC is the slope of the segment; no
    value function, so welfare is reported as not computed.
"""

import argparse
import contextlib
import importlib.metadata
import io
import os
import pathlib
import sys
import tempfile
from types import SimpleNamespace

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import common  # noqa: E402

# The stone states one of these, the uniform grid's step; the others it names without a value, and they are this file's
# choices (the clean room's log says what each rests on).
GRID_STEP = 0.005       # the uniform grid of m has a point every 0.005 at every level, up to the level's top (the stone)
ABOVE_LIMIT = 1e-6      # a natural member's savings grid starts this far above the limit, "just above" in the stone: where
                        # the shared population grid puts its first node (common.make_agrid)
MAXIT = 20000           # egm's most iterations; dolo's default of 1000 is too few for the toy's most patient type
CBAR = 1.0              # the scale of the expectation in the model file; it cancels in the rule
C_START = 1.0           # the calibrated c, which egm takes as its first, constant, rule

# The recast model of the stone ("The recasting"): symbols and equations as it writes them. The calibration, the domain,
# the grid's count and the placeholder for the exogenous block are filled in for each type.
MODEL = """# {name}
symbols:
    exogenous: [psi, xi]
    states: [m]
    poststates: [a]
    controls: [c]
    expectations: [mr]
    parameters: [beta, L, rho, R, G, a_min, cbar]
equations:
    transition:
        - m[t] = (m[t-1]-c[t-1])*R/(G*psi[t]) + xi[t]
    arbitrage:
        - beta*L*R*((G*psi[t+1]*c[t+1])/c[t])^(-rho) - 1 | 0.0 <= c[t] <= m[t] - a_min
    half_transition: |
        m[t] = a[t-1]*R/(G*psi[t]) + xi[t]
    reverse_state: |
        m[t] = a[t] + c[t]
    expectation: |
        mr[t] = beta*L*R*(G*psi[t+1]*c[t+1]/cbar)^(-rho)
    direct_response_egm: |
        c[t] = cbar*(mr[t])^(-1/rho)
calibration:
    beta: {beta}
    L: {L}
    rho: {rho}
    R: {R}
    G: {G}
    a_min: {a_min}
    cbar: {cbar}
    c: {c}
domain:
    m: [{m_lo}, {m_hi}]
exogenous: !Normal
    Sigma: [[0.01, 0.0], [0.0, 0.01]]
options:
    grid: !Cartesian
        orders: [{orders}]
"""


def _num(x):
    """A float as YAML 1.1 reads a float: the shortest decimal that reads back, with a point in its mantissa."""
    s = repr(float(x))
    if "e" in s and "." not in s.split("e")[0]:
        mantissa, exponent = s.split("e")
        s = f"{mantissa}.0e{exponent}"
    return s


def nested_grid(top, n, nest):
    """n points from 0 to top, evenly spaced after `nest` applications of log(1 + x): the multi-exponential spacing that
    the level's `nest` names (HARK's make_grid_exp_mult, here from zero)."""
    hi = float(top)
    for _ in range(nest):
        hi = np.log(hi + 1.0)
    grid = np.linspace(0.0, hi, n)
    for _ in range(nest):
        grid = np.exp(grid) - 1.0
    return grid


class LinearRule:
    """A rule read linearly through its points: c(m), and the MPC as the slope of the segment that holds m (at a point of
    the rule, the segment to its right). Beyond its ends the end segments continue."""

    def __init__(self, m, c):
        self.m, self.c = np.asarray(m, float), np.asarray(c, float)
        self.slope = np.diff(self.c) / np.diff(self.m)

    def _segment(self, x):
        return np.clip(np.searchsorted(self.m, x, side="right") - 1, 0, len(self.slope) - 1)

    def __call__(self, x):
        x = np.asarray(x, float)
        i = self._segment(x)
        return self.c[i] + self.slope[i] * (x - self.m[i])

    def derivative(self, x):
        return self.slope[self._segment(np.asarray(x, float))]

    def with_point(self, m, c):
        """The same rule with one more point."""
        i = int(np.searchsorted(self.m, m))
        if i < len(self.m) and self.m[i] == m:
            return LinearRule(self.m, np.concatenate([self.c[:i], [c], self.c[i + 1:]]))
        return LinearRule(np.insert(self.m, i, m), np.insert(self.c, i, c))


class DoloToolkit:
    name = "dolo"
    driver = "harness/adapters/dolo/adapter.py"
    description = ("Solve a member of a buffer-stock family (bst-natural/1 or bst-artificial/1) with dolo's endogenous "
                   "grid method, dolo.algos.egm.egm, and write its results file")
    representation = ("the joint nodes of (psi, xi), the product of the two shocks' nodes with the unemployment atom, "
                      "passed to dolo's egm as a FiniteDistribution of points and weights")
    diagnostics_method = (f"Gauss-Legendre in the log of each truncated lognormal law, {common.DIAG_NODES} nodes per piece "
                          "per shock, the transitory law's support split where m' crosses the rule's kink; the "
                          "unemployment state exact; its precision from doubling the nodes")
    # the stone's methods (dolo.cards.yaml), as a method file writes them (numerics.md): the tag where the target has one
    methods = [
        {"on": "policy.euler.solve", "method": "!time-iteration", "handler": "dolo.algos.egm.egm"},
        {"on": "policy", "method": "!Linear", "handler": "adapter"},
        {"on": "E_ψ_θ_j", "method": "!quadrature"},
        {"on": "cntn_to_dcsn.value", "method": "none: the adapter reports welfare as not computed", "handler": "adapter"},
        {"on": "arvl_to_dcsn", "method": "!histogram", "handler": "adapter"},
        {"on": "population.distribution", "method": "the adapters' shared fixed point, with deaths and newborns",
         "handler": "adapter"},
        {"on": "diagnostics.expectation", "method": "a finer quadrature of the stated laws than the household's",
         "handler": "adapter"},
    ]

    def __init__(self):
        self.model_dir = None            # where the model files go: the run's folder, set in main()
        self.solver = {"routine": "dolo.algos.egm.egm", "types": []}     # how each type's solve ended (provenance)

    def version(self):
        return importlib.metadata.version("dolo")       # dolo has no __version__

    def commit(self):
        return None                      # a release, named by its version

    def settings(self, level, lev):
        return {"level": level,
                "nodes_per_shock": lev["nodes"], "transition_nodes_per_shock": lev["transition_nodes"],
                "savings_points": lev["solve_points"], "savings_top": lev["solve_top"], "savings_nesting": lev["nest"],
                "savings_start_above_natural_limit": ABOVE_LIMIT,
                "solution_tolerance": lev["tol"], "max_iterations": MAXIT,
                "grid_points": self._orders(lev), "grid_max": lev["solve_top"], "grid_step": GRID_STEP,
                "histogram_points": lev["dist_points"], "histogram_top": lev["dist_top"],
                "diagnostics_nodes_per_piece": common.DIAG_NODES}

    @staticmethod
    def _orders(lev):
        return int(round(lev["solve_top"] / GRID_STEP)) + 1

    def _model_file(self, member, beta, a_min, lev):
        """Write the recast model file for one type and return its path."""
        if self.model_dir is None:
            self.model_dir = tempfile.mkdtemp(prefix="dolo-adapter-")
        text = MODEL.format(name=f"{member.family} member {member.hash[:12]}, beta {beta!r}",
                            beta=_num(beta), L=_num(member.L), rho=_num(member.rho), R=_num(member.R), G=_num(member.G),
                            a_min=_num(a_min), cbar=_num(CBAR), c=_num(C_START),
                            m_lo=_num(a_min), m_hi=_num(a_min + lev["solve_top"]), orders=self._orders(lev))
        path = pathlib.Path(self.model_dir) / f"model-beta-{beta!r}.yaml"
        if "http" in str(path):
            raise ValueError(f"dolo's yaml_import reads a path that holds 'http' as a URL: {path}")
        path.write_text(text, encoding="utf-8")
        return path

    def solve(self, member, beta, nodes, own):
        import dolo
        from dolo.algos.egm import egm
        from dolo.numeric.distribution import FiniteDistribution

        rho, L, R, G = member.rho, member.L, member.R, member.G
        P, PSI, XI = common.joint_shocks(member, *nodes)
        # a_min, the constraint in force in what is solved: a_Art for an artificial member, the natural limit of the nodes
        # for a natural one, by the arithmetic of the effective member (common.effective_member_block)
        kappa = float(PSI.min()) * G / R
        a_nat = None if kappa >= 1 else -float(XI.min()) * kappa / (1 - kappa) + 0.0
        a_min = float(member.a_art) if a_nat is None else max(float(member.a_art), a_nat)
        # ---- encode: the model file, the nodes, the savings grid and the uniform grid of m
        model = dolo.yaml_import(str(self._model_file(member, beta, a_min, own)))
        grid, _ = model.discretize()                       # the uniform grid of m, from domain and options.grid
        dp = FiniteDistribution(np.column_stack([PSI, XI]), np.asarray(P, float))
        start = a_min + (ABOVE_LIMIT if member.natural else 0.0)      # at a_min the kink's point is solved; above the
        a_grid = start + nested_grid(own["solve_top"], own["solve_points"], own["nest"])   # natural limit, c' > 0
        # ---- the call; egm prints three numbers for every node at every iteration
        with contextlib.redirect_stdout(io.StringIO()):
            sol = egm(model, grid=grid, dp=dp, a_grid=a_grid, η_tol=own["tol"], maxit=MAXIT)
        ended = {"beta": float(beta), "iterations": int(sol.iterations), "a_converged": bool(sol.a_converged),
                 "a_tol": float(sol.a_tol), "err": float(sol.err)}
        self.solver["types"] = [t for t in self.solver["types"] if t["beta"] != float(beta)] + [ended]
        if not sol.a_converged:
            raise RuntimeError(f"dolo's egm did not converge for beta {beta}: err {sol.err:.3e} against {sol.a_tol:.1e} "
                               f"after {MAXIT} iterations")
        # ---- decode: sol.dr is a cubic spline through egm's rule at the uniform grid's nodes; read those values linearly
        m_nodes = sol.dr.endo_grid.nodes
        rule = LinearRule(m_nodes[:, 0], sol.dr(m_nodes)[:, 0])
        if not member.natural:
            # the kink's point, from the Euler equation at a = a_min: m_k = a_min + u'^-1(beta L R E[(G psi)^-rho u'(c(m'))])
            rhs = beta * L * R * common.expected_marginal_value(rule, a_min, P, PSI, XI, R, G, rho)[0]
            c_k = float(common.inverse_marginal_utility(rhs, rho))
            rule = rule.with_point(a_min + c_k, c_k)
        return SimpleNamespace(cFunc=rule, vFunc=None, mNrmMin=a_min)


TOOLKIT = DoloToolkit()


def main(argv):
    out = argparse.ArgumentParser(add_help=False)
    out.add_argument("--out")
    TOOLKIT.model_dir = out.parse_known_args(argv)[0].out      # the model files go beside the results
    try:
        return common.run(argv, TOOLKIT)
    finally:
        config = sys.modules.get("dolo.config")
        if config is not None:                # dolo makes a directory in the system's temporary folder on import and
            with contextlib.suppress(OSError):    # leaves it there, empty
                os.rmdir(config.temp_dir)


if __name__ == "__main__":
    main(sys.argv[1:])
