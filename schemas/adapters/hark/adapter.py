"""HARK's adapter for the buffer-stock families: a parameter file in, HARK's solution, a results file out.

The adapter solves a member of a buffer-stock family with HARK's MarkovConsumerType and writes the files the schemas ask for: a request file
of comparison points (generated from a level-1 solution when none is given), a method file, a settings file and
`results.json`, which it validates against `bst/results.schema.json`. The checker then verifies the report:

    python ../../checker/check.py <member.yaml> --verify-results <out>/results.json

How the member is solved.
  1. The checker reads the member: its hash and its laws, the stated member.
  2. The adapter discretizes the laws itself, since HARK has no truncated law: equiprobable bins of each law, each node the
     bin's exact conditional mean, so that every mean is one by the law's own normalization. What HARK then solves is the
     adapter's effective member (effective-member.md). The results file reports that member's expectations, lowest values
     and derived parameters, decides every condition of conditions.md on it, and takes every status from those verdicts.
  3. Each type is solved by HARK's MarkovConsumerType with two employment states, employed and unemployed, and identical
     rows: unemployment with probability wp whatever the previous state, the nonpersistent chain that writes the
     buffer-stock families' unemployment event as a state. The employed state's income is the scaled employed draw, the unemployed state's the
     income while unemployed xi_u; psi is drawn in both. The two states' rules must then be the same function of m, which
     the adapter asserts. The rule is cubic Hermite and the value function is on.
  4. The stationary population, under the population measure and, when the adapter's verdicts say it exists, the income
     measure: a lottery onto an asset grid (Young, 2010) with mortality and newborn replacement in one sparse linear solve;
     under the income measure the permanent shock is tilted by psi and survivors weighted by L G (Harmenberg, 2021). Since
     the next state does not depend on the current one, the distribution of end-of-period assets is the whole state.
  5. Every quantity the schema asks for: the rule and its MPC at the request file's points, the exported rule, the kink and
     the two targets, the generalized Lorenz ordinates, masses and means, welfare in utils, marginal welfare, the Euler
     residuals against a Gauss-Legendre quadrature in the logs split at the kink, with that quadrature's precision and the
     same residual under the adapter's own nodes, and the stationarity residual.

HARK is pinned to a commit on its branch natural-limit-infimum, stacked on its pull request #1858. #1858's Markov solver
evaluates each next state's expectation at the current state's points, as the standard solver does; released HARK
interpolates it on each state's own grid instead. The branch computes the natural borrowing constraint from the infima
of the laws, which the adapter records on each distribution, rather than from the lowest nodes, so a member that states
natural is solved under the stated laws' limit at every number of nodes.

Usage, with HARK at the pin (see README.md):
    python adapter.py <member.yaml> --out <dir> [--level 1|2|3|4|low|medium|high] [--request <request.yaml>] [--nodes N]
"""

import argparse
import json
import math
import os
import pathlib
import platform
import sys
from types import SimpleNamespace

import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.optimize import brentq
from scipy.sparse import csr_matrix, identity
from scipy.sparse.linalg import spsolve
from scipy.special import logsumexp, ndtr, ndtri

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from common import *  # noqa: E402,F401,F403  the code the adapters share (common.py)
from common import _lottery, _sorted  # noqa: E402,F401

ADAPTER_VERSION = "0.1"
SAME_RULE = 1e-12         # the largest relative difference allowed between the two employment states' rules


def installed_hark_commit():
    """The installed HARK's commit, from its distribution's direct_url.json (PEP 610), or None for an install without one.
    HARK.__version__ does not tell two installs from git apart; the commit does."""
    try:
        import importlib.metadata
        info = json.loads(importlib.metadata.distribution("econ-ark").read_text("direct_url.json") or "{}")
        return info.get("vcs_info", {}).get("commit_id")
    except Exception:
        return None


# ------------------------------------------------------------------------------------------------ the solution (HARK)
def _labeled(P, PSI, XI, name, bounds):
    """HARK's joint distribution of the permanent and transitory shocks, with the laws' own bounds, ((psi_inf, xi_inf),
    (psi_sup, xi_sup)), recorded as its limit: HARK reads the infima for the natural borrowing constraint."""
    from HARK.distributions import DiscreteDistribution, DiscreteDistributionLabeled
    limit = {"infimum": np.array(bounds[0], float), "supremum": np.array(bounds[1], float)}
    return DiscreteDistributionLabeled.from_unlabeled(
        DiscreteDistribution(P, np.vstack([PSI, XI]), seed=0, limit=limit), name=name, var_names=["PermShk", "TranShk"])


def shock_bounds(member):
    """The stated laws' bounds for each distribution HARK is given, as ((psi_inf, xi_inf), (psi_sup, xi_sup)): employed,
    psi and the scaled employed draw; unemployed, psi and xi_u; and the joint law, psi and the lower and upper of the
    two."""
    scale = employed_scale(member)
    psi = (float(member.psi.infimum), float(member.psi.supremum))
    emp = (scale * float(member.theta.infimum), scale * float(member.theta.supremum))
    xi_u = float(member.xi_u)
    joint = (min(emp[0], xi_u), max(emp[1], xi_u)) if member.wp > 0 else emp
    return {state: ((psi[0], xi[0]), (psi[1], xi[1]))
            for state, xi in (("employed", emp), ("unemployed", (xi_u, xi_u)), ("joint", joint))}


def boro_cnst_art(member):
    """HARK's artificial constraint: a_Art, or none for a member of a natural family, whose limit HARK computes itself from
    the infima recorded on its distributions."""
    return None if member.natural else float(member.a_art)


def _grid(lev):
    return dict(tolerance=lev["tol"], aXtraMin=1e-6, aXtraMax=lev["solve_top"], aXtraCount=lev["solve_points"],
                aXtraNestFac=lev["nest"], aXtraExtra=[None])


def solve_type(member, beta, nodes, lev):
    """One type solved by HARK's MarkovConsumerType on the nonpersistent chain: two states, employed and unemployed, every row
    (1 - wp, wp), each state's income its own nodes. HARK's constructors for the chain and the income process are switched
    off, since HARK otherwise rebuilds both from its defaults, the chain at construction and the income process on any
    update; the adapter asserts that HARK solved with its own. The two states' rules and values must be the same function of
    m, since the end-of-period value does not depend on the current state; the adapter asserts that too, and returns the
    employed state's solution with its rule, value and lower limit."""
    from HARK.ConsumptionSaving.ConsMarkovModel import MarkovConsumerType, init_indshk_markov
    R, G, L, wp = member.R, member.G, member.L, float(member.wp)
    states = state_shocks(member, *nodes)
    bounds = shock_bounds(member)
    chain = np.array([[1.0 - wp, wp], [1.0 - wp, wp]])
    constructors = dict(init_indshk_markov["constructors"], MrkvArray=None, IncShkDstn=None)
    p = dict(CRRA=member.rho, Rfree=[np.array([R, R])], PermGroFac=[np.array([G, G])], LivPrb=[np.array([L, L])],
             DiscFac=beta, BoroCnstArt=boro_cnst_art(member), cycles=0, T_cycle=1, vFuncBool=True, CubicBool=True,
             MrkvArray=[chain], MrkvPrbsInit=np.array([1.0, 0.0]), NewbornTransShk=True,
             IncShkDstn=[[_labeled(*states[0], "employed", bounds["employed"]),
                          _labeled(*states[1], "unemployed", bounds["unemployed"])]],
             PermShkStd=np.array([[0.1, 0.1]]), TranShkStd=np.array([[0.1, 0.1]]), PermShkCount=3, TranShkCount=3,
             UnempPrb=np.array([0.0, 0.0]), IncUnemp=np.array([0.0, 0.0]), UnempPrbRet=None, IncUnempRet=None,
             T_retire=0, T_age=None, AgentCount=1, constructors=constructors, **_grid(lev))
    agent = MarkovConsumerType(**p, verbose=False)
    agent.solve()
    assert np.array_equal(np.asarray(agent.MrkvArray[0]), chain), "HARK rebuilt the chain"
    for d, (P, PSI, XI) in zip(agent.IncShkDstn[0], states):
        assert (np.array_equal(np.asarray(d.pmv), P) and np.array_equal(np.asarray(d.atoms[0]), PSI)
                and np.array_equal(np.asarray(d.atoms[1]), XI)), "HARK rebuilt the income process"
    sol = agent.solution[0]
    lows = np.asarray(sol.mNrmMin, float)
    assert lows[0] == lows[1], ("the two states' lower limits differ", lows)
    m = lows[0] + np.geomspace(1e-6, lev["solve_top"], 2000)
    for f, what in ((sol.cFunc, "rules"), (sol.vFunc, "values")):
        e, u = np.asarray(f[0](m), float), np.asarray(f[1](m), float)
        gap = float(np.max(np.abs(e - u) / np.maximum(1.0, np.abs(e))))
        assert gap <= SAME_RULE, (f"the two employment states' {what} differ: the chain is not the nonpersistent one", gap)
    return SimpleNamespace(agent=agent, solution=[SimpleNamespace(cFunc=sol.cFunc[0], vFunc=sol.vFunc[0], mNrmMin=float(lows[0]))])


def solve_standard(member, beta, P, PSI, XI, lev):
    """The same type solved by HARK's standard IndShockConsumerType on the same joint nodes: the comparison the adapter's gate
    measures the Markov solution against (README.md)."""
    from HARK.ConsumptionSaving.ConsIndShockModel import IndShockConsumerType
    p = dict(CRRA=member.rho, Rfree=[member.R], PermGroFac=[member.G], LivPrb=[member.L], DiscFac=beta,
             BoroCnstArt=boro_cnst_art(member), cycles=0, T_cycle=1, vFuncBool=True, CubicBool=True,
             PermShkStd=[0.1], TranShkStd=[0.1], PermShkCount=3, TranShkCount=3,
             UnempPrb=0.0, IncUnemp=0.0, UnempPrbRet=0.0, IncUnempRet=0.0, T_retire=0, T_age=None, AgentCount=1, **_grid(lev))
    agent = IndShockConsumerType(**p, verbose=False)
    agent.IncShkDstn = [_labeled(P, PSI, XI, "income", shock_bounds(member)["joint"])]
    agent.solve()
    d = agent.IncShkDstn[0]
    assert np.array_equal(np.asarray(d.pmv), P) and np.array_equal(np.asarray(d.atoms[1]), XI), "HARK rebuilt the income process"
    return agent


# ------------------------------------------------------------------------------------------------ the whole file
# Each entry on a stage target carries its method's tag where there is one, and names the adapter's routine as its handler
# (numerics.md, "Tags and handlers"); HARK's cubic, whose slopes are the solution's MPCs, has no tag.
METHODS = [
    {"on": "policy.euler.solve", "method": "!time-iteration", "handler": "endogenous-grid"},
    {"on": "policy", "handler": "hark:cubic-hermite"},
    {"on": "E_ψ_θ_j", "method": "!quadrature", "handler": "hark:equiprobable-exact-mean-nodes-by-employment-state"},
    {"on": "cntn_to_dcsn.value", "method": "value-function"},
    {"on": "arvl_to_dcsn", "method": "!histogram", "handler": "hark:equiprobable-exact-mean-nodes-by-employment-state"},
    {"on": "population.distribution", "method": "hark:lottery-histogram-linear-solve"},
    {"on": "diagnostics.expectation", "method": "hark:gauss-legendre-log-support-split-at-kink"},
]


class HarkToolkit:
    """HARK's side of the adapter (common.py, "The Toolkit protocol")."""
    name = "HARK"
    driver = f"schemas/adapters/hark/adapter.py {ADAPTER_VERSION}"
    description = __doc__.splitlines()[0]
    representation = ("the unemployment event a state of a chain with identical rows; the newborn draws the employed "
                      "branch; the natural limit from the nodes' lowest values, as HARK computes it")
    diagnostics_method = "hark:gauss-legendre-log-support-split-at-kink"
    methods = METHODS
    solver = {"iteration": "HARK's MarkovConsumerType, infinite horizon, until the solution distance is below "
                           "solve_tolerance",
              "chain": "two employment states with identical rows (1 - wp, wp): the nonpersistent chain; "
                       "the two states' rules asserted equal",
              "kink": "where HARK's lower envelope of the unconstrained cubic rule and the 45-degree line "
                      "leaves the line; HARK's first endogenous gridpoint sits at a = aXtraMin = 1e-6 above it",
              "shock_nodes": "the laws' equiprobable bins with exact conditional means, handed to HARK by "
                             "employment state; HARK's own lognormal construction is not used"}

    @staticmethod
    def version():
        import HARK
        return HARK.__version__

    @staticmethod
    def commit():
        return installed_hark_commit()

    @staticmethod
    def settings(level, lev):
        return {"level": level, "nodes_per_shock": lev["nodes"], "transition_nodes_per_shock": lev["transition_nodes"],
                "solve_grid_points": lev["solve_points"], "solve_grid_min": 1e-6, "solve_grid_max": lev["solve_top"],
                "solve_grid_nesting": lev["nest"], "solve_tolerance": lev["tol"],
                "distribution_grid_points": lev["dist_points"], "distribution_grid_top": lev["dist_top"],
                "diagnostics_nodes_per_piece": DIAG_NODES}

    @staticmethod
    def solve(member, beta, nodes, lev):
        return solve_type(member, beta, nodes, lev).solution[0]


TOOLKIT = HarkToolkit()


def main(argv=None):
    return run(argv, TOOLKIT)


if __name__ == "__main__":
    main()
