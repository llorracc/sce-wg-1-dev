"""HARK's adapter for bst/1: a parameter file in, HARK's solution, a results file out.

The adapter solves a bst/1 member with HARK's MarkovConsumerType and writes the files the schemas ask for: a request file
of comparison points (generated from a level-1 solution when none is given), a method file, a settings file and
`results.json`, which it validates against `bst-1/results.schema.json`. The checker then verifies the report:

    python ../../checker/check.py <member.yaml> --verify-results <out>/results.json

How the member is solved.
  1. The checker reads the member: its hash and its laws, the stated member.
  2. The adapter discretizes the laws itself, since HARK has no truncated law: equiprobable bins of each law, each node the
     bin's exact conditional mean, so that every mean is one by the law's own normalization. What HARK then solves is the
     adapter's effective member (effective-member.md). The results file reports that member's expectations, lowest values
     and derived parameters, decides every condition of conditions.md on it, and takes every status from those verdicts.
  3. Each type is solved by HARK's MarkovConsumerType with two employment states, employed and unemployed, and identical
     rows: unemployment with probability wp whatever the previous state, the nonpersistent chain that writes bst/1 as a
     member of the Markov family. The employed state's income is the scaled employed draw, the unemployed state's the
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

HERE = pathlib.Path(__file__).resolve().parent
SCHEMAS = HERE.parent.parent
PROBS = ["0.01", "0.05", "0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9", "0.95", "0.99", "0.999", "1"]
REQUEST_U = ["0.01", "0.05", "0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9", "0.95", "0.99"]
ABOVE_99 = [1.5, 2.0, 4.0, 8.0]          # the request's points above the 99th percentile, as multiples of it
# The precision levels: the solution grid (points, top, nesting, HARK's convergence tolerance), the nodes per shock in the
# household's expectation and in the population's transition, and the distribution grid (points, top). HARK's default
# tolerance of 1e-6 leaves human wealth and the limiting MPC unconverged above the grid, so the levels set their own.
LEVELS = {1: dict(solve_points=300, solve_top=100.0, nest=3, tol=1e-8, nodes=7, transition_nodes=7, dist_points=4000, dist_top=60.0),
          2: dict(solve_points=600, solve_top=200.0, nest=3, tol=1e-10, nodes=15, transition_nodes=15, dist_points=8000, dist_top=120.0),
          3: dict(solve_points=1200, solve_top=400.0, nest=3, tol=1e-12, nodes=31, transition_nodes=31, dist_points=16000, dist_top=240.0),
          4: dict(solve_points=2400, solve_top=800.0, nest=3, tol=1e-12, nodes=63, transition_nodes=31, dist_points=32000, dist_top=480.0)}
NAMED_LEVELS = {"low": 1, "medium": 2, "high": 3}
DIAG_NODES = 32                           # Gauss-Legendre nodes per piece per shock in the diagnostics' expectation
ADAPTER_VERSION = "0.1"
QUANTILE_PROBS = PROBS    # the probabilities the quantile maps carry: the results schema's own, read in main()
THREAD_VARS = ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS")
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


def schema_quantile_probabilities(schemas):
    """The probabilities the results schema asks quantiles at: the required keys of the map that DistributionBlock.quantiles
    refers to. Read from the schema, so that a file matches the schema it is validated against."""
    schema = json.load(open(os.path.join(schemas, "bst-1", "results.schema.json"), encoding="utf-8"))
    ref = schema["$defs"]["DistributionBlock"]["properties"]["quantiles"]["$ref"].rsplit("/", 1)[-1]
    return list(schema["$defs"][ref]["required"])


def blas_threads():
    """The thread count the linear algebra runs with: the first of OpenBLAS's, OpenMP's and MKL's variables that is set, else every
    logical core, OpenBLAS's default."""
    for k in THREAD_VARS:
        v = os.environ.get(k, "").strip()
        if v.isdigit() and int(v) >= 1:
            return int(v)
    return os.cpu_count() or 1


def hardware():
    """The hardware, as the schema's provenance asks for it: the architecture and the logical cores, nothing that names the
    machine."""
    return f"{platform.machine()}, {os.cpu_count()} logical cores"


def numerical_environment():
    """The schema's free-form provenance.environment: the interpreter, the numerical libraries, the BLAS build and its thread
    variables. No operating-system string."""
    import numba
    import scipy
    try:
        blas = np.show_config(mode="dicts")["Build Dependencies"]["blas"]
        blas = f"{blas.get('name')} {blas.get('version')}"
    except Exception:
        blas = "unknown"
    return {"python": sys.version.split()[0], "numpy": np.__version__, "scipy": scipy.__version__, "numba": numba.__version__,
            "blas": blas, "thread_variables": {k: os.environ[k] for k in THREAD_VARS if k in os.environ}}


# ------------------------------------------------------------------------------------------------ the checker's objects
def load_checker(schemas):
    sys.path.insert(0, os.path.join(schemas, "checker"))
    import bst1, canonical  # noqa: E402
    return bst1, canonical


def file_hash(canonical, path):
    """The checker's hash of a strict-YAML file: canonical JSON of the parsed values, SHA-256."""
    return canonical.model_hash(canonical.load_strict(open(path, encoding="utf-8").read()))


def dump_strict_yaml(data, path):
    """Write a mapping in the strict subset (plain scalars, flow lists; no booleans, tags, anchors)."""
    import yaml
    open(path, "w", encoding="utf-8").write(yaml.safe_dump(data, sort_keys=False, default_flow_style=None, width=120, allow_unicode=True))


# ------------------------------------------------------------------------------------------------ the laws, discretized
def _lognormal_like(law):
    return type(law).__name__ in ("TruncatedLogNormal", "LogNormal")


def _z_bounds(law):
    nrm = law.normal
    return (nrm.bot if math.isfinite(nrm.bot) else -8.5), (nrm.top if math.isfinite(nrm.top) else 8.5)


def law_nodes(law, n):
    """(probabilities, values): n equiprobable nodes of a shock law, each the exact conditional mean of its bin (the solver's and
    the transition's discretization); a Discrete or Degenerate law is its own atoms."""
    name = type(law).__name__
    if _lognormal_like(law):
        nrm = law.normal
        loc, s = nrm.location, nrm.scale
        Fb, Ft = ndtr(nrm.bot), ndtr(nrm.top)
        edges = ndtri(Fb + (Ft - Fb) * np.arange(n + 1) / n)
        den = ndtr(edges[1:]) - ndtr(edges[:-1])
        num = ndtr(edges[1:] - s) - ndtr(edges[:-1] - s)
        return np.full(n, 1.0 / n), np.exp(loc + 0.5 * s * s) * num / den
    if name == "Discrete":
        return np.asarray(law.params["probs"], float), np.asarray(law.params["values"], float)
    if name == "Degenerate":
        return np.array([1.0]), np.array([1.0])
    raise NotImplementedError(f"no discretization for the law {name} yet")


def law_quadrature(law, n, split_at=None):
    """(weights, values) of a Gauss-Legendre rule in the log of a (truncated) lognormal law, in n nodes per piece, the support
    split at `split_at` (in the law's own units) when that value lies inside it: the diagnostics' expectation. A Discrete or
    Degenerate law is summed exactly."""
    if not _lognormal_like(law):
        return law_nodes(law, n)
    nrm = law.normal
    loc, s = nrm.location, nrm.scale
    bot, top = _z_bounds(law)
    edges = [bot, top]
    if split_at is not None and split_at > 0:
        z_split = (math.log(split_at) - loc) / s
        if bot < z_split < top:
            edges = [bot, z_split, top]
    ws, xs = [], []
    for lo, hi in zip(edges[:-1], edges[1:]):
        z, w = leggauss(n)
        z = 0.5 * (hi - lo) * z + 0.5 * (hi + lo)
        ws.append(0.5 * (hi - lo) * w * np.exp(-0.5 * z * z) / math.sqrt(2 * math.pi) / nrm.mass)
        xs.append(np.exp(loc + s * z))
    w = np.concatenate(ws)
    return w / w.sum(), np.concatenate(xs)


def employed_scale(member):
    return float(member.employed_scale) if member.employed_scale is not None else 1.0


def state_shocks(member, p_psi, psi, p_th, th):
    """The income shocks of each employment state, as (probabilities, psi, xi) over the product of the permanent nodes and the
    state's transitory nodes: employed, the scaled employed draws; unemployed, the income while unemployed xi_u."""
    scale = employed_scale(member)
    employed = (np.outer(p_psi, p_th).ravel(), np.repeat(psi, len(th)), np.tile(scale * th, len(psi)))
    unemployed = (np.asarray(p_psi, float).copy(), np.asarray(psi, float).copy(), np.full(len(psi), float(member.xi_u)))
    return employed, unemployed


def joint_shocks(member, p_psi, psi, p_th, th):
    """The joint income shocks (P, PSI, XI) over the product of the permanent nodes and the transitory nodes (the unemployment
    atom, then the scaled employed draws): the two states mixed by the chain's row."""
    scale = employed_scale(member)
    if member.wp > 0:
        p_xi = np.concatenate([[member.wp], (1.0 - member.wp) * p_th])
        xi = np.concatenate([[member.xi_u], scale * th])
    else:
        p_xi, xi = p_th, scale * th
    return np.outer(p_psi, p_xi).ravel(), np.repeat(psi, len(xi)), np.tile(xi, len(psi))


def shocks(member, n):
    """The nodes at n equiprobable nodes per shock, the joint shocks they give, and the newborn's first draws: the employed
    branch only (bst/1's model schema: a newborn is born employed), as (probabilities, values of m)."""
    p_psi, psi = law_nodes(member.psi, n)
    p_th, th = law_nodes(member.theta, n)
    P, PSI, XI = joint_shocks(member, p_psi, psi, p_th, th)
    return (p_psi, psi, p_th, th), P, PSI, XI, (p_th, employed_scale(member) * th)


# ------------------------------------------------------------------------------------------------ the effective member
def expectations_and_lowest(member, p_psi, psi, p_th, th):
    """The expectations the family names (conditions.md) under one representation of the laws (equiprobable nodes plus the
    unemployment state), and that representation's lowest values of psi and of the income ratio: numbers free of the
    representation's form, which is what the schema sees of an effective member."""
    rho = member.rho
    scale = employed_scale(member)
    if member.wp > 0:
        p_xi = np.concatenate([[member.wp], (1.0 - member.wp) * p_th])
        xi = np.concatenate([[member.xi_u], scale * th])
    else:
        p_xi, xi = np.asarray(p_th, float), scale * th
    psi_low, inc_low = float(psi.min()), float(xi.min())
    if member.wp > 0 and member.xi_u == 0.0:
        p_min = float(member.wp)                 # income is zero whatever psi draws: the checker's own rule for p_min
    else:
        p_min = float(p_xi[xi == inc_low].sum()) * float(p_psi[psi == psi_low].sum())
    lg = np.log(psi)
    E = {"psi_mean": float(np.dot(p_psi, psi)), "theta_mean": float(np.dot(p_th, th)),
         "psi_pow_1_minus_rho": float(np.dot(p_psi, psi ** (1.0 - rho))), "psi_inverse": float(np.dot(p_psi, 1.0 / psi)),
         "psi_log": float(np.dot(p_psi, lg)), "psi_log_psi": float(np.dot(p_psi, psi * lg)),
         "psi_squared": float(np.dot(p_psi, psi * psi)), "psi_pow_rho_minus_1": float(np.dot(p_psi, psi ** (rho - 1.0))),
         "psi_pow_rho": float(np.dot(p_psi, psi ** rho)), "worst_income_mass": p_min}
    return E, {"psi": psi_low, "income": inc_low}


def effective_member_block(bst1, member, p_psi, psi, p_th, th, representation, population=None):
    """What the toolkit solved, as the schema asks for it (effective-member.md): the expectations the family names under the
    solver's own nodes; the lowest values of psi and of the income ratio in that representation; the derived parameters those
    lowest values give, the natural limit among them, as HARK computes it from the discretized shocks' minimum; and, when the
    population's forward transition runs under another representation, that one's expectations and lowest values in the
    optional `population` block, which decides the GIC-Szeidl, the GIC-Harmenberg, the welfare conditions and the tail
    exponents (the natural limit and the constraint in force stay the household's)."""
    R, G = member.R, member.G
    E, lowest = expectations_and_lowest(member, p_psi, psi, p_th, th)
    natural = bst1.natural_limit_from(lowest["psi"], lowest["income"], G, R)   # None when psi_min >= R/G: no finite limit
    a_art = float(member.a_art)
    in_force = a_art if natural is None else max(a_art, natural)
    block = {"expectations": E, "lowest": lowest,
             "derived": {"natural_limit": natural, "constraint_in_force": in_force,
                         "worst_income": lowest["psi"] * lowest["income"], "employed_scale": employed_scale(member)},
             "representation": representation}
    if population is not None:
        p_psi_t, psi_t, p_th_t, th_t, text = population
        E_t, lowest_t = expectations_and_lowest(member, p_psi_t, psi_t, p_th_t, th_t)
        block["population"] = {"expectations": E_t, "lowest": lowest_t, "representation": text}
    return block


def population_expectations(eff):
    """The expectations that decide the conditions on the stationary population: the population block's when present, else
    the household's (the checker's rule)."""
    return eff["population"]["expectations"] if "population" in eff else eff["expectations"]


def own_conditions(bst1, member, beta, E, E_pop, binds):
    """Every condition of conditions.md decided on the effective member: the factors by the checker's own arithmetic on the
    reported expectations (`bst1.Member.factors`, with the population's E[log psi] and E[psi log psi] for the GIC-Szeidl and
    the GIC-Harmenberg), and the two welfare conditions by the lower-tail case: the artificial constraint binding (every
    welfare mean finite), else the atom at the worst income that every finite representation has, with the population's
    worst-income mass and E[psi^q]."""
    rho, L, R, G = member.rho, member.L, member.R, member.G
    E_conditions = dict(E, psi_log=E_pop["psi_log"], psi_log_psi=E_pop["psi_log_psi"])
    out = {c["name"]: {"factor": float(c["factor"]), "bound": float(c["bound"]), "holds": bool(c["holds"])}
           for c in member.factors(beta, E_conditions)}
    thorn = (R * beta * L) ** (1.0 / rho)
    for key, q, moment in (("welfare", rho - 1.0, E_pop["psi_pow_rho_minus_1"]), ("marginal_welfare", rho, E_pop["psi_pow_rho"])):
        if binds:
            out[key] = {"case": bst1.CASE_BINDING, "factor": None, "holds": True}
        elif q <= 0:
            out[key] = {"case": "no negative moment needed", "factor": None, "holds": True}
        else:
            f = float(bst1.atom_factor(E_pop["worst_income_mass"], q, rho, L, G, thorn, moment))
            out[key] = {"case": bst1.CASE_ATOM, "factor": f, "holds": f < 1.0}
    return out


def tail_root(log_phi, start):
    """The smallest z > start with phi(z) = 1, given log phi, or None when phi stays below 1 (the checker's search)."""
    z = start if start > 0 else 1e-6
    if log_phi(z) >= 0:
        return z if start > 0 else None
    step = 1e-6
    while log_phi(z + step) < 0:
        step *= 2
        if z + step > 1e6:
            return None
    return float(brentq(log_phi, z, z + step, xtol=1e-12))


def own_domain(bst1, member, beta, conds, E, derived, p_psi, psi):
    """The statuses, from the family's domain rules (conditions.md) applied to the toolkit's own verdicts: the checker's
    `_domain` with the effective member's expectations in place of the stated law's closed forms; E and the psi nodes are the
    household's for the kink and the two targets, and the tail exponents are taken from the nodes passed in (the population's
    when its representation differs). R(1 - kappa_min)/G, the growth factor of m at high wealth, is min(thorn, R)/G."""
    rho, L, R, G = member.rho, member.L, member.R, member.G
    thorn = (R * beta * L) ** (1.0 / rho)
    growth = min(thorn, R) / G
    natural, in_force = derived["natural_limit"], derived["constraint_in_force"]
    d = {"kink": natural is None or in_force > natural + bst1.TOLERANCE,
         "buffer_stock_target": growth * E["psi_inverse"] < 1.0, "pseudo_target": growth < 1.0}
    keep = p_psi > 0
    lp, lg = np.log(p_psi[keep]), np.log(psi[keep])
    log_moment = lambda k: float(logsumexp(lp + k * lg))
    log_growth = math.log(growth)
    if L < 1:
        population = lambda z: math.log(L) + z * log_growth + log_moment(-z)
        income = lambda j: math.log(L * G) + j * log_growth + log_moment(1.0 - j)
        d["population_measure"] = True
        d["population_tail_exponent"] = tail_root(population, 0.0)
        d["income_measure"] = L * G < 1
        d["income_tail_exponent"] = tail_root(income, 0.0) if d["income_measure"] else None
    else:
        population = lambda z: z * log_growth + log_moment(-z)
        income = lambda j: j * log_growth + log_moment(1.0 - j)
        d["population_measure"] = conds["GIC-Szeidl"]["holds"]
        d["population_tail_exponent"] = tail_root(population, 1e-9) if d["population_measure"] else None
        d["income_measure"] = conds["GIC-Harmenberg"]["holds"]
        d["income_tail_exponent"] = tail_root(income, 1e-9) if d["income_measure"] else None
    for measure in ("population", "income"):
        exponent, exists = d[f"{measure}_tail_exponent"], d[f"{measure}_measure"]
        d[f"{measure}_mean"] = exists and (exponent is None or exponent > 1)
        d[f"{measure}_variance"] = exists and (exponent is None or exponent > 2)
    d["welfare"] = d["population_measure"] and conds["welfare"]["holds"]
    d["marginal_welfare"] = d["population_measure"] and conds["marginal_welfare"]["holds"]
    return d


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
    """HARK's artificial constraint: a_Art, or none for a member that states natural, whose limit HARK computes itself from
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


def crra_u(c, rho):
    c = np.asarray(c, float)
    return np.log(c) if abs(rho - 1.0) < 1e-12 else c ** (1.0 - rho) / (1.0 - rho)


def inverse_marginal_utility(x, rho):
    return x ** (-1.0 / rho)


# ------------------------------------------------------------------------------------------------ the stationary population
def make_agrid(n, top, a_lo, natural):
    """The asset grid: geometric nodes above the constraint in force, with a node AT the constraint only when it is artificial
    (mass sits there). At the natural constraint no household ever arrives, and a node there would carry lottery mass at which
    the zero-income event gives m = a_lo, c = 0 and an infinite marginal utility and value."""
    nodes = a_lo + np.geomspace(1e-6, top - a_lo, n)
    return nodes if natural else np.concatenate([[a_lo], nodes])


def _lottery(agrid, x):
    n = len(agrid)
    x = np.clip(x, agrid[0], agrid[-1])
    j = np.clip(np.searchsorted(agrid, x, side="right") - 1, 0, n - 2)
    w_hi = (x - agrid[j]) / (agrid[j + 1] - agrid[j])
    return j, 1.0 - w_hi, w_hi


def transition(cf, agrid, P, PSI, XI, R, G, a_lo, tilt=False):
    """The survivors' transition on the asset grid (a linear lottery), the probabilities tilted by psi under the income measure."""
    n = len(agrid)
    rows, cols, vals = [], [], []
    wts = P * PSI if tilt else P
    for k in range(len(P)):
        m_next = R * agrid / (G * PSI[k]) + XI[k]
        a_next = np.maximum(m_next - np.asarray(cf(m_next)), a_lo)
        j, wlo, whi = _lottery(agrid, a_next)
        rows += [j, j + 1]
        cols += [np.arange(n), np.arange(n)]
        vals += [wts[k] * wlo, wts[k] * whi]
    return csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(n, n))


def newborn_dist(cf, agrid, nb_p, nb_m, a_lo):
    nu = np.zeros(len(agrid))
    for p_k, m_k in zip(nb_p, nb_m):
        a0 = max(float(m_k) - float(cf(float(m_k))), a_lo)
        j, wlo, whi = _lottery(agrid, np.array([a0]))
        nu[j[0]] += p_k * wlo[0]
        nu[j[0] + 1] += p_k * whi[0]
    return nu


def stationary(T, nu, survivor_share):
    """mu = s T mu + (1 - s) nu, s the survivors' share of mass (L, or L G under the income measure); s = 1: the eigenvector."""
    n = T.shape[0]
    if survivor_share < 1.0:
        mu = spsolve((identity(n, format="csc") - survivor_share * T.tocsc()), (1.0 - survivor_share) * nu)
    else:
        mu = np.full(n, 1.0 / n)
        for _ in range(200000):
            new = T @ mu
            new /= new.sum()
            if np.abs(new - mu).max() < 1e-14:
                mu = new
                break
            mu = new
    mu = np.clip(np.asarray(mu).ravel(), 0.0, None)
    return mu / mu.sum()


def arrivals(mu, agrid, P, PSI, XI, R, G, survivor_share, nb_p, nb_m, tilt=False):
    """The beginning-of-period cross-section of m as weighted samples: survivors from every (asset node, shock) and newborns."""
    m_s = (R * agrid[:, None] / (G * PSI[None, :]) + XI[None, :]).ravel()
    w_k = P * PSI if tilt else P
    w_s = (survivor_share * mu[:, None] * w_k[None, :]).ravel()
    m = np.concatenate([m_s, np.asarray(nb_m, float)])
    w = np.concatenate([w_s, (1.0 - survivor_share) * np.asarray(nb_p, float)])
    keep = w > 0
    return m[keep], w[keep] / w[keep].sum()


class Population:
    """One stationary population (one type, one measure): the distribution on the asset grid and the arrivals cross-section.

    Only the arrivals' m and weights are kept; c, a, the MPC and the constraint mask are recomputed from the rule when asked for,
    the same function on the same points, so the same values bit for bit, which keeps the memory of the finest levels in
    bounds."""

    def __init__(self, cf, agrid, P, PSI, XI, R, G, a_lo, survivor_share, nb_p, nb_m, tilt):
        self.T = transition(cf, agrid, P, PSI, XI, R, G, a_lo, tilt=tilt)
        self.nu = newborn_dist(cf, agrid, nb_p, nb_m, a_lo)
        self.s = survivor_share
        self.mu = stationary(self.T, self.nu, survivor_share)
        self.args = (agrid, P, PSI, XI, R, G, survivor_share, nb_p, nb_m, tilt)
        self.m, self.w = arrivals(self.mu, *self.args)
        self.cf, self.a_lo = cf, a_lo

    @property
    def c(self):
        return np.asarray(self.cf(self.m), float)

    @property
    def a(self):
        return self.m - self.c

    @property
    def mpc(self):
        return np.asarray(self.cf.derivative(self.m), float)

    @property
    def at_floor(self):
        return self.a <= self.a_lo + 1e-9

    def derived(self):
        """(c, a, the MPC, the constraint mask) in one evaluation of the rule, for the type's own statistics."""
        c = self.c
        a = self.m - c
        return c, a, self.mpc, a <= self.a_lo + 1e-9

    def stationarity_residual(self):
        """The largest change in the GL ordinates of m over one forward step of the reported distribution. Releases the
        transition afterwards: the arrivals arrays are all the statistics need."""
        mu1 = self.s * (self.T @ self.mu) + (1.0 - self.s) * self.nu
        mu1 /= mu1.sum()
        m1, w1 = arrivals(mu1, *self.args)
        g0, g1 = gl_ordinates(self.m, self.w), gl_ordinates(m1, w1)
        self.T = self.nu = None
        return max(abs(g0[k] - g1[k]) for k in PROBS)


def pooled_pairs(pops, shares, key):
    """(x, w) of one variable over the types, stacked by share: the two arrays a pooled distribution statistic needs. One
    variable at a time, each type's x recomputed from its rule, to bound the memory of the finest levels."""
    return (np.concatenate([getattr(p, key) for p in pops]),
            np.concatenate([s * p.w for s, p in zip(shares, pops)]))


def pooled_population_block(pops, shares, mean_defined):
    """The pooled population block: means and masses exactly as share-weighted sums of the types' own; the distributions and the
    quartile means from one variable's stacked pairs at a time."""
    out = {}
    for key in ("m", "a", "c"):
        x, w = pooled_pairs(pops, shares, key)
        out[key] = distribution_block(x, w, mean_defined)
        del x, w
    mean_c = float(sum(s * np.dot(p.w, p.c) for s, p in zip(shares, pops)))
    out["mean_c"] = {"status": "value", "value": mean_c} if mean_defined else {"status": "undefined"}
    out["mass_at_constraint"] = float(sum(s * p.w[p.at_floor].sum() for s, p in zip(shares, pops)))
    out["fraction_a_nonpositive"] = float(sum(s * p.w[p.a <= 1e-12].sum() for s, p in zip(shares, pops)))
    out["mean_mpc"] = float(sum(s * np.dot(p.w, p.mpc) for s, p in zip(shares, pops)))
    a, w = pooled_pairs(pops, shares, "a")
    out["mpc_by_a_quartile"] = by_a_quartile(a, w, np.concatenate([p.mpc for p in pops]))
    return out


def pooled_income_block(incs, shares, mean_defined):
    if any(i is None for i in incs):
        return {"status": "undefined"}
    out = {"status": "value"}
    for key in ("m", "a"):
        x, w = pooled_pairs(incs, shares, key)
        out[key] = distribution_block(x, w, mean_defined)
        del x, w
    out["mass_at_constraint"] = float(sum(s * i.w[i.at_floor].sum() for s, i in zip(shares, incs)))
    mean_a = float(sum(s * np.dot(i.w, i.a) for s, i in zip(shares, incs)))
    out["mean_a"] = {"status": "value", "value": mean_a} if mean_defined else {"status": "undefined"}
    out["mean_mpc"] = float(sum(s * np.dot(i.w, i.mpc) for s, i in zip(shares, incs)))
    return out


def pooled_welfare_blocks(per_type, shares, pdom, rho):
    """W, F and M pooled are share-weighted means of the types' means (exact); the quartile means, the mean at the constraint and
    the GL ordinates of u' come from the stacked (a, w, u') arrays, u' recomputed from each type's rule."""
    pops = [d["pop"] for d in per_type]
    welfare = ({"status": "value", "mean_value": float(sum(s * d["Ev"] for s, d in zip(shares, per_type))),
                "mean_felicity": float(sum(s * d["Eu"] for s, d in zip(shares, per_type)))}
               if pdom["welfare"] else {"status": "undefined"})
    a, w = pooled_pairs(pops, shares, "a")
    up = np.concatenate([p.c ** (-rho) for p in pops])
    ends = np.cumsum([0] + [len(p.m) for p in pops])
    ups = [up[i:j] for i, j in zip(ends[:-1], ends[1:])]       # each type's own u', as views of the stacked array
    quart = by_a_quartile(a, w, up)
    floors = [p.at_floor for p in pops]
    floor_mass = sum(s * p.w[f].sum() for s, p, f in zip(shares, pops, floors))
    at_c = (float(sum(s * np.dot(p.w[f], u[f]) for s, p, u, f in zip(shares, pops, ups, floors)) / floor_mass)
            if floor_mass > 0 else None)
    if pdom["marginal_welfare"]:
        marginal = {"status": "value", "mean": float(sum(s * np.dot(p.w, u) for s, p, u in zip(shares, pops, ups))),
                    "by_a_quartile": quart, "at_constraint": at_c, "gl": gl_ordinates(up, w)}
        if at_c is None:
            marginal["undefined"] = ["at_constraint"]
    else:
        marginal = {"status": "undefined", "by_a_quartile": [None] + quart[1:], "at_constraint": None,
                    "undefined": ["mean", "by_a_quartile[0]", "at_constraint"]}
    return welfare, marginal


# ------------------------------------------------------------------------------------------------ statistics of weighted samples
def _sorted(x, w):
    o = np.argsort(x, kind="stable")
    ws = w[o]
    ws /= w.sum()               # in place: one array fewer at the pooled stage's peak, the same quotients
    return x[o], ws


def gl_ordinates(x, w):
    """Generalized Lorenz ordinates GL(p) = integral_0^p Q(u) du at the schema's probabilities."""
    x, w = _sorted(x, w)
    W = np.cumsum(w)
    cum = np.cumsum(x * w)
    out = {}
    for ps in PROBS:
        p = float(ps)
        k = int(np.searchsorted(W, p, side="left"))
        # W[k] - w[k], the mass below sample k, only where it is needed
        out[ps] = float(cum[-1]) if k >= len(x) else float((cum[k - 1] if k > 0 else 0.0) + x[k] * (p - (W[k] - w[k])))
    return out


def quantiles(x, w):
    x, w = _sorted(x, w)
    W = np.cumsum(w)
    return {ps: float(x[min(int(np.searchsorted(W, float(ps), side="left")), len(x) - 1)]) for ps in QUANTILE_PROBS}


def distribution_block(x, w, mean_defined=True):
    block = {"gl": gl_ordinates(x, w), "quantiles": quantiles(x, w)}
    if not mean_defined:
        block["gl"]["1"] = None
        block["undefined"] = ["1"]
    return block


def by_a_quartile(a, w, values):
    """Weighted means of `values` within the quartiles of a (by quantile rank: a mass point needs no tie rule)."""
    o = np.argsort(a, kind="stable")
    v = values[o]
    ws = w[o]
    ws /= w.sum()
    del o
    W = np.cumsum(ws)
    Wprev = np.subtract(W, ws, out=ws)          # W - w, in the sorted weights' place (they are not needed again)
    out = []
    for lo, hi in ((0.0, 0.25), (0.25, 0.5), (0.5, 0.75), (0.75, 1.0)):
        part = np.minimum(W, hi)                # each sample's weight inside [lo, hi), built in place
        part -= np.maximum(Wprev, lo)
        np.clip(part, 0.0, None, out=part)
        out.append(float(np.dot(part, v) / part.sum()))
    return out


def population_block(m, w, c, a, mpc, at_floor, mean_defined):
    return {
        "m": distribution_block(m, w, mean_defined),
        "a": distribution_block(a, w, mean_defined),
        "c": distribution_block(c, w, mean_defined),
        "mean_c": {"status": "value", "value": float(np.dot(w, c))} if mean_defined else {"status": "undefined"},
        "mass_at_constraint": float(w[at_floor].sum()),
        "fraction_a_nonpositive": float(w[a <= 1e-12].sum()),
        "mean_mpc": float(np.dot(w, mpc)),
        "mpc_by_a_quartile": by_a_quartile(a, w, mpc),
    }


def income_block(pop, mean_defined):
    if pop is None:
        return {"status": "undefined"}
    _c, a, mpc, at_floor = pop.derived()
    return {"status": "value",
            "m": distribution_block(pop.m, pop.w, mean_defined), "a": distribution_block(a, pop.w, mean_defined),
            "mass_at_constraint": float(pop.w[at_floor].sum()),
            "mean_a": {"status": "value", "value": float(np.dot(pop.w, a))} if mean_defined else {"status": "undefined"},
            "mean_mpc": float(np.dot(pop.w, mpc))}


def welfare_blocks(w, v, u, up, a, at_floor, dom):
    """W = E[v(m)] and F = E[u(c)] in one block; M = E[u'(c)], by quartile of a and at the constraint, in the other."""
    welfare = ({"status": "value", "mean_value": float(np.dot(w, v)), "mean_felicity": float(np.dot(w, u))}
               if dom["welfare"] else {"status": "undefined"})
    quart = by_a_quartile(a, w, up)
    at_c = float(np.dot(w[at_floor], up[at_floor]) / w[at_floor].sum()) if at_floor.any() else None
    if dom["marginal_welfare"]:
        marginal = {"status": "value", "mean": float(np.dot(w, up)), "by_a_quartile": quart, "at_constraint": at_c,
                    "gl": gl_ordinates(up, w)}
        if at_c is None:
            marginal["undefined"] = ["at_constraint"]          # no mass at the constraint: no conditional mean there
    else:
        # the mean and the bottom quartile's mean diverge with the lower tail; the upper quartiles stay defined (results.md)
        marginal = {"status": "undefined", "by_a_quartile": [None] + quart[1:], "at_constraint": None,
                    "undefined": ["mean", "by_a_quartile[0]", "at_constraint"]}
    return welfare, marginal


# ------------------------------------------------------------------------------------------------ the rule's special points
def expected_marginal_value(cf, a, P, PSI, XI, R, G, rho):
    """E[(G psi)^(-rho) u'(c(m'))] at end-of-period assets a (scalar or array), under a discrete joint law."""
    a = np.atleast_1d(np.asarray(a, float))
    m_next = R * a[:, None] / (G * PSI[None, :]) + XI[None, :]
    c_next = np.asarray(cf(m_next.ravel()), float).reshape(m_next.shape)
    return np.dot((G * PSI) ** (-rho) * c_next ** (-rho), P)


def kink_point(cf, member, beta, a_lo, P, PSI, XI):
    """m*: the largest m at which the artificial constraint binds in HARK's rule, i.e. where the rule leaves the 45-degree line
    c = m - a_lo (its lower envelope with the unconstrained rule), with the rule's slope on each side. The model's own kink under
    the solver's expectation, u'(m* - a_lo) = beta L R E[(G psi)^-rho u'(c(m'(a_lo)))], brackets the search (HARK's first
    endogenous gridpoint sits at a = aXtraMin above it)."""
    rhs = beta * member.L * member.R * expected_marginal_value(cf, a_lo, P, PSI, XI, member.R, member.G, member.rho)[0]
    m_euler = a_lo + inverse_marginal_utility(rhs, member.rho)
    gap = lambda m: float(cf(m)) - (m - a_lo) + 1e-12     # > 0 on the constrained segment, < 0 once the rule bends away
    lo, hi = max(a_lo + 1e-9, m_euler - 1e-3), m_euler + 1e-3
    m_k = brentq(gap, lo, hi, xtol=1e-14) if gap(lo) > 0 > gap(hi) else m_euler
    d = 1e-6 * max(1.0, abs(m_k))
    der = lambda m: float(cf.derivative(np.array([m]))[0])
    return {"status": "value", "m": float(m_k), "slope_below": der(m_k - d), "slope_above": der(m_k + d)}, m_euler


def special_point(cf, f, lo, hi):
    try:
        m = brentq(f, lo, hi, xtol=1e-12)
    except ValueError:
        return {"status": "undefined"}
    return {"status": "value", "m": float(m), "c": float(cf(m)), "mpc": float(cf.derivative(np.array([m]))[0])}


# ------------------------------------------------------------------------------------------------ the diagnostics
def exact_expected_marginal_value(cf, member, a, m_kink, n=DIAG_NODES, m_floor=-math.inf):
    """E[(G psi)^(-rho) u'(c(m'))] at one a by the diagnostics' expectation: Gauss-Legendre in the log of each lognormal law,
    the transitory law's support split where m' crosses the rule's kink (the integrand's own kink), for each permanent node;
    the unemployment state exact. m' is kept at or above m_floor, the rule's lower limit: under natural the stated laws'
    worst draw from the limit lands on it up to rounding, and HARK's rule is not defined below it."""
    R, G, rho = member.R, member.G, member.rho
    scale = employed_scale(member)
    p_psi, psi = law_quadrature(member.psi, n)
    total = 0.0
    for pp, ps in zip(p_psi, psi):
        base = R * a / (G * ps)
        split = (m_kink - base) / scale if m_kink is not None else None
        p_th, th = law_quadrature(member.theta, n, split_at=split)
        emp = float(np.dot(p_th, np.asarray(cf(np.maximum(base + scale * th, m_floor)), float) ** (-rho)))
        if member.wp > 0:
            emp = member.wp * float(cf(max(base + member.xi_u, m_floor))) ** (-rho) + (1.0 - member.wp) * emp
        total += pp * (G * ps) ** (-rho) * emp
    return total


def euler_residuals(cf, member, beta, a_lo, points, m_kink, n=DIAG_NODES, m_floor=-math.inf):
    """r(m) = min(c_hat - c, m - a_lo - c)/c at the comparison points, c_hat from the diagnostics' expectation (results.md)."""
    out = []
    for m in points:
        c = float(cf(m))
        if c <= 0.0:
            raise ValueError(f"no Euler residual at m = {m}: the rule consumes nothing there (fix the request file)")
        E = exact_expected_marginal_value(cf, member, m - c, m_kink, n=n, m_floor=m_floor)
        c_hat = inverse_marginal_utility(beta * member.L * member.R * E, member.rho)
        out.append(float(min(c_hat - c, m - a_lo - c) / c))
    return out, float(max(abs(r) for r in out))


def euler_residuals_effective(cf, member, beta, a_lo, points, P, PSI, XI):
    """The same residual under the toolkit's own representation of the laws (the solver's nodes): the solver's own error, with
    the discretization's taken out."""
    out = []
    for m in points:
        c = float(cf(m))
        E = expected_marginal_value(cf, m - c, P, PSI, XI, member.R, member.G, member.rho)[0]
        c_hat = inverse_marginal_utility(beta * member.L * member.R * E, member.rho)
        out.append(float(min(c_hat - c, m - a_lo - c) / c))
    return out, float(max(abs(r) for r in out))


# ------------------------------------------------------------------------------------------------ the request file
def round3(x):
    return float(f"{x:.3g}")


def m_infimum(member):
    """The infimum of m over the model's support: the worst income plus the return on the constraint's assets at the permanent
    shock that makes it smallest (a property of the member, not of any toolkit's nodes)."""
    xi_inf = employed_scale(member) * getattr(member.theta, "infimum", 1.0)
    if member.wp > 0:
        xi_inf = min(xi_inf, member.xi_u)
    a_lo = float(member.a_art)
    ends = [p for p in (getattr(member.psi, "infimum", 1.0), getattr(member.psi, "supremum", 1.0)) if 0 < p < math.inf]
    return xi_inf + (min(member.R * a_lo / (member.G * p) for p in ends) if ends else 0.0)


def generate_request(member, report, nodes, Pt, PSIt, XIt, nb, a_lo, natural, path):
    """The comparison points from a level-1 solution: the stationary quantiles of m at the request probabilities, the lower end
    of m, and 1.5, 2, 4 and 8 times the 99th percentile, to three significant figures (results.md). The lower end is the
    model's own infimum of m (toolkit-independent); where the rule consumes nothing there (a natural constraint met by the
    zero-income event: no Euler residual exists at c = 0) the 0.001 quantile stands in."""
    lev = LEVELS[1]
    R, G, L = member.R, member.G, member.L
    m_inf = m_infimum(member)
    types = []
    for t in member.types:
        cf = solve_type(member, t["beta"], nodes, lev).solution[0].cFunc
        pop = Population(cf, make_agrid(lev["dist_points"], lev["dist_top"], a_lo, natural), Pt, PSIt, XIt, R, G, a_lo, L,
                         nb[0], nb[1], False)
        q = quantiles(pop.m, pop.w)
        low = m_inf
        if not (math.isfinite(low) and low > a_lo and float(cf(low)) > 0.0):
            ms, ws = _sorted(pop.m, pop.w)
            low = float(ms[min(int(np.searchsorted(np.cumsum(ws), 0.001, side="left")), len(ms) - 1)])
        pts = {round3(q[u]) for u in REQUEST_U} | {round3(low)} | {round3(q["0.99"] * k) for k in ABOVE_99}
        pts = sorted(p for p in pts if float(cf(p)) > 0.0)
        types.append({"beta": t["beta"], "points": pts})
    request = {"family": "bst/1", "parameter_file_sha256": report["hash"],
               "rule": "stationary quantiles of m at u = 0.01, 0.05, 0.1, 0.2, ..., 0.9, 0.95, 0.99 from a level-1 solution; "
                       "the lower end of m (the model's infimum of m, or the 0.001 quantile where consumption is zero at the "
                       "infimum); and 1.5, 2, 4 and 8 times the 99th percentile; three significant figures",
               "types": types}
    dump_strict_yaml(request, path)
    return request


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


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("member")
    ap.add_argument("--schemas", default=str(SCHEMAS), help="the schemas directory (default: the one this adapter is in)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--level", default="1")
    ap.add_argument("--request", default=None)
    ap.add_argument("--nodes", type=int, default=None, help="nodes per shock in the household's expectation (default: the level's)")
    args = ap.parse_args(argv)
    os.makedirs(args.out, exist_ok=True)
    level = NAMED_LEVELS.get(args.level) or int(args.level)
    lev = dict(LEVELS[level])
    if args.nodes:
        lev["nodes"] = args.nodes
    bst1, canonical = load_checker(args.schemas)
    global QUANTILE_PROBS
    QUANTILE_PROBS = schema_quantile_probabilities(args.schemas)
    member = bst1.load_member(pathlib.Path(args.member))
    report = member.report()
    rho, R, G, L = member.rho, member.R, member.G, member.L
    nodes, P, PSI, XI, nb = shocks(member, lev["nodes"])
    nodes_t, Pt, PSIt, XIt, nbt = shocks(member, lev["transition_nodes"])
    # the effective member: the household's law is the solver's nodes; the population's forward transition uses the same bins
    # at levels 1-3 and a coarser set at level 4, reported then in the optional `population` block, which decides the
    # conditions on the stationary population (the GIC-Szeidl, the GIC-Harmenberg, the welfare conditions, the tail exponents)
    p_psi, psi_nodes, p_th, th_nodes = nodes
    same = lev["transition_nodes"] == lev["nodes"]
    representation = (f"equiprobable bins of each law, {lev['nodes']} per shock in the household's expectation"
                      + (" and in the population's forward transition" if same else "")
                      + ", each node the bin's exact conditional mean; the unemployment event a state of a chain with "
                        "identical rows; the newborn draws the employed branch; the natural limit from the nodes' lowest "
                        "values, as HARK computes it")
    population = None
    p_psi_pop, psi_pop = p_psi, psi_nodes
    if not same:
        p_psi_pop, psi_pop, p_th_pop, th_pop = nodes_t
        population = (p_psi_pop, psi_pop, p_th_pop, th_pop,
                      f"the same construction at {lev['transition_nodes']} per shock in the population's forward transition "
                      f"(the household solves on {lev['nodes']})")
    eff = effective_member_block(bst1, member, p_psi, psi_nodes, p_th, th_nodes, representation, population)
    E_eff = eff["expectations"]
    E_pop = population_expectations(eff)
    a_lo = float(eff["derived"]["constraint_in_force"])      # the constraint in force in what is solved (HARK's mNrmMin)
    a_nat_eff = eff["derived"]["natural_limit"]
    binds = a_nat_eff is None or a_lo > a_nat_eff + bst1.TOLERANCE   # the artificial constraint binds: a kink, mass at a_lo
    natural = not binds                                      # the constraint never binds: no node at a_lo (see make_agrid)
    import HARK
    commit = installed_hark_commit()

    # ---- the request file (the comparison points)
    if args.request:
        request_path = args.request
        request = canonical.load_strict(open(request_path, encoding="utf-8").read())
    else:
        request_path = os.path.join(args.out, "request.yaml")
        nodes1, P1, PSI1, XI1, nb1 = shocks(member, LEVELS[1]["nodes"])
        request = generate_request(member, report, nodes1, P1, PSI1, XI1, nb1, a_lo, natural, request_path)
    points_by_beta = {float(t["beta"]): [float(x) for x in t["points"]] for t in request["types"]}

    # ---- the method and settings files (numerics.md), on the parts the stage file's targets name (model.md, "Method targets")
    methods_path = os.path.join(args.out, "methods.yaml")
    settings_path = os.path.join(args.out, "settings.yaml")
    dump_strict_yaml({"methods": METHODS}, methods_path)
    dump_strict_yaml({"settings": {
        "level": level, "nodes_per_shock": lev["nodes"], "transition_nodes_per_shock": lev["transition_nodes"],
        "solve_grid_points": lev["solve_points"], "solve_grid_min": 1e-6, "solve_grid_max": lev["solve_top"],
        "solve_grid_nesting": lev["nest"], "solve_tolerance": lev["tol"],
        "distribution_grid_points": lev["dist_points"], "distribution_grid_top": lev["dist_top"],
        "diagnostics_nodes_per_piece": DIAG_NODES}}, settings_path)

    # ---- each type
    types_out, per_type, own_domains = [], [], []
    status_keys = ("kink", "buffer_stock_target", "pseudo_target", "income_measure", "welfare", "marginal_welfare",
                   "population_mean", "income_mean")
    for i, t in enumerate(member.types):
        beta, share = float(t["beta"]), float(t["share"])
        # the conditions and the statuses: the toolkit's own, on its effective member
        conds = own_conditions(bst1, member, beta, E_eff, E_pop, binds)
        dom = own_domain(bst1, member, beta, conds, E_eff, eff["derived"], p_psi_pop, psi_pop)
        stated = report["types"][i]["domain"]
        differs = [k for k in status_keys if bool(stated.get(k)) != bool(dom.get(k))]
        sol = solve_type(member, beta, nodes, lev).solution[0]
        cf, vf = sol.cFunc, sol.vFunc
        # HARK's constraint in force is the effective one. An artificial one is exact. Under natural HARK reaches the
        # laws' limit by iterating its recursion, which stops on the rule's convergence a little above the limit (4e-9
        # on the toy at level 1), so it is held below the population grid's first node, 1e-6 above.
        if member.natural:
            assert -1e-9 < float(sol.mNrmMin) - a_lo < 1e-6, (sol.mNrmMin, a_lo)
        else:
            assert abs(float(sol.mNrmMin) - a_lo) < 1e-9, (sol.mNrmMin, a_lo)
        m_floor = float(sol.mNrmMin)
        pts = points_by_beta[beta]
        agrid = make_agrid(lev["dist_points"], lev["dist_top"], a_lo, natural)
        pop = Population(cf, agrid, Pt, PSIt, XIt, R, G, a_lo, L, nbt[0], nbt[1], False)
        # the income measure exists when the toolkit's own verdicts say so; its survivors' share of mass is L G, and when
        # L G >= 1 the newborns' share vanishes and the measure is the eigenvector of the tilted transition (Harmenberg)
        LG = L * G
        inc = (Population(cf, agrid, Pt, PSIt, XIt, R, G, a_lo, min(LG, 1.0), nbt[0], nbt[1], True)
               if dom["income_measure"] else None)
        c, a, mpc, at_floor = pop.derived()      # the type's own statistics; only pop.m and pop.w outlive this iteration
        v = np.asarray(vf(pop.m), float)
        u = crra_u(c, rho)
        up = c ** (-rho)
        welfare, marginal = welfare_blocks(pop.w, v, u, up, a, at_floor, dom)
        kink, m_euler = kink_point(cf, member, beta, a_lo, P, PSI, XI) if dom["kink"] else ({"status": "undefined"}, None)
        m_lo = (kink["m"] if kink["status"] == "value" else a_lo) + 1e-6
        hi = lev["solve_top"]
        target = (special_point(cf, lambda x: R * (x - float(cf(x))) * E_eff["psi_inverse"] / G + 1.0 - x, m_lo, hi)
                  if dom["buffer_stock_target"] else {"status": "undefined"})
        pseudo = (special_point(cf, lambda x: (x - float(cf(x))) - (G / R) * (x - 1.0), m_lo, hi)
                  if dom["pseudo_target"] else {"status": "undefined"})
        m_dense = np.unique(np.concatenate([np.geomspace(max(float(pop.m.min()), 1e-6), hi, 400),
                                            [kink["m"]] if kink["status"] == "value" else []]))
        r, r_max = euler_residuals(cf, member, beta, a_lo, pts, kink.get("m"), m_floor=m_floor)
        r_fine, _ = euler_residuals(cf, member, beta, a_lo, pts, kink.get("m"), n=2 * DIAG_NODES, m_floor=m_floor)
        precision = float(max(abs(x - y) for x, y in zip(r, r_fine)))     # the diagnostic's own error: doubling its nodes
        r_eff, r_eff_max = euler_residuals_effective(cf, member, beta, a_lo, pts, P, PSI, XI)
        stationarity = {"population": pop.stationarity_residual(),
                        "income": inc.stationarity_residual() if inc is not None else None,
                        "method": "one forward step of the adapter's lottery transition on the reported distribution, same nodes"}
        types_out.append({
            "beta": beta, "share": share, "conditions": conds, "comparison_points": pts,
            "rule": {"c": [float(x) for x in np.asarray(cf(np.asarray(pts)), float)],
                     "mpc": [float(x) for x in np.asarray(cf.derivative(np.asarray(pts)), float)]},
            "exported_rule": {"m": [float(x) for x in m_dense], "c": [float(x) for x in np.asarray(cf(m_dense), float)],
                              "range": [float(m_dense[0]), float(m_dense[-1])]},
            "kink": kink, "target": target, "pseudo_target": pseudo,
            "population": population_block(pop.m, pop.w, c, a, mpc, at_floor, dom["population_mean"]),
            "income_measure": income_block(inc, dom["income_mean"]),
            "welfare": welfare, "marginal_welfare": marginal,
            "euler_residuals": {"r": r, "max_abs": r_max, "expectation_method": "hark:gauss-legendre-log-support-split-at-kink",
                                "expectation_precision": precision, "under_effective_laws": {"r": r_eff, "max_abs": r_eff_max}},
            "stationarity_residual": stationarity})
        per_type.append(dict(share=share, pop=pop, inc=inc, Ev=float(np.dot(pop.w, v)), Eu=float(np.dot(pop.w, u))))
        own_domains.append(dom)
        mean_a = float(np.dot(pop.w, a))
        del v, u, up, c, a, mpc, at_floor
        print(f"type beta {beta}: kink {kink.get('m')} (Euler {m_euler}), target {target.get('m')}, mean a {mean_a:.5f}, "
              f"W {welfare.get('mean_value')}, max|r| {r_max:.2e} (precision {precision:.1e}, own nodes {r_eff_max:.1e}), "
              f"stationarity {stationarity['population']:.1e}, arrivals {len(pop.m):,}"
              + (f"; own verdicts differ from the stated member's on {differs}" if differs else ""), flush=True)

    # ---- pooled by share (one stacked variable at a time; the means exactly from the types' own)
    pdom = {k: all(d[k] for d in own_domains) for k in own_domains[0] if not k.endswith("exponent")}
    shares = [d["share"] for d in per_type]
    pooled_welfare, pooled_marginal = pooled_welfare_blocks(per_type, shares, pdom, rho)
    results = {
        "family": "bst/1",
        "parameter_file_sha256": report["hash"],
        "effective_member": eff,
        "method_file_sha256": file_hash(canonical, methods_path),
        "settings_sha256": file_hash(canonical, settings_path),
        "request_file_sha256": file_hash(canonical, request_path),
        "toolkit": {"name": "HARK", "version": HARK.__version__, "driver": f"schemas/adapters/hark/adapter.py {ADAPTER_VERSION}",
                    **({"commit": commit} if commit else {})},
        "provenance": {"hardware": hardware(), "threads": blas_threads(),
                       "method_file": os.path.basename(methods_path),
                       "settings_file": os.path.basename(settings_path), "request_file": os.path.basename(request_path),
                       "parameter_file": os.path.basename(args.member),
                       "environment": numerical_environment(),
                       "solver": {"iteration": "HARK's MarkovConsumerType, infinite horizon, until the solution distance is below "
                                               "solve_tolerance",
                                  "chain": "two employment states with identical rows (1 - wp, wp): the nonpersistent chain; "
                                           "the two states' rules asserted equal",
                                  "kink": "where HARK's lower envelope of the unconstrained cubic rule and the 45-degree line "
                                          "leaves the line; HARK's first endogenous gridpoint sits at a = aXtraMin = 1e-6 above it",
                                  "shock_nodes": "the laws' equiprobable bins with exact conditional means, handed to HARK by "
                                                 "employment state; HARK's own lognormal construction is not used"}},
        "types": types_out,
        "pooled": {"population": pooled_population_block([d["pop"] for d in per_type], shares, pdom["population_mean"]),
                   "income_measure": pooled_income_block([d["inc"] for d in per_type], shares, pdom["income_mean"]),
                   "welfare": pooled_welfare, "marginal_welfare": pooled_marginal},
    }
    out_path = os.path.join(args.out, "results.json")
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=1, allow_nan=False)
    print(f"wrote {out_path} ({os.path.getsize(out_path) // 1024} KB)", flush=True)
    try:
        import jsonschema
    except ImportError:
        print("jsonschema not importable: not validated here", flush=True)
        return out_path
    schema = json.load(open(os.path.join(args.schemas, "bst-1", "results.schema.json"), encoding="utf-8"))
    jsonschema.Draft202012Validator(schema).validate(results)
    print("results.json validates against bst-1/results.schema.json", flush=True)
    return out_path


if __name__ == "__main__":
    main()
