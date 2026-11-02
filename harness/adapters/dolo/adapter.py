"""dolo's adapter for the buffer-stock families: a parameter file in, dolo's solution, a results file out.

The adapter solves a member of a buffer-stock family with dolo's endogenous grid method, `dolo.algos.egm.egm`, and writes
the files the schemas ask for: a request file of comparison points (generated from a level-1 solution when none is
given), a method file, a settings file and `results.json`, validated against `bst/results.schema.json`. The checker then
verifies the report:

    python ../../../schemas/checker/check.py <member.yaml> --verify-results <out>/results.json

How the member is solved (the Rosetta Stone, ../../../rosetta/dolo.md).
  1. The checker reads the member: its hash and its laws, the stated member.
  2. The household, normalized by permanent income, is written as a dolo model file: the state m, the control c, the
     poststate a, the exogenous psi and xi, the transition m' = a R/(G psi') + xi', and the Euler equation with the
     complementarity 0 <= c <= m - a_min, with EGM's four blocks. One model is written for each type.
  3. dolo's model-file language cannot state a truncated lognormal, and its own equiprobable nodes are bin medians. So the
     adapter passes the same nodes HARK's adapter builds, as a `FiniteDistribution`: equiprobable bins of each law, each
     node its bin's exact conditional mean, with the unemployment atom. Both toolkits then solve the same effective
     member (effective-member.md).
  4. `egm` iterates on a savings grid, the same multi-exponential grid HARK's adapter uses at each level, starting at
     a_min for an artificial member and 1e-6 above it otherwise. It returns its rule resampled on the model's uniform grid
     of m as a cubic spline, which rounds the kink. The adapter reads the rule back as egm's own iteration holds it:
     linear between the spline's node values, which are the endogenous rule's, with the kink's point added from the
     Euler equation at a = a_min (the class Rule). The MPC is the slope of the segment that holds m.
  5. dolo gives no value function, so welfare is reported as not computed. Everything else, the population, the
     effective member, the conditions, the statuses, the statistics and the residuals, comes from the code the adapters
     share (../common.py), as for HARK.

The adapter uses dolo's release 0.4.9.20, which needs Python below 3.12:
    uv run --python 3.11 --with dolo==0.4.9.20 --with jsonschema --with pyyaml --with referencing \\
        python adapter.py <member.yaml> --out <dir> [--level 1|2|3|4|low|medium|high] [--request <request.yaml>]
"""

import contextlib
import io
import pathlib
import sys
import tempfile
from types import SimpleNamespace

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from common import *  # noqa: E402,F401,F403  the code the adapters share (common.py)

ADAPTER_VERSION = "0.1"
# dolo's own setting at each level, beside the shared node counts and grids: the points of the uniform grid of m on which
# egm resamples its rule, from a_min to the level's solve_top, so that a point falls every 0.005 near the kink.
RULE_POINTS = {1: 20001, 2: 40001, 3: 80001, 4: 160001}
MAX_ITERATIONS = 50000

MODEL = """symbols:
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
    beta: {beta!r}
    L: {L!r}
    rho: {rho!r}
    R: {R!r}
    G: {G!r}
    a_min: {a_min!r}
    cbar: 1.0
    m: {m_cal!r}
    c: 1.0
    a: {a_cal!r}
    psi: 1.0
    xi: 1.0
domain:
    m: [{m_lo!r}, {m_hi!r}]
exogenous: !Normal
    Σ: [[0.01, 0.0], [0.0, 0.01]]
options:
    grid: !Cartesian
        orders: [{n_m}]
"""


def nested_exp_grid(lo, hi, n, nest):
    """The multi-exponential grid HARK's adapter solves on (HARK's make_grid_exp_mult): n points from lo to hi, equally
    spaced after log(x + 1) is taken `nest` times, so that the points crowd toward lo."""
    a, b = float(lo), float(hi)
    for _ in range(nest):
        a, b = np.log(a + 1.0), np.log(b + 1.0)
    g = np.linspace(a, b, n)
    for _ in range(nest):
        g = np.exp(g) - 1.0
    return g


class Rule:
    """dolo's rule, read back as dolo's own iteration holds it: linear between points, with the kink exact.

    egm iterates on the linear interpolation of its endogenous points, clipped to the complementarity's bounds, and then
    resamples that rule on the model's uniform grid of m as a cubic spline. The spline passes through its values at the
    grid's nodes, which are the endogenous rule's own values there, but between them it rounds the kink and ripples, by
    up to 10^-6 below it, so that households just below the kink would hold a sliver of assets. The rule is therefore read
    as the linear interpolation of the node values, with the kink's point added: the endogenous point at a = a_min, where
    c = m - a_min, found from the Euler equation on the same rule (dolo.md, "Departures"). Below the kink the node values
    are m - a_min exactly, since egm clips to the bound there. The MPC is the slope of the segment that holds m; above the
    top node the last segment is extended."""

    def __init__(self, xs, ys):
        self.xs, self.ys = np.asarray(xs, float), np.asarray(ys, float)
        self.slopes = np.diff(self.ys) / np.diff(self.xs)

    def _segment(self, x):
        return np.clip(np.searchsorted(self.xs, x, side="right") - 1, 0, len(self.slopes) - 1)

    def __call__(self, m):
        x = np.asarray(m, float)
        k = self._segment(x)
        out = self.ys[k] + self.slopes[k] * (x - self.xs[k])
        return float(out) if x.ndim == 0 else out

    def derivative(self, m):
        x = np.atleast_1d(np.asarray(m, float))
        return self.slopes[self._segment(x)]


def read_rule(dr, member, beta, a_min, P, PSI, XI, with_kink):
    """The Rule from egm's DecisionRule: its values at the uniform grid's nodes, and, where the constraint can bind, the
    kink's point m_k = a_min + u'^(-1)(beta L R E[(G psi)^(-rho) c(m'(a_min))^(-rho)])."""
    nodes = np.asarray(dr.endo_grid.nodes, float).ravel()
    values = np.asarray(dr.eval_s(nodes.reshape(-1, 1)), float).ravel()
    rule = Rule(nodes, values)
    if not with_kink:
        return rule, None
    E = expected_marginal_value(rule, a_min, P, PSI, XI, member.R, member.G, member.rho)[0]
    m_k = a_min + inverse_marginal_utility(float(beta) * member.L * member.R * E, member.rho)
    keep = np.abs(nodes - m_k) > 1e-12
    xs = np.concatenate([nodes[keep], [m_k]])
    ys = np.concatenate([values[keep], [m_k - a_min]])
    order = np.argsort(xs)
    return Rule(xs[order], ys[order]), float(m_k)


def solve_type(member, beta, nodes, lev, level=None):
    """One type of the member by dolo's egm on the adapter's nodes: the rule, no value, and the rule's lower limit."""
    from dolo import yaml_import
    from dolo.algos.egm import egm
    from dolo.numeric.distribution import FiniteDistribution

    a_min = float(member.a_art)                  # the constraint in force of the stated member: a_Art, or the laws' limit
    m_hi = float(lev["solve_top"])
    n_m = RULE_POINTS[level if level is not None else _level_of(lev)]
    text = MODEL.format(beta=float(beta), L=float(member.L), rho=float(member.rho), R=float(member.R),
                        G=float(member.G), a_min=a_min, m_cal=a_min + 1.5, a_cal=a_min + 0.5,
                        m_lo=a_min, m_hi=m_hi, n_m=n_m)
    with tempfile.TemporaryDirectory() as tmp:
        path = pathlib.Path(tmp) / "household.yaml"
        path.write_text(text, encoding="utf-8")
        model = yaml_import(str(path))
    P, PSI, XI = joint_shocks(member, *nodes)
    dp = FiniteDistribution(np.column_stack([PSI, XI]), P)
    grid, _ = model.discretize()
    xtra = nested_exp_grid(1e-6, m_hi, lev["solve_points"], lev["nest"])
    # a_min itself is solved wherever the constraint can bind. Under bst-natural/1 the zero-income atom would take m' to
    # the limit from a = a_min, where c' = 0 and marginal utility has no finite value, so the grid starts 1e-6 above it.
    at_limit = member.family == "bst-natural/1"
    a_grid = a_min + (xtra if at_limit else np.concatenate([[0.0], xtra]))
    with contextlib.redirect_stdout(io.StringIO()):     # egm prints at every node of every iteration (dolo.md)
        sol = egm(model, grid=grid, dp=dp, a_grid=a_grid, η_tol=float(lev["tol"]), maxit=MAX_ITERATIONS)
    if not sol.a_converged:
        raise RuntimeError(f"dolo's egm did not converge for beta {beta}: last change {sol.err:.3e} after "
                           f"{sol.iterations} iterations (tolerance {lev['tol']})")
    rule, m_kink = read_rule(sol.dr, member, beta, a_min, P, PSI, XI, with_kink=not at_limit)
    return SimpleNamespace(cFunc=rule, vFunc=None, mNrmMin=a_min, kink=m_kink, iterations=int(sol.iterations),
                           err=float(sol.err))


def _level_of(lev):
    for k, v in LEVELS.items():
        if v["solve_points"] == lev["solve_points"] and v["solve_top"] == lev["solve_top"]:
            return k
    raise ValueError("not one of the levels")


METHODS = [
    {"on": "policy.euler.solve", "method": "!time-iteration", "handler": "dolo:egm"},
    {"on": "policy", "method": "!Linear", "handler": "adapter:linear-through-dolo-node-values-with-kink"},
    {"on": "E_ψ_θ_j", "method": "!quadrature", "handler": "adapter:equiprobable-exact-mean-nodes-as-finite-distribution"},
    {"on": "cntn_to_dcsn.value", "method": "none: not computed"},
    {"on": "arvl_to_dcsn", "method": "!histogram", "handler": "adapter:equiprobable-exact-mean-nodes"},
    {"on": "population.distribution", "method": "adapter:lottery-histogram-linear-solve"},
    {"on": "diagnostics.expectation", "method": "adapter:gauss-legendre-log-support-split-at-kink"},
]


class DoloToolkit:
    """dolo's side of the adapter (common.py, "The Toolkit protocol")."""
    name = "dolo"
    driver = f"harness/adapters/dolo/adapter.py {ADAPTER_VERSION}"
    description = __doc__.splitlines()[0]
    representation = ("the unemployment event an atom of the joint nodes, passed to dolo as a FiniteDistribution; the "
                      "newborn draws the employed branch; the constraint in force the stated member's, a_Art or the "
                      "laws' limit, as the bound of dolo's complementarity")
    diagnostics_method = "adapter:gauss-legendre-log-support-split-at-kink"
    methods = METHODS
    solver = {"iteration": "dolo's egm, iterated until the largest change in the endogenous rule and state is below "
                           "solve_tolerance",
              "rule": "linear between the values of egm's cubic spline at the nodes of the model's uniform grid of m, "
                      "which are egm's own endogenous rule there; the MPC the slope of the segment",
              "kink": "the endogenous point at a = a_min, from the Euler equation on that rule, added to the rule's "
                      "points; below it c = m - a_min, as egm clips to the bound",
              "shock_nodes": "the laws' equiprobable bins with exact conditional means, the same as HARK's adapter's, "
                             "passed as a FiniteDistribution; dolo's own discretization is not used",
              "value": "none: dolo's egm gives no value function, so welfare is not computed"}

    @staticmethod
    def version():
        import importlib.metadata
        return importlib.metadata.version("dolo")

    @staticmethod
    def commit():
        return None

    @staticmethod
    def settings(level, lev):
        return {"level": level, "nodes_per_shock": lev["nodes"], "transition_nodes_per_shock": lev["transition_nodes"],
                "solve_grid_points": lev["solve_points"], "solve_grid_min": 1e-6, "solve_grid_max": lev["solve_top"],
                "solve_grid_nesting": lev["nest"], "solve_tolerance": lev["tol"], "max_iterations": MAX_ITERATIONS,
                "rule_grid_points": RULE_POINTS[level], "rule_grid_max": lev["solve_top"],
                "distribution_grid_points": lev["dist_points"], "distribution_grid_top": lev["dist_top"],
                "diagnostics_nodes_per_piece": DIAG_NODES}

    @staticmethod
    def solve(member, beta, nodes, lev):
        return solve_type(member, beta, nodes, lev)


TOOLKIT = DoloToolkit()


def main(argv=None):
    return run(argv, TOOLKIT)


if __name__ == "__main__":
    main()
