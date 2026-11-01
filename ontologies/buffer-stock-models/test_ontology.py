"""Tests of the ontology of buffer-stock models.

    uv run --with pyyaml --with jsonschema --with referencing --with scipy --with numpy --with rdflib --with pytest pytest -q

The generator already refuses a source that fails its checks; these tests run it, and then check what the ontology
claims:
- the generated files are current, and the Turtle file parses as RDF;
- the generator refuses a broken source;
- the moments' formulas agree with the closed forms of the mean-one lognormal;
- every condition, evaluated from the ontology's own formulas, gives the schemas' checker's verdict, and every plain
  factor its value, for every type of every member of the buffer-stock families;
- every implication among the conditions alone holds on sampled models, and is tested on enough of them that it is not
  vacuous; and conditions the ontology keeps apart do come apart;
- the axioms classify the families' members as the README says, each in exactly the scenario its family writes;
- each written form a term names in the parameter file or the stage file exists there.

The ontology states its terms; the checker computes them for the schemas. Agreement between the two is the test that the
ontology denotes what the schemas write.
"""

from __future__ import annotations

import copy
import math
import re
import sys
from pathlib import Path

import numpy as np
import pytest

import generate
import formulas

HERE = Path(__file__).resolve().parent
SCHEMAS = HERE.parent.parent / "schemas"
sys.path.insert(0, str(SCHEMAS / "checker"))
import bst1  # noqa: E402  the schemas' checker

SOURCE, _ = generate.load()
BY_NAME = {row["name"]: (kind, row) for kind, row in generate.rows(SOURCE)}
CONDITIONS = {c["name"]: c for c in SOURCE["conditions"]}
BST = SCHEMAS / "bst"
MEMBERS = sorted([*BST.glob("*/members/*.yaml"), *BST.glob("other/*/members/*.yaml")])
SCENARIOS = ("natural", "natural-no-point-mass", "artificial", "zero-infima")
FOLDER = {bst1.FAMILIES[family]: folder for family, folder in bst1.FOLDERS.items()}   # the principal two in bst/, the others in bst/other/
# The checker's names for the ontology's conditions, and the conditions the checker does not compute: the condition of
# Ma, Stachurski and Toda, which the families' conditions.md does not name.
CHECKER_NAME = {c["name"]: c["short"] for c in SOURCE["conditions"]}
NOT_IN_CHECKER = {"discounted-return"}
MARGIN = 1e-9


def environment(primitives: dict, expectation, bounds: dict) -> dict:
    """Every symbol of the ontology for one model, from its primitives, its law of ψ and its bounds, by the ontology's
    own formulas: the moments under the law, then the quantities in order."""
    env = dict(primitives)
    env.update(bounds)
    for m in SOURCE["moments"]:
        env[m["symbol"]] = formulas.evaluate(m["formula"], {**env, "E": expectation})
    for q in SOURCE["quantities"]:
        try:
            env[q["symbol"]] = formulas.evaluate(q["formula"], env)
        except ZeroDivisionError:
            env[q["symbol"]] = math.inf
    return env


def holds(env: dict) -> dict:
    return {name: bool(formulas.evaluate(c["holds"], env)) for name, c in CONDITIONS.items()}


def margins(env: dict) -> dict:
    """How far each condition is from its boundary, so that a sample on a boundary can be set aside."""
    out = {}
    for name, c in CONDITIONS.items():
        left, right = re.split(r"\s*<\s*", c["holds"])
        out[name] = abs(formulas.evaluate(left, env) - formulas.evaluate(right, env))
    return out


def discrete(atoms, weights):
    atoms, weights = np.asarray(atoms, float), np.asarray(weights, float)
    return lambda g: float(np.sum(weights * g(atoms)))


def lognormal(sigma: float, nodes: int = 120):
    """The expectation under the mean-one lognormal with standard deviation σ of the log, by Gauss-Hermite."""
    x, w = np.polynomial.hermite_e.hermegauss(nodes)
    atoms = np.exp(-sigma**2 / 2 + sigma * x)
    return discrete(atoms, w / w.sum())


# The generated files and the generator's refusals.

def test_generated_files_are_current():
    assert generate.main(["--check"]) == 0


def test_turtle_parses_as_rdf():
    rdflib = pytest.importorskip("rdflib")
    graph = rdflib.Graph().parse(data=generate.TURTLE.read_text(encoding="utf-8"), format="turtle")
    ns = rdflib.Namespace(SOURCE["ontology"]["namespace"])
    rows = {s for s in graph.subjects() if str(s).startswith(str(ns) + "BSM_")}
    assert len(rows) == len(generate.rows(SOURCE))


@pytest.mark.parametrize("break_it", [
    lambda s: s["results"][0]["assumes"].append("no-such-condition"),
    lambda s: s["conditions"][0].update(holds="thorn < undefined_symbol"),
    lambda s: s["objects"][3]["sources"].update(bst=["not-an-anchor-of-the-page"]),
    lambda s: s["objects"][3].setdefault("written_as", {}).update(registry="not-a-registry-key"),
    lambda s: s["quantities"][1].update(id=s["quantities"][0]["id"]),
    lambda s: s["model-classes"][1].update(subclass_of="no-such-class"),
    lambda s: s["objects"][7].update(law={"pd": ["PD_9999999"]}),
    lambda s: s["quantities"][0].update(formula="E(X)"),
    lambda s: next(r for r in s["objects"] if r["name"] == "value-arrival").update(perch="perch-decision"),
    lambda s: next(r for r in s["objects"] if r["name"] == "stage").update(bellman_concept="not-a-bellman-concept"),
    lambda s: next(r for r in s["objects"] if r["name"] == "value-decision").update(of_state="consumption"),
    lambda s: next(r for r in s["results"] if r["name"] == "liquidity-constrained-limit").update(limit_in="crra"),
])
def test_the_generator_refuses_a_broken_source(break_it):
    broken = copy.deepcopy(SOURCE)
    break_it(broken)
    with pytest.raises(generate.SourceError):
        generate.check(broken)


# The formulas.

@pytest.mark.parametrize("sigma", [0.05, 0.1, 0.3, 0.6])
@pytest.mark.parametrize("rho", [1.5, 2.0, 4.0])
def test_moments_agree_with_the_lognormal_closed_forms(sigma, rho):
    primitives = {"rho": rho, "beta": 0.96, "L": 1.0, "R": 1.03, "G": 1.01, "wp": 0.0, "xi_u": 0.0, "a_Art": 0.0}
    env = environment(primitives, lognormal(sigma), {"psi_min": 0.0, "xi_min": 0.0, "xi_atom": 0.0, "p_worst": 0.0})
    s2 = sigma**2
    assert env["E_psi_inv"] == pytest.approx(math.exp(s2), rel=1e-12)
    assert env["E_psi_1mrho"] == pytest.approx(math.exp((1 - rho) * (-rho) * s2 / 2), rel=1e-12)
    assert env["E_log_psi"] == pytest.approx(-s2 / 2, rel=1e-12)
    assert env["E_psi_log_psi"] == pytest.approx(s2 / 2, rel=1e-10)
    assert env["E_psi_mrho"] == pytest.approx(math.exp(rho * (rho + 1) * s2 / 2), rel=1e-10)


def member_environment(member: bst1.Member, beta: float) -> dict:
    """The ontology's symbols for one type of a stated member: primitives and bounds from the member, the moments by the
    ontology's formulas under the checker's closed forms."""
    E = member.expectations()
    closed = {"E(X**-1)": E["psi_inverse"], "E(X**(1 - rho))": E["psi_pow_1_minus_rho"], "E(log(X))": E["psi_log"],
              "E(X*log(X))": E["psi_log_psi"], "E(X**(-rho))": member.psi.moment(-member.rho)}
    env = {"rho": member.rho, "beta": beta, "L": member.L, "R": member.R, "G": member.G, "wp": member.wp,
           "xi_u": member.xi_u, "a_Art": member.a_art, "psi_min": member.psi.infimum, "xi_min": member.xi_infimum(),
           "psi_max": member.psi.supremum, "theta_min": member.theta.infimum, "theta_max": member.theta.supremum,
           "xi_atom": member.xi_mass_at_infimum(), "p_worst": member.worst_income_probability()}
    for m in SOURCE["moments"]:
        env[m["symbol"]] = closed[m["formula"]]
    for q in SOURCE["quantities"]:
        try:
            env[q["symbol"]] = formulas.evaluate(q["formula"], env)
        except ZeroDivisionError:
            env[q["symbol"]] = math.inf
    a_nat = member.natural_borrowing_constraint()
    env["a_Nat"], env["a_min"] = a_nat, max(member.a_art, a_nat)
    return env


@pytest.mark.parametrize("path", MEMBERS, ids=lambda p: p.stem)
def test_conditions_agree_with_the_checker(path):
    member = bst1.load_member(path)
    for t in member.types:
        env = member_environment(member, t["beta"])
        ours = holds(env)
        theirs = {f["name"]: f for f in member.factors(t["beta"], member.expectations())}
        assert {n for n in CONDITIONS if CHECKER_NAME[n] not in theirs} == NOT_IN_CHECKER
        for name, c in CONDITIONS.items():
            if name in NOT_IN_CHECKER:
                continue
            assert ours[name] == theirs[CHECKER_NAME[name]]["holds"], (path.stem, t["beta"], name)
            if c["name"] not in ("gic-szeidl", "gic-harmenberg"):  # the checker writes these two as log and exp
                factor = env[BY_NAME[c["factor"]][1]["symbol"]]
                assert factor == pytest.approx(theirs[CHECKER_NAME[name]]["factor"], rel=1e-12), (path.stem, name)


# The implications among the conditions.

def sampled_models(n: int, seed: int = 20261031):
    rng = np.random.default_rng(seed)
    for i in range(n):
        if i % 3 == 0:
            expectation = lognormal(rng.uniform(0.0, 0.8))
        else:
            k = int(rng.integers(1, 6))
            atoms = rng.uniform(0.05, 3.0, size=k)
            weights = rng.dirichlet(np.ones(k))
            atoms = atoms / np.sum(weights * atoms)  # mean one
            expectation = discrete(atoms, weights)
        primitives = {"rho": rng.uniform(1.01, 8.0), "beta": rng.uniform(0.3, 1.3), "L": min(1.0, rng.uniform(0.8, 1.05)),
                      "R": rng.uniform(0.85, 1.2), "G": rng.uniform(0.85, 1.2), "wp": rng.uniform(0, 0.3),
                      "xi_u": 0.0, "a_Art": 0.0}
        bounds = {"psi_min": 0.0, "xi_min": 0.0, "xi_atom": 0.0, "p_worst": rng.uniform(0.0, 1.0)}
        yield environment(primitives, expectation, bounds)


IMPLICATIONS = [r for r in SOURCE["results"]
                if r["concludes"] and all(x.removeprefix("not ") in CONDITIONS for x in r["assumes"] + r["concludes"])]


def test_there_are_implications_to_test():
    assert len(IMPLICATIONS) >= 10


def test_every_implication_among_the_conditions_holds():
    tested = {r["name"]: 0 for r in IMPLICATIONS}
    for env in sampled_models(6000):
        verdict, margin = holds(env), margins(env)

        def true(literal):
            return not verdict[literal[4:]] if literal.startswith("not ") else verdict[literal]

        for r in IMPLICATIONS:
            involved = [x.removeprefix("not ") for x in r["assumes"] + r["concludes"]]
            if any(margin[c] < MARGIN for c in involved):
                continue
            if all(true(x) for x in r["assumes"]):
                tested[r["name"]] += 1
                assert all(true(x) for x in r["concludes"]), (r["name"], {k: env[k] for k in ("rho", "beta", "L", "R", "G")})
    vacuous = [name for name, count in tested.items() if count < 50]
    assert not vacuous, f"premises too rarely met to test: {vacuous}"


def test_the_growth_conditions_are_distinct():
    """GIC-Mod, GIC-Szeidl and GIC are three conditions, not one: there are models that satisfy each and not the next
    stronger, as the paper's example with a larger permanent shock shows."""
    found = {("gic", "gic-szeidl"): False, ("gic-szeidl", "gic-mod"): False, ("wric", "ric"): False,
             ("gic-harmenberg", "gic"): False, ("gic-liv", "gic"): False}
    for env in sampled_models(3000):
        v = holds(env)
        for weaker, stronger in found:
            if v[weaker] and not v[stronger]:
                found[(weaker, stronger)] = True
    assert all(found.values()), [pair for pair, seen in found.items() if not seen]


# The axioms.

def axiom_holds(name: str, env: dict) -> bool:
    return bool(formulas.evaluate(BY_NAME[name][1]["check"], env))


# What the axioms say of each member: the scenario axioms, and whether the paper's hypotheses hold.
EXPECTED = {
    "library": {"bounded-support": True, "natural-in-force": True, "point-mass-at-joint-worst-income": True,
                "zero-income-event": True, "no-artificial-constraint": True, "infinite-lives": True},
    "toy-natural": {"bounded-support": True, "natural-in-force": True, "point-mass-at-joint-worst-income": False,
                    "no-point-mass-at-joint-worst-income": True, "zero-income-event": False, "infinite-lives": False},
    "toy": {"bounded-support": True, "natural-in-force": False, "artificial-tighter": True, "positive-floors": True,
            "no-borrowing": True, "zero-income-event": False},
    "toy-untruncated": {"bounded-support": False, "zero-infimum": True, "no-zero-income-event": True, "no-borrowing": True,
                        "artificial-tighter": False, "infinite-lives": False},
    # BST's experiment "The Liquidity Constrained Solution as a Limit": three natural rungs and the restrained consumer.
    **{f"bst-p-zero-{wp}": {"bounded-support": True, "natural-in-force": True, "point-mass-at-joint-worst-income": True,
                            "zero-income-event": True, "no-artificial-constraint": True, "infinite-lives": True}
       for wp in ("0.005", "0.0005", "0.00005")},
    "iid-ui-artificial": {"bounded-support": True, "natural-in-force": False, "artificial-tighter": True,
                          "positive-floors": True, "no-borrowing": True, "zero-income-event": False},
    "bst-restrained": {"bounded-support": True, "natural-in-force": False, "artificial-tighter": True,
                       "positive-floors": True, "no-borrowing": True, "zero-income-event": False, "infinite-lives": True},
}
# The class each family's members fall in, and the four scenario classes.
SCENARIO_OF = {"bst-natural/1": "natural-with-point-mass", "bst-natural-no-point-mass/1": "natural-without-point-mass",
               "bst-artificial/1": "with-artificial-constraint", "bst-zero-infima/1": "zero-infima"}


def _member(stem):
    return bst1.load_member(next(p for p in MEMBERS if p.stem == stem))


@pytest.mark.parametrize("stem", sorted(EXPECTED))
def test_the_axioms_classify_the_members(stem):
    member = _member(stem)
    env = member_environment(member, member.types[0]["beta"])
    assert axiom_holds("crra-above-one", env) and axiom_holds("asset-return", env)
    for axiom, expected in EXPECTED[stem].items():
        assert axiom_holds(axiom, env) is expected, (stem, axiom)


def _in_class(name: str, env: dict) -> bool:
    """Whether a model meets the checkable axioms of a class and of every class above it."""
    classes = {c["name"]: c for c in SOURCE["model-classes"]}
    while name:
        for axiom in classes[name].get("axioms", []):
            if "check" in BY_NAME[axiom][1] and not axiom_holds(axiom, env):
                return False
        name = classes[name].get("subclass_of")
    return True


@pytest.mark.parametrize("path", MEMBERS, ids=lambda p: p.stem)
def test_each_member_is_in_exactly_its_family_s_scenario(path):
    """The four scenarios partition the class: each member meets its family's scenario's axioms and no other's."""
    member = bst1.load_member(path)
    env = member_environment(member, member.types[0]["beta"])
    inside = [s for s in SCENARIO_OF.values() if _in_class(s, env)]
    assert inside == [SCENARIO_OF[member.family]], (path.stem, inside)


def test_every_member_is_covered():
    assert {p.stem for p in MEMBERS} == set(EXPECTED)


# The classes.

def test_the_classes_form_a_tree():
    classes = {c["name"]: c for c in SOURCE["model-classes"]}
    for name, c in classes.items():
        seen, at = set(), name
        while "subclass_of" in classes[at]:
            assert at not in seen
            seen.add(at)
            at = classes[at]["subclass_of"]
        assert at == "buffer-stock-model" or "benchmark_of" in c, name
    assert classes["perfect-foresight-benchmark"].get("benchmark_of") == "buffer-stock-model"


def test_the_two_constraints_are_told_apart():
    """The natural and the artificial constraint make different models: the atom at the worst transitory shock is
    required only where the natural constraint is in force; the natural constraint never binds and an artificial one
    does; the constrained perfect-foresight benchmark is the artificial class's limit as the shocks vanish, as BST's own
    class approaches it as the zero-income event's probability vanishes."""
    classes = {c["name"]: c for c in SOURCE["model-classes"]}
    results = {r["name"]: r for r in SOURCE["results"]}
    assert BY_NAME["point-mass-at-joint-worst-income"][1]["check"] == "p_worst > 0"
    assert BY_NAME["point-mass-at-joint-worst-income"][1]["of"] == "natural-with-point-mass"
    assert classes["with-artificial-constraint"]["reduces_to"]["when"] == "a_Art <= a_Nat"
    assert (results["natural-constraint-never-binds"]["within"], results["natural-constraint-never-binds"]["concludes"]) \
        == ("natural-with-point-mass", ["not constraint-binds"])
    assert (results["zero-infima-constraint-binds"]["within"], results["zero-infima-constraint-binds"]["concludes"]) \
        == ("zero-infima", ["constraint-binds"])
    assert classes["bst-model"]["subclass_of"] == "natural-with-point-mass"
    assert (results["artificial-constraint-binds"]["within"], results["artificial-constraint-binds"]["concludes"]) \
        == ("with-artificial-constraint", ["constraint-binds"])
    pfc = classes["perfect-foresight-constrained"]
    assert pfc["subclass_of"] == "perfect-foresight-benchmark" and pfc["benchmark_of"] == "liquidity-constrained"
    assert classes["liquidity-constrained"]["subclass_of"] == "buffer-stock-model"
    assert results["liquidity-constrained-limit"]["limit_in"] == "liquidity-constrained"
    for name in ("pf-constrained", "pf-constraint-relevance", "pf-constrained-without-ric", "pf-constrained-degenerate",
                 "pf-constraint-slack", "pf-constrained-converges"):
        assert results[name]["within"] == "perfect-foresight-constrained", name


# The denotation: the written forms the ontology names exist in the schemas.

def _schema_paths(node, prefix="") -> set[str]:
    out = set()
    for key, child in node.get("properties", {}).items():
        out.add(prefix + key)
        out |= _schema_paths(child, prefix + key + ".")
        if "items" in child:
            out |= _schema_paths(child["items"], prefix + key + "[].")
    return out


def _family_schema(scenario: str) -> dict:
    """A family's parameter schema with its references to the shared definitions written in."""
    import json
    common = json.loads((BST / "parameters.common.schema.json").read_text(encoding="utf-8"))["$defs"]
    schema = json.loads((FOLDER[scenario] / "parameters.schema.json").read_text(encoding="utf-8"))
    for key, spec in schema["properties"].items():
        ref = spec.get("$ref", "")
        if "parameters.common.schema.json#" in ref:
            schema["properties"][key] = common[ref.rsplit("/", 1)[1]]
    return schema


def test_parameter_file_keys_exist():
    paths = set().union(*(_schema_paths(_family_schema(s)) for s in SCENARIOS))
    named = [r["written_as"]["parameter-file"] for _, r in generate.rows(SOURCE) if "parameter-file" in r.get("written_as", {})]
    assert named and all(p in paths for p in named), [p for p in named if p not in paths]


def _in_stage(spelling: str, stage: str) -> bool:
    parts = [spelling] if spelling.startswith(("E_", "D_")) else spelling.split(".")
    return all(re.search(rf"id={re.escape(part)}\b", stage) or re.search(rf"(?<![\w]){re.escape(part)}(?![\w])", stage)
               for part in parts)


def test_stage_file_identifiers_exist():
    """Every spelling the ontology names is in one of the four families' stage files."""
    stage = "\n".join((FOLDER[s] / "bellman" / f"{s}.bl").read_text(encoding="utf-8") for s in SCENARIOS)
    named = [r["written_as"]["bellman-sym"] for _, r in generate.rows(SOURCE) if "bellman-sym" in r.get("written_as", {})]
    missing = [s for s in named if not _in_stage(s, stage)]
    assert named and not missing, missing
    assert "!mrgnvl" not in stage and all(_in_stage(s, stage) for s in ("D_{m}V", "D_{k}V[<]", "D_{a}V[>]"))


# Bellman-SYM's terms.

def test_every_value_and_function_of_a_state_has_its_perch():
    for row in SOURCE["objects"]:
        if row["category"] == "value" or "of_state" in row:
            assert "perch" in row and "of_state" in row, row["name"]


def test_the_three_perches_and_their_states():
    perches = {r["name"]: r for r in SOURCE["objects"] if r["category"] == "perch"}
    assert set(perches) == {"perch-arrival", "perch-decision", "perch-continuation"}
    states = {r["perch"]: r["name"] for r in SOURCE["objects"] if r["category"] == "state" and "perch" in r}
    assert states == {"perch-arrival": "kapital", "perch-decision": "market-resources",
                      "perch-continuation": "end-of-period-assets"}


def test_the_formats_roles():
    roles = {fmt: spec["role"] for fmt, spec in SOURCE["ontology"]["formats"].items()}
    assert roles == {"bst": "notation", "registry": "notation", "parameter-file": "calibration",
                     "bellman-sym": "notation"}


def test_no_row_is_an_event():
    """A two-point outcome is a shock on a two-point set, as Bellman-SYM has it; the category event is gone."""
    assert "event" not in SOURCE["categories"]
    assert {r["category"] for r in SOURCE["objects"]} <= set(SOURCE["categories"])


def test_the_ontology_names_no_toolkit():
    """The owner's instruction of 2026-11-01: the ontology names no toolkit, and nothing peculiar to how a toolkit solves
    or simulates a model. Each toolkit's names for the terms, and its departures from them, are in its Rosetta Stone."""
    text = (HERE / "source.yaml").read_text(encoding="utf-8")
    assert "hark" not in SOURCE["ontology"]["sources"] and "realization" not in SOURCE["ontology"]["format_roles"]
    for _, row in generate.rows(SOURCE):
        assert "hark" not in row.get("written_as", {}) and "hark" not in row.get("sources", {}), row["name"]
        assert row.get("where") != "hark", row["name"]
    named = sorted({w for w in ("HARK", "Econ-ARK", "QuantEcon", "Dolo", "JAX") if w in text})
    assert named == [], named


def test_the_conditions_of_ma_stachurski_and_toda():
    """Their discounted-return factor is E[(Þ̊_𝒢/ψ)^ϱ]; it is Þ̊_𝒢^ϱ without permanent shocks, so that their condition
    is then the GIC; and the mean return times their s̄ = Þ̊_R is the GIC-Mod's factor, so that their stationarity
    condition is the RIC with the GIC-Mod."""
    rng = np.random.default_rng(20261101)
    for _ in range(200):
        sigma, rho = rng.uniform(0.05, 0.6), rng.uniform(1.01, 8.0)
        primitives = {"rho": rho, "beta": rng.uniform(0.3, 1.3), "L": rng.uniform(0.9, 1.0), "R": rng.uniform(0.9, 1.2),
                      "G": rng.uniform(0.9, 1.2), "wp": 0.0, "xi_u": 0.0, "a_Art": 0.0}
        bounds = {"psi_min": 0.0, "xi_min": 0.5, "xi_atom": 0.0, "p_worst": 0.0}
        E = lognormal(sigma)
        env = environment(primitives, E, bounds)
        assert env["g_beta_R"] == pytest.approx(E(lambda x: (env["thorn_G"] / x) ** rho), rel=1e-9)
        assert env["thorn_R"] * (env["R"] / env["G"]) * env["E_psi_inv"] == pytest.approx(env["thorn_G_mod"], rel=1e-12)
        sure = environment(primitives, discrete([1.0], [1.0]), bounds)
        assert sure["g_beta_R"] == pytest.approx(sure["thorn_G"] ** rho, rel=1e-12)
        assert (sure["g_beta_R"] < 1) == (sure["thorn_G"] < 1)
    results = {r["name"]: r for r in SOURCE["results"]}
    assert (results["mst-existence"]["assumes"], results["mst-existence"]["within"]) \
        == (["fvac", "discounted-return"], "liquidity-constrained")
    assert BY_NAME["no-borrowing"][1]["check"] == "a_min == 0 and (wp == 0 or xi_u > 0)"
