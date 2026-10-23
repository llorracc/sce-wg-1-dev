"""The checker's tests for bst-markov_ui-and-agg/1 (markov.py), against bst/1's where the family reduces to it:

    uv run --with jsonschema --with pyyaml --with scipy --with numpy --with pytest pytest -q schemas/checker

A bst/1 member written as the Markov family's model schema describes ("A bst/1 member as a member of this family") solves
the same problem, so its conditions, its limits and its tail exponents must be bst/1's.
"""

from __future__ import annotations

import copy
import math
from pathlib import Path

import numpy as np
import pytest

import bst1
import markov
from canonical import load_strict

SCHEMAS = Path(__file__).resolve().parent.parent
MEMBERS = SCHEMAS / "bst-1" / "members"
FAMILY_MEMBERS = SCHEMAS / "bst-markov_ui-and-agg" / "members"


def as_markov(member: dict) -> dict:
    """A bst/1 parameter file's mapping written in the Markov family: one group, the chain unemployment with probability
    wp every quarter whatever the previous state, both incomes while unemployed xi_u, the employed scale bst/1's."""
    wp, xi_u = member["income"]["unemployment"]["prob"], member["income"]["unemployment"]["income"]
    return {"family": "bst-markov_ui-and-agg/1", "period": "quarter", "crra": member["crra"], "splurge": 0.0,
            "survival": member["survival"], "return": member["return"],
            "borrowing_constraint": member["borrowing_constraint"],
            "shocks": {"permanent_shock": member["income"]["permanent_shock"],
                       "employed_shock": member["income"]["employed_shock"]},
            "regimes": {"recession": {"exit_hazard": 1.0}},
            "employment": {"benefit_quarters": 2, "job_finding": {"normal": 1 - wp, "recession": 1 - wp},
                           "income_employed": (1 - wp * xi_u) / (1 - wp), "income_with_benefits": xi_u,
                           "income_without_benefits": xi_u, "unemployed_permanent_income": "continues"},
            "groups": [{"name": "bst1", "share": 1.0, "growth": member["income"]["growth"],
                        "job_loss": {"normal": wp, "recession": wp}, "newborn_income": {"median": 1.0, "sd_log": 0.0},
                        "types": member["types"]}]}


def _toy() -> dict:
    return load_strict((MEMBERS / "toy.yaml").read_text())


@pytest.mark.parametrize("name", ["toy", "toy-untruncated"])
def test_the_reduction_to_bst1_gives_bst1_s_conditions(name):
    data = load_strict((MEMBERS / f"{name}.yaml").read_text())
    stated, family = bst1.Member(data), markov.MarkovMember(as_markov(data))
    group = family.groups[0]
    for t in data["types"]:
        mine = {c["name"]: c for c in stated.conditions(t["beta"])["conditions"]}
        theirs = {c["name"]: c for c in family.factors(group, t["beta"])}
        for c in ["AIC", "RIC", "FHWC", "PF-FVAC", "FVAC", "GIC-Szeidl", "GIC-Liv"]:
            assert theirs[c]["margin"] == pytest.approx(mine[c]["margin"], abs=1e-14), (c, t["beta"])
        for c in ["WRIC", "GIC", "GIC-Mod"]:
            for entry in theirs[c]["by_state"]:
                assert entry["margin"] == pytest.approx(mine[c]["margin"], abs=1e-14), (c, entry["state"], t["beta"])


@pytest.mark.parametrize("name", ["toy", "toy-untruncated"])
def test_the_reduction_to_bst1_gives_bst1_s_limits_and_tail(name):
    data = load_strict((MEMBERS / f"{name}.yaml").read_text())
    stated, family = bst1.Member(data), markov.MarkovMember(as_markov(data))
    group = family.groups[0]
    beta = data["types"][len(data["types"]) // 2]["beta"]
    imp = family.implications(group, beta)
    for j in markov.STATES:
        assert imp["natural_limits"][j] == pytest.approx(stated.natural_borrowing_constraint(), abs=1e-12)
        assert imp["constraint_in_force"][j] == pytest.approx(stated.a_art, abs=1e-12)
    domain = stated.report()["types"][len(data["types"]) // 2]["domain"]
    assert imp["population_tail_exponent"] == pytest.approx(domain["population_tail_exponent"], rel=1e-10)
    assert sum(imp["employment_marginal"].values()) == pytest.approx(1.0, abs=1e-12)


def test_lognormal_laws_give_a_zero_limit_in_every_state():
    data = as_markov(load_strict((MEMBERS / "toy-untruncated.yaml").read_text()))
    for switch in markov.SWITCHES:
        data["employment"]["unemployed_permanent_income"] = switch
        family = markov.MarkovMember(data)
        assert np.all(family.groups[0].limits(None) == 0.0), switch


def test_the_artificial_limit_sits_inside_the_recursion():
    # With truncated laws and a low income without benefits, X's own term is the larger, so its natural limit lies above
    # the employed state's. An artificial limit between the two binds in E; the limits are the recursion's fixed point
    # with the artificial limit inside, and none lies below max(a_Art, a_Nat(j))
    data = as_markov(_toy())
    data["employment"]["income_with_benefits"] = 0.15
    data["employment"]["income_without_benefits"] = 0.05
    data["employment"]["income_employed"] = 1.0
    data["employment"]["job_finding"] = {"normal": 0.5, "recession": 0.25}
    data["groups"][0]["job_loss"] = {"normal": 0.05, "recession": 0.07}
    data["borrowing_constraint"] = "natural"
    group = markov.MarkovMember(data).groups[0]
    natural = group.limits(None)
    assert natural[3] > natural[0]
    a_art = 0.5 * (natural[0] + natural[3])
    inside = group.limits(a_art)
    assert inside[0] == pytest.approx(a_art, abs=1e-14)
    assert np.all(inside >= np.maximum(a_art, natural) - 1e-15)
    terms = group.growth * group.psi_min() / data["return"] * (inside - group.xi_min())
    for j in range(4):
        assert inside[j] == pytest.approx(max(a_art, max(terms[group.P[j] > 0])), abs=1e-14), j


def test_frozen_permanent_income_changes_the_matrix_conditions():
    data = as_markov(_toy())
    beta = data["groups"][0]["types"][3]["beta"]
    margins = {}
    for switch in markov.SWITCHES:
        data["employment"]["unemployed_permanent_income"] = switch
        family = markov.MarkovMember(copy.deepcopy(data))
        margins[switch] = {c["name"]: c for c in family.factors(family.groups[0], beta)}
    # under frozen the unemployed states' growth is one, which lowers the human-wealth factor below continues'
    assert margins["frozen"]["FHWC"]["factor"] < margins["continues"]["FHWC"]["factor"]
    # grows fixes psi at one when unemployed, which removes its spread from the FVAC
    assert margins["grows"]["FVAC"]["factor"] != margins["continues"]["FVAC"]["factor"]


@pytest.mark.parametrize("change, problem", [
    (lambda d: d.update(borrowing_constraint=-5.0), "below the lowest natural limit"),
    (lambda d: d["employment"].update(benefit_quarters=3), "benefit_quarters"),
    (lambda d: d["groups"][0].update(share=0.9), "shares do not sum"),
    (lambda d: d["groups"][0]["types"].reverse(), "beta must increase"),
])
def test_member_rules(change, problem):
    data = as_markov(_toy())
    change(data)
    with pytest.raises(markov.MarkovMemberError, match=problem):
        markov.MarkovMember(data)


def test_the_employment_marginal_is_the_chain_s_with_newborns_employed():
    data = as_markov(_toy())
    group = markov.MarkovMember(data).groups[0]
    mu = group.employment_marginal()
    L, P = data["survival"], group.P
    assert mu @ (L * P) + (1 - L) * np.eye(4)[0] == pytest.approx(mu, abs=1e-14)
    assert not math.isclose(mu[0], markov.stationary(P)[0], abs_tol=1e-6)


@pytest.mark.parametrize("name", ["toy-as-hafiscal", "paper-one-group", "paper-published"])
def test_the_filed_members_are_valid(name):
    member = markov.load_member(FAMILY_MEMBERS / f"{name}.yaml")
    assert len(member.hash) == 64
    for g in member.groups:
        assert np.all(g.limits(member.a_art_value()) == 0.0), g.name   # a_Art = 0 under lognormal laws: no effect


def test_toy_as_hafiscal_is_the_toy_written_in_the_family():
    filed = load_strict((FAMILY_MEMBERS / "toy-as-hafiscal.yaml").read_text())
    written = as_markov(_toy())
    written["groups"][0]["name"] = "toy"
    numbers, words = leaves(filed), leaves(written)
    assert {k: v for k, v in numbers.items() if isinstance(v, float)} == pytest.approx(
        {k: v for k, v in words.items() if isinstance(v, float)}, abs=1e-15)
    assert {k: v for k, v in numbers.items() if isinstance(v, str)} == {k: v for k, v in words.items() if isinstance(v, str)}


def leaves(data, prefix=""):
    """Every leaf of a mapping by its path, numbers as floats."""
    out = {}
    if isinstance(data, dict):
        for k, v in data.items():
            out.update(leaves(v, f"{prefix}/{k}"))
    elif isinstance(data, list):
        for i, v in enumerate(data):
            out.update(leaves(v, f"{prefix}[{i}]"))
    else:
        out[prefix] = float(data) if isinstance(data, (int, float)) and not isinstance(data, bool) else data
    return out


@pytest.mark.parametrize("change, problem", [
    (lambda d: d["groups"][0]["newborn_income"].update(mean=1.0), "newborn_income"),
    (lambda d: d["employment"]["job_finding"].update(normal=0.0), "job_finding"),
    (lambda d: d["employment"].update(unemployed_permanent_income="stays"), "unemployed_permanent_income"),
    (lambda d: d.update(splurge=1.0), "splurge"),
])
def test_the_validator_refuses(change, problem):
    data = load_strict((FAMILY_MEMBERS / "paper-one-group.yaml").read_text())
    change(data)
    with pytest.raises(markov.MarkovMemberError, match=problem):
        markov.MarkovMember(data)


@pytest.mark.parametrize("world", markov.SWITCHES)
def test_the_dropout_calibrations_are_paper_published_s_middle_type(world):
    # The Bellman calibrations state one type of one group in the stage file's names; their numbers must be the member's
    import yaml

    calibration = yaml.safe_load((SCHEMAS / "bst-markov_ui-and-agg" / "bellman"
                                  / f"hafiscal-dropout-middle-type-{world}.yml").read_text(encoding="utf-8"))["calibration"]
    data = load_strict((FAMILY_MEMBERS / "paper-published.yaml").read_text())
    group = next(g for g in data["groups"] if g["name"] == "dropout")
    employment, laws = data["employment"], data["shocks"]
    expected = {"β": group["types"][3]["beta"], "ℒ": data["survival"], "ϱ": data["crra"], "R": data["return"],
                "𝒢": group["growth"], "a_Art": data["borrowing_constraint"], "a_Nat": 0.0,
                "σ_ψ": laws["permanent_shock"]["LogNormal"]["sd_log"], "σ_θ": laws["employed_shock"]["LogNormal"]["sd_log"],
                "e": employment["income_employed"], "ξ_u": employment["income_with_benefits"],
                "ξ_x": employment["income_without_benefits"], "P_u": world,
                "p_exit": data["regimes"]["recession"]["exit_hazard"], "sep_n": group["job_loss"]["normal"],
                "sep_r": group["job_loss"]["recession"], "find_n": employment["job_finding"]["normal"],
                "find_r": employment["job_finding"]["recession"]}
    assert calibration == expected
