"""The checker's tests for bst-markov_ui-and-agg/1 (markov.py), against bst/1's where the family reduces to it:

    uv run --with jsonschema --with pyyaml --with scipy --with numpy --with pytest pytest -q schemas/checker

A bst/1 member written as the Markov family's model schema describes ("A bst/1 member as a member of this family")
solves the same problem, so its conditions, its limits and its tail exponents must be bst/1's.
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
    assert ({k: v for k, v in numbers.items() if isinstance(v, str)}
            == {k: v for k, v in words.items() if isinstance(v, str)})


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

    folder = SCHEMAS / "bst-markov_ui-and-agg" / "bellman"
    text = (folder / f"hafiscal-dropout-middle-type-{world}.yml").read_text(encoding="utf-8")
    calibration = yaml.safe_load(text)["calibration"]
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


def consistent_results(member: markov.MarkovMember) -> dict:
    """A results file whose effective member is the stated member: the stated values, reported as a toolkit would report
    its own, with made-up but coherent statistics for the rest."""
    probs = ["0.01", "0.05", "0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9", "0.95", "0.99", "0.999",
             "1"]
    points = [0.5, 1.0, 2.0]
    x = 0.2                                             # a made-up mean MPC, and the paper's MPC of a population at it
    mpc = {"mean": float(markov.paper_mpc(x, member.splurge)), "mean_mpc": x}
    groups = []
    for g in member.groups:
        E = g.expectations()
        natural, in_force = g.limits(None), g.limits(member.a_art_value())
        by_state = {s: {k: float(E[k][j]) for k in markov.STATE_KEYS} for j, s in enumerate(markov.STATES)}
        types = []
        for t in g.types:
            conditions = {}
            for c in member.factors(g, t["beta"]):
                if c["name"] == "GIC-Harmenberg":
                    conditions[c["name"]] = {"status": "not computed"}
                elif "by_state" in c:
                    conditions[c["name"]] = {"by_state": {e["state"]: {k: e[k] for k in ("factor", "bound", "holds")}
                                                          for e in c["by_state"]}}
                else:
                    conditions[c["name"]] = {k: c[k] for k in ("factor", "bound", "holds")}
            mu = g.employment_marginal()
            types.append({
                "beta": t["beta"], "share": t["share"], "conditions": conditions, "comparison_points": points,
                "rule": {s: {"m": points + [0.1], "c": [0.4, 0.7, 1.1, 0.1], "mpc": [0.5, 0.3, 0.2, 1.0]}
                         for s in markov.STATES},
                "exported_rule": {s: {"m": [0.1, 1.0], "c": [0.1, 0.7], "range": [0.1, 1.0]} for s in markov.STATES},
                "employment_shares": {s: float(mu[j]) for j, s in enumerate(markov.STATES)},
                "wealth": {"gl": {p: 0.1 * float(p) for p in probs}, "median": 0.4},
                "paper_mpc": mpc,
                "euler_residuals": {"by_state": {s: {"r": [1e-6, -1e-6, 0.0], "max_abs": 1e-6} for s in markov.STATES},
                                    "max_abs": 1e-6, "expectation_method": "gauss-legendre", "expectation_precision": 1e-9},
                "stationarity_residual": 1e-9})
        groups.append({
            "name": g.name,
            "effective_member": {
                "chain": {"normal": g.P.tolist(),
                          "recession": markov.chain(g.sep["recession"], member.find["recession"]).tolist()},
                "by_state": by_state, "theta_mean": float(member.theta.moment(1.0)),
                "derived": {"natural_limit": {s: (None if math.isinf(natural[j]) else float(natural[j]))
                                              for j, s in enumerate(markov.STATES)},
                            "constraint_in_force": {s: float(in_force[j]) for j, s in enumerate(markov.STATES)},
                            "worst_income": {s: float(E["psi_lowest"][j] * E["income_lowest"][j])
                                             for j, s in enumerate(markov.STATES)}}},
            "types": types,
            "levels": {"gl": {"0.2": 0.1, "0.4": 0.8, "0.6": 2.5, "0.8": 6.0, "1": 14.0}, "median_ratio": 0.4,
                       "paper_mpc": mpc}})
    return {"family": "bst-markov_ui-and-agg/1", "parameter_file_sha256": member.hash, "method_file_sha256": "0" * 64,
            "settings_sha256": "0" * 64, "request_file_sha256": "0" * 64,
            "toolkit": {"name": "test", "version": "0"}, "provenance": {"hardware": "test", "threads": 1},
            "groups": groups,
            "pooled": {"levels": {"gl": {"0.25": 0.2, "0.5": 1.5, "0.75": 4.0, "1": 14.0}, "paper_mpc": mpc,
                                  "paper_mpc_by_quartile": [mpc, mpc, mpc, mpc]}}}


@pytest.mark.parametrize("name", ["toy-as-hafiscal", "paper-one-group", "paper-published"])
def test_a_consistent_report_validates_and_verifies(name):
    member = markov.load_member(FAMILY_MEMBERS / f"{name}.yaml")
    results = consistent_results(member)
    assert markov.validate_results(results) == []
    assert member.verify_results(results) == []


def _first_type(d):
    return d["groups"][0]["types"][0]


@pytest.mark.parametrize("change, problem", [
    (lambda d: d.update(parameter_file_sha256="1" * 64), "parameter_file_sha256"),
    (lambda d: d["groups"][0]["effective_member"]["chain"]["normal"][0].__setitem__(0, 0.5), "chain/normal"),
    (lambda d: d["groups"][0]["effective_member"]["derived"]["constraint_in_force"].update(E=-1.0),
     "constraint_in_force/E"),
    (lambda d: _first_type(d)["conditions"]["FVAC"].update(factor=0.5), "FVAC/factor"),
    (lambda d: _first_type(d)["conditions"]["GIC-Mod"]["by_state"]["X"].update(holds=False), "GIC-Mod/X/holds"),
    (lambda d: _first_type(d)["employment_shares"].update(E=0.9), "employment_shares/E"),
    (lambda d: _first_type(d)["paper_mpc"].update(mean=0.99), "paper_mpc/mean"),
    (lambda d: _first_type(d)["rule"]["U_1"].update(m=[9.0, 9.1, 9.2, 9.3]), "rule/U_1/m"),
    (lambda d: d["groups"][0]["levels"]["gl"].update({"1": None}), "levels/gl/1"),
])
def test_an_inconsistent_report_is_caught(change, problem):
    member = markov.load_member(FAMILY_MEMBERS / "paper-one-group.yaml")
    results = consistent_results(member)
    change(results)
    assert markov.validate_results(results) == []
    found = member.verify_results(results)
    assert any(problem in p for p in found), found


def test_a_representation_s_bottom_nodes_are_not_its_lowest_values():
    # A toolkit that reports its lowest nodes, above the truncated laws' infima, in place of the infima its
    # representation carries, is caught: its natural limits would then move with the number of nodes
    member = markov.load_member(FAMILY_MEMBERS / "toy-as-hafiscal.yaml")
    results = consistent_results(member)
    eff = results["groups"][0]["effective_member"]
    for s in markov.STATES:
        eff["by_state"][s]["psi_lowest"] *= 1.05
    found = member.verify_results(results)
    assert any("psi_lowest" in p and "laws'" in p for p in found), found
    assert any("natural_limit" in p for p in found), found
