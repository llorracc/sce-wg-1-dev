"""Tests of the ontology of buffer-stock models.

    uv run --with pyyaml --with jsonschema --with referencing --with scipy --with numpy --with rdflib --with pytest pytest -q

The generator already refuses a source that fails its checks; these tests run it, and then check what the ontology
claims:
- the generated files are current, and the Turtle file parses as RDF;
- the generator refuses a broken source;
- the moments' formulas agree with the closed forms of the mean-one lognormal;
- every condition, evaluated from the ontology's own formulas, gives the schemas' checker's verdict, and every plain
  factor its value, for every type of every bst/1 member;
- every implication among the conditions alone holds on sampled models, and is tested on enough of them that it is not
  vacuous; and conditions the ontology keeps apart do come apart;
- the axioms classify the bst/1 members as the README says;
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
MEMBERS = sorted((SCHEMAS / "bst-1" / "members").glob("*.yaml"))
# The checker's names for the ontology's conditions.
CHECKER_NAME = {c["name"]: c["short"] for c in SOURCE["conditions"]}
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


def member_environment(member: bst1.Member, beta: float) -> dict:
    """The ontology's symbols for one type of a stated member: primitives and bounds from the member, the moments by the
    ontology's formulas under the checker's closed forms."""
    E = member.expectations()
    closed = {"E(X**-1)": E["psi_inverse"], "E(X**(1 - rho))": E["psi_pow_1_minus_rho"], "E(log(X))": E["psi_log"],
              "E(X*log(X))": E["psi_log_psi"]}
    env = {"rho": member.rho, "beta": beta, "L": member.L, "R": member.R, "G": member.G, "wp": member.wp,
           "xi_u": member.xi_u, "a_Art": member.a_art, "psi_min": member.psi.infimum, "xi_min": member.xi_infimum(),
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
        for name, c in CONDITIONS.items():
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


# What the axioms say of each bst/1 member: membership in buffer-stock-model, and whether the paper's hypotheses hold.
EXPECTED = {
    "library": {"point-mass-at-worst-transitory": True, "zero-income-event": True, "no-artificial-constraint": True,
                "infinite-lives": True},
    "toy": {"point-mass-at-worst-transitory": True, "zero-income-event": False, "no-artificial-constraint": False,
            "infinite-lives": False},
    "toy-untruncated": {"point-mass-at-worst-transitory": False, "zero-income-event": False,
                        "no-artificial-constraint": True, "infinite-lives": False},
}


@pytest.mark.parametrize("stem", sorted(EXPECTED))
def test_the_axioms_classify_the_members(stem):
    member = bst1.load_member(SCHEMAS / "bst-1" / "members" / f"{stem}.yaml")
    env = member_environment(member, member.types[0]["beta"])
    assert axiom_holds("crra-above-one", env) and axiom_holds("asset-return", env)
    for axiom, expected in EXPECTED[stem].items():
        assert axiom_holds(axiom, env) is expected, (stem, axiom)


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


# The denotation: the written forms the ontology names exist in the schemas.

def _schema_paths(node, prefix="") -> set[str]:
    out = set()
    for key, child in node.get("properties", {}).items():
        out.add(prefix + key)
        out |= _schema_paths(child, prefix + key + ".")
        if "items" in child:
            out |= _schema_paths(child["items"], prefix + key + "[].")
    return out


def test_parameter_file_keys_exist():
    import json
    paths = _schema_paths(json.loads((SCHEMAS / "bst-1" / "parameters.schema.json").read_text(encoding="utf-8")))
    named = [r["written_as"]["parameter-file"] for _, r in generate.rows(SOURCE) if "parameter-file" in r.get("written_as", {})]
    assert named and all(p in paths for p in named), [p for p in named if p not in paths]


def test_stage_file_identifiers_exist():
    stage = (SCHEMAS / "bst-1" / "bellman" / "buffer_stock.bl").read_text(encoding="utf-8")
    named = [r["written_as"]["bellman-sym"] for _, r in generate.rows(SOURCE) if "bellman-sym" in r.get("written_as", {})]
    missing = []
    for spelling in named:
        parts = spelling.split(".") if not spelling.startswith("E_") else [spelling]
        for part in parts:
            if not (re.search(rf"id={re.escape(part)}\b", stage) or re.search(rf"(?<![\w]){re.escape(part)}(?![\w])", stage)):
                missing.append(spelling)
    assert named and not missing, missing


def test_every_condition_has_a_hark_name_or_says_why_not():
    unnamed = [c["name"] for c in SOURCE["conditions"] if "hark" not in c.get("written_as", {})]
    assert unnamed == [], unnamed
