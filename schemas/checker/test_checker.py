"""Tests for the checker: the laws' closed forms against numerical integration, the members, and the rejections.

    uv run --with jsonschema --with pyyaml --with scipy --with pytest pytest -q schemas/checker
"""

from __future__ import annotations

import copy
import math
from pathlib import Path

import pytest
from scipy.integrate import quad
from scipy.special import ndtr, ndtri

from bst1 import CASE_ATOM, CASE_BINDING, Member, MemberError, load_member, validate_results, verdict
from canonical import StrictYAMLError, load_strict, model_hash
from laws import law_from_mapping
from test_results_schema import sample as schema_sample

MEMBERS = Path(__file__).resolve().parent.parent / "bst-1" / "members"


def numerical(law, f):
    """E[f(X)] by quadrature, from a quantile function or a density built outside the law's own code."""
    name = law.name
    p = law.params
    if name in ("LogNormal", "TruncatedLogNormal"):
        n = law.normal
        lo, hi = ndtr(n.bot), ndtr(n.top)
        return quad(lambda u: f(math.exp(n.location + n.scale * ndtri(lo + u * (hi - lo)))), 0, 1,
                    limit=200, epsabs=1e-13, epsrel=1e-12)[0]
    if name == "Uniform":
        w = p["half_width"]
        return quad(lambda x: f(x) / (2 * w), 1 - w, 1 + w, epsabs=1e-13, epsrel=1e-12)[0]
    if name == "NormalMixture":
        total = 0.0
        for w, n in zip(law.weights, law.normals):
            lo, hi = n.lower(), n.upper()
            lo = n.location - 12 * n.scale if math.isinf(lo) else lo
            hi = n.location + 12 * n.scale if math.isinf(hi) else hi
            density = lambda x, n=n: math.exp(-0.5 * ((x - n.location) / n.scale) ** 2) / (
                n.scale * math.sqrt(2 * math.pi) * n.mass)
            total += w * quad(lambda x: f(math.exp(law.shift + x)) * density(x), lo, hi, limit=200,
                              epsabs=1e-13, epsrel=1e-12)[0]
        return total
    if name == "Tabulated":
        us = [u for u, _ in law.points]
        qs = [q for _, q in law.points]

        def Q(u):
            for (u0, q0), (u1, q1) in zip(law.points, law.points[1:]):
                if u0 <= u <= u1 and u1 > u0:
                    return q0 + (q1 - q0) * (u - u0) / (u1 - u0)
            return qs[-1]

        return quad(lambda u: f(Q(u)), 0, 1, points=sorted(set(us))[1:-1], limit=200, epsabs=1e-13)[0]
    raise NotImplementedError(name)


LAWS = [
    {"LogNormal": {"sd_log": 0.3}},
    {"TruncatedLogNormal": {"sd_log": 0.2, "bot": -2.0, "top": 2.0}},
    {"TruncatedLogNormal": {"sd_log": 0.4, "bot": -3.0}},
    {"TruncatedLogNormal": {"sd_log": 0.1, "top": 1.5}},
    {"Uniform": {"half_width": 0.4}},
    {"NormalMixture": {"components": [
        {"weight": 0.1, "mean_log": -0.9, "sd_log": 0.30, "bot": -3.0, "top": 3.0},
        {"weight": 0.9, "mean_log": 0.1, "sd_log": 0.05, "bot": -3.0, "top": 3.0}]}},
    {"NormalMixture": {"components": [
        {"weight": 0.5, "mean_log": -0.2, "sd_log": 0.2},
        {"weight": 0.5, "mean_log": 0.2, "sd_log": 0.1, "top": 2.0}]}},
    {"Tabulated": {"points": [[0.0, 0.5], [0.1, 0.5], [0.5, 1.0], [1.0, 1.6]]}},
    {"Tabulated": {"points": [[0.0, 0.5], [0.4, 0.75], [0.4, 1.1], [1.0, 1.4]]}},
]


@pytest.mark.parametrize("mapping", LAWS, ids=[next(iter(m)) + str(i) for i, m in enumerate(LAWS)])
def test_closed_forms_match_quadrature(mapping):
    law = law_from_mapping(mapping)
    assert law.check() == []
    assert law.moment(1.0) == pytest.approx(1.0, abs=1e-12)
    for k in (-1.0, -0.5, 0.5, 2.0, 3.0):
        assert law.moment(k) == pytest.approx(numerical(law, lambda x: x ** k), rel=1e-8)
    assert law.mean_log == pytest.approx(numerical(law, math.log), abs=1e-9)
    assert law.mean_x_log_x == pytest.approx(numerical(law, lambda x: x * math.log(x)), abs=1e-9)


def test_truncated_lognormal_keeps_the_stated_standard_deviation():
    law = law_from_mapping({"TruncatedLogNormal": {"sd_log": 0.25, "bot": -2.0, "top": 2.0}})
    variance = numerical(law, lambda x: (math.log(x) - law.mean_log) ** 2)
    assert math.sqrt(variance) == pytest.approx(0.25, rel=1e-9)
    assert law.normal.scale == pytest.approx(0.25 * 1.1368472343385565, rel=1e-9)


def test_mixture_components_have_the_stated_means_after_truncation():
    law = law_from_mapping(LAWS[5])
    for n, c in zip(law.normals, law.params["components"]):
        assert n.mean() == pytest.approx(c["mean_log"], abs=1e-12)


@pytest.mark.parametrize("mapping, problem", [
    ({"LogNormal": {"sd_log": 0.0}}, "sd_log"),
    ({"TruncatedLogNormal": {"sd_log": 0.1, "bot": 1.0, "top": -1.0}}, "bot must be below top"),
    ({"Uniform": {"half_width": 1.0}}, "half_width"),
    ({"Discrete": {"values": [0.8, 1.3], "probs": [0.5, 0.5]}}, "mean"),
    ({"Discrete": {"values": [1.2, 0.8], "probs": [0.5, 0.5]}}, "increasing"),
    ({"NormalMixture": {"components": [
        {"weight": 0.5, "mean_log": 0.1, "sd_log": 0.2}, {"weight": 0.5, "mean_log": -0.1, "sd_log": 0.2}]}}, "order"),
    ({"Tabulated": {"points": [[0.0, 0.5], [0.5, 1.0], [1.0, 1.5]]}}, "line through its neighbors"),
    ({"Tabulated": {"points": [[0.0, 0.5], [0.1, 0.5], [0.5, 1.0], [1.0, 1.7]]}}, "mean"),
    ({"Tabulated": {"points": [[0.0, 0.5], [0.0, 0.6], [0.5, 1.0], [1.0, 1.6]]}}, "repeated"),
])
def test_law_rules(mapping, problem):
    assert any(problem in p for p in law_from_mapping(mapping).check())


def test_members_load_and_report():
    for name in ("library", "toy", "toy-untruncated"):
        member = load_member(MEMBERS / f"{name}.yaml")
        report = member.report()
        assert report["valid"], name
        assert len(report["hash"]) == 64
        for t in report["types"]:
            assert t["domain"]["buffer_stock_target"], (name, t["beta"])


def test_library_member_is_the_no_mortality_case():
    report = load_member(MEMBERS / "library.yaml").report()
    t = report["types"][0]
    names = {c["name"]: c for c in t["conditions"]}
    assert names["GIC-Szeidl"]["holds"] and names["GIC-Harmenberg"]["holds"]
    assert t["domain"]["population_measure"] and t["domain"]["income_measure"]
    assert report["implications"]["worst_income_probability"] == pytest.approx(0.005)
    assert report["implications"]["natural_borrowing_constraint"] == 0.0
    assert not t["domain"]["kink"]
    # The zero-income event: E[v] needs wp^(1/rho) L (G/thorn)^(rho-1) E[psi^(rho-1)] < 1, which holds; E[u'(c)] needs
    # (G/thorn)^rho E[psi^rho] < 1, which the GIC defeats.
    w = t["welfare"]
    assert w["welfare_factor"] == pytest.approx(0.005 ** 0.5 * (1.03 / t["thorn"]) * 1.0, rel=1e-9)
    assert w["welfare_finite"] and t["domain"]["welfare"]
    assert w["marginal_factor"] == pytest.approx((1.03 / t["thorn"]) ** 2 * math.exp(0.01), rel=1e-9)
    assert not w["marginal_finite"] and not t["domain"]["marginal_welfare"]
    # With L = 1 the tail exponents solve (thorn/G)^z E[psi^-z] = 1 and (thorn/G)^j E[psi^(1-j)] = 1; for a lognormal
    # psi the first is 2 log(G/thorn)/sigma^2 - 1, and the GIC makes the income-weighted mean finite.
    sigma2 = 0.01
    expected = 2 * math.log(1.03 / t["thorn"]) / sigma2 - 1
    assert t["domain"]["population_tail_exponent"] == pytest.approx(expected, rel=1e-6)
    assert t["domain"]["income_tail_exponent"] > 1 and t["domain"]["income_mean"]


def test_toy_member_conditions():
    report = load_member(MEMBERS / "toy.yaml").report()
    assert report["implications"]["worst_income_probability"] == 0.0
    assert report["implications"]["natural_borrowing_constraint"] < 0.0
    assert report["implications"]["newborn_min_resources"] > 0.0
    for t in report["types"]:
        assert t["domain"]["kink"]
        assert t["domain"]["welfare"] and t["domain"]["marginal_welfare"]
        assert t["welfare"]["welfare_case"] == "the artificial constraint binds"
        assert t["domain"]["population_measure"]
        assert t["domain"]["population_tail_exponent"] is None or t["domain"]["population_tail_exponent"] > 2


def test_lower_tail_cases_without_an_artificial_constraint():
    # The toy under the natural constraint alone: both laws truncated, so a positive density at the floor in two shocks;
    # E[v] (q = 1) is finite and E[u'(c)] (q = 2) is not at rho = 2.
    toy = load_strict((MEMBERS / "toy.yaml").read_text())
    toy["borrowing_constraint"] = "natural"
    t = Member(toy).report()["types"][0]
    assert t["welfare"]["welfare_case"].endswith("2 shock(s)")
    assert t["domain"]["welfare"] and not t["domain"]["marginal_welfare"]
    # The stationary tail's exponent is max(n, rho): with n = 2 the marginal mean is finite for rho < 2 and the value's mean
    # for every rho.
    toy["crra"] = 1.5
    t = Member(toy).report()["types"][0]
    assert t["domain"]["welfare"] and t["domain"]["marginal_welfare"]
    toy["crra"] = 3.0
    t = Member(toy).report()["types"][0]
    assert t["domain"]["welfare"] and not t["domain"]["marginal_welfare"]
    # The untruncated toy: a lognormal at zero is thin, so every moment is finite.
    t = load_member(MEMBERS / "toy-untruncated.yaml").report()["types"][0]
    assert not t["domain"]["kink"]
    assert t["welfare"]["welfare_case"] == "a thin density at the floor"
    assert t["domain"]["welfare"] and t["domain"]["marginal_welfare"]


def test_hash_ignores_the_written_form_of_a_number():
    a = load_strict((MEMBERS / "library.yaml").read_text())
    b = copy.deepcopy(a)
    b["return"] = 1.040
    b["types"][0]["share"] = 1
    assert model_hash(a) == model_hash(b)
    b["return"] = 1.041
    assert model_hash(a) != model_hash(b)


@pytest.mark.parametrize("text, problem", [
    ("a: &x 1\nb: *x\n", "anchor"),
    ("a: 1\na: 2\n", "repeated key"),
    ("a: !!float 1\n", "tag"),
    ("a: .inf\n", "infinite"),
    ("a: true\n", "boolean"),
])
def test_strict_yaml(text, problem):
    with pytest.raises(StrictYAMLError, match=problem):
        load_strict(text)


def _library():
    return load_strict((MEMBERS / "library.yaml").read_text())


@pytest.mark.parametrize("change, problem", [
    (lambda d: d["types"].append({"beta": 0.95, "share": 0.5}), "increasing"),
    (lambda d: d["types"][0].update(share=0.9), "shares sum"),
    (lambda d: d["income"]["unemployment"].update(prob=0.0, income=0.5), "with prob 0"),
    (lambda d: d.update(borrowing_constraint=0.5), "borrowing_constraint"),
    (lambda d: d.update(borrowing_constraint=-0.5), "below the natural constraint"),
    (lambda d: d.update(crra=0.5), "crra"),
    (lambda d: d.update(crra=1.0), "crra"),
    (lambda d: d["income"].update(permanent_shock={"Formula": {"defines": "quantile", "language": "infix",
                                                             "expression": "1"}}), "permanent_shock"),
    (lambda d: d.update(extra=1), "extra"),
])
def test_member_rules(change, problem):
    data = _library()
    change(data)
    with pytest.raises(MemberError, match=problem):
        Member(data)


def test_natural_keyword_resolves_to_the_natural_constraint():
    data = _library()
    data["borrowing_constraint"] = "natural"
    member = Member(data)
    assert member.a_art == 0.0
    toy = load_strict((MEMBERS / "toy.yaml").read_text())
    toy["borrowing_constraint"] = "natural"
    member = Member(toy)
    assert member.a_art == pytest.approx(member.natural_borrowing_constraint())
    assert not member.report()["types"][0]["domain"]["kink"]


def test_bellman_calibration_matches_the_filed_one():
    import yaml

    member = load_member(MEMBERS / "library.yaml")
    filed = yaml.safe_load((MEMBERS.parent / "bellman" / "community-library.yml").read_text())["calibration"]
    written = member.bellman_calibration(0)
    assert set(written) == set(filed)
    for key, value in filed.items():
        assert written[key] == pytest.approx(value), key
    assert "calibration:" in member.bellman_calibration_yaml(0)
    with pytest.raises(ValueError, match="no Bellman-SYM family"):
        load_member(MEMBERS / "toy.yaml").bellman_calibration(0)
    untruncated = load_member(MEMBERS / "toy-untruncated.yaml").bellman_calibration(6)
    assert untruncated["β"] == 0.990 and untruncated["a_Nat"] == 0.0 and untruncated["μ"] == 0.7


def _consistent_results(member: Member) -> dict:
    """A results file whose effective member coincides with the stated member: the stated values, reported as a toolkit
    would report its own, with the statuses that its own verdicts imply."""
    data = schema_sample()
    data["parameter_file_sha256"] = member.hash
    data["effective_member"] = {"expectations": member.expectations(), "lowest": member.lowest(),
                                "derived": member.derived()}
    c = member.conditions(member.types[0]["beta"])
    block = {x["name"]: {"factor": x["factor"], "bound": x["bound"], "holds": x["holds"]} for x in c["conditions"]}
    w = c["welfare"]
    block["welfare"] = {"case": w["welfare_case"], "factor": w["welfare_factor"], "holds": w["welfare_finite"]}
    block["marginal_welfare"] = {"case": w["marginal_case"], "factor": w["marginal_factor"],
                                 "holds": w["marginal_finite"]}
    t = data["types"][0]
    t["beta"] = member.types[0]["beta"]
    t["conditions"] = block
    d = c["domain"]
    t["kink"] = {"status": "value", "m": 0.4, "slope_below": 1.0, "slope_above": 0.9} if d["kink"] else {"status": "undefined"}
    for key, defined in (("target", d["buffer_stock_target"]), ("pseudo_target", d["pseudo_target"])):
        t[key] = {"status": "value", "m": 1.3, "c": 1.0, "mpc": 0.1} if defined else {"status": "undefined"}
    if not d["income_measure"]:
        t["income_measure"] = {"status": "undefined"}
    if not d["welfare"]:
        t["welfare"] = {"status": "undefined"}
    if d["marginal_welfare"]:
        t["marginal_welfare"] = {"status": "value", "mean": 1.0, "by_a_quartile": [2.0, 1.0, 0.7, 0.4],
                                 "at_constraint": None, "undefined": ["at_constraint"]}
    return data


def test_a_consistent_report_verifies():
    member = load_member(MEMBERS / "library.yaml")
    data = _consistent_results(member)
    assert validate_results(data) == []
    assert member.verify_results(data) == []
    # The library member's kink is undefined, its target defined and its marginal welfare undefined, by its own verdicts.
    t = data["types"][0]
    assert t["kink"]["status"] == "undefined" and t["target"]["status"] == "value"
    assert t["marginal_welfare"]["status"] == "undefined"
    assert t["conditions"]["welfare"]["case"] == CASE_ATOM


@pytest.mark.parametrize("change, problem", [
    (lambda d: d["types"][0]["conditions"]["FVAC"].update(factor=d["types"][0]["conditions"]["FVAC"]["factor"] * 1.1),
     "FVAC/factor"),
    (lambda d: d["types"][0]["conditions"]["GIC-Mod"].update(holds=False), "GIC-Mod/holds"),
    (lambda d: d["types"][0]["target"].update(status="undefined"), "target/status"),
    (lambda d: d["types"][0]["kink"].update(status="value", m=0.4, slope_below=1.0, slope_above=0.9), "kink/status"),
    (lambda d: d["effective_member"]["derived"].update(natural_limit=-0.1), "natural_limit"),
    (lambda d: d["effective_member"]["expectations"].update(psi_inverse=0.9), "psi_inverse"),
    (lambda d: d["types"][0]["conditions"]["welfare"].update(case=CASE_BINDING), "welfare/case"),
    (lambda d: d.update(parameter_file_sha256="1" * 64), "sha256"),
])
def test_an_inconsistent_report_is_caught(change, problem):
    member = load_member(MEMBERS / "library.yaml")
    data = _consistent_results(member)
    change(data)
    assert validate_results(data) == []
    problems = member.verify_results(data)
    assert any(problem in p for p in problems), problems


def test_the_population_block_decides_the_population_conditions():
    # The library member has L = 1, so the GIC-Szeidl decides whether the stationary population exists. A population
    # block whose E[log psi] is far below the household's flips that verdict, and the toolkit's report must follow it.
    member = load_member(MEMBERS / "library.yaml")
    data = _consistent_results(member)
    population = {"expectations": dict(member.expectations(), psi_log=-1.0), "lowest": member.lowest()}
    data["effective_member"]["population"] = population
    assert validate_results(data) == []
    # A report still decided on the household's law is caught at the condition's bound.
    stale = member.verify_results(data)
    assert any("GIC-Szeidl/bound" in p for p in stale), stale
    t = data["types"][0]
    szeidl = t["conditions"]["GIC-Szeidl"]
    szeidl.update(bound=-1.0, holds=szeidl["factor"] < -1.0)
    assert not szeidl["holds"]
    # With the verdict corrected, the statuses that follow from it must follow.
    stale = member.verify_results(data)
    assert any("welfare/status" in p for p in stale), stale
    t["welfare"] = {"status": "undefined"}
    t["marginal_welfare"] = {"status": "undefined", "by_a_quartile": [None] * 4, "at_constraint": None,
                             "undefined": ["mean", "by_a_quartile", "at_constraint"]}
    assert member.verify_results(data) == []
    # The population block's lowest values are held to the stated infima as well.
    data["effective_member"]["population"]["lowest"] = {"psi": member.lowest()["psi"], "income": -0.0}
    assert validate_results(data) == []
    assert member.verify_results(data) == []


def test_a_toolkit_lowest_value_below_the_infimum_is_caught():
    member = load_member(MEMBERS / "toy.yaml")
    low = member.lowest()
    assert low["psi"] > 0 and low["income"] > 0
    # A representation's lowest value lies at or above the law's infimum, which is the limit of those values.
    problems = member.verify_results({
        "family": "bst/1", "parameter_file_sha256": member.hash,
        "effective_member": {"expectations": member.expectations(), "lowest": {"psi": low["psi"] * 0.5, "income": low["income"]},
                             "derived": member.derived()},
        "types": [],
    })
    assert any("lowest/psi" in p and "below the stated infimum" in p for p in problems)


def test_verdicts_name_the_undecided_margin():
    assert verdict(0.1) == "holds" and verdict(-0.1) == "fails" and verdict(1e-14) == "undecided"
    report = load_member(MEMBERS / "library.yaml").report()
    assert report["member"] == "stated"
    assert all(c["verdict"] in ("holds", "fails") for c in report["types"][0]["conditions"])


def test_welfare_condition_fails_for_an_impatient_zero_income_member():
    # Valid (FVAC and WRIC hold) but so impatient, with so likely a zero-income event, that E[v] = -inf.
    data = _library()
    data["crra"] = 5.0
    data["types"] = [{"beta": 0.5, "share": 1.0}]
    data["income"]["unemployment"] = {"prob": 0.5, "income": 0.0}
    report = Member(data).report()
    t = report["types"][0]
    assert t["valid"]
    assert not t["domain"]["welfare"]
    assert not report["pooled_domain"]["welfare"]
