"""The checker for a bst-markov_ui-and-agg/1 parameter file, for the STATED member: the employment chain, the constraint in
force by state, the conditions as dominant eigenvalues over the chain, the domain rules and the implications.

The statements follow bst-markov_ui-and-agg/conditions.md, in BST's notation: psi the permanent shock, theta the employed
draw, e the scale of employed income, xi_u and xi_x the incomes with and without benefits, L survival, G a group's growth,
P the normal regime's chain over the employment states J = (E, U_2, U_1, X), and P_u the switch for permanent income in a
quarter of unemployment. The stationary problem is the normal regime's, since normal is absorbing, so every condition is
on the normal chain. Everything is computed from the laws' closed-form moments, for one type of one group at a time; under
`continues` every condition reduces to bst/1's with the group's growth (bst1.py).
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import jsonschema
import numpy as np
from referencing import Registry, Resource
from scipy.optimize import brentq

from canonical import load_strict, model_hash
from laws import TOLERANCE, filled, law_from_mapping

SCHEMAS = Path(__file__).resolve().parent.parent
PARAMETER_SCHEMA = SCHEMAS / "bst-markov_ui-and-agg" / "parameters.schema.json"
SHOCK_LAW_SCHEMA = SCHEMAS / "shock-laws.schema.json"

STATES = ("E", "U_2", "U_1", "X")
SWITCHES = ("continues", "grows", "frozen")
EMPLOYED = 0
# The precision of a closed-form evaluation; a condition whose margin lies within it is undecided for the stated member.
STATED_PRECISION = 1e-12
CONDITION_NAMES = ["AIC", "RIC", "WRIC", "FHWC", "PF-FVAC", "FVAC", "GIC", "GIC-Mod", "GIC-Szeidl", "GIC-Harmenberg",
                   "GIC-Liv"]


class MarkovMemberError(ValueError):
    """The file is not a valid bst-markov_ui-and-agg/1 member; the message lists every problem found."""


def _validator():
    shock_uri = SHOCK_LAW_SCHEMA.as_uri()

    def absolute(node):
        if isinstance(node, dict):
            return {key: (shock_uri if key == "$ref" and value == "../shock-laws.schema.json" else absolute(value))
                    for key, value in node.items()}
        if isinstance(node, list):
            return [absolute(item) for item in node]
        return node

    registry = Registry().with_resource(shock_uri, Resource.from_contents(json.loads(SHOCK_LAW_SCHEMA.read_text())))
    return jsonschema.Draft202012Validator(absolute(json.loads(PARAMETER_SCHEMA.read_text())), registry=registry,
                                           format_checker=jsonschema.FormatChecker())


def validate(data) -> list[str]:
    """The parameter validator's complaints, as sentences with the path of each."""
    return [f"{'/'.join(str(p) for p in e.absolute_path) or '/'}: {e.message}"
            for e in sorted(_validator().iter_errors(data), key=lambda e: list(e.absolute_path))]


def verdict(margin: float) -> str:
    if abs(margin) <= STATED_PRECISION:
        return "undecided"
    return "holds" if margin > 0 else "fails"


def chain(sep: float, find: float) -> np.ndarray:
    """The employment chain of one regime, rows the previous state and columns this quarter's, as the stage file writes it:
    the employed lose their job with probability sep; the unemployed find one with probability find, and otherwise count
    down their two quarters of benefits, U_2 then U_1, before X, where they stay until they find one."""
    return np.array([[1.0 - sep, sep, 0.0, 0.0],
                     [find, 0.0, 1.0 - find, 0.0],
                     [find, 0.0, 0.0, 1.0 - find],
                     [find, 0.0, 0.0, 1.0 - find]])


def dominant_eigenvalue(M: np.ndarray) -> float:
    """The Perron root of a nonnegative matrix: its spectral radius, an eigenvalue of its own."""
    return float(max(abs(np.linalg.eigvals(M))))


def stationary(P: np.ndarray) -> np.ndarray:
    """The chain's stationary distribution pi, the left eigenvector of P for the eigenvalue one."""
    n = len(P)
    A = np.vstack([P.T - np.eye(n), np.ones(n)])
    b = np.concatenate([np.zeros(n), [1.0]])
    return np.linalg.lstsq(A, b, rcond=None)[0]


class Group:
    """One group's chain and the laws of next quarter's growth, permanent shock and income in each employment state."""

    def __init__(self, member: "MarkovMember", data: dict):
        self.member = member
        self.name = data["name"]
        self.share = data["share"]
        self.G = data["growth"]
        self.sep = data["job_loss"]
        self.newborn = data["newborn_income"]
        self.types = data["types"]
        self.P = chain(self.sep["normal"], member.find["normal"])
        unemployed_growth = {"continues": self.G, "grows": self.G, "frozen": 1.0}[member.P_u]
        self.growth = np.array([self.G] + [unemployed_growth] * 3)
        # psi is drawn when employed, and in a quarter of unemployment only under continues; otherwise it is one
        self.psi_drawn = np.array([True] + [member.P_u == "continues"] * 3)

    # The laws in each state j as next quarter's state: E[(G(j) psi)^k | j], E[log psi | j], E[psi log psi | j].
    def growth_moment(self, k: float) -> np.ndarray:
        psi = self.member.psi
        return np.array([self.growth[j] ** k * (psi.moment(k) if self.psi_drawn[j] else 1.0) for j in range(4)])

    def log_psi(self) -> np.ndarray:
        return np.array([self.member.psi.mean_log if d else 0.0 for d in self.psi_drawn])

    def psi_log_psi(self) -> np.ndarray:
        return np.array([self.member.psi.mean_x_log_x if d else 0.0 for d in self.psi_drawn])

    def M(self, f: np.ndarray) -> np.ndarray:
        """M_f[j, j'] = P[j, j'] f(j'), with f the conditional expectation of a function of next quarter's state and shock."""
        return self.P * np.asarray(f)[None, :]

    # The lowest values by state, and their masses.
    def psi_min(self) -> np.ndarray:
        return np.array([self.member.psi.infimum if d else 1.0 for d in self.psi_drawn])

    def psi_min_mass(self) -> np.ndarray:
        return np.array([self.member.psi.mass_at_infimum if d else 1.0 for d in self.psi_drawn])

    def xi_min(self) -> np.ndarray:
        m = self.member
        return np.array([m.e * m.theta.infimum, m.xi_u, m.xi_u, m.xi_x])

    def xi_min_mass(self) -> np.ndarray:
        return np.array([self.member.theta.mass_at_infimum, 1.0, 1.0, 1.0])

    def limits(self, a_art: float | None) -> np.ndarray:
        """The constraint in force by state, the fixed point of
            a_min(j) = max(a_Art, max over j' with P[j, j'] > 0 of (G(j') psi_min(j')/R)(a_min(j') - xi_min(j'))),
        with the artificial limit inside the recursion (conditions.md, "The constraint in force, by state"); with
        a_art None it is the natural limits a_Nat(j). Iterated from zero, each bracket being nonpositive; -inf in every
        state when the recursion has no finite fixed point."""
        mult = self.growth * self.psi_min() / self.member.R
        floor = self.xi_min()
        reach = self.P > 0
        a = np.zeros(4)
        lower = -math.inf if a_art is None else a_art
        for _ in range(1_000_000):
            terms = mult * (a - floor)
            new = np.array([max(lower, max(terms[reach[j]])) for j in range(4)])
            if np.min(new) < -1e12:
                return np.full(4, -math.inf)
            if np.max(np.abs(new - a)) <= 1e-15 * max(1.0, np.max(np.abs(new))):
                return new
            a = new
        raise RuntimeError("the constraint's recursion did not converge")

    def worst_income_probability(self) -> np.ndarray:
        """p_worst(j): the probability, from j, of reaching next quarter a state whose income floor xi_min psi_min is the
        worst reachable one and of drawing that floor there; zero unless the floor is an atom of both laws there."""
        floor = self.xi_min() * self.psi_min()
        mass = self.xi_min_mass() * self.psi_min_mass()
        out = np.zeros(4)
        for j in range(4):
            reach = self.P[j] > 0
            worst = np.min(floor[reach])
            out[j] = float(np.sum(self.P[j][reach & np.isclose(floor, worst, rtol=0, atol=TOLERANCE)]
                                  * mass[reach & np.isclose(floor, worst, rtol=0, atol=TOLERANCE)]))
        return out

    def employment_marginal(self) -> np.ndarray:
        """mu = (1 - L) e_E (I - L P)^(-1): the stationary population's employment shares, newborns entering E; pi when
        L = 1."""
        L = self.member.L
        if L >= 1.0:
            return stationary(self.P)
        e_E = np.eye(4)[EMPLOYED]
        return (1.0 - L) * np.linalg.solve((np.eye(4) - L * self.P).T, e_E)


class MarkovMember:
    """A bst-markov_ui-and-agg/1 member, parsed from its parameter file's mapping."""

    def __init__(self, data: dict):
        self.data = data
        problems = validate(data)
        if problems:
            raise MarkovMemberError("; ".join(problems))
        self.hash = model_hash(filled(data))  # over the filled form, as bst/1's: omitted bounds written in
        self.rho = data["crra"]
        self.L = data["survival"]
        self.R = data["return"]
        self.splurge = data["splurge"]
        self.a_art = data["borrowing_constraint"]
        self.natural = self.a_art == "natural"   # the file's word, before it resolves to the lowest a_Nat(j)
        self.psi = law_from_mapping(data["shocks"]["permanent_shock"])
        self.theta = law_from_mapping(data["shocks"]["employed_shock"])
        self.p_exit = data["regimes"]["recession"]["exit_hazard"]
        employment = data["employment"]
        self.benefit_quarters = employment["benefit_quarters"]
        self.find = employment["job_finding"]
        self.e = employment["income_employed"]
        self.xi_u = employment["income_with_benefits"]
        self.xi_x = employment["income_without_benefits"]
        self.P_u = employment["unemployed_permanent_income"]
        self.groups = [Group(self, g) for g in data["groups"]]
        problems = self._check()
        if problems:
            raise MarkovMemberError("; ".join(problems))

    def _check(self) -> list[str]:
        """The validity conditions of conditions.md that the parameter validator cannot state."""
        problems = []
        for name, law in (("permanent_shock", self.psi), ("employed_shock", self.theta)):
            problems += [f"shocks/{name}: {p}" for p in law.check()]
        if self.benefit_quarters != 2:
            problems.append("employment/benefit_quarters: only 2 has a stage file")
        if abs(sum(g.share for g in self.groups) - 1.0) > TOLERANCE:
            problems.append("groups: the shares do not sum to one")
        for g in self.groups:
            betas = [t["beta"] for t in g.types]
            if any(b2 <= b1 for b1, b2 in zip(betas, betas[1:])):
                problems.append(f"groups/{g.name}/types: beta must increase, with no repeat")
            if abs(sum(t["share"] for t in g.types) - 1.0) > TOLERANCE:
                problems.append(f"groups/{g.name}/types: the shares do not sum to one")
        if problems:
            return problems
        lowest = min(float(np.min(g.limits(None))) for g in self.groups)
        if self.natural:
            if math.isinf(lowest):
                problems.append("borrowing_constraint: 'natural' names no finite constraint")
        elif lowest > -math.inf and self.a_art < lowest - TOLERANCE:
            problems.append(f"borrowing_constraint {self.a_art!r} is below the lowest natural limit {lowest!r}; a looser "
                            "artificial limit binds in no state, so write the natural one or 'natural'")
        for g in self.groups:
            for t in g.types:
                c = {x["name"]: x for x in self.factors(g, t["beta"])}
                if not c["FVAC"]["holds"]:
                    problems.append(f"groups/{g.name}: the FVAC fails for beta {t['beta']!r}")
                if not (c["RIC"]["holds"] or all(w["holds"] for w in c["WRIC"]["by_state"])):
                    problems.append(f"groups/{g.name}: neither the RIC nor the WRIC holds for beta {t['beta']!r}")
        return problems

    def a_art_value(self) -> float | None:
        """The artificial limit in the recursion: none for natural."""
        return None if self.natural else float(self.a_art)

    def factors(self, g: Group, beta: float) -> list[dict]:
        """The conditions of conditions.md's table for one type of group g, from the closed-form moments; a by-state
        condition carries one entry per state of J. GIC-Harmenberg's chain for L = 1 is stated in words only, so it is
        not computed."""
        rho, L, R = self.rho, self.L, self.R
        thorn = (R * beta * L) ** (1 / rho)
        thorn_bar = min(thorn, R)               # R (1 - kappa_min)
        beta_ring = beta * L

        def factor(name, value, bound=1.0, governs=""):
            margin = bound - value
            return {"name": name, "factor": float(value), "bound": float(bound), "holds": bool(value < bound),
                    "margin": float(margin), "verdict": verdict(margin), "governs": governs}

        def by_state(name, values, governs):
            entries = [dict(factor(name, v), state=s) for s, v in zip(STATES, values)]
            return {"name": name, "by_state": entries, "holds": all(x["holds"] for x in entries), "governs": governs}

        p_worst = g.worst_income_probability()
        Gpsi = g.growth_moment(1.0)                                  # E[G(j') psi' | j'], G(j') since E[psi] = 1
        inv = g.growth_moment(-1.0)                                  # E[1/(G(j') psi') | j']
        pi = stationary(g.P)
        szeidl_rhs = float(np.dot(pi, np.log(g.growth) + g.log_psi()))
        return [
            factor("AIC", thorn, governs="consumption growth below one as m grows"),
            factor("RIC", thorn / R, governs="the limiting MPC is positive"),
            by_state("WRIC", p_worst ** (1 / rho) * thorn / R, "existence in place of the RIC"),
            factor("FHWC", dominant_eigenvalue(g.M(Gpsi / R)), governs="finite human wealth"),
            factor("PF-FVAC", dominant_eigenvalue(g.M(beta_ring * g.growth ** (1 - rho))),
                   governs="finite perfect-foresight value of autarky"),
            factor("FVAC", dominant_eigenvalue(g.M(beta_ring * g.growth_moment(1 - rho))),
                   governs="finite value of autarky"),
            by_state("GIC", thorn_bar / (g.P @ Gpsi), "the pseudo-target exists in that state"),
            by_state("GIC-Mod", thorn_bar * (g.P @ inv), "the buffer stock target exists in that state"),
            factor("GIC-Szeidl", math.log(thorn_bar), szeidl_rhs, governs="with L = 1, the stationary population exists"),
            {"name": "GIC-Harmenberg", "factor": None, "bound": None, "holds": None, "verdict": "not computed",
             "governs": "with L = 1, the income-weighted stationary population exists; its chain is stated in words only"},
            factor("GIC-Liv", L * dominant_eigenvalue(g.M(thorn_bar / g.growth)),
                   governs="aggregate balanced growth with estate destruction"),
        ]

    def _root(self, phi, start: float = 0.0) -> float | None:
        """The smallest z > start with phi(z) = 1, given phi increasing through one, or None when phi stays below one."""
        log_phi = lambda z: math.log(phi(z))   # noqa: E731
        z = start if start > 0 else 1e-6
        if log_phi(z) >= 0:
            return z if start > 0 else None
        step = 1e-6
        while log_phi(z + step) < 0:
            step *= 2
            if z + step > 1e6:
                return None
        return brentq(log_phi, z, z + step, xtol=1e-12)

    def implications(self, g: Group, beta: float) -> dict:
        """The domain rules' roots and the implications of conditions.md for one type of group g."""
        L, R, rho = self.L, self.R, self.rho
        thorn_bar = min((R * beta * L) ** (1 / rho), R)
        limits = g.limits(self.a_art_value())
        natural = g.limits(None)
        # the moments' roots: L lambda(M_f) = 1, f = (thorn_bar/(G psi))^eps for the population measure's moments, and
        # f = (G psi)^eps for the levels of permanent income
        pop = self._root(lambda z: L * dominant_eigenvalue(g.M(thorn_bar ** z * g.growth_moment(-z)))) if L < 1 else None
        levels = self._root(lambda z: L * dominant_eigenvalue(g.M(g.growth_moment(z)))) if L < 1 else None
        income_measure = L * dominant_eigenvalue(g.M(g.growth_moment(1.0)))
        kink = [bool(not self.natural and limits[j] == self.a_art_value()
                     and self.a_art_value() > max((g.growth * g.psi_min() / R * (limits - g.xi_min()))[g.P[j] > 0]) + TOLERANCE)
                for j in range(4)]
        return {
            "limiting_mpc": max(1 - thorn_bar / R, 0.0),
            "constraint_in_force": dict(zip(STATES, map(float, limits))),
            "natural_limits": dict(zip(STATES, map(float, natural))),
            "worst_income": dict(zip(STATES, map(float, g.xi_min() * g.psi_min()))),
            "worst_income_probability": dict(zip(STATES, map(float, g.worst_income_probability()))),
            "newborn_min_resources": self.e * self.theta.infimum,
            "employment_marginal": dict(zip(STATES, map(float, g.employment_marginal()))),
            "population_tail_exponent": pop,
            "income_measure_factor": float(income_measure),
            "income_measure_exists": bool(income_measure < 1) if L < 1 else None,
            "levels_tail_exponent": levels,
            "kink": dict(zip(STATES, kink)),
        }

    def report(self) -> dict:
        return {"family": "bst-markov_ui-and-agg/1",
                "groups": [{"name": g.name, "share": g.share,
                            "chain": {"normal": g.P.tolist(), "recession": chain(g.sep["recession"], self.find["recession"]).tolist()},
                            "types": [{"beta": t["beta"], "share": t["share"], "conditions": self.factors(g, t["beta"]),
                                       "implications": self.implications(g, t["beta"])} for t in g.types]}
                           for g in self.groups]}


def load_member(path: Path) -> MarkovMember:
    return MarkovMember(load_strict(Path(path).read_text()))
