"""The checker for a bst/1 parameter file: validation, the laws' moments, the conditions, the domain rules, the implications.

The statements follow bst-1/conditions.md, in BST's notation: psi the permanent shock, xi the transitory shock, theta the
employed draw, wp the unemployment probability, xi_min the unemployment income, L survival, G growth, a_Art and a_Nat the
artificial and natural borrowing constraints. Everything is computed exactly from the laws' closed-form moments; nothing
here discretizes a shock.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import jsonschema
from referencing import Registry, Resource
from scipy.optimize import brentq

from canonical import load_strict, model_hash
from laws import FLOOR_ATOM, FLOOR_DENSITY, FLOOR_THIN, TOLERANCE, law_from_mapping

SCHEMAS = Path(__file__).resolve().parent.parent
PARAMETER_SCHEMA = SCHEMAS / "bst-1" / "parameters.schema.json"
SHOCK_LAW_SCHEMA = SCHEMAS / "shock-laws.schema.json"


class MemberError(ValueError):
    """The file is not a valid bst/1 member; the message lists every problem found."""


def _validator():
    shock_uri = SHOCK_LAW_SCHEMA.as_uri()
    parameter_schema = json.loads(PARAMETER_SCHEMA.read_text())
    shock_schema = json.loads(SHOCK_LAW_SCHEMA.read_text())

    def absolute(node):
        if isinstance(node, dict):
            return {key: (shock_uri if key == "$ref" and value == "../shock-laws.schema.json" else absolute(value))
                    for key, value in node.items()}
        if isinstance(node, list):
            return [absolute(item) for item in node]
        return node

    registry = Registry().with_resource(shock_uri, Resource.from_contents(shock_schema))
    return jsonschema.Draft202012Validator(absolute(parameter_schema), registry=registry,
                                           format_checker=jsonschema.FormatChecker())


def validate(data) -> list[str]:
    """The validator's complaints, as sentences with the path of each."""
    problems = []
    for error in sorted(_validator().iter_errors(data), key=lambda e: list(e.absolute_path)):
        path = "/".join(str(p) for p in error.absolute_path) or "/"
        problems.append(f"{path}: {error.message}")
    return problems


class Member:
    """A valid bst/1 member with its laws, the moments of its shocks, and its conditions."""

    def __init__(self, data: dict):
        self.data = data
        problems = validate(data)
        if problems:
            raise MemberError("; ".join(problems))
        self.hash = model_hash(data)
        self.rho = data["crra"]
        self.types = data["types"]
        self.L = data["survival"]
        self.R = data["return"]
        income = data["income"]
        self.G = income["growth"]
        self.wp = income["unemployment"]["prob"]
        self.xi_min = income["unemployment"]["income"]
        self.psi = law_from_mapping(income["permanent_shock"])
        self.theta = law_from_mapping(income["employed_shock"])
        # The employed draw's scale, which keeps the mean of the transitory shock at one; it needs wp * xi_min < 1.
        self.employed_scale = None
        if self.wp * self.xi_min < 1:
            self.employed_scale = (1 - self.wp * self.xi_min) / (1 - self.wp)
        self.a_art = data["borrowing_constraint"]
        problems = self._check()
        if problems:
            raise MemberError("; ".join(problems))

    def _check(self) -> list[str]:
        problems = []
        shares = sum(t["share"] for t in self.types)
        if abs(shares - 1) > TOLERANCE:
            problems.append(f"types: shares sum to {shares!r}, not 1")
        betas = [t["beta"] for t in self.types]
        if any(b <= a for a, b in zip(betas, betas[1:])):
            problems.append("types: betas must be strictly increasing, so that the file has one written form")
        if self.wp == 0 and self.xi_min != 0:
            problems.append("income/unemployment: with prob 0, income must be 0")
        if self.employed_scale is None:
            problems.append("income/unemployment: prob times income must be below 1, or the employed earn nothing")
        for name, law in (("permanent_shock", self.psi), ("employed_shock", self.theta)):
            problems += [f"income/{name}: {p}" for p in law.check()]
        if problems:
            return problems
        a_nat = self.natural_borrowing_constraint()
        if self.a_art == "natural":
            if math.isinf(a_nat):
                problems.append("borrowing_constraint: 'natural' names no finite constraint, since kappa >= 1")
            else:
                self.a_art = a_nat
        elif a_nat > -math.inf and self.a_art < a_nat - TOLERANCE:
            problems.append(f"borrowing_constraint {self.a_art!r} is below the natural constraint {a_nat!r}; "
                            "a looser artificial constraint never binds, so write the natural one or 'natural'")
        return problems

    # The transitory shock xi: xi_min with probability wp, else the scaled employed draw.

    def xi_infimum(self) -> float:
        employed_low = self.employed_scale * self.theta.infimum
        return min(self.xi_min, employed_low) if self.wp > 0 else employed_low

    def xi_mass_at_infimum(self) -> float:
        low = self.xi_infimum()
        employed_low = self.employed_scale * self.theta.infimum
        mass = 0.0
        if self.wp > 0 and self.xi_min == low:
            mass += self.wp
        if employed_low == low:
            mass += (1 - self.wp) * self.theta.mass_at_infimum
        return mass

    def worst_income_probability(self) -> float:
        """p_min, the probability that income takes its lowest value; BST's wp when the unemployment event pays nothing."""
        if self.wp > 0 and self.xi_min == 0:
            return self.wp
        return self.xi_mass_at_infimum() * self.psi.mass_at_infimum

    def natural_borrowing_constraint(self) -> float:
        """a_Nat, the lowest assets from which the worst income still allows positive consumption; -inf when none."""
        kappa = self.psi.infimum * self.G / self.R
        if kappa >= 1:
            return -math.inf
        return -self.xi_infimum() * kappa / (1 - kappa) + 0.0  # + 0.0 turns a negative zero into zero

    def newborn_min_resources(self) -> float:
        """The lowest m a newborn can have: born employed, with no assets."""
        return self.employed_scale * self.theta.infimum

    def xi_floor_kind(self) -> str:
        """How the transitory shock behaves at its lowest value: the unemployment atom, or the employed draw's floor."""
        employed_low = self.employed_scale * self.theta.infimum
        if self.wp > 0 and self.xi_min <= employed_low:
            return FLOOR_ATOM
        return self.theta.floor_kind

    def lower_tail_moment(self, q: float, thorn: float) -> dict:
        """Whether E[(m - m_min)^(-q)] under the stationary population is finite, and why.

        With a binding artificial constraint the rule keeps consumption above a positive floor. Otherwise the mass near the
        natural constraint comes from the worst income: an atom there gives runs, each continuing with probability
        p_min * L and shrinking resources above the floor by p_min^(1/rho) thorn/(G psi), so the moment is finite exactly
        when p_min^(1 - q/rho) L (G/thorn)^q E[psi^q] < 1; a positive density at the floor in n of the two shocks gives a
        one-step landing law of order (distance)^n, and the stationary tail's exponent is max(n, rho): for rho < n the
        constraint binds near the floor and the tail is the landing law's, for rho > n the household saves a vanishing
        amount there and the tail steepens to rho, so the moment is finite exactly when q < max(n, rho); a density that
        vanishes faster than any power (a lognormal at zero) leaves every moment finite. Derived 2026-10-18 with the
        BufferStockTheory session, which checked the atom case and the one-density regimes numerically.
        """
        a_nat = self.natural_borrowing_constraint()
        if math.isinf(a_nat) or self.a_art > a_nat + TOLERANCE:
            return {"finite": True, "factor": None, "case": "the artificial constraint binds"}
        if q <= 0:
            return {"finite": True, "factor": None, "case": "no negative moment needed"}
        p_min = self.worst_income_probability()
        if p_min > 0:
            factor = p_min ** (1 - q / self.rho) * self.L * (self.G / thorn) ** q * self.psi.moment(q)
            return {"finite": factor < 1, "factor": factor, "case": "an atom at the worst income"}
        kinds = [self.psi.floor_kind, self.xi_floor_kind()]
        if FLOOR_THIN in kinds:
            return {"finite": True, "factor": None, "case": "a thin density at the floor"}
        order = kinds.count(FLOOR_DENSITY)
        return {"finite": q < max(order, self.rho), "factor": None,
                "case": f"a positive density at the floor in {order} shock(s)"}

    # The conditions, for one type.

    def conditions(self, beta: float) -> dict:
        rho, L, R, G = self.rho, self.L, self.R, self.G
        psi = self.psi
        thorn = (R * beta * L) ** (1 / rho)
        thorn_bar = min(thorn, R)
        p_min = self.worst_income_probability()
        E_psi_inv = psi.moment(-1.0)
        E_psi_1mrho = psi.moment(1.0 - rho)
        E_log_psi = psi.mean_log
        E_psi_log_psi = psi.mean_x_log_x
        E_psi_sq = psi.moment(2.0)

        def factor(name, value, bound=1.0, governs=""):
            return {"name": name, "factor": value, "bound": bound, "holds": value < bound,
                    "margin": bound - value, "governs": governs}

        # Welfare: E[v(m)] and E[u(c)] need E[(m - m_min)^(1 - rho)]; marginal welfare E[u'(c)] needs E[(m - m_min)^(-rho)].
        welfare = self.lower_tail_moment(rho - 1, thorn)
        marginal = self.lower_tail_moment(rho, thorn)

        out = {
            "thorn": thorn, "thorn_bar": thorn_bar, "worst_income_probability": p_min,
            "conditions": [
                factor("AIC", thorn, governs="consumption growth below one as m grows"),
                factor("RIC", thorn / R, governs="the limiting MPC is positive"),
                factor("WRIC", p_min ** (1 / rho) * thorn / R, governs="existence in place of the RIC"),
                factor("FHWC", G / R, governs="finite human wealth"),
                factor("PF-FVAC", beta * L * G ** (1 - rho), governs="finite perfect-foresight value of autarky"),
                factor("FVAC", beta * L * G ** (1 - rho) * E_psi_1mrho, governs="finite value of autarky"),
                factor("GIC", thorn / G, governs="the pseudo-target exists"),
                factor("GIC-Mod", thorn * E_psi_inv / G, governs="the buffer stock target exists"),
                factor("GIC-Szeidl", math.log(thorn / G), E_log_psi,
                       governs="with L = 1, the stationary population exists"),
                factor("GIC-Harmenberg", thorn / G, math.exp(E_psi_log_psi),
                       governs="with L = 1, the income-weighted stationary population exists"),
                factor("GIC-Liv", L * thorn / G, governs="aggregate balanced growth with estate destruction"),
            ],
            "welfare": {
                "welfare_finite": welfare["finite"], "welfare_factor": welfare["factor"], "welfare_case": welfare["case"],
                "marginal_finite": marginal["finite"], "marginal_factor": marginal["factor"],
                "marginal_case": marginal["case"],
            },
            "rate_condition": {"value": (R / G) * (thorn / G), "E_psi_squared": E_psi_sq,
                               "fast_approach": (R / G) * (thorn / G) < E_psi_sq},
            "implications": {
                "limiting_mpc": max(1 - thorn / R, 0.0),
                "mpc_at_lower_limit": 1 - p_min ** (1 / rho) * thorn / R,
            },
        }
        by_name = {c["name"]: c for c in out["conditions"]}
        out["valid"] = by_name["FVAC"]["holds"] and (by_name["RIC"]["holds"] or by_name["WRIC"]["holds"])
        out["domain"] = self._domain(thorn_bar, by_name, out["welfare"])
        return out

    def _tail_root(self, log_phi, start: float) -> float | None:
        """The smallest z > start with phi(z) = 1, given log phi, or None when phi stays below 1."""
        z = start if start > 0 else 1e-6
        if log_phi(z) >= 0:
            return z if start > 0 else None
        step = 1e-6
        while log_phi(z + step) < 0:
            step *= 2
            if z + step > 1e6:
                return None
        return brentq(log_phi, z, z + step, xtol=1e-12)

    def _domain(self, thorn_bar: float, by_name: dict, welfare: dict) -> dict:
        L, G = self.L, self.G
        psi = self.psi
        growth = thorn_bar / G
        a_nat = self.natural_borrowing_constraint()
        d = {}
        d["buffer_stock_target"] = growth * psi.moment(-1.0) < 1
        d["pseudo_target"] = growth < 1
        d["kink"] = True if math.isinf(a_nat) else self.a_art > a_nat + TOLERANCE
        log_growth = math.log(growth)
        if L < 1:
            # Mortality: a mixture over ages with weights (1 - L) L^s, and the income measure's weight L G per age. The
            # roots are found on log phi, since the moments of psi grow beyond double precision for large orders.
            population = lambda z: math.log(L) + z * log_growth + psi.log_moment(-z)
            income = lambda j: math.log(L * G) + j * log_growth + psi.log_moment(1.0 - j)
            d["population_measure"] = True
            d["population_tail_exponent"] = self._tail_root(population, 0.0)
            d["income_measure"] = L * G < 1
            d["income_tail_exponent"] = self._tail_root(income, 0.0) if d["income_measure"] else None
        else:
            # No mortality: the invariant laws of the chain and of its income-weighted (Harmenberg) version.
            population = lambda z: z * log_growth + psi.log_moment(-z)
            income = lambda j: j * log_growth + psi.log_moment(1.0 - j)
            d["population_measure"] = by_name["GIC-Szeidl"]["holds"]
            d["population_tail_exponent"] = self._tail_root(population, 1e-9) if d["population_measure"] else None
            d["income_measure"] = by_name["GIC-Harmenberg"]["holds"]
            d["income_tail_exponent"] = self._tail_root(income, 1e-9) if d["income_measure"] else None
        for measure in ("population", "income"):
            exponent = d[f"{measure}_tail_exponent"]
            exists = d[f"{measure}_measure"]
            d[f"{measure}_mean"] = exists and (exponent is None or exponent > 1)
            d[f"{measure}_variance"] = exists and (exponent is None or exponent > 2)
        d["welfare"] = d["population_measure"] and welfare["welfare_finite"]
        d["marginal_welfare"] = d["population_measure"] and welfare["marginal_finite"]
        return d

    def bellman_calibration(self, type_index: int = 0) -> dict:
        """The calibration mapping of bellman/buffer_stock.bl for one type, in the stage file's names.

        Bellman has no derived parameters, so a_Nat is computed here and written beside a_Art. The stage file writes the
        lognormal family for both shocks; a member with another law has no stage file yet (see shock-laws.md, "Bellman-SYM
        counterparts"), and the converter says so.
        """
        for name, law in (("permanent_shock", self.psi), ("employed_shock", self.theta)):
            if law.name != "LogNormal":
                raise ValueError(f"{name} is {law.name}, which has no Bellman-SYM family; the stage file writes LogNormal")
        a_nat = self.natural_borrowing_constraint()
        if math.isinf(a_nat):
            a_nat = self.a_art  # no finite natural constraint; the artificial one is the constraint in force
        return {
            "β": self.types[type_index]["beta"], "ℒ": self.L, "ρ": self.rho, "R": self.R, "𝒢": self.G,
            "a_Art": self.a_art, "a_Nat": a_nat,
            "σ_ψ": self.psi.params["sd_log"], "σ_θ": self.theta.params["sd_log"],
            "p_zero": self.wp, "ξ_min": self.xi_min,
        }

    def bellman_calibration_yaml(self, type_index: int = 0) -> str:
        import yaml

        header = (f"# bst/1 member {self.hash[:12]}…, type {type_index} (β = {self.types[type_index]['beta']}): the "
                  "calibration of bellman/buffer_stock.bl, written by the checker.\n")
        body = yaml.safe_dump({"calibration": self.bellman_calibration(type_index)}, allow_unicode=True,
                              sort_keys=False, default_flow_style=False)
        return header + body

    def report(self) -> dict:
        shocks = {}
        for name, law in (("permanent_shock", self.psi), ("employed_shock", self.theta)):
            shocks[name] = {
                "law": law.name, "mean": law.moment(1.0), "E_inverse": law.moment(-1.0),
                "E_log": law.mean_log, "E_x_log_x": law.mean_x_log_x, "E_square": law.moment(2.0),
                "infimum": law.infimum, "supremum": law.supremum, "mass_at_infimum": law.mass_at_infimum,
            }
        types = []
        for t in self.types:
            c = self.conditions(t["beta"])
            c["beta"] = t["beta"]
            c["share"] = t["share"]
            types.append(c)
        pooled = {}
        for key in types[0]["domain"]:
            if key.endswith("exponent"):
                continue
            pooled[key] = all(t["domain"][key] for t in types)
        return {
            "family": self.data["family"], "hash": self.hash, "valid": all(t["valid"] for t in types),
            "shocks": shocks,
            "implications": {
                "xi_infimum": self.xi_infimum(),
                "worst_income_probability": self.worst_income_probability(),
                "natural_borrowing_constraint": self.natural_borrowing_constraint(),
                "borrowing_constraint": self.a_art,
                "employed_scale": self.employed_scale,
                "newborn_min_resources": self.newborn_min_resources(),
            },
            "types": types, "pooled_domain": pooled,
        }


def load_member(path: Path) -> Member:
    data = load_strict(Path(path).read_text())
    return Member(data)
