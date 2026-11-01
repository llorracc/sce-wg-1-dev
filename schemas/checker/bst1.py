"""The checker for a parameter file of the four buffer-stock families, one for each borrowing-constraint scenario
(constraint-scenarios.md): validation, the scenario's requirements, the laws' moments, the conditions, the domain rules, the
implications; and the verification of a results file against the member it reports on.

The statements follow bst/conditions.md, in BST's notation: psi the permanent shock, xi the transitory shock, theta the
employed draw, wp the unemployment probability, xi_u the unemployment income, L survival, G growth, a_Art and a_Nat the
artificial and natural borrowing constraints. What is computed here is computed for the STATED member, the one the parameter
file names, from the laws' closed-form moments; it is the limit that a toolkit's effective member approaches, and nothing
here discretizes a shock. A results file reports the toolkit's effective member through the expectations the family names,
and the verification below checks only what needs no representation of the laws (effective-member.md).
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import jsonschema
from referencing import Registry, Resource
from scipy.optimize import brentq

from canonical import load_strict, model_hash
from laws import FLOOR_ATOM, FLOOR_DENSITY, FLOOR_THIN, TOLERANCE, filled, law_from_mapping

SCHEMAS = Path(__file__).resolve().parent.parent
BST = SCHEMAS / "bst"
# The four families, each a borrowing-constraint scenario with its own folder, parameter schema and stage file.
FAMILIES = {"bst-natural/1": "natural", "bst-natural-no-point-mass/1": "natural-no-point-mass",
            "bst-artificial/1": "artificial", "bst-zero-infima/1": "zero-infima"}
# The two principal scenarios have their folders in bst/; the other two are in bst/other/ (bst/model.md, "Families").
PRINCIPAL = ("natural", "artificial")
FOLDERS = {family: BST / scenario if scenario in PRINCIPAL else BST / "other" / scenario
           for family, scenario in FAMILIES.items()}
PARAMETER_SCHEMAS = {family: FOLDERS[family] / "parameters.schema.json" for family in FAMILIES}
STAGE_FILES = {family: FOLDERS[family] / "bellman" / f"{scenario}.bl" for family, scenario in FAMILIES.items()}
COMMON_SCHEMA = BST / "parameters.common.schema.json"
RESULTS_SCHEMA = BST / "results.schema.json"
SHOCK_LAW_SCHEMA = SCHEMAS / "shock-laws.schema.json"

# The precision of a closed-form evaluation; a condition whose margin lies within it is undecided for the stated member.
STATED_PRECISION = 1e-12
# The agreement asked of a toolkit's arithmetic: a reported factor against the one recomputed from its own expectations.
ARITHMETIC_TOLERANCE = 1e-9

CONDITION_NAMES = ["AIC", "RIC", "WRIC", "FHWC", "FVAC-PF", "FVAC", "GIC", "GIC-Mod", "GIC-Szeidl", "GIC-Harmenberg",
                   "GIC-Liv"]
EXPECTATION_NAMES = ["psi_mean", "theta_mean", "psi_pow_1_minus_rho", "psi_inverse", "psi_log", "psi_log_psi",
                     "psi_squared", "psi_pow_rho_minus_1", "psi_pow_rho", "worst_income_mass"]
CASE_BINDING = "the constraint binds"
CASE_ATOM = "an atom at the worst income"


class MemberError(ValueError):
    """The file is not a valid member of a buffer-stock family; the message lists every problem found."""


def _resource(path: Path) -> dict:
    """A schema with its file's URI as its $id, so that its relative references resolve against its own place."""
    data = json.loads(path.read_text())
    data["$id"] = path.resolve().as_uri()
    return data


def _validator(family: str):
    registry = Registry()
    for path in (SHOCK_LAW_SCHEMA, COMMON_SCHEMA):
        resource = _resource(path)
        registry = registry.with_resource(resource["$id"], Resource.from_contents(resource))
    return jsonschema.Draft202012Validator(_resource(PARAMETER_SCHEMAS[family]), registry=registry,
                                           format_checker=jsonschema.FormatChecker())


def validate(data) -> list[str]:
    """The parameter validator's complaints, as sentences with the path of each, against the schema of the family the file
    names."""
    family = data.get("family") if isinstance(data, dict) else None
    if family not in FAMILIES:
        return [f"family: {family!r} is not one of the buffer-stock families {sorted(FAMILIES)}; bst/1 is retired, its "
                "members split by borrowing-constraint scenario (constraint-scenarios.md)"]
    problems = []
    for error in sorted(_validator(family).iter_errors(data), key=lambda e: list(e.absolute_path)):
        path = "/".join(str(p) for p in error.absolute_path) or "/"
        problems.append(f"{path}: {error.message}")
    return problems


def validate_results(data) -> list[str]:
    """The results validator's complaints, as sentences with the path of each."""
    validator = jsonschema.Draft202012Validator(json.loads(RESULTS_SCHEMA.read_text()))
    problems = []
    for error in sorted(validator.iter_errors(data), key=lambda e: list(e.absolute_path)):
        path = "/".join(str(p) for p in error.absolute_path) or "/"
        problems.append(f"{path}: {error.message}")
    return problems


def verdict(margin: float) -> str:
    """holds, fails, or undecided when the margin lies within the precision of a closed-form evaluation."""
    if abs(margin) < STATED_PRECISION:
        return "undecided"
    return "holds" if margin > 0 else "fails"


def _close(a, b, tolerance=ARITHMETIC_TOLERANCE) -> bool:
    if a is None or b is None:
        return a is None and b is None
    if math.isinf(a) or math.isinf(b):
        return a == b
    return abs(a - b) <= tolerance * max(1.0, abs(a), abs(b))


def natural_limit_from(lowest_psi: float, lowest_income: float, G: float, R: float) -> float | None:
    """a_Nat from the lowest values of a representation: the capitalized worst income; None when psi_min >= R/G."""
    kappa = lowest_psi * G / R
    if kappa >= 1:
        return None
    return -lowest_income * kappa / (1 - kappa) + 0.0


class Member:
    """A valid member of a buffer-stock family with its laws, the moments of its shocks, and its conditions: the stated
    member."""

    def __init__(self, data: dict):
        self.data = data
        problems = validate(data)
        if problems:
            raise MemberError("; ".join(problems))
        self.hash = model_hash(filled(data))  # over the filled form: omitted bounds written in
        self.rho = data["crra"]
        self.types = data["types"]
        self.L = data["survival"]
        self.R = data["return"]
        income = data["income"]
        self.G = income["growth"]
        self.wp = income["unemployment"]["prob"]
        self.xi_u = income["unemployment"]["income"]
        self.psi = law_from_mapping(income["permanent_shock"])
        self.theta = law_from_mapping(income["employed_shock"])
        # The employed draw's scale, which keeps the mean of the transitory shock at one; it needs wp * xi_u < 1.
        self.employed_scale = None
        if self.wp * self.xi_u < 1:
            self.employed_scale = (1 - self.wp * self.xi_u) / (1 - self.wp)
        self.family = data["family"]
        self.scenario = FAMILIES[self.family]
        # The constraint in force: a_Art in the artificial scenario; the natural constraint a_Nat in the natural ones, and 0
        # in the zero-infima scenario, resolved once the laws are checked. natural: no artificial constraint is stated and
        # the natural one is not the binding kind (in the zero-infima scenario it binds, as an artificial one at 0 would).
        self.a_art = data.get("borrowing_constraint")
        self.natural = self.scenario in ("natural", "natural-no-point-mass")
        problems = self._check()
        if problems:
            raise MemberError("; ".join(problems))

    @property
    def xi_min(self):
        """The unemployment income xi_u under its former name, for readers of this module that still use it."""
        return self.xi_u

    def _check(self) -> list[str]:
        problems = []
        shares = sum(t["share"] for t in self.types)
        if abs(shares - 1) > TOLERANCE:
            problems.append(f"types: shares sum to {shares!r}, not 1")
        betas = [t["beta"] for t in self.types]
        if any(b <= a for a, b in zip(betas, betas[1:])):
            problems.append("types: betas must be strictly increasing, so that the file has one written form")
        if self.wp == 0 and self.xi_u != 0:
            problems.append("income/unemployment: with prob 0, income must be 0")
        if self.employed_scale is None:
            problems.append("income/unemployment: prob times income must be below 1, or the employed earn nothing")
        for name, law in (("permanent_shock", self.psi), ("employed_shock", self.theta)):
            problems += [f"income/{name}: {p}" for p in law.check()]
        if problems:
            return problems
        return problems + self._scenario_problems()

    def _scenario_problems(self) -> list[str]:
        """What the family's scenario requires of the laws and the constraint (constraint-scenarios.md)."""
        problems = []
        a_nat = self.natural_borrowing_constraint()
        s = self.scenario
        if s in ("natural", "natural-no-point-mass"):
            for name, law in (("permanent_shock", self.psi), ("employed_shock", self.theta)):
                if not (law.infimum > 0 and not math.isinf(law.supremum)):
                    problems.append(f"income/{name}: the natural scenarios need a law with a strictly positive lower and a "
                                    f"finite upper bound; {law.name} spans [{law.infimum!r}, {law.supremum!r}]")
            if math.isinf(a_nat):
                problems.append("income: G psi_min >= R, so h_min is infinite and there is no finite natural constraint")
            p_worst = self.worst_income_probability()
            if s == "natural" and not p_worst > 0:
                problems.append("income: the joint worst income, the worst transitory income with psi at its floor, has "
                                "probability zero, so the member is bst-natural-no-point-mass/1")
            if s == "natural-no-point-mass" and p_worst > 0:
                problems.append(f"income: the joint worst income is a point mass, with probability {p_worst!r}, so the "
                                "member is bst-natural/1")
            if not problems:
                self.a_art = a_nat
        elif s == "artificial":
            if not (self.psi.infimum > 0 and self.xi_infimum() > 0):
                problems.append("income: the artificial scenario needs the floors of psi and of transitory income strictly "
                                "positive, so that h_min > 0; with a zero floor the member is bst-zero-infima/1, or "
                                "bst-natural/1 when the zero is a zero-income event")
            elif not math.isinf(a_nat) and not self.a_art > a_nat + TOLERANCE:
                problems.append(f"borrowing_constraint {self.a_art!r} is not above the natural constraint {a_nat!r}; an "
                                "artificial constraint no tighter has no effect, so the member is a natural one")
        elif s == "zero-infima":
            if not (self.psi.infimum == 0 or self.theta.infimum == 0):
                problems.append("income: the zero-infima scenario needs the infimum of psi or of theta to be zero")
            if self.wp > 0 and self.xi_u == 0:
                problems.append("income/unemployment: a zero-income event makes E[xi^(-rho)] infinite, so a >= 0 is never "
                                "reached; with bounded laws the member is bst-natural/1")
            for name, law, needed in (("employed_shock", self.theta, True),
                                      ("permanent_shock", self.psi, self.psi.infimum == 0)):
                if needed and not _finite_moment(law, -self.rho):
                    problems.append(f"income/{name}: E[x^(-rho)] is infinite, so a >= 0 is never reached")
            if not problems:
                self.a_art = 0.0
        return problems

    # The transitory shock xi: xi_u with probability wp, else the scaled employed draw.

    def xi_infimum(self) -> float:
        employed_low = self.employed_scale * self.theta.infimum
        return min(self.xi_u, employed_low) if self.wp > 0 else employed_low

    def xi_mass_at_infimum(self) -> float:
        low = self.xi_infimum()
        employed_low = self.employed_scale * self.theta.infimum
        mass = 0.0
        if self.wp > 0 and self.xi_u == low:
            mass += self.wp
        if employed_low == low:
            mass += (1 - self.wp) * self.theta.mass_at_infimum
        return mass

    def worst_income_probability(self) -> float:
        """p_min, the probability that income takes its lowest value; BST's wp when the unemployment event pays nothing."""
        if self.wp > 0 and self.xi_u == 0:
            return self.wp
        return self.xi_mass_at_infimum() * self.psi.mass_at_infimum

    def natural_borrowing_constraint(self) -> float:
        """a_Nat, the lowest assets from which the worst income still allows positive consumption; -inf when none."""
        limit = natural_limit_from(self.psi.infimum, self.xi_infimum(), self.G, self.R)
        return -math.inf if limit is None else limit

    def newborn_min_resources(self) -> float:
        """The lowest m a newborn can have: born employed, with no assets."""
        return self.employed_scale * self.theta.infimum

    def xi_floor_kind(self) -> str:
        """How the transitory shock behaves at its lowest value: the unemployment atom, or the employed draw's floor."""
        employed_low = self.employed_scale * self.theta.infimum
        if self.wp > 0 and self.xi_u <= employed_low:
            return FLOOR_ATOM
        return self.theta.floor_kind

    # What a toolkit reports about its effective member, here evaluated for the stated member: the limits.

    def expectations(self) -> dict:
        """The expectations the family names (conditions.md), under the stated member's laws."""
        rho, psi = self.rho, self.psi
        return {
            "psi_mean": psi.moment(1.0), "theta_mean": self.theta.moment(1.0),
            "psi_pow_1_minus_rho": psi.moment(1.0 - rho), "psi_inverse": psi.moment(-1.0),
            "psi_log": psi.mean_log, "psi_log_psi": psi.mean_x_log_x, "psi_squared": psi.moment(2.0),
            "psi_pow_rho_minus_1": psi.moment(rho - 1.0), "psi_pow_rho": psi.moment(rho),
            "worst_income_mass": self.worst_income_probability(),
        }

    def lowest(self) -> dict:
        """The infima of the stated member: the limits of a representation's lowest values as it refines."""
        return {"psi": self.psi.infimum, "income": self.xi_infimum()}

    def derived(self) -> dict:
        """The derived parameters of the stated member."""
        a_nat = self.natural_borrowing_constraint()
        return {
            "natural_limit": None if math.isinf(a_nat) else a_nat,
            "constraint_in_force": self.a_art,
            "worst_income": self.psi.infimum * self.xi_infimum(),
            "employed_scale": self.employed_scale,
        }

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
        BufferStockTheory session, which checked the atom case and the one-density regimes numerically. A finite
        representation always has an atom at its lowest value, so an effective member falls under the atom case whenever
        its artificial constraint does not bind.
        """
        a_nat = self.natural_borrowing_constraint()
        if self.scenario == "zero-infima" or math.isinf(a_nat) or self.a_art > a_nat + TOLERANCE:
            return {"finite": True, "factor": None, "case": CASE_BINDING}
        if q <= 0:
            return {"finite": True, "factor": None, "case": "no negative moment needed"}
        p_min = self.worst_income_probability()
        if p_min > 0:
            factor = atom_factor(p_min, q, self.rho, self.L, self.G, thorn, self.psi.moment(q))
            return {"finite": factor < 1, "factor": factor, "case": CASE_ATOM}
        kinds = [self.psi.floor_kind, self.xi_floor_kind()]
        if FLOOR_THIN in kinds:
            return {"finite": True, "factor": None, "case": "a thin density at the floor"}
        order = kinds.count(FLOOR_DENSITY)
        return {"finite": q < max(order, self.rho), "factor": None,
                "case": f"a positive density at the floor in {order} shock(s)"}

    # The conditions, for one type.

    def factors(self, beta: float, E: dict) -> list[dict]:
        """The family's conditions as arithmetic on the expectations E and the parameters: the same arithmetic for the
        stated member, from its closed forms, and for a toolkit's effective member, from what it reports."""
        rho, L, R, G = self.rho, self.L, self.R, self.G
        thorn = (R * beta * L) ** (1 / rho)
        p_min = E["worst_income_mass"]

        def factor(name, value, bound=1.0, governs=""):
            margin = bound - value
            return {"name": name, "factor": value, "bound": bound, "holds": value < bound, "margin": margin,
                    "verdict": verdict(margin), "governs": governs}

        return [
            factor("AIC", thorn, governs="consumption growth below one as m grows"),
            factor("RIC", thorn / R, governs="the limiting MPC is positive"),
            factor("WRIC", p_min ** (1 / rho) * thorn / R, governs="existence in place of the RIC"),
            factor("FHWC", G / R, governs="finite human wealth"),
            factor("FVAC-PF", beta * L * G ** (1 - rho), governs="finite perfect-foresight value of autarky"),
            factor("FVAC", beta * L * G ** (1 - rho) * E["psi_pow_1_minus_rho"], governs="finite value of autarky"),
            factor("GIC", thorn / G, governs="the pseudo-target exists"),
            factor("GIC-Mod", thorn * E["psi_inverse"] / G, governs="the buffer stock target exists"),
            factor("GIC-Szeidl", math.log(thorn / G), E["psi_log"],
                   governs="with L = 1, the stationary population exists"),
            factor("GIC-Harmenberg", thorn / G, math.exp(E["psi_log_psi"]),
                   governs="with L = 1, the income-weighted stationary population exists"),
            factor("GIC-Liv", L * thorn / G, governs="aggregate balanced growth with estate destruction"),
        ]

    def conditions(self, beta: float) -> dict:
        rho, L, R, G = self.rho, self.L, self.R, self.G
        thorn = (R * beta * L) ** (1 / rho)
        thorn_bar = min(thorn, R)
        E = self.expectations()
        p_min = E["worst_income_mass"]

        # Welfare: E[v(m)] and E[u(c)] need E[(m - m_min)^(1 - rho)]; marginal welfare E[u'(c)] needs E[(m - m_min)^(-rho)].
        welfare = self.lower_tail_moment(rho - 1, thorn)
        marginal = self.lower_tail_moment(rho, thorn)

        out = {
            "member": "stated",
            "thorn": thorn, "thorn_bar": thorn_bar, "worst_income_probability": p_min,
            "conditions": self.factors(beta, E),
            "welfare": {
                "welfare_finite": welfare["finite"], "welfare_factor": welfare["factor"], "welfare_case": welfare["case"],
                "marginal_finite": marginal["finite"], "marginal_factor": marginal["factor"],
                "marginal_case": marginal["case"],
            },
            "rate_condition": {"value": (R / G) * (thorn / G), "E_psi_squared": E["psi_squared"],
                               "fast_approach": (R / G) * (thorn / G) < E["psi_squared"]},
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
        d["kink"] = self.scenario == "zero-infima" or math.isinf(a_nat) or self.a_art > a_nat + TOLERANCE
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

    # The verification of a results file: what needs no representation of the laws.

    def verify_results(self, results: dict) -> list[str]:
        """The problems a results file has against this member, with none meaning the report is consistent.

        Checked: the identity; the lowest values against the stated infima; the derived parameters as arithmetic on the
        lowest values; the expectations against what every law obeys, up to the reported mean; for each type, every
        factor as arithmetic on the reported expectations, every verdict against its factor, every status against the
        verdicts, and the welfare conditions' cases and factors. When the population block is present, its expectations
        decide the GIC-Szeidl, the GIC-Harmenberg and the welfare conditions, the household's everything else. Not
        checked, since it would need the representation: the expectations' values themselves, which are the toolkit's to
        compute.
        """
        problems = []
        rho, L, R, G = self.rho, self.L, self.R, self.G
        if results.get("family") != self.data["family"]:
            problems.append(f"family: {results.get('family')!r} is not {self.data['family']!r}")
        if results.get("parameter_file_sha256") != self.hash:
            problems.append("parameter_file_sha256: not this member's hash")
        effective = results["effective_member"]
        E, low, der = effective["expectations"], effective["lowest"], effective["derived"]
        # The population's representation, when it differs from the household's, decides the conditions on the
        # stationary population: the GIC-Szeidl, the GIC-Harmenberg, the welfare conditions and the tail exponents.
        population = effective.get("population")
        E_pop = population["expectations"] if population else E
        E_conditions = dict(E, psi_log=E_pop["psi_log"], psi_log_psi=E_pop["psi_log_psi"])

        # The lowest values lie at or above the stated member's infima, their limits as a representation refines.
        stated_low = self.lowest()
        blocks = [("effective_member/lowest", low)]
        if population:
            blocks.append(("effective_member/population/lowest", population["lowest"]))
        for where_low, values in blocks:
            for key in ("psi", "income"):
                if values[key] < stated_low[key] - TOLERANCE:
                    problems.append(f"{where_low}/{key}: {values[key]!r} lies below the stated infimum "
                                    f"{stated_low[key]!r}, which no representation of the law can reach")

        # The derived parameters are the arithmetic of the lowest values and the parameters.
        natural = natural_limit_from(low["psi"], low["income"], G, R)
        if not _close(der["natural_limit"], natural):
            problems.append(f"effective_member/derived/natural_limit: {der['natural_limit']!r} is not the capitalized "
                            f"worst income of the reported lowest values, {natural!r}")
        in_force = self.a_art if natural is None else max(self.a_art, natural)
        if not _close(der["constraint_in_force"], in_force):
            problems.append(f"effective_member/derived/constraint_in_force: {der['constraint_in_force']!r} is not "
                            f"max(a_Art, a_Nat) = {in_force!r}")
        if not _close(der["worst_income"], low["psi"] * low["income"]):
            problems.append("effective_member/derived/worst_income: not the product of the reported lowest values")
        if not _close(der["employed_scale"], self.employed_scale):
            problems.append(f"effective_member/derived/employed_scale: {der['employed_scale']!r} is not the family's "
                            f"(1 - wp xi_u)/(1 - wp) = {self.employed_scale!r}")

        # The expectations obey what every law obeys, by Jensen, up to the reported mean.
        expectation_blocks = [("effective_member/expectations", E)]
        if population:
            expectation_blocks.append(("effective_member/population/expectations", E_pop))
        for where_E, X in expectation_blocks:
            m = X["psi_mean"]
            slack = ARITHMETIC_TOLERANCE * max(1.0, abs(m))
            jensen = [
                ("psi_pow_1_minus_rho", X["psi_pow_1_minus_rho"], m ** (1 - rho), True),
                ("psi_inverse", X["psi_inverse"], 1 / m, True),
                ("psi_log", X["psi_log"], math.log(m), False),
                ("psi_log_psi", X["psi_log_psi"], m * math.log(m), True),
                ("psi_squared", X["psi_squared"], m * m, True),
                ("psi_pow_rho", X["psi_pow_rho"], m ** rho, True),
                ("psi_pow_rho_minus_1", X["psi_pow_rho_minus_1"], m ** (rho - 1), rho - 1 >= 1),
            ]
            for name, value, bound, convex in jensen:
                if convex and value < bound - slack:
                    problems.append(f"{where_E}/{name}: {value!r} is below {bound!r}, the least any law with mean "
                                    f"{m!r} allows")
                if not convex and value > bound + slack:
                    problems.append(f"{where_E}/{name}: {value!r} is above {bound!r}, the most any law with mean "
                                    f"{m!r} allows")

        # Each type: the factors, the verdicts, the statuses, the welfare conditions.
        types = results["types"]
        if len(types) != len(self.types):
            problems.append(f"types: {len(types)} reported, {len(self.types)} in the member")
        for i, (t, stated) in enumerate(zip(types, self.types)):
            where = f"types/{i}"
            beta = t["beta"]
            if not _close(beta, stated["beta"]):
                problems.append(f"{where}/beta: {beta!r} is not the member's {stated['beta']!r}")
                continue
            reported = t["conditions"]
            for c in self.factors(beta, E_conditions):
                r = reported[c["name"]]
                if not _close(r["factor"], c["factor"]):
                    problems.append(f"{where}/conditions/{c['name']}/factor: {r['factor']!r} is not the arithmetic of "
                                    f"the reported expectations and the parameters, {c['factor']!r}")
                if not _close(r["bound"], c["bound"]):
                    problems.append(f"{where}/conditions/{c['name']}/bound: {r['bound']!r} is not {c['bound']!r}")
                if r["holds"] != (r["factor"] < r["bound"]):
                    problems.append(f"{where}/conditions/{c['name']}/holds: {r['holds']!r} disagrees with the factor")

            thorn = (R * beta * L) ** (1 / rho)
            thorn_bar = min(thorn, R)
            kink = natural is None or in_force > natural + TOLERANCE
            target = thorn_bar * E["psi_inverse"] / G < 1
            pseudo = thorn_bar / G < 1
            population_measure = L < 1 or reported["GIC-Szeidl"]["holds"]
            income_measure = (L * G < 1) if L < 1 else reported["GIC-Harmenberg"]["holds"]

            # The welfare conditions, on the population's law: the case follows the constraint, and the atom case's
            # factor is arithmetic.
            for key, q, moment in (("welfare", rho - 1, E_pop["psi_pow_rho_minus_1"]),
                                   ("marginal_welfare", rho, E_pop["psi_pow_rho"])):
                w = reported[key]
                if kink:
                    if w["case"] != CASE_BINDING:
                        problems.append(f"{where}/conditions/{key}/case: the constraint binds in the "
                                        f"effective member, so the case is {CASE_BINDING!r}, not {w['case']!r}")
                    if not w["holds"]:
                        problems.append(f"{where}/conditions/{key}/holds: a binding constraint makes every "
                                        "welfare mean finite")
                elif w["case"] == CASE_ATOM:
                    expected = atom_factor(E_pop["worst_income_mass"], q, rho, L, G, thorn, moment)
                    if not _close(w["factor"], expected):
                        problems.append(f"{where}/conditions/{key}/factor: {w['factor']!r} is not the atom case's "
                                        f"arithmetic, {expected!r}")
                    if w["holds"] != (expected < 1):
                        problems.append(f"{where}/conditions/{key}/holds: disagrees with the factor")
                elif w["case"] == CASE_BINDING:
                    problems.append(f"{where}/conditions/{key}/case: the artificial constraint does not bind in the "
                                    "effective member")
            welfare = population_measure and reported["welfare"]["holds"]
            marginal = population_measure and reported["marginal_welfare"]["holds"]

            expected_statuses = {
                "kink": kink, "target": target, "pseudo_target": pseudo, "income_measure": income_measure,
                "welfare": welfare, "marginal_welfare": marginal,
            }
            for key, defined in expected_statuses.items():
                status = t[key]["status"]
                if defined and status == "undefined":
                    problems.append(f"{where}/{key}/status: undefined, but the toolkit's own verdicts define it")
                if not defined and status != "undefined":
                    problems.append(f"{where}/{key}/status: {status!r}, but the toolkit's own verdicts leave it "
                                    "undefined")
        return problems

    def bellman_calibration(self, type_index: int = 0) -> dict:
        """The calibration mapping of the family's stage file for one type, in the stage file's names.

        Each stage file writes its laws' family: TruncatedLogNormal in the natural and artificial scenarios, LogNormal in the
        zero-infima scenario; a member with another law has no stage file yet, and the converter says so. Bellman-SYM has no
        derived parameters, so the stage files write the natural limit out from the laws' bounds, which come from here.
        """
        want = "LogNormal" if self.scenario == "zero-infima" else "TruncatedLogNormal"
        for name, law in (("permanent_shock", self.psi), ("employed_shock", self.theta)):
            if law.name != want:
                raise ValueError(f"{name} is {law.name}; the stage file of {self.family} writes {want}")
        cal = {"β": self.types[type_index]["beta"], "ℒ": self.L, "ϱ": self.rho, "R": self.R, "𝒢": self.G}
        if self.scenario == "artificial":
            cal["a_Art"] = self.a_art
        if want == "TruncatedLogNormal":
            for sym, law in (("ψ", self.psi), ("θ", self.theta)):
                cal.update({f"μ_{sym}": law.normal.location, f"s_{sym}": law.normal.scale,
                            f"{sym}_min": law.infimum, f"{sym}_max": law.supremum})
        else:
            cal.update({"σ_ψ": self.psi.params["sd_log"], "σ_θ": self.theta.params["sd_log"]})
        cal["p_zero"] = self.wp
        if self.scenario != "natural":
            # With p_zero = 0 the unemployment income is never paid; the natural limit's worst transitory income is then
            # the employed floor, which the stage file reads as min(ξ_u, the scaled employed floor).
            xi_u = self.xi_u
            if self.wp == 0 and self.scenario == "natural-no-point-mass":
                xi_u = self.employed_scale * self.theta.infimum
            cal["ξ_u"] = xi_u
        return cal

    def bellman_calibration_yaml(self, type_index: int = 0) -> str:
        import yaml

        stage = STAGE_FILES[self.family].relative_to(SCHEMAS)
        header = (f"# {self.family} member {self.hash[:12]}…, type {type_index} (β = {self.types[type_index]['beta']}): "
                  f"the calibration of {stage}, written by the checker.\n")
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
            "family": self.data["family"], "hash": self.hash, "member": "stated",
            "valid": all(t["valid"] for t in types),
            "shocks": shocks,
            "expectations": self.expectations(), "lowest": self.lowest(), "derived": self.derived(),
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


def atom_factor(p_min: float, q: float, rho: float, L: float, G: float, thorn: float, E_psi_q: float) -> float:
    """The factor of the atom case: E[(m - m_min)^(-q)] is finite exactly when it is below one."""
    return p_min ** (1 - q / rho) * L * (G / thorn) ** q * E_psi_q


def _finite_moment(law, k: float) -> bool:
    """Whether E[x^k] of a law is finite."""
    try:
        value = law.moment(k)
    except (OverflowError, ValueError, ZeroDivisionError):
        return False
    return value is not None and math.isfinite(value)


def load_member(path: Path) -> Member:
    data = load_strict(Path(path).read_text())
    return Member(data)
